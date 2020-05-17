from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .managers import *

import random

class GamingPlatform(models.Model):
    gaming_platform_id = models.AutoField(primary_key=True)

    PC = "PC"
    XBOX = "XBOX"
    NINTENDO_SWITCH = "Nintendo Switch"
    PLAYSTATION = "PlayStation"

    PLATFORM_NAME_CHOICES = [
        (PC, 'PC'),
        (XBOX, 'Xbox'),
        (NINTENDO_SWITCH, 'Nintendo Switch'),
        (PLAYSTATION, 'Playstation')
    ]

     #NULL SHOULD BE FALSE! NULL=True for testing currently, CHANGE THIS LATER
     #Unique should be True! CHANGE LATER
    platform_name = models.CharField(
        max_length=32, 
        unique=False, 
        null=True,
        choices = PLATFORM_NAME_CHOICES,
        default = PC
    )

    objects = GamingPlatformManager()

    class Meta:
        db_table = "user_gaming_platform"



class WarframeAccount(models.Model):
    warframe_account_id = models.AutoField(primary_key=True)
    warframe_alias = models.CharField(max_length=32, unique=True, default="") #default should not be ""

    #ADDED UNIQUE=FALSE AND NULL=TRUE FOR TESTING. REVIEW THIS LATER!!!
    gaming_platform_id = models.ForeignKey(
        GamingPlatform, 
        on_delete=models.PROTECT,
        unique=False,
        null=True,
        db_column="gaming_platform_id"
    )
    is_blocked = models.BooleanField(default=False)

    objects = WarframeAccountManager()

    def __str__(self):
        return self.warframe_alias

    class Meta:
        db_table = "user_warframe_account"


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
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

    linked_warframe_account_id = models.OneToOneField(
        WarframeAccount,
        on_delete=models.PROTECT,
        null=True,
        db_column="linked_warframe_account_id", #if attribute ommited, would append another _id to this table column name
    )

    beta_tester = models.BooleanField(default=True)

    email_verification_code = models.EmailField(
        unique=True,
        default=None
    )

    warframe_account_verification_code = models.CharField(
        max_length=12, unique=True,
        default=""
    )
        
    REQUIRED_FIELDS = [] #used in interactive only IT.

    objects = UserManager()

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def user_email_verified(self, email):
        pass

    def generate_new_warframe_verification_code(self, new_wf_verfication_code=None):
        '''
        Changes the warframe verification code of a user. An automatic
        one is generated by default, but
        '''
        pass

    #Just use the default one from PermissionsMixin
    '''
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True
    '''

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


class PasswordRecovery(models.Model):
    password_recovery_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        default=None # validation should make sure default doesn't execute
    )

    #default should not execute
    recovery_code = models.CharField(max_length=32, default="") 
    datetime_code_created = models.DateTimeField(auto_now_add=True, blank=True)
    datetime_code_used = models.DateTimeField(null=True, blank=True, default=None)

    objects = PasswordRecoveryManager()

    def _generate_password_recovery_code(self):
        pass

    class Meta: 
        db_table = "user_password_recovery"





