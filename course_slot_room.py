from room_allocation import course_rooms
from csp import course_slot
from generate_course_list import course_list

for course in course_list:
	s=''
	for room in course_rooms[course]:
		s+=room
		s+=' '
	if(course_rooms[course]!=[]):
		print(course+','+str(course_slot[course])+','+s)
	