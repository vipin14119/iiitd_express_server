from django.contrib import admin
from .models import Course, CourseSlot, UserCourses, User

admin.site.register(Course)
admin.site.register(CourseSlot)
admin.site.register(User)
admin.site.register(UserCourses)
# Register your models here.
