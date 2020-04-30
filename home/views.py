from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request, 'home/index.html', context=None)
	
