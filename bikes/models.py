from django.db import models
from parkings.models import Parking
from rest_framework.exceptions import ValidationError
from shapely import Point
from users.models import User
import uuid 

class Bike(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    code = models.IntegerField(max_length=10)
    qr_code = models.UUIDField( 
        default = uuid.uuid4, 
        editable = False
        ) 
    is_available = models.BooleanField()
    last_taken_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def clean(self) -> None:
        boundary = Parking.objects.filter(name="boundary").first()
        point = Point(self.lon, self.lat)
        if boundary is not None and not point.within(other=boundary.get_polygon_from_area()):
            raise ValidationError(detail={"detail": "Bike cannot be parked outside boundary"})