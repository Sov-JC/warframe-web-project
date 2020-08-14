from django.db import models
from user.models import User, WarframeAccount

# Create your models here.
class PrivateMessage(models.Model):
	private_message_id = models.AutoField(primary_key=True)
	datetime_created = models.DateTimeField(auto_now_add=True)
	sender_warframe_account_id = models.ForeignKey(WarframeAccount, 
		on_delete=models.PROTECT,
		db_column="sender_warframe_account_id",
		related_name= "private_msgs_sent"
	)
	receiver_warframe_account_id = models.ForeignKey(WarframeAccount, 
		on_delete=models.PROTECT,
		db_column="receiver_warframe_account_id",
		related_name = "private_msgs_received"
	)
	has_been_read = models.BooleanField(default=False)

	

	def _delete_all_messages_between(self, warframe_account_one, warframe_account_two):
		'''
		Delete all private messages between warframe_account_one and warframe_account_two
		'''
		raise NotImplementedError


	# Incomplete
	def _has_sender_exceeded_distinct_receivers_limit(self, warframe_account, limit):
		'''
		Determine if 'warframe_account' has sent messages
		to more than 'limit' different WarframeAccount instances.

		For instance, if a user has sent messages to 51 or more different warframe accounts
		and the limit is set to 50 then True is returned. If the same limit is applied
		and 'warframe_account' has sent messages to 50 or less different warframe accounts
		then False is returns.

		This operation is useful to 
		'''
		raise NotImplementedError

	def _delete_pic_between(self, closer_warframe_account, closee_warframe_account):
		'''Deletes the PrivateInteractionClosed

		:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
		:type [ParamName]: [ParamType](, optional)
		...
		:raises [ErrorType]: [ErrorDescription]
		...
		:return: [ReturnDescription]
		:rtype: [ReturnType]
		'''

		raise NotImplementedError

	def _get_least_recent_receiver_wfa(self, warframe_account):
		'''
		Returns the WarframeAccount instance that 'warframe_account' sent a message
		too least recently.
		'''

		#O(logn + 50) = O(logn) search where n is the size of private messages

		raise NotImplementedError
	
	def _delete_all_messages_of_least_recent_receiver(self, warframe_account):
		'''
		Detects the least recent Warframe Account instance that 'warframe_account' has sent a message to
		and deletes all messages between these two WarframeAccount instances. In addition deletes
		their corresponding private_interactions_closed settings.

		Returns the warframe_account_id of the
		'''

		receiver_target = self._get_least_recent_receivers_wfa(warframe_account)

		raise NotImplementedError
		
	
	def save(self, *args, **kwargs):
		if self.sender_warframe_account_id == self.receiver_warframe_account_id:
			raise ValueError('sender_warframe_account and receiver_warframe_account cannot be the same. '\
				'(a user warframe account cannot message itself.)')

		sender_wfa = self.sender_warframe_account_id

		DISTINCT_RECEIVERS_LIMIT = 50

		exceeded_distinct_receivers_limit = self._has_sender_exceeded_distinct_receivers_limit(sender_wfa,DISTINCT_RECEIVERS_LIMIT)
		

		if(exceeded_distinct_receivers_limit):
			'''
			Delete messages between 'sender' WarframeAccount instance and the
			Warframe account instance that the 'sender' least recently messaged.
			'''
			least_recent_receiver_wfa = self._get_least_recent_receiver_wfa(sender_wfa)
			self._delete_all_messages_between(sender_wfa, least_recent_receiver_wfa)
			self._delete_pic_information_between(sender_wfa, least_recent_receiver_wfa)

		super(PrivateMessage, self).save(*args, **kwargs)


	class Meta:
		db_table = "privatemessage_private_message"
		# constraints = [
        #     models.UniqueConstraint(
        #         fields = [
        #             'sender_warframe_account_id',
        #             'receiver_warframe_account_id',
        #         ],
        #         name = 'unique_together_sender_wfa_and_receiver_wfa'
        #     )
        # ]
