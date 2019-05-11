from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Course, Enrollment, Student, Teacher
from ..serializers import StudentSerializer


client = Client()

def _clean_up_db():
    Course.objects.all().delete()
    Teacher.objects.all().delete()
    Student.objects.all().delete()
    Enrollment.objects.all().delete()

def _create_courses_with_enrollments():
    student1 = Student.objects.create(first_name='StudentFirst1',
                                      last_name='StudentLast1',
                                      email_address='student-email-address1')
    student2 = Student.objects.create(first_name='StudentFirst2',
                                      last_name='StudentLast2',
                                      email_address='student-email-address2')
    student3 = Student.objects.create(first_name='StudentFirst3',
                                      last_name='StudentLast3',
                                      email_address='student-email-address3')
    student4 = Student.objects.create(first_name='StudentFirst4',
                                      last_name='StudentLast4',
                                      email_address='student-email-address4')
    student5 = Student.objects.create(first_name='StudentFirst5',
                                      last_name='StudentLast5',
                                      email_address='student-email-address5')
    teacher1 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    teacher2 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    course1 = Course.objects.create(title='Title1',
                                    teacher=teacher1,
                                    start_date=date(2018, 9, 1))
    course2 = Course.objects.create(title='Title2',
                                    teacher=teacher2,
                                    start_date=date(2018, 10, 1))
    Enrollment.objects.create(course=course1,
                              student=student1,
                              grade='A')
    Enrollment.objects.create(course=course1,
                              student=student2,
                              grade='B')
    Enrollment.objects.create(course=course1,
                              student=student3,
                              grade='C')
    Enrollment.objects.create(course=course2,
                              student=student4,
                              grade='A')
    Enrollment.objects.create(course=course2,
                              student=student5,
                              grade='B')

    return (course1, course2,
            student1, student2, student3, student4, student5)

def _create_courses_with_no_enrollments():
    teacher1 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    teacher2 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    course1 = Course.objects.create(title='Title1',
                                    teacher=teacher1,
                                    start_date=date(2018, 9, 1))
    course2 = Course.objects.create(title='Title2',
                                    teacher=teacher2,
                                    start_date=date(2018, 10, 1))

    return (course1, course2)


class GetStudentsInCourseTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _assert_response(self, course_pk, expected_results):
        serializer = StudentSerializer(expected_results, many=True)

        response = client.get(reverse('get_students_in_course',
                                      kwargs={'pk': course_pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_enrolled_students_from_empty_db(self):
        enrollments = Enrollment.objects.all()
        self.assertEqual(0, len(enrollments))

        self._assert_response(1234567890, [])

    def test_get_enrolled_students_from_populated_db(self):
        (course1, course2,
         student1, student2, student3, student4, student5) = \
            _create_courses_with_enrollments()
        course3, course4 = _create_courses_with_no_enrollments()
        course1_students = [student1, student2, student3]
        course2_students = [student4, student5]
        course3_students = []
        course4_students = []

        self._assert_response(course1.pk, course1_students)
        self._assert_response(course2.pk, course2_students)
        self._assert_response(course3.pk, course3_students)
        self._assert_response(course4.pk, course4_students)
