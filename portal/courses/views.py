from datetime import date, datetime
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Course, Enrollment, Student, Teacher
from .serializers import CourseSerializer, StudentSerializer, TeacherSerializer
from .serializers import EnrollmentSerializer


def _get_course_data(request):
    raw_start_date = request.data.get('start_date')
    start_date = raw_start_date.replace('"', '')
    data = {
        'title': request.data.get('title'),
        'teacher': request.data.get('teacher'),
        'start_date': start_date,
    }

    return data

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_delete_update_student(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        student.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_post_students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email_address': request.data.get('email_address'),
        }
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_delete_update_teacher(request, pk):
    try:
        teacher = Teacher.objects.get(pk=pk)
    except Teacher.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeacherSerializer(teacher)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        teacher.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = StudentSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_post_teachers(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email_address': request.data.get('email_address'),
        }
        serializer = TeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_delete_update_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        course.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        data = _get_course_data(request)
        serializer = CourseSerializer(course, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_post_courses(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        data = _get_course_data(request)
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_delete_update_enrollment(request, pk):
    try:
        enrollment = Enrollment.objects.get(pk=pk)
    except Enrollment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EnrollmentSerializer(enrollment)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        enrollment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = EnrollmentSerializer(enrollment, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_post_enrollments(request):
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        data = {
            'course': request.data.get('course'),
            'student': request.data.get('student'),
            'grade': request.data.get('grade'),
        }
        serializer = EnrollmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_students_in_course(request, pk):
    if request.method == 'GET':
        course_enrollments = Enrollment.objects.filter(course=pk)
        students = [Student.objects.get(pk=x.student.pk)
                    for x in course_enrollments]
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_courses_taken_by_student(request, pk):
    if request.method == 'GET':
        student_enrollments = Enrollment.objects.filter(student=pk)
        courses = [Course.objects.get(pk=x.course.pk)
                   for x in student_enrollments]
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_courses_by_title(request, title):
    if request.method == 'GET':
        courses = Course.objects.filter(title__icontains=title)
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_courses_by_start_date(request, date):
    if request.method == 'GET':
        start_datetime = datetime.strptime(date, '%Y-%m-%d')
        courses = Course.objects.filter(start_date=start_datetime.date())
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticatedOrReadOnly, ))
def get_students_by_name(request, name):
    if request.method == 'GET':
        students = Student.objects.filter(Q(first_name__icontains=name) |
                                          Q(last_name__icontains=name))
        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data)
