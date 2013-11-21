# The back-end file for the Honeypot Analyzer.
# This program reads in records from a HoneyD log file,
# parses them, and stores them in a SQLite database.
#
# Command line usage:
#       python backend_new.py --log <logfile name> --db <database name>
#	   
# You can find out more about HoneyD here: http://www.honeyd.org
#
# Authors: 
# 	Thai-Son Le
# 	Stephen Antalis
# 	Stephen Finney


import argparse
import csv
import json
import os
import requests
from time import time


def process_args():
	"""Returns the names of the database and log file."""
	
	# A small description of the application for the manual
	about_app = 'Process a HoneyD log file and store it into a database.'


	# Parse the command line arguments (if specified) and 
	# assign their values to some variables.
	arg_parser = argparse.ArgumentParser(description = about_app)

	# Unique ID pulled from login information from front end
	arg_parser.add_argument('-c', '--client', type=str, default='user',
							help='the user\'s name. Default: user')

	# Log file name
	arg_parser.add_argument('-l', '--log', type=str, default='logfile.log',
							help='the log file\'s name. Default: logfile.log')

	# Database name						
	arg_parser.add_argument('-d', '--db', type=str, default='logs',
							help='the database\'s name. Default: logs')

	# Bool to see if this is a static log file that won't need to be checked for updates
	arg_parser.add_argument('-s', '--static', type=bool, default=True,
							help='is this log file static? Default: True')

	# Bool to see if this is an update to an earlier static log file
	arg_parser.add_argument('-u', '--update', type=bool, default=False,
							help='is this an update of an earlier log file? Default: False')
	
	args = vars( arg_parser.parse_args() )
	
	client_name, log_name, db_name, static_bool, update_bool = args.values()

	return (client_name, log_name, db_name, static_bool, update_bool)

def process_log(log_name, db_name, last_update = 0):
	"""Processes the log entries and inserts them into the database.
	
	Keyword arguments:
	log_name -- the log file's name
	db_name  -- the database file's name
	"""


	url = 'http://localhost:5984/' + str(db_name)
	headers = {'content-type': 'application/json'}
	
	
	with open(log_name, 'r') as log:
		if log.seek(-1) == last_update:
			return last_update
		
		# Time this function's runtime
		start = time()
		
		csv_data = csv.reader(log, delimiter=' ')

		batch = []
		
		for row in csv_data:
						
			if "honeyd" in row[1]:
				continue
				
				
			elif "icmp" in row[1]:
			
				entry["date"], entry["time_of_day"] = rreplace(row[0], '-', ' ', 1).split()
				
				entry["protocol"] = row[1][:4]

				entry["connection"], entry["src_ip"], \
				entry["dst_ip"] = row[2:5]
				
				entry["info"] = ''.join(row[5] + " " + row[6])
				
				if '[' in row[-1]:
					entry["environment"] = row[-1]

				batch.append(entry)

				# Insert the entries when the count reaches 5000.
				# Preliminary benchmarks report a speed of about 6,000 records per second
				# for batch inserts of 5,000.
				if len(docs) >= 5000:
					payload = {"docs":batch}

					req = requests.post(url, 
							data=json.dumps( payload, separators=(',', ': ') ), 
							 headers=headers)
					if not req.status_code in (200,201):
						print("A problem occurred when saving records to the database.")
						print("HTTP Response: " + str(req.status_code))
						return
					batch = []
							  
		
			elif "udp" in row[1] or "tcp" in row[1]:
					
				entry["date"], entry["time_of_day"] = rreplace(row[0], '-', ' ', 1).split()			
				
				entry["protocol"] = row[1][:3]

				entry["connection"], entry["src_ip"], \
				entry["src_port"], entry["dst_ip"], entry["dst_port"] = row[2:7]
				
				if len(row) >= 9:
					entry["info"] = ''.join(row[7] + " " + row[8])
				elif len(row) >= 8:
					entry["info"] = ''.join(row[7])
									
				if '[' in row[-1]:
					entry["environment"] = row[-1]
					
				batch.append(entry)

				if len(docs) >= 5000:
					payload = {"docs":batch}

					req = requests.post(url, 
						data=json.dumps( payload, separators=(',', ': ') ), 
						 headers=headers)
					if not req.status_code in (200,201):
						print("A problem occurred when saving records to the database.")
						print("HTTP Response: " + str(req.status_code))
						return
					batch = []


		last_update = log.tell()
		with open(log_name[:-3] + "txt", 'w') as pointers:
			pointers.write(str(last_update))	
				
	end = time()
	print("Program Complete.")
	print("Processing time: " + str(end-start))
		
	return last_update
		
		
def rreplace(s, old, new, occurrence):
	"""Returns new string with the replaced character(s).
	
	Credit goes to "mg." from StackOverflow, Question ID: 2556108
	
	Keyword arguments:
	s   -- the string to parse
	old -- the character to find and replace
	new -- the new character to replace the old one(s) with
	"""
	
	li = s.rsplit(old, occurrence)
	return new.join(li)

def main():
	client_name, log_name, db_name, static_bool, update_bool = process_args()

	# We will use the front end to create our unique client folders which will be contained inside the Clients folder
	# We will store usernames and passwords in a database controlled by the frontend
	
	if static_bool:
		path = ("Clients/" + str(client_name) + "/" + (log_name))
	
		if update_bool:
			with open("Clients/" + client_name + "/" + log_name[:-3] + "txt", 'r') as pointers:
				last_update = int(pointers.readline())

			
			process_log(path, db_name, last_update) 
		else:
			process_log(path, db_name)

	else:
		# Assume log file is on program server (will probably change later)
		
		path = ("Clients/" + client_name + "/" + log_name)

		try:
			with open(path[:-3] + "txt", 'r') as pointers:
				last_update = int(pointers.readline())
				
		except IOError:
			last_update = 0
			pass

		while True:
			last_update = process_log(path, db_name, last_update)
			
		

# Main code below
if __name__ == "__main__":
	main()































        
	
