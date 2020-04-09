from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin 

class Relic(models.Model):
    relic_id = models.AutoField(primary_key=True)
    relic_name = models.CharField(max_length=32, unique=True)
    wiki_url = models.CharField(max_length=512,unique=True)

class GamingPlatform(models.Model):
    gaming_platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=32, unique=True)

class WarframeAccount(models.Model):
    warframe_account_id = models.AutoField(primary_key=True)
    gaming_platform_id = models.ForeignKey(
        'GamingPlatform', 
        on_delete=models.PROTECT)
    is_blocked = models.BooleanField(default=False)


# code snippet from:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
class UserManager(BaseUserManager):
    
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) #???
        user.set_password(password) #???
        user.save(using=self._db) #??
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    #username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email' 
    EMAIL_FIELD = 'email' 

    email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # admin, not a super-user
    #admin = models.BooleanField(default=False) # a superuser

    #linked_warframe_account_id = "not_implemented_yet"
    beta_tester = models.BooleanField(default=True)
    user_verification_email_code = models.CharField(max_length=32, unique=True)
    warframe_account_verification_code = models.CharField(max_length=12, unique=True)
        
    REQUIRED_FIELDS = [] #used in interactive only IT.

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


    #Just use the default one from PermissionsMixin
    '''
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True
    '''

    def has_module_perms(self, app_label):
        return True
    
    '''
    @property
    def is_staff(self):
        return self.staff
    '''

    '''
    @property
    def is_admin(self):
        return self.admin
    '''
    
    '''
    @property
    def is_active(self):
        return self.active
    '''

    def __str__(self):
        return self.email




