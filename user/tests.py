from django.test import TestCase
from .models import User

from django.db.utils import IntegrityError

# Create your tests here.
def create_user(email = None, password = None):
	User.objects.create_user(email=email, password=password)
	pass

def crate_super_user(email = None, password = None):
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
	
	def test_create_regular_user_method_with_invalid_email_or_password(self):
		VALID_EMAIL = "regularuser@example.com"
		VALID_PASSWORD = "tangodjango551"

		INVALID_EMAIL = "invalidemail"
		INVALID_PASSWORD = "1"

		user_instance_one = User.objects.create_user(VALID_EMAIL, INVALID_PASSWORD)
		user_instance_two = User.objects.create_user(INVALID_EMAIL, VALID_PASSWORD)

		self.assertEqual(user_instance_one, None)
		self.assertEqual(user_instance_two, None)

	def test_create_super_user_with_valid_required_fields(self):
		pass


class LoginViewTestCase(TestCase):

	def test_valid_login_form_but_failed_authentication(self):
		"""
		When a user inputs valid login information but authentication fails
		user should be redirected to the same login page with an error message
		saying the email/password combination was incorrect.
		"""
		pass

	def test_user_login_attempt_when_user_already_logged_in(self):
		"""
		A 404 should be displayed if a user attempts to visit the login page when
		they are already logged in.
		"""
		pass

	def test_home_page_redirect_when_loggin_attempt_successful(self):
		"""
		User should be sent to the login page when they've successfully logged in
		"""
		pass


class LogoutViewTestCase(TestCase):

	pass