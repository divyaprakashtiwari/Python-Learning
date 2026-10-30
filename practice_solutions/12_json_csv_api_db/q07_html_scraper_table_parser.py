"""
Question 7: Standard Library HTML Scraping & Table Extraction Engine
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- Subclassing html.parser.HTMLParser for structured HTML document processing
- Entity decoding via html.unescape and filtering out <script> and <style> blocks
- Structured <table> extraction, capturing <th> headers and <tr>/<td> row data
- Anchor link crawling and relative URL resolution via urllib.parse.urljoin
- Human-readable text sanitization with whitespace normalization
"""

import html
import json
import urllib.parse
from html.parser import HTMLParser
from typing import List, Dict, Any, Optional


class TableAndLinkParser(HTMLParser):
    """
    SAX-style HTML parser extracting tables, links, and readable plain text.
    """

    def __init__(self, base_url: str = "") -> None:
        super().__init__()
        self.base_url = base_url

        # State tracking
        self._ignored_depth = 0
        self._in_table = False
        self._in_tr = False
        self._in_th = False
        self._in_td = False
        self._in_a = False

        # Current element accumulation
        self._current_cell_text: List[str] = []
        self._current_link_text: List[str] = []
        self._current_href: Optional[str] = None
        self._current_row_headers: List[str] = []
        self._current_row_cells: List[str] = []
        self._current_table_headers: List[str] = []
        self._current_table_rows: List[Dict[str, str]] = []

        # Collected results
        self.tables: List[List[Dict[str, str]]] = []
        self.links: List[Dict[str, str]] = []
        self.text_tokens: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        tag_lower = tag.lower()
        attr_dict = {k.lower(): v for k, v in attrs}

        if tag_lower in ("script", "style"):
            self._ignored_depth += 1
            return

        if self._ignored_depth > 0:
            return

        if tag_lower == "table":
            self._in_table = True
            self._current_table_headers = []
            self._current_table_rows = []

        elif tag_lower == "tr" and self._in_table:
            self._in_tr = True
            self._current_row_headers = []
            self._current_row_cells = []

        elif tag_lower == "th" and self._in_tr:
            self._in_th = True
            self._current_cell_text = []

        elif tag_lower == "td" and self._in_tr:
            self._in_td = True
            self._current_cell_text = []

        elif tag_lower == "a":
            href = attr_dict.get("href")
            if href and not href.startswith("javascript:") and not href.startswith("#"):
                self._in_a = True
                self._current_href = href
                self._current_link_text = []

    def handle_endtag(self, tag: str) -> None:
        tag_lower = tag.lower()

        if tag_lower in ("script", "style"):
            self._ignored_depth = max(0, self._ignored_depth - 1)
            return

        if self._ignored_depth > 0:
            return

        if tag_lower == "th" and self._in_th:
            self._in_th = False
            cell_val = html.unescape("".join(self._current_cell_text)).strip()
            self._current_row_headers.append(cell_val)

        elif tag_lower == "td" and self._in_td:
            self._in_td = False
            cell_val = html.unescape("".join(self._current_cell_text)).strip()
            self._current_row_cells.append(cell_val)

        elif tag_lower == "tr" and self._in_tr:
            self._in_tr = False
            if self._current_row_headers and not self._current_table_headers:
                self._current_table_headers = list(self._current_row_headers)
            elif self._current_row_cells:
                # Build row dictionary
                row_dict: Dict[str, str] = {}
                headers = self._current_table_headers
                for idx, cell_val in enumerate(self._current_row_cells):
                    col_name = headers[idx] if idx < len(headers) and headers[idx] else f"col_{idx}"
                    row_dict[col_name] = cell_val
                self._current_table_rows.append(row_dict)

        elif tag_lower == "table" and self._in_table:
            self._in_table = False
            if self._current_table_rows:
                self.tables.append(self._current_table_rows)

        elif tag_lower == "a" and self._in_a:
            self._in_a = False
            link_text = html.unescape("".join(self._current_link_text)).strip()
            if self._current_href:
                absolute_url = urllib.parse.urljoin(self.base_url, self._current_href)
                self.links.append({"text": link_text, "url": absolute_url})
            self._current_href = None

    def handle_data(self, data: str) -> None:
        if self._ignored_depth > 0:
            return

        unescaped_data = html.unescape(data)
        if self._in_th or self._in_td:
            self._current_cell_text.append(unescaped_data)

        if self._in_a:
            self._current_link_text.append(unescaped_data)

        stripped = unescaped_data.strip()
        if stripped:
            self.text_tokens.append(stripped)


class HTMLDataScraper:
    """
    High-level scraper interface using TableAndLinkParser.
    """

    @staticmethod
    def extract_tables(html_content: str) -> List[List[Dict[str, str]]]:
        """Extracts structured table rows from HTML."""
        parser = TableAndLinkParser()
        parser.feed(html_content)
        return parser.tables

    @staticmethod
    def extract_links(html_content: str, base_url: str = "") -> List[Dict[str, str]]:
        """Extracts anchor links resolving relative URLs to absolute."""
        parser = TableAndLinkParser(base_url=base_url)
        parser.feed(html_content)
        return parser.links

    @staticmethod
    def get_text_content(html_content: str) -> str:
        """Extracts human-readable plain text without scripts/styles."""
        parser = TableAndLinkParser()
        parser.feed(html_content)
        return " ".join(parser.text_tokens)


if __name__ == "__main__":
    html_sample = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample Financial Report</title>
    <style>body { font-family: Arial; }</style>
</head>
<body>
    <h1>Q3 Quarterly Performance &amp; Metrics</h1>
    <p>Please review our official <a href="/reports/q3.pdf">PDF Documentation</a> or visit <a href="https://partner.com">Partner Portal</a>.</p>
    
    <table id="financials">
        <tr>
            <th>Quarter</th>
            <th>Revenue</th>
            <th>Profit</th>
        </tr>
        <tr>
            <td>Q1 2026</td>
            <td>$1,200,000</td>
            <td>$350,000</td>
        </tr>
        <tr>
            <td>Q2 2026</td>
            <td>$1,450,000</td>
            <td>$420,000</td>
        </tr>
    </table>
</body>
</html>
"""

    scraper = HTMLDataScraper()

    print("=== 1. Structured Table Extraction ===")
    tables = scraper.extract_tables(html_sample)
    print(f"Extracted Tables Count: {len(tables)}")
    print(f"Table 0 Rows:\n{json.dumps(tables[0], indent=2)}")

    print("\n=== 2. Link Extraction with URL Resolution ===")
    links = scraper.extract_links(html_sample, base_url="https://company.example.com/investors/")
    print(f"Extracted Links:\n{json.dumps(links, indent=2)}")

    print("\n=== 3. Sanitized Text Content ===")
    clean_text = scraper.get_text_content(html_sample)
    print(f"Plain Text:\n{clean_text}")
    print(f"Sanitized Plain Text Contains 'Q3 Quarterly Performance & Metrics': {'Q3 Quarterly Performance & Metrics' in clean_text}")
