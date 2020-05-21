from django.db import models
from django.conf import settings

from user.models import User
from user.models import WarframeAccount
from relicinventory.models import Relic

from .managers import *

class RelicQuality(models.Model):
    relic_quality_id = models.AutoField(primary_key=True)
    INTACT = "Intact"
    EXCEPTIONAL = "Exceptional"
    FLAWLESS = "Flawless"
    RADIANT = "Radiant"
    RELIC_QUALITY_NAME_CHOICES = [
        (INTACT,"Intact"),
        (EXCEPTIONAL,"Exceptional"),
        (FLAWLESS, "Flawless"),
        (RADIANT, "Radiant")
    ]
    relic_quality_name = models.CharField(
        max_length=64, 
        unique=True,
        choices=RELIC_QUALITY_NAME_CHOICES
    )

    class Meta:
        db_table = "group_relic_quality"


class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    host_warframe_account_id = models.OneToOneField(
        WarframeAccount,
        on_delete = models.PROTECT,
        db_column = "host_user_id"
    )
    relic_id = models.ForeignKey(
        Relic, 
        on_delete = models.PROTECT,
    )
    run_type_id = models.ForeignKey(
        'RunType',
        on_delete = models.PROTECT
    )
    players_in_group = models.IntegerField()
    relic_quality_id = models.ForeignKey(
        RelicQuality,
        on_delete = models.PROTECT
    )
    datetime_created = models.DateTimeField(auto_now_add=True)

    objects = GroupManager()

    class Meta:
        db_table="group_group"


class RunType(models.Model):
    run_type_id = models.AutoField(primary_key=True)
    ONE_BY_ONE = "one by one"
    TWO_BY_TWO = "two by two"
    FOUR_BY_FOUR = "four by four"

    RUN_TYPE_NAME_CHOICES = [
        (ONE_BY_ONE, 'one by One'),
        (TWO_BY_TWO, 'two by two'),
        (FOUR_BY_FOUR, 'four by four')
    ]

    type_name = models.CharField(
        max_length=16, 
        unique=True,
        choices=RUN_TYPE_NAME_CHOICES
    )

    objects = RunTypeManager()

    class Meta:
        db_table = "group_run_type"


