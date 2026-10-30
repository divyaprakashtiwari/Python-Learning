"""
Question 4: Enterprise SQLite Repository with Parameterized Queries & ACID Transactions
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- SQLite connection management, row_factory = sqlite3.Row, foreign key PRAGMA
- Parameterized CRUD operations preventing SQL injection
- Transaction management using context manager (with conn:)
- Atomic batch operations with automatic rollback on constraint violations
- Safe error handling and resource cleanup
"""

import sqlite3
from typing import Dict, Any, Optional, List


class ProductRepository:
    """
    Enterprise SQLite repository managing relational tables,
    schema migrations, parameterized queries, and ACID transactions.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON;")

    def init_schema(self) -> None:
        """Creates normalized categories and products tables."""
        with self._conn:
            self._conn.executescript("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    price REAL NOT NULL CHECK(price >= 0),
                    stock INTEGER NOT NULL DEFAULT 0,
                    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
                    created_at TEXT NOT NULL DEFAULT (datetime('now'))
                );
            """)

    def add_category(self, name: str) -> int:
        """Inserts a new product category and returns its ID."""
        with self._conn:
            cursor = self._conn.execute(
                "INSERT INTO categories (name) VALUES (?);", (name,)
            )
            return cursor.lastrowid  # type: ignore[return-value]

    def create_product(self, product: Dict[str, Any]) -> int:
        """Inserts a single product using parameterized placeholders."""
        with self._conn:
            cursor = self._conn.execute(
                """
                INSERT INTO products (sku, name, price, stock, category_id)
                VALUES (:sku, :name, :price, :stock, :category_id);
                """,
                product,
            )
            return cursor.lastrowid  # type: ignore[return-value]

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves product details as a dictionary or None."""
        cursor = self._conn.execute(
            """
            SELECT p.id, p.sku, p.name, p.price, p.stock, p.category_id, c.name AS category_name, p.created_at
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?;
            """,
            (product_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def update_stock(self, product_id: int, quantity_delta: int) -> bool:
        """Adjusts product stock atomically."""
        with self._conn:
            cursor = self._conn.execute(
                """
                UPDATE products
                SET stock = stock + ?
                WHERE id = ? AND (stock + ?) >= 0;
                """,
                (quantity_delta, product_id, quantity_delta),
            )
            return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        """Deletes a product by ID."""
        with self._conn:
            cursor = self._conn.execute("DELETE FROM products WHERE id = ?;", (product_id,))
            return cursor.rowcount > 0

    def try_batch_insert(self, products: List[Dict[str, Any]]) -> bool:
        """
        Attempts to batch insert products within a single transaction.
        If any record fails, rolls back completely and returns True to indicate rollback occurred.
        """
        try:
            with self._conn:
                self._conn.executemany(
                    """
                    INSERT INTO products (sku, name, price, stock, category_id)
                    VALUES (:sku, :name, :price, :stock, :category_id);
                    """,
                    products,
                )
            return False  # Successfully inserted without rollback
        except sqlite3.IntegrityError as err:
            print(f"Batch Insertion Exception Handled: sqlite3.IntegrityError - {err}")
            return True  # Rollback occurred

    def close(self) -> None:
        """Closes the underlying database connection."""
        self._conn.close()


if __name__ == "__main__":
    repo = ProductRepository(db_path=":memory:")
    repo.init_schema()

    print("=== 1. Category and Product Creation ===")
    cat_id = repo.add_category("Electronics")
    print(f"Category Created ID: {cat_id}")

    prod_id = repo.create_product({
        "sku": "SKU-LAP-001",
        "name": "Ultra Laptop 15-inch",
        "price": 1299.99,
        "stock": 25,
        "category_id": cat_id,
    })
    print(f"Product Created ID: {prod_id}, SKU: 'SKU-LAP-001'")

    print("\n=== 2. Product Retrieval & Stock Adjustment ===")
    prod = repo.get_product_by_id(prod_id)
    print(f"Initial Stock: {prod['stock'] if prod else 'N/A'}")

    repo.update_stock(prod_id, quantity_delta=-5)  # sell 5 units
    updated_prod = repo.get_product_by_id(prod_id)
    print(f"Updated Stock (after -5 delta): {updated_prod['stock'] if updated_prod else 'N/A'}")

    print("\n=== 3. Batch Insert with Atomic Rollback on Constraint Violation ===")
    invalid_batch = [
        {"sku": "SKU-MOU-001", "name": "Wireless Mouse", "price": 29.99, "stock": 50, "category_id": cat_id},
        {"sku": "SKU-LAP-001", "name": "Duplicate SKU Laptop", "price": 999.00, "stock": 5, "category_id": cat_id},  # Duplicate SKU!
    ]
    rollback_occurred = repo.try_batch_insert(invalid_batch)

    # Verify Wireless Mouse was NOT inserted due to rollback
    cursor = repo._conn.execute("SELECT * FROM products WHERE sku = 'SKU-MOU-001';")
    mou_inserted = cursor.fetchone() is not None
    print(f"Rollback Verified: Duplicate batch was rolled back; Wireless Mouse was NOT inserted: {not mou_inserted}")

    repo.close()
