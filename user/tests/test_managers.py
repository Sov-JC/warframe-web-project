from django.test import TestCase
from django.urls import reverse
from user.models import *
from chat.models import *
from relicinventory.models import *
from user.managers import *
from django.core import mail
from django.utils import timezone
from datetime import datetime, timedelta
import string

class GamingPlatformManagerTests(TestCase):
	fixtures=["user_app-user-status.json", "user_app-gaming-platforms.json"]
	
	def setUp(self):
		pass
		
	def test__create_warframe_account_without_warframe_alias_throws_exception(self):
		'''
		_create_warframe_account should throw a ValueError when a warframe_alias argument is
		not set with the exception message "warframe_alias argument is required".
		'''
		
		with self.assertRaisesMessage(ValueError, "warframe_alias argument is required"):
			WarframeAccount.objects._create_warframe_account()


	def test_create_warframe_account_sets_defaults(self):
		'''
		create_warframe_account should create a warframe account with the defaults working. 
		The defaults set the gaming platform to PC and the is_blocked property to False
		'''
		wfa = WarframeAccount.objects.create_warframe_account(warframe_alias="joeTenno")

		self.assertEqual(wfa.warframe_alias, "joeTenno")
		self.assertEqual(wfa.is_blocked, False)
		self.assertEqual(wfa.gaming_platform_id.platform_name, 'PC')



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

class PasswordRecoveryManagerTests(TestCase):

	fixtures=[
		"user_app-user-status.json", 
		"user_app-gaming-platforms.json",
		#"relicinventory_app-relics.json"
	]

	def setUp(self):
		'''
		Create a test user with email 'testuser@example.com' with a linked
		warframe account 'warframeaccount1'.
		'''
		email = 'testuser@example.com'
		password = 'testPassword123'

		wfa1 = WarframeAccount.objects.create_warframe_account(
			warframe_alias="warframeaccount1",
		)
		
		User.objects.create_user(
			email=email,
			linked_warframe_account_id=wfa1,
			password=password)

	def test__generate_password_recovery_code_returns_valid_random_string(self):
		'''
		Should return a fixed length random string of valid characters
		'''

		chars = "a1"
		length = 254

		generated_string = ""

		for i in range(length):
			generated_string += chars[random.randint(0,len(chars)-1)]

		all_string_valid = True

		for ch in generated_string:
			if ch not in chars:
				all_string_valid = False

		msg = "Expected generated string to contain only valid characters, but non valid characters exists."
		self.assertEqual(all_string_valid, True, msg=msg)

		self.assertEqual(len(generated_string), 254)

	def test_generate_password_recovery_code_returns_valid_random_string(self):
		'''
		Should return a fixed length random string of valid characters.
		'''
		valid_numbers = "0123456789"
		valid_chars = string.ascii_letters + valid_numbers

		#the max length of the recovery code field
		expected_length = PasswordRecovery._meta.get_field('recovery_code').max_length

		generated_string = ""

		for i in range(expected_length):
			generated_string += valid_chars[random.randint(0,len(valid_chars)-1)]

		all_string_valid = True

		for ch in generated_string:
			if ch not in valid_chars:
				all_string_valid = False

		msg = "Expected generated string to contain only valid characters, but non valid characters exists."
		self.assertEqual(all_string_valid, True, msg=msg)

		self.assertEqual(len(generated_string), expected_length)

	def test_create_password_recovery_creates_password_recovery_row(self):
		'''Calling create_password_recovery should create a password_recovery
		row.'''
		user = User.objects.get(email="testuser@example.com")
		time_now = timezone.now()
		time_20ms_ago = timezone.now() - timedelta(milliseconds=20)# time 20 ms ago
		password_recovery = PasswordRecovery.objects.create_password_recovery(user)

		msg="Expected password_recovery.user_id field to reference user with email of 'testuser@example.com'"
		self.assertEqual(password_recovery.user_id.pk, User.objects.get(email="testuser@example.com").pk)
		
		recovery_code = password_recovery.recovery_code
		expected_length = PasswordRecovery._meta.get_field('recovery_code').max_length

		msg="Expected the length of the recovery_code to be the maximum length of \
		the recovery code field's max_length value."
		self.assertEqual(len(recovery_code), expected_length)
		
		msg="Expected datetime_code_created field to be less than 20ms old and not in the future"
		self.assertLessEqual(time_20ms_ago, password_recovery.datetime_code_created, msg=msg)
		self.assertLessEqual(password_recovery.datetime_code_created, timezone.now(), msg=msg)

	def test__create_password_recovery_with_no_user_raises_value_error(self):
		'''Should raise a ValueError if a user is not set as an argument.'''
		raise NotImplementedError()

	def test_created_password_recovery_generates_http_link_on_debug_mode_enabled(self):
		'''If debug mode is enabled in the settings, the default password link
		that's generated should be HTTP, not HTTPS, for testing and debugging purposes.
		HTTPS otherwise.
		'''
		raise Exception

	def test_send_password_recovery_email_sends_new_password_recovery_email(self):
		'''Should send a new password recovery email to the user's registered email.'''
		user = User.objects.get(email="testuser@example.com")
		PasswordRecovery.objects.send_password_recovery_email(user)

		self.assertEqual(len(mail.outbox), 1, msg="Expected email to be sent out.")

		print("user's recovery code is: " + user.password_recovery.recovery_code)
		msg = "Expected recovery code to be sent along with the email"
		self.assertEqual(user.password_recovery.recovery_code in mail.outbox[0], True, msg=msg)

		raise NotImplementedError()

class WarframeAccountManagerTests(TestCase):
	fixtures=[
		"user_app-user-status.json", 
		"user_app-gaming-platforms.json",
		"relicinventory_app-relics.json"
	]

	def test_get_linked_and_online_wfas_that_own_relic(self):
		'''Should return a Set of Warframe account ids that are online, are 
		from a particular gaming platform, and own a specific Relic.
		'''
		# Create two users with a linked warframe account. Set their online status to online.
		# Make these two accounts have a common relic in their inventory.
		print(UserStatus.objects.all())
		online_status = UserStatus.objects.get(user_status_name=UserStatus.ONLINE)

		
		pc_gaming_platform = GamingPlatform.objects.get(platform_name=GamingPlatform.PC)

		wfa_test1 = WarframeAccount.objects.create_warframe_account("wfa_test1")
		wfa_test2 = WarframeAccount.objects.create_warframe_account("wfa_test2")
		relic = Relic.objects.get(pk=30)

		user_test1 = User.objects.create_user(
			email="wfa_test1@gmail.com",
			password="jqoiwjeq123",
			linked_warframe_account_id=wfa_test1,
			user_status=online_status)
		user_test2 = User.objects.create_user(
			email="wfa_test2@gmail.com",
			password="jqoiwjeq123", 
			linked_warframe_account_id=wfa_test2,
			user_status=online_status)
		
		OwnedRelic.objects.add_relics_to_inventory(wfa_test1, [relic.pk])
		OwnedRelic.objects.add_relics_to_inventory(wfa_test2, [relic.pk])

		wfa_ids = WarframeAccount.objects.get_linked_wfa_ids_that_own_relic_on_platform(relic, pc_gaming_platform)

		msg="Expected the call to function 'get_linked_wfa_ids_that_own_relic_on_platform' " \
			"to return only two warframe account ids."
		self.assertTrue(len(wfa_ids) == 2, msg=msg)

		msg = "Expected wfa_test1.pk and wfa_test2.pk to be the only pks in the list returned by " \
			+ "function 'get_linked_wfa_ids_that_own_relic_on_platform()'"
		
		is_subset = set([wfa_test1.pk, wfa_test2.pk]).issubset(wfa_ids)
		self.assertTrue(is_subset, msg=msg)