from rest_framework import serializers
from .models import Course, Enrollment, Student, Teacher


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('first_name',
                  'last_name',
                  'email_address',
                  'created_at',
                  'updated_at')


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ('first_name',
                  'last_name',
                  'email_address',
                  'created_at',
                  'updated_at')


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('title',
                  'teacher',
                  'start_date',
                  'created_at',
                  'updated_at')



class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = ('course',
                  'student',
                  'grade',
                  'created_at',
                  'updated_at')
