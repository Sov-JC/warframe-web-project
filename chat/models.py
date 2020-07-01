from django.db import models
from django.conf import settings

from user.models import User
from user.models import WarframeAccount

from django.db import DataError
from .managers import *

from django.db.models import Q

# Create your models here.
class Chat(models.Model):
	chat_id = models.AutoField(primary_key=True)
	datetime_created = models.DateTimeField(auto_now_add=True, blank=True)

	'''
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
	'''

	objects = ChatManager()
	
	class Meta:
		'''
		constraints = [
			models.UniqueConstraint(
				fields = [
					'person_one_warframe_account_id',
					'person_two_warframe_account_id',
				],
				name = 'different_warframe_accounts_in_private_chat'
			)
		]
		'''
		

class ChatUser(models.Model):
	chat_user_id = models.AutoField(primary_key=True)
	warframe_account_id = models.ForeignKey(
		WarframeAccount,
		on_delete=models.PROTECT,
		default=None,
		db_column='warframe_account_id'
	)
	chat_id = models.ForeignKey(
		Chat,
		on_delete = models.CASCADE,
		default=None,
		db_column='chat_id'
	)
	#still_in_chat = models.BooleanField(default=True)
	#datetime_left_chat = models.DateTimeField(null=True, default=None)
	#datetime_last_viewed_chat = models.DateTimeField(null=True, default=None)

	objects = ChatUserManager()

	"""
	#Untested
	def exit_chat(self):
		'''
		"Remove" the user from the chat. This sets the still_in_chat
		field to False. This does not delete this chat_user instance.
		In addition, sets datetime_last_viewed_chat and datetime_left_chat to timezone.now()

		Returns self
		'''
		self.still_in_chat = False
		self.datetime_left_chat = timezone.now()
		self.datetime_last_viewed_chat = timezone.now()

		return self
	"""

	def _find_wfa_partner(self, warframe_account, chat):
		#
		
		chat_user_m = apps.get_model(app_label='chat', model_name='chatuser')
		query_set1 = chat_user_m.select_related('chat').filter(chat_id = chat)

		chat_users_in_chat = chat_user_m.objects.filter(chat_id=chat)

		#since there can only be two chat users in a chat, we return the chat user
		if len(chat_users_in_chat) > 2:
			raise IntegrityError("Detected a chat with more than two chat users in chat %{data}s", {"chat":chat.pk})

		for chat_user in chat:
			pass

		raise NotImplemented

	#Tested
	def _find_duplicates_from_nums(self, numbers):
		'''From a an array of integers, return a list of numbers that are duplicates
		in the list. If numbers is None or empty, returns an empty list.
		'''
		if numbers == None:
			return []

		#create a copy and sort it
		numbers = list(numbers) 
		numbers.sort()

		duplicates = set()

		if len(numbers) <= 1:
			return []

		for i in range(1, len(numbers)):
			if numbers[i] == numbers[i-1]:
				duplicates.add(i)
		
		return list(duplicates)
	
	#Tested
	def _chat_between_wfa_already_exists(self, warframe_account_one, warframe_account_two):
		'''Check if there already exists a chat between two warframe accounts. If they do
		exist in the chat, return True. False otherwise.
		'''

		chat_user_m = apps.get_model(app_label='chat', model_name='chatuser')

		#get the chat ids that 'warframe_account_one' and 'warframe_account_two' are in
		wfa_one_chats_in_ids = chat_user_m.objects.filter(warframe_account_id = warframe_account_one).values_list('chat_id', flat=True)
		wfa_two_chats_in_ids = chat_user_m.objects.filter(warframe_account_id = warframe_account_two).values_list('chat_id', flat=True)

		wfa_one_chats_in_ids = list(wfa_one_chats_in_ids)
		wfa_two_chats_in_ids = list(wfa_two_chats_in_ids)

		#chat ids that wfa_one and wfa two have been in
		duplicate_chat_ids = self._find_duplicates_from_nums(wfa_one_chats_in_ids + wfa_two_chats_in_ids)

		#since two warframe accounts can ever be in one chat, and the same pair
		#of warframe accounts cannot exist in more than 1 chat, duplicate_chat_ids should
		#return only one chat if the two warframe accounts are in a chat.

		if len(duplicate_chat_ids) == 0:
			return False
		elif len(duplicate_chat_ids) == 1:
			return True
		else:
			raise DataError("Detected multiple chats that contain the same pair of warframe accounts (\
				warframe_account_one and warframe_account_two). Please check the integrity of your database with regards to 'duplicate chats'!")


	def _get_chat_users_in_chat(self, chat):
		'''Obtain all chat_user instances in an array that reference 'chat'

		:param chat: A chat instance to determine chat_user references
		:type chat: Chat
		...
		...
		:return: A an array of chat users referncing 'chat'
		:rtype: A list of ChatUser instances
		'''
		raise NotImplementedError

	def _update_results_in_duplicate_chat(self, chat_user, warframe_account_one, warframe_account_two):
		'''Check if as a result of updating chat_user, it will result in a duplicate chat. A duplicate chat
		is a chat between two Warframe accounts that occurs more than once in the database state. For example, 
		a chat with pk = 830 with Joe and Lisa, and another chat with pk = 900 containing Joe and Lisa as well.
		
		:param chat_user: The chat user that is to be updated.
		:type chat_user: A ChatUser instance
		...
		:return: Returns True if updating the chat_user would result in a database state containing a duplicate chat between two users. 
		False otherwise.
		:rtype: Boolean
		'''
		return

	
	#untested
	def saveOLD(self, *args, **kwargs):
		#Check that chat_id is not referenced
		#by more than 2 chat_user instances. That is, 
		#check the chat has no more than 2 users in it.
		#chat_user_m = apps.get_model(app_label="chat", model_name="chatuser")
		#q = chat_user_m.objects.filter(chat_id=self.chat_id).values_list('chat_id')
		
		#try 2

		#determine if this save is an update, or the creation of a row
		is_new = self._state.adding

		if is_new:
			# This is a CREATE operation

			# Check that the chat referenced does not contain more than 1 other user in the chat in the database.
			chat_users_in_chat = self.chat_id.chatuser_set.all()

			# Check that the chat you want to insert the chat user in is not already full
			if len(chat_users_in_chat) >= 1:
				raise DataError("Cannot assign this ChatUser instance to a Chat with pk %(pk)s because this \
					chat already contains at least 2 users (the chat is full)" % {'pk':chat.pk})
			
			# Check that as a result of inserting the chat user instances you won't have
			# two chats in the database after calling save() that each have the 'same' chat users.
			# 
			# For example:
			#	A chat with pk 16 with Joe and Jessica in the chat
			#	and another chat with pk 32 with Joe and Jessica again.
			# 
			# This check is necessary as to not violate the business logic that there should
			# not be more than one chat between two different warframe accounts to capture the
			# idea of a sort of "unique chat area" that two warframe accounts use to chat between each other.

			if len(chat_users_in_chat) == 1:
				chat_user_in_chat = chat_users_in_chat[0]
				chat_user_wfa = chat_user_in_chat.warframe_account_id

				if(chat_user_in_chat.warframe_account_id.pk is not self.warframe_account.pk):
					if(_chat_between_wfa_already_exists(chat_user_wfa, _self.warframe_account_id)):
						raise DataError("Attempted to add a chat user to a chat that would result \
							in duplicates chats for chat interaction between two particular WarframeAcccount instances.")
				else:
					# chat_user_in_chat's warframe_account_id is the same as self.warframe_account_id
					# meaning that after the save() there will be two warframe accounts in the same chat room.
					# But since this case is handled by the 'no_duplicate_warframe_accounts_in_chat' constraint
					# will just let the database constraint handle it.
					pass 
		else:
			# This is an UPDATE operation. Chat users cannot be updated.
			return

			#Don't allow chat_id and 'warframe_account_id' to be changed.
			pass

		super(ChatUser, self).save(*args, **kwargs)
	
	#Untested
	def save(self, *args, **kwargs):
		is_new = self._state.adding

		if is_new:
			# This is a CREATE operation

			# Check that the chat referenced does not contain more than 1 other user in the chat in the database.
			chat_users_in_chat = self.chat_id.chatuser_set.all()

			# Check that the chat you want to insert the chat user in is not already full
			if len(chat_users_in_chat) >= 2:
				raise DataError("Cannot assign this ChatUser instance to a Chat with pk %(pk)s because this \
					chat already contains at least 2 users (the chat is full)" % {'pk':self.chat_id.pk})
			
			# Check that as a result of inserting the chat user instances you won't have
			# two chats in the database after calling save() that each have the 'same' chat users.
			# 
			# For example:
			#	A chat with pk 16 with Joe and Jessica in the chat
			#	and another chat with pk 32 with Joe and Jessica again.
			# 
			# This check is necessary as to not violate the business logic that there should
			# not be more than one chat between two different warframe accounts to capture the
			# idea of a sort of "unique chat area" that two warframe accounts use to chat between each other.

			if len(chat_users_in_chat) == 1:
				chat_user_in_chat = chat_users_in_chat[0]
				chat_user_wfa = chat_user_in_chat.warframe_account_id

				#print("chat_user_in_chat.warframe_account_id.pk: ")
				#print(chat_user_in_chat.warframe_account_id.pk)
				#print("self.warframe_account_id.pk:")
				#print(self.warframe_account_id.pk)
				#print("chat_user_in_chat.warframe_account_id.pk != (self.warframe_account_id.pk):")
				#print(chat_user_in_chat.warframe_account_id.pk != self.warframe_account_id.pk)

				if(chat_user_in_chat.warframe_account_id.pk != (self.warframe_account_id.pk)):
					if(self._chat_between_wfa_already_exists(chat_user_wfa, self.warframe_account_id)):
						raise DataError("Attempted to add a chat user to a chat that would result " + \
							"in duplicate chats between two particular WarframeAcccount instances.")
				else:
					# chat_user_in_chat's warframe_account_id is the same as self.warframe_account_id
					# meaning that after the save() there will be two warframe accounts in the same chat room.
					# But since this case is handled by the 'no_duplicate_warframe_accounts_in_chat' constraint
					# will just let the database constraint handle it.
					pass 
		else:
			# This is an update. Don't do anything on an update since a chat user cannot be updated
			return

		super(ChatUser, self).save(*args, **kwargs)

	class Meta:
		db_table = "chat_chat_user"
		constraints = [
			models.UniqueConstraint(
				fields=['warframe_account_id','chat_id'],
				name='no_duplicate_warframe_accounts_in_chat'
			)
		]


class ChatMessage(models.Model):
	chat_message_id = models.AutoField(primary_key=True)
	chat_user_id = models.ForeignKey(
		ChatUser,
		on_delete = models.CASCADE,
		default=None,
		db_column="chat_user_id"
	)

	message = models.CharField(max_length=512, blank=True, default=None)
	datetime_created = models.DateTimeField(auto_now_add=True, blank=True)
	has_been_read = models.BooleanField(default=False)


	objects = ChatMessageManager()
	
	class Meta:
		db_table = 'chat_chat_message'
