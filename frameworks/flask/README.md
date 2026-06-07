# Flask Lightweight Web Framework

Flask is a micro-framework it gives you routing, request/response handling, and templates. You add everything else as needed.

## Quick Start

```bash
# Install
pip install flask

# Run the app
python app.py
# or
flask run --debug

# Test
curl http://localhost:5000/
curl http://localhost:5000/api/users
curl http://localhost:5000/api/users/1
```

## What's in `app.py`

- Basic routing with different HTTP methods
- Blueprints for modular route organization
- Request parsing (query params, JSON body)
- Error handlers (404, 400, 401, 500)
- Simple API key authentication decorator
- Before/after request hooks
- CRUD operations (Create, Read, Update, Delete)

## When to Use Flask

✅ Small to medium APIs (< 20 endpoints)
✅ Prototyping and MVPs
✅ Microservices
✅ When you want control over your stack

❌ Large apps that need conventions (use Django)
❌ High-performance async (use FastAPI)
❌ Built-in admin panel (use Django)

## Extensions Worth Knowing

- `Flask-SQLAlchemy` ORM integration
- `Flask-Migrate` Database migrations (Alembic)
- `Flask-Login` Session-based authentication
- `Flask-CORS` Cross-Origin Resource Sharing
- `Flask-Limiter` Rate limiting
- `Flask-Caching` Response caching
