from django.shortcuts import render
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import json
import urllib
import os

from django.core import serializers
from .models import Course, CourseSlot, UserCourses, User, Faculty, People, User

from iiitd_express.settings import BASE_DIR


faculty = "https://www.iiitd.ac.in/people/faculty"
visiting_faculty = "https://www.iiitd.ac.in/people/visiting-faculty"
adminstration = "https://www.iiitd.ac.in/people/administration"

@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print data
        username = data['username']
        password = data['password']
        if(len(User.objects.filter(username=username)) > 0):
            user = User.objects.filter(username=username, password=password)[0]
            json_dict = {
                'username': user.username,
                'password': user.password
            }
            return JsonResponse({'code': 2, 'data': json_dict})
        else:
            user = User(username=username, password=password)
            user.save()
            json_dict = {
                'username': user.username,
                'password': user.password
            }
            return JsonResponse({'code': 1, 'data': json_dict})



@csrf_exempt
def get_faculty_json_from_link(request):
    faculty = "https://www.iiitd.ac.in/people/faculty"
    f = urllib.urlopen(faculty)
    soup = BeautifulSoup(f.read(), 'html.parser')

    faculty_names = []
    faculty_links = []
    faculty_designation = []
    faculty_education = []
    faculty_interest = []

    for data in soup.find_all('div', class_='card rteleft facultycard'):
        split = []
        count = 0
        for a in data.find_all('a'):
            if(a.text != ''):
                personal_link = "https://iiitd.ac.in"+a.get("href")
                faculty_links.append(personal_link)
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
        faculty = Faculty(name=faculty_names[i], designation=faculty_designation[i],education= faculty_education[i], interest=faculty_interest[i], link=faculty_links[i])
        faculty.save()
        obj = {
            'name': faculty_names[i],
            'designation': faculty_designation[i],
            'education': faculty_education[i],
            'interest': faculty_interest[i],
            'link': faculty_links[i]
        }
        json_dict.append(obj)

    return JsonResponse(json_dict, safe=False)

@csrf_exempt
def get_faculty_json(request):
    faculties = Faculty.objects.all()
    json_dict = []
    for faculty in faculties:
        obj = {
            'name': faculty.name,
            'designation': faculty.designation,
            'education': faculty.education,
            'interest': faculty.interest,
            'link': faculty.link,
            'email': faculty.email,
            'website': faculty.website
        }
        # url = urllib.urlopen(faculty.link)
        # soup = BeautifulSoup(url.read(), 'html.parser')
        # div =  soup.find_all('div', class_='field field-name-field-contact field-type-text-long field-label-above')[0]
        # atags = div.find_all('a')
        # email = "NA"
        # website = "NA"
        # try:
        #     email = atags[0].text
        # except:
        #     continue
        # try:
        #     website = atags[1].text
        # except:
        #     continue
        # faculty.email = email
        # faculty.website = website
        # faculty.save()
        # print email
        # print website
        json_dict.append(obj)
    return JsonResponse({'code': 1, 'data': json_dict})

@csrf_exempt
def get_directory_json(request):

    types = ['acad', 'fms', 'serv']
    final_dict = {}
    for type in types:
        peoples = People.objects.filter(type=type)
        json_dict = []
        for people in peoples:
            obj = {
                'name': people.name,
                'designation': people.designation,
                'room': people.room,
                'email': people.email
            }
            json_dict.append(obj)
        final_dict[type] = json_dict

    return JsonResponse({'code': 1, 'data': final_dict})


def get_academic_link_json():
    acad_link = "http://iiitd.ac.in/people/administration"
    url = urllib.urlopen(acad_link)
    soup = BeautifulSoup(url.read(), 'html.parser')
    divs = soup.findAll('div', attrs={'id': 'cards-container'})[-2:]
    print divs
    for div in divs:
        for card in div.find_all('div', class_='card rteleft'):
            name = card.find('strong').text
            fields = card.find('p').text.split("\n")
            people = People(name=name, designation=fields[0], room=fields[1], email=fields[2])
            people.save()
            print people


    # atags = div.find_all('a')
    # email = "NA"
    # website = "NA"
    # try:
    #     email = atags[0].text
    # except:
    #     continue
    # try:
    #     website = atags[1].text
    # except:
    #     continue
    # faculty.email = email
    # faculty.website = website
    # faculty.save()
    # print email
    # print website

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


@csrf_exempt
def get_my_courses(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username=username)

            usercourses = map(lambda x: x.course, UserCourses.objects.filter(user=user))

            json_data = []
            for course in usercourses:
                slots = course.courseslot_set.all()
                slots_json = []
                for slot in slots:
                    slots_json.append({
                        "id": slot.id,
                        "room": slot.room,
                        "start_time": slot.start_time,
                        "end_time": slot.end_time,
                        "day": slot.day
                    })
                json_data.append({
                    "id": course.id,
                    "code": course.code,
                    "name": course.name,
                    "slots": slots_json
                })
            return  JsonResponse({'code': 1, 'data': json_data})
        except:
            return JsonResponse({'code': -1, 'data': []})


@csrf_exempt
def get_courses(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = User.objects.get(username=username)

        all_courses = Course.objects.all()
        usercourses = map(lambda x: x.course, UserCourses.objects.filter(user=user))
        not_selected_courses = list(set(all_courses) - set(usercourses))

        json_data = []
        for course in usercourses:
            slots = course.courseslot_set.all()
            slots_json = []
            for slot in slots:
                slots_json.append({
                    "id": slot.id,
                    "room": slot.room,
                    "start_time": slot.start_time,
                    "end_time": slot.end_time,
                    "day": slot.day
                })
            json_data.append({
                "id": course.id,
                "code": course.code,
                "name": course.name,
                "slots": slots_json,
                "added": 1
            })
        for course in not_selected_courses:
            slots = course.courseslot_set.all()
            slots_json = []
            for slot in slots:
                slots_json.append({
                    "id": slot.id,
                    "room": slot.room,
                    "start_time": slot.start_time,
                    "end_time": slot.end_time,
                    "day": slot.day
                })
            json_data.append({
                "id": course.id,
                "code": course.code,
                "name": course.name,
                "slots": slots_json,
                "added": 0
            })
        return  JsonResponse({'code': 1, 'data': json_data})
        # try:

        # except:
        #     return JsonResponse({'code': -1, 'data': []})

def get_all_courses(request):
    all_courses = Course.objects.all()
    json_data = []
    for course in all_courses:
        slots = course.courseslot_set.all()
        slots_json = []
        for slot in slots:
            slots_json.append({
                "id": slot.id,
                "room": slot.room,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "day": slot.day
            })
        json_data.append({
            "id": course.id,
            "code": course.code,
            "name": course.name,
            "slots": slots_json
        })

    return  JsonResponse({'code': 1, 'data': json_data})

@csrf_exempt
def add_course(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        code = data['code']
        print "Adding Code : "+ code
        user = User.objects.get(username=username)
        course = Course.objects.get(code=code)

        if len(UserCourses.objects.filter(user=user, course=course)) < 1:
            user_course = UserCourses(user=user, course=course)
            user_course.save()
            return JsonResponse({"code": 1, "data": "Course has been added succesfully"})
        else:
            return JsonResponse({"code": 1, "data": "Course had been already added before"})


@csrf_exempt
def remove_course(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        code = data['code']
        print "Removing Code : "+ code
        user = User.objects.get(username=username)
        course = Course.objects.get(code=code)

        if len(UserCourses.objects.filter(user=user, course=course)) > 0:
            usercourse = UserCourses.objects.get(user=user, course=course)
            usercourse.delete()
            return JsonResponse({"code": 1, "data": "Course has been deleted succesfully"})
        else:
            return JsonResponse({"code": 1, "data": "No Such course added to remove"})


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
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        day = data['day'].upper()

        user = User.objects.get(username=username)

        all_courses = Course.objects.all()
        usercourses = map(lambda x: x.course, UserCourses.objects.filter(user=user))
        slots = []

        for course in usercourses:
            course_slots = course.courseslot_set.all()
            for slot in course_slots:
                slots.append(slot)

        final_slots = []
        for slot in slots:
            if slot.day == day:
                final_slots.append(slot)
        # slots = CourseSlot.objects.filter(day=day)

        slots_json = []

        for slot in final_slots:
            slots_json.append({
                "id": slot.id,
                "course": slot.course.code,
                "name": slot.course.name,
                "room": slot.room,
                "start_time": slot.start_time,
                "end_time": slot.end_time,
                "day": slot.day
            })
        return  JsonResponse({'code': 1, 'data': slots_json})
