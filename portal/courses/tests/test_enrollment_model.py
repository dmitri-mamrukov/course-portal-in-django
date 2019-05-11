from datetime import date
from django.test import TestCase
from ..models import Course, Enrollment, Student, Teacher


class EnrollmentModelTests(TestCase):

    def tearDown(self):
        Course.objects.all().delete()
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Enrollment.objects.all().delete()

    def test_enrollment_creation(self):
        student = Student.objects.create(first_name='First',
                                         last_name='Last',
                                         email_address='student-email-address')
        teacher = Teacher.objects.create(first_name='First',
                                         last_name='Last',
                                         email_address='teacher-email-address')
        start_date = date(2018, 9, 1)
        course = Course.objects.create(title='Title',
                                       teacher=teacher,
                                       start_date=start_date)

        enrollment = Enrollment.objects.create(course=course,
                                               student=student,
                                               grade=None)

        self.assertEqual(course, enrollment.course)
        self.assertEqual(student, enrollment.student)
        self.assertIsNone(enrollment.grade)
