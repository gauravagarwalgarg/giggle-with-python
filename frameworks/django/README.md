# Django Full-Featured Web Framework

Django is Python's "batteries-included" web framework. Use it when you need:
- Admin panel out of the box
- ORM with migrations
- Authentication, sessions, CSRF protection
- Template engine
- Form handling and validation

## Quick Start

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Django
pip install django

# Create a new project
django-admin startproject myproject .

# Create an app
python manage.py startapp myapp

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

```
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── myapp/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── serializers.py  (DRF)
    └── tests.py
```

## Key Commands

```bash
python manage.py makemigrations    # Generate migrations from model changes
python manage.py migrate           # Apply migrations
python manage.py shell             # Django shell with ORM access
python manage.py test              # Run tests
python manage.py collectstatic     # Gather static files for production
python manage.py dbshell           # Database CLI
```

## When to Use Django

✅ Content-heavy sites, CMS, e-commerce
✅ Projects that need an admin interface
✅ Teams that want conventions over configuration
✅ REST APIs (with Django REST Framework)

❌ Microservices (too heavy)
❌ WebSocket-heavy apps (use FastAPI or channels)
❌ Simple APIs with 2-3 endpoints (use Flask/FastAPI)
