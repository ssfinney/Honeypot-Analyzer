import sqlite3


# Connect to the database file: log.sqlite
mydb = sqlite3.connect('log.sqlite')
cursor = mydb.cursor()

# Use this code to remove the table(s) for the database
#cursor.execute("DROP TABLE ICMP;")
#cursor.execute("DROP TABLE TCP;")
#cursor.execute("DROP TABLE UDP;")

#cursor.execute('CREATE TABLE ICMP' + \
#					'(DATE string, PROTOCOL string, CONNECTION varchar(1), ' + \
#					'SRCIP string, DSTIP string, INFO string, COMMENT string);')

#cursor.execute('CREATE TABLE TCP' + \
#					'(DATE string, PROTOCOL string, CONNECTION varchar(1), ' + \
#					'SRCIP string, SRCPORT string, DSTIP string, ' + \
#					'DSTPORT string, INFO string, COMMENT string);')

#cursor.execute('CREATE TABLE UDP' + \
#					'(DATE string, PROTOCOL string, CONNECTION varchar(1), ' + \
#					'SRCIP string, SRCPORT string, DSTIP string, ' + \
#					'DSTPORT string, INFO string, COMMENT string);')
					
cursor.execute('Create Table Log' + \
			   '(Date string, Time string, Protocol string,'+\
			   'Connection string, Source_IP string, Source_Port string,'+\
			   'Dest_IP string, Dest_Port string, Info string,'+\
			   'Environment string);')

cursor.close()
print("Database initialized.")
