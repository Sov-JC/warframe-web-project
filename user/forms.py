# appname/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


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
    email_address = forms.EmailField(max_length=EMAIL_ADDR_MAX_LEN)
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput,
    )