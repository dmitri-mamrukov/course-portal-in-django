from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from rest_framework.test import APIClient
from .common import set_up_admin, clean_up_admin
from ..models import Teacher
from ..serializers import TeacherSerializer


client = APIClient()

def _clean_up_db():
    Teacher.objects.all().delete()

def _create_two_teachers():
    teacher1 = Teacher.objects.create(first_name='First1',
                                      last_name='Last1',
                                      email_address='email-address1')
    teacher2 = Teacher.objects.create(first_name='First2',
                                      last_name='Last2',
                                      email_address='email-address2')

    return (teacher1, teacher2)


class GetAllTeachersTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _do_get(self):
        response = client.get(reverse('get_post_teachers'))

        return response

    def test_get_all_teachers_from_empty_db(self):
        teachers = Teacher.objects.all()
        self.assertEqual(0, len(teachers))
        serializer = TeacherSerializer(teachers, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_teachers_from_populated_db(self):
        _create_two_teachers()
        teachers = Teacher.objects.all()
        self.assertEqual(2, len(teachers))
        serializer = TeacherSerializer(teachers, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleTeacherTest(TestCase):

    def setUp(self):
        self._teacher1, self._teacher2 = _create_two_teachers()

    def tearDown(self):
        _clean_up_db()

    def _do_get(self, teacher_pk):
        response = client.get(reverse('get_delete_update_teacher',
                                      kwargs={'pk': teacher_pk}))

        return response

    def test_get_teacher(self):
        teacher = Teacher.objects.get(pk=self._teacher1.pk)
        serializer = TeacherSerializer(teacher)

        response = self._do_get(self._teacher1.pk)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_missing_teacher(self):
        response = self._do_get(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewTeacherTest(TestCase):

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
        response = client.post(reverse('get_post_teachers'),
                               data=json.dumps(payload),
                               content_type='application/json')

        return response

    def test_create_teacher_without_authentication(self):
        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_teacher(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_teacher_without_authentication(self):
        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invalid_teacher(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleTeacherTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._teacher1, self._teacher2 = _create_two_teachers()

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

    def _do_update(self, teacher_pk, payload):
        response = client.put(reverse('get_delete_update_teacher',
                                      kwargs={'pk': teacher_pk}),
                              data=json.dumps(payload),
                              content_type='application/json')

        return response

    def test_update_teacher_without_authentication(self):
        response = self._do_update(self._teacher1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_teacher(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._teacher1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_teacher_without_authentication(self):
        response = self._do_update(self._teacher1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_invalid_teacher(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._teacher1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleTeacherTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._teacher1, self._teacher2 = _create_two_teachers()

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_delete(self, teacher_pk):
        response = client.delete(reverse('get_delete_update_teacher',
                                         kwargs={'pk': teacher_pk}))

        return response

    def test_delete_teacher_without_authentication(self):
        response = self._do_delete(self._teacher1.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_teacher(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(self._teacher1.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_missing_teacher_without_authentication(self):
        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_missing_teacher(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
