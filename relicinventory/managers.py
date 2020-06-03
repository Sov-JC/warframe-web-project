from django.db import models

class RelicManager(models.Manager):
	pass
	
class OwnedRelicManager(models.Manager):

	def get_user_owned_relics(self, user_id):
		'''
		Implement in schema 0.2.0 when owned relic's 
		user_id is removed in favor of warframe_account_id 
		'''

