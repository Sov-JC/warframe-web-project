from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm
from .forms import RegistrationForm
from .models import User
from django.template.loader import render_to_string
from django.core import mail

# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the users index.")

def cant_log_in(request):
	return HttpResponse("cant_log_in::view")

def login_view(request):
	if request.method == 'POST':
		print("request is 'POST'")
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email_address"]
			password = form.cleaned_data["password"]

			user = authenticate(email=email, password=password)

			if user is not None:
				if user.email_verified == False:
					print("Email is unverified")
					CODE = "unverified_email"
					msg = "You must verify your email before logging in. "
					msg += "Please click 'Can't log in' below for instructions."
					error = ValidationError(message=msg, code=CODE)
					form.add_error(field=None, error=error)
					return render(request, 'user/login.html', context={'form':form})
				else:
					login(request, user)
					return HttpResponseRedirect(reverse('home:index'))
			else:
				#TODO: add block feature is user fails too many attempts
				CODE = "invalid_email_password_combination"
				msg = "Email/Password combination is incorrect, please try again."
				error = ValidationError(message=msg, code=CODE)
				form.add_error(field=None, error=error)
				
				return render(request, 'user/login.html', context={'form':form})
		else:
			#print("form is invalid")
			return render(request, 'user/login.html', context = {'form':form})
	else:
		print("request is not 'POST'")
		form = LoginForm()
		return render(request, 'user/login.html', context={'form':form})
	

@login_required
def log_user_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:index'))

def profile(request):
	if request.method=="GET":
		if "wf_alias" in request.GET:
			alias = request.GET["wf_alias"]
			#user = User.objects.get_user_given_linked_wf_alias(alias)
			user = None

			return render(request, 'user/user-profile.html', context = {'user':user})

			if user is None:
				raise Http404("<h1>Warframe with that name does not exist.<h1><br>"+
					"Perhaps the user unlinked their warframe account?"
				)
			else:
				return render(request, 'user/user-profile.html', context = {'user':user})
		else:
			raise Http404("Expected wf_alias query as part of the GET request.")
	else:
		raise Http404("GET request expected.")


def register(request):
	
	if request.method=="POST":
		form = RegistrationForm(request.POST)

		if form.is_valid():
			#valid form
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password1"]

			try:
				user = User.objects.create_user(email, password)
				email_verification_code = user.email_verification_code
				
				#Send verification message to their email
				user.send_email_verification_msg(fail_silently=True)
				
			except IntegrityError:
				msg = "The email address is already registered on our site."
				code = "email_not_unique"
				error = ValidationError(msg, code)
				form.add_error(field = "email", error = error)
				return render(request, 'user/register.html', context={'form':form})

			return HttpResponse("Form is valid. <br>[Email: %(email)s]<br>" % {"email": email})
		else:
			return render(request, 'user/register.html', context={'form':form})

		return HttpResponse("This is a post")
	else:
		form = RegistrationForm()
		return render(request, 'user/register.html',context={'form':form})
	
	
def link_warframe_account(request):
	return render(request, 'user/link-wf-account.html')

#DEP
def verify_email(request):
	'''
	View displayed when a user registered, requesting them to
	check their email for an email confirmation code. This view
	is also used to redirect users that attempt to access views
	that require the user to have their email verified.
	'''
	pass
