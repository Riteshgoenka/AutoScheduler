f = open("prof_preferences.txt", "r")
prof_input={}

for line in f:
	line_without_newline=line.rstrip()
	cols=line_without_newline.split(",")
	prof_input[cols[0]]=cols[1:]