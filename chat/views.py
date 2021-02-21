from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#untested
@login_required
def manager(request):
	return render(request, template_name="chat/chat-manager.html")

#not tested
@login_required
@csrf_exempt
def ajax_delete_chat(request):

	is_in_chat = False #

	response = None
	if is_in_chat:
		#delete chat
		pass
	else:
		#return 403 - forbidden access.
		response = JsonResponse({"error": "Attempted to delete a chat the user is not in."})
		response.status_code = 403

	return response

	





