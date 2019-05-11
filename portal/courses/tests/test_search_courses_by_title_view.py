from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from ..models import Course, Teacher
from ..serializers import CourseSerializer


client = Client()

def _clean_up_db():
    Course.objects.all().delete()
    Teacher.objects.all().delete()

def _create_courses():
    teacher1 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    teacher2 = Teacher.objects.create(first_name='TeacherFirst1',
                                      last_name='TeacherLast1',
                                      email_address='teacher-email-address1')
    course1 = Course.objects.create(title='Math',
                                    teacher=teacher1,
                                    start_date=date(2018, 9, 1))
    course2 = Course.objects.create(title='Physics',
                                    teacher=teacher2,
                                    start_date=date(2018, 10, 1))
    course3 = Course.objects.create(title='Physical Patterns',
                                    teacher=teacher2,
                                    start_date=date(2018, 11, 1))
    course4 = Course.objects.create(title='Design Patterns I',
                                    teacher=teacher1,
                                    start_date=date(2019, 1, 1))
    course5 = Course.objects.create(title='Design Patterns II',
                                    teacher=teacher1,
                                    start_date=date(2019, 2, 1))

    return (course1, course2, course3, course4, course5)


class SearchCoursesByTitleTest(TestCase):

    def tearDown(self):
        _clean_up_db()

    def _assert_response(self, title, expected_results):
        serializer = CourseSerializer(expected_results, many=True)

        response = client.get(reverse('get_courses_by_title',
                                      kwargs={'title': title}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_courses_from_empty_db(self):
        courses = Course.objects.all()
        self.assertEqual(0, len(courses))

        self._assert_response(1234567890, [])

    def test_get_courses_from_populated_db(self):
        course1, course2, course3, course4, course5 = _create_courses()
        math_courses = [course1]
        pattern_courses = [course3, course4, course5]
        physic_courses = [course2, course3]
        python_courses = []

        self._assert_response('Math', math_courses)
        self._assert_response('pattern', pattern_courses)
        self._assert_response('physic', physic_courses)
        self._assert_response('python', python_courses)
