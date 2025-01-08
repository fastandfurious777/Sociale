from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str, first_name:str, last_name: str):
        """Creates and returns user"""
        if not email:
            raise ValueError("The Email field is required")
        if not first_name:
            raise ValueError("The First Name field is required")
        if not last_name:
            raise ValueError("The Last Name field is required")
        if not password:
            raise ValueError("The Password field is required")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, first_name: str, last_name: str):
        """Creates and returns superuser"""
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    joined_at = models.DateTimeField(
        verbose_name='date joined', 
        default=timezone.now
    )
    last_active_at = models.DateTimeField(
        verbose_name='last active', 
        default=timezone.now,
        null=True
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(verbose_name='active user', default=False)
    is_verified = models.BooleanField(verbose_name='verified email', default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def deactivate(self):
        self.is_active = False
        self.save()

    @property
    def is_eligible(self):
        return self.is_active and self.is_verified