"""
Pytest Examples fixtures, parametrize, mock, markers, and patterns.

Run with: pytest testing/ -v
Coverage: pytest testing/ --cov --cov-report=term-missing
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from dataclasses import dataclass


# =============================================================================
# CODE UNDER TEST a simple module to test
# =============================================================================

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True


class UserService:
    """Service we'll write tests for."""

    def __init__(self, db_client=None):
        self.db = db_client or {}

    def create_user(self, name: str, email: str) -> User:
        if not name or not email:
            raise ValueError("Name and email are required")
        if "@" not in email:
            raise ValueError("Invalid email format")
        if email in [u.email for u in self.db.values()]:
            raise ValueError("Email already exists")

        user_id = max(self.db.keys(), default=0) + 1
        user = User(id=user_id, name=name, email=email)
        self.db[user_id] = user
        return user

    def get_user(self, user_id: int) -> User | None:
        return self.db.get(user_id)

    def list_users(self, active_only: bool = False) -> list[User]:
        users = list(self.db.values())
        if active_only:
            users = [u for u in users if u.active]
        return users

    def deactivate_user(self, user_id: int) -> bool:
        user = self.db.get(user_id)
        if not user:
            return False
        user.active = False
        return True


def fetch_user_data(api_url: str, user_id: int) -> dict:
    """External API call we'll mock this in tests."""
    import requests
    resp = requests.get(f"{api_url}/users/{user_id}")
    resp.raise_for_status()
    return resp.json()


# =============================================================================
# FIXTURES reusable test setup
# =============================================================================

@pytest.fixture
def user_service():
    """Fresh UserService for each test."""
    return UserService()


@pytest.fixture
def populated_service():
    """UserService with pre-loaded data."""
    service = UserService()
    service.create_user("Alice", "alice@example.com")
    service.create_user("Bob", "bob@example.com")
    service.create_user("Charlie", "charlie@example.com")
    service.db[3].active = False  # Deactivate Charlie
    return service


@pytest.fixture
def sample_user():
    """A single User object for testing."""
    return User(id=1, name="Alice", email="alice@example.com")


# =============================================================================
# BASIC TESTS
# =============================================================================

class TestUserCreation:
    """Group related tests in classes."""

    def test_create_user_success(self, user_service):
        """Test successful user creation."""
        user = user_service.create_user("Alice", "alice@example.com")

        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.id == 1
        assert user.active is True

    def test_create_user_auto_increments_id(self, user_service):
        """IDs should auto-increment."""
        user1 = user_service.create_user("Alice", "alice@example.com")
        user2 = user_service.create_user("Bob", "bob@example.com")

        assert user1.id == 1
        assert user2.id == 2

    def test_create_user_empty_name_raises(self, user_service):
        """Should raise ValueError for empty name."""
        with pytest.raises(ValueError, match="Name and email are required"):
            user_service.create_user("", "alice@example.com")

    def test_create_user_invalid_email_raises(self, user_service):
        """Should raise ValueError for invalid email."""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user("Alice", "not-an-email")

    def test_create_user_duplicate_email_raises(self, populated_service):
        """Should prevent duplicate emails."""
        with pytest.raises(ValueError, match="Email already exists"):
            populated_service.create_user("Alice2", "alice@example.com")


# =============================================================================
# PARAMETRIZE run same test with different inputs
# =============================================================================

class TestParametrize:
    """Demonstrate pytest.mark.parametrize."""

    @pytest.mark.parametrize("name,email,expected_valid", [
        ("Alice", "alice@example.com", True),
        ("Bob", "bob@test.co.in", True),
        ("", "valid@email.com", False),      # Empty name
        ("Charlie", "invalid", False),        # No @ in email
        ("Dave", "", False),                   # Empty email
    ])
    def test_create_user_validation(self, user_service, name, email, expected_valid):
        """Test various input combinations."""
        if expected_valid:
            user = user_service.create_user(name, email)
            assert user.name == name
        else:
            with pytest.raises(ValueError):
                user_service.create_user(name, email)

    @pytest.mark.parametrize("input_val,expected", [
        (1, 1),
        (2, 4),
        (3, 9),
        (10, 100),
        (-3, 9),
    ])
    def test_square(self, input_val, expected):
        """Simple parametrized test."""
        assert input_val ** 2 == expected


# =============================================================================
# MOCKING replace external dependencies
# =============================================================================

class TestMocking:
    """Demonstrate unittest.mock with pytest."""

    @patch("requests.get")
    def test_fetch_user_data_success(self, mock_get):
        """Mock an HTTP request."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Alice"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_user_data("https://api.example.com", 1)

        # Assert
        assert result == {"id": 1, "name": "Alice"}
        mock_get.assert_called_once_with("https://api.example.com/users/1")

    @patch("requests.get")
    def test_fetch_user_data_not_found(self, mock_get):
        """Mock a 404 response."""
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404")
        mock_get.return_value = mock_response

        with pytest.raises(requests.HTTPError):
            fetch_user_data("https://api.example.com", 999)

    def test_mock_with_context_manager(self):
        """Alternative mock syntax using context manager."""
        with patch("builtins.open", MagicMock()) as mock_file:
            mock_file.return_value.__enter__ = MagicMock(return_value="file content")
            # Test code that reads a file...


# =============================================================================
# MARKERS categorize tests
# =============================================================================

@pytest.mark.slow
def test_slow_operation():
    """Mark tests that are slow skip with: pytest -m 'not slow'"""
    import time
    time.sleep(0.01)  # Simulate slow operation
    assert True


@pytest.mark.integration
def test_database_connection():
    """Integration tests skip with: pytest -m 'not integration'"""
    # Would test actual DB connection
    assert True


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Skip this test entirely."""
    assert False


@pytest.mark.skipif(
    condition=True,  # e.g., sys.platform == "win32"
    reason="Only runs on Linux"
)
def test_linux_specific():
    """Conditionally skip tests."""
    assert True


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """Expected to fail won't count as test failure."""
    assert 1 + 1 == 3  # Known incorrect


# =============================================================================
# CONFTEST PATTERNS (normally in conftest.py)
# =============================================================================

# In conftest.py, you'd put shared fixtures:
# @pytest.fixture(scope="session")
# def db_connection():
#     """One database connection for all tests."""
#     conn = create_connection()
#     yield conn
#     conn.close()
#
# @pytest.fixture(autouse=True)
# def reset_db(db_connection):
#     """Auto-reset database before each test."""
#     db_connection.execute("TRUNCATE ALL")
#     yield


# =============================================================================
# EXCEPTION TESTING
# =============================================================================

class TestExceptions:
    """Different ways to test exceptions."""

    def test_raises_with_message(self, user_service):
        """Assert exception type AND message."""
        with pytest.raises(ValueError) as exc_info:
            user_service.create_user("", "email@test.com")
        assert "required" in str(exc_info.value)

    def test_raises_specific_type(self):
        """Assert specific exception type."""
        with pytest.raises(ZeroDivisionError):
            1 / 0

    def test_does_not_raise(self, user_service):
        """Verify no exception is raised."""
        # This pattern is implicit if no exception, test passes
        user = user_service.create_user("Valid", "valid@test.com")
        assert user is not None


# =============================================================================
# TEMPORARY FILES AND DIRECTORIES
# =============================================================================

def test_with_tmp_path(tmp_path):
    """pytest provides tmp_path fixture for temp directories."""
    # tmp_path is a pathlib.Path unique per test
    file = tmp_path / "test.txt"
    file.write_text("hello")

    assert file.read_text() == "hello"
    assert file.exists()


def test_with_tmp_file(tmp_path):
    """Write and read JSON in temp directory."""
    import json
    data = {"key": "value", "numbers": [1, 2, 3]}

    json_file = tmp_path / "config.json"
    json_file.write_text(json.dumps(data))

    loaded = json.loads(json_file.read_text())
    assert loaded == data


# =============================================================================
# CUSTOM MARKERS (register in pytest.ini or pyproject.toml)
# =============================================================================

# In pyproject.toml:
# [tool.pytest.ini_options]
# markers = [
#     "slow: marks tests as slow",
#     "integration: marks integration tests",
#     "e2e: marks end-to-end tests",
# ]


if __name__ == "__main__":
    # Run tests from this file
    pytest.main([__file__, "-v", "--tb=short"])
