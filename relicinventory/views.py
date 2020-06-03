from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
@login_required
def my_inventory(request):

	if request.user.is_authenticated:
		return render(request, 'relicinventory/my-inventory.html')
	
	
	pass
