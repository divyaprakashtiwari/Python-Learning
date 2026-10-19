"""
Topic: Advanced Python - Regular Expressions (re Module)
--------------------------------------------------------
Questions Covered:
1. Core Matching Primitives: re.search vs re.match vs re.fullmatch with span and boundary checks.
2. Multiple Token Extraction: re.findall vs re.finditer with match object positional metadata.
3. Named Capture Groups: (?P<name>pattern) and structured extraction using match.groupdict().
4. Dynamic Regex Substitution: Using callable replacer in re.sub for PII masking and token transformation.
5. Lookaround Assertions: Positive/Negative Lookahead and Lookbehind for non-consuming constraints.
6. Greedy vs Lazy Quantifiers: Managing greedy consumption vs reluctant matching (* vs *?).
7. Compilation Flags: Using re.VERBOSE, re.IGNORECASE, re.MULTILINE, and re.DOTALL in complex grammars.
8. Advanced Tokenization with re.split: Splitting on complex multi-character delimiter sets.
9. Strict RFC Validators: Enterprise-grade regex validators for SemVer, IPv4 addresses, and ISO timestamps.
10. Architectural System: Security Log Analyzer & Intrusion Detection Engine detecting SQLi, XSS, and Path Traversal.
"""

import re
from urllib.parse import unquote
from typing import List, Dict, Any, Optional, Tuple


# ==============================================================================
# Question 1: Core Matching Primitives (search, match, fullmatch)
# ==============================================================================
def compare_matching_modes(pattern: str, text: str) -> Dict[str, Optional[Tuple[int, int]]]:
    """
    Compares match, search, and fullmatch on the input text.
    Returns dictionary with match spans or None if no match.
    """
    compiled = re.compile(pattern)
    m_match = compiled.match(text)
    m_search = compiled.search(text)
    m_full = compiled.fullmatch(text)

    return {
        "match": m_match.span() if m_match else None,
        "search": m_search.span() if m_search else None,
        "fullmatch": m_full.span() if m_full else None,
    }


def test_q1_matching_primitives():
    pat = r"\d+"
    # Leading whitespace: match fails (not at start 0), search succeeds, fullmatch fails
    text1 = "   42 items"
    res1 = compare_matching_modes(pat, text1)
    assert res1["match"] is None
    assert res1["search"] == (3, 5)
    assert res1["fullmatch"] is None

    # Number at very beginning
    text2 = "42 items"
    res2 = compare_matching_modes(pat, text2)
    assert res2["match"] == (0, 2)
    assert res2["search"] == (0, 2)
    assert res2["fullmatch"] is None

    # Entire string is digits
    text3 = "42"
    res3 = compare_matching_modes(pat, text3)
    assert res3["match"] == (0, 2)
    assert res3["search"] == (0, 2)
    assert res3["fullmatch"] == (0, 2)
    print("=== Q1: Core Matching Primitives Verified ===")


# ==============================================================================
# Question 2: Multiple Token Extraction (findall vs finditer)
# ==============================================================================
def extract_key_value_pairs(query_string: str) -> List[Tuple[str, str, int, int]]:
    """
    Extracts all key=value pairs from a query string using re.finditer,
    returning list of (key, value, start_pos, end_pos).
    """
    pattern = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)=([^&]+)")
    results = []
    for match in pattern.finditer(query_string):
        key = match.group(1)
        val = match.group(2)
        start, end = match.span()
        results.append((key, val, start, end))
    return results


def test_q2_token_extraction():
    qs = "user=alice&session_id=xyz123&timeout=3600&theme=dark"
    pairs = extract_key_value_pairs(qs)
    assert len(pairs) == 4
    assert pairs[0] == ("user", "alice", 0, 10)
    assert pairs[1] == ("session_id", "xyz123", 11, 28)
    assert pairs[2] == ("timeout", "3600", 29, 41)
    assert pairs[3] == ("theme", "dark", 42, 52)
    print("=== Q2: Token Extraction with finditer Verified ===")


# ==============================================================================
# Question 3: Named Capture Groups
# ==============================================================================
def parse_semantic_version(version_str: str) -> Optional[Dict[str, Any]]:
    """
    Parses a SemVer string (e.g. 'v2.14.3-alpha.1+build.2026') into structured dictionary
    using named capture groups (?P<name>...).
    """
    semver_pattern = re.compile(
        r"^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
        r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
        r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
    )
    m = semver_pattern.match(version_str)
    if not m:
        return None

    data = m.groupdict()
    return {
        "major": int(data["major"]),
        "minor": int(data["minor"]),
        "patch": int(data["patch"]),
        "prerelease": data.get("prerelease"),
        "build": data.get("build"),
    }


def test_q3_named_groups():
    v1 = parse_semantic_version("v1.2.3")
    assert v1 == {"major": 1, "minor": 2, "patch": 3, "prerelease": None, "build": None}

    v2 = parse_semantic_version("2.14.0-rc.1+build.89")
    assert v2 == {"major": 2, "minor": 14, "patch": 0, "prerelease": "rc.1", "build": "build.89"}

    assert parse_semantic_version("invalid-semver") is None
    print("=== Q3: Named Capture Groups Verified ===")


# ==============================================================================
# Question 4: Dynamic Regex Substitution with Callbacks (re.sub)
# ==============================================================================
def mask_credit_cards(text: str) -> str:
    """
    Replaces 16-digit credit cards formatted as XXXX-XXXX-XXXX-XXXX or XXXXXXXXXXXXXXXX
    with masked form showing only last 4 digits: ****-****-****-1234.
    """
    cc_pattern = re.compile(r"\b(\d{4})[- ]?(\d{4})[- ]?(\d{4})[- ]?(\d{4})\b")

    def replacer(match: re.Match) -> str:
        last4 = match.group(4)
        return f"****-****-****-{last4}"

    return cc_pattern.sub(replacer, text)


def test_q4_dynamic_substitution():
    raw_text = "Card 1: 4111-2222-3333-4444 and Card 2: 5555666677778888 paid invoice."
    masked = mask_credit_cards(raw_text)
    expected = "Card 1: ****-****-****-4444 and Card 2: ****-****-****-8888 paid invoice."
    assert masked == expected
    print("=== Q4: Dynamic Regex Substitution Verified ===")


# ==============================================================================
# Question 5: Lookaround Assertions (Lookahead and Lookbehind)
# ==============================================================================
def extract_usd_prices(text: str) -> List[float]:
    r"""
    Uses positive lookbehind (?<=\$) to match price digits preceded by a dollar sign,
    and negative lookahead (?!%) to ensure it is not a percentage or discount.
    """
    price_pattern = re.compile(r"(?<=\$)\d+(?:\.\d{2})?(?![%\d])")
    matches = price_pattern.findall(text)
    return [float(p) for p in matches]


def validate_password_complexity(password: str) -> bool:
    r"""
    Validates password complexity using multiple lookahead assertions:
    - At least 8 characters
    - At least one uppercase letter (?=.*[A-Z])
    - At least one lowercase letter (?=.*[a-z])
    - At least one digit (?=.*\d)
    - At least one special symbol (?=.*[@$!%*?&])
    """
    pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )
    return bool(pattern.match(password))


def test_q5_lookaround_assertions():
    text = "Items: Widget $19.99, Cable $5, Discount $10% off, Fee 25."
    prices = extract_usd_prices(text)
    # 19.99 and 5 matched, 10 ignored because of % negative lookahead, 25 ignored (no $)
    assert prices == [19.99, 5.0]

    assert validate_password_complexity("Secret1@") is True
    assert validate_password_complexity("short1@") is False  # < 8 chars
    assert validate_password_complexity("alllowercase1@") is False  # No uppercase
    assert validate_password_complexity("ALLUPPERCASE1@") is False  # No lowercase
    assert validate_password_complexity("NoDigitsHere!") is False
    assert validate_password_complexity("NoSpecialChars123") is False
    print("=== Q5: Lookaround Assertions Verified ===")


# ==============================================================================
# Question 6: Greedy vs Lazy (Reluctant) Quantifiers
# ==============================================================================
def extract_html_tag_contents(html: str) -> Tuple[List[str], List[str]]:
    """
    Compares greedy pattern '<.*>' with lazy pattern '<.*?>'.
    Returns (greedy_matches, lazy_matches).
    """
    greedy_pat = re.compile(r"<.*>")
    lazy_pat = re.compile(r"<.*?>")

    greedy_matches = greedy_pat.findall(html)
    lazy_matches = lazy_pat.findall(html)
    return greedy_matches, lazy_matches


def test_q6_greedy_vs_lazy():
    html_snippet = "<div><span>First</span><span>Second</span></div>"
    greedy, lazy = extract_html_tag_contents(html_snippet)

    # Greedy matches from the first '<' to the very last '>' across the entire string
    assert len(greedy) == 1
    assert greedy[0] == "<div><span>First</span><span>Second</span></div>"

    # Lazy matches individual tags
    assert lazy == ["<div>", "<span>", "</span>", "<span>", "</span>", "</div>"]
    print("=== Q6: Greedy vs Lazy Quantifiers Verified ===")


# ==============================================================================
# Question 7: Verbose Multiline Regular Expressions (re.VERBOSE)
# ==============================================================================
EMAIL_VERBOSE_REGEX = re.compile(
    r"""
    ^
    (?P<username> [a-zA-Z0-9_.+-]+ )   # Username / local part
    @
    (?P<domain>   [a-zA-Z0-9-]+       # Domain name
        (?:\.[a-zA-Z0-9-]+)*          # Optional subdomains
    )
    \.
    (?P<tld>      [a-zA-Z]{2,}        # Top-level domain (com, org, net, edu)
    )
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)


def parse_email_address(email_str: str) -> Optional[Dict[str, str]]:
    m = EMAIL_VERBOSE_REGEX.match(email_str.strip())
    return m.groupdict() if m else None


def test_q7_verbose_multiline():
    parsed = parse_email_address("developer.support@service.example.COM")
    assert parsed == {
        "username": "developer.support",
        "domain": "service.example",
        "tld": "COM",
    }
    assert parse_email_address("invalid-email@@domain") is None
    print("=== Q7: Verbose Multiline Expressions (re.VERBOSE) Verified ===")


# ==============================================================================
# Question 8: Advanced Tokenization with re.split
# ==============================================================================
def tokenize_math_expression(expr: str) -> List[str]:
    """
    Tokenizes mathematical expression into operands and operators,
    preserving operators by using capturing parentheses in re.split.
    """
    # Parentheses in pattern retain the matched delimiter in the output list
    pattern = re.compile(r"(\s*[\+\-\*\/\(\)]\s*)")
    raw_tokens = pattern.split(expr)
    return [t.strip() for t in raw_tokens if t and t.strip()]


def test_q8_advanced_resplit():
    expr = "34 + (12 * 5) - 100 / 4"
    tokens = tokenize_math_expression(expr)
    expected = ["34", "+", "(", "12", "*", "5", ")", "-", "100", "/", "4"]
    assert tokens == expected
    print("=== Q8: Advanced Tokenization with re.split Verified ===")


# ==============================================================================
# Question 9: Strict IPv4 and Network CIDR Validator
# ==============================================================================
def validate_ipv4_cidr(cidr_str: str) -> bool:
    """
    Validates an IPv4 CIDR string strictly checking 0-255 octet bounds and 0-32 prefix:
    e.g. '192.168.1.0/24' is valid, '256.0.0.1/33' is invalid.
    """
    # Octet 0-255 pattern: 25[0-5] | 2[0-4][0-9] | 1[0-9][0-9] | [1-9]?[0-9]
    octet = r"(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])"
    cidr_prefix = r"(?:3[0-2]|[1-2]?[0-9])"  # 0 to 32
    pattern = re.compile(f"^{octet}\\.{octet}\\.{octet}\\.{octet}(?:/{cidr_prefix})?$")
    return bool(pattern.match(cidr_str))


def test_q9_strict_ipv4_validator():
    assert validate_ipv4_cidr("192.168.1.1") is True
    assert validate_ipv4_cidr("10.0.0.0/8") is True
    assert validate_ipv4_cidr("0.0.0.0/0") is True
    assert validate_ipv4_cidr("255.255.255.255/32") is True

    assert validate_ipv4_cidr("256.1.1.1") is False  # 256 invalid
    assert validate_ipv4_cidr("192.168.1.1/33") is False  # /33 invalid
    assert validate_ipv4_cidr("192.168.1") is False  # 3 octets
    assert validate_ipv4_cidr("192.168.1.1.1") is False  # 5 octets
    print("=== Q9: Strict IPv4 CIDR Validator Verified ===")


# ==============================================================================
# Question 10: Architectural System: Security Log & Intrusion Detection Scanner
# ==============================================================================
class SecurityIncidentScanner:
    """
    Production-grade log parser and signature-based intrusion detection scanner.
    Extracts HTTP access log entries and detects SQLi, XSS, and Path Traversal.
    """
    # Common Log Format regex: IP ident auth [timestamp] "METHOD path PROTO" status bytes
    CLF_REGEX = re.compile(
        r'^(?P<ip>\S+)\s+\S+\s+(?P<user>\S+)\s+\[(?P<timestamp>[^\]]+)\]\s+'
        r'"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+(?P<proto>[^"]+)"\s+'
        r'(?P<status>\d{3})\s+(?P<bytes>\S+)'
    )

    ATTACK_SIGNATURES = {
        "SQL_INJECTION": re.compile(r"(?i)(?:\bunion\b\s+\ball\b\s+\bselect\b|\bunion\b\s+\bselect\b|'\s*or\s+'?1'?='?1|\bdrop\b\s+\btable\b)"),
        "PATH_TRAVERSAL": re.compile(r"(?:\.\./|\.\.\\|%2e%2e%2f)"),
        "XSS": re.compile(r"(?i)(?:<script.*?>|javascript:|onerror\s*=|onload\s*=)"),
    }

    def scan_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        m = self.CLF_REGEX.match(line.strip())
        if not m:
            return None

        entry = m.groupdict()
        path = entry["path"]
        decoded_path = unquote(path)

        detected_threats = []
        for threat_type, sig_regex in self.ATTACK_SIGNATURES.items():
            if sig_regex.search(path) or sig_regex.search(decoded_path):
                detected_threats.append(threat_type)

        return {
            "ip": entry["ip"],
            "timestamp": entry["timestamp"],
            "method": entry["method"],
            "path": path,
            "status": int(entry["status"]),
            "threats": detected_threats,
            "is_suspicious": len(detected_threats) > 0,
        }


def test_q10_security_incident_scanner():
    scanner = SecurityIncidentScanner()

    # 1. Normal benign request
    line_normal = '192.168.1.100 - alice [19/Oct/2026:14:00:01 +0000] "GET /products?page=2 HTTP/1.1" 200 4521'
    res1 = scanner.scan_log_line(line_normal)
    assert res1 is not None
    assert res1["ip"] == "192.168.1.100"
    assert res1["is_suspicious"] is False
    assert len(res1["threats"]) == 0

    # 2. SQL Injection request (URL encoded as seen in real HTTP logs)
    line_sqli = '10.0.0.5 - - [19/Oct/2026:14:01:05 +0000] "GET /users?id=1%27%20OR%201=1 HTTP/1.1" 400 320'
    res2 = scanner.scan_log_line(line_sqli)
    assert res2 is not None
    assert res2["is_suspicious"] is True
    assert "SQL_INJECTION" in res2["threats"]

    # 3. Path Traversal request
    line_traversal = '172.16.0.4 - - [19/Oct/2026:14:02:10 +0000] "GET /static/../../etc/passwd HTTP/1.1" 403 0'
    res3 = scanner.scan_log_line(line_traversal)
    assert res3 is not None
    assert res3["is_suspicious"] is True
    assert "PATH_TRAVERSAL" in res3["threats"]

    # 4. XSS attack request
    line_xss = '192.168.1.50 - - [19/Oct/2026:14:03:22 +0000] "POST /comment?text=<script>alert(1)</script> HTTP/1.1" 200 120'
    res4 = scanner.scan_log_line(line_xss)
    assert res4 is not None
    assert res4["is_suspicious"] is True
    assert "XSS" in res4["threats"]
    print("=== Q10: Architectural Security Log Scanner & IDS Verified ===")


# ==============================================================================
# Main Verification Execution
# ==============================================================================
if __name__ == "__main__":
    test_q1_matching_primitives()
    test_q2_token_extraction()
    test_q3_named_groups()
    test_q4_dynamic_substitution()
    test_q5_lookaround_assertions()
    test_q6_greedy_vs_lazy()
    test_q7_verbose_multiline()
    test_q8_advanced_resplit()
    test_q9_strict_ipv4_validator()
    test_q10_security_incident_scanner()
    print("\nAll 10 regular expressions practice questions passed successfully!")
