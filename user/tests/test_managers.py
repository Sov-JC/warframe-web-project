from django.test import TestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.managers import *

class LinkedOnlineUsersManagerTests(TestCase):

	def setUp(self):
		xbox = GamingPlatform(platform_name="Xbox")
		ps = GamingPlatform(platform_name="PlayStation")
		xbox.save()
		ps.save()

		online = UserStatus(user_status_name = "online").save()
		offline = UserStatus(user_status_name = "offline").save()

		wf_acc_1 = WarframeAccount(warframe_alias="wf1", gaming_platform_id=xbox)
		wf_acc_2 = WarframeAccount(warframe_alias="wf2", gaming_platform_id=xbox)
		wf_acc_3 = WarframeAccount(warframe_alias="wf3", gaming_platform_id=ps)

		wf_acc_1.save()
		wf_acc_2.save()
		wf_acc_3.save()

		user1 = User.objects.create_user(email = "example1@aaa.com", password="jqwioqwje90")
		user2 = User.objects.create_user(email = "example2@aaa.com", password="jqwioqwje90")
		user3 = User.objects.create_user(email = "example3@aaa.com", password="jqwioqwje90")
		user4 = User.objects.create_user(email = "unlinkedofflineuser@yahoo.com", password="je89j234j")


		user1.user_status = online
		user2.user_status = online
		user3.user_status = offline

		user1.linked_warframe_account_id = wf_acc_1
		user2.linked_warframe_account_id = wf_acc_2
		user3.linked_warframe_account_id = wf_acc_3

		user1.save()
		user2.save()
		user3.save()
		user4.save()

	def test_queryset(self):
		query_set = User.online_and_linked_users.all()
		user_1 = query_set[0]
		user_2 = query_set[1]
		
		self.assertEqual(2, len(query_set))
		
		self.assertEqual(user_1.email, "example1@aaa.com")
		self.assertEqual(user_2.email, "example2@aaa.com")

