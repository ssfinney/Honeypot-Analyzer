# The back-end file for the Honeypot Analyzer.
# This program reads in records from a HoneyD log file,
# parses them, and stores them in a SQLite database.
#
# You can find out more about HoneyD here: http://www.honeyd.org
#
# Authors: 
# 	Thai-Son Le
#	Stephen Antalis
# 	Stephen Finney


import argparse
import csv
import sqlite3
from time import time


def process_args():
	"""Returns the names of the database and log file."""
	
	# A small description of the application for the manual
	about_app = 'Process a HoneyD log file and store it into a database.'


	# Parse the command line arguments (if specified) and 
	# assign their values to some variables.
	arg_parser = argparse.ArgumentParser(description = about_app)

	arg_parser.add_argument('-l', '--log', type=str, default='logfile.log',
							help='the log file\'s name. Default: logfile.log')
							
	arg_parser.add_argument('-d', '--db', type=str, default='log.sqlite',
							help='the database\'s name. Default: log.sqlite')
	
	
	args = vars( arg_parser.parse_args() )
	
	db_name, log_name = args.values()

	
	return (log_name, db_name)


def process_log(log_name, db_name):
	"""Processes the log entries and inserts them into the database.
	
	Keyword arguments:
	log_name -- the log file's name
	db_name  -- the database file's name
	
	"""


	# Open a connection to the local SQLite database.
	#db = sqlite3.connect(db_name)
	
	
	with open(log_name, 'r') as log:
		
		# Time this function's runtime
		start = time()
		
		csv_data = csv.reader(log, delimiter=' ')
		
		for row in csv_data:
			
			if "honeyd" in row[1]:
				print("FIRE")
				continue
				
			elif "icmp" in row[1]:
				print("FIRE")
				date, protocol, connection, src_ip, \
				dst_ip, info, comment = row
				
				print(date + protocol + connection + src_ip+ \
					  dst_ip + info + comment)
		
		
	#if __name__ == __main__:
log_name, db_name = process_args()
		
process_log(log_name, db_name)
		