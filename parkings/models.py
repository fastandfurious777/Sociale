from django.db import models
from shapely import Polygon, Point, from_geojson
from django_rest.exceptions import ValidationError
import json

class Parking(models.Model):
    name = models.CharField(max_length=255)
    area = models.JSONField() 
    capacity = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

        
    def contains_point(self, lon, lat):
        """Checks if a given point (longitude, latitude) is within the parking area"""
        polygon =  self.get_polygon_from_coords()
        point = Point(lon, lat)
        return polygon.contains(point)
    
    def get_polygon_from_coords(self):
        """Converts a GeoJSON into a Polygon"""
        return from_geojson(self.area)
    
    def clean(self):
        if "type" not in self.area or "coordinates" not in self.area:
            raise ValidationError({"area": "Area must be a valid GeoJSON dictionary"})

        if self.area["type"] != "Polygon":
            raise ValidationError({"area": "Only 'Polygon' type is supported"})

        polygon = self.get_polygon_from_coords()

        with open("boundary.json", "r") as file:
            boundary = from_geojson(json.loads(file))
        
        if not polygon.within(boundary):
            raise ValidationError({"area": "Parking area cannot exceed outer boundaries"})