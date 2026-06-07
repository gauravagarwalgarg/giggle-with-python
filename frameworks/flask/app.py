"""
Flask Minimal web framework with routes, blueprints, and templates.

Flask gives you the essentials and lets you pick your own tools
for everything else (ORM, auth, etc.). Perfect for small-medium APIs.
"""
from flask import Flask, Blueprint, jsonify, request, abort
from functools import wraps


# =============================================================================
# APP SETUP
# =============================================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"


# =============================================================================
# BASIC ROUTES
# =============================================================================

@app.route("/")
def index():
    """Root endpoint."""
    return jsonify({
        "message": "Welcome to Flask API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "users": "/api/users",
            "items": "/api/items/<id>",
        }
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


# =============================================================================
# BLUEPRINTS organize routes into modules
# =============================================================================

# Blueprint for user-related routes
users_bp = Blueprint("users", __name__, url_prefix="/api/users")

# In-memory store for demo
_users_db: list[dict] = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
]


@users_bp.route("/", methods=["GET"])
def list_users():
    """GET /api/users list all users with optional filtering."""
    role = request.args.get("role")
    users = _users_db

    if role:
        users = [u for u in users if u["role"] == role]

    return jsonify({"users": users, "count": len(users)})


@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    """GET /api/users/<id> get a single user."""
    user = next((u for u in _users_db if u["id"] == user_id), None)
    if not user:
        abort(404, description=f"User {user_id} not found")
    return jsonify(user)


@users_bp.route("/", methods=["POST"])
def create_user():
    """POST /api/users create a new user.

    Expects JSON body: {"name": "...", "email": "...", "role": "..."}
    """
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        abort(400, description="name and email are required")

    new_user = {
        "id": max(u["id"] for u in _users_db) + 1 if _users_db else 1,
        "name": data["name"],
        "email": data["email"],
        "role": data.get("role", "user"),
    }
    _users_db.append(new_user)
    return jsonify(new_user), 201


@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id: int):
    """PUT /api/users/<id> update an existing user."""
    user = next((u for u in _users_db if u["id"] == user_id), None)
    if not user:
        abort(404, description=f"User {user_id} not found")

    data = request.get_json()
    if data.get("name"):
        user["name"] = data["name"]
    if data.get("email"):
        user["email"] = data["email"]
    if data.get("role"):
        user["role"] = data["role"]

    return jsonify(user)


@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """DELETE /api/users/<id> delete a user."""
    global _users_db
    before = len(_users_db)
    _users_db = [u for u in _users_db if u["id"] != user_id]

    if len(_users_db) == before:
        abort(404, description=f"User {user_id} not found")

    return "", 204


# =============================================================================
# MIDDLEWARE / DECORATORS auth, logging, etc.
# =============================================================================

def require_api_key(f):
    """Simple API key authentication decorator."""
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        if api_key != "my-secret-key":
            abort(401, description="Invalid or missing API key")
        return f(*args, **kwargs)
    return decorated


# Protected blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.route("/stats")
@require_api_key
def admin_stats():
    """GET /api/admin/stats protected endpoint."""
    return jsonify({
        "total_users": len(_users_db),
        "roles": {
            "admin": sum(1 for u in _users_db if u["role"] == "admin"),
            "user": sum(1 for u in _users_db if u["role"] == "user"),
        }
    })


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": str(error.description)}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "message": str(error.description)}), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({"error": "Unauthorized", "message": str(error.description)}), 401


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


# =============================================================================
# REQUEST HOOKS
# =============================================================================

@app.before_request
def log_request():
    """Log every incoming request."""
    # In production, use proper logging
    if app.debug:
        print(f"→ {request.method} {request.path}")


@app.after_request
def add_headers(response):
    """Add security headers to every response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# =============================================================================
# REGISTER BLUEPRINTS
# =============================================================================

app.register_blueprint(users_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    # Run with: python app.py
    # Or: flask run --debug
    print("Flask API running at http://localhost:5000")
    print("Try:")
    print("  curl http://localhost:5000/")
    print("  curl http://localhost:5000/api/users")
    print("  curl -X POST http://localhost:5000/api/users -H 'Content-Type: application/json' -d '{\"name\": \"Dave\", \"email\": \"dave@example.com\"}'")
    print("  curl http://localhost:5000/api/admin/stats -H 'X-API-Key: my-secret-key'")
    app.run(debug=True, port=5000)
