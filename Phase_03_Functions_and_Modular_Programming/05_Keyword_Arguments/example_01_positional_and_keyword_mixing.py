"""
Phase 3 - Topic 05: Keyword Arguments
Example 01: Mixing Positional and Keyword Arguments & Ordering Rules

Demonstrates:
  - Calling functions using explicit `parameter_name=value` keyword syntax
  - Passing keyword arguments in any order for clarity
  - Combining positional arguments (first) with keyword arguments (after)
  - Handling `TypeError` when a parameter receives both a positional and keyword value
"""


def create_cloud_vm(
    instance_name: str,
    region: str,
    vcpus: int = 2,
    memory_gb: int = 8,
    preemptible: bool = False,
) -> str:
    """Return a summary of a provisioned virtual machine."""
    tier = "Spot/Preemptible" if preemptible else "On-Demand"
    return (
        f"VM '{instance_name}' [{region}] -> "
        f"{vcpus} vCPUs, {memory_gb} GB RAM ({tier})"
    )


def main() -> None:
    print("=== 1. All Keyword Arguments (Order-Independent) ===")
    # Keyword arguments can be passed in any order!
    vm_1 = create_cloud_vm(
        region="ap-south-1",
        memory_gb=32,
        instance_name="ml-trainer-01",
        vcpus=8,
        preemptible=True,
    )
    print(f"  {vm_1}")

    print("\n=== 2. Mixing Positional (First) and Keyword (After) ===")
    vm_2 = create_cloud_vm("web-prod-01", "us-east-1", preemptible=False, memory_gb=16)
    print(f"  {vm_2}")

    print("\n=== 3. Catching Duplicate Parameter Assignment (`TypeError`) ===")
    try:
        # `"web-prod-02"` binds to `instance_name` positionally, then `instance_name=` duplicates it
        create_cloud_vm("web-prod-02", "eu-west-1", instance_name="duplicate-name")  # type: ignore[misc]
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
