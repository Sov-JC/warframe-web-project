from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return HttpResponse("Hello, world. You're at the home index.")
