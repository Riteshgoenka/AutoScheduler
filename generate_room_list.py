f = open("room_capacity.txt", "r")
room_list={}

for line in f:
	line_without_newline=line.rstrip()
	cols=line_without_newline.split(",")
	room_list[cols[0]]=cols[1]