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
from django.template.loader import render_to_string
from django.core import mail


# Create your views here.
def index(request):
	return HttpResponse("")

def manager(request):
	return HttpResponse("privatemessage::manager")