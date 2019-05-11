from django.test import TestCase
from ..models import Student


class StudentModelTests(TestCase):

    def tearDown(self):
        Student.objects.all().delete()

    def test_student_creation(self):
        student = Student.objects.create(first_name='First',
                                         last_name='Last',
                                         email_address='email-address')

        self.assertEqual('First', student.first_name)
        self.assertEqual('Last', student.last_name)
        self.assertEqual('email-address', student.email_address)
