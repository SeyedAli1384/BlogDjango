# DigiMarket — Django Blog Platform

DigiMarket is a Django-based blogging application built as a learning project to practise backend development, database-backed web applications, authentication, and containerized deployment.

The project began as my own implementation. AI tools assisted with the later frontend redesign and documentation. I am continuing to learn, review, and improve the codebase.

## Features

- User registration and login
- Blog creation and management
- Blog feed and detail pages
- Topic-based blog organization
- Comments and user activity
- Responsive interface with shared navigation and footer
- Django ORM and database migrations
- Automated tests
- Docker and Docker Compose deployment
- Gunicorn application server
- Redis service configured through environment variables
- Persistent Docker volumes for application data and Redis

> Feature availability and behavior depend on the current implementation. This is a learning project, not a production-ready blogging service.

## Technology Stack

- **Language:** Python
- **Web framework:** Django
- **Database:** SQLite
- **Cache/service:** Redis
- **Application server:** Gunicorn
- **Containers:** Docker and Docker Compose
- **Frontend:** HTML, CSS, Django templates

## Project Structure

```text
BlogDjango/
├── core/
│   ├── migrations/
│   └── templates/
│       └── core/
├── static/
│   └── styles/
├── templates/
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── manage.py
├── .env.example
├── .dockerignore
└── README.md
```

## Requirements

For local development:

- Python 3.13 or a compatible Python version
- pip
- Git

For containerized deployment:

- Docker Engine
- Docker Compose plugin

## Run Locally

Clone the repository and enter the project directory:

```bash
git clone https://github.com/SeyedAli1384/BlogDjango.git
cd BlogDjango
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your local environment file from the example:

```bash
cp .env.example .env
```

Edit `.env` and configure a new, private Django `SECRET_KEY`. Keep `DEBUG` and `ALLOWED_HOSTS` appropriate for your environment. Do not commit `.env`.

Apply migrations and start Django:

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

The local setup depends on the environment variables and services required by the current settings. If Redis is enabled for your local configuration, start a Redis service and configure `REDIS_URL` accordingly.

## Run with Docker Compose

Create the environment file if it does not already exist:

```bash
cp .env.example .env
```

Edit `.env` before starting the application. Use a unique secret key and keep this file private.

Build and start the services:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs --tail=100 web
```

Open http://127.0.0.1:8000/.

Stop the services:

```bash
docker compose down
```

The Compose configuration uses named volumes for persistent application data and Redis data. A normal `docker compose down` does not remove these volumes. Avoid `docker compose down -v` unless you intentionally want to delete the associated persisted data.

## Environment Variables

The `.env.example` file documents the expected configuration:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django signing and security-related operations |
| `DEBUG` | Enables or disables Django debug mode |
| `ALLOWED_HOSTS` | Hosts permitted by Django |
| `SQLITE_PATH` | Path to the SQLite database |
| `REDIS_URL` | Redis connection URL |

Use placeholder values in `.env.example`; keep real secrets and private configuration in `.env`, which should not be committed.

## Tests and Checks

Run the Django test suite:

```bash
python manage.py test
```

Run Django's system checks:

```bash
python manage.py check
```

Check for uncreated migrations:

```bash
python manage.py makemigrations --check --dry-run
```

When running the containerized setup, these commands can also be executed inside the web container:

```bash
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec web python manage.py showmigrations
docker compose exec redis redis-cli ping
```

## Current Status

The Dockerized application has been built and started successfully in the development environment. Database migrations, Django system checks, the test suite, static-file collection, and the Redis connectivity check have been verified there.

This status describes the tested environment; it is not a claim of a production deployment or a security audit.

## Learning Goals

This project provides practice with:

- Django views, templates, models, and migrations
- Database-backed application features
- Authentication and user interactions
- Environment-based configuration
- Docker image builds and Compose services
- Persistent volumes and application deployment
- Automated testing and Git-based development

## Limitations

- This is a learning project and may require additional security, accessibility, and usability work.
- SQLite is used for the current database configuration.
- Production deployment would require a separate review of settings, secrets, database backups, monitoring, and operational security.
- AI tools assisted with the frontend redesign and documentation; the project is still subject to ongoing review and learning.

## License

No license has been specified yet. All rights are reserved by default unless a license is added to the repository.
