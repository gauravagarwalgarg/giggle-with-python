"""
FastAPI Modern async web framework with automatic OpenAPI docs.

FastAPI gives you:
- Automatic request validation (via Pydantic)
- Auto-generated OpenAPI/Swagger docs
- Async support out of the box
- Dependency injection system
- Type-safe request/response handling

Run with: uvicorn main:app --reload
Docs at: http://localhost:8000/docs
"""
from datetime import datetime
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Path, Depends, Header, status
from pydantic import BaseModel, Field, EmailStr


# =============================================================================
# APP SETUP
# =============================================================================

app = FastAPI(
    title="GiggleWithPython API",
    description="Example FastAPI application with CRUD operations",
    version="1.0.0",
)


# =============================================================================
# PYDANTIC MODELS request/response validation
# =============================================================================

class UserRole(str, Enum):
    """Enum for user roles shows up as dropdown in docs."""
    admin = "admin"
    user = "user"
    moderator = "moderator"


class UserBase(BaseModel):
    """Shared fields between create and response."""
    name: str = Field(..., min_length=1, max_length=100, examples=["Alice"])
    email: str = Field(..., examples=["alice@example.com"])
    role: UserRole = UserRole.user


class UserCreate(UserBase):
    """Request body for creating a user."""
    password: str = Field(..., min_length=8, examples=["securepass123"])


class UserUpdate(BaseModel):
    """Request body for updating all fields optional."""
    name: str | None = None
    email: str | None = None
    role: UserRole | None = None


class UserResponse(UserBase):
    """Response model what the API returns (no password!)."""
    id: int
    created_at: datetime
    is_active: bool = True

    model_config = {"from_attributes": True}


class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: list[UserResponse]
    total: int
    page: int
    per_page: int
    pages: int


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    code: str | None = None


# =============================================================================
# IN-MEMORY DATABASE (replace with real DB in production)
# =============================================================================

_db: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin",
        "password": "hashed_pw", "created_at": datetime(2024, 1, 1), "is_active": True},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user",
        "password": "hashed_pw", "created_at": datetime(2024, 2, 15), "is_active": True},
    3: {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "moderator",
        "password": "hashed_pw", "created_at": datetime(2024, 3, 20), "is_active": False},
}
_next_id = 4


# =============================================================================
# DEPENDENCIES reusable logic injected into routes
# =============================================================================

async def verify_api_key(x_api_key: Annotated[str, Header()] = ""):
    """Dependency validates API key from header.

    FastAPI's DI system is powerful use it for auth, DB sessions, etc.
    """
    if x_api_key != "my-secret-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return x_api_key


async def get_user_or_404(user_id: Annotated[int, Path(ge=1)]) -> dict:
    """Dependency fetch user or raise 404."""
    user = _db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user


# =============================================================================
# ROUTES CRUD operations
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with API info."""
    return {
        "message": "FastAPI Example",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get(
    "/api/users",
    response_model=PaginatedResponse,
    summary="List users",
    tags=["users"],
)
async def list_users(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    per_page: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
    role: UserRole | None = None,
    is_active: bool | None = None,
    search: Annotated[str | None, Query(description="Search by name")] = None,
):
    """List users with pagination, filtering, and search.

    Query parameters are automatically validated by FastAPI.
    """
    users = list(_db.values())

    # Apply filters
    if role:
        users = [u for u in users if u["role"] == role.value]
    if is_active is not None:
        users = [u for u in users if u["is_active"] == is_active]
    if search:
        users = [u for u in users if search.lower() in u["name"].lower()]

    # Paginate
    total = len(users)
    start = (page - 1) * per_page
    items = users[start:start + per_page]

    return PaginatedResponse(
        items=[UserResponse(**u) for u in items],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page,
    )


@app.get(
    "/api/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
    responses={404: {"model": ErrorResponse}},
)
async def get_user(user: Annotated[dict, Depends(get_user_or_404)]):
    """Get a single user by ID.

    Uses dependency injection to handle the 404 case.
    """
    return UserResponse(**user)


@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
async def create_user(user_data: UserCreate):
    """Create a new user.

    Request body is automatically validated against UserCreate schema.
    """
    global _next_id

    # Check for duplicate email
    if any(u["email"] == user_data.email for u in _db.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {user_data.email} already registered"
        )

    new_user = {
        "id": _next_id,
        "name": user_data.name,
        "email": user_data.email,
        "role": user_data.role.value,
        "password": f"hashed_{user_data.password}",  # Hash in production!
        "created_at": datetime.now(),
        "is_active": True,
    }
    _db[_next_id] = new_user
    _next_id += 1

    return UserResponse(**new_user)


@app.patch(
    "/api/users/{user_id}",
    response_model=UserResponse,
    tags=["users"],
)
async def update_user(
    user_data: UserUpdate,
    user: Annotated[dict, Depends(get_user_or_404)],
):
    """Partially update a user only provided fields are changed."""
    update_dict = user_data.model_dump(exclude_unset=True)
    if "role" in update_dict and update_dict["role"]:
        update_dict["role"] = update_dict["role"].value

    user.update(update_dict)
    return UserResponse(**user)


@app.delete(
    "/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
    dependencies=[Depends(verify_api_key)],  # Protected!
)
async def delete_user(user_id: Annotated[int, Path(ge=1)]):
    """Delete a user requires API key.

    The dependencies parameter protects this endpoint.
    """
    if user_id not in _db:
        raise HTTPException(status_code=404, detail="User not found")
    del _db[user_id]


# =============================================================================
# ITEMS another resource to show patterns
# =============================================================================

class Item(BaseModel):
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    description: str | None = None
    tags: list[str] = []


_items: list[dict] = []


@app.post("/api/items", tags=["items"], status_code=201)
async def create_item(item: Item):
    """Create an item demonstrates nested validation."""
    item_dict = item.model_dump()
    item_dict["id"] = len(_items) + 1
    _items.append(item_dict)
    return item_dict


@app.get("/api/items", tags=["items"])
async def list_items(
    min_price: float | None = None,
    max_price: float | None = None,
    tag: str | None = None,
):
    """List items with price range and tag filtering."""
    items = _items
    if min_price is not None:
        items = [i for i in items if i["price"] >= min_price]
    if max_price is not None:
        items = [i for i in items if i["price"] <= max_price]
    if tag:
        items = [i for i in items if tag in i["tags"]]
    return items


# =============================================================================
# STARTUP / SHUTDOWN EVENTS
# =============================================================================

@app.on_event("startup")
async def startup():
    """Run on app startup initialize connections, caches, etc."""
    print("🚀 FastAPI starting up...")


@app.on_event("shutdown")
async def shutdown():
    """Run on app shutdown close connections, flush buffers."""
    print("👋 FastAPI shutting down...")


if __name__ == "__main__":
    import uvicorn

    print("Starting FastAPI server...")
    print("Docs: http://localhost:8000/docs")
    print("ReDoc: http://localhost:8000/redoc")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
