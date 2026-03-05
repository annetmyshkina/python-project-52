
install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

build:
	./build.sh

run:
	uv run python manage.py runserver

render-start:
	gunicorn task_manager.wsgi:application

build:
	./build.sh

test:
	coverage run manage.py test
	coverage report

check:
	uv run ruff check . --exclude="**/migrations/" --exclude="task_manager/settings.py"

format:
	uv run ruff format . --exclude="**/migrations/" --exclude="task_manager/settings.py"

fix:
	uv run ruff check --fix .

run:
	uv run python manage.py runserver

ci:
	check test

deploy:
	migrate collectstatic build