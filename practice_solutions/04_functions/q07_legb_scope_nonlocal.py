"""
Topic 04 - Functions: Question 7
Problem: LEGB Scope Resolution, nonlocal and global keywords, and built-in shadowing.
"""

import builtins

# Module-level Global Scope
state_val = "GLOBAL"
print(f'Initial Global State: "{state_val}"')


def outer_scope():
    # Enclosing Scope
    state_val = "ENCLOSING"

    def read_local():
        # Local Scope
        state_val = "LOCAL"
        print(f'Local Resolution Inside inner(): "{state_val}"')

    def modify_nonlocal():
        nonlocal state_val
        state_val = "MODIFIED_BY_NONLOCAL"

    def modify_global():
        global state_val
        state_val = "MODIFIED_BY_GLOBAL"

    read_local()

    # Test nonlocal mutation
    modify_nonlocal()
    print("After modify_nonlocal():")
    print(f'- Enclosing state_val is now: "{state_val}"')
    # Print outer global state without accessing local
    print(f'- Global state_val is still: "{globals()["state_val"]}"')

    # Test global mutation
    modify_global()
    print("After modify_global():")
    print(f'- Enclosing state_val is still: "{state_val}"')
    print(f'- Global state_val is now: "{globals()["state_val"]}"')


outer_scope()

# 4. Built-in Shadowing & Recovery
print("Shadowed Built-in Recovery:")
# Shadow sum locally
sum_original = builtins.sum
sum = 42  # Shadows built-in sum in current module namespace

try:
    # Attempting to call integer sum
    sum([1, 2])  # type: ignore
except TypeError as err:
    print(f"- Attempted shadowed sum([1, 2]): Caught TypeError ({err})")

# Recover via standard builtins module
recovered_sum = builtins.sum([1, 2])
print(f"- Recovered via builtins.sum([1, 2]): {recovered_sum}")

# Clean up shadow
del sum
