from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from shapely import Point, Polygon
import ast
import uuid

class Bike(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    # Encrypted code for opening the locker
    code = models.TextField()
    is_available = models.BooleanField()
    last_taken_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def clean(self):
        min_lon: float = 19.732238
        max_lon: float = 20.228873
        min_lat: float = 49.946199
        max_lat: float = 50.148339
        if self.lon<min_lon or self.lon>max_lon:
            raise ValidationError({"detail": "Longtitude cannot exceeed Krakow"})
        if self.lat<min_lat or self.lat>max_lat:
            raise ValidationError({"detail":"Latitude cannot exceeed Krakow"})
    
    @classmethod
    def class_name(cls):
        return "Bike"

        
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True,blank=True)

    def clean(self):
        if self.started_at >= self.finished_at:
            raise ValidationError({"detail": "'finished_at' cannot be before 'started_at'"})
    
    @classmethod
    def class_name(cls):
        return "Rental"

class Parking(models.Model):
    name = models.CharField(max_length=100, unique=True)
    coords = models.TextField()
        
    def contains_point(self, lon: float, lat: float) -> bool:
        """Checks if a given point (longitude, latitude) is within the parking area"""
        polygon: Polygon =  self.get_polygon_from_coords()
        point = Point(lon, lat)
        return polygon.contains(point)
    
    def get_polygon_from_coords(self) -> Polygon:
        """Convert a string representation of a list (coords) to a list object"""
        converted_coords: list[tuple[float, float]] = ast.literal_eval(self.coords)
        return Polygon(converted_coords)
    
    def clean(self):
        # Checks if polygon is inside Krakow
        krakow = Polygon([
        (19.934227, 50.151481),
        (20.147812, 50.114320),
        (20.169171, 49.957535),
        (19.812178, 49.941828),
        (19.766410 , 50.182752)
        ])
        polygon: Polygon = self.get_polygon_from_coords()
        if not polygon.within(krakow):
            raise ValidationError({"detail": "Parking area cannot exceeed Krakow"})
        #Later more validation will be implemented, but who knows when :) 

    @classmethod
    def class_name(cls):
        return "Rental"
    
#After refactoring the reset should be improved
class ResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default = uuid.uuid4,unique=True)
    updated_at = models.DateTimeField()
    def __str__(self):
        return f'{self.user.username}, has {self.uuid}, created at {self.last_updated}'
    
    def set_uuid(self,user):
        self.user = user
        self.uuid = uuid.uuid4()
        self.updated_at= timezone.now()
        self.save()
