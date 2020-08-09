from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.managers import *
from user.forms import *
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

class RegistrationFormTests(SimpleTestCase):

	def test_invalid_email_field(self):
		'''
		Each form instance with valid form parameters except
		the email should cause the form's is_valid() 
		function to return False
		'''

		invalid_emails = [
			"",
			"a1",
			"a2@",
			"@yahoo.com",
			"@ya.com@yahoo.com",
			"...@yahoo.com..."
		]
				
		#valid passwords
		password1="exampl&@^e12391823&@^"
		password2=password1
		
		#test the invalid emails cause their corresponding form's is_valid to return false 
		for email in invalid_emails:
			reg_form = RegistrationForm(data={'email':email, 'password1':password1, 'password2': password2})
			self.assertEqual(reg_form.is_valid(), False)


	def test_valid_form_level_validation(self):
		'''
		A RegistrationForm with all valid fields and
		valid in the form level should return True when
		is_valid() is called
		'''
		#valid fields
		email = "valid123@gmail.com"
		password1 = "jk39lopq*&"
		password2 = "jk39lopq*&"

		form_data = {'email':email, 'password1':password1, 'password2': password2}
		form = RegistrationForm(data=form_data)

		self.assertEqual(form.is_valid(), True)

	def test_unmatching_password_fields(self):
		'''
		If the two password fields do not match, is_valid should return False.
		It should also contain the error code for 'password_mismatch'.
		'''
		email = "valid123@gmail.com"
		password1 = "pw1234567"
		password2 = "pw1233333"
		form_data = {'email':email, 'password1':password1, 'password2': password2}
		form = RegistrationForm(data=form_data)

		self.assertEqual(form.is_valid(), False)

		#check for error code
		self.assertEqual(form.non_field_errors().as_data()[0].code, "password_mismatch")
		
class TestForgotPasswordForm(SimpleTestCase):

	def test_forgot_password_form_accepts_email(self):
		email = "testaccount@gmail.com"
		data = {'email_address':email}
		self.assertEqual(ForgotPasswordForm(data=data).is_valid(), True)

		email = ""
		data = {'emailaddress':email}
		self.assertEqual(ForgotPasswordForm(data=data).is_valid(), False)

		email = None
		data = {'emailaddress':email}
		self.assertEqual(ForgotPasswordForm(data=data).is_valid(), False)

		email = "123"
		data = {'emailaddress':email}
		self.assertEqual(ForgotPasswordForm(data=data).is_valid(), False)

class TestChangePasswordForm(SimpleTestCase):
	
	def test_clean_raises_validation_error_on_different_passwords(self):
		'''Should return a Validation Error with code 'password_mismatch'
		if password1 and password2 don't match
		'''
		data = {'password1': "aaaaaaaaa", 'password2':"bbbbbbbbbb"}
		f = ChangePasswordForm(data=data)
		msg = "Form should not be valid because password1 and password2 are different"
		self.assertEqual(f.is_valid(), False, msg=msg)

		msg="Expected password_mismatch error because password1 and password2 are not equal"
		self.assertEqual(f.has_error(field=NON_FIELD_ERRORS, code='password_mismatch'), True, msg=msg)

	def test_clean_raises_no_error_when_pw1_and_pw_are_equal(self):
		'''
		Should return no Validation Error when password1 and password2 are equal
		'''
		data = {'password1': "testpassword123", 'password2':"testpassword123"}
		form = ChangePasswordForm(data=data)
		msg = "Form should be valid because password1 and password2 are equal and valid"
		self.assertEqual(form.is_valid(), True, msg = msg)

		msg = "Error with code 'password_mismatch' should not have occured because password1 "\
			"and password2 are equal."
		print("-------->" + str(form.errors))
		print("type: " + str(type(form.errors)))
		self.assertEqual("password_mismatch" not in form.errors, True, msg=msg)



