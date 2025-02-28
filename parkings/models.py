from django.db import models
from shapely import Point
from rest_framework.exceptions import ValidationError
from . utils import validate_polygon

class Parking(models.Model):
    name = models.CharField(max_length=255)
    area = models.JSONField() 
    capacity = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

        
    def contains_point(self, lon, lat):
        """Checks if a given point (longitude, latitude) is within the parking area"""
        polygon =  self.get_polygon_from_area()
        point = Point(lon, lat)
        return polygon.contains(point)
    
    def get_polygon_from_area(self):
        """Converts a GeoJSON into a Polygon"""
        return validate_polygon(self.area)
        
    def clean(self):
        polygon = self.get_polygon_from_area()

        boundary = Parking.objects.filter(name="boundary").first()
        
        if boundary is not None and not polygon.within(boundary.get_polygon_from_area()):
            raise ValidationError({"detail": "Parking area cannot exceed outer boundaries"})