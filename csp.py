from generate_course_list import course_list
from generate_student_list import student_list
from generate_room_list import room_list
import secrets

total_capacity=0
slots_per_day=4
days=6
total_slots=days*slots_per_day

course_numstudents={}
courses=[]
common_students={}
available_slots={}
course_slot={}
slot_courses={}
slot_numstudents={}

for room in room_list:
	total_capacity+=int(room_list[room])

for course in course_list:
	c=course_list[course]
	courses.append(course)
	course_numstudents[course]=len(c)
	common_students[course]={}
	for course2 in course_list:
		common_students[course][course2]=len(set(course_list[course2]).intersection(c))

for course in courses:
	available_slots[course]=list(range(1,total_slots+1))

courses_copy=list(courses)

for i in list(range(1,total_slots+1)):
	slot_numstudents[i]=0
	slot_courses[i]=[]

for i in list(range(0,len(course_list))):
	minslots=total_slots
	minlist=[]
	for course in courses:
		num_aval_slots=len(available_slots[course])
		if(num_aval_slots<minslots):
			minslots=num_aval_slots
			minlist=[]
			minlist.append(course)
		elif(num_aval_slots==minslots):
			minlist.append(course)
	c=secrets.choice(minlist)
	s=secrets.choice(available_slots[c])
	slot_numstudents[s]+=course_numstudents[c]
	course_slot[c]=s
	slot_courses[s].append(c)
	courses.remove(c)
	for course in courses:
		if(common_students[c][course]>0):
			try:
				available_slots[course].remove(s)
			except:
				pass
		elif(slot_numstudents[s]+course_numstudents[course]>total_capacity):
			try:
				available_slots[course].remove(s)
			except:
				pass

c=secrets.choice(courses_copy)
s=course_slot[c]
available_slots[c]=[]
for snew in list(range(1,total_slots+1)):
	val=1
	if(s!=snew):
		for course in slot_courses[snew]:
			if(common_students[course][c]>0):
				val=0
				break
		if(slot_numstudents[snew]+course_numstudents[c]>total_capacity):
			val=0
		if(val==1):
			available_slots[c].append(snew)

if available_slots[c]:
	snew=secrets.choice(available_slots[c])

print(slot_courses)