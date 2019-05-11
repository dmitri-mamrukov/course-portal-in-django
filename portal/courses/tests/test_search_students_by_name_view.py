from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Student
from ..serializers import StudentSerializer


client = Client()

def _clean_up_db():
    Student.objects.all().delete()

def _create_students():
    student1 = Student.objects.create(first_name='John',
                                      last_name='Green',
                                      email_address='student-email-address1')
    student2 = Student.objects.create(first_name='Alice',
                                      last_name='Johnson',
                                      email_address='student-email-address2')
    student3 = Student.objects.create(first_name='Tim',
                                      last_name='Stevenson',
                                      email_address='student-email-address3')
    student4 = Student.objects.create(first_name='Sonny',
                                      last_name='Sullivan',
                                      email_address='student-email-address4')
    student5 = Student.objects.create(first_name='Bill',
                                      last_name='Thompson',
                                      email_address='student-email-address5')

    return (student1, student2, student3, student4, student5)


class SearchStudentsByNameTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _assert_response(self, name, expected_results):
        serializer = StudentSerializer(expected_results, many=True)

        response = client.get(reverse('get_students_by_name',
                                      kwargs={'name': name}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_students_from_empty_db(self):
        students = Student.objects.all()
        self.assertEqual(0, len(students))

        self._assert_response('something', [])

    def test_get_students_from_populated_db(self):
        (student1, student2, student3, student4, student5) = _create_students()

        self._assert_response('john', [student1, student2])
        self._assert_response('son', [student2, student3, student4, student5])
        self._assert_response('python', [])
