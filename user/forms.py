# appname/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import User

from .validators import valid_password_characters


'''
class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
'''

class LoginForm(forms.Form):
    EMAIL_ADDR_MAX_LEN = 254
    email_address = forms.EmailField(
        max_length=EMAIL_ADDR_MAX_LEN,
        error_messages = {
            "required": "Email address is required.",
            "invalid": "Email is invalid" 
        }
    )
    
    password = forms.CharField(
        min_length=5,
        max_length=32,
        error_messages = {
            "required": "Password is required.",
        }
    )

class RegistrationForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        error_messages = {
            "required": "Email address is required",
            "invalid": "Email is invalid"
        },
    )

    #NOTE: if any of the password validators are modified for this form,
    #you should likely make sure they synchronize with the AUTH_PASSWORD_VALIDORS
    #settings.
    password1 = forms.CharField(
        max_length=32,
        min_length=8,
        validators=[valid_password_characters],
        error_messages = {
            "required": "Password field is required",
        }
    )

    password2 = forms.CharField(
        max_length=32,
        min_length=8,
        validators=[valid_password_characters],
        error_messages = {
            "required": "Confirmation password is required"
        }
    )

    def clean(self):
        cleaned_data = super().clean()

        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")

        if pw1 != pw2:
            raise forms.ValidationError(
                "Password and confirmation password do not match. The two passwords must be the same.",
                code="password_mismatch",
            )

class ForgotPasswordForm(forms.Form):
    email_address = forms.EmailField(
        error_messages={
            'required': 'Email field is required',
            'invalid': 'Email field is invalid',
        }
    )
    

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        max_length=32,
        min_length=8,
        validators=[valid_password_characters],
        error_messages={
            'required': 'Password field is required',
            'invalid': 'Password field is invalid',
        }
    )
    password2 = forms.CharField(
        max_length=32,
        min_length=8,
        validators=[valid_password_characters],
        error_messages={
            'required': 'Confirmation field is required',
            'invalid': 'Confirmation field is invalid',
        }
    )

    def clean(self):
        cleaned_data = super().clean()

        pw1 = cleaned_data.get("password1")
        pw2 = cleaned_data.get("password2")

        if pw1 != pw2:
            raise forms.ValidationError(
                "Password and confirmation password do not match. The two passwords must be the same.",
                code="password_mismatch",
            )


