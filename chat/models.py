from django.db import models
from django.conf import settings

from user.models import User
from user.models import WarframeAccount

from .managers import *

# Create your models here.
class Chat(models.Model):
	chat_id = models.AutoField(primary_key=True)
	date_created = models.DateTimeField(auto_now_add=True, blank=True)
	person_one_warframe_account_id = models.ForeignKey(
		WarframeAccount,
		on_delete=models.PROTECT,
		related_name = "person_one_wf_account_id", #this is prob incorrect - might need to name it something like 'chat_person_one'
		default=None,
	)
	person_two_warframe_account_id = models.ForeignKey(
		WarframeAccount,
		on_delete=models.PROTECT,
		related_name = "person_two_wf_account_id", #this is prob incorrect
		default=None,
	)
	
	person_one_still_in_chat = models.BooleanField(default=True)
	person_two_still_in_chat = models.BooleanField(default=True)

	objects = ChatManager()
	
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
		on_delete = models.CASCADE,
		default=None
	)
	formUserID = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete = models.PROTECT,
		default=None
	)
	message = models.CharField(max_length=45, default=None)
	message_created = models.DateTimeField(auto_now_add=True, blank=True)

	objects = ChatMessageManager()

	class Meta:
		db_table = 'chat_chat_message'
