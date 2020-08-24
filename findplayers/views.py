from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from relicinventory.models import OwnedRelic, Relic
from user.models import User, WarframeAccount, GamingPlatform
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def index(request):
	return HttpResponse("")

#name="search"
def search(request):
	relic_name = request.GET.get('relic_name', '')
	print('[relic_name:%s]' % relic_name)
	
	user = None
	if request.user.is_authenticated and request.user.is_wfa_linked:
		user = request.user
	
	# Obtain the gaming platform from request cookies. Return a 404 if invalid gaming platform.
	gaming_platform_cookie_value = request.COOKIES.get("gaming-platform", None)
	gaming_platform = None
	if gaming_platform_cookie_value is None:
		GamingPlatform.objects.get(platform_name = GamingPlatform.PC)
	else:
		gaming_platform = get_object_or_404(GamingPlatform,
			platform_name__iexact=gaming_platform_cookie_value
		)

	relic = None
	try:
		relic = Relic.objects.get(relic_name__iexact=relic_name)
		print("Relic.objects.get(relic_name__icontains=relic_name) queryset ---")
		print(Relic.objects.get(relic_name__iexact=relic_name).query)
	except ObjectDoesNotExist:
		relic = None


	crowdedness_overview = Relic.objects.get_crowdedness_overview_data(
		gaming_platform=gaming_platform,
		linked_wfa_user=user,
	)
	
	# Set up context variables depending on whether or not a search was made for a particular relic.
	if relic == None:
		# A search for a relic was not made

		context = {'relic': None, 'crowdedness_overview': crowdedness_overview}
		return render(request, 'findplayers/search.html', context=context)
	else:
		# No search for a relic was made
		wfa_ids = WarframeAccount.objects.get_linked_wfas_that_own_relic_on_platform(relic, gaming_platform)
		wfa_ids = list(wfa_ids)

		wfas = WarframeAccount.objects.get(pk__in=wfa_ids)

		context = {'relic': relic, 'warframe_accounts': wfas, 'crowdedness_overview': crowdedness_overview}
		return render(request, 'findplayers/search.html', context=context)
	
	
