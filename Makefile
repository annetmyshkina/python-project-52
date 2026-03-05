
install:
	uv sync --extra dev

test:
	uv run coverage run manage.py test
	uv run coverage report
	uv run coverage xml

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
	uv run gunicorn task_manager.wsgi:application

deploy:
	uv run make migrate collectstatic build

