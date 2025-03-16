from rest_framework.exceptions import ValidationError
from django.db import models

from users.models import User
from bikes.models import Bike


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike, on_delete=models.PROTECT)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True,blank=True)

    class Status(models.TextChoices):
        # Status will be returned as nice looking string (label) eg. Started, Canceled 
        # See: https://docs.djangoproject.com/en/3.0/ref/models/fields/#field-choices-enum-auto-label
        STARTED = 'S'
        CANCELED = 'C'
        FINISHED = 'F'

    status = models.CharField(
        max_length=1,
        choices=Status.choices
    )
    def clean(self):
        if self.finished_at and self.started_at >= self.finished_at:
            raise ValidationError({"detail": "'finished_at' cannot be before 'started_at'"})

        # Excluding self.id ensures the current rental is not mistakenly checked against itself,
        # preventing an error when updating an existing rental.
        query = models.Q(user=self.user, status=self.Status.STARTED)
        if Rental.objects.filter(query).exclude(id=self.id).exists():
            raise ValidationError({"detail": "You cannot have more than one rental started"})