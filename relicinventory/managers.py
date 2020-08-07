from django.db import models
from django.apps import apps

class RelicManager(models.Manager):
	pass
	
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


