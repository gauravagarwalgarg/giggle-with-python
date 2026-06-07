"""
HTTP Requests requests library patterns, retry, auth, pagination.

The requests library is Python's de facto HTTP client. This file
covers patterns you'll use in every project that talks to APIs.
"""
import time
from typing import Any, Generator
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# =============================================================================
# SESSION SETUP connection pooling, retries, timeouts
# =============================================================================

def create_session(
    base_url: str = "",
    retries: int = 3,
    backoff_factor: float = 0.5,
    timeout: tuple[float, float] = (5.0, 30.0),
    headers: dict = None,
) -> requests.Session:
    """Create a configured session with retry logic and connection pooling.

    Args:
        base_url: Prepended to all relative URLs
        retries: Number of retry attempts for failed requests
        backoff_factor: Wait time multiplier between retries (0.5 → 0.5s, 1s, 2s)
        timeout: (connect_timeout, read_timeout) in seconds
        headers: Default headers for all requests
    """
    session = requests.Session()

    # Retry strategy retries on 429 (rate limit) and 5xx (server errors)
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE"],
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,
        pool_maxsize=10,
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Default headers
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "PythonClient/1.0",
        **(headers or {}),
    })

    # Store config on session for use in helper methods
    session._base_url = base_url
    session._timeout = timeout

    return session


# =============================================================================
# BASIC REQUESTS GET, POST, PUT, DELETE
# =============================================================================

def get_json(url: str, params: dict = None, headers: dict = None) -> dict:
    """Simple GET request that returns JSON."""
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def post_json(url: str, data: dict, headers: dict = None) -> dict:
    """POST JSON data and return response."""
    resp = requests.post(url, json=data, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def download_file(url: str, filepath: str, chunk_size: int = 8192) -> None:
    """Download a file with streaming (memory-efficient for large files)."""
    with requests.get(url, stream=True, timeout=30) as resp:
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                f.write(chunk)


# =============================================================================
# AUTHENTICATION PATTERNS
# =============================================================================

def with_bearer_token(session: requests.Session, token: str) -> requests.Session:
    """Add Bearer token authentication to session."""
    session.headers["Authorization"] = f"Bearer {token}"
    return session


def with_basic_auth(session: requests.Session, username: str, password: str) -> requests.Session:
    """Add Basic authentication to session."""
    session.auth = (username, password)
    return session


def with_api_key(session: requests.Session, key: str, header_name: str = "X-API-Key") -> requests.Session:
    """Add API key authentication to session."""
    session.headers[header_name] = key
    return session


class OAuth2Client:
    """OAuth2 client credentials flow for service-to-service auth."""

    def __init__(self, token_url: str, client_id: str, client_secret: str):
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token: str = ""
        self._expires_at: float = 0

    def get_token(self) -> str:
        """Get or refresh the access token."""
        if time.time() < self._expires_at - 60:  # Refresh 60s before expiry
            return self._token

        resp = requests.post(self.token_url, data={
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        })
        resp.raise_for_status()
        data = resp.json()

        self._token = data["access_token"]
        self._expires_at = time.time() + data.get("expires_in", 3600)
        return self._token

    def get_session(self) -> requests.Session:
        """Get a session with the current access token."""
        session = create_session()
        session.headers["Authorization"] = f"Bearer {self.get_token()}"
        return session


# =============================================================================
# PAGINATION handle paginated API responses
# =============================================================================

def paginate_offset(
    url: str,
    session: requests.Session = None,
    params: dict = None,
    page_size: int = 100,
    max_pages: int = 100,
) -> Generator[list, None, None]:
    """Paginate using offset/limit (common in REST APIs).

    Yields one page of results at a time.
    """
    session = session or requests.Session()
    params = params or {}

    for page in range(max_pages):
        page_params = {
            **params,
            "offset": page * page_size,
            "limit": page_size,
        }
        resp = session.get(url, params=page_params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # Handle different response formats
        items = data if isinstance(data, list) else data.get("results", data.get("items", []))

        if not items:
            break

        yield items

        if len(items) < page_size:
            break


def paginate_cursor(
    url: str,
    session: requests.Session = None,
    params: dict = None,
    cursor_field: str = "next_cursor",
) -> Generator[list, None, None]:
    """Paginate using cursor-based pagination (e.g., Slack, Twitter).

    More efficient than offset for large datasets.
    """
    session = session or requests.Session()
    params = params or {}
    cursor = None

    while True:
        page_params = {**params}
        if cursor:
            page_params["cursor"] = cursor

        resp = session.get(url, params=page_params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("results", data.get("items", []))
        yield items

        cursor = data.get(cursor_field)
        if not cursor:
            break


def paginate_link_header(
    url: str,
    session: requests.Session = None,
) -> Generator[list, None, None]:
    """Paginate using Link header (GitHub API style).

    The API returns a Link header with the URL for the next page.
    """
    session = session or requests.Session()

    while url:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        yield resp.json()

        # Parse Link header for next URL
        link_header = resp.headers.get("Link", "")
        url = None
        for part in link_header.split(","):
            if 'rel="next"' in part:
                url = part.split(";")[0].strip().strip("<>")
                break


# =============================================================================
# RATE LIMITING respect API limits
# =============================================================================

class RateLimitedSession:
    """Session wrapper that respects rate limits."""

    def __init__(self, session: requests.Session, requests_per_second: float = 10):
        self.session = session
        self.min_interval = 1.0 / requests_per_second
        self._last_request = 0.0

    def _wait(self):
        """Wait if we're making requests too fast."""
        elapsed = time.time() - self._last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_request = time.time()

    def get(self, url: str, **kwargs) -> requests.Response:
        self._wait()
        return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        self._wait()
        return self.session.post(url, **kwargs)


# =============================================================================
# ERROR HANDLING
# =============================================================================

def safe_request(url: str, method: str = "GET", **kwargs) -> dict[str, Any]:
    """Make a request with comprehensive error handling.

    Returns a standardized response dict instead of raising exceptions.
    """
    try:
        resp = requests.request(method, url, timeout=10, **kwargs)
        resp.raise_for_status()
        return {
            "success": True,
            "status_code": resp.status_code,
            "data": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text,
            "headers": dict(resp.headers),
        }
    except requests.exceptions.Timeout:
        return {"success": False, "error": "timeout", "message": f"Request to {url} timed out"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "connection", "message": f"Cannot connect to {url}"}
    except requests.exceptions.HTTPError as e:
        return {
            "success": False,
            "error": "http_error",
            "status_code": e.response.status_code,
            "message": str(e),
            "body": e.response.text[:500],
        }
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": "unknown", "message": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("HTTP Requests Demo")
    print("=" * 60)

    # Simple GET
    print("\n--- Simple GET ---")
    result = safe_request("https://httpbin.org/json")
    if result["success"]:
        print(f"  Status: {result['status_code']}")
        print(f"  Data keys: {list(result['data'].keys())}")
    else:
        print(f"  Error: {result['message']}")

    # POST with JSON
    print("\n--- POST ---")
    result = safe_request(
        "https://httpbin.org/post",
        method="POST",
        json={"name": "test", "value": 42}
    )
    if result["success"]:
        print(f"  Echoed data: {result['data'].get('json')}")

    # Error handling
    print("\n--- Error Handling ---")
    result = safe_request("https://httpbin.org/status/404")
    print(f"  404 response: success={result['success']}, error={result.get('error')}")

    print("\nDone! See function docstrings for more patterns.")
