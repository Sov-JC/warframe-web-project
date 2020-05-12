from django.db import models
from django.conf import settings

from user.models import User
from user.models import WarframeAccount

# Create your models here.
class Chat(models.Model):
	chat_id = models.AutoField(primary_key=True)
	date_created = models.DateTimeField(auto_now_add=True, blank=True)
	person_one_warframe_account_id = models.ForeignKey(
		WarframeAccount,
		on_delete=models.PROTECT
	)
	person_two_warframe_account_id = models.ForeignKey(
		WarframeAccount,
		on_delete=models.PROTECT
	)
	
	person_one_still_in_chat = models.BooleanField(default=True)
	person_two_still_in_chat = models.BooleanField(default=True)
	
	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields = [
					'person_one_warframe_account_id',
					'person_two_warframe_account_id',
				],
				name = 'different_warframe_accounts_in_private_chat'
			)
		]


class ChatMessage(models.Model):
	chat_message_id = models.AutoField(primary_key=True)
	chat_id = models.ForeignKey(
		Chat,
		on_delete = models.CASCADE
	)
	formUserID = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.PROTECT
	)
	message = models.CharField(max_length=45)
	message_created = models.DateTimeField(auto_now_add=True, blank=True)

	class Meta:
		db_table = 'chat_chat_message'
