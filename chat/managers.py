from django.db import models
from django.apps import apps
from django.utils import timezone
from django.db.models import Prefetch
from django.db import transaction

from projectutils.utils import query_debugger

from django.db.models import Count, Q

class ChatManager(models.Manager):

	def create_chat(self, **extra_fields):
		extra_fields.setdefault('datetime_created', timezone.now())

		chat = self.model(**extra_fields)
		chat.save()

		return chat

	#TODO: Rewrite to return the two chat user references created.
	def _create_chat_for_two_warframe_accounts(self, warframe_account_one, warframe_account_two):
		'''
		Create and return a chat for 'warframe_account_one' and 'warframe_account_two'
		
		@param: atomic If the chat should be created using a transaction (default True)
		'''
		if warframe_account_one is None or warframe_account_two is None:
			raise ValueError("warframe_account one and warframe_account_two cannot be None")

		chatuser_m = apps.get_model(app_label='chat', model_name='chatuser')
		chat_m = apps.get_model(app_label='chat', model_name='chat')
		
		chat = chat_m.objects.create_chat()
		chatuser_m.objects.create_chat_user(warframe_account_one, chat)
		chatuser_m.objects.create_chat_user(warframe_account_two, chat)

		return chat
	
	#TODO: Fix docstring
	def create_chat_for_two_warframe_accounts(self, warframe_account_one, warframe_account_two, atomic=True):
		'''
		Create a chat for 'warframe_account_one' and 'warframe_account_two'

		@param: atomic If the chat should be created using a transaction (default True)

		returns the chat instance created for the two warframe accounts
		'''
		if atomic:
			with transaction.atomic():
				return self._create_chat_for_two_warframe_accounts(warframe_account_one,warframe_account_two)
		else:
			return self._create_chat_for_two_warframe_accounts(warframe_account_one,warframe_account_two)
	
	def is_user_in_chat(self, chat_user_id, chat_id):
		''' check if the warframe account in still in a chat
		particular chat session '''
		raise NotImplementedError()

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

	#Untested
	def get_chat_user_partner(self, chat_user):
		'''
		Returns the ChatUser instance that's 'chat_user's partner in the chat
		'chat_user' is in. Returns None if there is no other chat user in 'chat_user's
		chat.
		'''
		chat_user_m = apps.get_model(app_label="chat", model_name="chatuser")
		#print('typeof(chat_user)')
		#print(type(chat_user))
		chat_users = chat_user_m.objects.filter(chat_id=chat_user.chat_id.pk).prefetch_related('warframe_account_id')

		if len(chat_users) < 2:
			return None

		if len(chat_users) == 2:
			if chat_users[0].warframe_account_id == chat_user.warframe_account_id:
				return chat_users[1]
			else:
				return chat_users[0]
	
	#No longer needed?
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
	
	#TODO: review tests
	#Untested
	def chats_wfa_is_in(self, warframe_account):
		'''Returns an array of Chat instances that 'warframe_account' is in.

		:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
		:type [ParamName]: [ParamType](, optional)
		...
		:raises [ErrorType]: [ErrorDescription]
		...
		:return: [ReturnDescription]
		:rtype: [ReturnType]
		'''
		chat_user_m = apps.get_model(app_label="chat",model_name="ChatUser")

		# chat_user instances of 'warframe_account'
		wfa_chat_user_instances = chat_user_m.objects.select_related('chat_id').filter(warframe_account_id=warframe_account)

		chats = [] # chats been in
		for chat_user in wfa_chat_user_instances:
			chats.append(chat_user.chat_id)
			
		return chats

	def has_received_new_chat_message(self, warframe_account, chat):
		'''
		returns true if user has receive a new message from chat partner,
		False otherwise
		'''
		raise NotImplementedError()
	
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
	
	"""
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
	"""
	
	def get_chats_in_and_count_new_msgs(self, warframe_account):
		'''Returns that Chat instances that 'warframe_account' is in, along with
		the ammount of new messages received for a particular chat.

		:param warframe_account: The WarframeAccount instance to determine the chats it is
		in.
		...
		:return: A list of pairs. In each pair, the first element represents the chat
		'warframe_account' is in, and the number of new messages present in that chat for
		'waframe_account'.
		:rtype: List
		'''
		chat_user_m = apps.get_model(app_label="chat", model_name="chatuser")

		# obtain chat pks that 'warframe_account' is in
		wfa_chats_as_values = self.chats_wfa_is_in(warframe_account)

		#get the chat_user instances that are a partner of "warframe_account"
		wfa_partner_chat_user_instances = chat_user_m.objects.filter(chat_id__in=wfa_chats_as_values).exclude(warframe_account_id=warframe_account)
		#print("wfa_partner_chat_user_instances.query:")
		#print(wfa_partner_chat_user_instances.query)
		#print("wfa_partner_chat_user_instances:")
		#print(wfa_partner_chat_user_instances)

		# Annotate the ChatUser instances to obtain all the new messages
		# received by 'warframe_account' for each chat present in.
		msgs_not_read = Count('chatmessage', filter=Q(chatmessage__has_been_read=False))
		#print("wfa_partner_chat_user_instances.annotate(new_msgs = msgs_not_read).query:")
		#print(wfa_partner_chat_user_instances.annotate(new_msgs = msgs_not_read).query)
		#print("wfa_partner_chat_user_instances.annotate(new_msgs = msgs_not_read):")
		#print(wfa_partner_chat_user_instances.annotate(new_msgs = msgs_not_read))
		wfa_partner_chat_user_instances = wfa_partner_chat_user_instances.annotate(new_msgs = msgs_not_read)

		# generate the list of pairs
		chats_with_new_messages_count = []
		for chat_user in wfa_partner_chat_user_instances:
			chats_with_new_messages_count.append((chat_user.chat_id, chat_user.new_msgs))

		return chats_with_new_messages_count

	

	#No longer needed?
	def chats_with_new_msgs(self, warframe_account):
		'''
		Get an array of Chat instances that WarframeAccount instance
		'warframe_account' has received new messages from.
		'''

		wfa = warframe_account
		chat_user_m = apps.get_model('chat', 'chatuser')
		chat_m = apps.get_model('chat', 'chat')

		# get all chats.
		all_chats = chat_m.objects.prefetch_related('chatuser_set').all()
		
		# get all chat_users
		chat_users = chat_user_m.objects \
			.select_related('chat_id', 'warframe_account_id') \
			.prefetch_related('chatmessage_set') \
			.all()

		#len(chat_user_m.objects.prefetch_related('chatmessage_set'))
		#len(chat_users)

		#Get chats 'warframe accounts' has been in
		chats_wfa_has_been_in = self.chats_wfa_has_been_in(warframe_account)
		chats_wfa_has_been_in_pks = [chat.pk for chat in chats_wfa_has_been_in]

		chats_with_new_msgs = []

		for chat_user in chat_users:
			#check if the chat_user has been in a chat with 'warframe_account'
			if (chat_user.chat_id.pk not in chats_wfa_has_been_in_pks):
				continue

			# the chat_user instance is a chat_user that has been in a chat
			# that 'warframe_account' has been in. This means that this
			# chat_user instance's warframe_account id refers to only
			# two possible waframe_account instances (either the 'warframe_account
			# itsself, or the partner due to the business logic of a chat -- a chat can only
			# contain 2 chat users)

			if(chat_user.warframe_account_id.pk == wfa.pk):
				# this chat_user corresponds to this 'warframe_account'
				# we can skip this chat_user since we are searching for the
				# partner's chat_user instance to determine the messages
				# this partner has sent to 'warframe_account'
				continue	

			# At this point, chat_user must be the 'partner' of 'warframe_account'.
			# Let's search the messages this 'partner' has sent to 'warframe_account
			wfa_partner_chat_user = chat_user

			# chat 'warframe_account' partner is in.
			# let's just call it 'chat' because both
			# the wfa and the partner are in this chat.
			chat = wfa_partner_chat_user.chat_id 

			# get the 'chat_user' instance of 'warframe_account' that is in
			# this chat
			q = all_chats.get(chat_id=chat.pk).chatuser_set.all()

			wfa_chat_user = q[0] if q[0].warframe_account_id==wfa else q[1]

			#we now have the chat user instace of 'warframe_account' (wfa_chat_user), and the 
			#chat_user instance of 'warframe_account's partner (wfa_partner_chat_user) for
			#chat 'chat'
			wfa_chat_user = wfa_chat_user
			wfa_partner_chat_user = wfa_partner_chat_user

			#traverse all the messages sent from the chat partner 
			#and determine if there are any new messages from
			#the chat partner to 'warframe_account'
			new_message_count = 0
			for chat_message in wfa_partner_chat_user.chatmessage_set.all():
				# if chat_message.datetime_created > wfa_chat_user.datetime_last_viewed_chat:
				# 	new_message_count += 1

				if chat_message.has_been_read == 0:
					new_message_count +=1

			if new_message_count > 0:
				chats_with_new_msgs.append(chat)
	
		return chats_with_new_msgs

	#No longer needed?
	def _get_non_duplicate_chats(self, chats):
		''' Accesses an array of Chat instances
		and removes all duplicates (based off primary key) 
		from the array, returning an array of unique 'chats' '''
		if chats is None:
			return []
			
		
		#holds all non-duplicate chat and chat ids of 'chats'
		chats_no_duplicate_ids = set()
		chats_no_duplicates = []
		
		for chat in chats:
			len_before_insertion = len(chats_no_duplicate_ids)
			chats_no_duplicate_ids.add(chat.pk)
			len_after_insertion = len(chats_no_duplicate_ids)

			if len_before_insertion != len_after_insertion:
				#This chat is unique because it was successfully inserted into the set.
				#Becuase this chat is unique, it means it does not exist in 'chats_no_duplicates'
				chats_no_duplicates.append(chat)
			else:
				#the chat already exists in 'chats_no_duplicate_ids', thefore
				#it must also exist in (and the chat should be be added to) 'chats_no_duplicates'
				pass

		return chats_no_duplicates 
		

	#Untested
	def get_displayable_chats(self, warframe_account):
		'''Returns all displayable chats as an array of Chat instances

		:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
		:type [ParamName]: [ParamType](, optional)
		...
		:raises [ErrorType]: [ErrorDescription]
		...
		:return: [ReturnDescription]
		:rtype: [ReturnType]
		'''
		#chats_still_in = self.chats_wfa_still_in(warframe_account)
		chats_in = self.chats_wfa_is_in
		#chats_with_new_msgs = self.chats_with_new_msgs(warframe_account)

		# Array containing chats_still_in and _chats_with_new_msgs might contain duplicates.
		# We don't want duplicates so let's remove them.
		displayable_chats = self._get_non_duplicate_chats(chats_still_in + chats_with_new_msgs)

		return displayable_chats


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

		#extra_fields.setdefault('still_in_chat', True)
		#extra_fields.setdefault('datetime_left_chat', None)
		#extra_fields.setdefault('datetime_last_viewed_chat', timezone.now())

		chat_user = self.model(warframe_account_id=warframe_account_id, chat_id=chat_id, **extra_fields)

		chat_user.save()

		return chat_user

class ChatMessageManager(models.Manager):

	def create_chat_message(self, chat_user_id = None, message="", **extra_fields):
		
		if chat_user_id is None:
			raise ValueError("chat_user_id cannot be None")
		
		extra_fields.setdefault("datetime_created", timezone.now())

		message = self.model(chat_user_id=chat_user_id, message=message, **extra_fields)

		message.save()

		return message
		

	

