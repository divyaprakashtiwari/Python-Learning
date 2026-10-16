"""
Topic 02: Control Flow
Question 02: Nested Conditionals

Master multi-level decision trees, hierarchical validations,
refactoring deeply nested conditionals (Guard Clauses), and complex state workflows.
"""

# ============================================================
# Q1: ATM Cash Withdrawal Pipeline
# ============================================================
# Question: Implement an ATM cash withdrawal workflow using nested conditionals:
# Check account status -> Verify PIN -> Validate daily limit by tier -> Verify sufficient balance.

print("=== Q1: ATM Cash Withdrawal Workflow ===")

def process_atm_withdrawal(account: dict, entered_pin: str, amount: float) -> dict:
    """Processes ATM withdrawal through multi-level authorization."""
    # Level 1: Account status check
    if account.get("is_active"):
        # Level 2: PIN validation
        if entered_pin == account.get("pin"):
            # Level 3: Daily withdrawal limit check based on account tier
            tier = account.get("tier", "STANDARD")
            daily_limit = 5000.0 if tier == "VIP" else 1500.0
            
            if amount <= daily_limit:
                # Level 4: Balance verification
                current_balance = account.get("balance", 0.0)
                if current_balance >= amount:
                    account["balance"] -= amount
                    return {
                        "status": "SUCCESS",
                        "withdrawn": amount,
                        "remaining_balance": account["balance"],
                        "message": f"Please collect your ${amount:,.2f}"
                    }
                else:
                    return {"status": "FAILED", "reason": f"Insufficient funds. Available: ${current_balance:,.2f}"}
            else:
                return {"status": "FAILED", "reason": f"Exceeds daily limit of ${daily_limit:,.2f} for {tier} tier"}
        else:
            return {"status": "FAILED", "reason": "Invalid PIN entered"}
    else:
        return {"status": "FAILED", "reason": "Account is locked or inactive"}

sample_account = {
    "account_number": "ACC-88219",
    "pin": "4921",
    "is_active": True,
    "tier": "STANDARD",
    "balance": 2500.0
}

test_scenarios = [
    ("4921", 500.0, "Valid withdrawal"),
    ("0000", 200.0, "Incorrect PIN"),
    ("4921", 2000.0, "Exceeds standard daily limit"),
    ("4921", 2200.0, "Exceeds remaining balance"),
]

for pin, amt, label in test_scenarios:
    res = process_atm_withdrawal(sample_account, pin, amt)
    print(f"  [{label:<28}] Status: {res['status']:<7} | {res.get('message', res.get('reason'))}")

# Explanation: Nested conditionals represent ordered prerequisites where each check
# depends upon the success of the preceding authorization step.


# ============================================================
# Q2: Multi-Factor Authentication (MFA) Verification
# ============================================================
# Question: Implement an MFA verification workflow:
# Password verification -> OTP verification -> Backup recovery code fallback -> Account lockout.

print("\n=== Q2: Multi-Factor Authentication Pipeline ===")

def verify_mfa_login(
    stored_cred: dict,
    input_password: str,
    input_otp: str = None,
    backup_code: str = None
) -> dict:
    """Verifies user credentials through primary and secondary authentication layers."""
    # Check lockout
    if stored_cred.get("failed_attempts", 0) >= 3:
        return {"authenticated": False, "status": "LOCKED", "msg": "Account locked due to 3 failed attempts"}
    
    # Layer 1: Password Check
    if input_password == stored_cred["password"]:
        # Reset failed password count on correct password
        stored_cred["failed_attempts"] = 0
        
        # Layer 2: Secondary factor (OTP or Backup code)
        if stored_cred.get("mfa_enabled", False):
            if input_otp and input_otp == stored_cred.get("current_otp"):
                return {"authenticated": True, "method": "PASSWORD + OTP", "msg": "Access granted"}
            else:
                # Fallback to backup one-time code
                if backup_code and backup_code in stored_cred.get("backup_codes", []):
                    stored_cred["backup_codes"].remove(backup_code)
                    return {"authenticated": True, "method": "BACKUP_CODE", "msg": "Access granted via emergency code"}
                else:
                    return {"authenticated": False, "status": "MFA_FAILED", "msg": "Invalid OTP and backup code"}
        else:
            return {"authenticated": True, "method": "PASSWORD_ONLY", "msg": "Access granted"}
    else:
        stored_cred["failed_attempts"] = stored_cred.get("failed_attempts", 0) + 1
        remaining = 3 - stored_cred["failed_attempts"]
        return {"authenticated": False, "status": "BAD_PASSWORD", "msg": f"Invalid password. {remaining} attempt(s) remaining"}

user_profile = {
    "username": "coder_pro",
    "password": "SecureHash#123",
    "mfa_enabled": True,
    "current_otp": "839201",
    "backup_codes": ["REC-1111", "REC-2222"],
    "failed_attempts": 0
}

attempts = [
    ("WrongPass", "839201", None),
    ("SecureHash#123", "000000", "REC-1111"),
    ("SecureHash#123", "839201", None),
]

for pwd, otp, bkp in attempts:
    res = verify_mfa_login(user_profile, pwd, otp, bkp)
    print(f"  Auth Attempt (pwd={'MATCH' if pwd == user_profile['password'] else 'WRONG'}, OTP={otp}): {res['msg']}")

# Explanation: MFA flows use nested verification: secondary factors are only
# checked after the primary factor succeeds, avoiding wasteful token decryptions.


# ============================================================
# Q3: Flight Baggage Allowance & Excess Fee Calculator
# ============================================================
# Question: Calculate permitted baggage allowance and excess fees based on:
# Route (Domestic vs International) -> Cabin Class (Economy, Business, First)
# -> Frequent Flyer Tier (Gold/Silver/None) -> Actual Baggage Weight.

print("\n=== Q3: Flight Baggage Fee Calculator ===")

def calculate_baggage_fee(
    route: str,
    cabin: str,
    flyer_tier: str,
    weight_kg: float
) -> dict:
    """Calculates free allowance and excess baggage penalties using nested rules."""
    route = route.upper()
    cabin = cabin.upper()
    flyer_tier = flyer_tier.upper()
    
    # Base allowance hierarchy
    if route == "DOMESTIC":
        excess_rate_per_kg = 15.0  # $15 per kg over limit
        if cabin == "ECONOMY":
            base_allowance = 15.0
        elif cabin == "BUSINESS":
            base_allowance = 30.0
        elif cabin == "FIRST":
            base_allowance = 40.0
        else:
            return {"error": f"Invalid cabin class: {cabin}"}
    elif route == "INTERNATIONAL":
        excess_rate_per_kg = 25.0  # $25 per kg over limit
        if cabin == "ECONOMY":
            base_allowance = 23.0
        elif cabin == "BUSINESS":
            base_allowance = 40.0
        elif cabin == "FIRST":
            base_allowance = 50.0
        else:
            return {"error": f"Invalid cabin class: {cabin}"}
    else:
        return {"error": f"Invalid route: {route}"}

    # Frequent flyer bonus allowance
    tier_bonus = 0.0
    if flyer_tier == "GOLD":
        tier_bonus = 15.0
    elif flyer_tier == "SILVER":
        tier_bonus = 10.0

    total_allowance = base_allowance + tier_bonus
    excess_weight = max(0.0, weight_kg - total_allowance)
    fee = excess_weight * excess_rate_per_kg
    
    return {
        "route": route,
        "cabin": cabin,
        "allowance": total_allowance,
        "actual_weight": weight_kg,
        "excess_weight": round(excess_weight, 1),
        "excess_fee": round(fee, 2)
    }

passengers = [
    ("Domestic", "Economy", "None", 18.0),
    ("Domestic", "Economy", "Gold", 28.0),
    ("International", "Business", "Silver", 45.0),
    ("International", "Economy", "None", 30.0),
]

for r, c, t, w in passengers:
    res = calculate_baggage_fee(r, c, t, w)
    print(f"  {r:<13} | {c:<8} | Tier: {t:<6} | Bag: {w:>4.1f}kg (Limit: {res['allowance']:>4.1f}kg) -> Fee: ${res['excess_fee']:.2f}")

# Explanation: Hierarchical conditional branching maps cleanly to travel/airline policy
# matrix configurations.


# ============================================================
# Q4: Cartesian Coordinate Quadrant & Axis Geometry
# ============================================================
# Question: Given (x, y) coordinates, use nested conditionals to categorize
# location: Origin, X-Axis, Y-Axis, or Quadrants I, II, III, IV.

print("\n=== Q4: Coordinate Quadrant Classifier ===")

def classify_coordinate(x: float, y: float) -> str:
    """Locates point in Cartesian 2D plane."""
    if x == 0:
        if y == 0:
            return "Origin (0, 0)"
        else:
            return f"On Y-Axis at y={y}"
    elif y == 0:
        return f"On X-Axis at x={x}"
    else:
        # Neither coordinate is 0: must lie in one of four quadrants
        if x > 0:
            if y > 0:
                return f"Quadrant I (+X, +Y)"
            else:
                return f"Quadrant IV (+X, -Y)"
        else:
            if y > 0:
                return f"Quadrant II (-X, +Y)"
            else:
                return f"Quadrant III (-X, -Y)"

points = [(0, 0), (0, 5), (-4, 0), (3, 7), (-2, 8), (-5, -9), (6, -3)]
for pt in points:
    print(f"  Point {str(pt):<10} -> {classify_coordinate(*pt)}")

# Explanation: Evaluating zero-axes first partitions the search space before
# quadrant sign evaluation, guaranteeing mutually exclusive classifications.


# ============================================================
# Q5: Restaurant Table Reservation Allocator
# ============================================================
# Question: Match a customer reservation request to restaurant seating:
# Party size -> Preference (Indoor/Outdoor/Bar) -> Accessibility needs -> Availability.

print("\n=== Q5: Restaurant Seating Allocator ===")

def allocate_table(
    party_size: int,
    area_pref: str,
    needs_wheelchair: bool,
    available_tables: list[dict]
) -> dict:
    """Matches reservation criteria with table constraints."""
    if party_size <= 0:
        return {"assigned": False, "reason": "Party size must be >= 1"}
        
    area_pref = area_pref.capitalize()
    
    # Find matching tables
    suitable_table = None
    for tbl in available_tables:
        if tbl["capacity"] >= party_size:
            # Check area preference
            if area_pref == "Any" or tbl["area"] == area_pref:
                # Check accessibility
                if not needs_wheelchair or tbl["wheelchair_accessible"]:
                    suitable_table = tbl
                    break
                    
    if suitable_table:
        return {
            "assigned": True,
            "table_id": suitable_table["id"],
            "area": suitable_table["area"],
            "capacity": suitable_table["capacity"],
            "message": f"Assigned Table #{suitable_table['id']} in {suitable_table['area']}"
        }
    else:
        return {
            "assigned": False,
            "reason": f"No available {area_pref} table for {party_size} people with requested accessibility"
        }

tables_db = [
    {"id": 101, "capacity": 2, "area": "Bar", "wheelchair_accessible": False},
    {"id": 102, "capacity": 4, "area": "Outdoor", "wheelchair_accessible": True},
    {"id": 103, "capacity": 6, "area": "Indoor", "wheelchair_accessible": True},
    {"id": 104, "capacity": 2, "area": "Indoor", "wheelchair_accessible": False},
]

requests = [
    (2, "Bar", False),
    (4, "Outdoor", True),
    (4, "Outdoor", False),
    (8, "Indoor", False),
]

for sz, area, wc in requests:
    res = allocate_table(sz, area, wc, tables_db)
    status = f"Table #{res.get('table_id')}" if res["assigned"] else f"WAITLIST ({res['reason']})"
    print(f"  Party of {sz} ({area}, Accessible={wc}) -> {status}")

# Explanation: Combining nested filtering with collection traversal powers
# reservation, matchmaking, and logistics engines.


# ============================================================
# Q6: Academic Scholarship & Financial Aid Evaluation
# ============================================================
# Question: Evaluate scholarship eligibility based on:
# GPA -> Family Income Bracket -> Leadership Points -> Community Service Hours.

print("\n=== Q6: Scholarship Eligibility Evaluator ===")

def evaluate_scholarship(
    gpa: float,
    family_income: float,
    leadership_score: int,
    volunteer_hours: int
) -> dict:
    """Evaluates merit-based and need-based financial awards."""
    # Top tier: Presidential Full-Ride Scholarship (Merit + High Performance)
    if gpa >= 3.8:
        if leadership_score >= 85 and volunteer_hours >= 100:
            award = "Presidential Full Merit Scholarship ($25,000/yr)"
            status = "APPROVED_FULL"
        else:
            if family_income <= 60_000:
                award = "Dean's Merit + Need Blend Grant ($15,000/yr)"
                status = "APPROVED_PARTIAL"
            else:
                award = "Academic Honors Award ($10,000/yr)"
                status = "APPROVED_PARTIAL"
    elif gpa >= 3.2:
        # Mid-tier: Need-based or community service focus
        if family_income <= 45_000:
            if volunteer_hours >= 50:
                award = "Opportunity Access Grant ($12,000/yr)"
                status = "APPROVED_PARTIAL"
            else:
                award = "Tuition Assistance Work-Study ($6,000/yr)"
                status = "APPROVED_WORK_STUDY"
        else:
            award = "Departmental Recognition ($3,000/yr)"
            status = "APPROVED_MINIMAL"
    else:
        award = "Ineligible for scholarship (GPA below 3.2 minimum threshold)"
        status = "DENIED"

    return {"gpa": gpa, "income": family_income, "status": status, "award": award}

students = [
    (3.9, 80_000, 90, 120),
    (3.85, 45_000, 70, 40),
    (3.4, 35_000, 60, 60),
    (2.9, 30_000, 80, 150),
]

for g, inc, lead, vol in students:
    outcome = evaluate_scholarship(g, inc, lead, vol)
    print(f"  GPA: {g:<4} | Income: ${inc:>6,.0f} -> [{outcome['status']:<19}] {outcome['award']}")

# Explanation: Multi-layered criteria enable institutions to tailor awards combining
# merit thresholds with socio-economic equity considerations.


# ============================================================
# Q7: Refactoring "Pyramid of Doom" with Guard Clauses
# ============================================================
# Question: Demonstrate the "Pyramid of Doom" anti-pattern (deeply nested ifs)
# and refactor it into clean, maintainable code using Guard Clauses (early returns).

print("\n=== Q7: Refactoring Deep Nesting (Guard Clauses) ===")

# ANTI-PATTERN: The "Pyramid of Doom"
def register_user_nested(user_dict: dict) -> str:
    """Anti-pattern: Deep nesting makes code hard to read and test."""
    if user_dict is not None:
        if "username" in user_dict and len(user_dict["username"]) >= 3:
            if "email" in user_dict and "@" in user_dict["email"]:
                if "age" in user_dict and user_dict["age"] >= 18:
                    if user_dict.get("terms_accepted", False):
                        return "SUCCESS: User successfully registered"
                    else:
                        return "FAILED: Terms and conditions must be accepted"
                else:
                    return "FAILED: User must be at least 18 years old"
            else:
                return "FAILED: Invalid email address"
        else:
            return "FAILED: Username must be at least 3 characters"
    else:
        return "FAILED: User payload cannot be null"

# BEST PRACTICE: Flattened with Guard Clauses (Return Early)
def register_user_flattened(user_dict: dict) -> str:
    """Clean pattern: Guard clauses fail fast and reduce indentation depth."""
    if user_dict is None:
        return "FAILED: User payload cannot be null"
    
    if "username" not in user_dict or len(user_dict["username"]) < 3:
        return "FAILED: Username must be at least 3 characters"
        
    if "email" not in user_dict or "@" not in user_dict["email"]:
        return "FAILED: Invalid email address"
        
    if "age" not in user_dict or user_dict["age"] < 18:
        return "FAILED: User must be at least 18 years old"
        
    if not user_dict.get("terms_accepted", False):
        return "FAILED: Terms and conditions must be accepted"
        
    return "SUCCESS: User successfully registered"

payloads = [
    None,
    {"username": "al"},
    {"username": "alice", "email": "bad_email"},
    {"username": "alice", "email": "alice@site.com", "age": 16},
    {"username": "alice", "email": "alice@site.com", "age": 22, "terms_accepted": True},
]

print("  Comparing Nested vs Flattened behavior:")
for p in payloads:
    res_nested = register_user_nested(p)
    res_flat = register_user_flattened(p)
    assert res_nested == res_flat, "Refactored logic diverged!"
    print(f"    Payload: {str(p):<55} -> {res_flat}")

# Explanation: Guard clauses check error/boundary cases first and exit immediately,
# keeping the happy path at the top level of indentation.


# ============================================================
# Q8: Vending Machine Transaction State Machine
# ============================================================
# Question: Implement a vending machine purchase algorithm:
# Item selection -> Stock check -> Payment amount check -> Change calculation.

print("\n=== Q8: Vending Machine Transaction Logic ===")

def vend_item(item_code: str, inserted_money: float, inventory: dict) -> dict:
    """Manages vending transaction and change calculation."""
    item_code = item_code.upper()
    
    # 1. Check if item exists in catalog
    if item_code in inventory:
        item = inventory[item_code]
        
        # 2. Check stock availability
        if item["stock"] > 0:
            price = item["price"]
            
            # 3. Check sufficient payment
            if inserted_money >= price:
                change = round(inserted_money - price, 2)
                item["stock"] -= 1  # Deduct stock
                return {
                    "success": True,
                    "item_name": item["name"],
                    "dispensed": True,
                    "change": change,
                    "remaining_stock": item["stock"],
                    "message": f"Dispensing {item['name']}. Change returned: ${change:.2f}"
                }
            else:
                shortage = round(price - inserted_money, 2)
                return {
                    "success": False,
                    "dispensed": False,
                    "refund": inserted_money,
                    "message": f"Insufficient funds. Insert ${shortage:.2f} more for {item['name']}."
                }
        else:
            return {
                "success": False,
                "dispensed": False,
                "refund": inserted_money,
                "message": f"Item '{item['name']}' is out of stock. Refund: ${inserted_money:.2f}"
            }
    else:
        return {
            "success": False,
            "dispensed": False,
            "refund": inserted_money,
            "message": f"Invalid item code '{item_code}'. Refund: ${inserted_money:.2f}"
        }

catalog = {
    "A1": {"name": "Espresso Roast", "price": 2.50, "stock": 3},
    "B2": {"name": "Protein Bar",    "price": 3.00, "stock": 0},
    "C3": {"name": "Mineral Water",  "price": 1.50, "stock": 5},
}

test_vends = [
    ("A1", 5.00),
    ("A1", 2.00),
    ("B2", 5.00),
    ("Z9", 2.00),
]

for code, cash in test_vends:
    res = vend_item(code, cash, catalog)
    print(f"  Selection: {code} (${cash:.2f}) -> {res['message']}")

# Explanation: State validation protects physical inventory from vending without
# complete payment, and protects customer currency through automatic refunds.


# ============================================================
# Q9: Medical Blood Donor Qualification Screener
# ============================================================
# Question: Screen blood donation candidates across multiple physiological gates:
# Age (18-65) -> Weight (>= 50kg) -> Hemoglobin (>= 12.5 g/dL) -> Travel risk.

print("\n=== Q9: Blood Donor Qualification Screener ===")

def screen_blood_donor(candidate: dict) -> dict:
    """Evaluates candidate eligibility through health parameters."""
    age = candidate.get("age", 0)
    
    # Gate 1: Age verification
    if 18 <= age <= 65:
        weight = candidate.get("weight_kg", 0.0)
        
        # Gate 2: Weight verification
        if weight >= 50.0:
            hb = candidate.get("hemoglobin", 0.0)
            
            # Gate 3: Hemoglobin level verification
            if hb >= 12.5:
                # Gate 4: Medical / Travel exclusion
                if not candidate.get("recent_surgery", False):
                    if not candidate.get("malaria_zone_travel", False):
                        return {"eligible": True, "reason": "Eligible to donate whole blood"}
                    else:
                        return {"eligible": False, "reason": "Temporary deferral: recent travel to malaria-endemic area"}
                else:
                    return {"eligible": False, "reason": "Temporary deferral: surgery within last 6 months"}
            else:
                return {"eligible": False, "reason": f"Hemoglobin {hb} g/dL below 12.5 g/dL minimum safety requirement"}
        else:
            return {"eligible": False, "reason": f"Weight {weight}kg below 50kg minimum threshold"}
    else:
        return {"eligible": False, "reason": f"Age {age} outside allowable 18-65 donation window"}

donors = [
    {"name": "Sam", "age": 25, "weight_kg": 68.0, "hemoglobin": 14.2, "recent_surgery": False, "malaria_zone_travel": False},
    {"name": "Kim", "age": 17, "weight_kg": 55.0, "hemoglobin": 13.0, "recent_surgery": False, "malaria_zone_travel": False},
    {"name": "Lee", "age": 40, "weight_kg": 46.0, "hemoglobin": 13.5, "recent_surgery": False, "malaria_zone_travel": False},
    {"name": "Pat", "age": 30, "weight_kg": 72.0, "hemoglobin": 11.8, "recent_surgery": False, "malaria_zone_travel": False},
    {"name": "Jan", "age": 35, "weight_kg": 75.0, "hemoglobin": 14.0, "recent_surgery": True, "malaria_zone_travel": False},
]

for d in donors:
    res = screen_blood_donor(d)
    status = "APPROVED" if res["eligible"] else "DEFERRED"
    print(f"  Donor {d['name']:<4} -> [{status:<8}] {res['reason']}")

# Explanation: Healthcare triage uses nested safety gates where any single failure
# halts screening to protect both the donor and the recipient.


# ============================================================
# Q10: Comprehensive Auto Insurance Premium Risk Engine
# ============================================================
# Question: Build an insurance rating engine that calculates annual premium based on:
# Driver Age (<25, 25-65, >65) -> Vehicle Category -> Past Violations -> Coverage Level.

print("\n=== Q10: Auto Insurance Rating Engine ===")

def calculate_auto_premium(
    driver_age: int,
    vehicle_type: str,
    accidents_last_3yrs: int,
    coverage: str
) -> dict:
    """Calculates actuarial risk and insurance premium via nested matrix."""
    # Base rate by vehicle class
    vehicle_type = vehicle_type.upper()
    coverage = coverage.upper()
    
    if vehicle_type == "SEDAN":
        base_rate = 800.0
    elif vehicle_type == "SUV":
        base_rate = 950.0
    elif vehicle_type == "SPORTS":
        base_rate = 1500.0
    elif vehicle_type == "COMMERCIAL_VAN":
        base_rate = 1200.0
    else:
        raise ValueError(f"Unknown vehicle type: {vehicle_type}")

    # Age surcharge factor
    if driver_age < 21:
        age_factor = 1.80  # +80% for young novice drivers
        age_group = "Young Novice (<21)"
    elif driver_age < 25:
        age_factor = 1.35  # +35%
        age_group = "Young Driver (21-24)"
    elif driver_age <= 65:
        age_factor = 1.00  # Standard baseline
        age_group = "Prime Driver (25-65)"
    else:
        age_factor = 1.20  # +20% for senior drivers
        age_group = "Senior Driver (>65)"

    # Driving record violation multiplier
    if accidents_last_3yrs == 0:
        violation_factor = 0.90  # 10% clean record discount!
    elif accidents_last_3yrs == 1:
        violation_factor = 1.25  # +25%
    elif accidents_last_3yrs == 2:
        violation_factor = 1.70  # +70%
    else:
        violation_factor = 2.50  # High risk driver

    # Coverage package multiplier
    if coverage == "LIABILITY_ONLY":
        coverage_factor = 0.70
    elif coverage == "STANDARD":
        coverage_factor = 1.00
    elif coverage == "COMPREHENSIVE_PLUS":
        coverage_factor = 1.45
    else:
        coverage_factor = 1.00

    final_premium = base_rate * age_factor * violation_factor * coverage_factor

    return {
        "vehicle": vehicle_type,
        "age_group": age_group,
        "accidents": accidents_last_3yrs,
        "coverage": coverage,
        "base_rate": base_rate,
        "annual_premium": round(final_premium, 2)
    }

quote_requests = [
    {"age": 19, "veh": "Sports", "accidents": 1, "cov": "Standard"},
    {"age": 35, "veh": "Sedan",  "accidents": 0, "cov": "Comprehensive_Plus"},
    {"age": 45, "veh": "SUV",    "accidents": 2, "cov": "Standard"},
    {"age": 70, "veh": "Sedan",  "accidents": 0, "cov": "Liability_Only"},
]

for q in quote_requests:
    q_res = calculate_auto_premium(q["age"], q["veh"], q["accidents"], q["cov"])
    print(f"  Age: {q['age']:<2} | {q_res['vehicle']:<7} | Acc: {q['accidents']} | {q_res['coverage']:<18} -> Premium: ${q_res['annual_premium']:>8,.2f}/yr")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q02 executed successfully!")
print("=" * 55)
