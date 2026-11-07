"""
Phase 6 - Section A (Complexity Analysis) - Topic 04: Best, Average and Worst Cases
Example 02: Amortized Analysis — Dynamic Array (`list.append`) Resizing Cost

Demonstrates:
  - Why an operation with O(n) worst-case spikes (when a dynamic array doubles capacity
    and copies all elements) still has O(1) **amortized** cost per `.append()`
"""


def simulate_dynamic_array_appends(total_inserts: int) -> None:
    """Simulate a geometric 2x capacity-doubling dynamic array and count total element copies."""
    capacity = 1
    size = 0
    total_work = 0
    resize_events: list[tuple[int, int, int]] = []

    for i in range(1, total_inserts + 1):
        if size == capacity:
            # Worst-case spike: allocate 2x array and copy `size` existing elements
            copy_cost = size
            capacity *= 2
            total_work += copy_cost
            resize_events.append((i, capacity, copy_cost))
        # Normal O(1) write into pre-allocated slot
        size += 1
        total_work += 1

    print(f"=== Dynamic Array Simulation ({total_inserts} Appends) ===")
    for step, new_cap, copied in resize_events:
        print(f"  Append #{step:>2}: resized capacity to {new_cap:>2} (copied {copied:>2} existing items)")
    print(f"  Total work across {total_inserts} appends : {total_work} operations")
    print(f"  Amortized cost per append   : {total_work / total_inserts:.2f} ops/append (<= 3 -> O(1) amortized!)")


def main() -> None:
    simulate_dynamic_array_appends(17)


if __name__ == "__main__":
    main()
