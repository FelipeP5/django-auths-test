from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Box(models.Model):
    things = models.CharField()

class CustomUser(AbstractUser):
    # username e password são obrigatórios
    email = models.EmailField(unique=True, null=False, blank=False)
    rights = models.BooleanField(default=False)