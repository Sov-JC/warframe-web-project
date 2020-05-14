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

#data = csv.reader(open("ADDRESS.csv"),delimiter=",")

''' 
The order that csv table data should be inserted.
Ordering is necessary because there are foreign key 
references in many tables.
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

#the table names are the same as the csv files. Ther name of
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
	#"gaming_platform": GamingPlatform.objects,
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


def display_table_is_populated_warning(table_name=""):
	input_data = input(
		("Attempted to insert data into the %s table and expected\n" % table_name) +
		"the db table to not be populated, but the table is currently populated.\n" +
		"Type 1 if you would like to populate anyways. Input any other value to cancel test data transfer.\n"
	)

	if input_data != 1:
		print("Test data transfer for table %s canceled." % table_name)

	return

def populate_relic_table():
	CSV_FILE_NAME = "relic"
	TABLE_NAME = "relic"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")

	if table_is_populated(TABLE_NAME):
		display_table_is_populated_warning()

	"""
	if len(Relic.objects.all()) != 0:
		display_table_is_populated_warning()
	"""
	
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
		print("[Success] relic.csv data transfered to the relic table ")

def populate_run_type_table():
	pass

def transfer_csv_table_data_to_db():
	for csv_file_name in CSV_DATA_INSERTION_ORDER:
		if csv_file_name == "relic":
			populate_relic_table()
		if csv_file_name ==  "run_type":
			populate_run_type_table()
		
	pass


transfer_csv_table_data_to_db()