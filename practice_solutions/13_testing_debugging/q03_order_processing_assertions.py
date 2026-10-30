"""
Question 3: Order Processing Engine & Specialized unittest Assertions
Topic: Testing, Debugging, and Profiling

Key Concepts Tested:
- Specialized assertions: assertAlmostEqual, assertCountEqual, assertDictEqual, assertIs, assertIn, assertIsInstance
- Structured exception verification via with self.assertRaises(Exc) as ctx:
- Exception attribute inspection (field, code, message)
- Diagnostic diffs and assertion precision
"""

import unittest
from typing import List, Dict, Any, Optional


class OrderValidationError(Exception):
    """Structured exception indicating business validation failures in orders."""

    def __init__(self, field: str, code: str, message: str) -> None:
        super().__init__(f"[{code}] {field}: {message}")
        self.field = field
        self.code = code
        self.message = message


DEFAULT_SENTINEL = object()


class OrderProcessingEngine:
    """
    E-commerce order calculation engine applying discounts, tax, and shipping.
    """

    def calculate_order(
        self,
        items: List[Dict[str, Any]],
        discount_pct: float = 0.0,
        tax_rate: float = 0.08,
        shipping: float = 10.0,
        promos: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        if not items:
            raise OrderValidationError(field="items", code="EMPTY_ITEMS", message="Order must contain at least one item")

        if discount_pct < 0.0 or discount_pct > 100.0:
            raise OrderValidationError(
                field="discount_pct",
                code="DISCOUNT_OVERFLOW",
                message=f"Discount must be in 0..100%, got: {discount_pct}",
            )

        subtotal = 0.0
        for idx, item in enumerate(items):
            qty = item.get("quantity", 0)
            price = item.get("price", 0.0)
            if qty <= 0:
                raise OrderValidationError(field=f"items[{idx}].quantity", code="INVALID_QUANTITY", message="Quantity must be > 0")
            if price < 0.0:
                raise OrderValidationError(field=f"items[{idx}].price", code="INVALID_PRICE", message="Price cannot be negative")
            subtotal += qty * price

        discount_amount = round(subtotal * (discount_pct / 100.0), 2)
        taxable_amount = max(0.0, subtotal - discount_amount)
        tax = round(taxable_amount * tax_rate, 2)
        total = round(taxable_amount + tax + shipping, 2)

        applied_promos = list(promos) if promos else []
        if tax_rate == 0.08:
            applied_promos.append("TAX_NY_8pct")

        return {
            "subtotal": round(subtotal, 2),
            "discount_amount": discount_amount,
            "tax": tax,
            "shipping": round(shipping, 2),
            "total": total,
            "applied_promos": applied_promos,
        }


class TestOrderProcessingAssertions(unittest.TestCase):
    """
    Exhaustive assertion suite testing boundary conditions and verifying
    specialized unittest assertion capabilities.
    """

    def setUp(self) -> None:
        self.engine = OrderProcessingEngine()

    def test_floating_point_tax_precision(self) -> None:
        items = [{"quantity": 3, "price": 19.99}]  # subtotal = 59.97
        res = self.engine.calculate_order(items, discount_pct=10.0, tax_rate=0.0825, shipping=5.0)
        # Verify monetary precision within 2 decimal places and delta tolerance
        self.assertAlmostEqual(res["subtotal"], 59.97, places=2)
        self.assertAlmostEqual(res["total"], 63.43, delta=0.01)

    def test_discount_unordered_coupons(self) -> None:
        items = [{"quantity": 1, "price": 100.0}]
        promos_in = ["SUMMER_SAVINGS", "LOYALTY_MEMBER"]
        res = self.engine.calculate_order(items, discount_pct=15.0, promos=promos_in)
        # assertCountEqual compares collections regardless of order
        expected_promos = ["LOYALTY_MEMBER", "SUMMER_SAVINGS", "TAX_NY_8pct"]
        self.assertCountEqual(res["applied_promos"], expected_promos)

    def test_dict_summary_equality(self) -> None:
        items = [{"quantity": 2, "price": 50.0}]
        res = self.engine.calculate_order(items, discount_pct=0.0, tax_rate=0.08, shipping=10.0)
        expected = {
            "subtotal": 100.0,
            "discount_amount": 0.0,
            "tax": 8.0,
            "shipping": 10.0,
            "total": 118.0,
            "applied_promos": ["TAX_NY_8pct"],
        }
        self.assertDictEqual(res, expected)

    def test_singleton_sentinel_identity(self) -> None:
        # Contrasts value equality (assertEqual) with object identity (assertIs)
        s1 = DEFAULT_SENTINEL
        s2 = DEFAULT_SENTINEL
        self.assertIs(s1, s2)
        self.assertEqual(s1, s2)

    def test_type_and_collection_membership(self) -> None:
        items = [{"quantity": 1, "price": 40.0}]
        res = self.engine.calculate_order(items)
        self.assertIsInstance(res["total"], float)
        self.assertIn("TAX_NY_8pct", res["applied_promos"])

    def test_exception_context_payload(self) -> None:
        items = [{"quantity": 1, "price": 100.0}]
        with self.assertRaises(OrderValidationError) as ctx:
            self.engine.calculate_order(items, discount_pct=150.0)

        # Inspect exception attributes inside context manager
        self.assertEqual(ctx.exception.field, "discount_pct")
        self.assertEqual(ctx.exception.code, "DISCOUNT_OVERFLOW")
        self.assertIn("0..100%", ctx.exception.message)


if __name__ == "__main__":
    print("=== Running Specialized unittest Assertions Suite ===")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestOrderProcessingAssertions)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n=== Assertions Deep Dive Summary ===")
    print(f"Assertions Deep Dive Tests Run: {result.testsRun}")
    print(f"All Assertion Tests Succeeded: {result.wasSuccessful()}")
