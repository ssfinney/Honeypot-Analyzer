#!/usr/bin/python
#simple python csv parser that export to SQL
import csv
import sqlite3

from time import time

# open the connection to the SQLite database.
# using SQLite3

mydb = sqlite3.connect('csvdb.sqlite')
cursor = mydb.cursor()

# read the log file using the python
# csv modules http://docs.python.org/library/csv.html
with open('logfile.log', "r") as fin:

	start = time()

	csv_data = csv.reader(fin, delimiter=' ')

	for row in csv_data:
		#print(row)
		commentSpot = 0

		if row[1] == "honeyd":
			pass

		elif row[1] == "icmp(1)":

			#date, protocol, connection, src_ip, \
			#dst_ip, info, comment = row
			
			row[0] = row[0][0:10]+' '+row[0][11:]
			#row[0] = row[0][::-1].replace('-',' ', 1)[::-1]

			for i in range(6, len(row) -1):
				row[5] += ' ' + row[i]

			if '[' not in row:
				row += '['

			temp = " ".join(row[5:]).split("[")

			del row[5:]

			row.append(temp[0].lstrip())
			row.append(temp[1][:-1])

			
			print(row)

			cursor.execute('INSERT INTO ICMP' + \
								'(DATE, PROTOCOL, CONNECTION, ' + \
								'SRCIP, DSTIP, INFO, COMMENT) ' + \
								'VALUES(?,?,?,?,?,?,?);', row)


		elif row[1] == "tcp(6)":

			row[0] = row[0][0:10]+' '+row[0][11:]


			if '[' not in row:
				row += '['

			temp = " ".join(row[7:]).split("[")

			del row[7:]

			row.append(temp[0].lstrip())
			row.append(temp[1][:-1])

			cursor.execute('INSERT INTO TCP' + \
								'(DATE, PROTOCOL, CONNECTION, SRCIP, SRCPORT, ' + \
								'DSTIP, DSTPORT, INFO, COMMENT) ' + \
								'VALUES(?,?,?,?,?,?,?,?,?);', row)


		elif row[1] == "udp(17)":

			row[0] = row[0][0:10]+' '+row[0][11:]

			if '[' not in row:
				row += '['
				
			temp = " ".join(row[7:]).split("[")
			

			del row[7:]

			row.append(temp[0].lstrip())
			row.append(temp[1])

			cursor.execute('INSERT INTO UDP' + \
								'(DATE, PROTOCOL, CONNECTION, SRCIP, SRCPORT,' + \
								'DSTIP, DSTPORT, INFO, COMMENT)' + \
								'VALUES(?,?,?,?,?,?,?,?,?);', row)

		else:

			unhandled = open('unhandled.log', 'rw+')
			unhandled.write(row)
			unhandled.close
			
end = time()
print("FINAL TIME: " + str(end - start))

cursor.close()
print("Import to SQLite is over")

