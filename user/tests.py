from django.test import TestCase
#from django.test import Client
from django.urls import reverse
from .models import *
from .managers import *

from django.db.utils import IntegrityError


class PasswordValidatorTests(TestCase):
	pass

class UserManagerTests(TestCase):

	def test_create_regular_user_method_with_valid_arguments(self):
		"""
		Custom User's create_user() method should create a user
		in the database when passed a valid email and password
		when the email address does not already exist in the database.
		"""

		VALID_EMAIL = "regularuser@example.com"
		VALID_PASSWORD = "tangodjango551"
		User.objects.create_user(VALID_EMAIL, VALID_PASSWORD)
		
		#all_users = User.objects.filter(email_address)
		user_instance = User.objects.get(email = VALID_EMAIL)
		self.assertEqual(user_instance.email, VALID_EMAIL)

	def test_create_regular_user_when_email_already_exists(self):
		"""
		No two users should have the same email address. An IntegrityError
		is raise if a user is created using an email that already exists in the 
		database.
		"""
		VALID_EMAIL = "regularuser@example.com"
		VALID_PASSWORD = "tangodjango551"

		User.objects.create_user(VALID_EMAIL,VALID_PASSWORD)

		self.assertRaises(IntegrityError, User.objects.create_user, VALID_EMAIL, VALID_PASSWORD)
	
	def test_create_regular_user_method_with_missing_email(self):
		VALID_PASSWORD = "tangodjango551"

		self.assertRaises(ValueError, User.objects.create_user, None, VALID_PASSWORD)

	def test_create_super_user_with_valid_required_fields(self):
		pass

	def test_get_user_given_linked_wf_alias_with_nonexisting_alias(self):
		"""
		Test the return type of the method get_user_given_linked_wf_alias() when
		fed a warframe alias that does not exist in the database. Also, check for null
		and empty string arguments to the method.
		"""
		UserOne = User.objects.get_user_given_linked_wf_alias("")
		UserTwo = User.objects.get_user_given_linked_wf_alias(None)
		UserThree = User.objects.get_user_given_linked_wf_alias("warframeTestUser3")
		
		self.assertEqual(UserOne, None) #argument of None
		self.assertEqual(UserTwo, None) #empty string argument
		self.assertEqual(UserThree, None) #warframe alias that does not exist in the database

	def test_get_user_given_linked_wf_alias_with_existing_alias(self):
		"""
		Should return the correct user whose linked account has
		the warframe alias 'tenno'
		"""
		WARFRAME_ALIAS = "tenno"
		wf_account = WarframeAccount(warframe_alias = WARFRAME_ALIAS)
		wf_account.save()
		print("warframe account object created and saved")
		print("[warframe_alias:%s]" % wf_account.warframe_alias)

		VALID_EMAIL = "regularuser@example.com"
		VALID_PASSWORD = "tangodjango551"
		user = User.objects.create_user(VALID_EMAIL, VALID_PASSWORD)

		user.linked_warframe_account_id = wf_account
		user.save()

		linked_wf_user = User.objects.get_user_given_linked_wf_alias(WARFRAME_ALIAS)

		self.assertEqual(linked_wf_user.email, VALID_EMAIL)

	def test_email_verified_users_with_no_verified_users(self):
		'''
		Should return an empty queryset when searching the database for all verified users
		'''

		verified_users = User.objects.email_verified_users()
		
		self.assertEqual(len(verified_users), 0)

	def test_email_verified_users_with_one_verified_user(self):
		user_one = User.objects.create_user("example@example.com",password="pw123")
		user_two = User.objects.create_user("example2@example.com",password="pw123")

		user_two_instance = User.objects.get(user_id=user_two.user_id)

		self.assertEquals(user_two_instance.email_verified, False)

		user_two_from_query_set = User.objects.filter(user_id=user_two.user_id)
		user_two_from_query_set.update(email_verified=True)

		verified_users = User.objects.email_verified_users()
		
		self.assertEqual(len(verified_users), 1)

	def test_email_verified_users_with_multiple_verified_users(self):
		verified_user_one = User.objects.create_user("example@example.com")
		verified_user_two = User.objects.create_user("example2@example.com")
		User.objects.create_user("example3@example.com")

		User.objects.filter(user_id=verified_user_one.user_id).update(email_verified=True)
		User.objects.filter(user_id=verified_user_two.user_id).update(email_verified=True)
		
		verified_users = User.objects.email_verified_users()

		self.assertEqual(len(verified_users), 2)


class UserModelTests(TestCase):
	pass

class LoginViewTestCase(TestCase):
	pass
	

class RegistrationViewTest(TestCase):
	pass


class LogoutViewTestCase(TestCase):
	pass

class ProfileViewTestCase(TestCase):
	def setUp(self):
		joe = User.objects.create_user(email = "joe@example.com", password="j934j3k29kl")
		david =User.objects.create_user(email = "david@example.com", password="mm2and94k3l2p")
		katherine = User.objects.create_user(email = "katherine@example.com", password="fjnwejrnkwer")

		pc_gaming_platform = GamingPlatform(platform_name="PC").save()

		wfa_joe_tenno = WarframeAccount(warframe_alias="joeTenno", gaming_platform_id = pc_gaming_platform)
		wfa_david_tenno = WarframeAccount(warframe_alias="davidTenno", gaming_platform_id = pc_gaming_platform)

		joe.linked_warframe_account_id = wfa_joe_tenno
		david.linked_warframe_account_id = wfa_david_tenno

	def test_profile_view_with_no_wf_alias_query_string_request(self):
		"""
		Get requests with no wf_alias query should return
		"""
		response = self.client.get(reverse('user:profile'))
		
		self.assertEqual(response.status_code, 404)

	def test_profile_view_with_non_existing_wf_alias(self):
		"""
		
		"""
		pass

		

		