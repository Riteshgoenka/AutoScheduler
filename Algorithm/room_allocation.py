from generate_room_list import room_list
from csp import slot_courses,course_numstudents

room_status={}
course_rooms={}
aval_rooms={}

for slot in slot_courses:
	available_rooms=[]
	room_capacity={}
	course_num=dict(course_numstudents)
	sorted_room_list = sorted(room_list, key=lambda x: int(room_list[x]))

	for room in sorted_room_list:
		room_capacity[room]=int(room_list[room])/2
		available_rooms.append(room)
		room_status[room]=2

	for course in slot_courses[slot]:
		aval_rooms[course]=list(available_rooms)
		course_rooms[course]=[]
		while (course_num[course] > 0):
			r=aval_rooms[course][len(aval_rooms[course])-1]
			if(room_capacity[r] < course_num[course]):
				if(room_status[r]==1):
					available_rooms.remove(r)
				else:
					room_status[r]-=1
				aval_rooms[course].remove(r)
				course_num[course]-=room_capacity[r]
				course_rooms[course].append(r)
			else:
				for room in available_rooms:
					if(room_capacity[room] >= course_num[course]):
						if(room_status[room]==1):
							available_rooms.remove(room)
						else:
							room_status[room]-=1
						aval_rooms[course].remove(room)
						course_num[course]=0
						course_rooms[course].append(room)
						break

print(course_rooms)