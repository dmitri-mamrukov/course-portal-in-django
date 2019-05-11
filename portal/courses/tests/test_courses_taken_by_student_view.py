from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Course, Enrollment, Student, Teacher
from ..serializers import CourseSerializer, StudentSerializer


client = Client()

def _clean_up_db():
    Course.objects.all().delete()
    Teacher.objects.all().delete()
    Student.objects.all().delete()
    Enrollment.objects.all().delete()

def _create_students():
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
    course3 = Course.objects.create(title='Title3',
                                    teacher=teacher1,
                                    start_date=date(2018, 11, 1))
    course4 = Course.objects.create(title='Title4',
                                    teacher=teacher2,
                                    start_date=date(2018, 12, 1))
    course5 = Course.objects.create(title='Title5',
                                    teacher=teacher1,
                                    start_date=date(2019, 1, 1))
    Enrollment.objects.create(course=course1,
                              student=student1,
                              grade='A')
    Enrollment.objects.create(course=course2,
                              student=student1,
                              grade='A')
    Enrollment.objects.create(course=course2,
                              student=student2,
                              grade='B')
    Enrollment.objects.create(course=course3,
                              student=student1,
                              grade='A')
    Enrollment.objects.create(course=course3,
                              student=student2,
                              grade='B')
    Enrollment.objects.create(course=course3,
                              student=student3,
                              grade='C')
    Enrollment.objects.create(course=course4,
                              student=student1,
                              grade='A')
    Enrollment.objects.create(course=course4,
                              student=student2,
                              grade='B')
    Enrollment.objects.create(course=course4,
                              student=student3,
                              grade='C')
    Enrollment.objects.create(course=course4,
                              student=student4,
                              grade='D')

    return (student1, student2, student3, student4, student5,
            course1, course2, course3, course4, course5)


class GetCoursesTakeByStudentTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _assert_response(self, student_pk, expected_results):
        serializer = CourseSerializer(expected_results, many=True)

        response = client.get(reverse('get_courses_taken_by_student',
                                      kwargs={'pk': student_pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_courses_from_empty_db(self):
        enrollments = Enrollment.objects.all()
        self.assertEqual(0, len(enrollments))

        self._assert_response(1234567890, [])

    def test_get_enrolled_students_from_populated_db(self):
        (student1, student2, student3, student4, student5,
         course1, course2, course3, course4, _) = _create_students()
        student1_courses = [course1, course2, course3, course4]
        student2_courses = [course2, course3, course4]
        student3_courses = [course3, course4]
        student4_courses = [course4]
        student5_courses = []

        self._assert_response(student1.pk, student1_courses)
        self._assert_response(student2.pk, student2_courses)
        self._assert_response(student3.pk, student3_courses)
        self._assert_response(student4.pk, student4_courses)
        self._assert_response(student5.pk, student5_courses)
