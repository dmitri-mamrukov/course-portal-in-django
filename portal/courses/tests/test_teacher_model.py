from django.test import TestCase
from ..models import Teacher


class TeacherTeacherTests(TestCase):

    def tearDown(self):
        Teacher.objects.all().delete()

    def test_teacher_creation(self):
        teacher = Teacher.objects.create(first_name='First',
                                         last_name='Last',
                                         email_address='email-address')

        self.assertEqual('First', teacher.first_name)
        self.assertEqual('Last', teacher.last_name)
        self.assertEqual('email-address', teacher.email_address)
