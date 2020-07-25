from django.core.exceptions import PermissionDenied
from .models import User

def email_validated_user(function):
	def wrap(request, *args, **kwargs):
		user = User.objects.get(pk=kwargs['email'])

		if User.email_verified == True:
			return function(request, *args, **kwargs)
		else:
			raise Exception("User must confirm their email address before accessing this view.")

	return wrap

def login_required_and_linked(function):
	def wrap(request, *args, **kwards):
		user = User.objects.get(pk=kwards['email'])

	raise NotImplementedError

		
		


	