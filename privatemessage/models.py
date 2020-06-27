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

	def save(self, *args, **kwargs):
		if self.sender_warframe_account_id == self.receiver_warframe_account_id:
			raise ValueError('sender_warframe_account and receiver_warframe_account cannot be the same. '\
				'(a user warframe account cannot message itself.)')

		super(PrivateMessage, self).save(*args, **kwargs)


	class Meta:
		db_table = "privatemessage_private_message"
		constraints = [
            models.UniqueConstraint(
                fields = [
                    'sender_warframe_account_id',
                    'receiver_warframe_account_id',
                ],
                name = 'unique_together_sender_wfa_and_receiver_wfa'
            )
        ]
