import sys, os, csv, django
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'warframe_web_project.settings'
django.setup()

from chat.models import *
from group.models import *
from relicinventory.models import Relic, OwnedRelic
from report.models import *
from user.models import *
#data = csv.reader(open("ADDRESS.csv"),delimiter=",")

''' 
The order that csv table data should be inserted.
Ordering is necessary because there are foreign key 
references in many tables. Referenced tables should
be inserted before refrencing tables.
'''
CSV_DATA_INSERTION_ORDER = [
	"relic",
	"run_type",
	"gaming_platform",
	"report_state",
	"warframe_account",
	"user",
	"password_recovery",
	"chat",
	"chat_message",
	"owned_relic",
	"group",
	"report_case",
	"video_proof",
	"image_proof",
]

#the table names are the same as the csv files. The name of
#the db table shares the same name as the csv file.
DB_TABLE_NAMES = [
	"relic",
	"run_type",
	"gaming_platform",
	"report_state",
	"warframe_account",
	"user",
	"password_recovery",
	"chat",
	"chat_message",
	"owned_relic",
	"group",
	"report_case",
	"video_proof",
	"image_proof",
]

DEFAULT_MANAGERS = {
	"relic": Relic.objects,
	"run_type": RunType.objects,
	"gaming_platform": GamingPlatform.objects,
	"report_state": ReportState.objects,
	"warframe_account": WarframeAccount.objects,
	"user": User.objects, 
	"password_recovery": PasswordRecovery.objects,
	"chat": Chat.objects,
	"chat_message": ChatMessage.objects,
	"owned_relic": OwnedRelic.objects,
	"group": Group.objects,
	"report_case": ReportCase.objects,
	"video_proof": VideoProof.objects,
	"image_proof": ImageProof.objects,
}

#remove this function?
def set_up():
	'''
	set up the django environment so
	that we can insert data into the default database
	'''
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = os.path.dirname(dir_path)
	sys.path.append(dir_path)
	os.environ['DJANGO_SETTINGS_MODULE'] = 'warframe_web_project.settings'
	django.setup()


def table_is_populated(table_name=None):

	if table_name is None or (table_name not in DB_TABLE_NAMES):
		return 0
	
	manager = DEFAULT_MANAGERS[table_name]

	if len(manager.all()) == 0:
		return False
	else:
		return True


def display_table_is_populated_warning_and_continue(table_name=""):
	'''
	Display a warning if the table the user wants to populate
	already has some rows inserted in case they forgot to truncate before
	data transfer.
	
	Return True is user wants to continue with the transfer of data to the DB.
	False otherwise
	'''
	input_data = input(
		("Attempted to insert data into the %s table and expected\n" % table_name) +
		"the db table to not be populated, but the table is currently populated.\n" +
		"Type 1 if you would like to populate anyways. Input any other value to cancel test data transfer.\n"
	)

	if input_data != '1':
		print("Test data transfer for table %s canceled." % table_name)
		return False

	return True

def populate_relic_table():
	CSV_FILE_NAME = "relic"
	TABLE_NAME = "relic"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")

	if table_is_populated(TABLE_NAME):
		if display_table_is_populated_warning_and_continue(TABLE_NAME) is False:
			return
	
	firstline = True
	for row in csv_data:
		if firstline:
			firstline = False
			continue
		
		relic = Relic()
		
		relic.relic_id=int(row[0])
		print("[relic_id:%s]" % (relic.relic_id))
		relic.relic_name = row[1]
		print("[relic_name:%s]" % (relic.relic_name))
		relic.wiki_url = row[2]
		print("[wiki_url:%s]" % (relic.wiki_url))

		relic.save()
	
	print("[Success] %s.csv data transfered to the %s table " % CSV_FILE_NAME, TABLE_NAME)

	return


def populate_run_type_table():
	CSV_FILE_NAME = "run_type"
	TABLE_NAME = "run_type"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")

	if table_is_populated(TABLE_NAME):
		if display_table_is_populated_warning_and_continue(TABLE_NAME) is False:
			return
	
	firstline = True
	for row in csv_data:
		if firstline:
			firstline = False
			continue
		
		run_type = RunType()
		
		run_type.run_type_id=int(row[0])
		print("[run_type_id:%s]" % (run_type.run_type_id))
		run_type.type_name = row[1]
		print("[type_name:%s]" % (run_type.type_name))

		run_type.save()

	print("[Success] %s.csv data transfered to the %s table " % CSV_FILE_NAME, TABLE_NAME)

	return

def populate_gaming_platform():
	CSV_FILE_NAME = "gaming_platform"
	TABLE_NAME = "gaming_platform"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")

	if table_is_populated(TABLE_NAME):
		if display_table_is_populated_warning_and_continue(TABLE_NAME) is False:
			return
	
	firstline = True
	for row in csv_data:
		if firstline:
			firstline = False
			continue
		
		gaming_platform = GamingPlatform()

		gaming_platform.gaming_platform_id = int(row[0])
		print("[gaming_platform_id:%s]" % gaming_platform.gaming_platform_id)

		gaming_platform.platform_name = row[1]
		print("[platform_name:%s]" % gaming_platform.platform_name)

		gaming_platform.save()

	return

def populate_report_state():
	pass

def populate_warframe_account():
	CSV_FILE_NAME = "warframe_account"
	TABLE_NAME = "warframe_account"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")

	if table_is_populated(TABLE_NAME):
		if display_table_is_populated_warning_and_continue(TABLE_NAME) is False:
			return
	
	firstline = True
	for row in csv_data:
		if firstline:
			firstline = False
			continue
		
		warframe_account = WarframeAccount()

		warframe_account.warframe_account_id = int(row[0])
		print("[warframe_account_id:%s]" % warframe_account.warframe_account_id)
		warframe_account.warframe_alias = row[1]
		print("[warframe_alias:%s]" % warframe_account.warframe_alias)
		warframe_account.is_blocked = row[2]
		print("[is_blocked:%s]" % warframe_account.is_blocked)

		gaming_platform_id = row[3]
		gaming_platform = GamingPlatform.objects.get(pk=int(gaming_platform_id))

		warframe_account.gaming_platform_id = gaming_platform
		print("[gaming_platform_id:%s]" % gaming_platform_id)

		warframe_account.save()

	print("[Success] %s.csv data transfered to the %s table " % (CSV_FILE_NAME, TABLE_NAME))

def populate_user():
	CSV_FILE_NAME = "user"
	TABLE_NAME = "user"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")

	if table_is_populated(TABLE_NAME):
		if display_table_is_populated_warning_and_continue(TABLE_NAME) is False:
			return
	
	firstline = True
	for row in csv_data:
		if firstline:
			firstline = False
			continue
		
		user_id = row[0]
		password = row[1]
		last_login = row[2]
		is_superuser = row[3]
		email = row[4]
		email_verification_code = row[5]
		email_verified = row[6]
		is_active = row[7]
		is_staff = row[8]
		beta_tester = row[9]
		warframe_account_verification_code = row[10]
		linked_warframe_account_id = row[11]

		user = User()

		user.user_id = user_id
		user.set_password(password)
		user.last_login = None if (last_login is '') else last_login
		user.is_superuser = True if is_superuser is '1' else '0'
		user.email = email
		user.email_verification_code = email_verification_code
		user.email_verified = True if email_verified is '1' else False
		user.is_active = True if is_active is '1' else False
		user.is_staff = True if is_staff is '1' else False
		user.beta_tester = True if beta_tester is '1' else False
		user.warframe_account_verification_code = warframe_account_verification_code

		linked_wf_account_id = WarframeAccount.objects.get(warframe_account_id=linked_warframe_account_id)
		print('warframe_account:%s' % linked_wf_account_id)
		user.linked_warframe_account_id = linked_wf_account_id

		print("[user.user_id:%s]" % user.user_id)
		print("[user.password:%s]" % user.password)
		print("[user.last_login:%s]" % user.last_login)
		print("[user.is_superuser:%s]" % user.is_superuser)
		print("[user.email_verified:%s]" % user.email_verified)
		print("[user.is_active:%s]" % user.is_active)
		print("[user.is_staff :%s]" % user.is_staff )
		print("[user.beta_tester:%s]" % user.beta_tester)
		print("[user.warframe_account_verification_code:%s]" % user.warframe_account_verification_code)
		#print("[@:%s]" % @)

		user.save()

	pass

"""
"relic",
	"run_type",
	"gaming_platform",
	"report_state",
	"warframe_account",
	"user",
	"password_recovery",
	"chat",
	"chat_message",
	"owned_relic",
	"group",
	"report_case",
	"video_proof",
	"image_proof",
"""

def transfer_csv_table_data_to_db():
	for csv_file_name in CSV_DATA_INSERTION_ORDER:
		if csv_file_name == "relic":
			populate_relic_table()
		if csv_file_name ==  "run_type":
			populate_run_type_table()
		
	pass

#transfer_csv_table_data_to_db()
#populate_run_type_table()
#populate_gaming_platform()
#populate_warframe_account()
populate_user()