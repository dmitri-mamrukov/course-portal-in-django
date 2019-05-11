# course-portal-in-django

Student Course Management system using Django REST Framework and PostgreSQL

##

I implemented a student course management system, using Django REST Framework (www.django-rest-framework.org) and Postgres, with the following functionality via RESTful endpoints:

* Get, adds, updates, and deletes students
* Get, adds, updates, and deletes teachers
* Get, adds, updates, and deletes courses
* Get, adds, updates, and deletes enrollments
* Get students enrolled in a given course
* Get courses a given student is enrolled in
* Search courses by title or start date
* Search students by name

Read (`GET`) actions are not restricted.

Write (`POST`, `PUT`, and `DELETE`) actions are authenticated.

**Authentication** and **permissions** are currently supported for the portal’s admins (which are created by
`python3 manage.py createsuperuser`).

**Rate-limiting** is supported and configured by `REST_FRAMEWORK` in courses/settings.py.
It’s possible to configure **policies** in different ways:
https://www.django-rest-framework.org/api-guide/throttling.

## Run/Test

See `Makefile`.
