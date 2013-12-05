# The back-end file for the Honeypot Analyzer.
# This program reads in records from a HoneyD log file,
# parses them, and sends them to our web application over HTTPS.
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
import requests
from time import time


def process_args():
	"""Returns the values of the command line arguments from the user."""
	
	# A small description of the application for the manual
	about_app = 'Process a HoneyD log file and send it to a database.'


	# Parse the command line arguments (if specified) and 
	# assign their values to some variables.
	arg_parser = argparse.ArgumentParser(description = about_app)


	# The list of arguments to add to the program.
	# Current list:
	#	User name		- The user's name on the website
	#	Log filename		- The logfile's name
	#	Static file boolean 	- Is this log static, i.e. not being updated by HoneyD?
	#	Update file boolean	- Is this file an update of a previously entered log?
	arg_list = [ 
		     ['--user', str, 'user', 'the user\'s name. Default: user'],
		     ['--log', str, 'logfile.log', 'the log file\'s name. Default: logfile.log'],
		     ['--update', bool, False, 'is this an update of an earlier log file? Default: False'],
		     ['--static', bool, True, 'is this log file static? If HoneyD is updating this file, choose False. Default: True'],
	           ]

	for arg in arg_list:
		arg_parser.add_argument(arg[0], type=arg[1], default=arg[2], help=arg[3])

	# Unique ID pulled from login information from front end
	#arg_parser.add_argument('-c', '--client', type=str, default='user',
	#						help='the user\'s name. Default: user')

	# Log file name
	#arg_parser.add_argument('-l', '--log', type=str, default='logfile.log',
	#						help='the log file\'s name. Default: logfile.log')

	# Database name						
	#arg_parser.add_argument('-d', '--db', type=str, default='logs',
	#						help='the database\'s name. Default: logs')

	# Bool to see if this is a static log file that won't need to be checked for updates
	#arg_parser.add_argument('-s', '--static', type=bool, default=True,
	#						help='is this log file static? Default: True')

	# Bool to see if this is an update to an earlier static log file
	#arg_parser.add_argument('-u', '--update', type=bool, default=False,
	#						help='is this an update of an earlier log file? Default: False')
	

	# Parse and retrieve the command line arguments given.
	args = vars( arg_parser.parse_args() )

	# The parser returns the arguments in this particular order.
	#static_bool, client_name, db_name, log_name, update_bool = args.values()
	update_bool, static_bool, user_name, log_name = args.values()

	# Let's return the arguments like this; it makes more sense
	return user_name, log_name, static_bool, update_bool


def process_log(log_name, user_name, last_update = 0):
	"""
	Processes the log entries and inserts them into the database.
	
	Keyword arguments:
	log_name    -- The log file's name.
	user_name   -- The user's name on the website.
	last_update -- The last update of this logfile, if it exists.
	"""


	url = 'http://localhost:8000/' + str(user_name) + "/bulkdocs"
	headers = {'content-type': 'application/json'}
	
	
	with open(log_name, 'r') as log:

		# Seek to position of last update
		# If last update is the end of the file, quit.
		if log.seek(-1) == last_update:
			return last_update
		else:
			log.seek(last_update)

		
		# Time this function's runtime
		start = time()
		
		csv_data = csv.reader(log, delimiter=' ')

		batch = []
		
		for row in csv_data:
						
			if "honeyd" in row[1]:
				continue

			else:
				# Do the parsing common to all protocol types
				entry["date"], entry["time_of_day"] = rreplace(row[0], '-', ' ', 1).split()
				
				entry["connection"], entry["src_ip"] = row[2:4]

				if '[' in row[-1]:
					entry["environment"] = row[-1]
				else:
					entry["environment"] = "-"
				
				
			if "icmp" in row[1]:
			
				entry["protocol"] = row[1][:4]

				entry["dst_ip"] = row[4]
				
				entry["info"] = ''.join(row[5] + " " + row[6])

				batch.append(entry)

				if save_data(url, headers, payload):
					batch = []

		
			elif "udp" in row[1] or "tcp" in row[1]:
					
				entry["protocol"] = row[1][:3]

				entry["src_port"], entry["dst_ip"], entry["dst_port"] = row[4:7]
				
				if len(row) >= 9:
					entry["info"] = ''.join(row[7] + " " + row[8])
				elif len(row) >= 8:
					entry["info"] = ''.join(row[7])
									
				batch.append(entry)

				if save_data(url, headers, payload):
					batch = []


		last_update = log.tell()
		with open(log_name[:-3] + "txt", 'w') as pointers:
			pointers.write(str(last_update))	
				
	end = time()
	print("Program Complete.")
	print("Processing time: " + str(end-start))
		
	return last_update
		
		
def rreplace(s, old, new, occurrence):
	"""
	Returns new string with the replaced character(s).
	
	Credit goes to "mg." from StackOverflow, Question ID: 2556108
	
	Keyword arguments:
	s   -- the string to parse
	old -- the character to find and replace
	new -- the new character to replace the old one(s) with
	"""
	
	li = s.rsplit(old, occurrence)
	return new.join(li)


def main():
	"""The main function for the program. It'll drive the methods and data."""

	user_name, log_name, static_bool, update_bool = process_args()

	# We will use the front end to create our unique client folders which will be contained inside the Clients folder
	# We will store usernames and passwords in a database controlled by the frontend
	
	if static_bool:

		path = ("Users/" + str(user_name) + "/" + (log_name))
	
		if update_bool:

			with open("Users/" + user_name + "/" + log_name[:-3] + "txt", 'r') as pointers:
				last_update = int(pointers.readline())
			
			process_log(path, user_name, last_update) 
		else:
			process_log(path, user_name)

	else:
		# Assume log file is on program server (will probably change later)
		path = ("Users/" + user_name + "/" + log_name)

		try:
			with open(path[:-3] + "txt", 'r') as pointers:
				last_update = int(pointers.readline())
				
		except IOError:
			last_update = 0

		while True:
			last_update = process_log(path, user_name, last_update)
			

def save_data(url, headers, payload):
	"""
	Saves the given payload into our web application's database over HTTPS

	Keyword arguments:
	url     -- The url to send the HTTPS POST request to.
	headers -- The headers to send along with the POST.
	payload -- The collection of records to send to the web application.
	"""

	# Insert the entries when the count reaches 5000.
	# Preliminary benchmarks report a speed of about 6,000 records per second
	# for batch inserts of 5,000.
	if len(docs) >= 5000:
		payload = {"docs":batch}

		req = requests.post(url, 
			data=json.dumps( payload, separators=(',', ': ') ), 
			headers=headers)

		if not req.status_code in (200,201):

			for i in range(0,5):
				print("A problem occurred when saving records to the database.")
				print("HTTP Response: " + str(req.status_code))
				print("Retrying..." + i + " attempts remaining")

				req = requests.post(url, 
					data=json.dumps( payload, separators=(',', ': ') ), 
					headers=headers)

			if not status_code in (200,201):
				print("Record save failed! We'll try again next time around.")


# Main code below
if __name__ == "__main__":
	main()

