from django.contrib import admin
from .models import Course, CourseSlot, UserCourses, User, Faculty, People

admin.site.register(Course)
admin.site.register(CourseSlot)
admin.site.register(User)
admin.site.register(UserCourses)
admin.site.register(Faculty)
admin.site.register(People)
# Register your models here.
