"""
Regex Patterns common regex for email, IP, URL, phone, dates.

Regular expressions are powerful but cryptic. This file provides
tested, copy-paste ready patterns for everyday validation.
"""
import re
from typing import Match


# =============================================================================
# EMAIL VALIDATION
# =============================================================================

# Simple email (covers 99% of valid emails)
EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

def is_valid_email(email: str) -> bool:
    """Validate email format (simple but practical)."""
    return bool(EMAIL_PATTERN.match(email))


# =============================================================================
# IP ADDRESSES
# =============================================================================

# IPv4
IPV4_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)

# IPv4 with CIDR notation
IPV4_CIDR_PATTERN = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)/(?:3[0-2]|[12]?\d)$"
)

def is_valid_ipv4(ip: str) -> bool:
    """Validate IPv4 address."""
    return bool(IPV4_PATTERN.match(ip))


# =============================================================================
# URLs
# =============================================================================

URL_PATTERN = re.compile(
    r"^https?://"                   # http:// or https://
    r"(?:[\w-]+\.)+[a-zA-Z]{2,}"   # Domain
    r"(?::\d{1,5})?"               # Optional port
    r"(?:/[^\s]*)?$"               # Optional path
)

# Extract URLs from text
URL_EXTRACT_PATTERN = re.compile(
    r"https?://(?:[\w-]+\.)+[a-zA-Z]{2,}(?::\d+)?(?:/[^\s\)\]\"'<>]*)?"
)

def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    return bool(URL_PATTERN.match(url))


def extract_urls(text: str) -> list[str]:
    """Extract all URLs from text."""
    return URL_EXTRACT_PATTERN.findall(text)


# =============================================================================
# PHONE NUMBERS
# =============================================================================

# Indian phone number
INDIA_PHONE_PATTERN = re.compile(
    r"^(?:\+91[\-\s]?)?[6-9]\d{9}$"
)

# US phone number
US_PHONE_PATTERN = re.compile(
    r"^(?:\+1[\-\s]?)?\(?[2-9]\d{2}\)?[\-\s]?\d{3}[\-\s]?\d{4}$"
)

# Generic international (E.164 format)
E164_PATTERN = re.compile(
    r"^\+[1-9]\d{1,14}$"
)

def is_valid_phone_india(phone: str) -> bool:
    """Validate Indian phone number."""
    cleaned = phone.replace(" ", "").replace("-", "")
    return bool(INDIA_PHONE_PATTERN.match(cleaned))


# =============================================================================
# DATES
# =============================================================================

# ISO date: 2024-06-15
ISO_DATE_PATTERN = re.compile(
    r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"
)

# DD/MM/YYYY or DD-MM-YYYY
DMY_DATE_PATTERN = re.compile(
    r"^(?:0[1-9]|[12]\d|3[01])[/\-](?:0[1-9]|1[0-2])[/\-]\d{4}$"
)

# Datetime: 2024-06-15T10:30:00 or 2024-06-15 10:30:00
DATETIME_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$"
)


# =============================================================================
# PASSWORDS / SECURITY
# =============================================================================

def validate_password(password: str, min_length: int = 8) -> dict[str, bool]:
    """Check password strength against common rules."""
    return {
        "min_length": len(password) >= min_length,
        "has_uppercase": bool(re.search(r"[A-Z]", password)),
        "has_lowercase": bool(re.search(r"[a-z]", password)),
        "has_digit": bool(re.search(r"\d", password)),
        "has_special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
        "no_spaces": " " not in password,
    }


# =============================================================================
# DATA EXTRACTION
# =============================================================================

# Extract hashtags
HASHTAG_PATTERN = re.compile(r"#(\w+)")

# Extract mentions (@username)
MENTION_PATTERN = re.compile(r"@([\w.]+)")

# Extract numbers (int and float)
NUMBER_PATTERN = re.compile(r"-?\d+\.?\d*")

# Extract quoted strings
QUOTED_PATTERN = re.compile(r'"([^"]*)"')

# Extract key=value pairs
KEY_VALUE_PATTERN = re.compile(r"(\w+)=([\w\"'][^,\s]*)")


def extract_hashtags(text: str) -> list[str]:
    return HASHTAG_PATTERN.findall(text)


def extract_mentions(text: str) -> list[str]:
    return MENTION_PATTERN.findall(text)


def extract_numbers(text: str) -> list[float]:
    return [float(n) for n in NUMBER_PATTERN.findall(text)]


# =============================================================================
# TEXT CLEANING
# =============================================================================

def clean_whitespace(text: str) -> str:
    """Normalize whitespace multiple spaces/tabs → single space."""
    return re.sub(r"\s+", " ", text).strip()


def remove_html_tags(html: str) -> str:
    """Strip HTML tags from string."""
    return re.sub(r"<[^>]+>", "", html)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug.

    "Hello World! 123" → "hello-world-123"
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)  # Remove non-alphanumeric
    text = re.sub(r"[\s_]+", "-", text)   # Spaces/underscores → hyphens
    text = re.sub(r"-+", "-", text)       # Multiple hyphens → single
    return text.strip("-")


def mask_sensitive(text: str) -> str:
    """Mask credit card numbers and SSNs in text."""
    # Credit card: keep last 4 digits
    text = re.sub(
        r"\b(\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?)(\d{4})\b",
        r"****-****-****-\2",
        text
    )
    # Email: mask local part
    text = re.sub(
        r"\b([\w.]{2})([\w.]*?)(@[\w.]+)\b",
        lambda m: m.group(1) + "*" * len(m.group(2)) + m.group(3),
        text
    )
    return text


# =============================================================================
# LOG PARSING
# =============================================================================

# Apache/Nginx access log
ACCESS_LOG_PATTERN = re.compile(
    r'(?P<ip>[\d.]+)\s-\s-\s'
    r'\[(?P<timestamp>[^\]]+)\]\s'
    r'"(?P<method>\w+)\s(?P<path>[^\s]+)\s(?P<protocol>[^"]+)"\s'
    r'(?P<status>\d+)\s(?P<size>\d+)'
)

def parse_access_log(line: str) -> dict | None:
    """Parse a single Apache/Nginx access log line."""
    match = ACCESS_LOG_PATTERN.match(line)
    if not match:
        return None
    return match.groupdict()


# =============================================================================
# NAMED GROUPS AND SUBSTITUTION
# =============================================================================

def reformat_date(text: str, from_format: str = "us", to_format: str = "iso") -> str:
    """Convert date formats in text using regex.

    US (MM/DD/YYYY) → ISO (YYYY-MM-DD)
    """
    if from_format == "us" and to_format == "iso":
        return re.sub(
            r"(\d{2})/(\d{2})/(\d{4})",
            r"\3-\1-\2",
            text
        )
    return text


if __name__ == "__main__":
    print("=" * 60)
    print("Regex Patterns Demo")
    print("=" * 60)

    # Email
    print("\n--- Email Validation ---")
    emails = ["user@example.com", "invalid@", "a.b+c@domain.co.in", "no spaces@x.com"]
    for email in emails:
        print(f"  {email:30} → {'✓' if is_valid_email(email) else '✗'}")

    # IP
    print("\n--- IP Validation ---")
    ips = ["192.168.1.1", "256.1.1.1", "10.0.0.1", "999.999.999.999"]
    for ip in ips:
        print(f"  {ip:20} → {'✓' if is_valid_ipv4(ip) else '✗'}")

    # URL extraction
    print("\n--- URL Extraction ---")
    text = "Visit https://example.com/page and http://api.dev:8080/v2/users for more"
    urls = extract_urls(text)
    for url in urls:
        print(f"  {url}")

    # Phone
    print("\n--- Phone (India) ---")
    phones = ["+91 9876543210", "9876543210", "+91-98765-43210", "1234567890"]
    for phone in phones:
        print(f"  {phone:20} → {'✓' if is_valid_phone_india(phone) else '✗'}")

    # Password
    print("\n--- Password Validation ---")
    checks = validate_password("MyP@ss123")
    for rule, passed in checks.items():
        print(f"  {rule:15} → {'✓' if passed else '✗'}")

    # Text cleaning
    print("\n--- Text Operations ---")
    print(f"  slugify: '{slugify('Hello World! 2024')}'")
    print(f"  clean:   '{clean_whitespace('  too   many   spaces  ')}'")
    print(f"  no html: '{remove_html_tags('<p>Hello <b>World</b></p>')}'")

    # Data extraction
    print("\n--- Data Extraction ---")
    social = "Check out #python and #coding! CC @gaurav.dev @alice"
    print(f"  Hashtags: {extract_hashtags(social)}")
    print(f"  Mentions: {extract_mentions(social)}")
    print(f"  Numbers: {extract_numbers('Price: $42.50, Qty: 3, Discount: -5.5%')}")
