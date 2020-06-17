from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.models import *
from django.contrib import auth
from django.utils import timezone


# Create your tests here.
class TestChatManager(TestCase):
	fixtures=["user_app-user-status.json", "user_app-gaming-platforms.json"]

	def setUp(self):
		#create warframe accounts for joe, daniel, and vanessa
		joe_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="joe_wfa")
		daniel_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="daniel_wfa")
		vanessa_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="vanessa_wfa")

		#create a chat that will be used between joe and daniel, and joe and vanessa
		chat_joe_and_daniel = Chat.objects.create()
		chat_joe_and_vanessa = Chat.objects.create()

		#create the chat_users for the chat 'chat_joe_and_daniel'.
		chat_user_joe = ChatUser(
			warframe_account_id=joe_wfa,
			chat_id = chat_joe_and_daniel,
			still_in_chat = True,
			datetime_left_chat = None,
			datetime_last_viewed_chat = timezone.now()
		)
		chat_user_joe.save()

		chat_user_daniel = ChatUser(
			warframe_account_id=daniel_wfa,
			chat_id = chat_joe_and_daniel,
			still_in_chat = True,
			datetime_left_chat = None,
			datetime_last_viewed_chat = timezone.now()
		)
		chat_user_daniel.save()

		#add joe and daniel to the chat and save these two chat users
		chat_user_joe.chat_id = chat_joe_and_daniel
		chat_user_daniel.chat_id = chat_joe_and_daniel

		chat_user_joe.save()
		chat_user_daniel.save()

		#joe and daniel are now in a chat but with no messages sent between them.
		#let's create some messages between joe and daniel

		#a message from joe to daniel saying "hi"
		joe_to_daniel_msg_1 = ChatMessage(
			chat_user_id = chat_user_joe,
			message = "hi",
			datetime_created = timezone.now()
		)
		#a message from daniel to joe
		daniel_to_joe_msg_1 = ChatMessage(
			chat_user_id = chat_user_daniel,
			message = "howdy!",
			datetime_created = timezone.now()
		)

		joe_to_daniel_msg_1.save()
		daniel_to_joe_msg_1.save()

	def test_get_chat_user_partner_returns_correct_partner(self):
		joe_wfa = WarframeAccount.objects.get(warframe_alias="joe_wfa")
		daniel_wfa = WarframeAccount.objects.get(warframe_alias="daniel_wfa")

		print("joe_wfa is:")
		print(joe_wfa)
		
		joe_chat_user_instances = ChatUser.objects.select_related('chat_id').filter(warframe_alias="joe_wfa")

		chats_joe_belongs_to = joe_chat_user_instances.order_by('chat_id').using('chat_id')

		chat_ids_joe_belongs_to = [chat.chat_id for chat in chats_joe_belongs_to]
		
		print("chat_ids joe belongs to:")
		print(chat_ids_joe_belongs_to)
		
		
		
		# chat_user.objects.selected_related.filter()


		# chat_user = ChatUser.objects.get(warframe_account_id="joe_wf")
		# chat.objects.get_chat_user_partner(

		pass