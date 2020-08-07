from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from django.contrib import auth

class TestMyInventoryView(TestCase):
	fixtures = [
		"relicinventory_app-relics.json",
		"user_app-gaming-platforms.json",
		"user_app-user-status.json"
	]

	def setUp(self):
		'''
		Create a test user with email 'testuser@example.com' with a linked
		warframe account 'warframeaccount1'. Log the user in.
		'''
		email = 'testuser@example.com'
		password = 'testPassword123'

		wfa1 = WarframeAccount.objects.create_warframe_account(
			warframe_alias="warframeaccount1",
		)
		
		User.objects.create_user(
			email=email,
			linked_warframe_account_id=wfa1,
			password=password)

		self.client.login(email=email, password=password)


	def test_view_inventory_with_unlinked_wfa_redirects_user(self):
		''' Should redirect a user that attempts to
		visit the Relic Inventory modification page if 
		the user does not have a Warframe account linked with 
		their site account.'''
		self.fail()

	def test_view_inventory_with_linked_warframe_account_displays_every_relic_in_db_as_option(self):
		'''
		The relic inventory page should display a list of every relic in the database,
		allowing them to check or uncheck the relic the own.
		'''
		#email = "testuser@example.com"
		#password = "testPassword123"
		#self.client.login(email="testuser@example.com", password=password)

		#self.client.login()

		all_relics = Relic.objects.all()

		response = self.client.get(reverse('relicinventory:my-inventory'))

		self.assertEqual(response.status_code, 200)

		print("response.context['all_relics']: " + str(response.context['all_relics']))
		all_relics_context = response.context['all_relics']

		relic_ids = set()
		for relic in all_relics_context:
			relic_ids.add(relic.pk)

		msg="Not all relics were passed passed to the relic inventory view"
		self.assertEqual(len(all_relics_context), len(all_relics), msg=msg)

	def test_owned_relic_are_sent_to_context(self):
		'''
		Should pass a list of relic ids that the user owns.
		'''
		relic = Relic.objects.get(pk=1)
		wfa = User.objects.get(email="testuser@example.com").linked_warframe_account_id
		owned_relic = OwnedRelic.objects.create_owned_relic(warframe_account=wfa, relic=relic)

		response = self.client.get(reverse('relicinventory:my-inventory'))

		self.assertEqual(response.status_code, 200)

		msg = "View should have passed the relic ids of relics the user owns."
		self.assertEqual(len(response.context['relic_ids_owned']), 1, msg=msg)
		self.assertEqual(list(response.context['relic_ids_owned'])[0], owned_relic.relic_id.pk, msg=msg)

class TestAjaxSaveInventoryChangesView(TestCase):
	fixtures = [
		"relicinventory_app-relics.json",
		"user_app-gaming-platforms.json",
		"user_app-user-status.json"
	]

	def setUp(self):
		'''
		Create a test user with email 'testuser@example.com' with a linked
		warframe account 'warframeaccount1'. Log the user in.
		'''
		email = 'testuser@example.com'
		password = 'testPassword123'

		wfa1 = WarframeAccount.objects.create_warframe_account(
			warframe_alias="warframeaccount1",
		)
		
		User.objects.create_user(
			email=email,
			linked_warframe_account_id=wfa1,
			password=password)

		self.client.login(email=email, password=password)

	def test_unlinked_warframe_account_returns_error_json_response(self):
		'''
		If a request is made with a logged in user but with no warframe account linked, the
		user should be redirected.
		'''
		raise NotImplementedError

	def test_logged_and_linked_user_attemts_to_change_inventory_in_method_other_than_ajax_returns_404(self):
		'''
		A logged in and linked user that has requested this view in a form that is not ajax
		should raise an Http 404 error.
		'''
		response = self.client.get(reverse('relicinventory:save-changes'))

		self.assertEqual(response.status_code, 404)

	def test_logged_in_and_linked_user_making_non_put_ajax_request_returns_json_error_msg(self):
		'''
		An ajax request from a logged in and linked user that is not a PUT method should
		return a JSON response containing an error informing the request must be in Ajax.
		'''
		
		response = self.client.get(reverse('relicinventory:save-changes'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		self.assertEqual(response.status_code, 200)

		msg="A non PUT method request from a logged in and linked user should have returned \
			an error message via JSON response"
		
		json_response = str(response.content, encoding='utf8')

		self.assertJSONEqual(json_response, {'error': 'Request method must be PUT.'}, msg=msg)

	def test_logged_and_linked_user_makes_put_ajax_request_returns_success_msg_as_json_response(self):
		'''
		A PUT ajax request made by a logged in an linked user should return a success
		msg if the inventory was updated successfully given the checked relic ids passed
		as data with the Ajax request. Additionally, the inventory must be updated
		appropriately.
		'''
		relic1 = Relic.objects.get(pk=1)
		relic2 = Relic.objects.get(pk=2)

		data = [relic1.pk, relic2.pk]
		response = self.client.put(reverse('relicinventory:save-changes'), data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

		self.assertEqual(response.status_code, 200)

		wfa = WarframeAccount.objects.get(warframe_alias="warframeaccount1")

		owned_relics = OwnedRelic.objects.filter(warframe_account_id = wfa).order_by('relic_id')

		# Get the pks of the relic the user has in his inventory
		relic_ids_in_inventory = [owned_relic.relic_id.pk for owned_relic in owned_relics]

		msg = "Two relics should have been added to the user's inventory"
		self.assertEqual(len(owned_relics), 2, msg=msg)

		msg = "Two relics (with primary keys 1 and 2) should have been added to the user's inventory"
		self.assertListEqual(relic_ids_in_inventory, [relic1.pk, relic2.pk], msg=msg)

		msg = "Expected a JSON response with the success message 'Inventory updated successfully'"
		self.assertJSONEqual(response.content, {'success':'Inventory updated successfully.'}, msg=msg)


	def test_logged_and_linked_user_makes_makes_put_ajax_request_returns_error_msg_json_response_if_inventory_update_failed(self):
		'''
		A PUT ajax request made by a logged in an linked user should return an error message
		if the inventory failed to update successfully given the checked relic ids passed as data 
		with the Ajax request.
		'''
		self.fail()

	def test_json_data_transfer_in_incorrect_format(self):
		'''
		Json data received must be an array of integers and the array length
		should not be more than twice the total number of relics 
		'''
		self.fail()







