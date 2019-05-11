from datetime import date, datetime
from django.core.serializers.json import json, DjangoJSONEncoder
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .common import set_up_admin, clean_up_admin
from ..models import Course, Enrollment, Student, Teacher
from ..serializers import EnrollmentSerializer


client = APIClient()

def _clean_up_db():
        Course.objects.all().delete()
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Enrollment.objects.all().delete()

def _create_two_enrollments():
    student1 = Student.objects.create(first_name='StudentFirst1',
                                      last_name='StudentLast1',
                                      email_address='student-email-address1')
    student2 = Student.objects.create(first_name='StudentFirst2',
                                      last_name='StudentLast2',
                                      email_address='student-email-address2')
    teacher1 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    teacher2 = Teacher.objects.create(first_name='TeacherFirst2',
                                      last_name='TeacherLast2',
                                      email_address='teacher-email-address2')
    course1 = Course.objects.create(title='Title1',
                                    teacher=teacher1,
                                    start_date=date(2018, 9, 1))
    course2 = Course.objects.create(title='Title2',
                                    teacher=teacher2,
                                    start_date=date(2018, 10, 1))
    enrollment1 = Enrollment.objects.create(course=course1,
                                            student=student1,
                                            grade='A')
    enrollment2 = Enrollment.objects.create(course=course2,
                                            student=student2,
                                            grade='B')

    return (enrollment1, enrollment2)


class GetAllEnrollmentsTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _do_get(self):
        response = client.get(reverse('get_post_enrollments'))

        return response

    def test_get_all_enrollments_from_empty_db(self):
        enrollments = Enrollment.objects.all()
        self.assertEqual(0, len(enrollments))
        serializer = EnrollmentSerializer(enrollments, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_enrollments_from_populated_db(self):
        _create_two_enrollments()
        enrollments = Enrollment.objects.all()
        self.assertEqual(2, len(enrollments))
        serializer = EnrollmentSerializer(enrollments, many=True)

        response = self._do_get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GetSingleEnrollmentTest(TestCase):

    def setUp(self):
        self._enrollment1, self._enrollment2 = _create_two_enrollments()

    def tearDown(self):
        _clean_up_db()

    def _do_get(self, enrollment_pk):
        response = client.get(reverse('get_delete_update_enrollment',
                                      kwargs={'pk': enrollment_pk}))

        return response

    def test_get_enrollment(self):
        course = Enrollment.objects.get(pk=self._enrollment1.pk)
        serializer = EnrollmentSerializer(course)

        response = self._do_get(self._enrollment1.pk)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_missing_enrollment(self):
        response = self._do_get(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewEnrollmentTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        student = Student.objects.create(first_name='First1',
                                         last_name='Last1',
                                         email_address='email-address1')
        teacher = Teacher.objects.create(first_name='First1',
                                         last_name='Last1',
                                         email_address='email-address1')
        course = Course.objects.create(title='Title1',
                                       teacher=teacher,
                                       start_date=date(2018, 9, 1))

        self._valid_payload = {
            'course': course.pk,
            'student': student.pk,
            'grade': None,
        }
        self._invalid_payload = {
            'course': None,
            'student': student.pk,
            'grade': None,
        }

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_post(self, payload):
        response = client.post(reverse('get_post_enrollments'),
                               data=json.dumps(payload),
                               content_type='application/json')

        return response

    def test_create_enrollment_without_authentication(self):
        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_enrollment(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_enrollment_without_authentication(self):
        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_invalid_enrollment(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_post(self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleEnrollmentTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._enrollment1, self._enrollment2 = _create_two_enrollments()

        self._valid_payload = {
            'course': self._enrollment1.course.pk,
            'student': self._enrollment1.student.pk,
            'grade': None,
        }
        self._invalid_payload = {
            'course': None,
            'student': self._enrollment1.student.pk,
            'grade': None,
        }

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_update(self, enrollment_pk, payload):
        response = client.put(reverse('get_delete_update_enrollment',
                                      kwargs={'pk': enrollment_pk}),
                              data=json.dumps(payload),
                              content_type='application/json')

        return response

    def test_update_enrollment_without_authentication(self):
        response = self._do_update(self._enrollment1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_enrollment(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._enrollment1.pk, self._valid_payload)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_invalid_enrollment_without_authentication(self):
        response = self._do_update(self._enrollment1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_invalid_enrollment(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_update(self._enrollment1.pk, self._invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleEnrollmentTest(TestCase):

    def setUp(self):
        self._admin_user = set_up_admin()
        self._enrollment1, self._enrollment2 = _create_two_enrollments()

    def tearDown(self):
        clean_up_admin(self._admin_user, client)
        _clean_up_db()

    def _do_delete(self, enrollment_pk):
        response = client.delete(reverse('get_delete_update_enrollment',
                                         kwargs={'pk': enrollment_pk}))

        return response

    def test_delete_enrollment_without_authentication(self):
        response = self._do_delete(self._enrollment1.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_enrollment(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(self._enrollment1.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_missing_enrollment_without_authentication(self):
        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_missing_enrollment(self):
        client.force_authenticate(user=self._admin_user)

        response = self._do_delete(1234567890)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
