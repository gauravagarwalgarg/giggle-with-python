# FastAPI Modern Async Web Framework

FastAPI is the fastest-growing Python web framework. Built on Starlette and Pydantic, it combines performance with developer experience.

## Quick Start

```bash
# Install
pip install fastapi uvicorn pydantic

# Run (with auto-reload)
uvicorn main:app --reload

# Or run directly
python main.py
```

## Interactive Docs

FastAPI generates API documentation automatically:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## What's in `main.py`

- Pydantic models for request/response validation
- CRUD endpoints with proper HTTP status codes
- Pagination, filtering, and search
- Dependency injection (auth, DB lookup)
- Path and query parameter validation
- Error handling with typed responses
- Startup/shutdown lifecycle events

## Test with curl

```bash
# List users
curl http://localhost:8000/api/users

# Get one user
curl http://localhost:8000/api/users/1

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Dave", "email": "dave@example.com", "password": "securepass123"}'

# Delete (needs API key)
curl -X DELETE http://localhost:8000/api/users/1 \
  -H "X-API-Key: my-secret-key"
```

## When to Use FastAPI

✅ Modern REST/GraphQL APIs
✅ Microservices
✅ Real-time applications (WebSockets)
✅ ML model serving
✅ When you want auto-generated docs

❌ Server-rendered HTML apps (use Django/Flask)
❌ Need built-in admin panel (use Django)
❌ Legacy Python (< 3.8) support needed
