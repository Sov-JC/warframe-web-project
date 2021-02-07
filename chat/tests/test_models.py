from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.models import *
from django.contrib import auth
from django.utils import timezone
from django.db.models import Q

from django.db import IntegrityError

from projectutils.utils import query_debugger

# Create your tests here.
class TestChatUserModel(TestCase):
	fixtures=["user_app-user-status.json", "user_app-gaming-platforms.json"]

	#REREAD
	def test_chat_user_save_method_raises_error_if_saving_a_chat_with_more_than_2_users(self):
		chat = Chat.objects.create_chat()

		bob_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="bob_wfa")
		dan_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="dan_wfa")

		intruder_wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="intruder_wfa")

		bob_chat_user = ChatUser.objects.create_chat_user(warframe_account_id=bob_wfa,chat_id=chat)
		dan_chat_user = ChatUser.objects.create_chat_user(warframe_account_id=dan_wfa,chat_id=chat)
		

		
		try:
			intruder_chat_user = ChatUser.objects.create_chat_user(warframe_account_id=intruder_wfa,chat_id=chat)
			msg = "intruder_chat_user should not be allowed to enter a chat that contains 2 (or more) people"
			self.fail(msg)
		except DataError:

			pass

	#Done
	def test__find_duplicates_from_nums_returns_original_list_with_numbers_arg_len_equal_to_one(self):
		'''
		Should return the original list of the length of the numbers argument is 1.
		'''
		response = ChatUser()._find_duplicates_from_nums(numbers = [23])
		self.assertEqual(len(response), 0)

	#Done
	def test__find_duplicates_from_nums_returns_empty_list_with_numbers_arg_len_less_than_one(self):
		'''
		Should return an empty list if numbers argument was None or the list was empty.
		'''
		response = ChatUser()._find_duplicates_from_nums([])
		responseTwo = ChatUser()._find_duplicates_from_nums(None)

		self.assertEqual(len(response), 0)
		self.assertEqual(responseTwo, [])

	#Done
	def test__find_duplicates_from_nums_returns_correct_value_with_arg_length_of_two(self):
		'''
		Should return the correct duplicate values when passed number arguments of length 2
		'''

		duplicates = ChatUser()._find_duplicates_from_nums([7,7])
		self.assertEqual(len(duplicates),1)
		
		duplicates = ChatUser()._find_duplicates_from_nums([1,3])
		self.assertEqual(len(duplicates), 0)
	
	#Done
	def test__chat_between_wfa_already_exist_function_with_two_warframe_accounts_in_a_chat(self):
		'''
		Should return the correct chat pk of the chat that two warframe accounts are in.
		'''
		chat = Chat.objects.create_chat()

		wf1 = WarframeAccount.objects.create_warframe_account("wfa1")
		wf2 = WarframeAccount.objects.create_warframe_account("wfa2")

		wfa1_chat_user = ChatUser.objects.create_chat_user(wf1, chat)
		wfa2_chat_user = ChatUser.objects.create_chat_user(wf2, chat)

		self.assertEqual(ChatUser()._chat_between_wfa_already_exists(wf1, wf2), True)
	
	#Done
	def test__chat_between_wfa_already_exists_with_two_warframe_accounts_not_in_chat_together(self):
		'''
		The call to the function with two warframe accounts as arguments that are now in a 
		chat together should return false
		'''
		
		#Create two waframe accounts that are not in a chat together
		wfa1_wfa = WarframeAccount.objects.create_warframe_account("wfa1")
		wfa2_wfa = WarframeAccount.objects.create_warframe_account("wfa2")

		self.assertEqual(ChatUser()._chat_between_wfa_already_exists(wfa1_wfa, wfa2_wfa), False)

	def test_chat_user_model_save_does_nothing_on_update(self):
		pass
	
	def test_chat_user_model_save_with_chat_reference_of_chat_that_is_full_raises_exception(self):
		'''
		An attempt to save a model (using CREATE as opposed to UPDATE) that references 
		a chat that already contains at least 2 users should raise an error.
		'''
		
		# Create a chat that is full (contains two chat users)
		wfa1 = WarframeAccount.objects.create_warframe_account("wfa1")
		wfa2 = WarframeAccount.objects.create_warframe_account("wfa2")
		full_chat = Chat.objects.create_chat_for_two_warframe_accounts(wfa1, wfa2)

		# Create a ChatUser instance that references this full_chat
		# and attempt to save it.
		wfa3 = WarframeAccount.objects.create_warframe_account("wfa3")
		wfa3_chat_user = ChatUser(
			warframe_account_id = wfa3,
			chat_id = full_chat
		)

		try:
			wfa3_chat_user.save()
			msg = "Saving a chat user instance that refrences a chat that is already full " + \
				"should return a DataError exception"
			self.fail(msg)
		except DataError:
			pass
	
	#Done, Not Reviewed
	def test_save_with_constraint_no_duplicate_warframe_account_in_chat_broken_raises_integrity_error(self):
		'''
		Attempting to save a ChatUser instance containing a WarframeAccount and Chat reference
		that atleady exists in the database should raise an Integrity error because 
		a chat cannot contain the same Warframe account more than once.
		'''

		# create a chat with a chat user. Attempt to
		# create another ChatUser instance referncing the same
		# chat and warframe account.
		chat = Chat.objects.create_chat()
		wfa1 = WarframeAccount.objects.create_warframe_account("WarframeAccount1")
		wfa1_chat_user = ChatUser.objects.create_chat_user(wfa1, chat)
		
		chat_user = ChatUser(warframe_account_id = wfa1, chat_id=chat)
		
		try:
			chat_user.save()
			msg = "chat_user.save() should have raised a DataError exception because " + \
				"an attempt was made to create a chat with two of the same users in the chat."
			self.fail(msg)
		except DataError:
			pass
	
	# Done, Not Reviewd
	def test_update_raises_programming_error(self):
		'''
		A save operation on a ChatUser should do nothing since ChatUser instances
		cannot be modified once created
		'''
		wfa1 = WarframeAccount.objects.create_warframe_account(warframe_alias="warframeaccount1")
		chat = Chat.objects.create_chat()
		wfa1_chat_user = ChatUser.objects.create_chat_user(wfa1, chat)

		#create a new wfa2, and make wfa1_chat_user's 
		# reference this WarframeAccount instance.
		wfa2 = WarframeAccount.objects.create_warframe_account("warframeaccount2")
		
		try:
			# perform the update, nothing should have changed in the database though
			msg = "ChatUser instances should not be allowed to update."
			wfa1_chat_user.warframe_account_id=wfa2
			wfa1_chat_user.save()
			self.fail(msg=msg)
		except ProgrammingError:
			pass
	
	# Not done.
	def test_chat_user_model_saves_successfully_with_appropriate_chat_and_warframe_account_combination(self):
		"""
		Should save the ChatUser instance with valid parameters and an appropriate database state.
		"""

		pass
	
	



