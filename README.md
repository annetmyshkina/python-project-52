### Hexlet tests and linter status:
[![Actions Status](https://github.com/annetmyshkina/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/annetmyshkina/python-project-52/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=annetmyshkina_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=annetmyshkina_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=annetmyshkina_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=annetmyshkina_python-project-52)

# [Task Manager](https://python-project-52-eaa3.onrender.com)
A Django-powered web app for managing tasks. It enables users to create tasks,  
assign team members, monitor progress, and apply labels for organization.    

The project has been deployed on the free demo service render.com,    
which offered time-limited resources during the deployment process.

## Features
* User Management: Registration, authentication, profile editing
* Task Management: Create, view, edit and delete tasks
* Task Statuses: Flexible status system to track progress
* Labels: Categorize tasks with custom labels
* Filtering: Convenient task filtering by status, executor, and labels
* Multilingual: Russian and English language support
* Security: Permission separation (only author can delete a task)

## Localization
The application supports two languages:

* English (en)
* Russian (ru)

Language switching is available in the navigation menu.

## Tech Stack
* Python 3.13+
* Django 6.0+ 
* PostgreSQL (production) / SQLite (development)
* Bootstrap 5 (via django-bootstrap5)
* Gunicorn (WSGI server)
* Whitenoise (static files)
* Rollbar (error tracking)
* django-filter (task filtering)
* python-dotenv (environment variables management)

## Requirements
* Python 3.13 or higher
* PostgreSQL (optional, for production)
* Make (for convenient command execution)

### Installation

install the project via [pip](https://pypi.org/project/pip/)

```bash
pip install --user git+https://github.com/annetmyshkina/python-project-52.git
```

or clone the repository:

```bash
git clone https://github.com/annetmyshkina/python-project-52.git
cd python-project-52
```
### Makefile commands:

Install dependencies and run:
```bash
make install    # Install dependencies (including dev)
make migrate    # Apply migrations
make run        # Start development server
```

Testing & Linting:
```bash
make check       # Run linter
make format      # Format code
make fix         # Auto-fix linting errors
make test        # Run tests with coverage report
```

Deployment:
```bash
make deploy  # Apply migrations, collect static files
```

