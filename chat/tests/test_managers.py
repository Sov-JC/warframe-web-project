from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.models import *
from django.contrib import auth
from django.utils import timezone
from django.db.models import Q

from projectutils.utils import query_debugger


# Create your tests here.
class TestChatManager(TestCase):
	fixtures=["user_app-user-status.json", "user_app-gaming-platforms.json"]

	def setUp(self):
		'''
		Create a chat between Joe and Daniel, with some messages
		between these two users within this chat. Create an additional user, Vanessa,
		that is not in the chat with anyone.
		'''

		#create warframe accounts for joe, daniel, and vanessa
		joe_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="joe_wfa")
		daniel_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="daniel_wfa")
		vanessa_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="vanessa_wfa")

		# Create a chat for joe_wfa and daniel_wfa
		chat_joe_and_daniel = Chat.objects.create()

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
			message = "Hi!",
			datetime_created = timezone.now()
		)
		#a message from daniel to joe
		daniel_to_joe_msg_1 = ChatMessage(
			chat_user_id = chat_user_daniel,
			message = "Howdy!",
			datetime_created = timezone.now()
		)

		joe_to_daniel_msg_1.save()
		daniel_to_joe_msg_1.save()

	def test_get_chat_user_partner_returns_correct_partner(self):
		joe_wfa = WarframeAccount.objects.get(warframe_alias="joe_wfa")
		daniel_wfa = WarframeAccount.objects.get(warframe_alias="daniel_wfa")

		# Get all instances of joe as a chat user. Do the same for daniel.
		chat_users_joe = ChatUser.objects.select_related('chat_id').filter(warframe_account_id=joe_wfa)
		chat_users_daniel = ChatUser.objects.select_related('chat_id').filter(warframe_account_id=daniel_wfa)

		# Obtain all the chats that joe and daniel belong to as an array
		chats_with_joe = [chat_user.chat_id for chat_user in chat_users_joe]
		chats_with_daniel = [chat_user.chat_id for chat_user in chat_users_daniel]
		
		# Get the chat_ids
		chats_with_joe_as_ids = [chat.chat_id for chat in chats_with_joe]
		chats_with_daniel_as_ids = [chat.chat_id for chat in chats_with_daniel]
		print("chats_with_joe_as_ids:")
		print(chats_with_joe_as_ids)
		print("chats_with_daniel_as_ids:")
		print(chats_with_daniel_as_ids)

		chat_ids_containing_joe_and_daniel = chats_with_joe_as_ids + (chats_with_daniel_as_ids)
		print("chat_ids_containing_joe_and_daniel:")
		print(chat_ids_containing_joe_and_daniel)

		chat_with_joe_and_daniel = Chat.objects.filter(chat_id__in = chat_ids_containing_joe_and_daniel)[0]
		print("chats with joe and daniel")
		print(chat_with_joe_and_daniel)

		joe_partner = Chat.objects.get_chat_user_partner(chat_user = joe_wfa, chat=chat_with_joe_and_daniel)
		daniel_partner = Chat.objects.get_chat_user_partner(chat_user = daniel_wfa, chat=chat_with_joe_and_daniel)

		self.assertEqual(joe_partner.warframe_account_id.warframe_alias, "daniel_wfa",
			msg="Expected daniel to be joe's chat partner for the chat with joe and daniel")
		self.assertEqual(daniel_partner.warframe_account_id.warframe_alias, "joe_wfa",
			msg="Expected joe to be daniel's partner for the chat with joe and daniel")



		'''
		print("chats_with_joe_and_daniel:")
		print(chats_with_joe_and_daniel)
		
		print("chats_with_joe:")
		print(chats_with_joe)
		print("chats_with_daniel:")
		print(chats_with_daniel)

		chat_ids_with_joe = ChatUser.objects.select_related('chat_id').filter(warframe_account_id=joe_wfa).only('chat_id')
		print("chat_ids_with_joe:")
		print(chat_ids_with_joe)
		print("[0]")
		print(chat_ids_with_joe[0])
		'''
		

		"""
		chats_with_joe_or_daniel = Chat.objects.raw(
			'''
			select c.*
			from chat_chat as c
			where c.chat_id in (
				select chat_chat.chat_id
				from ((chat_chat natural join chat_chat_user) natural join user_warframe_account)
				where warframe_alias = "joe_wfa" or warframe_alias = "daniel_wfa"
			)
			'''
		)
		"""
		
		return

	def test_get_chat_containing_warframe_accounts_returns_correct_chat(self):
		'''
		Should return the corresponding Chat that warframe_account instances
		'wfa_one' and 'wfa_two' belong to.
		'''
		joe_wfa = WarframeAccount.objects.get(warframe_alias="joe_wfa")
		daniel_wfa = WarframeAccount.objects.get(warframe_alias="daniel_wfa")

		# From the set-up, there is only one chat initialized, and that chat is the chat
		# between joe and daniel. Let's get that chat.
		chats = Chat.objects.all()
		msg = "There should only be one chat at this point (the chat between Joe and Daniel)"
		self.assertEqual(1, len(chats), msg=msg)
		chat_with_joe_and_daniel = Chat.objects.get(chat_id=chats[0].chat_id)

		#get the chat the test function responds with given 'joe_wfa' and 'daniel_wfa' as arguments
		chat_with_joe_and_daniel_test = Chat.objects.get_chat_containing_warframe_accounts(joe_wfa, daniel_wfa)

		self.assertEqual(chat_with_joe_and_daniel_test, chat_with_joe_and_daniel)

	def test_get_chat_containing_warframe_accounts_returns_none_when_two_accounts_not_in_chat_together(self):
		"""
		Should return none if two warframe accounts are not in the same chat together
		"""
		#get warframe accounts from setUp
		daniel_wfa = WarframeAccount.objects.get(warframe_alias="daniel_wfa")
		joe_wfa = WarframeAccount.objects.get(warframe_alias="joe_wfa")

		# Create two new users that are in a chat with each other, carl and ariel
		carl_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="carl_wfa")
		ariel_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="ariel_wfa")
		carl_wfa.save()
		ariel_wfa.save()

		ariel_and_carl_chat = Chat(datetime_created=timezone.now())
		ariel_and_carl_chat.save()

		chat_user_carl = ChatUser(
			warframe_account_id=carl_wfa,
			chat_id = ariel_and_carl_chat,
			still_in_chat = True,
			datetime_left_chat = None,
			datetime_last_viewed_chat = timezone.now()
		)

		chat_user_carl.save()

		chat_user_ariel = ChatUser(
			warframe_account_id=ariel_wfa,
			chat_id = ariel_and_carl_chat,
			still_in_chat = True,
			datetime_left_chat = None,
			datetime_last_viewed_chat = timezone.now()
		)

		chat_user_ariel.save()

		# call the function with carl and joe, two users that are not in a chat together
		test_call_one = Chat.objects.get_chat_containing_warframe_accounts(carl_wfa, joe_wfa)
		msg = "carl and joe are not suppose to be in the same chat"
		self.assertEqual(None, test_call_one, msg=msg)

		# call the function with carl and ariel, two users that are not in a chat together
		test_call_two = Chat.objects.get_chat_containing_warframe_accounts(joe_wfa, ariel_wfa)
		msg = "carl arial are not suppose to be in the same chat"
		self.assertEqual(None, test_call_two, msg=msg)
	
	def test_chats_wfa_still_in_returns_correct_chats(self):
		bob_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="bob123123")

		#Create 5 different warframe accounts. Create 5 chats,
		#each being between bob_wfa and one of the warframe accounts generated.

		warframe_accounts = []
		for i in range(5):
			warframe_alias = "warframe_alias"+str(i)
			warframe_account = WarframeAccount.objects.create_warframe_account(warframe_alias=warframe_alias)
			warframe_accounts.append(warframe_account)
				
		chat_users_excluding_bob = []
		chat_users_excluding_bob_pks = []
		for i in range(5):
			chat = Chat.objects.create_chat()

			chat_user_bob = ChatUser.objects.create_chat_user(warframe_account_id=bob_wfa,chat_id=chat)

			chat_user = ChatUser.objects.create_chat_user(warframe_account_id=warframe_accounts[i], chat_id=chat)
			chat_users_excluding_bob.append(chat_user)
			chat_users_excluding_bob_pks.append(chat_user.pk)

			print("chat_users of chat:" + str(chat))
			print("\t" + str(chat.chatuser_set.all()))
		
		chats_bob_in = Chat.objects.chats_wfa_still_in(bob_wfa)
		self.assertEqual(len(chats_bob_in), 5, msg="bob is suppose to be in 5 chats")

	#TODO: Reread
	@query_debugger
	def test_chats_wfa_has_been_in_returns_correct_chats(self):
		# create an additional chat betwen joe and vanessa with no messages between
		# the two of them 
		#settings.DEBUG = True

		joe_wfa = WarframeAccount.objects.get(warframe_alias="joe_wfa")
		vanessa_wfa = WarframeAccount.objects.get(warframe_alias="vanessa_wfa")
		
		daniel_wfa = WarframeAccount.objects.get(warframe_alias="daniel_wfa")
		
		joe_and_vanessa_chat = Chat.objects.create_chat()

		# create chat users
		chat_user_joe = ChatUser.objects.create_chat_user(joe_wfa, joe_and_vanessa_chat)
		chat_user_vanessa = ChatUser.objects.create_chat_user(vanessa_wfa, joe_and_vanessa_chat)

		# create chat
		chats_joe_has_been_in = Chat.objects.chats_wfa_has_been_in(warframe_account=joe_wfa)

		'''
		Joe should be in two chats. One between him and daniel (from the setUp), the other
		with him and vanessa 
		'''
		chats_joe_been_in = Chat.objects.chats_wfa_has_been_in(joe_wfa)
		chats_vanessa_been_in = Chat.objects.chats_wfa_has_been_in(vanessa_wfa)
		self.assertEqual(len(chats_joe_been_in), 2)
		self.assertEqual(len(chats_vanessa_been_in), 1)		
		
		joe_as_chat_user = ChatUser.objects.all().filter(warframe_account_id=joe_wfa)
		daniel_as_chat_user = ChatUser.objects.all().filter(warframe_account_id=daniel_wfa)

		list1 = joe_as_chat_user.value_list('chat_id') #chats joe is in
		list2 = daniel_as_chat_user.value_list('chat_id') #chats daniel is in

		#get the chat_id of the chat that joe and daniel are in
		chat_id_joe_and_daniel_are_in = list(set(list1) & set(list2))
		self.assertEqual(1, len(chat_id_joe_and_daniel_are_in), msg="Joe and daniel should only be in one chat")

		msg = "Joe and vanessa chat is suppose to be a chat that joe has been in"
		self.assertEqual((joe_and_vanessa_chat in chats_joe_been_in), True, msg)
		
		return 

	def test_DEBUG_get_chats_wfa_still_in(self):
		
		#create 50 chats. Joe is in each chat. 
		#in each chat the Joe is in, Joe has one 
		#other random person in it
		wfa_alias_1 = "joe"
		wfa_1 = WarframeAccount.objects.create_warframe_account(warframe_alias=wfa_alias_1)
		
		for chat in range(50):
			some_chat = Chat.objects.create_chat()

			wfa_alias_2 = ''.join(random.choice('abcdefghiklmn') for i in range(10))
			
			wfa_2 = WarframeAccount.objects.create_warframe_account(warframe_alias=wfa_alias_2)

			chat_user_1 = ChatUser.objects.create_chat_user(warframe_account_id=wfa_1, chat_id=some_chat)
			chat_user_2 = ChatUser.objects.create_chat_user(warframe_account_id=wfa_2, chat_id=some_chat)

		Chat.objects.get_chats_wfa_still_in(None)

	def test_chats_with_new_msgs(self):
		'''
		Should return the correct chats that a user has received new messages from
		'''
		# Create two chats. Each chat contains two users, and each of the chats will contain at least
		# one new msg for one of the two users in the chat.

		#Create the first chat 

		bob_wfa = WarframeAccount.objects.create_warframe_account("bob_wfa")
		dan_wfa = WarframeAccount.objects.create_wareframe_account("bob_wfa")
		
		chat1 = Chat.objects.create_chat()

		bob_chat1_user = ChatUser.objects.create_chat_user(bob_wfa, chat1)
		dan_chat1_user = ChatUser.objects.create_chat_user(dan_wfa, chat1)

		bob_to_dan_msg_0 = ChatMessage.objects.create_chat_message(bob_chat1_user, "hi")
		dan_to_bob_msg_0 = ChatMessage.objects.create_chat_message(dan_chat1_user, "howdy")
		dan_to_bob_msg_1 = ChatMessage.objects.create_chat_message(dan_chat1_user, "eyy")

		# bob should now have 2 new message from dan because the messages from dan to bob
		# was created after bob's corresponding 'datetime_last_viewed_chat' value was
		# initialized.
		#
		# similarly dan should have 1 new message from bob.
		
		self.assertEqual(Chat.objects.chats_with_new_msgs(bob_wfa), 2)

		self.assertEqual(Chat.objects.chats_with_new_msgs(dan_wfa), 1)

	@query_debugger
	def test_DEBUG_chats_with_new_msgs(self):
		#create 5 chats and warframe accounts
		chats = []
		wfas = []
		for i in range(5):
			chats.append(Chat.objects.create_chat())
			wfa_alias= ("warframe"+str(i))
			wfas.append(WarframeAccount.objects.create_warframe_account(wfa_alias))

		#to chats[0] add two chat users, warframe0 and warframe1
		
		main_chat = Chat.objects.create_chat()

		bob_wfa = WarframeAccount.objects.create_warframe_account("bob_wfa")
		dan_wfa = WarframeAccount.objects.create_warframe_account("dan_wfa")

		self.assertEqual(Chat.objects.chats_with_new_msgs(bob_wfa), 0)
		self.assertEqual(Chat.objects.chats_with_new_msgs(dan_wfa), 0)
		
		bob_chat_user = ChatUser.objects.create_chat_user(bob_wfa, main_chat)
		dan_chat_user = ChatUser.objects.create_chat_user(dan_wfa, main_chat)

		msg_from_bob_wfa0 = ChatMessage.objects.create_chat_message(bob_chat_user, "eyy")
		msg_from_bob_wfa1 = ChatMessage.objects.create_chat_message(bob_chat_user, "dewd")
		msg_from_bob_wfa2 = ChatMessage.objects.create_chat_message(bob_chat_user, "waaaazaaaaa!")

		msg_from_dan_wfa0 = ChatMessage.objects.create_chat_message(dan_chat_user, "yo dood who u iz?")
	
	def debugger(self):
		pass

		