
def open_and_seek(file_name, line_number=0, slice=100000):

	f = open(file_name, "r")
	
	while True:
	
		if line_number >= slice:
			line_number -= slice
			
		else:
			f.read(slice - line_number)
			return f
			
	f.read(line_number)
	return f
			

with open_and_seek("logfile.log", 52001) as f:
	print(f.read())