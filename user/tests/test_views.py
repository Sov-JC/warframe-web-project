from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from user.forms import *
from chat.models import *
from relicinventory.models import *
from user.managers import *
from django.contrib import auth
import django.core.mail

import datetime

class RegistrationViewTests(TestCase):
	fixtures = ['user_app-gaming-platforms.json', 'user_app-user-status.json']

	def test_registration_view_displays_registration_form(self):
		'''
		If a non POST request is made the registration form should be
		initialized and sent as context to the view as an unbound form.
		'''

		client = self.client

		path = reverse('user:register')

		response = client.get(path)
		
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Email address')
		self.assertContains(response, 'Password')
		self.assertContains(response, 'Select a password with at least')
		self.assertContains(response, "Repeat Password")

	def test_valid_registration_form_registers_user_and_redirects(self):
		'''
		A user that enters valid form data should have their account information stored
		in the database, and a message is sent to their registered email address with
		the remaining instructions.
		'''
		path = reverse('user:register')

		email = "example@gmail.com"
		password1 = "pw823j48293j4"
		password2 = "pw823j48293j4"

		
		self.assertRaises(User.DoesNotExist, User.objects.get, email=email)
		
		data = {"email":email, "password1": password1, "password2": password2}

		client = self.client

		response = client.post(path=path, data=data)

		self.assertEqual(response.status_code, 200)

		users = User.objects.all().filter(email=email)

		self.assertEqual(len(users), 1)

		#TODO: STILL NEEDS TO CHECK THAT IT REDIRECTS BUT REDIRECTION LINK HASN"T BEEN DETERMINED
		#YET. COME BACK TO THIS TEST LATER.
		raise Exception

class LoginViewTests(TestCase):
	fixtures = ['user_app-gaming-platforms.json', 'user_app-user-status.json']

	def setUp(self):
		#email verified users
		email1 = "validemail@gmail.com"
		pw1 = "validpw123123"
		user1 = User.objects.create_user(email=email1, password=pw1)
		user1.email_verified = True
		user1.save()
	
		email2 = "validemail2@gmail.com"
		pw2 = "validpw456456"
		user2 = User.objects.create_user(email=email2, password=pw2)
		user2.email_verified = True
		user2.save()

		#unverified email user
		email3 = "nonverifiedemailuser123@gmail.com"
		pw3 = "loremipsum123"
		User.objects.create_user(email=email3, password=pw3)

	def test_fixtures_used(self):
		gp = GamingPlatform.objects.all()
		print(gp)

	def test_verified_user_logs_in(self):
		'''
		A user with valid credentials who has validated their email
		should be able to log in.
		'''
		email = "user123@gmail.com"
		pw = "validpw123123"
		user = User.objects.create_user(email=email, password=pw)
		user.email_verified = True
		user.save()
		
		path = reverse('user:login')

		response = self.client.post(path=path, data={'email_address':email, 'password':pw})
		self.assertEqual(response.status_code, 302)

		user = auth.get_user(self.client)
		
		assert user.is_authenticated
		self.assertEqual(user.is_authenticated, True)
		
	def test_invalid_form(self):
		'''
		If a user inserts invalid form data, the login page is reloaded again
		'''
		email = "validemail@gmail.com" #from setUp
		invalid_password = "invalid123password"

		self.client.post(reverse('user:login'))

		pass

	



	def test_user_login_sets_session_cookie_to_one_month(self):
		'''
		When a user successfully logs in, their session cookie 
		should be set to 1 month
		'''
		assert False
		

	def test_user_login_attempts_cause_timeout(self):
		'''
		If a user attemps to log in too many times, they should be locked out
		for x amount of times after 10 attempts.
		'''
		pass

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

class ForgotPwEmailSentViewTests(TestCase):
	def test_view_is_displayed(self):
		'''
		Simple test case to check that the view is displayed.
		'''
		response = self.client.get(reverse('user:forgot_pw_email_sent'))

		self.assertEqual(response.status_code, 200, msg="Expected status code to be 200")
	
class ChangePasswordViewTests(TestCase):
	fixtures = ['user_app-gaming-platforms.json', 'user_app-user-status.json']

	def setUp(self):
		'''Create a user that had made a request to change their password
		Create another user who has not made a password request'''
		user1 = User.objects.create_user(email='user1@gmail.com',password="Kabcdefg1800")
		recovery_code="aaaabbbbccccddddeeeeffffgggghhhh" #32 chars long
		PasswordRecovery.objects.create_password_recovery(user1, recovery_code=recovery_code)

		user2 = User.objects.create_user(email="user2@gmail.com", password="J9ejwfjowejroij")

	def testRuns(self):
		self.fail()

	def test_no_such_key_sets_appropriate_error(self):
		'''A requst to the change_password view with a key that does
		not exist in the databse should set the error context variable
		to "Key does not exist".
		'''

		response = self.client.get(path=reverse("user:change_pw", args=["someinvalidkey2000"]))
		self.assertEqual(response.status_code, 200)

		NO_SUCH_KEY = "Key does not exist"
		
		msg = "Expected 'Key does not exist' error to be passed to the context via 'error' variable."
		self.assertEqual(response.context['error'], NO_SUCH_KEY, msg=msg)

	def test_expired_key_sets_appropriate_error(self):
		'''A key that exists in the database, but has expired, should set the 
		'error' context variable to 'Key has expired'. The expired time period,
		determined by the view, is 24 hours.
		'''
		password_recovery = User.objects.get(email="user1@gmail.com").password_recovery

		print("recovery code is %s" % (password_recovery.recovery_code))

		# Modify password_recovery's datetimecode to be 24 hours 5 seconds from now 
		now = timezone.now()
		twentyFourHours = datetime.timedelta(hours=23)
		fiveSeconds = datetime.timedelta(seconds=5)
		expiredDatetime = now-twentyFourHours-fiveSeconds
		PasswordRecovery.objects.all().filter(pk=password_recovery.pk).update(datetime_code_created = expiredDatetime)

		response = self.client.get(reverse("user:change_pw", args=[password_recovery.recovery_code]))
		self.assertEqual(response.status_code, 200)

		EXPIRED_KEY = "Key has expired"
		msg = "Expected context to have 'error' key with value of '%s.'" %(EXPIRED_KEY)
		self.assertIn('error',response.context, msg=msg)
		self.assertEqual(response.context['error'], EXPIRED_KEY, msg=msg)

	def test_valid_and_non_expired_key_on_non_post_request_displays_view(self):
		'''A valid key that is not expired should display the view with an
		unbound form and the key argument (passed to the view) as context.
		'''
		key = User.objects.get(email="user1@gmail.com").password_recovery.recovery_code

		response = self.client.get(reverse('user:change_pw', args=[key]))
		self.assertEqual(response.status_code, 200)

		msg= "Dicitonary keys 'form' and 'key' should be passed into the context."
		self.assertIn('form', response.context)
		self.assertIn('key', response.context)
		
		self.assertFalse(response.context['form'].is_bound, msg="Expected form to not be bound")
		self.assertTrue(isinstance(response.context['form'], ChangePasswordForm))
		msg="Expected the key received by the view as an argument to be passed to the context."
		self.assertEqual(response.context['key'], key, msg=msg)

	def test_post_request_with_valid_and_non_expired_key_but_invalid_form_displays_error(self):
		'''A POST request made with a valid and non-expired key (passed into the view as an argument).
		should display the error messages if the form was not filled out correctly.
		'''
		self.fail()
	
	def test_post_request_with_valid_key_and_no_form_errors_resets_users_password(self):
		'''A POST request made with a valid and non-expired key (passed into the view as an argument).
		should change the user's password if the 'Change Password' form was filled out correctly.
		'''
		self.fail()

