from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from relicinventory.models import OwnedRelic
# Create your views here.


def index(request):
	return HttpResponse("")

#name="search"
def search(request):
	return HttpResponse("a:findplayers - search")
