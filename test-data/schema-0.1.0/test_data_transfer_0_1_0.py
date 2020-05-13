import sys, os, csv, django
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.dirname(dir_path)
dir_path = os.path.dirname(dir_path)
sys.path.append(dir_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'warframe_web_project.settings'
django.setup()
from chat.models import *
from relicinventory.models import *
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

def relic_table_transfer():
	CSV_FILE_NAME = "relic"
	TABLE_NAME = "relic"
	
	print("Reading csv file '%s'..." % CSV_FILE_NAME)
	csv_data = csv.reader(open("%s.csv" % CSV_FILE_NAME),delimiter=",")
	
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


		print("[Success] relic.csv data transfered to the relic table -- Not saved though.")
	

def transfer_data_to_db():
	for csv_file_name in CSV_DATA_INSERTION_ORDER:
		if csv_file_name == "relic":
			relic_table_transfer()
		
	pass

transfer_data_to_db()

"""
firstline = True
for row in data:
	if firstline:
		firstline = False
		continue
	print("Reading ADDRESS model ...")
	addr = ADDRESS()
	
	addr.Address_ID=int(row[0])
	print("Address_ID = " + str(addr.Address_ID))

	addr.Zip_Post=row[1]
	print("Zip_Post = " + addr.Zip_Post)

	addr.Address_1=row[2]	
	print("Address_1  = " + addr.Address_1)

	addr.Address_2=row[3]	
	print("Address_2  = " + addr.Address_2)

	addr.Country=row[4]	
	print("Country  = " + addr.Country)

	addr.State=row[5]	
	print("State  = " + addr.State)

	addr.City_Town=row[6]
	print("City_Town  = " + addr.City_Town)

	addr.Name=row[7]	
	print("Name  = " + addr.Name)


	addr.save()
	print("ADDRESS read SUCCESSFUL")
"""