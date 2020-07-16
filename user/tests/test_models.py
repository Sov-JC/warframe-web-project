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

	