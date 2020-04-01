from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    username = models.CharField(max_length-40, unique=True)
    email = models.EmailField()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'