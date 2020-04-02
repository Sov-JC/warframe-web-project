from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser

# Create your models here.
class User(AbstractBaseUser):

    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []


