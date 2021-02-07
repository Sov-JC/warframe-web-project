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
from django.utils.html import escape
from django.conf import settings


import random
import string

class GamingPlatformManager(models.Manager):


	pass

class WarframeAccountManager(models.Manager):

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

	# Not tested yet.
	def get_linked_wfa_ids_that_own_relic_on_platform_and_are_online(self, relic, gaming_platform):
		'''Obtain Warframe account ids that are online and own a particular relic on a specific
		gaming platform.

		:param relic: The Relic instance that Warframe account owns, defaults to [DefaultParamVal]
		:type relic: Relic
		:param gaming_platform: The gaming platform
		:type gaming_platform: GamingPlatform object
		...
		:return: A set of Warframe account ids that have 'relic' in their
		inventory, are online, and belong to the gaming platform 'gaming_platform'.

		If @relic or @gaming_platform is None, returns an empty set
		:rtype: Set of Warframe account ids.
		'''
		if relic == None or gaming_platform == None:
			raise ValueError("relic and gaming_platform cannot be None")

		user_status_m = apps.get_model('user', 'UserStatus')
		owned_relic_m = apps.get_model('relicinventory', 'OwnedRelic')
		online_user_status = user_status_m.objects.get(user_status_name="Online")
		

		wfa_ids = owned_relic_m.objects.filter(relic_id=relic.pk, 
			warframe_account_id__user__user_status_id=online_user_status,
			warframe_account_id__gaming_platform_id=gaming_platform.pk
			).select_related(
			'warframe_account_id__user__user_status',
			'warframe_account_id__gaming_platform_id'
			).values_list(
			"warframe_account_id",
			flat=True
			)

		return set(wfa_ids)

	

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
		'''
		
		'''
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
	def send_pw_recovery_email(self, user, fail_silently=False):
		'''Send a new password recovery email to a user's registered email
		address. Note: This implicitly updates the password recovery code by deleting
		the record of the old password recovery code and then creating a new one. The newly created
		recovery code is then sent along with the pw recovery email integrated into a link
		that the user may click on.

		:param user: User to send a password recovery email to
		:type user: User model instance
		'''
		password_recovery_code = self.generate_password_recovery_code()

		print("user is: " + str(user))
		
		# delete the referencing one-to-one field instance, PasswordRecovery, if it exists
		if hasattr(user, 'password_recovery'):
			#delete the instance
			print("About to delete password_recovery record with code: " + user.password_recovery.recovery_code)
			rows_deleted = user.password_recovery.delete()
			print("rows deleted - " + str(rows_deleted))

		password_recovery_code = self.create_password_recovery(user)

		# Generate the url that the user will click on to be redirected to the 'change
		# password page.
		PROTOCOL = "http://" # NOTE: REFACTOR THIS! It should be https in the future. Currently set to http for development.
		DOMAIN = settings.DOMAIN_NAME
		from django.urls import reverse
		PATH = (reverse('user:change_pw', args=[password_recovery_code.recovery_code]))
		print("PROTOCOL: %s, DOMAIN: %s, PATH: %s" % (PROTOCOL, DOMAIN, PATH))
		change_pw_url = ("%s%s%s") % (PROTOCOL,DOMAIN,PATH)
		print("change_pw_url is: " + str(change_pw_url))
		
		#email content setup
		PW_RECOVERY_EMAIL_PATH = "email/forgot-password.html"
		template_name = PW_RECOVERY_EMAIL_PATH
		context = {'change_pw_url':change_pw_url}
		subject = "Vaulted Runs - Password Recovery Request"
		html_message = render_to_string(template_name, context)
		from_email = settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else None
		to = user.email

		return mail.send_mail(subject=subject, message = "", html_message=html_message, from_email=from_email, recipient_list=[to], fail_silently=fail_silently)

#DEP
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
		#extra_fields.setdefault('user_status', 'Offline')

		#TODO: make reference to .utils.py
		user.email_verification_code = self._generate_email_verification_code()
		user.warframe_account_verification_code = self._generate_warframe_account_verification_code()

		#user_status_model = apps.get_model('user', 'UserStatus')

		#print("[extra_fields.get('user_status_name):%s]" % extra_fields.get("user_status"))
		
		#user_status = user_status_model.objects.get(user_status_name=extra_fields.get("user_status"))

		#user.user_status = user_status

		user.save(using=self._db)
		
		return user
	
	#required
	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		extra_fields.setdefault('is_staff', False)

		# Set user status to offline
		user_status_m = apps.get_model('user', 'UserStatus')
		offline_user_status_name = user_status_m.OFFLINE
		offline_user_status = user_status_m.objects.get(user_status_name=offline_user_status_name)
		extra_fields.setdefault('user_status', offline_user_status)
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

class UserStatusManager(models.Manager):
	pass