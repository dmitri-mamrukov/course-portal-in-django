from datetime import date
from django.test import TestCase
from ..models import Course, Teacher


class CourseModelTests(TestCase):

    def tearDown(self):
        Course.objects.all().delete()
        Teacher.objects.all().delete()

    def test_course_creation(self):
        teacher = Teacher.objects.create(first_name='First',
                                         last_name='Last',
                                         email_address='email-address')
        start_date = date(2018, 9, 1)

        course = Course.objects.create(title='Title',
                                       teacher=teacher,
                                       start_date=start_date)

        self.assertEqual('Title', course.title)
        self.assertEqual(teacher, course.teacher)
        self.assertEqual(start_date, course.start_date)
