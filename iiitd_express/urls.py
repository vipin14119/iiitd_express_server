"""iiitd_express URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from main.views import (get_faculty_json, get_visiting_faculty_json, get_mess_menu,
get_my_courses, get_course_slots, get_day_courses, add_course, get_all_courses, get_courses, remove_course,
get_directory_json, register_user)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_faculty_json', get_faculty_json, name='get_faculty_json'),
    url(r'^get_visiting_faculty_json', get_visiting_faculty_json, name='get_visiting_faculty_json'),
    url(r'^get_mess_menu', get_mess_menu, name='get_mess_menu'),
    url(r'^get_my_courses', get_my_courses, name='get_my_courses'),
    url(r'^get_course_slots', get_course_slots, name='get_course_slots'),
    url(r'^get_day_courses', get_day_courses, name='get_day_courses'),
    url(r'^get_all_courses', get_courses, name='get_all_courses'),
    url(r'^add_course', add_course, name='add_course'),
    url(r'^remove_course', remove_course, name='remove_course'),
    url(r'^get_directory_json', get_directory_json, name='get_directory_json'),
    url(r'^register_user', register_user, name='register_user'),
]
