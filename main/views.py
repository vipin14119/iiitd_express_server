from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import json
import urllib
import os

from django.core import serializers
from .models import Course, CourseSlot, UserCourses, User

from iiitd_express.settings import BASE_DIR


faculty = "https://www.iiitd.ac.in/people/faculty"
visiting_faculty = "https://www.iiitd.ac.in/people/visiting-faculty"
adminstration = "https://www.iiitd.ac.in/people/administration"

@csrf_exempt
def get_faculty_json(request):
    faculty = "https://www.iiitd.ac.in/people/faculty"
    f = urllib.urlopen(faculty)
    soup = BeautifulSoup(f.read(), 'html.parser')

    faculty_names = []
    faculty_designation = []
    faculty_education = []
    faculty_interest = []

    for data in soup.find_all('div', class_='card rteleft facultycard'):
        split = []
        count = 0
        for a in data.find_all('a'):
            if(a.text != ''):
                faculty_names.append(a.text)
        for c in data.find_all('p'):
            if count == 0:
                faculty_designation.append(c.text)
            elif count == 1:
                faculty_education.append(c.text)
            elif count == 2:
                faculty_interest.append(c.text)
            else:
                break
            count += 1
    del(faculty_names[-1])
    for i in range(0, 14):
        faculty_education.pop()
        faculty_interest.pop()
        faculty_designation.pop()

    faculty_education[1] = "PhD in Contemporary India at King's College London"

    json_dict = []

    for i in range(len(faculty_names)):
        obj = {
            'name': faculty_names[i],
            'designation': faculty_designation[i],
            'education': faculty_education[i],
            'interest': faculty_interest[i]
        }
        json_dict.append(obj)

    return JsonResponse(json_dict, safe=False)



def get_visiting_faculty_json(request):
    if request.method == 'GET':
        visiting_faculty = "https://www.iiitd.ac.in/people/visiting-faculty"
    	vf = urllib.urlopen(visiting_faculty)
    	soup = BeautifulSoup(vf.read(), 'html.parser')

    	faculty_names = []
    	faculty_education = []
    	faculty_recognition = []

    	for data in soup.find_all('div', class_='card rteleft facultycard'):
    		split = []
    		count = 0
    		for a in data.find_all('strong'):
    			if(a.text != ''):
    				faculty_names.append(a.text)
    		for c in data.find_all('p'):
    			if count % 2 == 0:
    				faculty_recognition.append(c.text)
    			elif count % 2 == 1:
    				faculty_education.append(c.text)
    			else:
    				break
    			count += 1

    	output_recognition = []
    	for i in faculty_recognition:
    		if(i != ''):
    			output_recognition.append(i)

    	print len(faculty_names)
    	print len(faculty_education)
    	print len(output_recognition)


    	json_dict = []

        for i in range(len(faculty_names)):
            obj = {
                'name': faculty_names[i],
                'designation': faculty_recognition[i],
                'education': faculty_education[i],
            }
            json_dict.append(obj)

        return JsonResponse(json_dict, safe=False)


@csrf_exempt
def get_mess_menu(request):
    file_path = os.path.join(BASE_DIR, 'main')
    f_obj = open(os.path.join(file_path, 'breakfast.txt'), 'r')
    breakfast_lines = f_obj.readlines()
    f_obj.close()

    f_obj = open(os.path.join(file_path, 'lunch.txt'), 'r')
    lunch_lines = f_obj.readlines()
    f_obj.close()

    f_obj = open(os.path.join(file_path, 'snacks.txt'), 'r')
    snacks_lines = f_obj.readlines()
    f_obj.close()

    f_obj = open(os.path.join(file_path, 'dinner.txt'), 'r')
    dinner_lines = f_obj.readlines()
    f_obj.close()

    json_obj = {}
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i in range(len(days)):
        breakfast = breakfast_lines[i].split(',')
        lunch = lunch_lines[i].split(',')
        snack = snacks_lines[i].split(',')
        dinner = dinner_lines[i].split(',')
        for v in dinner[1:]:
            print 'DINNER_ITEMS.add(new MessItem("'+v+'"));'
        obj = {
            'breakfast': breakfast[1:],
            'lunch': lunch[1:],
            'snack': snack[1:],
            'dinner': dinner[1:],
        }
        json_obj[days[i]] =  obj


    return JsonResponse({'code': 1, 'data': json_obj})


def get_courses(request):
    all_courses = Course.objects.all()
    usercourses = map(lambda x: x.course, UserCourses.objects.filter(user__username='admin'))
    final_courses = [course for course in all_courses if course not in usercourses]
    print final_courses
    json_data = []
    for course in final_courses:
        json_data.append({
            "id": course.id,
            "code": course.code,
            "name": course.name
        })
    return  JsonResponse({'code': 1, 'data': json_data})


@csrf_exempt
def add_course(request):
    if request.method == "POST":
        code = json.loads(request.body)['code']
        user = User.objects.get(username="admin")
        course = Course.objects.get(code=code)

        if len(UserCourses.objects.filter(user=user, course=course)) < 1:
            user_course = UserCourses(user=user, course=course)
            user_course.save()
            return JsonResponse({"code": 1, "data": "Course has been added succesfully"})
        else:
            return JsonResponse({"code": 1, "data": "Course had been already added before"})


@csrf_exempt
def get_course_slots(request):
    if request.method == "POST":
        code = json.loads(request.body)['code']
        slots = CourseSlot.objects.filter(course__code=code)
        slots_json = []

        for slot in slots:
            slots_json.append({
                "id": slot.id,
                "room": slot.room,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "day": slot.day
            })
        return  JsonResponse({'code': 1, 'data': slots_json})


@csrf_exempt
def get_day_courses(request):
    if request.method == "POST":
        day = json.loads(request.body)['day'].upper()
        slots = CourseSlot.objects.filter(day=day)

        slots_json = []

        for slot in slots:
            slots_json.append({
                "id": slot.id,
                "course": slot.course.code,
                "room": slot.room,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "day": slot.day
            })
        return  JsonResponse({'code': 1, 'data': slots_json})