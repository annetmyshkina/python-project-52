
install:
	uv sync

test:
	coverage run manage.py test
	coverage report
	coverage xml

check:
	uv run ruff check . --exclude="**/migrations/" --exclude="task_manager/settings.py"

format:
	uv run ruff format . --exclude="**/migrations/" --exclude="task_manager/settings.py"

fix:
	uv run ruff check --fix .

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

build:
	./build.sh

run:
	uv run python manage.py runserver

render-start:
	gunicorn task_manager.wsgi:application

deploy:
	migrate collectstatic build

