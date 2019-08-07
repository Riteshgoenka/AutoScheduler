f = open("student_courses.txt", "r")
student_list={}

for line in f:
	line_without_newline=line.rstrip()
	cols=line_without_newline.split(",")
	student_list[cols[0]]=cols[1:]