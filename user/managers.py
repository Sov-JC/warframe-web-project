from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin 
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from user import utils
from django.apps import apps
from django.template.loader import render_to_string
from django.core import mail
from django.conf import settings
from projectutils import generators
from django.utils import timezone


import random
import string

class GamingPlatformManager(models.Manager):


	pass

class WarframeAccountManager(models.Manager):
	def get_wf_accounts_of_online_users_with_relic(self, relic_name=None):
		'''
		Obtain all warframe accounts that are linked to a user that have the relic
		'relic_name' in their inventory	and are online.
		'''

		if relic_name is None:
			raise ValueError("relic_name cannot be None")

		

		wf_accounts = self.all()
		
		return wf_accounts;

	def _create_warframe_account(self, warframe_alias=None, **extra_fields):
		if warframe_alias == None:
			raise ValueError("warframe_alias argument is required")
		
		wf_account = self.model(warframe_alias=warframe_alias, **extra_fields)
		
		wf_account.save(using=self._db)
		

		return wf_account

	
	def create_warframe_account(self, warframe_alias=None, **extra_fields):
		'''
		Create a warframe account. If a gaming platform is not specified, 
		it will be set to PC.
		'''
		extra_fields.setdefault('is_blocked', False)

		#if a gaming platform isn't specified, it defaults to the PC gaming platform
		gaming_platform_model = apps.get_model('user', 'GamingPlatform')
		pc_choice = gaming_platform_model.PC
		pc_gaming_platform = gaming_platform_model.objects.get(platform_name=pc_choice)
		extra_fields.setdefault('gaming_platform_id', pc_gaming_platform) 

		wf_account = self._create_warframe_account(warframe_alias, **extra_fields)

		return wf_account

class OnlineAndLinkedWarframeAccountManager(models.Manager):
	'''
	A manager for Warframe accounts that are linked to a User
	object, and whose user status is 'Online'
	'''
	def get_queryset(self):
		#linked_users = super().get_queryset().filter(linked_warframe_account)
		# warframe_accounts = super().get_queryset()
		# return super().get_queryset().filter("user_user_status_id__user_status_name = 'online'")
		pass


class PasswordRecoveryManager(models.Manager):

	def create_recovery_code_for_user(self):
		'''
		~To implement in db schema 0.2.0~
		Creates a new recovery code for a user.
		'''
		raise NotImplementedError()

	def _create_password_recovery(self, user, **extra_fields):
		if not user:
			raise ValueError("The given user must be set")
		
		extra_fields.setdefault('datetime_code_created', timezone.now())
		
		password_recovery = self.model(user_id=user, **extra_fields)
		password_recovery.save()

		return password_recovery

	def create_password_recovery(self, user, **extra_fields):
		generated_recovery_code = self.generate_password_recovery_code()
		extra_fields.setdefault('recovery_code', generated_recovery_code)
		extra_fields.setdefault('datetime_code_used', None)

		return self._create_password_recovery(user, **extra_fields)

	def _generate_password_recovery_code(self, chars, length):
		'''Generates a password recovery code.

		:param chars: Characters that the generator can select from
		to generate the recovery code
		:type chars: String
		:param length: The length of the password recovery code.
		...
		:return: A password recovery code
		:rtype: String
		'''
		return generators.generate_random_string(chars, length)
	
	def generate_password_recovery_code(self):
		'''Generates a fixed length, random string of chars.
		Valid chars are numbers and letters (uppercase and lowercase). The length
		of the password recovery code is equal to the max_length property
		of the 'recovery_code' field of this manager's model.
		...
		:return: A randomly generated password recovery code
		:rtype: String
		'''
		#get the max_length of the 'recovery_code' CharField
		length = self.model._meta.get_field('recovery_code').max_length

		chars = (string.ascii_letters + "0123456789")
		return self._generate_password_recovery_code(chars, length)

	#Untested
	def send_password_recovery_email(self, user, fail_silently=False):
		'''Send a password recovery email to a user's registered email
		address. Note: This deletes the currenct recovery code held by the referncing
		PasswordRecovery instance of 'user' and then creates a new one. The recovery code
		for the new PasswordRecovery instance is sent via email.
		'''
		password_recovery_code = self.generate_password_recovery_code()

		print("user is: " + str(user))
		
		# delete the referencing one-to-one field instance, PasswordRecovery, if it exists
		if hasattr(user, 'password_recovery'):
			#delete the instance
			print("About to delete password_recovery record with code: " + user.password_recovery.recovery_code)
			rows_deleted = user.password_recovery.delete()
			print("rows deleted - " + str(rows_deleted))
		else:
			print("user.password_recovery is None. No referencing PasswordRecovery deleted.")
			#delete

		password_recovery_code = self.create_password_recovery(user)
		
		#email content setup
		EMAIL_VERIFICATION_MSG_PATH = "email/forgot-password.html"
		template_name = EMAIL_VERIFICATION_MSG_PATH
		context = {"password_recovery_code": password_recovery_code}
		subject = "Vaulted Runs - Password Recovery Request"
		html_message = render_to_string(template_name, context)
		from_email = settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else None
		to = user.email

		return mail.send_mail(subject=subject, message = "", html_message=html_message, from_email=from_email, recipient_list=[to], fail_silently=fail_silently)

class LinkedOnlineUsersManager(models.Manager):
	def get_queryset(self):
		users = super().get_queryset().exclude(linked_warframe_account_id__isnull=True).filter(user_status_id__user_status_name="online")
		print("query is: " + users.query)
		return users
		

# code reference from:
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser
class UserManager(BaseUserManager):
	
	#TODO: replace with utils function
	''' helper function for generating a verification code for a warframe account'''
	def _generate_warframe_account_verification_code(self):
		VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		CODE_LENGTH = 12
		generated_wfa_verification_code = ""

		for i in range(0,CODE_LENGTH):
			rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
			generated_wfa_verification_code += rand_char

		return generated_wfa_verification_code

	#TODO: replace with utils function
	def _generate_email_verification_code(self):
		VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		CODE_LENGTH = 32
		generated_email_verification_code = ""

		for i in range(0,CODE_LENGTH):
			rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
			generated_email_verification_code += rand_char

		return generated_email_verification_code

	#TODO: move user_status information to the create_user() function
	#instead of _create_user(). This is to pass it in as part of **extra_fields
	#on the create_user() function
	def _create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields) #???
		user.set_password(password) #???
		extra_fields.setdefault('user_status', 'offline')

		#TODO: make reference to .utils.py
		user.email_verification_code = self._generate_email_verification_code()
		user.warframe_account_verification_code = self._generate_warframe_account_verification_code()

		user_status_model = apps.get_model('user', 'UserStatus')

		#print("[extra_fields.get('user_status_name):%s]" % extra_fields.get("user_status"))
		
		user_status = user_status_model.objects.get(user_status_name=extra_fields.get("user_status"))

		user.user_status = user_status

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
		extra_fields.setdefault('email_verified', True)

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

	
	# !! DANGER - BUG !! refactor this, the query should factor in gaming platform as
	# well. wf_alias is not sufficient!!!
	def get_user_given_linked_wf_alias(self, wf_alias):
		'''
		Get the user whos linked warframe account has the alias of wf_alias

		returns None is user does not exist. That is, there is no user who
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
		verified_users = self.all().filter(email_verified=True)
		return verified_users

