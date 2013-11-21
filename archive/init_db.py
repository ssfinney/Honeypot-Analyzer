import sqlite3


# Connect to the database file: log.sqlite
mydb = sqlite3.connect('log.sqlite')
cursor = mydb.cursor()

# Use this code to remove the table(s) for the database
#cursor.execute("DROP TABLE Log;")

					
cursor.execute('Create Table Log' + \
			   '(Date string, Time string, Protocol string,'+\
			   'Connection string, Source_IP string, Source_Port string,'+\
			   'Dest_IP string, Dest_Port string, Info string,'+\
			   'Environment string);')

mydb.commit()
cursor.close()
print("Database initialized.")
