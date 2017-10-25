from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^timetable/', include('timetable.urls')),
    url(r'^', include('timetable.urls'))
]
