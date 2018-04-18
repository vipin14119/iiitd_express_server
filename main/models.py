from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=200, unique=True, null=False, blank=False)
    password = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.username


class Course(models.Model):
    code = models.CharField(max_length=30, unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=500)
    designation = models.CharField(max_length=2000)
    education = models.CharField(max_length=2000)
    interest = models.CharField(max_length=2000)
    link = models.CharField(max_length=2000)
    email = models.CharField(max_length=50)
    website = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class People(models.Model):
    TYPE_CHOICES = (
        ('acad', 'Academic'),
        ('fms', 'FMS'),
        ('serv', 'Services'),
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=200, blank=True, null=True)
    room = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='acad')

    def __str__(self):
        return self.name

class CourseSlot(models.Model):

    DAY_CHOICES = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    room = models.CharField(max_length=20, blank=False)
    start_time = models.CharField(max_length=100, blank=False)
    end_time = models.CharField(max_length=100, blank=False)
    day = models.CharField(max_length=3, choices=DAY_CHOICES)

    def __str__(self):
        return str(self.course.name) + " -> " + str(self.day)

class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username) + " -- " + str(self.course.name)
