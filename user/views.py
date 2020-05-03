from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import LoginForm

# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the users index.")

def login_view(request):
	if request.method == 'POST':
		print("request is 'POST'")
		form = LoginForm(request.POST)
		if form.is_valid():
			print("form is valid")
			email = form.cleaned_data["email_address"]
			password = form.cleaned_data["password"]

			print("[email:" + email +"]")
			print("[password: " + password + "]")

			user = authenticate(email=email, password=password)

			if user is not None:
				print("user is not 'None', attempting to login...")
				login(request, user)
				print("login execed")
				return HttpResponseRedirect(reverse('home:index'))
			else:
				return render(request, 'user/login.html', context={'form':form})
		else:
			print("form is invalid")
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
		if "wf_alias" in request.GET :
			return HttpResponse("wf_alias exists")
		else:
			return HttpResponse("wf_alias does not exist")
	else:
		return HttpResponse("This is not a GET method, expected GET request.")