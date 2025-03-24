from django.db import models
from rest_framework.exceptions import ValidationError
from shapely import Point, from_geojson, errors


class Parking(models.Model):
    name = models.CharField(max_length=255, unique=True)
    area = models.TextField()
    capacity = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def contains_point(self, lon, lat):
        """Checks if a given point (longitude, latitude) is within the parking area"""
        polygon = self.get_polygon_from_area()
        point = Point(lon, lat)
        return polygon.contains(point)

    def get_polygon_from_area(self):
        """Converts a GeoJSON into a Polygon"""
        try:
            geom = from_geojson(self.area, on_invalid="raise")
        except errors.GEOSException as exc:
            raise ValidationError({"detail": f"Parking area is invalid: {exc}"})

        if geom.geom_type not in {"Polygon", "MultiPolygon"}:
            raise ValidationError("Parking area must be a Polygon or MultiPolygon type")

        return geom

    def clean(self):
        if self.capacity <= 0:
            raise ValidationError({"detail": "Capacity must be greater than zero."})

        if Parking.objects.filter(name=self.name).exclude(id=self.id).exists():
            raise ValidationError({"detail": "Parking with this name already exists."})

        polygon = self.get_polygon_from_area()

        # Outer boundary eg. city
        boundary = Parking.objects.filter(name="boundary").first()

        if boundary and not polygon.within(boundary.get_polygon_from_area()):
            raise ValidationError(
                {"detail": "Parking area cannot exceed outer boundary"}
            )
