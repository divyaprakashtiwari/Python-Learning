"""
Phase 5 - Topic 13: Shallow Copy vs Deep Copy
Example 02: The Nested Mutable Trap in Shallow Copies (`copy.copy` vs `copy.deepcopy`)

Demonstrates:
  - How a shallow copy of a nested dictionary/list shares references to inner mutable objects
  - How mutating an inner list in a shallow copy corrupts the original structure
  - How `copy.deepcopy()` recursively clones all nested mutable objects
"""

import copy


def main() -> None:
    base_template = {
        "env": "production",
        "Ports": [80, 443],
    }

    print("=== 1. Shallow Copy Shares Inner Mutable References ===")
    shallow_cfg = copy.copy(base_template)
    print(f"  Outer dicts distinct (`is`)? : {base_template is not shallow_cfg}")
    print(f"  Inner lists SHARED (`is`)?   : {base_template['Ports'] is shallow_cfg['Ports']}")

    shallow_cfg["Ports"].append(8080)  # Mutates the shared inner list!
    print(f"  base_template after shallow inner mutation: {base_template} (CORRUPTED!)")

    print("\n=== 2. Deep Copy (`copy.deepcopy`) Isolates All Nested Levels ===")
    clean_template = {"env": "production", "Ports": [80, 443]}
    deep_cfg = copy.deepcopy(clean_template)
    print(f"  Inner lists SHARED (`is`)?   : {clean_template['Ports'] is deep_cfg['Ports']}")

    deep_cfg["Ports"].append(9090)
    print(f"  clean_template : {clean_template} (completely untouched!)")
    print(f"  deep_cfg       : {deep_cfg}")


if __name__ == "__main__":
    main()
