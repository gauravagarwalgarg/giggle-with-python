"""
Web Scraping with BeautifulSoup and requests.

Practical patterns for extracting data from web pages.
Always respect robots.txt and rate-limit your requests.

Adapted from code_snippets/BeautifulSoup.
"""
import csv
import time
from typing import Generator
from dataclasses import dataclass, field

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install dependencies: pip install requests beautifulsoup4 lxml")
    raise


# =============================================================================
# BASIC SCRAPING fetch and parse HTML
# =============================================================================

def fetch_page(url: str, timeout: int = 10) -> BeautifulSoup:
    """Fetch a URL and return a parsed BeautifulSoup object.

    Uses lxml parser for speed. Falls back to html.parser if lxml unavailable.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; PythonScraper/1.0)"
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    try:
        return BeautifulSoup(response.text, "lxml")
    except Exception:
        return BeautifulSoup(response.text, "html.parser")


def extract_links(soup: BeautifulSoup, base_url: str = "") -> list[dict]:
    """Extract all links from a page."""
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        # Convert relative URLs to absolute
        if href.startswith("/"):
            href = base_url.rstrip("/") + href
        links.append({
            "text": a_tag.get_text(strip=True),
            "url": href,
        })
    return links


def extract_table(soup: BeautifulSoup, table_index: int = 0) -> list[dict]:
    """Extract an HTML table into a list of dicts.

    Uses the first row as headers.
    """
    tables = soup.find_all("table")
    if table_index >= len(tables):
        return []

    table = tables[table_index]
    rows = table.find_all("tr")

    if not rows:
        return []

    # Get headers from first row
    headers = [th.get_text(strip=True) for th in rows[0].find_all(["th", "td"])]

    # Parse data rows
    data = []
    for row in rows[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if cells:
            data.append(dict(zip(headers, cells)))

    return data


# =============================================================================
# SCRAPING PATTERNS
# =============================================================================

@dataclass
class Article:
    """Represents a scraped article."""
    title: str
    summary: str
    url: str
    tags: list[str] = field(default_factory=list)


def scrape_articles(soup: BeautifulSoup) -> list[Article]:
    """Extract articles from a blog page.

    Adapted from code_snippets/BeautifulSoup/scrape.py.
    Adjust selectors for your target site.
    """
    articles = []

    for article_tag in soup.find_all("article"):
        # Extract title
        title_tag = article_tag.find(["h1", "h2", "h3"])
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"

        # Extract summary
        summary_tag = article_tag.find("p")
        summary = summary_tag.get_text(strip=True) if summary_tag else ""

        # Extract link
        link_tag = article_tag.find("a", href=True)
        url = link_tag["href"] if link_tag else ""

        # Extract tags/categories
        tag_elements = article_tag.find_all("span", class_="tag")
        tags = [t.get_text(strip=True) for t in tag_elements]

        articles.append(Article(
            title=title,
            summary=summary[:200],
            url=url,
            tags=tags,
        ))

    return articles


def extract_video_links(soup: BeautifulSoup) -> list[str]:
    """Extract YouTube video links from embedded iframes.

    Adapted from code_snippets/BeautifulSoup/scrape.py.
    """
    links = []
    for iframe in soup.find_all("iframe"):
        src = iframe.get("src", "")
        if "youtube" in src or "youtu.be" in src:
            # Extract video ID from embed URL
            parts = src.split("/")
            if len(parts) >= 5:
                vid_id = parts[4].split("?")[0]
                links.append(f"https://youtube.com/watch?v={vid_id}")
    return links


# =============================================================================
# PAGINATION handle multi-page results
# =============================================================================

def scrape_paginated(
    base_url: str,
    page_param: str = "page",
    max_pages: int = 10,
    delay: float = 1.0,
) -> Generator[BeautifulSoup, None, None]:
    """Generator that yields parsed pages, following pagination.

    Respects rate limiting with configurable delay between requests.
    """
    for page_num in range(1, max_pages + 1):
        url = f"{base_url}?{page_param}={page_num}"
        try:
            soup = fetch_page(url)
            yield soup
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                break  # No more pages
            raise

        if page_num < max_pages:
            time.sleep(delay)  # Be polite


# =============================================================================
# EXPORT RESULTS save scraped data
# =============================================================================

def save_to_csv(data: list[dict], filename: str, fieldnames: list[str] | None = None):
    """Save scraped data to CSV file.

    Adapted from code_snippets/BeautifulSoup and Python-CSV patterns.
    """
    if not data:
        return

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} records to {filename}")


def save_to_json(data: list[dict], filename: str):
    """Save scraped data to JSON file."""
    import json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} records to {filename}")


# =============================================================================
# ROBUST SCRAPING with retries and error handling
# =============================================================================

def scrape_with_retry(
    url: str,
    max_retries: int = 3,
    backoff: float = 2.0,
) -> BeautifulSoup | None:
    """Fetch a page with exponential backoff retry."""
    for attempt in range(1, max_retries + 1):
        try:
            return fetch_page(url)
        except requests.RequestException as e:
            if attempt == max_retries:
                print(f"Failed after {max_retries} attempts: {e}")
                return None
            wait = backoff ** attempt
            print(f"Attempt {attempt} failed, retrying in {wait}s...")
            time.sleep(wait)
    return None


# =============================================================================
# CSS SELECTORS more concise element selection
# =============================================================================

def css_selector_examples(soup: BeautifulSoup):
    """Demonstrate CSS selector syntax vs find/find_all.

    soup.select() uses CSS selector syntax which is often more concise.
    """
    # By class
    items = soup.select(".product-item")

    # By ID
    header = soup.select_one("#main-header")

    # Nested selector
    nav_links = soup.select("nav > ul > li > a")

    # Attribute selector
    external_links = soup.select('a[target="_blank"]')

    # Multiple classes
    featured = soup.select(".product.featured")

    # nth-child
    even_rows = soup.select("tr:nth-child(even)")

    return items, header, nav_links, external_links, featured, even_rows


if __name__ == "__main__":
    print("=" * 60)
    print("Web Scraping Demo")
    print("=" * 60)

    # Parse a local HTML snippet
    html = """
    <html>
    <body>
        <h1>Example Page</h1>
        <article>
            <h2><a href="/post/1">First Post</a></h2>
            <p>This is the first article summary.</p>
        </article>
        <article>
            <h2><a href="/post/2">Second Post</a></h2>
            <p>This is the second article summary.</p>
        </article>
        <table>
            <tr><th>Name</th><th>Age</th><th>City</th></tr>
            <tr><td>Alice</td><td>30</td><td>NYC</td></tr>
            <tr><td>Bob</td><td>25</td><td>LA</td></tr>
        </table>
        <a href="https://example.com">External</a>
        <a href="/about">About</a>
    </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")

    # Extract articles
    print("\n--- Articles ---")
    articles = scrape_articles(soup)
    for article in articles:
        print(f"  {article.title}: {article.summary}")

    # Extract table
    print("\n--- Table Data ---")
    table_data = extract_table(soup)
    for row in table_data:
        print(f"  {row}")

    # Extract links
    print("\n--- Links ---")
    links = extract_links(soup, base_url="https://example.com")
    for link in links:
        print(f"  {link['text']}: {link['url']}")

    print("\n--- Notes ---")
    print("  Install: pip install requests beautifulsoup4 lxml")
    print("  Always check robots.txt before scraping")
    print("  Use time.sleep() between requests to be polite")
