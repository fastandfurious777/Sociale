"""
from django.db import models

class Bike(models.Model):
    name = models.CharField()
    #lat and longtitude, maby with geodjango
    encrypted_code = models.TextField()
    is_available = models.BooleanField()
"""
    
