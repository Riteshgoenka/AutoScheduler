from generate_course_list import course_list
from generate_student_list import student_list
from generate_room_list import room_list
from generate_prof_input_list import prof_input
import secrets
from random import shuffle
import math
import numpy

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

##
#\brief Import variables from the files generating course_list, room_list, student_list. 
#\var total_capacity It is the maximum number of students that can take examination at once.
#\var course_list It is the course list

##
#\brief
# Here we attempt to get a random feasible solution(ie a solution which satisfies all hard  constraints).
#  \li \c That is we first randomly allot a course to to a slot.
#  \li \c Then we allot slots to courses in  similar fashion.
#  \li \c If we fail in this attempt we restart the loop and allot the course some other random slot.
# Note- Here we are considering that there exists finitely many solutions for the given number of slots. 

#Simulated Annealing constants

n=1
temperature = 30000
alpha = 0.99
t_limit = math.pow(10,-11)
iterator = 10
for room in room_list:
	total_capacity+=int(room_list[room])

## \brief Create a 2d array of the common students in the course1 and course2 

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

val = 0
while(not val):
	try:
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
				elif(slot_numstudents[s]+course_numstudents[course]>0.8*total_capacity):
					try:
						available_slots[course].remove(s)
					except:
						pass
		val = 1
	except:
		pass

def consequtive_exams():
	## \var sum Stores the penalty incurred
	# \brief  Takes into account the student is not overloaded with exams on a particular day.
	# \return This returns the total penalty incurred if exams of the student are clustered. 
	total = {}
	sum=0
	for i in list(range(1,slots_per_day)):
		total[i-1]=0
	for s in list(range(1,slots_per_day)):
		for i in list(range(1,slots_per_day)):
			for c1 in slot_courses[s]:
					for c2 in slot_courses[s+i]:
						if((s-1)%slots_per_day < slots_per_day-i):
							total[i-1] += common_students[c1][c2]
	for i in list(range(0,slots_per_day-1)):
		sum+=(slots_per_day-i)*total[i]
	return sum

def prof_preference():
	total = 0
	for c in prof_input:
		if course_slot[c] in prof_input[c]:
			total += 1
	return total

def calc_score():
	## \var result total penalty
	# \return This returns the total penalty Due to Constraints 
	result = (5*consequtive_exams()+25*prof_preference())*n
	return result

count_t = 0

## STEP ANHEALING
#\brief Here we generate neighbourhood solutions and try to get to to the most optimized solution by iterating over solutions.

while(temperature > t_limit):
	for i in list(range(0,iterator)):
		c=secrets.choice(courses_copy)
		s=course_slot[c]
		slot_list=list(range(1,total_slots+1))
		shuffle(slot_list)
		for snew in slot_list:
			val=1
			if(s!=snew):
				for course in slot_courses[snew]:
					if(common_students[course][c]>0):
						val=0
						break
				if(slot_numstudents[snew]+course_numstudents[c]>0.8*total_capacity):
					val=0
				if(val==1):
					count_t += 1
					o_x = calc_score()
					slot_courses[s].remove(c)
					course_slot[c]=snew
					slot_courses[snew].append(c)
					o_q = calc_score()
					var = o_x - o_q
					if (var < 0):
						prob = math.exp(var/temperature)
						rand = numpy.random.choice([0,1], p=[prob, 1-prob])
						if(rand == 1):
							slot_courses[snew].remove(c)
							course_slot[c]=s
							slot_courses[s].append(c)
					break
	temperature *= alpha

## Hill Climbing
# \brief In approximately 5-10% of cases, the simulated annealing algorithm had not sufficiently explored the neighbourhood of its best solution.

iterate = 0
while(iterate < 1000):
	for i in list(range(0,iterator)):
		c=secrets.choice(courses_copy)
		s=course_slot[c]
		slot_list=list(range(1,total_slots+1))
		shuffle(slot_list)
		for snew in slot_list:
			val=1
			if(s!=snew):
				for course in slot_courses[snew]:
					if(common_students[course][c]>0):
						val=0
						break
				if(slot_numstudents[snew]+course_numstudents[c]>0.8*total_capacity):
					val=0
				if(val==1):
					o_x = calc_score()
					slot_courses[s].remove(c)
					course_slot[c]=snew
					slot_courses[snew].append(c)
					o_q = calc_score()
					var = o_x - o_q
					if (var > 0):
						iterate=0
					else:
						iterate+=1
						slot_courses[snew].remove(c)
						course_slot[c]=s
						slot_courses[s].append(c)
					break