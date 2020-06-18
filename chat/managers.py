from django.db import models
from django.apps import apps

class ChatManager(models.Manager):

	def is_user_in_chat(self, chat_user_id, chat_id):
		''' check if the warframe account in still in a chat
		particular chat session '''
		pass
		
	def _get_wf_accounts_interacted_with(self, warframe_account):
		'''
		Returns all warframe accounts 'warframe_account' has been in a chat with
		'''
		if warframe_account is None:
			raise ValueError("'warframe_account' argument is required")

		return self.all().filter(warframe_account_id = warframe_account.warframe_account_id)

	def test(self):
		pass

	'''DEP'''
	def get_warframe_accounts_in_active_conversation_with(self, warframe_account):
		'''
		Returns all warframe accounts 'warframe_account' is 'actively' in a chat conversation with.

		'warframe_account' is in an 'active' conversation with another warframe account,
		(let's call this account other account 'other_warframe_account' for 
		the sake of exaplanation) if:
		- The 'warframe_account' has messaged or had been messaged 
		- The 'warframe_account' had not left the chat
		- The 'warframe_account' had left the chat, but since leaving the chat has received
		  new messages from another warframe account
		'''

		if warframe_account is None:
			raise ValueError("'warframe_account' argument is required")

		#wf_accounts_interacted_with = self._get_wf_accounts_interacted_with(warframe_account=warframe_account)

		q = self.objects.filter(warframe_account_id=warframe_account.warframe_account_id)
		q = q.filter()

	#TODO: REMOVE
	def select_related_example(self):
		pass

	def get_chat_containing_warframe_accounts(self, wfa_one, wfa_two):
		'''
		Returns the chat that warframe_account instances 'wfa_one' and 'wfa_two'
		are in. Since any chat can only contain two warframe_accounts, this is the same
		as saying "get the chat containing wfa_one and wfa_two".
		'''
		raise NotImplementedError()

	def get_chat_user_partner(self, chat_user, chat):
		'''
		Returns the chat partner of 'chat_user'. Since there can only be two chat_users 
		in a chat, this just returns the other chat_user that is in the chat
		'''

		if chat_user == None:
			raise ValueError("chat_user, an instance of ChatUser model, is required.")
		if chat == None:
			raise ValueError("chat, an instance of Chat model, is required.")

		#chat_user_model = apps.get_model(app_label = 'chat', model_name = 'chatUser')
		#q = chat_user_model.objects.select_related('chat_id')
		#q = q.filter(chat_id=chat.chat_id)

		chat_model = apps.get_model(app_label='chat', model_name='chat')
		
		#Returns all the chat users. This will be two chat_user instances.
		target_chat = chat_model.objects.get(chat_id = chat.chat_id)
		print("Target_chat is: ")
		print(target_chat)
		chat_users = target_chat.chatuser_set
		
		partner = chat_users.exclude(warframe_account_id = chat_user.warframe_account_id)[0]
		
		return partner


	def get_displayable_chats_of_wf_account(self, warframe_account):
		'''
		Returns all chats that are 'displayable' to
		Warframe account 'warframe_account'. For a reference to what
		'displayable' means, please read documentation.
		'''

		
		#Get all the chats that warframe_account is in
		chat_user_model = apps.get_model(app_label='chat', model_name='ChatUser')
		

		wfa_id = warframe_account.warframe_account_id
		q1 = chat_user_model.objects.select_related('chat_id').filter(warframe_account_id=wfa_id, still_in_chat=True)


		#TODO: qX should query and make sure datetime left is not NULL
		'''
		q3 = chat_user_model.objects.selected_related('chat_id').filter(warframe_account_id=wfa_id, still_in_chat=False)

		
		q2 = chat_user_model.objects.selected_related('chat_id').filter(warframe_account_id=wfa_id, still_in_chat=False)
		q2 = q2.chat_message_set()
		'''
		
		#Get all the chats that warframe_acocunt has left, but has received
		#a message since the time they left the chat
		chat_message_model = apps.get_model(app_label='chat', model_name='ChatMessage')
		q2 = chat_message_model.select_related('chat_user_id').filter()

		#start
		chat_user_model.objects.all().filter(warframe_account_id = wfa_id, still_in_chat=False)
		#end
		
		return


class ChatUserManager(models.Manager):

	

	pass

class ChatMessageManager(models.Manager):
	pass

