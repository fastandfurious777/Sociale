import uuid
from django.db import models
from rest_framework.exceptions import ValidationError

from parkings.selectors import check_parking_location
from users.models import User


class Bike(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    code = models.IntegerField()
    qr_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_available = models.BooleanField()
    last_taken_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    last_updated = models.DateTimeField(auto_now=True)

    def start_rent(self, user):
        if not self.is_available:
            raise ValidationError({"detail": "Bike is not available"})
        self.is_available = False
        self.last_taken_by = user
        self.validate_location()
        self.full_clean()
        self.save()

    def finish_rent(self, lon, lat):
        self.is_available = True
        self.lon = lon
        self.lat = lat
        self.validate_location()
        self.full_clean()
        self.save()

    def validate_location(self):
        if not check_parking_location(lon=self.lon, lat=self.lat):
            raise ValidationError({"detail": "Bike is not in a parking location"})
