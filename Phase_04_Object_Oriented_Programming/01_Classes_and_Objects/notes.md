# Phase 4 — Topic 01: Classes and Objects

## 1. Introduction

**Object-Oriented Programming (OOP)** is a programming paradigm that organizes software around **objects** that bundle together **state (attributes/data)** and **behavior (methods/functions)** rather than keeping data and functions separate.

- **Class (The Blueprint):** A user-defined type created with the `class` keyword (e.g., `class SmartThermostat:`) that specifies what attributes and methods its instances will have.
- **Object / Instance (The Concrete Product):** A live in-memory entity created by calling the class (`living_room = SmartThermostat("Living Room", 21.5, 24.0)`). One class can produce thousands of independent objects, each maintaining its own state in memory.

---

## 2. Why is it used?

- **Cohesion (Bundling State + Rules):** Instead of passing loose dictionaries around (`reserve_stock(product_dict, qty)`) where any caller might corrupt `product_dict["stock"] = -99`, a `Product` class bundles `self.stock` together with validated methods like `product.reserve_stock(qty)`.
- **Modeling Real-World & System Entities:** Database models (`User`, `Order`), network clients (`HTTPClient`), GUI widgets, and DSA nodes (`ListNode`, `TreeNode`, `Graph`) map naturally to classes.
- **Extensibility:** Classes unlock inheritance, polymorphism, encapsulation, and operator overloading (`__add__`, `__len__`, `__repr__`).

---

## 3. Syntax

```python
# 1. Defining a Class (PEP 8 uses PascalCase / CapWords for class names)
class SmartThermostat:
    def __init__(self, room_name: str, current_temp_c: float, target_temp_c: float) -> None:
        # Instance attributes stored on `self`
        self.room_name = room_name
        self.current_temp_c = current_temp_c
        self.target_temp_c = target_temp_c

    def heating_status(self) -> str:
        # Instance method: `self` refers to the specific object calling the method
        if self.current_temp_c < self.target_temp_c:
            return "HEATING"
        return "IDLE"


# 2. Instantiating Objects (Calling the class like a function)
thermostat_1 = SmartThermostat("Living Room", 21.5, 24.0)
thermostat_2 = SmartThermostat("Bedroom", 25.0, 22.0)

# 3. Accessing Attributes and Calling Methods via Dot (`.`) Notation
print(thermostat_1.room_name)         # "Living Room"
print(thermostat_1.heating_status())  # "HEATING"
```

---

## 4. Explanation (Step-by-Step)

### Step 1: What Happens When You Call `SmartThermostat("Living Room", 21.5, 24.0)`?
1. Python calls `SmartThermostat.__new__(SmartThermostat)` to allocate a blank `SmartThermostat` instance in heap memory.
2. Python automatically calls `SmartThermostat.__init__(instance, "Living Room", 21.5, 24.0)`, passing the newly created object as the first parameter **`self`**.
3. Inside `__init__`, `self.room_name = room_name` stores the attribute inside the object's internal dictionary (`instance.__dict__`).
4. Python returns the initialized object reference to the caller.

### Step 2: What Is `self`?
`self` is **not** a reserved keyword in Python, though it is an unbreakable PEP 8 convention. When you call `living_room.heating_status()` with zero arguments inside the parentheses, Python automatically translates that method call into:
```python
SmartThermostat.heating_status(living_room)
```
That is why every instance method definition **must** declare `self` as its first parameter!

### Step 3: How Python Stores Object Attributes (`__dict__` vs `__slots__`)
- By default, every custom object has a dictionary named **`obj.__dict__`** mapping attribute names (`"hostname"`) to their values (`"api-prod-01"`). This allows adding attributes dynamically at runtime, at the cost of extra memory per instance.
- Declaring **`__slots__ = ("timestamp", "cpu_load")`** on a class tells Python to store attributes in a compact C-level array instead of allocating a `__dict__` per instance—saving 40–60% memory when creating millions of small objects (like `TreeNode` or `MetricPoint`) and preventing accidental attribute typos!

---

## 5. Minimum 3 Examples

### Example 1: Defining a Class Blueprint and Instantiating Independent Objects
File: `example_01_defining_classes_and_instantiating_objects.py`

```python
class SmartThermostat:
    """Blueprint for a smart home thermostat device."""

    def __init__(self, room_name: str, current_temp_c: float, target_temp_c: float) -> None:
        self.room_name = room_name
        self.current_temp_c = current_temp_c
        self.target_temp_c = target_temp_c

    def heating_status(self) -> str:
        """Return whether the thermostat is HEATING, COOLING, or IDLE."""
        if self.current_temp_c < self.target_temp_c:
            return "HEATING"
        if self.current_temp_c > self.target_temp_c:
            return "COOLING"
        return "IDLE"

    def describe(self) -> str:
        """Return a formatted status line for this thermostat instance."""
        return (
            f"[{self.room_name:<12}] Current: {self.current_temp_c:.1f}C | "
            f"Target: {self.target_temp_c:.1f}C | Mode: {self.heating_status()}"
        )


def main() -> None:
    print("=== 1. Instantiating Multiple Independent Objects from One Class ===")
    living_room = SmartThermostat("Living Room", 21.5, 24.0)
    bedroom = SmartThermostat("Master Bed", 26.0, 22.0)
    study = SmartThermostat("Home Office", 23.0, 23.0)

    for device in (living_room, bedroom, study):
        print(f"  {device.describe()}")

    print("\n=== 2. Modifying State on One Instance Does Not Affect Others ===")
    living_room.current_temp_c = 24.0
    print(f"  Updated Living Room : {living_room.describe()}")
    print(f"  Unchanged Bedroom   : {bedroom.describe()}")

    print("\n=== 3. How `self` Works Under the Hood ===")
    # `living_room.heating_status()` is syntactic sugar for:
    bound_result = living_room.heating_status()
    unbound_result = SmartThermostat.heating_status(living_room)
    print(f"  living_room.heating_status()                 -> {bound_result}")
    print(f"  SmartThermostat.heating_status(living_room)  -> {unbound_result}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Object Identity (`is` vs `==`), Type Inspection (`isinstance`), and `__dict__`
File: `example_02_object_identity_type_and_namespace_dict.py`

```python
class ServerNode:
    """Standard class backed by a per-instance `__dict__` namespace."""

    def __init__(self, hostname: str, ip_address: str) -> None:
        self.hostname = hostname
        self.ip_address = ip_address


class CompactMetricPoint:
    """Memory-efficient class using `__slots__` (no per-instance `__dict__`)."""

    __slots__ = ("timestamp", "cpu_load")

    def __init__(self, timestamp: int, cpu_load: float) -> None:
        self.timestamp = timestamp
        self.cpu_load = cpu_load


def main() -> None:
    print("=== 1. Object Identity (`is`) vs Attribute Values ===")
    node_a = ServerNode("api-prod-01", "10.0.1.15")
    node_b = ServerNode("api-prod-01", "10.0.1.15")
    node_alias = node_a

    print(f"  node_a is node_b        : {node_a is node_b} (two separate objects in memory)")
    print(f"  node_a is node_alias    : {node_a is node_alias} (alias to same object)")
    print(f"  isinstance(node_a, ServerNode) : {isinstance(node_a, ServerNode)}")
    print(f"  isinstance(node_a, object)     : {isinstance(node_a, object)} (all classes inherit from object)")

    print("\n=== 2. Inspecting the Instance Namespace (`obj.__dict__`) ===")
    print(f"  Initial node_a.__dict__ : {node_a.__dict__}")
    # Dynamically adding a new attribute at runtime updates `node_a.__dict__`
    node_a.region = "ap-south-1"
    print(f"  After adding `.region`  : {node_a.__dict__}")
    print(f"  node_b.__dict__         : {node_b.__dict__} (unaffected!)")

    print("\n=== 3. Preventing Accidental Dynamic Attributes with `__slots__` ===")
    metric = CompactMetricPoint(1730716800, 0.74)
    print(f"  metric.timestamp={metric.timestamp}, metric.cpu_load={metric.cpu_load}")
    print(f"  Has `__dict__`?         : {hasattr(metric, '__dict__')}")
    try:
        metric.typo_attribute = 99.9
    except AttributeError as err:
        print(f"  Caught expected AttributeError: {err}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Collaborating Objects (E-Commerce Order & Product Domain Model)
File: `example_03_bank_account_domain_model.py`

```python
class Product:
    """Represents a catalog item with SKU, name, unit price, and available stock."""

    def __init__(self, sku: str, name: str, price: float, stock: int) -> None:
        self.sku = sku
        self.name = name
        self.price = price
        self.stock = stock

    def reserve_stock(self, quantity: int) -> bool:
        """Deduct `quantity` from `self.stock` if available; return True on success."""
        if quantity <= 0 or quantity > self.stock:
            return False
        self.stock -= quantity
        return True


class Order:
    """Represents a customer order containing line items of `Product` objects."""

    def __init__(self, order_id: str, customer_name: str) -> None:
        self.order_id = order_id
        self.customer_name = customer_name
        self.line_items: list[tuple[Product, int]] = []

    def add_product(self, product: Product, quantity: int) -> str:
        """Attempt to reserve stock and add `(product, quantity)` to the order."""
        if not product.reserve_stock(quantity):
            return (
                f"FAILED: Cannot add {quantity}x '{product.name}' "
                f"(only {product.stock} in stock)"
            )
        self.line_items.append((product, quantity))
        return f"ADDED : {quantity}x '{product.name}' @ INR {product.price:,.2f}"

    def total_amount(self) -> float:
        """Calculate the grand total across all reserved line items."""
        return round(sum(prod.price * qty for prod, qty in self.line_items), 2)

    def print_invoice(self) -> None:
        """Print a formatted invoice summary."""
        print(f"  Invoice {self.order_id} | Customer: {self.customer_name}")
        for prod, qty in self.line_items:
            line_total = prod.price * qty
            print(f"    - {prod.sku} | {prod.name:<18} x{qty} = INR {line_total:,.2f}")
        print(f"    Total Payable: INR {self.total_amount():,.2f}")


def main() -> None:
    print("=== 1. Creating Catalog Product Objects ===")
    laptop = Product("SKU-101", "ThinkPad Laptop", 85000.0, stock=3)
    mouse = Product("SKU-202", "Wireless Mouse", 1500.0, stock=10)

    print("=== 2. Collaborating Objects: Building an Order ===")
    order = Order("ORD-9001", "Divya Prakash")
    print(f"  {order.add_product(laptop, 1)}")
    print(f"  {order.add_product(mouse, 2)}")
    print(f"  {order.add_product(laptop, 5)}")  # Exceeds remaining stock (2)

    print("\n=== 3. Final Invoice & Updated Product Stock ===")
    order.print_invoice()
    print(f"  Remaining stock -> {laptop.name}: {laptop.stock}, {mouse.name}: {mouse.stock}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_defining_classes_and_instantiating_objects.py`)
```text
=== 1. Instantiating Multiple Independent Objects from One Class ===
  [Living Room ] Current: 21.5C | Target: 24.0C | Mode: HEATING
  [Master Bed  ] Current: 26.0C | Target: 22.0C | Mode: COOLING
  [Home Office ] Current: 23.0C | Target: 23.0C | Mode: IDLE

=== 2. Modifying State on One Instance Does Not Affect Others ===
  Updated Living Room : [Living Room ] Current: 24.0C | Target: 24.0C | Mode: IDLE
  Unchanged Bedroom   : [Master Bed  ] Current: 26.0C | Target: 22.0C | Mode: COOLING

=== 3. How `self` Works Under the Hood ===
  living_room.heating_status()                 -> IDLE
  SmartThermostat.heating_status(living_room)  -> IDLE
```

### Output — Example 2 (`example_02_object_identity_type_and_namespace_dict.py`)
```text
=== 1. Object Identity (`is`) vs Attribute Values ===
  node_a is node_b        : False (two separate objects in memory)
  node_a is node_alias    : True (alias to same object)
  isinstance(node_a, ServerNode) : True
  isinstance(node_a, object)     : True (all classes inherit from object)

=== 2. Inspecting the Instance Namespace (`obj.__dict__`) ===
  Initial node_a.__dict__ : {'hostname': 'api-prod-01', 'ip_address': '10.0.1.15'}
  After adding `.region`  : {'hostname': 'api-prod-01', 'ip_address': '10.0.1.15', 'region': 'ap-south-1'}
  node_b.__dict__         : {'hostname': 'api-prod-01', 'ip_address': '10.0.1.15'} (unaffected!)

=== 3. Preventing Accidental Dynamic Attributes with `__slots__` ===
  metric.timestamp=1730716800, metric.cpu_load=0.74
  Has `__dict__`?         : False
  Caught expected AttributeError: 'CompactMetricPoint' object has no attribute 'typo_attribute' and no __dict__ for setting new attributes
```

### Output — Example 3 (`example_03_bank_account_domain_model.py`)
```text
=== 1. Creating Catalog Product Objects ===
=== 2. Collaborating Objects: Building an Order ===
  ADDED : 1x 'ThinkPad Laptop' @ INR 85,000.00
  ADDED : 2x 'Wireless Mouse' @ INR 1,500.00
  FAILED: Cannot add 5x 'ThinkPad Laptop' (only 2 in stock)

=== 3. Final Invoice & Updated Product Stock ===
  Invoice ORD-9001 | Customer: Divya Prakash
    - SKU-101 | ThinkPad Laptop    x1 = INR 85,000.00
    - SKU-202 | Wireless Mouse     x2 = INR 3,000.00
    Total Payable: INR 88,000.00
  Remaining stock -> ThinkPad Laptop: 2, Wireless Mouse: 8
```

---

## 7. Code Explanation

1. **Method Binding (`example_01`):** `living_room.heating_status()` is a **bound method** call. Accessing `heating_status` on the instance `living_room` automatically binds `self = living_room`. Accessing `SmartThermostat.heating_status` on the class returns the underlying function, which requires passing `living_room` explicitly.
2. **Universal Base Class `object` (`example_02`):** In Python 3, every class implicitly inherits from `object` (`class ServerNode:` is identical to `class ServerNode(object):`), so `isinstance(node_a, object)` is always `True`.
3. **Collaborating Objects (`example_03`):** `Order` holds a list of `(Product, int)` tuples and delegates stock validation to `product.reserve_stock(quantity)` rather than reaching into `product.stock` directly.

---

## 8. Common Mistakes

1. **Forgetting `self` as the first parameter of an instance method:**
   ```python
   class Counter:
       def reset():  # <-- Missing `self`!
           pass
   c = Counter()
   c.reset()  # TypeError: Counter.reset() takes 0 positional arguments but 1 was given
   ```
   The `"1 was given"` in that famous error message is `c` (`self`) being passed automatically by Python!
2. **Forgetting `self.` when reading or assigning an instance attribute inside a method:**
   - Writing `room_name = "Kitchen"` inside a method creates a temporary **local variable** that vanishes when the method returns instead of updating `self.room_name`.
3. **Forgetting parentheses `()` when instantiating a class:**
   - Writing `order = Order` binds `order` to the **class object itself** instead of creating a new `Order` instance! Always call `Order(...)`.

---

## 9. Practice Questions

1. **Easy — `Rectangle` Class:**
   Create a `Rectangle` class with `width` and `height` attributes and methods `area()`, `perimeter()`, and `is_square() -> bool`. Instantiate two rectangles and print their metrics.

2. **Medium — `Stopwatch` State Machine:**
   Create a `Stopwatch` class with attributes `elapsed_sec: float = 0.0` and `is_running: bool = False`, and methods `start()`, `record_lap(seconds: float)`, `stop()`, and `reset()` that prevent recording laps when the stopwatch is stopped.

3. **Hard — `Library` and `Book` Collaborating Objects:**
   Create a `Book(isbn, title, author, available_copies)` class and a `Member(member_id, name)` class where `member.borrow_book(book)` and `member.return_book(book)` maintain both `book.available_copies` and `member.borrowed_books` without allowing duplicate borrows of the same ISBN.

---

## 10. Interview Questions

### Q1: Why does `c.method()` raise `TypeError: method() takes 0 positional arguments but 1 was given` when `def method():` is defined without `self`?
**Answer:**
When a function defined inside a class is accessed through an instance (`c.method`), Python's descriptor protocol turns it into a **bound method** that automatically prepends the instance `c` as the first positional argument (`Class.method(c)`). If the method signature has 0 parameters (`def method():`), passing `c` supplies 1 positional argument to a 0-parameter function, raising `TypeError`.

### Q2: By default, what does `node_a == node_b` return for two instances of a custom class with identical attribute values?
**Answer:**
 **`False`!** Unless a custom class overrides `__eq__` (or uses `@dataclass`), it inherits `object.__eq__`, which compares **memory identity (`node_a is node_b`)** rather than comparing `node_a.__dict__ == node_b.__dict__`.

### Q3: What is `__slots__` in Python classes, and what are its pros and cons?
**Answer:**
Declaring `__slots__ = ("attr1", "attr2")` tells Python not to allocate a dynamic `__dict__` dictionary for each instance, instead reserving fixed-offset descriptors on the class.
- **Pros:** Reduces per-instance memory footprint by 40–60%, speeds up attribute access slightly, and prevents accidental attribute creation via typos.
- **Cons:** Prevents dynamically adding new attributes at runtime, requires subclasses to also declare `__slots__` to keep the memory savings, and does not support weak references unless `"__weakref__"` is included in `__slots__`.
