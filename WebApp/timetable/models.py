from django.contrib.auth.models import Permission, User
from django.db import models

class Course(models.Model):
	course_id = models.CharField(max_length=10)
	slot = models.CharField(max_length=10)
	rooms = models.CharField(max_length=50)

	def __str__(self):
		return self.course_id

class Student(models.Model):
	roll_no = models.CharField(max_length=10)
	courses = models.ManyToManyField(Course)

	def __str__(self): 
		return self.roll_no

class Professor(models.Model):
	Prof_id = models.CharField(max_length=10)
	courses = models.ManyToManyField(Course)

	def __str__(self): 
		return self.Prof_id
