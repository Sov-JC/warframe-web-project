from django.conf import settings
from django.db import models
from user.models import User, WarframeAccount
from .managers import RelicManager, OwnedRelicManager

# Create your models here.
class Relic(models.Model):
	relic_id = models.AutoField(primary_key=True)
	relic_name = models.CharField(max_length=32, unique=True, default=None)
	wiki_url = models.CharField(max_length=512, default=None)

	objects = RelicManager()

	class Meta:
		db_table = "relicinventory_relic"

class OwnedRelic(models.Model):
	owned_relic_id = models.AutoField(primary_key=True)
	warframe_account_id = models.ForeignKey(
		WarframeAccount,
		on_delete=models.PROTECT,
		default=None, # validation should make sure default doesn't execute
		db_column="warframe_account_id"
	)
	relic_id = models.ForeignKey(
		'Relic',
		on_delete=models.CASCADE,
		default=None, # validation should make sure default doesn't execute
		db_column="relic_id"
	)

	objects = OwnedRelicManager()

	class Meta:
		db_table = "relicinventory_owned_relic"
		constraints = [
			models.UniqueConstraint(
				fields=['warframe_account_id','relic_id'],
				name='unique_relic_owned'
			)
		]