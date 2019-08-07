f = open("course_students.txt", "r")
course_list={}

for line in f:
	line1=line.rstrip(",")
	cols=line1.split(",")
	try:
		cols.remove('\n')
	except:
		pass
	course_list[cols[0]]=cols[1:]