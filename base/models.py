import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from rest_framework.exceptions import ValidationError

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
        
class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True,blank=True)

    def clean(self):
        if self.started_at >= self.finished_at:
            raise ValidationError({"detail": "'finished_at' cannot be before 'started_at'"})

class Parking(models.Model):
    name = models.CharField(max_length=100, unique=True)
    coords = models.PolygonField()
        
    def contains_point(self, lon: float, lat: float) -> bool:
        """Checks if a given point (latitude, longitude) is within the parking area"""
        polygon = self.coords.prepared
        return polygon.contains(Point(lon, lat))
    
    def clean(self):
        #checks if polygon is inside cracow 
        #add geodjango to project
        raise ValidationError({"detail": "Parking area cannot exceeed Krakow"})
    

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
