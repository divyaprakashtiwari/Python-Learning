"""
Topic 03 - Data Structures: Question 6
Problem: Organizational records grouping and dictionary methods (setdefault, get, fromkeys, popitem).
"""

employees = [
    (101, "Alice", "Engineering", 125000),
    (102, "Bob", "Marketing", 90000),
    (103, "Charlie", "Engineering", 140000),
    (104, "Diana", "Human Resources", 85000),
    (105, "Evan", "Marketing", 95000)
]

# 1. Categorized Grouping with setdefault()
dept_map = {}
for emp_id, name, dept, salary in employees:
    dept_map.setdefault(dept, []).append((name, salary))

print("Grouped Departments via setdefault():")
for dept, members in dept_map.items():
    print(f"- {dept}: {members}")

# Average salary computation per department
print("\nDepartment Average Compensation:")
for dept, members in dept_map.items():
    avg_sal = sum(s for _, s in members) / len(members)
    print(f"- {dept}: ${avg_sal:,.2f}")

# 2. Defensive Retrieval with get()
query_dept = "Research & Development"
result = dept_map.get(query_dept, "No active personnel")
print(f"\nDefensive Lookup for '{query_dept}':")
print(f"Result: '{result}'")

# 3. Template Initialization with fromkeys()
unique_depts = list(dept_map.keys())
audit_status_map = dict.fromkeys(unique_depts, "PENDING_AUDIT")
print("\nInitial Audit Status Map via fromkeys():")
print(audit_status_map)

# 4. Cache Eviction with popitem() (LIFO order in Python 3.7+)
popped_dept, popped_members = dept_map.popitem()
print("\nEvicted Most Recent Department via popitem():")
print(f"Popped: ('{popped_dept}', {popped_members})")
print(f"Remaining departments: {list(dept_map.keys())}")
