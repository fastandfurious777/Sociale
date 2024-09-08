import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default = uuid.uuid4,unique=True)
    last_updated = models.DateTimeField()
    def __str__(self):
        return f'{self.user.username}, has {self.uuid}, created at {self.last_updated}'
    
    def set_uuid(self,user):
        self.user = user
        self.uuid = uuid.uuid4()
        self.last_updated = timezone.now()
        self.save()
