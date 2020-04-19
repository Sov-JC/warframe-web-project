from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse
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

def logout(request):
	return HttpResponse("Not implemented yet")