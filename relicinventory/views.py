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


@login_required
def my_inventory(request):
	linked_wfa = request.user.linked_warframe_account_id
	if linked_wfa is None:
		#TODO: replace this with a redirect.
		return HttpResponse("Linked Warframe Account Required.") #for now
	else:
		relics_in_inventory = OwnedRelic.objects.get_wfa_relics(linked_wfa)
		ids_relics_in_inventory = relics_in_inventory.values_list('relic_id', flat=True)

		#The ids of the relics the user owned as a set of ids
		relic_ids_owned = set(ids_relics_in_inventory)

		all_relics = Relic.objects.all()

		relic_names = Relic.objects.all().values_list('relic_name', flat=True)
		relic_names = list(relic_names)
		relic_names = {"relic_names": relic_names}

		# List of all relics in the database as a list of pairs
		all_relics_json_script = list(Relic.objects.all().values_list('relic_id', 'relic_name'))

		# Convert into a dictionary to make use of json_script in template
		all_relics_json_script = {'relics': all_relics_json_script}

		context = {'relic_ids_owned':relic_ids_owned, 'all_relics': all_relics, "all_relics_json_script": all_relics_json_script}
		return render(request, 'relicinventory/my-inventory.html', context = context)

@login_required
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

				msg = {'success': 'Inventory updated successfully.'}
				
				# Clear the Warframe account's inventory.
				try:
					OwnedRelic.objects.filter(warframe_account_id=linked_wfa).delete()
					OwnedRelic.objects.add_relics_to_inventory(linked_wfa, checked_relic_ids)
				except Exception as e:
					print(e)
					msg = {'error': 'Inventory failed to update'}

				response = msg
				
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

	
	
	
	
