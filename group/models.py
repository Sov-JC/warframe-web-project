from django.db import models
from django.conf import settings

from user.models import User

# Create your models here.
class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    host_user_id = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.PROTECT,
        db_column = "host_user_id"
    )
    relic_id = models.ForeignKey(
        'Relic', 
        on_delete = models.PROTECT
    )
    run_type_id = models.ForeignKey(
        'RunType',
        on_delete = models.PROTECT
    )
    players_in_group = models.IntegerField()