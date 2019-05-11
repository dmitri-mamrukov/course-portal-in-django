from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APIClient
from .common import set_up_admin, clean_up_admin
from ..models import Student
from ..serializers import StudentSerializer


client = APIClient()

def _clean_up_db():
    Student.objects.all().delete()

def _create_two_students():
    student1 = Student.objects.create(first_name='First1',
                                      last_name='Last1',
                                      email_address='email-address1')
    student2 = Student.objects.create(first_name='First2',
                                      last_name='Last2',
                                      email_address='email-address2')

    return (student1, student2)


class GetAllStudentsTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _do_get(self):
        response = client.get(reverse('get_post_students'))

        return response

    def test_get_all_students_from_empty_db(self):
        students = Student.objects.all()
        self.assertEqual(0, len(students))
        serializer = StudentSerializer(students, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_students_from_populated_db(self):
        _create_two_students()
        students = Student.objects.all()
        self.assertEqual(2, len(students))
        serializer = StudentSerializer(students, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleStudentTest(TestCase):

    def setUp(self):
        self._student1, self._student2 = _create_two_students()

    def tearDown(self):
        _clean_up_db()

    def _do_get(self, student_pk):
        response = client.get(reverse('get_delete_update_student',
                                      kwargs={'pk': student_pk}))

        return response

    def test_get_student(self):
        student = Student.objects.get(pk=self._student1.pk)
        serializer = StudentSerializer(student)

        response = self._do_get(self._student1.pk)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_missing_student(self):
        response = self._do_get(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewStudentTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._valid_payload = {
            'first_name': 'First1',
            'last_name': 'Last1',
            'email_address': 'email-address1',
        }
        self._invalid_payload = {
            'first_name': '',
            'last_name': 'Last2',
            'email_address': 'email-address2',
        }

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_post(self, payload):
        response = client.post(reverse('get_post_students'),
                               data=json.dumps(payload),
                               content_type='application/json')

        return response

    def test_create_student_without_authentication(self):
        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_student(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_student_without_authentication(self):
        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invalid_student(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleStudentTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._student1, self._student2 = _create_two_students()
        self._valid_payload = {
            'first_name': 'NewFirst1',
            'last_name': 'NewLast1',
            'email_address': 'new-email-address1',
        }
        self._invalid_payload = {
            'first_name': '',
            'last_name': 'NewLast2',
            'email_address': 'new-email-address2',
        }

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_update(self, student_pk, payload):
        response = client.put(reverse('get_delete_update_student',
                                      kwargs={'pk': student_pk}),
                              data=json.dumps(payload),
                              content_type='application/json')

        return response

    def test_update_student_without_authentication(self):
        response = self._do_update(self._student1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_student(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._student1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_student_without_authentication(self):
        response = self._do_update(self._student1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_invalid_student(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._student1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleStudentTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._student1, self._student2 = _create_two_students()

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_delete(self, student_pk):
        response = client.delete(reverse('get_delete_update_student',
                                         kwargs={'pk': student_pk}))

        return response

    def test_delete_student_without_authentication(self):
        response = self._do_delete(self._student1.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_student(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(self._student1.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_missing_student_without_authentication(self):
        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_missing_student(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
