from django.conf.urls import url
from . import views

app_name = 'timetable'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^userlogin$', views.login_user, name='userlogin'),
	url(r'^userlogout$', views.logout_user, name='userlogout'),
	url(r'^password/$', views.change_password, name='password')
]