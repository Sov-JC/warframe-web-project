from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
from .forms import *
from .models import User, PasswordRecovery
from django.template.loader import render_to_string
from django.core import mail



def index(request):
	return HttpResponse("Hello, world. You're at the users index.")

#Untested
def cant_log_in(request):
	return render(request, 'user/cant-log-in.html')

#Untested
#name="forgot_pw_email_sent"
def forgot_pw_email_sent(request):
	'''
	View that gives user small instructions on what to do 
	after they've successfully submitted a password recovery request.
	'''
	return render(request, 'user/forgot-pw-email-sent.html')

#Untested
#name="forgot_pw"
def forgot_password(request):
	#print("[request.post:%s]" % request.POST)
	#print("request data: %s" % request.body)

	if request.method == 'POST':
		form = ForgotPasswordForm(request.POST)

		if form.is_valid():
			# Check if the email address is registered in the database.
			try:
				user = User.objects.get(email = form.cleaned_data['email_address'])

				delivered_msgs = PasswordRecovery.objects.send_pw_recovery_email(user)
				
				if delivered_msgs == 0:
					print("Failed to send password recovery email.")
					code = "send_mail_failed"
					msg = "The password recovery email failed to transmit."
					form.add_error(None, ValidationError(message=msg, code=code))
				else:
					# Email sent successfully. Redirect to success page.
					print("Email sent successfully")
					return HttpResponseRedirect(reverse('user:forgot_pw_email_sent'))
			except ObjectDoesNotExist:
				# User with that email does not exist. Set appropriate form error.
				code = "email_does_not_exist"
				msg = "There exists no registered account with that email address on this site. Are you sure "\
					"that's the correct email address?"
				form.add_error(None, ValidationError(message=msg, code=code))

		context = {'form': form}
		return render(request, 'user/forgot-password.html', context)
	else:
		form = ForgotPasswordForm()
		context = {'form': form}
		return render(request, 'user/forgot-password.html', context)

#Untested
#name="resend_email_code"
def resend_email_code(request):
	return HttpResponse("resent_email_code::view")

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email_address"]
			password = form.cleaned_data["password"]

			user = authenticate(email=email, password=password)

			if user is not None:
				print("User is not None")
				print("user:", user)
				if user.email_verified == False:
					print("Email is unverified")
					CODE = "unverified_email"
					msg = "You must verify your email before logging in. "
					msg += "Please see 'Can't log in' below for instructions."
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
			#valid 
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password1"]

			try:
				user = User.objects.create_user(email, password)
				email_verification_code = user.email_verification_code
				
				#Send verification message to their email
				user.send_email_verification_msg(fail_silently=False)
				
			except IntegrityError:
				msg = "The email address is already registered on our site."
				code = "email_not_unique"
				error = ValidationError(msg, code)
				form.add_error(field = "email", error = error)
				return render(request, 'user/register.html', context={'form':form})

			#return HttpResponse("Automated Test Response:<br>Form is valid. Thank you for registering. <br>[Email: %(email)s]<br>Please verify by your email" % {"email": email})
			#return render(request, 'user/registration-complete')
			return HttpResponseRedirect(reverse('user:user_registration_complete'))
		else:
			return render(request, 'user/register.html', context={'form':form})

		return HttpResponse("This is a post") # Never executes?
	else:
		form = RegistrationForm()
		return render(request, 'user/register.html',context={'form':form})
	
	
def link_warframe_account(request):
	return render(request, 'user/link-wf-account.html')

@login_required
def linked_warframe_account_required(request):
	return render(request, 'user/linked-wfa-required.html')

#Untested
#name="change_pw"
def change_password(request, key):
	'''
	Change a user's password whose password recovery code matches 'key'.
	'''
	password_recovery = None 
	user = None

	KEY_VALIDITY_DURATION = 24*60*60*1000 # Keys (password recovery code) are valid for up to 24 hours

	NO_SUCH_KEY = "Key does not exist" # The key does not exist in the DB
	EXPIRED_KEY = "Key has expired" # They key has expired

	# Check if the key exists in the database
	try:
		password_recovery = PasswordRecovery.objects.get(recovery_code=key)
		user = password_recovery.user_id
	except ObjectDoesNotExist:
		context = {'error': NO_SUCH_KEY}
		#print("NO_SUCH_KEY error")
		return render(request, 'user/change-password.html', context=context)

	key_has_expired = password_recovery.has_recovery_code_expired(KEY_VALIDITY_DURATION)

	# Check if the key has expired
	if key_has_expired:
		context = {'error': EXPIRED_KEY, 'form': None}
		#print("EXPIRED_KEY error")
		return render(request, 'user/change-password.html', context=context)
	
	if request.method == 'POST':
		#print("request.POST is: ", request.POST)
		form = ChangePasswordForm(request.POST)

		#print("request.POST is: " + str(request.POST))

		if form.is_valid():
			#print("form is valid with key: ", key)
			user.set_password(form.cleaned_data['password1'])
			user.save()
			PasswordRecovery.objects.filter(pk=password_recovery.pk).delete()
			return HttpResponseRedirect(reverse("home:index"))
			#redirect user to home page with a flash message.
		else:
			#print("form is invalid!")
			
			context= {'form':form, 'key':key}
			return render(request, 'user/change-password.html', context=context)
	else:
		#print("request method is not POST")
		form = ChangePasswordForm()
		context = {'form': form, 'key':key}
		return render(request, 'user/change-password.html', context=context)

#DEP
def verify_email(request):
	'''
	View displayed when a user registered, requesting them to
	check their email for an email confirmation code. This view
	is also used to redirect users that attempt to access views
	that require the user to have their email verified.
	'''
	pass

#TODO: REMOVE!
def test_send_email_verification_msg(request):
	template_name = "email/email-verification.html"
	context = None
	subject = "Email Verification"
	html_message = render_to_string(template_name, context)

	from django.conf import settings
	from_email = settings.EMAIL_HOST_USER if settings.EMAIL_HOST_USER else None
	
	to = "marilisdiaz@bellsouth.net"

	mail.send_mail(subject=subject, message = "msg2", html_message=html_message, from_email=from_email, recipient_list=[to],)
	
	return HttpResponse("test_send_email_verification_msg :: view")

def user_registration_complete(request):
	#Displays a user registration complete message. 
	#NOTE: "click here to resend confirmation message does not work!"
	return render(request, "user/user-registration-complete.html")

#TODO: REMOVE!
def test_user_registration_complete(request):
	return render(request, "user/user-registration-complete.html")