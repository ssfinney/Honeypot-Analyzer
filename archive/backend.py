#!/usr/bin/python
#simple python csv parser that export to SQL
import csv
import MySQLdb

# open the connection to the MySQL server.
# using MySQLdb

mydb = MySQLdb.connect(host='localhost',
	user='csv',
	passwd='csv',
	db='csvdb')
cursor = mydb.cursor()

# read the log file using the python
# csv modules http://docs.python.org/library/csv.html
with open('logfile.log', "r") as fin:
	csv_data = csv.reader(fin, delimiter=' ')
	for row in csv_data:
		commentSpot = 0
		if row[1] == "honeyd":
			pass
		elif row[1] == "icmp(1)":	
			row[0] = row[0][0:10]+' '+row[0][11:]
			for i in range(6, len(row) -1):
				row[5] += ' ' + row[i]
			del row[6:]
			cursor.execute('INSERT INTO HONEYD(DATE, PROTOCOL, CONNECTION, SRCIP, DSTIP, INFO)' 'VALUES(%s, %s, %s, %s, %s, %s)', row)
		elif row[1] == "tcp(6)":
			row[0] = row[0][0:10]+' '+row[0][11:]
			temp = " ".join(row[7:]).split("[")
			del row[7:]
			row.append(temp[0].lstrip())
			row.append(temp[1][:-1]
			cursor.execute('INSERT INTO HONEYD(DATE, PROTOCOL, CONNECTION, SRCIP, SRCPORT, DSTIP, DSTPORT, INFO, COMMENT)'
					
cursor.close()
print "Import to MySQL is over"
