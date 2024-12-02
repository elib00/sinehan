from django.db import models
from django.contrib.auth.models import AbstractUser

def media_path(instance, filename): 
    return f'{filename}' 

class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, unique=True)
    
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]