from django.contrib import admin

from .models import Course, Enrollment, Student, Teacher

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Enrollment)
