from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    

    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ["username"]
    
    def __str__(self):
        return self.email