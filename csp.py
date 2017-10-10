from generate_course_list import course_list
from generate_student_list import student_list
from generate_room_list import room_list
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

prof_input = {}

n = 1   # (Experimental constant, to be varied to check best solution)
weight = [100*n , 100*n , 25*n]

#Simulated Annealing constants
temperature = 30000
alpha = 0.599
t_limit = math.pow(10,-11)
iterator = 10

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
				elif(slot_numstudents[s]+course_numstudents[course]>total_capacity):
					try:
						available_slots[course].remove(s)
					except:
						pass
		val = 1
	except:
		pass

print(slot_courses)

def consequtive_exams():
	total = 0
	for s in list(range(1,total_slots+1)):
		if(s%slots_per_day != 0):
			for c1 in slot_courses[s]:
				for c2 in slot_courses[s+1]:
					total += common_students[c1][c2]
	return total

def day(num):
	return math.ceil(num/slots_per_day)
def comb(x,y):
	return math.factorial(x)/(math.factorial(y)*math.factorial(x-y))
def daily_exam_limit():
	student_slot_list = {}
	for student in student_list:
		try:
			for c in student_list[student]:
				try:
					student_slot_list[student].append(course_slot[c])
				except:
					student_slot_list[student] = []
					student_slot_list[student].append(course_slot[c])
		except:
			pass
	total = 0
	for student in student_list:
		if (len(student_list[student])!=0):
			util = list(map(day, student_slot_list[student]))
			for d in list(range(1,days+1)):
				exam_count=util.count(d)
				if (exam_count > 2):
					total += comb(exam_count,3)
	return total

def prof_preference():
	total = 0
	for c in prof_input:
		if course_slot[c] in prof_input[c]:       # (prof_input) needs to be defined #
			continue
		else:
			total += 1
	return total

def calc_score():
	result = (100*consequtive_exams()+100*daily_exam_limit()+25*prof_preference())*n
	return result

count_t = 0
print (calc_score())
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
				if(slot_numstudents[snew]+course_numstudents[c]>total_capacity):
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

print(slot_courses)
print (calc_score())
print (count_t)