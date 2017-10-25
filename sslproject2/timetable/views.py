from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student, Professor, Course
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def index(request):
	#return render(request, 'timetable/index.html')
	return render(request, 'timetable/login.html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			X=Student.objects.filter(roll_no=username)
			if X:
				linked_courses = [l for l in Student.objects.filter(roll_no=username)[0].courses.all()]
				return render(request, 'timetable/display.html', {'context': linked_courses})
			else:
				linked_courses = [l for l in Professor.objects.filter(Prof_id=username)[0].courses.all()]
				return render(request, 'timetable/displayp.html', {'context': linked_courses})
		else:
			return render(request, 'timetable/login.html', {'error_message': 'Invalid login'})

		#Student.objects.all().delete()
		#Professor.objects.all().delete()
		#Course.objects.all().delete()
		# csvfile = request.FILES['file1']
		# file_data = csvfile.read().decode("utf-8")
		# f1 = file_data.split("\n")
		# for line in f1:
		# 	cols=line.split(",")
		# 	temp=Course(course_id=cols[0],slot=cols[1],rooms=cols[2])
		# 	temp.save()

		# csvfile = request.FILES['file2']
		# file_data = csvfile.read().decode("utf-8")
		# f2 = file_data.split("\n")

		# for line in f2:
		# 	line_without_newline=line.rstrip()
		# 	cols=line_without_newline.split(",")
		# 	temp=Student(roll_no=cols[0])
		# 	temp.save()
		# 	for course in cols[1:]:
		# 		x=Course.objects.filter(course_id=course)
		# 		if x:
		# 			temp.courses.add(x[0])

		# csvfile = request.FILES['file3']
		# file_data = csvfile.read().decode("utf-8")
		# f3 = file_data.split("\n")

		# for line in f3:
		# 	line_without_newline=line.rstrip()
		# 	cols=line_without_newline.split(",")
		# 	temp=Professor(Prof_id=cols[0])
		# 	temp.save()
		# 	for course in cols[1:]:
		# 		x=Course.objects.filter(course_id=course)
		# 		if x:
		# 			temp.courses.add(x[0])

		# x = Student.objects.all()
		# for y in x:
		# 	s = y.roll_no
		# 	e = s + '@iitb.ac.in'
		# 	p = s + 'pass'
		# 	check = User.objects.filter(username=s)
		# 	if not check:
		# 		user = User.objects.create_user(username=s,email=e,password=p)
		# 		user.save()
		# x = Professor.objects.all()
		# for y in x:
		# 	s = y.Prof_id
		# 	e = s + '@iitb.ac.in'
		# 	p = s + 'pass'
		# 	check = User.objects.filter(username=s)
		# 	if not check:
		# 		user = User.objects.create_user(username=s,email=e,password=p)
		# 		user.save()

	return render(request, 'timetable/login.html')

def logout_user(request):
	logout(request)
	return render(request, 'timetable/login.html')

def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			# messages.success(request, 'Your password was successfully updated!')
			return redirect('/timetable/password/')
		# else:
		# 	messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'timetable/change_password.html', {
		'form': form
	})