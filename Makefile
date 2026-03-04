
install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi:application

check:
	uv run ruff check . --exclude="**/migrations/" --exclude="task_manager/settings.py"

format:
	uv run ruff format . --exclude="**/migrations/" --exclude="task_manager/settings.py"

fix:
	uv run ruff check --fix .