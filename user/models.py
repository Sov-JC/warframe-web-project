from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

'''
imports used in code snippet
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
'''
# code snippet from:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) #???
        user.set_password() #???
        user.save(using=self._db) #??
        return user
    
    #???
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)

# Create your models here.
class User(AbstractBaseUser):

    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()




