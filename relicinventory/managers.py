from django.db import models
from django.apps import apps
from django.db.models import Count

from user.models import UserStatus

class RelicManager(models.Manager):
	#Not tested yet
	def get_crowdedness_overview_data(self, gaming_platform, linked_wfa_user=None):
		'''Returns a list of dictionaries. Each dictionary with keys "relic_id", "relic_id__name",
		"count", and (if @user is not None and linked with a warframe account) "owned_relic". Each element
		represents a relic id, along with its name, whether @linked_wfa_user's wfa has the relic in 
		their inventory (if the @linked_wfa_user is not None), and the total numbers of online (and linked) users
		that own the correponding relic on the @gaming_platform gaming platform.

		Example: 

		(If user is None): 
		[{'relic_id' : '23', 'relic_id__relic_name':'Axi S3', 'count':'56'}, ...]

		(If user is not None with a linked warframe account):
		[{'relic_id' : '23', 'relic_id__relic_name':'Axi S3', 'count':'56', 'owned_relic': True}, ...]

		:param gaming_platform:
		:type gaming_platform:
		:param user: The user whose warframe account's inventory should be searched for to determine
		if he has the corresponding relic in the queryset of Relic objects in their inventory.
		:type user: User
		...
		:return: Returns a list of dictionaries. Each dictionary contains the following keys:
		relic_id, relic_id__relic_name, count, and, if @user is not none, owned_relic.
		:rtype: List of dictionaries
		'''
		print("@@@linked_wfa_user is: ", linked_wfa_user)
		if linked_wfa_user != None:
			if linked_wfa_user.is_wfa_linked is False:
				raise ValueError("linked_wfa_user must have a linked Warframe account if linked_wfa_user is not None")

		owned_relic_m = apps.get_model('relicinventory', 'OwnedRelic')
		user_status_m = apps.get_model('user', 'UserStatus')
		relic_m = apps.get_model('relicinventory', 'Relic')
		
		online_user_status = user_status_m.objects.get(user_status_name=user_status_m.ONLINE)

		query_set = owned_relic_m.objects.filter(
			warframe_account_id__user__user_status_id=online_user_status,
			warframe_account_id__gaming_platform_id=gaming_platform.pk
		).select_related(
			'warframe_account_id__user_id__user_status_id',
			'relic',
		).values(
			'relic_id',
			'relic_id__relic_name'
		).annotate(
			count=Count("relic_id")
		).order_by("relic_id")

		#print("qs.query is: ---")
		#print(query_set.query)
		#print("query_set is: ---")
		#print(query_set)

		query_set = list(query_set)

		# All relics that are now in query_set represent those relics that are owned by at least
		# one online user. The query_set does not contain relics that are not owned by users
		# that are currently online. Let's add those relics, along with appropriate corresponding,
		# data, to query_set.
		all_relics = relic_m.objects.all().values_list('relic_id','relic_name')
		RELIC_ID = 0
		RELIC_NAME = 1

		qs_missing_relic_ids = [row["relic_id"] for row in query_set]
		qs_missing_relic_ids = set(qs_missing_relic_ids)

		for relic in all_relics:
			if relic[RELIC_ID] not in qs_missing_relic_ids:

				query_set_item = {
					"relic_id": relic[RELIC_ID],
					"relic_id__relic_name": relic[RELIC_NAME],
					"count": 0
				}

				query_set.append(query_set_item)
		
		# If user is not None, then modify the queryset by adding "owned_relic" key to each 
		# dictionary. owned_relic's value is boolean True if the user owns this relic, False
		# if not.
		if linked_wfa_user is not None:
			user_warframe_account = linked_wfa_user.linked_warframe_account_id

			relic_ids_owned = owned_relic_m.objects.get_relic_ids_of_wfa_owned_relics(user_warframe_account)
			print("relic_ids_owned: ", relic_ids_owned)

			for row in query_set:
				if row["relic_id"] in relic_ids_owned:
					row["owned_relic"] = True
				else:
					row["owned_relic"] = False

		
		
		return query_set



class OwnedRelicManager(models.Manager):

	#Tested
	def create_owned_relic(self, warframe_account, relic, **extra_fields):
		if warframe_account is None or relic is None:
			raise ValueError("warframe_account and relic arguments cannot be None")

		chat_user = self.model(**extra_fields)

		chat_user.warframe_account_id = warframe_account
		chat_user.relic_id = relic

		chat_user.save()

		return chat_user

	#Tested
	def get_wfa_relics(self, warframe_account):
		'''Return a QuerySet of Relic objects that 'warframe_account' has
		logged in his Relics Inventory.

		:param warframe_account: The WarframeAccount instance.
		:type warframe_account: WarframeAccount
		...
		:return: A QuerySet of Relic instances that belong to the user
		:rtype: QuerySet of Relics
		'''
		relic_m = apps.get_model(app_label="relicinventory", model_name="relic") 

		wfa_owned_relics = list(self.filter(warframe_account_id=warframe_account).values_list('relic_id', flat=True))
		relics = relic_m.objects.filter(relic_id__in=wfa_owned_relics)

		return relics

	#Untested
	def get_relic_ids_of_wfa_owned_relics(self, warframe_account):
		'''Returns a set of Relic ids that are in @warframe_account's
		inventory
		'''
		owned_relic_m = apps.get_model("relicinventory", "OwnedRelic")

		owned_relics = owned_relic_m.objects.filter(warframe_account_id=warframe_account)

		return set(owned_relics.values_list("relic_id", flat=True))



	#Tested
	def clear_wfa_inventory(self, warframe_account):
		'''Removes all relics in a Warframe account's inventory
		by deleting all OwnedRelic instances referencing this account.

		:param warframe_account: The WarframeAccount instance used to clear
		the inventory of.
		:type warframe_account: WarframeAccount
		...
		:return: returns the number of objects deleted and a dictionary with the number of deletions per object type
		:rtype: Tuple(Int, Dictionary)
		'''

		return self.filter(warframe_account_id=warframe_account).delete()[0]
		
	
	#Untested
	#Incomplete
	def add_relics_to_inventory(self, warframe_account, relic_ids):
		'''Add relics to a Warframe account's inventory by creating a series of
		OwnedRelic instances. Assumes the relic ids actually exist in the
		database and the user does not already have the relics in
		their inventory.

		:param relic_ids: The IDs of the relics the user would like
		to add to their inventory. 
		:type relic_ids: set of integers
		:param warframe_account: The WarframeAccount instance
		:type warframe_account: WarframeAccount
		'''
		if warframe_account is None or relic_ids is None:
			return []

		relic_m = apps.get_model(app_label='relicinventory', model_name='relic')

		all_relics = relic_m.objects.all()
		relic_ids_set = set(relic_ids) # wrap around a set for efficient search operations
		relics_to_add = [] # relics to add to a users inventory

		# Append all relics that the user wants to add to their inventory
		# to the list of 'relics_to_add'
		for relic in all_relics:
			if relic.relic_id in relic_ids_set:
				print(relic.relic_name + " added to a user's inventory.")
				relics_to_add.append(relic)

		# Create and add the OwnedRelic instances
		# for each Relic in 'relics_to_add' to a list
		# in perpartion for a bulk_create operation.
		owned_relics = []
		for relic in relics_to_add:
			owned_relic = self.model(warframe_account_id = warframe_account, relic_id=relic)
			owned_relics.append(owned_relic)
			print(owned_relic)
		
		self.bulk_create(owned_relics)

		return owned_relics

	

	
	


