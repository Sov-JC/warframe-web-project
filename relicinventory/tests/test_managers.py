from django.test import TestCase

from django.db import models
from django.apps import apps
from django.utils import timezone
from django.db.models import Prefetch
from django.db import transaction
from projectutils.utils import query_debugger
from user.models import *
from relicinventory.models import *

from django.db.models import Count, Q

class TestOwnedRelicManager(TestCase):
	fixtures=[
		"user_app-user-status.json", 
		"user_app-gaming-platforms.json",
		"relicinventory_app-relics.json"
	]

	def setUp(self):
		#Create an account. Add two relics to this accounts inventory.
		wfa = WarframeAccount.objects.create_warframe_account("testaccount1")
		relic1 = Relic.objects.get(pk=10)
		relic2 = Relic.objects.get(pk=20)
		owned_relic_one = OwnedRelic.objects.create_owned_relic(wfa, relic1)
		owned_relic_two = OwnedRelic.objects.create_owned_relic(wfa, relic2)

	#Complete
	def test_create_owned_relic_creates_an_owned_relic(self):
		'''
		Should save an OwnedRelic instance with an existing
		warframe_account and relic passed in as arguments
		to the function.
		'''
		wfa1 = WarframeAccount.objects.create_warframe_account("warframeaccount1")
		relic = Relic.objects.get(pk=100)
		OwnedRelic.objects.create_owned_relic(wfa1, relic)

		owned_relic_get = OwnedRelic.objects.get(warframe_account_id=wfa1, relic_id=relic)

		msg = "OwnedRelic instance should have been saved to the database, but it was "\
			"not found in the database after it was created."
		self.assertEqual(owned_relic_get.relic_id.pk, 100, msg=msg)

	#Complete
	def test_get_wfa_relics_gets_all_relics_in_wfa_inventory(self):
		'''
		Should return all relics that a user has logged in their inventory
		as a QuerySet of Relic instances.
		'''
		wfa1 = WarframeAccount.objects.create_warframe_account("warframe1")
		relic = Relic.objects.get(pk=2)
		
		msg = "Newly created warframe account instance should have no relics logged " \
			"in their inventory."
		self.assertEqual(0, len(OwnedRelic.objects.get_wfa_relics(wfa1)), msg=msg)

		owned_relic = OwnedRelic.objects.create_owned_relic(wfa1, relic)

		msg="One relic is supposed to be in the Warframe account's inventory."
		relics = OwnedRelic.objects.get_wfa_relics(wfa1)
		self.assertEqual(1, len(relics), msg=msg)

		msg = "Expected relic to have a primary key of 2."
		self.assertEqual(relics[0].pk, 2, msg)



