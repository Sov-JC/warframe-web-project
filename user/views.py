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
		form = LoginForm(request.POST)
		
		if form.is_valid():
			email = form.cleaned_data["email_address"]
			password = form.cleaned_data["password"]

			user = authenticate(username=email, password=password)

			if user is not None:
				login(request, user)
				return HttpResponse("User is not None. Authentication occured but not logged in.")
			else:
				return HttpResponse("User authentication failed")


			return HttpResponse("Form is valid")
		else:
			return HttpResponse("Form invalid!")
	
	form = LoginForm()
	
	context = {'form': form}

	return render(request, 'user/login.html', context)


@login_required
def log_user_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:index'))