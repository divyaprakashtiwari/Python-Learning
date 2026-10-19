"""
Topic 12: JSON, CSV, API, Database
Question 07: Web Scraping Basics (urllib)

A comprehensive, production-grade guide to web scraping and HTML parsing using Python's
standard library (urllib.request, html.parser.HTMLParser, urllib.robotparser, urllib.parse).
Covers tag extraction, relative link resolution, HTML table parsing, robots.txt compliance,
rate-limiting, HTML entity unescaping, pagination crawling, Open Graph metadata extraction,
and an architectural standard-library scraping engine.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import html
from html.parser import HTMLParser
import time
import urllib.parse
import urllib.robotparser
from typing import List, Dict, Any, Optional, Set, Tuple


# =====================================================================
# Q1: Tag and Text Extraction with html.parser.HTMLParser
# =====================================================================
class HeadingAndTitleParser(HTMLParser):
    """Extracts the <title> tag and all heading tags (h1-h6) with their text content."""
    def __init__(self):
        super().__init__()
        self.title: Optional[str] = None
        self.headings: List[Dict[str, str]] = []
        self._current_tag: Optional[str] = None
        self._text_accumulator: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag in ("title", "h1", "h2", "h3", "h4", "h5", "h6"):
            self._current_tag = tag
            self._text_accumulator = []

    def handle_endtag(self, tag: str):
        if tag == self._current_tag:
            content = "".join(self._text_accumulator).strip()
            if tag == "title":
                self.title = content
            else:
                self.headings.append({"tag": tag, "text": content})
            self._current_tag = None
            self._text_accumulator = []

    def handle_data(self, data: str):
        if self._current_tag:
            self._text_accumulator.append(data)


def q1_html_tag_and_text_extraction():
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Python Learning Portal</title></head>
    <body>
        <h1>Main Curriculum</h1>
        <p>Introduction to Python.</p>
        <h2>Module 1: Basics</h2>
        <h3>Variables and Types</h3>
        <h2>Module 2: Advanced</h2>
    </body>
    </html>
    """
    parser = HeadingAndTitleParser()
    parser.feed(sample_html)

    assert parser.title == "Python Learning Portal"
    assert len(parser.headings) == 4
    assert parser.headings[0] == {"tag": "h1", "text": "Main Curriculum"}
    assert parser.headings[1] == {"tag": "h2", "text": "Module 1: Basics"}
    assert parser.headings[2] == {"tag": "h3", "text": "Variables and Types"}
    assert parser.headings[3] == {"tag": "h2", "text": "Module 2: Advanced"}

    print("=== Q1: Tag & Heading Extraction Verified ===")


# =====================================================================
# Q2: Link Extraction and Canonical URL Resolution
# =====================================================================
class LinkExtractor(HTMLParser):
    """Extracts all anchor href links, converting relative URLs to absolute URLs."""
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: List[Dict[str, Any]] = []
        self._current_href: Optional[str] = None
        self._text_parts: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            raw_href = attrs_dict.get("href")
            if raw_href:
                self._current_href = raw_href
                self._text_parts = []

    def handle_endtag(self, tag: str):
        if tag == "a" and self._current_href:
            anchor_text = "".join(self._text_parts).strip()
            absolute_url = urllib.parse.urljoin(self.base_url, self._current_href)
            is_internal = urllib.parse.urlsplit(absolute_url).netloc == urllib.parse.urlsplit(self.base_url).netloc

            self.links.append({
                "raw_href": self._current_href,
                "absolute_url": absolute_url,
                "text": anchor_text,
                "is_internal": is_internal
            })
            self._current_href = None
            self._text_parts = []

    def handle_data(self, data: str):
        if self._current_href:
            self._text_parts.append(data)


def q2_link_extraction_and_url_resolution():
    base = "https://docs.python.org/3/library/"
    html_markup = """
    <div>
        <a href="urllib.html">Urllib Library</a>
        <a href="/3/tutorial/index.html">Tutorial</a>
        <a href="../reference/index.html">Language Reference</a>
        <a href="https://pypi.org/project/requests/">Requests on PyPI</a>
    </div>
    """
    extractor = LinkExtractor(base)
    extractor.feed(html_markup)

    links = extractor.links
    assert len(links) == 4

    # Relative to current folder
    assert links[0]["absolute_url"] == "https://docs.python.org/3/library/urllib.html"
    assert links[0]["text"] == "Urllib Library"
    assert links[0]["is_internal"] is True

    # Root-relative
    assert links[1]["absolute_url"] == "https://docs.python.org/3/tutorial/index.html"
    assert links[1]["is_internal"] is True

    # Directory parent relative (..)
    assert links[2]["absolute_url"] == "https://docs.python.org/3/reference/index.html"
    assert links[2]["is_internal"] is True

    # External
    assert links[3]["absolute_url"] == "https://pypi.org/project/requests/"
    assert links[3]["is_internal"] is False

    print("=== Q2: Link Extraction & Canonical Resolution Verified ===")


# =====================================================================
# Q3: Media and Image Extraction with Attribute Normalization
# =====================================================================
class ImageExtractor(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.images: List[Dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs):
        if tag == "img":
            attr_dict = dict(attrs)
            src = attr_dict.get("src", "")
            if src:
                abs_src = urllib.parse.urljoin(self.base_url, src)
                self.images.append({
                    "src": abs_src,
                    "alt": attr_dict.get("alt", ""),
                    "width": attr_dict.get("width", "auto"),
                    "height": attr_dict.get("height", "auto")
                })


def q3_media_image_extraction():
    base = "https://example.com/blog/"
    html_sample = """
    <article>
        <img src="images/banner.png" alt="Hero Banner" width="1200" height="400">
        <img src="/static/logo.svg" alt="Site Logo">
        <img src="https://cdn.example.org/photo.jpg">
    </article>
    """
    extractor = ImageExtractor(base)
    extractor.feed(html_sample)

    imgs = extractor.images
    assert len(imgs) == 3
    assert imgs[0]["src"] == "https://example.com/blog/images/banner.png"
    assert imgs[0]["alt"] == "Hero Banner"
    assert imgs[0]["width"] == "1200"

    assert imgs[1]["src"] == "https://example.com/static/logo.svg"
    assert imgs[1]["alt"] == "Site Logo"

    assert imgs[2]["src"] == "https://cdn.example.org/photo.jpg"
    assert imgs[2]["alt"] == ""

    print("=== Q3: Image & Media Extraction Verified ===")


# =====================================================================
# Q4: Parsing Nested HTML Tables to Structured Dictionaries
# =====================================================================
class HTMLTableParser(HTMLParser):
    """Extracts tabular <table> structures into rows of dictionaries based on <th> headers."""
    def __init__(self):
        super().__init__()
        self.tables: List[List[Dict[str, str]]] = []
        self._in_table = False
        self._current_table_headers: List[str] = []
        self._current_row: List[str] = []
        self._current_table_rows: List[List[str]] = []
        self._cell_text: List[str] = []
        self._in_header = False

    def handle_starttag(self, tag: str, attrs):
        if tag == "table":
            self._in_table = True
            self._current_table_headers = []
            self._current_table_rows = []
        elif tag == "th":
            self._in_header = True
            self._cell_text = []
        elif tag == "td":
            self._cell_text = []
        elif tag == "tr":
            self._current_row = []

    def handle_endtag(self, tag: str):
        if tag == "th":
            self._current_table_headers.append("".join(self._cell_text).strip())
            self._in_header = False
        elif tag == "td":
            self._current_row.append("".join(self._cell_text).strip())
        elif tag == "tr":
            if self._current_row:
                self._current_table_rows.append(self._current_row)
        elif tag == "table":
            # Map headers to rows
            table_dict_list = []
            for r in self._current_table_rows:
                row_dict = {}
                for idx, col_name in enumerate(self._current_table_headers):
                    val = r[idx] if idx < len(r) else ""
                    row_dict[col_name] = val
                table_dict_list.append(row_dict)
            self.tables.append(table_dict_list)
            self._in_table = False

    def handle_data(self, data: str):
        if self._in_table:
            self._cell_text.append(data)


def q4_html_table_parsing():
    html_markup = """
    <table id="rankings">
        <thead>
            <tr><th>Rank</th><th>Language</th><th>Share</th></tr>
        </thead>
        <tbody>
            <tr><td>1</td><td>Python</td><td>28.5%</td></tr>
            <tr><td>2</td><td>JavaScript</td><td>18.2%</td></tr>
            <tr><td>3</td><td>Java</td><td>15.4%</td></tr>
        </tbody>
    </table>
    """
    parser = HTMLTableParser()
    parser.feed(html_markup)

    assert len(parser.tables) == 1
    table = parser.tables[0]
    assert len(table) == 3
    assert table[0] == {"Rank": "1", "Language": "Python", "Share": "28.5%"}
    assert table[1] == {"Rank": "2", "Language": "JavaScript", "Share": "18.2%"}
    assert table[2] == {"Rank": "3", "Language": "Java", "Share": "15.4%"}

    print("=== Q4: HTML Table Parsing Verified ===")


# =====================================================================
# Q5: Robots.txt Politeness and Path Authorization
# =====================================================================
def verify_robots_txt(robots_content: str, user_agent: str, target_url: str) -> bool:
    """Uses urllib.robotparser.RobotFileParser to verify crawl permissions."""
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(robots_content.splitlines())
    return rp.can_fetch(user_agent, target_url)


def q5_robots_txt_politeness():
    robots_data = """
    User-agent: Googlebot
    Disallow: /private/

    User-agent: AgyBot
    Disallow: /admin/
    Disallow: /api/secret/
    Crawl-delay: 5

    User-agent: *
    Disallow: /restricted/
    """

    # AgyBot permissions
    assert verify_robots_txt(robots_data, "AgyBot", "https://example.com/blog") is True
    assert verify_robots_txt(robots_data, "AgyBot", "https://example.com/admin/settings") is False
    assert verify_robots_txt(robots_data, "AgyBot", "https://example.com/api/secret/token") is False

    # Default crawler permissions
    assert verify_robots_txt(robots_data, "GenericBot", "https://example.com/admin/dashboard") is True
    assert verify_robots_txt(robots_data, "GenericBot", "https://example.com/restricted/page") is False

    print("=== Q5: Robots.txt Politeness Engine Verified ===")


# =====================================================================
# Q6: Per-Domain Rate-Limiting & Throttler
# =====================================================================
class DomainRateLimiter:
    """Enforces minimum time intervals between requests targeting the same domain."""
    def __init__(self, delay_seconds: float = 0.05):
        self.delay = delay_seconds
        self.last_access: Dict[str, float] = {}

    def throttle(self, url: str) -> float:
        """Blocks if necessary and returns the time slept."""
        netloc = urllib.parse.urlsplit(url).netloc
        now = time.time()
        last = self.last_access.get(netloc, 0.0)
        elapsed = now - last
        slept = 0.0

        if elapsed < self.delay:
            wait_time = self.delay - elapsed
            time.sleep(wait_time)
            slept = wait_time

        self.last_access[netloc] = time.time()
        return slept


def q6_domain_rate_limiting():
    limiter = DomainRateLimiter(delay_seconds=0.04)

    # First access to domain A: no wait
    w1 = limiter.throttle("https://site-a.com/page1")
    assert w1 == 0.0

    # Immediate second access to domain A: throttled
    w2 = limiter.throttle("https://site-a.com/page2")
    assert w2 > 0.0

    # Access to different domain B: no wait
    w3 = limiter.throttle("https://site-b.com/page1")
    assert w3 == 0.0

    print("=== Q6: Domain Rate Limiting & Throttling Verified ===")


# =====================================================================
# Q7: Entity Unescaping and Text Sanitization
# =====================================================================
class TextStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text_chunks: List[str] = []

    def handle_data(self, data: str):
        self.text_chunks.append(data)


def clean_html_to_plaintext(raw_html: str) -> str:
    """Strips all HTML tags and resolves character entities to clean unicode text."""
    # 1. Unescape HTML entities first (&amp;, &lt;, &quot;, &#39;)
    unescaped = html.unescape(raw_html)
    # 2. Extract text chunks via HTMLParser
    stripper = TextStripper()
    stripper.feed(unescaped)
    raw_text = " ".join("".join(stripper.text_chunks).split())
    return raw_text


def q7_entity_unescaping_and_text_sanitization():
    dirty_html = """
    <div class="content">
        <p>Ben &amp; Jerry&#39;s &quot;Ice Cream&quot; is &gt; average!</p>
        <script>alert('malicious')</script>
        <span>Price: &euro;4.50</span>
    </div>
    """
    clean_text = clean_html_to_plaintext(dirty_html)

    assert "Ben & Jerry's" in clean_text
    assert '"Ice Cream"' in clean_text
    assert "> average!" in clean_text
    assert "Price: €4.50" in clean_text
    assert "<p>" not in clean_text
    assert "<script>" not in clean_text

    print("=== Q7: Entity Unescaping & Markup Stripping Verified ===")


# =====================================================================
# Q8: Pagination and Breadth-First Crawling Simulator
# =====================================================================
def crawl_pagination_simulation(
    mock_pages: Dict[str, str],
    start_url: str,
    max_pages: int = 5
) -> List[str]:
    """Simulates BFS pagination crawling, visiting next links up to max_pages."""
    visited: Set[str] = set()
    queue: List[str] = [start_url]
    crawl_order: List[str] = []

    while queue and len(visited) < max_pages:
        current_url = queue.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)
        crawl_order.append(current_url)

        # Extract links from page
        page_html = mock_pages.get(current_url, "")
        extractor = LinkExtractor(current_url)
        extractor.feed(page_html)

        for link in extractor.links:
            target = link["absolute_url"]
            if target not in visited and target in mock_pages:
                queue.append(target)

    return crawl_order


def q8_pagination_breadth_first_crawler():
    mock_web = {
        "https://blog.test/page/1": '<a href="/page/2">Next</a>',
        "https://blog.test/page/2": '<a href="/page/3">Next</a> <a href="/page/1">Prev</a>',
        "https://blog.test/page/3": '<a href="/page/4">Next</a>',
        "https://blog.test/page/4": '<a href="/page/5">Next</a>',
        "https://blog.test/page/5": '<a href="/page/6">Next</a>',
        "https://blog.test/page/6": '<span>End of pages</span>'
    }

    crawled = crawl_pagination_simulation(mock_web, "https://blog.test/page/1", max_pages=3)
    assert crawled == [
        "https://blog.test/page/1",
        "https://blog.test/page/2",
        "https://blog.test/page/3"
    ]

    print("=== Q8: Pagination & BFS Crawling Simulator Verified ===")


# =====================================================================
# Q9: Open Graph and Metadata Tag Extraction
# =====================================================================
class MetadataParser(HTMLParser):
    """Extracts standard meta tags (description, author) and Open Graph tags (og:title, etc)."""
    def __init__(self):
        super().__init__()
        self.metadata: Dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs):
        if tag == "meta":
            attrs_dict = dict(attrs)
            key = attrs_dict.get("name") or attrs_dict.get("property")
            content = attrs_dict.get("content")
            if key and content:
                self.metadata[key.lower()] = content


def q9_opengraph_metadata_extraction():
    sample_head = """
    <head>
        <meta name="description" content="Master standard Python web scraping.">
        <meta name="author" content="Divya Prakash Tiwari">
        <meta property="og:title" content="Python Web Scraping Fundamentals">
        <meta property="og:description" content="No third-party packages needed.">
        <meta property="og:image" content="https://example.com/banner.png">
        <meta property="og:type" content="article">
    </head>
    """
    parser = MetadataParser()
    parser.feed(sample_head)

    meta = parser.metadata
    assert meta["description"] == "Master standard Python web scraping."
    assert meta["author"] == "Divya Prakash Tiwari"
    assert meta["og:title"] == "Python Web Scraping Fundamentals"
    assert meta["og:image"] == "https://example.com/banner.png"
    assert meta["og:type"] == "article"

    print("=== Q9: Open Graph & Metadata Extraction Verified ===")


# =====================================================================
# Q10: Architectural Standard-Library Web Scraper Engine
# =====================================================================
class ScrapeResult:
    def __init__(self, url: str, title: str, metadata: Dict[str, str], links: List[str], tables: List[List[Dict[str, str]]]):
        self.url = url
        self.title = title
        self.metadata = metadata
        self.links = links
        self.tables = tables

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "metadata": self.metadata,
            "links_count": len(self.links),
            "tables_count": len(self.tables)
        }


class StandardScraper:
    """
    Enterprise-grade HTML scraper engine using only Python standard library.
    Integrates heading extraction, link extraction, table parsing, and metadata scraping.
    """
    def __init__(self, user_agent: str = "AgyScraper/1.0"):
        self.user_agent = user_agent

    def scrape_html(self, html_text: str, base_url: str) -> ScrapeResult:
        # Title and headings
        h_parser = HeadingAndTitleParser()
        h_parser.feed(html_text)
        title = h_parser.title or "Untitled"

        # Metadata
        m_parser = MetadataParser()
        m_parser.feed(html_text)

        # Links
        l_parser = LinkExtractor(base_url)
        l_parser.feed(html_text)
        links = [l["absolute_url"] for l in l_parser.links]

        # Tables
        t_parser = HTMLTableParser()
        t_parser.feed(html_text)

        return ScrapeResult(
            url=base_url,
            title=title,
            metadata=m_parser.metadata,
            links=links,
            tables=t_parser.tables
        )


def q10_architectural_scraper_engine():
    doc = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Engineering Portal</title>
        <meta name="description" content="Technical resources and specs">
        <meta property="og:title" content="Engineering Portal">
    </head>
    <body>
        <h1>Systems Architecture</h1>
        <p>Resource links:</p>
        <a href="/specs/api">API Specifications</a>
        <a href="https://external.io/docs">External Docs</a>

        <table>
            <tr><th>Component</th><th>Status</th></tr>
            <tr><td>Cache Layer</td><td>Active</td></tr>
        </table>
    </body>
    </html>
    """
    scraper = StandardScraper()
    result = scraper.scrape_html(doc, "https://internal.corp/hub/")

    assert result.title == "Engineering Portal"
    assert result.metadata["description"] == "Technical resources and specs"
    assert "https://internal.corp/specs/api" in result.links
    assert "https://external.io/docs" in result.links
    assert len(result.tables) == 1
    assert result.tables[0][0] == {"Component": "Cache Layer", "Status": "Active"}

    d = result.to_dict()
    assert d["links_count"] == 2
    assert d["tables_count"] == 1

    print("=== Q10: Architectural StandardScraper Engine Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_html_tag_and_text_extraction()
    q2_link_extraction_and_url_resolution()
    q3_media_image_extraction()
    q4_html_table_parsing()
    q5_robots_txt_politeness()
    q6_domain_rate_limiting()
    q7_entity_unescaping_and_text_sanitization()
    q8_pagination_breadth_first_crawler()
    q9_opengraph_metadata_extraction()
    q10_architectural_scraper_engine()

    print("\nAll 10 web scraping practice questions passed successfully!")
