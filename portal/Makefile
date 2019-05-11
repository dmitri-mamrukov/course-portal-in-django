run-server:
	python3 manage.py runserver

show-migrations:
	python3 manage.py showmigrations

reset-migrations:
	./reset-migrations.sh

clear-migration-history:
	python3 manage.py migrate --fake courses zero

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

test:
	python3 manage.py test

coverage:
	coverage run --source='.' manage.py test
	coverage report
