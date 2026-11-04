"""
Phase 4 - Topic 05: Inheritance
Example 03: Inheritance (`IS-A`) vs Composition (`HAS-A`)

Demonstrates:
  - Why inheriting from `list` or an unrelated class just to reuse 1-2 methods
    exposes unwanted parent methods
  - How Composition (`HAS-A`: holding a component object as an attribute) creates
    cleaner, more flexible designs
"""


class AuditLogger:
    """Reusable component for recording structured audit events."""

    def __init__(self) -> None:
        self.entries: list[str] = []

    def record(self, actor: str, action: str) -> None:
        self.entries.append(f"actor={actor} | action={action}")


class SecureDocumentVault:
    """
    Uses COMPOSITION (`HAS-A` AuditLogger) instead of inheriting from `AuditLogger` or `list`.
    Callers cannot accidentally call `.clear()` or `.pop()` on the vault!
    """

    def __init__(self, vault_name: str) -> None:
        self.vault_name = vault_name
        self._documents: dict[str, str] = {}
        self.logger = AuditLogger()  # HAS-A relationship (Composition)

    def store_document(self, user: str, doc_id: str, content: str) -> None:
        self._documents[doc_id] = content
        self.logger.record(user, f"stored {doc_id}")

    def read_document(self, user: str, doc_id: str) -> str:
        self.logger.record(user, f"read {doc_id}")
        return self._documents.get(doc_id, "<NOT FOUND>")


def main() -> None:
    print("=== Composition (`HAS-A`): `SecureDocumentVault` + `AuditLogger` ===")
    vault = SecureDocumentVault("Legal-Contracts")
    vault.store_document("aarav", "DOC-01", "Non-Disclosure Agreement")
    content = vault.read_document("priya", "DOC-01")
    print(f"  Retrieved document : {content!r}")
    print("  Audit trail entries:")
    for entry in vault.logger.entries:
        print(f"    - {entry}")


if __name__ == "__main__":
    main()
