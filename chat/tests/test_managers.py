from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.models import *
from django.contrib import auth
from django.utils import timezone
from django.db.models import Q
import time

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
			#still_in_chat = True,
			#datetime_left_chat = None,
			#datetime_last_viewed_chat = timezone.now()
		)
		chat_user_joe.save()

		chat_user_daniel = ChatUser(
			warframe_account_id=daniel_wfa,
			chat_id = chat_joe_and_daniel,
			#still_in_chat = True,
			#datetime_left_chat = None,
			#datetime_last_viewed_chat = timezone.now()
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

	#TODO: Fix logic
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
		#print("chats_with_joe_as_ids:")
		#print(chats_with_joe_as_ids)
		#print("chats_with_daniel_as_ids:")
		#print(chats_with_daniel_as_ids)

		chat_ids_containing_joe_and_daniel = chats_with_joe_as_ids + (chats_with_daniel_as_ids)
		#print("chat_ids_containing_joe_and_daniel:")
		#print(chat_ids_containing_joe_and_daniel)

		chat_with_joe_and_daniel = Chat.objects.filter(chat_id__in = chat_ids_containing_joe_and_daniel)[0]
		#print("chats with joe and daniel")
		#print(chat_with_joe_and_daniel)

		#Chat.objects.create_chat()
		joe_partner = Chat.objects.get_chat_user_partner(chat_user = joe_wfa)
		daniel_partner = Chat.objects.get_chat_user_partner(chat_user = daniel_wfa)

		self.assertEqual(joe_partner.warframe_account_id.warframe_alias, "daniel_wfa",
			msg="Expected daniel to be joe's chat partner for the chat with joe and daniel")
		self.assertEqual(daniel_partner.warframe_account_id.warframe_alias, "joe_wfa",
			msg="Expected joe to be daniel's partner for the chat with joe and daniel")
		
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
			#still_in_chat = True,
			#datetime_left_chat = None,
			#datetime_last_viewed_chat = timezone.now()
		)

		chat_user_carl.save()

		chat_user_ariel = ChatUser(
			warframe_account_id=ariel_wfa,
			chat_id = ariel_and_carl_chat,
			#still_in_chat = True,
			#datetime_left_chat = None,
			#datetime_last_viewed_chat = timezone.now()
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
	
	#TODO: Reread
	#Done
	def test_chats_wfa_has_been_in_returns_correct_chats(self):
		# create an additional chat betwen joe and vanessa with no messages between
		# the two of them 
		joe_wfa = WarframeAccount.objects.get(warframe_alias="joe_wfa")
		vanessa_wfa = WarframeAccount.objects.get(warframe_alias="vanessa_wfa")
		
		#the warframe account of daniel
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

		list1 = joe_as_chat_user.values_list('chat_id', flat=True) #chats joe is in
		list2 = daniel_as_chat_user.values_list('chat_id', flat=True) #chats daniel is in
		

		#get the chat_id of the chat that joe and daniel are in
		chat_id_joe_and_daniel_are_in = list(set(list1) & set(list2))
		self.assertEqual(1, len(chat_id_joe_and_daniel_are_in), msg="Joe and daniel should only be in one chat")

		msg = "Joe and vanessa chat is suppose to be a chat that joe has been in"
		
		self.assertEqual((joe_and_vanessa_chat in chats_joe_been_in), True, msg)
	
	"""
	#@query_debugger
	def test_chats_wfa_still_in_returns_correct_chats(self):
		'''
		Should return an array of the correct chats that the warframe account is in
		'''

		# Create a chat between two chat users: bob and dan. 

		bob_wfa = WarframeAccount.objects.create_warframe_account("bob_wfa")
		dan_wfa = WarframeAccount.objects.create_warframe_account("dan_wfa")

		bob_and_dan_chat = Chat.objects.create_chat()

		bob_chat_user = ChatUser.objects.create_chat_user(bob_wfa, bob_and_dan_chat)
		dan_chat_user = ChatUser.objects.create_chat_user(dan_wfa, bob_and_dan_chat)
		
		chat = Chat.objects.chats_wfa_still_in(bob_wfa)[0]
		self.assertEqual(chat, bob_and_dan_chat, msg="Bob is suppose to be in the chat with Dan.")
		chat = Chat.objects.chats_wfa_still_in(dan_wfa)[0]
		self.assertEqual(chat, bob_and_dan_chat, msg="Dan is suppose to be in the chat with Bob.")

		# Make bob leave the only chat he is in
		bob_chat_user.exit_chat()
		bob_chat_user.save()
		chat = Chat.objects.chats_wfa_still_in(bob_wfa)
		self.assertEqual(chat, [], msg="Bob is not suppose to be in a chat.")
		
		# Make dan leave the chat
		dan_chat_user.exit_chat()
		dan_chat_user.save()

		chat = Chat.objects.chats_wfa_still_in(dan_wfa)
		self.assertEqual(chat, [], msg="Dan is not suppose to be in a chat.")

		# Make bob re-enter the chat
		bob_chat_user.enter_chat().save()
		chat = Chat.objects.chats_wfa_still_in(bob_wfa)[0]
		self.assertEqual(chat, bob_and_dan_chat, "Bob is suppose to be in the same chat as Dan.")
	"""
	
	'''
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
		'''

	#TODO: Reread
	#Done
	def test_chats_with_new_msgs_returns_correct_chats_with_new_msgs(self):
		'''
		Should return the correct chats that a user has received new messages from
		'''
		# Create two chats. Each chat contains two users, and each of the chats will contain at least
		# one new msg for one of the two users in the chat.

		#Create the first chat 

		bob_wfa = WarframeAccount.objects.create_warframe_account("bob_wfa")
		dan_wfa = WarframeAccount.objects.create_warframe_account("dan_wfa")
		
		chat = Chat.objects.create_chat()

		bob_chat_user = ChatUser.objects.create_chat_user(bob_wfa, chat)
		dan_chat_user = ChatUser.objects.create_chat_user(dan_wfa, chat)

		dan_to_bob_msg_0 = ChatMessage.objects.create_chat_message(dan_chat_user, "howdy")
		time.sleep(0.01)
		dan_to_bob_msg_1 = ChatMessage.objects.create_chat_message(dan_chat_user, "eyy")
		time.sleep(0.01)

		# bob should now have 2 new message from dan because the messages from dan to bob
		# was created after bob's corresponding 'datetime_last_viewed_chat' value was
		# initialized.
		#
		# similarly dan should have 1 new message from bob.
		chats = Chat.objects.chats_with_new_msgs(bob_wfa)
		msg = "The chat between bob and dan should be a chat that bob_wfa has received new messages in"
		self.assertEqual((len(chats) == 1 and chats[0] == chat), 1, msg=msg)
		
		msg = "There should be no chat for which dan has received a new message because" \
			"he has not received any messages"
		self.assertEqual([], Chat.objects.chats_with_new_msgs(dan_wfa), msg=msg)

	#TODO: Reread
	#Done
	def test_chats_with_new_msgs_returns_correct_chats_with_new_msgs_2(self):
		'''
		Should return the correct chats that a user has received new messages from
		'''
		
		# Create 20 'bots'.
		# Bots 5 through 10 (0-base) send bob 1 message each
		# Bots 15 through 17 (0-base) send eve 1 message each
		
		bob_wfa = WarframeAccount.objects.create_warframe_account("bob_wfa")

		eve_wfa = WarframeAccount.objects.create_warframe_account("eve_wfa")

		wfa_alias_prefix = "warframe"

		warframe_accounts = []
		for i in range(20):
			alias = wfa_alias_prefix + str(i)
			wfa = WarframeAccount.objects.create_warframe_account(alias)
			warframe_accounts.append(wfa)

		chats_with_bob = []

		#send messages to bob
		for i in range(5,11):
			chat = Chat.objects.create_chat()
			chats_with_bob.append(chat)

			bob_chat_user = ChatUser.objects.create_chat_user(bob_wfa, chat_id=chat)
			warframe_account_chat_user = ChatUser.objects.create_chat_user(warframe_accounts[i], chat_id=chat)

			ChatMessage.objects.create_chat_message(warframe_account_chat_user, "hi")
			
		chats_with_eve = []

		#send messages to eve
		for i in range(15,18):
			chat = Chat.objects.create_chat()
			chats_with_eve.append(chat)

			eve_chat_user = ChatUser.objects.create_chat_user(eve_wfa, chat_id=chat)
			warframe_account_chat_user = ChatUser.objects.create_chat_user(warframe_accounts[i], chat_id=chat)

			ChatMessage.objects.create_chat_message(warframe_account_chat_user, "hi")
		
		chats_with_new_msgs = Chat.objects.chats_with_new_msgs(bob_wfa)
		msg="func call should return length of chats that bob has been in"
		self.assertEqual(len(chats_with_new_msgs), len(chats_with_bob), msg)
		
		chats_with_new_msgs = Chat.objects.chats_with_new_msgs(eve_wfa)
		msg="func call should return length of chats that eve has been in"
		self.assertEqual(len(chats_with_new_msgs), len(chats_with_eve), msg)

	#Done
	def test__get_non_duplicate_chats_with_none_chat(self):
		'''
		Calling _get_non_duplicate_chats with none for 'chat' as an argument should return
		an empty list
		'''
		self.assertEqual(Chat.objects._get_non_duplicate_chats(None), [])
	
	#Done
	def test__get_non_duplicate_chats_with_list_of_chats_returns_list_of_unique_chats(self):
		'''
		Calling _get_non_duplicate_chats with an array of duplicate chat instances returns
		should return a new list of chat instances with duplicates removed.
		'''
		chat1 = Chat.objects.create_chat()
		chat2 = chat1
		chat3 = chat1
		chat4 = Chat.objects.create_chat()

		#chats with duplicates
		chats = []
		chats.append(chat1)
		chats.append(chat2)
		chats.append(chat3)
		chats.append(chat4)

		#chats with no duplicates
		chats_no_duplicates = Chat.objects._get_non_duplicate_chats(chats)

		self.assertEqual(len(chats_no_duplicates), 2, msg="chats should contain 2 chats")

		contains_chat1 = False
		contains_chat4 = False

		for chat in chats_no_duplicates:
			if chat.pk == chat1.pk:
				contains_chat1 = True
			elif chat.pk == chat4.pk:
				contains_chat4 = True

		msg="chats_no_duplicates should only have 2 unique chats, chat1 and chat4"
		self.assertEqual(contains_chat1, True, msg=msg)
		self.assertEqual(contains_chat4, True, msg=msg)

	def test_get_displayable_chats_with_warframe_still_in_chats_and_having_new_msgs_in_some_chats_returns_these_chats(self):
		'''
		Calling get_displayable_chats should return the list (with duplicates remove) of
		chat instances for which he is still in a chat with or has received new msgs from.
		'''

		'''create a chat between wfa_bob and wfa_ellen and have ellen send bob a message'''
		wfa_bob = WarframeAccount.objects.create_warframe_account("bob_wfa")
		wfa_ellen = WarframeAccount.objects.create_warframe_account("ellen_wfa")

		#chat for bob and ellen
		#Chat.objects.create_chat_for_two_warframe_accounts(wfa_bob, wfa_ellen)
		bob_and_ellen_chat = Chat.objects.create_chat()
		bob_chat_user1 = ChatUser.objects.create_chat_user(wfa_bob, bob_and_ellen_chat)
		ellen_chat_user1 = ChatUser.objects.create_chat_user(wfa_ellen, bob_and_ellen_chat)

		#have ellen send bob a message, marking bob_and_ellen_chat as a chat
		#bob is still in and has received a new message for.
		ChatMessage.objects.create_chat_message(ellen_chat_user1, "Hi, Bob!")

		msg = "The chat between bob and ellen should be a displayable chat because the chat checks the requirements " \
			"for being a displayable chat."

		for chat in Chat.objects.all():
			print("chat: " + str(chat.pk))
			for chat_user in chat.chatuser_set.all():
				print("	users in chat: " + chat_user.warframe_account_id.warframe_alias)

		self.assertEqual(len(Chat.objects.get_displayable_chats(wfa_bob)), 1, msg=msg)

		msg = "Chat between bob and ellen should be a displayable chat."
		self.assertEqual(Chat.objects.get_displayable_chats(wfa_bob)[0], bob_and_ellen_chat, msg=msg)

		''' Create a chat between Bob and Greg with no new messages for Bob from Greg'''
		wfa_greg = WarframeAccount.objects.create_warframe_account("greg_wfa")
		
		bob_and_greg_chat = Chat.objects.create_chat()

		Chat.objects.create_chat_for_two_warframe_accounts(wfa_bob, wfa_greg)

		msg = "Bob should have two displayable chats, one between him and ellen, the other between him and greg"
		self.assertEqual(len(Chat.objects.get_displayable_chats(wfa_bob)),2, msg=msg)

	#Tests after rewrite of chat app.

	



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

		