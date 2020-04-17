from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm

# Create your views here.
def index(request):
	return HttpResponse("Hello, world. You're at the users index.")

def login(request):

	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			return HttpResponse("Form is valid")
		else:
			return HttpResponse("Form invalid!")
	
	form = LoginForm()
	
	context = {'form': form}

	return render(request, 'login.html', context)

def logout(request):
	return HttpResponse("Not implemented yet")