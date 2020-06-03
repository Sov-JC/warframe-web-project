from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin 
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


import random


class GamingPlatformManager(models.Manager):
	pass

class WarframeAccountManager(models.Manager):
	pass

class PasswordRecoveryManager(models.Manager):
	pass


# code snippet from:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
class UserManager(BaseUserManager):

	''' helper function for generating a verification code for a warframe account'''
	def _generate_warframe_account_verification_code(self):
		VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		CODE_LENGTH = 12
		generated_wfa_verification_code = ""

		for i in range(0,CODE_LENGTH):
			rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
			generated_wfa_verification_code += rand_char

		return generated_wfa_verification_code

	def _generate_email_verification_code(self):
		VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		CODE_LENGTH = 32
		generated_email_verification_code = ""

		for i in range(0,CODE_LENGTH):
			rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
			generated_email_verification_code += rand_char

		return generated_email_verification_code


	def _create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields) #???
		user.set_password(password) #???

		user.email_verification_code = self._generate_email_verification_code()
		user.warframe_account_verification_code = self._generate_warframe_account_verification_code()
		
		user.save(using=self._db) #??
		return user
	
	#required
	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_staff', False)
		return self._create_user(email, password, **extra_fields)

	#required
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

	"""
	def get_user_given_linked_wf_alias_OLD(self, wf_alias):
		'''
		Get the user whos linked warframe account has the alias of wf_alias

		returns None is used does not exist. That is, there is no user who
		has a warframe account linked with the alias of 'wf_alias' 
		'''
		warframe_account = None
		user = None
	  
		try:
			warframe_account = WarframeAccount.objects.get(warframe_alias=wf_alias)
			user = self.get(linked_warframe_account_id=warframe_account)
		except ObjectDoesNotExist:
			print("No such warframe account exists or no user has that warframe account linked.")
			user = None

		return user
	"""

	def get_user_given_linked_wf_alias(self, wf_alias):
		'''
		Get the user whos linked warframe account has the alias of wf_alias

		returns None is used does not exist. That is, there is no user who
		has a warframe account linked with the alias of 'wf_alias' 
		'''
		user = None
		try:
			#User's linked_warframe_account_id is a one-to-one relationship,
			#because of this we can pass filter arguments
			#unique to one-to-one relationships.
			user_query_set = self.all().filter(linked_warframe_account_id__warframe_alias = wf_alias)
			user = user_query_set.first()
		except ObjectDoesNotExist:
			print("No such warframe account exists or no user has that warframe account linked.")
			user = None
		
		return user

	def email_verified_users(self):
		pass


class UserTestDataTransferManager(BaseUserManager):
	"""
	Manager for transfering test data from csv files to
	the default db during development. This manager
	is very similar to the default User manager used in production.
	"""

	def _create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields) #???
		user.set_password(password) #???

		

		#user.email_verification_code = self._generate_email_verification_code()
		#user.warframe_account_verification_code = self._generate_warframe_account_verification_code()
		
		user.save(using=self._db)
		return user
	
	#required
	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_staff', False)
		return self._create_user(email, password, **extra_fields)

	#required
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


