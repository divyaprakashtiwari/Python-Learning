"""
Topic 05 - Object-Oriented Programming (OOP): Question 2
Problem: Class Variables vs Instance Variables and Attribute Shadowing.
"""

from typing import List


class CloudServerNode:
    """Demonstrates class-level vs instance-level variable semantics and shadowing."""

    total_active_nodes: int = 0
    cluster_datacenter: str = "us-east-1"
    node_registry: List["CloudServerNode"] = []

    def __init__(self, node_id: str, cpu_cores: int, ram_gb: int):
        self.node_id = node_id
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb
        self.is_online = True

        CloudServerNode.total_active_nodes += 1
        CloudServerNode.node_registry.append(self)

    def terminate(self) -> None:
        """Decommissions the node instance and decrements the shared class counter."""
        if not self.is_online:
            raise RuntimeError("Node already offline")

        self.is_online = False
        CloudServerNode.total_active_nodes = max(0, CloudServerNode.total_active_nodes - 1)
        if self in CloudServerNode.node_registry:
            CloudServerNode.node_registry.remove(self)


# 1. Cluster Initialization
node_a = CloudServerNode("node-01", 8, 32)
node_b = CloudServerNode("node-02", 16, 64)
node_c = CloudServerNode("node-03", 4, 16)

print("Initial Cluster Status:")
print(f"- Active Nodes: {CloudServerNode.total_active_nodes}")
print(f"- Node IDs: {[n.node_id for n in CloudServerNode.node_registry]}")
print(f'- Default Region: "{CloudServerNode.cluster_datacenter}"')

# 2. Decommissioning node_b
node_b.terminate()
print("\nAfter Terminating node-02:")
print(f"- Active Nodes: {CloudServerNode.total_active_nodes}")
print(f"- Node IDs: {[n.node_id for n in CloudServerNode.node_registry]}")

# 3. Class Attribute Shadowing on an individual instance
node_a.cluster_datacenter = "ap-south-1"  # Creates instance attribute, shadowing class var
print("\nShadowing Verification:")
print(f'- node_a Region (Instance Override): "{node_a.cluster_datacenter}"')
print(f'- node_c Region (Inherited Class Default): "{node_c.cluster_datacenter}"')

# 4. Updating Shared Class Variable
CloudServerNode.cluster_datacenter = "eu-central-1"
print('\nAfter Updating Class Region (CloudServerNode.cluster_datacenter = "eu-central-1"):')
print(f'- node_a Region: "{node_a.cluster_datacenter}" (Still shadowed)')
print(f'- node_c Region: "{node_c.cluster_datacenter}" (Reflects class update)')
