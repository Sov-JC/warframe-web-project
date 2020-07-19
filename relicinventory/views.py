from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Relic, OwnedRelic
from django.views.decorators.csrf import csrf_exempt
import json



# Create your views here.
#Untested
@login_required
def my_inventory(request):
	linked_wfa = request.user.linked_warframe_account_id
	if linked_wfa is None:
		#TODO: replace this with a redirect.
		return HttpResponse("Linked Warframe Account Required.") #for now
	else:
		relics_in_inventory = OwnedRelic.objects.get_wfa_relics(linked_wfa)
		ids_relics_in_inventory = relics_in_inventory.values_list('relic_id', flat=True)

		#The ids of the relics the user owned as a set of relic ids
		relic_ids_owned = set(ids_relics_in_inventory)

		all_relics = Relic.objects.all()

		context = {'relic_ids_owned':relic_ids_owned, 'all_relics': all_relics}
		return render(request, 'relicinventory/my-inventory.html', context = context)

#Untested
#@login_required
#@csrf_exempt
def ajax_save_inventory_changes(request):
	
	linked_wfa = request.user.linked_warframe_account_id
	if linked_wfa is not None:
		if request.is_ajax():
			if request.method == 'PUT':
				print("PUT method detected.")
				print("request.body: " + str(request.body))

				checked_relic_ids = json.loads(request.body)
				print("checked_relic_ids: ")
				print(checked_relic_ids)
				
				# Clear the Warframe account's inventory.
				OwnedRelic.objects.filter(warframe_account_id=linked_wfa).delete()
				OwnedRelic.objects.add_relics_to_inventory(linked_wfa, checked_relic_ids)

				response = {'success': 'Inventory updated successfully.'}
				
				return JsonResponse(response)
			else:
				response = {'error': 'Request method must be PUT.'}
				return JsonResponse(response) # Request method must 'PUT'
		else:
			response = {'error': 'Request must be Ajax.'}
			raise Http404() # Request must be through Ajax only
	else:
		#linked wfa required
		response = {'error': 'Linked warframe account required'}
		return JsonResponse(response)

	
	
	
	
