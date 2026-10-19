"""
Topic 12: JSON, CSV, API, Database
Question 04: SQLite Database CRUD

A comprehensive, production-grade guide to relational database operations with Python's
built-in `sqlite3` module. Covers DDL schemas, parameterized query injection defense,
CRUD operations, custom row factories, transactions & savepoints, batch executemany,
custom Python UDFs & aggregates, automated schema migrations, Full-Text Search (FTS5),
and an architectural Repository Pattern.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import sqlite3
import hashlib
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


# =====================================================================
# Q1: Connection Lifecycle, DDL Schemas, and Constraints
# =====================================================================
def q1_connection_ddl_and_constraints():
    """
    Demonstrates in-memory database creation, table creation with constraints
    (PRIMARY KEY, UNIQUE, NOT NULL, CHECK), and foreign key activation.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Foreign keys are disabled by default in SQLite; always enable explicitly
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );
    """)

    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            price REAL NOT NULL CHECK(price >= 0.0),
            in_stock INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        );
    """)
    conn.commit()

    # Insert valid records
    cursor.execute("INSERT INTO categories (name) VALUES (?);", ("Electronics",))
    cat_id = cursor.lastrowid
    assert cat_id == 1

    cursor.execute(
        "INSERT INTO products (category_id, title, price) VALUES (?, ?, ?);",
        (cat_id, "Noise Cancelling Headphones", 199.99)
    )
    conn.commit()

    # Verify CHECK constraint violation (negative price)
    check_failed = False
    try:
        cursor.execute("INSERT INTO products (category_id, title, price) VALUES (?, ?, ?);", (cat_id, "Bad Item", -10.0))
        conn.commit()
    except sqlite3.IntegrityError:
        check_failed = True
        conn.rollback()
    assert check_failed is True

    # Verify UNIQUE constraint violation
    unique_failed = False
    try:
        cursor.execute("INSERT INTO categories (name) VALUES (?);", ("Electronics",))
        conn.commit()
    except sqlite3.IntegrityError:
        unique_failed = True
        conn.rollback()
    assert unique_failed is True

    conn.close()
    print("=== Q1: SQLite Schema & Constraints Verified ===")


# =====================================================================
# Q2: Parameterized Queries & SQL Injection Immunity
# =====================================================================
def q2_sql_injection_defense():
    """
    Demonstrates vulnerability of string formatting (f-strings) to SQL injection
    and proves parameterized queries (? and :named) safely neutralize attack payloads.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, is_admin INTEGER);")
    cursor.execute("INSERT INTO users (username, is_admin) VALUES ('alice', 0), ('admin', 1);")
    conn.commit()

    # Malicious SQL injection payload intended to bypass authentication / filter
    malicious_input = "' OR '1'='1"

    # 1. Parameterized positional query ('?')
    cursor.execute("SELECT * FROM users WHERE username = ?;", (malicious_input,))
    results_safe = cursor.fetchall()
    # Safely found 0 users because username was treated literally as "' OR '1'='1"
    assert len(results_safe) == 0

    # 2. Parameterized named query (':name')
    cursor.execute(
        "SELECT * FROM users WHERE username = :uname AND is_admin = :admin_flag;",
        {"uname": "alice", "admin_flag": 0}
    )
    alice_row = cursor.fetchone()
    assert alice_row is not None
    assert alice_row[1] == "alice"
    assert alice_row[2] == 0

    conn.close()
    print("=== Q2: Parameterized Queries & SQL Injection Defense Verified ===")


# =====================================================================
# Q3: Complete CRUD Workflow with rowcount and Foreign Key Cascades
# =====================================================================
def q3_crud_operations():
    """
    Demonstrates full Create, Read, Update, Delete lifecycle with affected row counts
    and cascading deletes.
    """
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT);")
    cursor.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            author_id INTEGER,
            title TEXT,
            FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
        );
    """)

    # CREATE
    cursor.execute("INSERT INTO authors (name) VALUES (?);", ("George Orwell",))
    author_id = cursor.lastrowid
    cursor.execute("INSERT INTO books (author_id, title) VALUES (?, ?);", (author_id, "1984"))
    cursor.execute("INSERT INTO books (author_id, title) VALUES (?, ?);", (author_id, "Animal Farm"))
    conn.commit()

    # READ
    cursor.execute("SELECT title FROM books WHERE author_id = ? ORDER BY title ASC;", (author_id,))
    titles = [row[0] for row in cursor.fetchall()]
    assert titles == ["1984", "Animal Farm"]

    # UPDATE
    cursor.execute("UPDATE books SET title = ? WHERE title = ?;", ("Nineteen Eighty-Four", "1984"))
    assert cursor.rowcount == 1
    conn.commit()

    cursor.execute("SELECT title FROM books WHERE id = 1;")
    assert cursor.fetchone()[0] == "Nineteen Eighty-Four"

    # DELETE with CASCADE: deleting the author should automatically delete all their books
    cursor.execute("DELETE FROM authors WHERE id = ?;", (author_id,))
    assert cursor.rowcount == 1
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM books;")
    assert cursor.fetchone()[0] == 0

    conn.close()
    print("=== Q3: CRUD Operations with Cascading Deletes Verified ===")


# =====================================================================
# Q4: Custom Row Factories and Object Mapping
# =====================================================================
@dataclass
class Account:
    id: int
    holder: str
    balance: float


def account_row_factory(cursor, row):
    """Custom factory turning query tuples into strongly typed dataclass instances."""
    return Account(id=row[0], holder=row[1], balance=row[2])


def q4_row_factories():
    """
    Demonstrates sqlite3.Row for column-name indexing and custom dataclass row factories.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, holder TEXT, balance REAL);")
    cursor.execute("INSERT INTO accounts VALUES (1, 'Alice', 2500.50), (2, 'Bob', 120.00);")
    conn.commit()

    # 1. Using built-in sqlite3.Row
    conn.row_factory = sqlite3.Row
    row_cursor = conn.cursor()
    row_cursor.execute("SELECT id, holder, balance FROM accounts WHERE holder = 'Alice';")
    row = row_cursor.fetchone()

    # Access by column name (case-insensitive) or index
    assert row["holder"] == "Alice"
    assert row["balance"] == 2500.50
    assert row[0] == 1
    assert list(row.keys()) == ["id", "holder", "balance"]

    # 2. Custom Dataclass Factory
    conn.row_factory = account_row_factory
    dc_cursor = conn.cursor()
    dc_cursor.execute("SELECT id, holder, balance FROM accounts ORDER BY id ASC;")
    accounts = dc_cursor.fetchall()

    assert len(accounts) == 2
    assert isinstance(accounts[0], Account)
    assert accounts[0].holder == "Alice"
    assert accounts[1].holder == "Bob"
    assert accounts[1].balance == 120.00

    conn.close()
    print("=== Q4: Row Factories (sqlite3.Row & Dataclass) Verified ===")


# =====================================================================
# Q5: Transactions, Atomic Rollbacks, and Savepoints
# =====================================================================
def q5_transactions_and_savepoints():
    """
    Demonstrates transaction boundaries, atomic rollbacks on failure,
    and partial rollbacks using SAVEPOINT.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE balances (user TEXT PRIMARY KEY, amount REAL);")
    cursor.execute("INSERT INTO balances VALUES ('Alice', 1000.0), ('Bob', 500.0);")
    conn.commit()

    # Function transferring funds atomically
    def transfer_funds(sender: str, receiver: str, amount: float, should_fail_at_end: bool = False):
        try:
            with conn: # 'with conn' automatically manages transactions (BEGIN / COMMIT / ROLLBACK)
                # Deduct from sender
                cursor.execute("UPDATE balances SET amount = amount - ? WHERE user = ?;", (amount, sender))
                # Add to receiver
                cursor.execute("UPDATE balances SET amount = amount + ? WHERE user = ?;", (amount, receiver))

                if should_fail_at_end:
                    raise RuntimeError("Simulated network failure right before commit")
        except RuntimeError:
            pass

    # Successful transfer
    transfer_funds("Alice", "Bob", 200.0)
    cursor.execute("SELECT amount FROM balances WHERE user = 'Alice';")
    assert cursor.fetchone()[0] == 800.0
    cursor.execute("SELECT amount FROM balances WHERE user = 'Bob';")
    assert cursor.fetchone()[0] == 700.0

    # Failed transfer must rollback completely
    transfer_funds("Alice", "Bob", 300.0, should_fail_at_end=True)
    cursor.execute("SELECT amount FROM balances WHERE user = 'Alice';")
    assert cursor.fetchone()[0] == 800.0  # unchanged!
    cursor.execute("SELECT amount FROM balances WHERE user = 'Bob';")
    assert cursor.fetchone()[0] == 700.0  # unchanged!

    # Nested transactions using SAVEPOINT
    cursor.execute("SAVEPOINT sp_batch;")
    cursor.execute("INSERT INTO balances VALUES ('Charlie', 250.0);")
    cursor.execute("SAVEPOINT sp_inner;")
    cursor.execute("INSERT INTO balances VALUES ('David', 150.0);")
    # Rollback only to sp_inner
    cursor.execute("ROLLBACK TO SAVEPOINT sp_inner;")
    cursor.execute("RELEASE SAVEPOINT sp_batch;")
    conn.commit()

    cursor.execute("SELECT user FROM balances ORDER BY user ASC;")
    users = [r[0] for r in cursor.fetchall()]
    assert "Charlie" in users
    assert "David" not in users  # Rolled back

    conn.close()
    print("=== Q5: Transactions & Savepoints Verified ===")


# =====================================================================
# Q6: Batch Processing with executemany and Streaming Fetch
# =====================================================================
def q6_batch_executemany_and_streaming():
    """
    Demonstrates fast bulk loading with cursor.executemany and memory-efficient
    result iteration with fetchmany generator.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE metrics (id INTEGER PRIMARY KEY, metric_name TEXT, reading REAL);")

    # 1. Batch insertion of 1,000 records
    data_batch = [(f"sensor_{i % 10}", float(i * 1.5)) for i in range(1000)]
    cursor.executemany("INSERT INTO metrics (metric_name, reading) VALUES (?, ?);", data_batch)
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM metrics;")
    assert cursor.fetchone()[0] == 1000

    # 2. Generator-based streaming with fetchmany to avoid loading all into memory
    def stream_fetch_chunks(cur, size=150):
        while True:
            rows = cur.fetchmany(size)
            if not rows:
                break
            yield rows

    cursor.execute("SELECT id, metric_name, reading FROM metrics ORDER BY id ASC;")
    total_fetched = 0
    chunk_counts = []
    for chunk in stream_fetch_chunks(cursor, size=150):
        chunk_counts.append(len(chunk))
        total_fetched += len(chunk)

    assert total_fetched == 1000
    # 1000 / 150 = 6 chunks of 150 (900) + 1 chunk of 100
    assert chunk_counts == [150, 150, 150, 150, 150, 150, 100]

    conn.close()
    print("=== Q6: Batch executemany & Streaming fetchmany Verified ===")


# =====================================================================
# Q7: User-Defined Functions (UDFs) and Custom Aggregates
# =====================================================================
class GeometricMeanAggregate:
    """Custom SQLite Aggregate function computing geometric mean: (x1 * x2 * ... * xn) ** (1/n)."""
    def __init__(self):
        self.product = 1.0
        self.count = 0

    def step(self, value):
        if value is not None and value > 0:
            self.product *= float(value)
            self.count += 1

    def finalize(self):
        if self.count == 0:
            return 0.0
        return self.product ** (1.0 / self.count)


def q7_custom_udfs_and_aggregates():
    """
    Registers custom Python functions and aggregate classes directly into the SQLite query engine.
    """
    conn = sqlite3.connect(":memory:")

    # 1. Scalar UDF: SHA-256 hash function callable from SQL
    def sql_sha256(text: Optional[str]) -> Optional[str]:
        if text is None:
            return None
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    # 2. Scalar UDF: Regex match function
    def sql_regex_match(pattern: str, string: Optional[str]) -> int:
        if string is None:
            return 0
        return 1 if re.search(pattern, string) else 0

    conn.create_function("sha256", 1, sql_sha256)
    conn.create_function("regex_match", 2, sql_regex_match)

    # 3. Aggregate UDF
    conn.create_aggregate("geom_mean", 1, GeometricMeanAggregate)

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE items (name TEXT, score REAL);")
    cursor.execute("INSERT INTO items VALUES ('alpha-01', 2.0), ('beta-02', 8.0), ('gamma-99', 32.0);")
    conn.commit()

    # Test scalar UDFs in SQL
    cursor.execute("SELECT sha256('hello')")
    expected_hash = hashlib.sha256(b"hello").hexdigest()
    assert cursor.fetchone()[0] == expected_hash

    cursor.execute("SELECT name FROM items WHERE regex_match('^[a-z]+-[0-9]{2}$', name) = 1 ORDER BY name;")
    matched = [r[0] for r in cursor.fetchall()]
    assert matched == ["alpha-01", "beta-02", "gamma-99"]

    # Test aggregate UDF in SQL: geometric mean of (2, 8, 32) = (512)**(1/3) = 8.0
    cursor.execute("SELECT geom_mean(score) FROM items;")
    geo_mean = cursor.fetchone()[0]
    assert round(geo_mean, 2) == 8.0

    conn.close()
    print("=== Q7: Custom Python UDFs & Aggregates in SQLite Verified ===")


# =====================================================================
# Q8: Automated Database Schema Migration Engine
# =====================================================================
class MigrationEngine:
    """
    Tracks and executes sequential schema migrations, recording applied versions
    in an internal `schema_migrations` metadata table.
    """
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._init_migration_table()

    def _init_migration_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def get_applied_versions(self) -> List[int]:
        cursor = self.conn.execute("SELECT version FROM schema_migrations ORDER BY version ASC;")
        return [row[0] for row in cursor.fetchall()]

    def apply_migrations(self, migrations: List[Tuple[int, str, str]]):
        """
        migrations is a list of tuples: (version, migration_name, sql_script)
        """
        applied = set(self.get_applied_versions())
        for version, name, sql_script in sorted(migrations, key=lambda m: m[0]):
            if version in applied:
                continue
            with self.conn:
                self.conn.executescript(sql_script)
                self.conn.execute(
                    "INSERT INTO schema_migrations (version, name) VALUES (?, ?);",
                    (version, name)
                )


def q8_schema_migrations_engine():
    conn = sqlite3.connect(":memory:")
    engine = MigrationEngine(conn)

    migrations = [
        (1, "create_customers_table", """
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE
            );
        """),
        (2, "add_customer_metadata", """
            ALTER TABLE customers ADD COLUMN created_year INTEGER DEFAULT 2024;
            CREATE INDEX idx_customers_year ON customers(created_year);
        """),
    ]

    engine.apply_migrations(migrations)
    assert engine.get_applied_versions() == [1, 2]

    # Insert data against migrated schema
    conn.execute("INSERT INTO customers (email, created_year) VALUES ('vip@corp.io', 2025);")
    conn.commit()

    cursor = conn.execute("SELECT email, created_year FROM customers WHERE email = 'vip@corp.io';")
    row = cursor.fetchone()
    assert row[0] == "vip@corp.io"
    assert row[1] == 2025

    # Re-running migrations is idempotent
    engine.apply_migrations(migrations)
    assert engine.get_applied_versions() == [1, 2]

    conn.close()
    print("=== Q8: Automated Schema Migration Engine Verified ===")


# =====================================================================
# Q9: In-Memory Full-Text Search (FTS5) Engine
# =====================================================================
def q9_full_text_search_fts5():
    """
    Demonstrates SQLite's built-in FTS5 virtual table engine for rapid keyword searching,
    phrase queries, and BM25 relevance ranking.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create FTS5 virtual table
    cursor.execute("""
        CREATE VIRTUAL TABLE articles USING fts5(
            title,
            body,
            tokenize='porter ascii'
        );
    """)

    articles = [
        ("Python Concurrency", "Learn threading, multiprocessing, and asyncio for scalable Python backends."),
        ("PostgreSQL vs SQLite", "Comparing embedded SQLite storage engines with client-server PostgreSQL databases."),
        ("Machine Learning Systems", "Building neural network pipelines using Python, PyTorch, and distributed training.")
    ]
    cursor.executemany("INSERT INTO articles (title, body) VALUES (?, ?);", articles)
    conn.commit()

    # Search for token "concurrency" (stemmed by porter tokenizer)
    cursor.execute("SELECT title FROM articles WHERE articles MATCH 'concurrency';")
    res1 = cursor.fetchall()
    assert len(res1) == 1
    assert res1[0][0] == "Python Concurrency"

    # Search for "Python AND (asyncio OR database)"
    cursor.execute("SELECT title FROM articles WHERE articles MATCH 'Python AND asyncio';")
    res2 = cursor.fetchall()
    assert len(res2) == 1
    assert res2[0][0] == "Python Concurrency"

    # Search with prefix matching "distribut*"
    cursor.execute("SELECT title FROM articles WHERE articles MATCH 'distribut*';")
    res3 = cursor.fetchall()
    assert len(res3) == 1
    assert res3[0][0] == "Machine Learning Systems"

    conn.close()
    print("=== Q9: Full-Text Search (FTS5) Engine Verified ===")


# =====================================================================
# Q10: Architectural Repository Pattern with Context Management
# =====================================================================
class UserRepository:
    """
    Encapsulates database access for the User domain model following the
    Enterprise Repository Pattern with automatic schema initialization.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    role TEXT NOT NULL DEFAULT 'viewer'
                );
            """)

    def create(self, username: str, email: str, role: str = "viewer") -> int:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO users (username, email, role) VALUES (?, ?, ?);",
                (username, email, role)
            )
            return cursor.lastrowid

    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM users WHERE username = ?;", (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_role(self, user_id: int, new_role: str) -> bool:
        with self.conn:
            cursor = self.conn.execute(
                "UPDATE users SET role = ? WHERE id = ?;",
                (new_role, user_id)
            )
            return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        with self.conn:
            cursor = self.conn.execute("DELETE FROM users WHERE id = ?;", (user_id,))
            return cursor.rowcount > 0

    def list_all(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM users ORDER BY id ASC;")
        return [dict(r) for r in cursor.fetchall()]

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def q10_architectural_repository_pattern():
    with UserRepository(":memory:") as repo:
        # Create
        u1_id = repo.create("antigravity", "agent@deepmind.com", "admin")
        u2_id = repo.create("coder_bob", "bob@example.com", "developer")

        assert u1_id == 1
        assert u2_id == 2

        # Read
        u1 = repo.get_by_id(u1_id)
        assert u1["username"] == "antigravity"
        assert u1["role"] == "admin"

        u2 = repo.get_by_username("coder_bob")
        assert u2["email"] == "bob@example.com"

        # Update
        updated = repo.update_role(u2_id, "lead_developer")
        assert updated is True
        assert repo.get_by_id(u2_id)["role"] == "lead_developer"

        # List all
        all_users = repo.list_all()
        assert len(all_users) == 2

        # Delete
        deleted = repo.delete(u1_id)
        assert deleted is True
        assert repo.get_by_id(u1_id) is None
        assert len(repo.list_all()) == 1

    print("=== Q10: Architectural Repository Pattern Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_connection_ddl_and_constraints()
    q2_sql_injection_defense()
    q3_crud_operations()
    q4_row_factories()
    q5_transactions_and_savepoints()
    q6_batch_executemany_and_streaming()
    q7_custom_udfs_and_aggregates()
    q8_schema_migrations_engine()
    q9_full_text_search_fts5()
    q10_architectural_repository_pattern()

    print("\nAll 10 SQLite database practice questions passed successfully!")
