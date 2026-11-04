# Phase 3 — Topic 05: Keyword Arguments

## 1. Introduction

When calling a function in Python, **keyword arguments** allow you to pass values by explicitly naming the target parameter (`parameter_name=value`) rather than relying solely on positional order.

For example, instead of remembering whether `vcpus` or `memory_gb` comes first in `create_cloud_vm("web-01", "us-east-1", 4, 16)`, you can write `create_cloud_vm("web-01", "us-east-1", memory_gb=16, vcpus=4)`.

Python also lets you:
- **Enforce keyword-only arguments** using a bare `*` divider in the function signature so callers cannot pass unreadable bare booleans (`True, False, True`).
- **Unpack a dictionary** of settings directly into keyword arguments at the call site using the `**` operator (`connect_redis(**prod_config)`).

---

## 2. Why is it used?

- **Self-Documenting Call Sites (Eliminating the "Boolean Trap"):** Compare `export_report("Q3", True, False, True)` with `export_report("Q3", include_charts=True, compress_pdf=False, send_email=True)`. Keyword arguments turn cryptic literals into readable specifications.
- **Order Independence:** Callers don't have to memorize the exact parameter order of functions with 5+ parameters.
- **Configuration Driven Calls (`**config`):** Backend applications often load settings from JSON/YAML into a `dict` and pass them directly to database or HTTP clients via `**settings`.

---

## 3. Syntax

```python
# 1. Passing keyword arguments at the call site (order-independent)
create_cloud_vm(region="ap-south-1", instance_name="api-01", vcpus=4)

# 2. Mixing positional (MUST come first) and keyword arguments (MUST come after)
create_cloud_vm("api-01", "ap-south-1", memory_gb=32)

# 3. Enforcing keyword-only parameters with bare `*` in `def`
def export_report(title: str, *, include_charts: bool = False) -> str:
    ...

# 4. Unpacking a dict into keyword arguments at the call site
config = {"host": "localhost", "port": 6379}
connect_redis(**config)
```

---

## 4. Explanation (Step-by-Step)

### Step 1: Call-Site Ordering Rule (Positional Before Keyword)
At any function call site:
- All **positional arguments** must be listed **before** any **keyword arguments**.
- Writing a positional argument after a keyword argument (`func(a=1, 2)`) raises a compile-time `SyntaxError: positional argument follows keyword argument`.
- Once you switch to keyword arguments in a call, their relative order no longer matters (`func(1, c=3, b=2)` is completely valid).

### Step 2: Duplicate Parameter Detection
Python first binds all positional arguments by index, and then binds keyword arguments by name. If a keyword argument names a parameter that already received a positional argument (`create_cloud_vm("web-01", "us-east-1", instance_name="dup")`), Python raises `TypeError: got multiple values for argument 'instance_name'`.

### Step 3: Enforcing Keyword-Only Parameters (`*`)
Placing a bare asterisk `*` in the `def` parameter list (`def export_report(title, *, include_charts=False):`) acts as a wall:
- No positional arguments are allowed past `*`.
- Every parameter after `*` **must** be passed as `name=value`.
- Their default values are stored in the dictionary `func.__kwdefaults__`.

### Step 4: Dictionary Unpacking (`**mapping`)
When you call `connect_redis(**prod_config)`, Python unpacks each `"key": value` pair in `prod_config` as if you had written `key=value` in the function call. Every key must be a `str` matching a valid parameter name (unless the function accepts `**kwargs`).

---

## 5. Minimum 3 Examples

### Example 1: Mixing Positional and Keyword Arguments & Ordering Rules
File: `example_01_positional_and_keyword_mixing.py`

```python
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
        create_cloud_vm("web-prod-02", "eu-west-1", instance_name="duplicate-name")
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
```

---

### Example 2: Enforcing Keyword-Only Arguments (`*`) to Prevent Boolean Trap
File: `example_02_keyword_only_parameters.py`

```python
def export_report_bad(
    title: str,
    include_charts: bool = False,
    compress_pdf: bool = False,
    send_email: bool = False,
) -> str:
    """Ambiguous at call site when booleans are passed positionally."""
    return (
        f"Report({title!r}): charts={include_charts}, "
        f"compress={compress_pdf}, email={send_email}"
    )


def export_report_clean(
    title: str,
    *,  # Forces all subsequent parameters to be passed by KEYWORD
    include_charts: bool = False,
    compress_pdf: bool = False,
    send_email: bool = False,
) -> str:
    """Self-documenting API: boolean flags MUST be named at the call site."""
    return (
        f"Report({title!r}): charts={include_charts}, "
        f"compress={compress_pdf}, email={send_email}"
    )


def main() -> None:
    print("=== 1. The 'Boolean Trap' in Positional Calls ===")
    # Looking at this call alone, nobody knows what `True, False, True` mean:
    mystery_call = export_report_bad("Q3 Revenue", True, False, True)
    print(f"  Positional booleans : {mystery_call}")

    print("\n=== 2. Keyword-Only (`*`) Enforces Self-Documenting Calls ===")
    clean_call = export_report_clean(
        "Q3 Revenue",
        include_charts=True,
        compress_pdf=False,
        send_email=True,
    )
    print(f"  Keyword-only flags  : {clean_call}")
    print(f"  __kwdefaults__ dict : {export_report_clean.__kwdefaults__}")

    print("\n=== 3. Positional Call to Keyword-Only Function Raises `TypeError` ===")
    try:
        export_report_clean("Q3 Revenue", True)
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
```

---

### Example 3: Unpacking Dictionaries into Keyword Arguments (`**config`)
File: `example_03_unpacking_dict_as_keyword_args.py`

```python
def connect_redis(
    host: str = "127.0.0.1",
    port: int = 6379,
    db: int = 0,
    decode_responses: bool = True,
) -> str:
    """Simulate opening a Redis client connection."""
    return (
        f"Redis(host={host!r}, port={port}, db={db}, "
        f"decode_responses={decode_responses})"
    )


def main() -> None:
    print("=== 1. Unpacking a Config Dictionary (`**prod_config`) ===")
    prod_config = {
        "host": "redis.cache.internal",
        "port": 6380,
        "db": 2,
        "decode_responses": True,
    }
    # `**prod_config` expands key-value pairs into keyword arguments
    conn_1 = connect_redis(**prod_config)
    print(f"  Unpacked call : {conn_1}")

    print("\n=== 2. Combining Base Config with Overrides (`{**base, **override}`) ===")
    staging_override = {**prod_config, "host": "staging-redis.local", "db": 5}
    conn_2 = connect_redis(**staging_override)
    print(f"  Overridden    : {conn_2}")

    print("\n=== 3. Unknown Key in Unpacked Dictionary Raises `TypeError` ===")
    invalid_config = {"host": "localhost", "max_connections": 50}
    try:
        connect_redis(**invalid_config)
    except TypeError as err:
        print(f"  Caught expected TypeError: {err}")


if __name__ == "__main__":
    main()
```

---

## 6. Output

### Output — Example 1 (`example_01_positional_and_keyword_mixing.py`)
```text
=== 1. All Keyword Arguments (Order-Independent) ===
  VM 'ml-trainer-01' [ap-south-1] -> 8 vCPUs, 32 GB RAM (Spot/Preemptible)

=== 2. Mixing Positional (First) and Keyword (After) ===
  VM 'web-prod-01' [us-east-1] -> 2 vCPUs, 16 GB RAM (On-Demand)

=== 3. Catching Duplicate Parameter Assignment (`TypeError`) ===
  Caught expected TypeError: create_cloud_vm() got multiple values for argument 'instance_name'
```

### Output — Example 2 (`example_02_keyword_only_parameters.py`)
```text
=== 1. The 'Boolean Trap' in Positional Calls ===
  Positional booleans : Report('Q3 Revenue'): charts=True, compress=False, email=True

=== 2. Keyword-Only (`*`) Enforces Self-Documenting Calls ===
  Keyword-only flags  : Report('Q3 Revenue'): charts=True, compress=False, email=True
  __kwdefaults__ dict : {'include_charts': False, 'compress_pdf': False, 'send_email': False}

=== 3. Positional Call to Keyword-Only Function Raises `TypeError` ===
  Caught expected TypeError: export_report_clean() takes 1 positional argument but 2 were given
```

### Output — Example 3 (`example_03_unpacking_dict_as_keyword_args.py`)
```text
=== 1. Unpacking a Config Dictionary (`**prod_config`) ===
  Unpacked call : Redis(host='redis.cache.internal', port=6380, db=2, decode_responses=True)

=== 2. Combining Base Config with Overrides (`{**base, **override}`) ===
  Overridden    : Redis(host='staging-redis.local', port=6380, db=5, decode_responses=True)

=== 3. Unknown Key in Unpacked Dictionary Raises `TypeError` ===
  Caught expected TypeError: connect_redis() got an unexpected keyword argument 'max_connections'
```

---

## 7. Code Explanation

1. **Order Independence (`example_01`):** In `create_cloud_vm(region="ap-south-1", memory_gb=32, instance_name="ml-trainer-01", ...)`, Python matches each argument by parameter name rather than slot index.
2. **Eliminating the Boolean Trap (`example_02`):** By placing `*` after `title`, `export_report_clean` makes `export_report_clean("Q3 Revenue", True)` a `TypeError`, forcing every caller to write `include_charts=True`.
3. **Dictionary Unpacking (`example_03`):** `connect_redis(**prod_config)` unpacks the 4 keys of `prod_config` into keyword arguments. If `invalid_config` contains a key (`"max_connections"`) that is not a parameter of `connect_redis`, Python raises `TypeError: got an unexpected keyword argument`.

---

## 8. Common Mistakes

1. **Putting a positional argument after a keyword argument at the call site:**
   - `create_cloud_vm(instance_name="web-01", "us-east-1")` is a `SyntaxError`. Positional arguments must always come first.
2. **Passing duplicate keys when unpacking multiple dictionaries in a single call:**
   - Calling `func(**dict_a, **dict_b)` directly when both dicts share a key raises `TypeError: got multiple values for keyword argument`. Instead, merge them into a single dict first (`func(**{**dict_a, **dict_b})` or `func(**(dict_a | dict_b))`), where right-hand keys cleanly override left-hand keys.
3. **Confusing `*` (bare asterisk) with `*args`:**
   - Bare `*` **rejects** extra positional arguments completely; `*args` **accepts** extra positional arguments into a tuple. Both make any parameters that follow them keyword-only.

---

## 9. Practice Questions

1. **Easy — HTTP Request Builder with Keyword-Only Options:**
   Write `send_request(method: str, url: str, *, timeout: int = 10, verify_ssl: bool = True, retries: int = 3) -> str` and test calling it with positional `method` and `url` plus keyword-only options in different orders.

2. **Medium — Safe Config Merger (`|` Unpacking):**
   Given `default_theme = {"font": "Inter", "size": 14, "dark_mode": False}` and `user_prefs = {"size": 16, "dark_mode": True}`, write a function `render_editor(font: str, size: int, dark_mode: bool) -> str` and call it by merging and unpacking both dictionaries using `render_editor(**(default_theme | user_prefs))`.

3. **Hard — Filtering Unknown Keys Before `**` Unpacking:**
   Suppose an external JSON payload has extra keys (`{"host": "db.local", "port": 5432, "extra_debug": True, "created_by": "admin"}`). Write a helper `call_with_known_keys(func, payload: dict)` that uses `inspect.signature(func).parameters` to filter `payload` down to only valid parameter names before calling `func(**filtered_payload)`.

---

## 10. Interview Questions

### Q1: Can a required parameter (without a default value) appear *after* a parameter with a default value in Python?
**Answer:**
Yes, **if and only if** the required parameter is a **keyword-only parameter** (placed after `*` or `*args`)!
For example:
```python
def deploy(env: str = "staging", *, api_key: str) -> None:
    ...
```
This is completely valid because `api_key` can only ever be passed by name (`deploy(api_key="secret")`), so there is no positional ambiguity when `env` uses its default value.

### Q2: Why does `func(**{'a': 1}, a=2)` raise a `TypeError`, whereas `func(**{'a': 1, 'a': 2})` does not?
**Answer:**
- In a dictionary literal `{'a': 1, 'a': 2}`, duplicate keys overwrite earlier keys during dictionary construction, resulting in a single-key dict `{'a': 2}` before `func` is even called.
- In `func(**{'a': 1}, a=2)`, Python unpacks keyword arguments at the call site and forbids supplying the same keyword parameter twice in one call, raising `TypeError: func() got multiple values for keyword argument 'a'`.

### Q3: What is the "Boolean Trap" in API design, and how do Python's keyword-only arguments solve it?
**Answer:**
The "Boolean Trap" occurs when a function accepts positional boolean parameters (e.g., `repaint(True, False)`), making call sites unreadable because the reader cannot tell what `True` and `False` control without looking up the function definition. Placing `*` before boolean parameters (`def repaint(*, immediate: bool, clear_background: bool):`) forces every caller to write `repaint(immediate=True, clear_background=False)`.
