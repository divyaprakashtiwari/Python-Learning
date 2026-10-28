r"""
Question 7: Enterprise Log Parsing & PII Redaction Engine
Topic: Advanced Python

Key Concepts Tested:
- Verbose regular expressions with re.VERBOSE and re.MULTILINE
- Named capture groups (?P<name>...) and match.groupdict()
- PII redaction and token masking via re.sub and callable substitution handlers
- Backreferences in replacement templates (\g<name>)
- URL parameter parsing via regex
- IP address octet validation and corrupt entry filtering
"""

import re
from typing import List, Dict, Any


class SecurityLogAnalyzer:
    """
    Enterprise log analysis engine providing regex-based structured log parsing,
    PII redaction, and URL token extraction.
    """

    LOG_PATTERN = re.compile(
        r"""
        ^\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\]\s+
        \[(?P<level>INFO|WARNING|ERROR|CRITICAL)\]\s+
        \[(?P<client_ip>(?:\d{1,3}\.){3}\d{1,3})\]\s+
        User<(?P<username>[\w\-]+)>:\s+
        (?P<message>.*)$
        """,
        re.VERBOSE | re.MULTILINE,
    )

    CC_PATTERN = re.compile(r"\b(?P<c1>\d{4})[- ]?\d{4}[- ]?\d{4}[- ]?(?P<c4>\d{4})\b")
    SSN_PATTERN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
    EMAIL_PATTERN = re.compile(r"\b([a-zA-Z0-9_.+-])([a-zA-Z0-9_.+-]*)([a-zA-Z0-9_.+-])@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)\b")
    QUERY_PARAM_PATTERN = re.compile(r"[?&](?P<key>[^=&#]+)=(?P<val>[^&#]+)")

    @staticmethod
    def _is_valid_ipv4(ip: str) -> bool:
        """Validates that each octet of an IPv4 address is in 0..255."""
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

    def parse_log_dump(self, raw_text: str) -> List[Dict[str, Any]]:
        """
        Extracts structured records from raw log text using named groups.
        Filters out corrupt or invalid entries (e.g. invalid IP addresses).
        """
        records = []
        for match in self.LOG_PATTERN.finditer(raw_text):
            entry = match.groupdict()
            if self._is_valid_ipv4(entry["client_ip"]):
                records.append(entry)
        return records

    def redact_sensitive_data(self, message_text: str) -> str:
        """
        Redacts credit cards, SSNs, and obfuscates email addresses in message text.
        """
        # 1. Mask credit cards: 4111-2222-3333-4444 -> 4111-XXXX-XXXX-4444
        sanitized = self.CC_PATTERN.sub(r"\g<c1>-XXXX-XXXX-\g<c4>", message_text)

        # 2. Redact SSN: 123-45-6789 -> ***-**-****
        sanitized = self.SSN_PATTERN.sub("***-**-****", sanitized)

        # 3. Obfuscate Email: admin@corp.io -> a***n@corp.io
        def mask_email(match: re.Match) -> str:
            first_char = match.group(1)
            last_char = match.group(3)
            domain = match.group(4)
            return f"{first_char}***{last_char}@{domain}"

        sanitized = self.EMAIL_PATTERN.sub(mask_email, sanitized)
        return sanitized

    def extract_query_parameters(self, url: str) -> Dict[str, str]:
        """
        Parses URL query parameters into a key-value dictionary using regex.
        """
        return {
            m.group("key"): m.group("val")
            for m in self.QUERY_PARAM_PATTERN.finditer(url)
        }


if __name__ == "__main__":
    analyzer = SecurityLogAnalyzer()

    sample_logs = """[2026-10-25 14:30:15] [INFO] [192.168.1.100] User<dev_lead>: Query user profile with email admin@corp.io
[2026-10-25 14:32:00] [ERROR] [10.0.0.5] User<billing_agent>: Failed payment for card 4111-2222-3333-4444 with SSN 123-45-6789
[2026-10-25 14:35:00] [CRITICAL] [999.999.999.999] User<attacker>: Spoofed header attack detected
[INVALID] This is a malformed log line without proper formatting"""

    print("=== 1. Structured Log Parsing ===")
    parsed_records = analyzer.parse_log_dump(sample_logs)
    print(f"Parsed {len(parsed_records)} Valid Log Records (invalid IP filtered):")
    for idx, rec in enumerate(parsed_records, 1):
        print(f"Record {idx}: {rec}")

    print("\n=== 2. PII Redaction & Data Sanitization ===")
    raw_error_msg = parsed_records[1]["message"]
    sanitized_msg = analyzer.redact_sensitive_data(raw_error_msg)
    print(f"Original Message:  '{raw_error_msg}'")
    print(f"Sanitized Message: '{sanitized_msg}'")

    raw_info_msg = parsed_records[0]["message"]
    sanitized_info = analyzer.redact_sensitive_data(raw_info_msg)
    print(f"Original Info:     '{raw_info_msg}'")
    print(f"Sanitized Info:    '{sanitized_info}'")

    print("\n=== 3. URL Query Parameter Extraction ===")
    sample_url = "https://api.corp.net/v1/search?tenant=acme&filter=active&page=2#heading"
    params = analyzer.extract_query_parameters(sample_url)
    print(f"Extracted Query Parameters: {params}")
