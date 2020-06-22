from django.db import models
from django.apps import apps
from django.utils import timezone
from django.db.models import Prefetch

from projectutils.utils import query_debugger

class ChatManager(models.Manager):

	def create_chat(self, **extra_fields):
		extra_fields.setdefault('datetime_created', timezone.now())

		chat = self.model(**extra_fields)
		chat.save()

		return chat

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

	def get_chat_containing_warframe_accounts(self, wfa_one, wfa_two):
		'''
		Get the chat that warframe_account instances 'wfa_one' and 'wfa_two'
		are in. Assumes there are at most 2 warframe accounts in any one chat.

		Returns the Chat model instance that the two warframe accounts are in. 
		
		Returns None if there is no Chat model instance that the two accounts are in.
		Returns None if the two warframe accounts are the same.
		'''
		if wfa_one.pk == wfa_two.pk:
			return None


		chat_user_m = apps.get_model(app_label='chat', model_name='ChatUser')
		
		# Get 'chat_id's of the chats wfa_one is in
		chat_ids_wfa_one_is_in = chat_user_m.objects.filter(warframe_account_id=wfa_one).values_list('chat_id', flat=True)

		# Do the same for 'wfa_two'
		chat_ids_wfa_two_is_in = chat_user_m.objects.filter(warframe_account_id=wfa_two).values_list('chat_id', flat=True)

		if len(chat_ids_wfa_one_is_in) == 0 or len(chat_ids_wfa_two_is_in) == 0:
			return None

		# The chat that the two warframe accounts are in is the chat_id that they both reference. Let's get that
		# particular chat. The logic below can be thought of as
		# 'get the chat wfa_one is in AND wfa_two is in'.
		chats_qs = self.all().filter(
				chat_id__in = chat_ids_wfa_one_is_in
			).filter(
				chat_id__in=chat_ids_wfa_two_is_in
			)
		
		chat = None

		# Get the chat if it was found
		if chats_qs:
			chat = chats_qs[0]
		
		return chat

	def get_chat_user_partner(self, chat_user):
		raise NotImplementedError()
	
	def get_chat_user_partner_REFACTOR_THIS(self, chat_user, chat):
		'''
		Returns an instance of chat_user representing the chat partner
		of 'chat_user'
		'''
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
	
	@query_debugger
	def chats_wfa_has_been_in(self, warframe_account):
		'''
		Returns an array of Chat pks that 'warframe_account' has been in.
		'''		
		chat_user_m = apps.get_model(app_label="chat",model_name="ChatUser")
		#chat_m = apps.get_model(app_label="chat", model_name="Chat")

		# chat_user instances of 'warframe_account'
		wfa_chat_user_instances = chat_user_m.objects.select_related('chat_id').filter(warframe_account_id=warframe_account)

		chats = [] # chats been in
		for chat_user in wfa_chat_user_instances:
			chats.append(chat_user.chat_id.pk)
			
		return chats

	def has_received_new_chat_message(self, warframe_account, chat):
		'''
		returns true if user has receive a new message from chat partner,
		False otherwise
		'''
		pass
	
	def new_chat_messages_received_from_chat(self, chat_user):
		'''
		Returns a QuerySet of chat_messages that are new to 'chat_user'. 
		A new message is a message sent to 'chat_user' after 'chat_user'
		last viewed the chat OR a message sent to 'chat_user' after having left
		the chat
		'''
		chat_user_m = apps.get_model(app_label="chat", model_name="chat_user")

		# get the last time the chat user viewed the chat
		dt_last_viewed_chat = chat_user.datetime_last_viewed_chat

		# Get the other chat_user that is in the chat
		partner = self.get_chat_user_partner(chat_user)

		# Get all the messages sent by chat partner after last viewing the chat
		# or after having left the chat
		chat_messages_by_partner = chat_user_m.select_related('chat_user_id').filter(chat_user_id=partner.chat_user_id)
		new_chat_messages = chat_messages_by_partner.filter(datetime_created__gte=dt_last_viewed_chat)

		return new_chat_messages

	#DEP
	def chats_wfa_received_new_messages_from(self, warframe_account):
		'''
		returns a QuerySet of chats that the user has received new messages from

		returns chats warframe_account has received new messages 
		from
		'''
		
		wfa_id = warframe_account.warframe_account_id
		#chats_wfa_has_been_in(warframe_account)
		
		chats_wfa_been_in = self.chats_wfa_has_been_in(warframe_account)

		chat_user_m = apps.get_model('chat', 'chat_user')

		#the ids of all chats that warframe_account has received new messages from
		chat_ids = set()
		
		for chat in chats_wfa_been_in:
			#get the chat_user instance of warframe_account for this particular chat
			chat_id = chat.chat_id
			chat_user = chat_user_m.objects.get(warframe_account_id=wfa_id, chat_id=chat_id)

			#get new messages received
			new_messages = self.new_chat_messages_received_from_chat(chat_user)

			if new_messages:
				chat_ids.add(chat_id)
		
		
		chats = self.all().filter(chat_id__in=list(chat_ids))

		return chats
	
	def chats_wfa_has_left(self, warframe_account):
		'''
		returns a query set of chat objects that the 'warframe_account'
		has left.
		'''
		#chats_wfa_has_been_in(wfa)
		wfa = warframe_account

		#get models
		chat_user_m = apps.get_model('chat', 'ChatUser')
		chat_m = apps.get_model('chat', 'Chat')
		
		# join chat and chat user to efficiently
		# select chats that the user has left
		q = chat_user_m.select_related('chat_id')
		q = q.filter(still_in_chat=False, warframe_account_id=wfa.warframe_account_id)

		#chat_ids of every chat that the user has been in but has left
		ids_of_chats_left = q.values_list('chat_id').distinct()

		chats_left = chat_m.object.filter(chat_id__in=ids_of_chats_left)
		
		return chats_left

	def chats_left_but_received_new_messages(self, warframe_account):
		#chats_wfa_has_been_in = chats_user_has_been_in(warframe_account)
		#chats_left = chats_wfa_has_left(warframe_account)
		#pass

		raise NotImplementedError()

	
	def chats_with_new_msgs(self, warframe_account):
		'''
		Get an array of Chat instances that WarframeAccount instance
		'warframe_account' has received new messages from.
		'''

		wfa = warframe_account
		chat_user_m = apps.get_model('chat', 'chatuser')
		chat_m = apps.get_model('chat', 'chat')

		# get all chats.
		all_chats = chat_m.fetch_related('chatuser').all()
		
		query_set = chat_user_m.objects \
			.select_related('chat', 'warframe_account_id') \
			.prefetch_related('chat_message') \
			.all()

		#primary keys of the chats 'warframe accounts' has been in
		chats_wfa_has_been_in_pks = self.chats_wfa_has_been_in(warframe_account).values_list('warframe_account_id', flat=True)

		chats_with_new_msgs = []

		for chat_user in query_set:
			#check if the chat_user has been in a chat with 'warframe_account'
			if (chat_user.chat.pk not in chats_wfa_has_been_in_pks):
				continue

			# the chat_user instance is a chat_user that has been in a chat
			# that 'warframe_account' has been in. This means that this
			# chat_user instance's warframe_account id refers to only
			# two possible waframe_account instances (either the 'warframe_account
			# its self, or the partner due to the business logic of a chat - a chat can only
			# contain 2 chat users)

			if(chat_user.warframe_account.pk == wfa.pk):
				# this chat_user corresponds to this 'warframe_account'
				# we can skip this chat_user since we are searching for the
				# partner's chat_user instance to determine the messages
				# this partner has sent to 'warframe_account'
				continue	

			# At this point, chat_user must be the 'partner' of 'warframe_account'.
			# Let's search the messages this partner has sent to 'warframe_account

			# get the chat_user instance that represents the 'warframe_account' 
			# in this particular chat
			

			# chat chat_user is in. 
			chat = chat_user.chat_id 

			# get the 'chat_user' instance of 'warframe_account' that is in
			# this chat
			warframe_account_chat_user = all_chats.get(chat_id=chat.pk) 
			
			#find chat_user instance of 'warframe_account', this 'chat_user' instance's chat partner.
			#for inner_chat_user in chat_user:
			#	if chat_user.chat_id == chat_user
			
			new_msgs_in_this_chat = False

			for chat_message in chat_user.chatmessage_set.all():
				#if chat_message.datetime_created > warframe_account_chat_user
				pass

		raise NotImplementedError

	#ToDo: Finish making tests
	def chats_wfa_still_in(self, warframe_account):
		'''
		Returns an array of Chat instances that
		'warframe_account' is in and has the 
		'still_in_chat'	flag set to True
		'''
		wfa = warframe_account

		query_set = self.prefetch_related('chatuser_set__warframe_account_id')
		
		chats = []

		for chat in query_set:
			chat_users = chat.chatuser_set.all()

			if len(chat_users) == 0:
				continue
			
			if(chat_users[0].warframe_account_id == wfa):
				chats.append(chat)
			elif(chat_users[1].warframe_account_id == wfa):
				chats.append(chat)
			
		
		return chats

	def get_displayable_chats(self, warframe_account):
		chats_still_in = self.chats_wfa_still_in(warframe_account)
		chats_with_new_msgs = self.chats_with_new_msgs_for_wfa(warframe_account)
		#chats_left_but_received_new_messages = SomeObject.objects.chats_left_but_received_new_messages(warframe_account)

		#return chats_still_in 
		pass

	#INCOMPLETE
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

	def create_chat_user(self, warframe_account_id=None, chat_id=None, **extra_fields):
		if warframe_account_id is None:
			raise ValueError("warframe_account_id is required")
		if chat_id is None:
			raise ValueError("chat_id is required")

		extra_fields.setdefault('still_in_chat', True)
		extra_fields.setdefault('datetime_left_chat', None)
		extra_fields.setdefault('datetime_last_viewed_chat', timezone.now())

		chat_user = self.model(warframe_account_id=warframe_account_id, chat_id=chat_id, **extra_fields)

		chat_user.save()

		return chat_user

class ChatMessageManager(models.Manager):

	def create_chat_message(self, chat_user_id = None, message="", **extra_fields):
		
		if chat_user_id is None:
			print("chat_user_id cannot be None")
		
		extra_fields.setdefault("datetime_created", timezone.now())

		message = self.model(chat_user_id=chat_user_id, message=message, **extra_fields)

		message.save()

		return message
		

	

