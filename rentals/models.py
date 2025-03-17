from rest_framework.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import User
from bikes.models import Bike


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    bike = models.ForeignKey(Bike, on_delete=models.SET_NULL, null=True, blank=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True,blank=True)

    class Status(models.TextChoices):
        # Status will be stored in the database in lowercase (e.g. "started") but displayed to user as "Started" 
        # See: https://docs.djangoproject.com/en/3.0/ref/models/fields/#enumeration-types
        STARTED = "started", "Started"
        CANCELED = "canceled", "Canceled"
        FINISHED = "finished", "Finished"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.STARTED
    )
    def clean(self):
        if self.finished_at and self.started_at >= self.finished_at:
            raise ValidationError({"detail": "Rental finish date cannot be before the start date"})

        # Excluding self.id ensures the current rental is not mistakenly checked against itself,
        # preventing an error when updating an existing rental.)
        query = models.Q(user=self.user, status=self.Status.STARTED)
        if Rental.objects.filter(query).exclude(id=self.id).exists():
            raise ValidationError({"detail": "You cannot have more than one rental started"})