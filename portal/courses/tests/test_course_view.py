from datetime import date, datetime
from django.core.serializers.json import json, DjangoJSONEncoder
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .common import set_up_admin, clean_up_admin
from ..models import Course, Teacher
from ..serializers import CourseSerializer


client = APIClient()

def _clean_up_db():
    Course.objects.all().delete()
    Teacher.objects.all().delete()

def _create_two_courses():
    teacher1 = Teacher.objects.create(first_name='First1',
                                      last_name='Last1',
                                      email_address='email-address1')
    teacher2 = Teacher.objects.create(first_name='First2',
                                      last_name='Last2',
                                      email_address='email-address2')
    course1 = Course.objects.create(title='Title1',
                                    teacher=teacher1,
                                    start_date=date(2017, 9, 1))
    course2 = Course.objects.create(title='Title2',
                                    teacher=teacher2,
                                    start_date=date(2018, 9, 1))

    return (course1, course2)


class GetAllCoursesTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _do_get(self):
        response = client.get(reverse('get_post_courses'))

        return response

    def test_get_all_courses_from_empty_db(self):
        courses = Course.objects.all()
        self.assertEqual(0, len(courses))
        serializer = CourseSerializer(courses, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_courses_from_populated_db(self):
        _create_two_courses()
        courses = Course.objects.all()
        self.assertEqual(2, len(courses))
        serializer = CourseSerializer(courses, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleCourseTest(TestCase):

    def setUp(self):
        self._course1, self._course2 = _create_two_courses()

    def tearDown(self):
        _clean_up_db()

    def _do_get(self, course_pk):
        response = client.get(reverse('get_delete_update_course',
                                      kwargs={'pk': course_pk}))

        return response

    def test_get_course(self):
        course = Course.objects.get(pk=self._course1.pk)
        serializer = CourseSerializer(course)

        response = self._do_get(self._course1.pk)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_missing_course(self):
        response = self._do_get(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCourseTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        teacher = Teacher.objects.create(first_name='First',
                                         last_name='Last',
                                         email_address='email-address')

        self._valid_payload = {
            'title': 'Title1',
            'teacher': teacher.pk,
            'start_date': json.dumps(date(2017, 9, 1),
                                     cls=DjangoJSONEncoder),
        }
        self._invalid_payload = {
            'title': '',
            'teacher': teacher.pk,
            'start_date': json.dumps(date(2017, 9, 1),
                                     cls=DjangoJSONEncoder),
        }

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_post(self, payload):
        response = client.post(reverse('get_post_courses'),
                               data=json.dumps(payload),
                               content_type='application/json')

        return response

    def test_create_course_without_authentication(self):
        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_course_without_authentication(self):
        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invalid_course(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCourseTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._course1, self._course2 = _create_two_courses()
        self._valid_payload = {
            'title': 'NewTitle1',
            'teacher': self._course1.teacher.pk,
            'start_date': json.dumps(date(2017, 10, 1),
                                     cls=DjangoJSONEncoder),
        }
        self._invalid_payload = {
            'title': '',
            'teacher': self._course1.teacher.pk,
            'start_date': json.dumps(date(2018, 10, 1),
                                     cls=DjangoJSONEncoder),
        }

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_update(self, course_pk, payload):
        response = client.put(reverse('get_delete_update_course',
                                      kwargs={'pk': course_pk}),
                              data=json.dumps(payload),
                              content_type='application/json')

        return response

    def test_update_course_without_authentication(self):
        response = self._do_update(self._course1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_course(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._course1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_course_without_authentication(self):
        response = self._do_update(self._course1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_invalid_course(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._course1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCourseTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._course1, self._course2 = _create_two_courses()

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_delete(self, course_pk):
        response = client.delete(reverse('get_delete_update_course',
                                         kwargs={'pk': course_pk}))

        return response

    def test_delete_course_without_authentication(self):
        response = self._do_delete(self._course1.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_course(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(self._course1.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_missing_course_without_authentication(self):
        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_missing_course(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
