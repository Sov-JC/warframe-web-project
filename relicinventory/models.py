from django.conf import settings
from django.db import models
from user.models import User
from .managers import OwnedRelicManager

# Create your models here.
class Relic(models.Model):
    relic_id = models.AutoField(primary_key=True)
    relic_name = models.CharField(max_length=32, unique=True, default=None)
    wiki_url = models.CharField(max_length=512, default=None)

class OwnedRelic(models.Model):
	owned_relic_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		default=None # validation should make sure default doesn't execute
	)
	relic_id = models.ForeignKey(
		'Relic',
		on_delete=models.PROTECT,
		default=None # validation should make sure default doesn't execute
	)

	objects = OwnedRelicManager()

	class Meta:
		db_table = "owned_relic"
		constraints = [
			models.UniqueConstraint(
				fields=['user_id','relic_id'],
				name='unique_relic_owned'
			)
		]

	


	

