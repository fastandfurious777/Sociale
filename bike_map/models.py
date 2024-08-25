from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bike(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    encrypted_code = models.TextField()
    is_available = models.BooleanField()
    last_taken_by = models.ForeignKey(User, on_delete=models.PROTECT)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(null=True,blank=True)
    is_completed = models.BooleanField(null=True)

    def __init__(self):
        super().__init__(self)
        self.bike.is_available = False
        self.is_completed = False
        self.bike.last_taken_by = self.user
        self.bike.save()
        self.save()

    def end_rental(self):
        self.end_time = timezone.now()
        self.bike.is_available = True
        self.is_completed = True
        self.bike.save()
        self.save()
