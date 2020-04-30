from django.test import TestCase
from .models import User

# Create your tests here.
def create_user(email = None, password = None):
	User.objects.create_user(email=email, password=password)
	pass

def crate_super_user(email = None, password = None):
	pass

class UserModelTests(TestCase):

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
		pass

	
	def test_create_regular_user_method_with_invalid_email_or_password(self):
		pass

	def test_create_regular_user_with_no_email_or_password(self):
		pass

class LoginViewTestCase(TestCase):
	pass