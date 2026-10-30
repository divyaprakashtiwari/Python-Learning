"""
Question 8: Enterprise Email Hygiene & Validation Engine
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- RFC-compliant email syntax validation via regular expressions
- Local part, plus-tag, domain, subdomain, and TLD component extraction
- Risk classification (disposable temporary domains, role-based mailboxes)
- Canonical provider-specific normalization (Gmail dot-stripping and alias removal)
- Batch validation metrics and hygiene reporting
"""

import re
from typing import Tuple, Optional, Dict, Any, List


class EmailValidatorSuite:
    """
    Enterprise email hygiene engine supporting syntax verification,
    component decomposition, disposable/role-based risk classification, and normalization.
    """

    DISPOSABLE_DOMAINS = {
        "mailinator.com",
        "tempmail.com",
        "10minutemail.com",
        "guerrillamail.com",
        "throwawaymail.com",
    }

    ROLE_ACCOUNTS = {
        "admin",
        "administrator",
        "support",
        "info",
        "sales",
        "billing",
        "contact",
        "help",
        "security",
    }

    EMAIL_REGEX = re.compile(
        r"^(?P<local>[a-zA-Z0-9_\-+.]+)@(?P<domain>[a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})$"
    )

    def validate_syntax(self, email: str) -> Tuple[bool, str]:
        """
        Validates email formatting according to RFC constraints:
        - Non-empty local-part and valid domain
        - No consecutive dots (..) in local part
        - No leading/trailing dots in local part
        - Valid domain with at least 2-character alphabetic TLD
        """
        clean_email = email.strip()
        if not clean_email or "@" not in clean_email:
            return (False, "Missing '@' separator or empty email")

        match = self.EMAIL_REGEX.match(clean_email)
        if not match:
            return (False, "Invalid overall email format")

        local_part = match.group("local")
        domain_part = match.group("domain")

        # Local part dot constraints
        if ".." in local_part:
            return (False, "Consecutive dots '..' in local part")
        if local_part.startswith(".") or local_part.endswith("."):
            return (False, "Local part cannot start or end with a dot")

        # Domain part dot constraints
        if ".." in domain_part or domain_part.startswith(".") or domain_part.endswith("."):
            return (False, "Invalid domain dot structure")

        return (True, "Valid")

    def parse_email(self, email: str) -> Dict[str, Optional[str]]:
        """Deconstructs email into local_part, tag, domain, and tld."""
        clean_email = email.strip()
        is_valid, _ = self.validate_syntax(clean_email)
        if not is_valid:
            raise ValueError(f"Cannot parse invalid email: '{clean_email}'")

        local, domain = clean_email.split("@", 1)

        # Detect plus-tag
        tag: Optional[str] = None
        base_local = local
        if "+" in local:
            base_local, tag = local.split("+", 1)

        domain_parts = domain.lower().split(".")
        tld = domain_parts[-1]

        return {
            "local_part": base_local,
            "tag": tag,
            "domain": domain.lower(),
            "tld": tld,
        }

    def is_disposable(self, domain: str) -> bool:
        """Checks if domain is a known temporary/disposable provider."""
        return domain.lower() in self.DISPOSABLE_DOMAINS

    def is_role_account(self, local_part: str) -> bool:
        """Flags generic departmental role accounts."""
        clean_local = local_part.lower().split("+")[0]
        return clean_local in self.ROLE_ACCOUNTS

    def normalize_email(self, email: str) -> str:
        """
        Normalizes email to canonical form.
        For Gmail/Googlemail: lowercases, strips dots from local part, and removes plus aliases.
        """
        parsed = self.parse_email(email)
        domain = parsed["domain"]
        local = parsed["local_part"] or ""

        if domain in ("gmail.com", "googlemail.com"):
            clean_local = local.replace(".", "").lower()
            return f"{clean_local}@gmail.com"

        return f"{local.lower()}@{domain}"

    def batch_process(self, emails: List[str]) -> Dict[str, Any]:
        """Validates, classifies, and cleans a list of raw email addresses."""
        valid_count = 0
        invalid_emails = []
        disposable_count = 0
        role_count = 0
        cleaned_list = []

        for raw in emails:
            is_valid, reason = self.validate_syntax(raw)
            if not is_valid:
                invalid_emails.append((raw, reason))
                continue

            valid_count += 1
            parsed = self.parse_email(raw)
            domain = parsed["domain"] or ""
            local = parsed["local_part"] or ""

            if self.is_disposable(domain):
                disposable_count += 1
            if self.is_role_account(local):
                role_count += 1

            cleaned_list.append(self.normalize_email(raw))

        return {
            "total_processed": len(emails),
            "valid_count": valid_count,
            "invalid_count": len(invalid_emails),
            "invalid_details": invalid_emails,
            "disposable_count": disposable_count,
            "role_based_count": role_count,
            "cleaned_emails": cleaned_list,
        }


if __name__ == "__main__":
    suite = EmailValidatorSuite()

    test_emails = [
        "Alex.Dev+marketing@gmail.com",
        "support@corporate.co.uk",
        "fraudulent..user@domain.com",
        "temporary.user@mailinator.com",
        "plainaddress",
        "dr.jane_doe@hospital.org",
    ]

    print("=== 1. Batch Verification ===")
    results = suite.batch_process(test_emails)
    print("Batch Verification Summary:")
    print(f"- Total Processed: {results['total_processed']}")
    print(f"- Valid Emails: {results['valid_count']}")
    print(f"- Invalid Syntax: {results['invalid_count']} ({[e[0] for e in results['invalid_details']]})")
    print(f"- Disposable Emails: {results['disposable_count']}")
    print(f"- Role-Based Accounts: {results['role_based_count']}")

    print("\n=== 2. Component Decomposition ===")
    sample_email = "Alex.Dev+marketing@gmail.com"
    parsed = suite.parse_email(sample_email)
    print(f"Parsed Components for '{sample_email}':")
    for k, v in parsed.items():
        print(f"  '{k}': '{v}'")

    print("\n=== 3. Canonical Normalization ===")
    normalized = suite.normalize_email(sample_email)
    print(f"Normalized Gmail Address: '{normalized}'")

    print("\n=== 4. Edge Cases & Syntax Rejections ===")
    invalid_cases = [".leadingdot@domain.com", "trailingdot.@domain.com", "nodomain@.com"]
    for case in invalid_cases:
        valid_flag, reason = suite.validate_syntax(case)
        print(f"'{case}': Valid={valid_flag} (Reason: {reason})")
