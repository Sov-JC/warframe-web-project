from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin 

import random

class RunType(models.Model):
    runTypeID = models.AutoField(primary_key=True)
    ONE_BY_ONE = "OO"
    TWO_BY_TWO = "TT"
    FOUR_BY_FOUR = "FF"

    TYPE_NAME_CHOICES = [
        (ONE_BY_ONE, 'One by One'),
        (TWO_BY_TWO, 'Two by Two'),
        (FOUR_BY_FOUR, 'Four by Four')
    ]

    typeName = models.CharField(
        max_length=16, 
        unique=True,
        choices=TYPE_NAME_CHOICES
    )

class Relic(models.Model):
    relic_id = models.AutoField(primary_key=True)
    relic_name = models.CharField(max_length=32, unique=True)
    wiki_url = models.CharField(max_length=512)

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

''' helper function for generating a verification code for a warframe account'''
def _generate_warframe_account_verification_code():
    VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    CODE_LENGTH = 12
    generated_verification_code = ""

    for i in range(0,CODE_LENGTH):
        rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
        generated_verification_code += rand_char


    return generated_verification_code

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
    #email_verification_code = models.CharField(max_length=32, unique=True, null=True)
    warframe_account_verification_code = models.CharField(
        max_length=12, unique=True,
         default=_generate_warframe_account_verification_code
    )
        
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

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    host_user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT
    )
    relic_id = models.ForeignKey(
        'Relic', 
        on_delete = models.PROTECT
    )
    run_type_id = models.ForeignKey(
        'RunType',
        on_delete = models.PROTECT
    )
    players_in_group = models.IntegerField()

''' helper function for generating an email verification code'''
def _generate_email_verification_code():
        VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'        
        CODE_LENGTH = 32
        generated_verification_code = ""

        for i in range(0,CODE_LENGTH):
            rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
            generated_veriffication_code += rand_char

        return generated_verification_code

class EmailVerificationCode(models.Model):
    email_verification_code_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
        )
    email_verification_code = models.CharField(max_length=32, default=_generate_email_verification_code)

    class Meta:
        db_table = "user_email_verification_code"

class PasswordRecovery(models.Model):
    password_recovery_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    #default should not execute
    recovery_code = models.CharField(max_length=32, default="") 
    dateCodeCreated = models.DateTimeField(auto_now_add=True, blank=True)
    dateCodeUsed = models.DateTimeField(null=True, blank=True, default=None)

    def _generate_password_recovery_code(self):
        pass





