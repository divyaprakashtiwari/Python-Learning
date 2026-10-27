"""
Topic 03 - Data Structures: Question 4
Problem: Role-Based Access Control (RBAC) permission matrix using Set operations.
"""

# 1. Given role permission sets
admin_perms = {"read", "write", "delete", "deploy", "audit", "manage_users"}
dev_perms = {"read", "write", "deploy", "debug"}
auditor_perms = {"read", "audit", "export_logs"}
guest_perms = {"guest_login", "browse"}

# 2. Compute security audit sets using operator syntax
shared_dev_auditor = dev_perms & auditor_perms
dev_exclusive = dev_perms - auditor_perms
divergent_privileges = dev_perms ^ auditor_perms
total_unique = admin_perms | dev_perms | auditor_perms

print(f"Shared Dev & Auditor: {shared_dev_auditor}")
print(f"Developer-Exclusive: {dev_exclusive}")
print(f"Divergent Privileges (Symmetric Diff): {divergent_privileges}")
print(f"Total Unique System Privileges: {len(total_unique)} permissions -> {total_unique}")

# 3. Structural Relationship Audits
is_dev_subset = dev_perms <= admin_perms
rogue_perms = dev_perms - admin_perms
print(f"Is Dev a Subset of Admin: {is_dev_subset} (Rogue Permissions: {rogue_perms})")

is_guest_disjoint = guest_perms.isdisjoint(admin_perms)
print(f"Is Guest Disjoint from Admin: {is_guest_disjoint}")

# 4. In-Place Mutation
dev_copy = dev_perms.copy()
dev_copy.intersection_update(auditor_perms)
print(f"Dev Permissions after intersection_update with Auditor: {dev_copy}")
