"""
Phase 4 - Topic 06: Multiple Inheritance
Example 01: The Diamond Problem and C3 Linearization (`__mro__` & `mro()`)

Demonstrates:
  - How Multiple Inheritance (`class D(B, C):` where `B(A)` and `C(A)`) forms a Diamond
  - How Python's C3 Linearization algorithm computes a deterministic Method Resolution Order (MRO)
  - Why cooperative `super()` calls each class in the diamond ONCE instead of calling `A` twice!
"""


class BaseNode:
    """Top of the diamond (Class A)."""

    def process(self) -> list[str]:
        return ["BaseNode.process"]


class AuthLayer(BaseNode):
    """Left branch of the diamond (Class B)."""

    def process(self) -> list[str]:
        return ["AuthLayer.process"] + super().process()


class RateLimitLayer(BaseNode):
    """Right branch of the diamond (Class C)."""

    def process(self) -> list[str]:
        return ["RateLimitLayer.process"] + super().process()


class APIGatewayEndpoint(AuthLayer, RateLimitLayer):
    """Bottom of the diamond (Class D inheriting from B and C)."""

    def process(self) -> list[str]:
        return ["APIGatewayEndpoint.process"] + super().process()


def main() -> None:
    print("=== 1. Inspecting C3 Linearization MRO (`APIGatewayEndpoint.mro()`) ===")
    mro_names = [cls.__name__ for cls in APIGatewayEndpoint.mro()]
    print(f"  MRO : {' -> '.join(mro_names)}")

    print("\n=== 2. Cooperative `super()` Traversal Across the Diamond ===")
    endpoint = APIGatewayEndpoint()
    execution_chain = endpoint.process()
    for step_idx, step_name in enumerate(execution_chain, start=1):
        print(f"  Step {step_idx}: {step_name}")
    print(f"  Notice `BaseNode.process` ran exactly ONCE (not twice)!")


if __name__ == "__main__":
    main()
