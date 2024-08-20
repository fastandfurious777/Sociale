from django.db import models
from django.contrib.auth.models import User

class Bike(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()
    encrypted_code = models.TextField()
    is_available = models.BooleanField()
    last_taken_by = models.ForeignKey(User, on_delete=models.PROTECT)
    last_updated = models.DateTimeField(auto_now=True)
