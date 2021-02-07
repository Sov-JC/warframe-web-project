from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.models import *
from django.contrib import auth

#from django.test.utils import override_settings


class TestUserModel(TestCase):
	fixtures = ["user_app-user-status.json", "user_app-gaming-platforms.json"]

	#@override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend')
	def test_send_email_verification_msg_sends_verification_email_to_registered_email(self):
		'''
		An email verification message should be sent to a user's
		registered email address.
		'''
		user = User.objects.create_user(email="jorge.costafreda@yahoo.com",password="11pw22pw33pw")

		assert(user.send_email_verification_msg(fail_silently=False) == 1)

	

class TestPasswordRecoveryModel(TestCase):
	fixtures = ["user_app-user-status.json", "user_app-gaming-platforms.json"]

	def setUp(self):
		# Create a user with a linked warframe account. Create a password recovery
		# record that referenced this user.
		wfa = WarframeAccount.objects.create_warframe_account("Warframeaccount1")
		user = User.objects.create_user(email="testuser@yahoo.com", linked_warframe_account_id=wfa, password="Jjiowej89")
		PasswordRecovery.objects.create_password_recovery(user)

	def test_has_recovery_code_expired_returns_false_on_non_expired_code(self):
		ONE_HOUR_EXPIRE_PERIOD = 60*60*1000 # one hour

		password_recovery = User.objects.get(email="testuser@yahoo.com").password_recovery
		
		response = password_recovery.has_recovery_code_expired(ONE_HOUR_EXPIRE_PERIOD)
		msg="Expected true because the password recovery was created less than one hour ago"
		self.assertFalse(response, msg=msg)

	def test_has_recovery_code_expired_returns_true_on_expired_code(self):
		ONE_HOUR_EXPIRE_PERIOD = 60*60*1000

		print("timedetal(ONE_HOUR_EXPIRE_PERIOD) %s" % (datetime.timedelta(milliseconds=ONE_HOUR_EXPIRE_PERIOD).total_seconds()))

		one_hour = datetime.timedelta(hours=1)
		five_seconds = datetime.timedelta(seconds=5)
		now = timezone.now()

		user = User.objects.get(email="testuser@yahoo.com")
		password_recovery_qs = PasswordRecovery.objects.filter(user_id=user)

		# Change time datetime_code_created to 1 hours and 1 second into the past
		print("password_recovery: %s" % password_recovery_qs)
		password_recovery_qs.update(datetime_code_created = ((now - one_hour) - five_seconds))
		
		password_recovery = user.password_recovery

		msg = "Since datetime_code_created is 1 hour 1 second into the past and the expire period is 1 hour " \
			"the code should be expired"
		print("password_recovery type: %s" % (type(password_recovery)))
		response = password_recovery.has_recovery_code_expired(ONE_HOUR_EXPIRE_PERIOD)
		self.assertTrue(response, msg=msg)

	def test_has_recovery_code_raises_value_error_on_negative_arg(self):
		'''Should return a validation error mentioning 'validity_duration'
		must be positive
		'''
		password_recovery = User.objects.get(email="testuser@yahoo.com").password_recovery

		try:
			password_recovery.has_recovery_code_expired(-500)
			self.fail(msg="ValueError should have been raised because negative argument")
		except ValueError:
			pass
	