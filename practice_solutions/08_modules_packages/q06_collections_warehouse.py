"""
Topic 08 - Modules and Packages: Question 6
Problem: Warehouse Inventory and Fulfillment Tracker coordinating collections module structures.
"""

from collections import Counter, defaultdict, deque, namedtuple, OrderedDict
from typing import Any, Dict, List, Tuple


class WarehouseFulfillmentTracker:
    """Manages warehouse cataloging, inventory arithmetic, queues, and LRU cache via collections."""

    # 1. Schema-Enforced Records with namedtuple
    ItemRecord = namedtuple("ItemRecord", ["sku", "category", "unit_cost", "quantity"])

    # 2. Grouped Cataloging with defaultdict
    def build_category_index(self, items: List[ItemRecord]) -> Dict[str, Any]:
        """Categorizes items and aggregates total valuation using defaultdict."""
        catalog = defaultdict(list)
        valuations = defaultdict(float)

        for item in items:
            catalog[item.category].append(item)
            valuations[item.category] += item.unit_cost * item.quantity

        return {
            cat: {"count": len(items_list), "total_cost": valuations[cat]}
            for cat, items_list in catalog.items()
        }

    # 3. Inventory Balance Arithmetic with Counter
    def reconcile_inventory(
        self,
        initial_stock: Dict[str, int],
        dispatches: List[ItemRecord],
        returns: List[ItemRecord]
    ) -> Counter:
        """Applies net inventory movements using Counter.subtract and Counter.update."""
        stock = Counter(initial_stock)

        # Subtract dispatches
        disp_counter = Counter({item.sku: item.quantity for item in dispatches})
        stock.subtract(disp_counter)

        # Add returns
        ret_counter = Counter({item.sku: item.quantity for item in returns})
        stock.update(ret_counter)

        return stock


# 4. High-Throughput Queue Buffering with deque
class OrderDispatchQueue:
    """O(1) bi-directional dispatch queue with VIP prioritization."""

    def __init__(self, max_capacity: int = 100):
        self._queue: deque = deque(maxlen=max_capacity)

    def enqueue_standard(self, order_id: str) -> None:
        self._queue.append(order_id)

    def enqueue_expedited_vip(self, order_id: str) -> None:
        self._queue.appendleft(order_id)

    def dispatch_next(self) -> str:
        if not self._queue:
            raise IndexError("Dispatch queue is empty")
        return self._queue.popleft()


# 5. Recency Cache Tracking with OrderedDict (LRU)
class LRUCatalogCache:
    """Fixed-capacity Least-Recently-Used cache using OrderedDict."""

    def __init__(self, capacity: int = 3):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()

    def get(self, key: str) -> Any:
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: str, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


# Verification & Execution
tracker = WarehouseFulfillmentTracker()

items = [
    tracker.ItemRecord("SKU-A", "Electronics", 120.0, 5),
    tracker.ItemRecord("SKU-B", "Electronics", 45.0, 10),
    tracker.ItemRecord("SKU-C", "Apparel", 25.0, 20)
]

initial = {"SKU-A": 50, "SKU-B": 30, "SKU-C": 100}
dispatched = [
    tracker.ItemRecord("SKU-A", "Electronics", 120.0, 15),
    tracker.ItemRecord("SKU-C", "Apparel", 25.0, 40)
]
returned = [tracker.ItemRecord("SKU-A", "Electronics", 120.0, 2)]

updated_stock = tracker.reconcile_inventory(initial, dispatched, returned)
top_stock = updated_stock.most_common(2)

print("Reconciled Stock Counts:")
print(f"- SKU-A: {updated_stock['SKU-A']} (50 - 15 + 2)")
print(f"- SKU-B: {updated_stock['SKU-B']} (30 - 0)")
print(f"- SKU-C: {updated_stock['SKU-C']} (100 - 40)")
print(f"Top 2 Stocked Items: {top_stock}")

# Queue verification
dq = OrderDispatchQueue(max_capacity=10)
print("\nDispatch Queue Operations:")
dq.enqueue_standard("ORD-101")
print("- Enqueue Standard ORD-101")
dq.enqueue_expedited_vip("ORD-999")
print("- Enqueue Expedited VIP ORD-999")
next_ord = dq.dispatch_next()
print(f"- Next Dispatched: {next_ord} (Expedited processed first)")

# Category Catalog
cat_summary = tracker.build_category_index(items)
print("\nCategory Catalog:")
for cat, info in cat_summary.items():
    print(f"- {cat}: {info['count']} items, Total Cost: ${info['total_cost']:.2f}")
