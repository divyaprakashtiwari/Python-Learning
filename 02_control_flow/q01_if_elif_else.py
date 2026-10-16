"""
Topic 02: Control Flow
Question 01: if / elif / else Fundamentals

Master decision-making in Python: conditional logic, multi-branch evaluations,
boundary checking, validation, and complex rule engines.
"""

# ============================================================
# Q1: Number Classification and Parity Checker
# ============================================================
# Question: Write a function that classifies an integer as positive, negative,
# or zero, and determines whether non-zero numbers are even or odd.

print("=== Q1: Number Classification ===")

def classify_number(n: int) -> str:
    """Classifies an integer's sign and parity."""
    if not isinstance(n, int):
        return f"Error: Input '{n}' is not an integer."
    
    if n > 0:
        parity = "even" if n % 2 == 0 else "odd"
        return f"{n} is positive and {parity}"
    elif n < 0:
        parity = "even" if n % 2 == 0 else "odd"
        return f"{n} is negative and {parity}"
    else:
        return "0 is zero (neither positive nor negative, but even)"

test_values = [42, -17, 0, -8, 15]
for val in test_values:
    print(f"  classify_number({val:<3}) -> {classify_number(val)}")

# Explanation: `if / elif / else` tests conditions sequentially and halts at the
# first branch evaluating to True.


# ============================================================
# Q2: Academic Grading System with Boundary Verification
# ============================================================
# Question: Build a grading function that maps percentage scores (0-100) to
# letter grades (A+, A, B, C, D, F) with strict boundary and invalid-input handling.

print("\n=== Q2: Academic Grading System ===")

def calculate_grade(score: float) -> dict:
    """Evaluates percentage score to letter grade and honors designation."""
    if not isinstance(score, (int, float)):
        return {"score": score, "valid": False, "error": "Score must be numeric"}
    if score < 0.0 or score > 100.0:
        return {"score": score, "valid": False, "error": f"Score {score} out of range [0, 100]"}
    
    if score >= 97.0:
        grade, remark = "A+", "Outstanding / Dean's Honor"
    elif score >= 90.0:
        grade, remark = "A", "Excellent"
    elif score >= 80.0:
        grade, remark = "B", "Above Average"
    elif score >= 70.0:
        grade, remark = "C", "Average"
    elif score >= 60.0:
        grade, remark = "D", "Pass"
    else:
        grade, remark = "F", "Fail / Needs Retake"
        
    return {"score": score, "valid": True, "grade": grade, "remark": remark}

sample_scores = [100.0, 93.5, 89.9, 75.0, 62.0, 48.5, -5.0, 105.0]
for sc in sample_scores:
    res = calculate_grade(sc)
    if res["valid"]:
        print(f"  Score: {sc:<5} -> Grade: {res['grade']:<2} ({res['remark']})")
    else:
        print(f"  Score: {sc:<5} -> REJECTED: {res['error']}")

# Explanation: Order of branches matters in `elif`. Always evaluate the most restrictive
# threshold (e.g. >= 97) before broader thresholds (>= 90).


# ============================================================
# Q3: Gregorian Leap Year Determination
# ============================================================
# Question: Implement the full Gregorian calendar leap year rule:
# A year is a leap year if it is divisible by 4, EXCEPT century years,
# which must also be divisible by 400.

print("\n=== Q3: Leap Year Determination ===")

def is_leap_year(year: int) -> tuple[bool, str]:
    """Determines leap year status with explanatory rationale."""
    if not isinstance(year, int) or year <= 0:
        return False, "Year must be a positive integer"
    
    if year % 400 == 0:
        return True, f"{year} is a leap year (divisible by 400)"
    elif year % 100 == 0:
        return False, f"{year} is NOT a leap year (century year not divisible by 400)"
    elif year % 4 == 0:
        return True, f"{year} is a leap year (divisible by 4 and not a century year)"
    else:
        return False, f"{year} is NOT a leap year (not divisible by 4)"

test_years = [2000, 1900, 2024, 2023, 2400, 2100]
for yr in test_years:
    is_leap, reason = is_leap_year(yr)
    flag = "LEAP YEAR" if is_leap else "COMMON YEAR"
    print(f"  {yr:<5} -> [{flag:<11}] {reason}")

# Explanation: Checking `year % 400 == 0` first avoids complex compound Boolean expressions
# and handles centuries like 1900 vs 2000 accurately.


# ============================================================
# Q4: Progressive Marginal Income Tax Calculator
# ============================================================
# Question: Compute progressive tax for an income using marginal tax brackets.
# (Taxing slices of income at respective rates rather than the entire amount flatly).

print("\n=== Q4: Progressive Tax Calculator ===")

def calculate_marginal_tax(taxable_income: float) -> dict:
    """Calculates progressive tax across graduated income brackets."""
    if taxable_income < 0:
        raise ValueError("Taxable income cannot be negative.")
    
    # Brackets: (upper_limit, marginal_rate)
    brackets = [
        (10_000, 0.00),   # First 10,000 at 0%
        (40_000, 0.10),   # 10,001 to 40,000 at 10%
        (85_000, 0.20),   # 40,001 to 85,000 at 20%
        (float('inf'), 0.30)  # Over 85,000 at 30%
    ]
    
    total_tax = 0.0
    previous_limit = 0.0
    breakdown = []
    
    for limit, rate in brackets:
        if taxable_income > previous_limit:
            # Portion of income subject to this bracket
            taxable_slice = min(taxable_income, limit) - previous_limit
            tax_for_slice = taxable_slice * rate
            total_tax += tax_for_slice
            breakdown.append({
                "bracket": f"${previous_limit:,.0f} - ${limit:,.0f}" if limit != float('inf') else f">${previous_limit:,.0f}+",
                "rate": f"{int(rate * 100)}%",
                "slice": taxable_slice,
                "tax": tax_for_slice
            })
            previous_limit = limit
        else:
            break
            
    effective_rate = (total_tax / taxable_income * 100) if taxable_income > 0 else 0.0
    return {
        "income": taxable_income,
        "total_tax": total_tax,
        "effective_rate": effective_rate,
        "breakdown": breakdown
    }

income_examples = [8_500, 25_000, 60_000, 120_000]
for inc in income_examples:
    report = calculate_marginal_tax(inc)
    print(f"  Income: ${report['income']:>7,.0f} | Total Tax: ${report['total_tax']:>7,.2f} | Effective Rate: {report['effective_rate']:.1f}%")

# Explanation: Real-world calculations apply progressive brackets with conditionals
# to prevent "tax cliff" anomalies where earning $1 more reduces net income.


# ============================================================
# Q5: Triangle Validity and Geometric Classification
# ============================================================
# Question: Given three side lengths, determine:
# 1. Can they form a valid triangle (Triangle Inequality Theorem: a+b>c, a+c>b, b+c>a)?
# 2. If valid, classify as Equilateral, Isosceles, or Scalene.
# 3. Check if it is a Right-Angled triangle using Pythagorean theorem with float tolerance.

print("\n=== Q5: Triangle Classification ===")

def classify_triangle(a: float, b: float, c: float) -> dict:
    """Validates and classifies triangle sides."""
    # Side lengths must be positive
    if a <= 0 or b <= 0 or c <= 0:
        return {"valid": False, "reason": "All sides must be strictly positive"}
    
    # Triangle Inequality Theorem
    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        return {"valid": False, "reason": "Fails triangle inequality (sum of 2 sides <= 3rd side)"}
    
    # Side equality classification
    if a == b == c:
        triangle_type = "Equilateral"
    elif a == b or b == c or a == c:
        triangle_type = "Isosceles"
    else:
        triangle_type = "Scalene"
        
    # Right-angled check (a^2 + b^2 == c^2 for sorted sides)
    sides = sorted([a, b, c])
    is_right_angled = abs((sides[0]**2 + sides[1]**2) - sides[2]**2) < 1e-9
    
    return {
        "valid": True,
        "type": triangle_type,
        "is_right_angled": is_right_angled,
        "perimeter": a + b + c
    }

tri_tests = [
    (5, 5, 5),
    (5, 5, 8),
    (3, 4, 5),
    (1, 2, 10),
    (6, 8, 10),
]

for t in tri_tests:
    res = classify_triangle(*t)
    if res["valid"]:
        rt = " + Right-Angled" if res["is_right_angled"] else ""
        print(f"  Sides {str(t):<12} -> Valid {res['type']}{rt} (Perimeter: {res['perimeter']})")
    else:
        print(f"  Sides {str(t):<12} -> INVALID ({res['reason']})")

# Explanation: Float comparisons for geometry should use epsilon tolerance (`1e-9`)
# to guard against round-off inaccuracy in calculations like Pythagorean theorem.


# ============================================================
# Q6: 24-Hour Time of Day and Greeting Scheduler
# ============================================================
# Question: Parse an hour integer (0-23) and return a greeting and period of day:
# Night, Early Morning, Morning, Afternoon, Evening, or Night, with error reporting.

print("\n=== Q6: Time of Day Classification ===")

def get_time_period(hour: int) -> dict:
    """Classifies an hour into greeting and circadian period."""
    if not isinstance(hour, int) or hour < 0 or hour > 23:
        return {"valid": False, "error": f"Invalid hour: {hour}. Must be between 0 and 23."}
    
    if 5 <= hour < 8:
        period, greeting = "Early Morning", "Good dawn! Ready for an early start?"
    elif 8 <= hour < 12:
        period, greeting = "Morning", "Good morning!"
    elif 12 <= hour < 17:
        period, greeting = "Afternoon", "Good afternoon!"
    elif 17 <= hour < 21:
        period, greeting = "Evening", "Good evening!"
    else:  # Covers 21-23 and 0-4
        period, greeting = "Night", "Good night! Time to rest."
        
    return {"valid": True, "hour": hour, "period": period, "greeting": greeting}

test_hours = [2, 6, 9, 14, 18, 22, -1, 25]
for h in test_hours:
    res = get_time_period(h)
    if res["valid"]:
        print(f"  Hour {h:02d}:00 -> [{res['period']:<13}] {res['greeting']}")
    else:
        print(f"  Hour {str(h):<5} -> {res['error']}")

# Explanation: Python chained comparisons (e.g., `5 <= hour < 8`) make range checks
# clean and readable without redundant `and` operators.


# ============================================================
# Q7: Body Mass Index (BMI) Health Risk Categorizer
# ============================================================
# Question: Implement a BMI calculator that accepts metric (kg, meters) or
# imperial (lbs, inches), calculates BMI, and categorizes per WHO standards.

print("\n=== Q7: BMI Health Categorizer ===")

def compute_bmi(weight: float, height: float, unit_system: str = "metric") -> dict:
    """Computes BMI and WHO classification."""
    if weight <= 0 or height <= 0:
        return {"valid": False, "error": "Weight and height must be strictly positive"}
    
    if unit_system.lower() == "metric":
        # weight in kg, height in meters
        bmi = weight / (height ** 2)
    elif unit_system.lower() == "imperial":
        # weight in lbs, height in inches (BMI = lbs * 703 / inches^2)
        bmi = (weight * 703.0) / (height ** 2)
    else:
        return {"valid": False, "error": f"Unknown unit system '{unit_system}'"}
        
    # WHO classification
    if bmi < 18.5:
        category, risk = "Underweight", "Possible nutritional deficiency"
    elif bmi < 25.0:
        category, risk = "Normal weight", "Low risk (healthy range)"
    elif bmi < 30.0:
        category, risk = "Overweight (Pre-obese)", "Moderate risk"
    elif bmi < 35.0:
        category, risk = "Obese Class I", "High risk"
    elif bmi < 40.0:
        category, risk = "Obese Class II", "Very high risk"
    else:
        category, risk = "Obese Class III (Severe)", "Extremely high risk"
        
    return {
        "valid": True,
        "bmi": round(bmi, 2),
        "category": category,
        "risk": risk
    }

patients = [
    {"name": "Patient A", "weight": 48.0, "height": 1.65, "unit": "metric"},
    {"name": "Patient B", "weight": 70.0, "height": 1.75, "unit": "metric"},
    {"name": "Patient C", "weight": 85.0, "height": 1.70, "unit": "metric"},
    {"name": "Patient D", "weight": 210.0, "height": 70.0, "unit": "imperial"},
]

for p in patients:
    res = compute_bmi(p["weight"], p["height"], p["unit"])
    print(f"  {p['name']}: BMI={res['bmi']} -> {res['category']} ({res['risk']})")

# Explanation: Combining input normalization (metric/imperial conversion) with conditional
# thresholds produces robust, production-style domain services.


# ============================================================
# Q8: E-Commerce Shipping & Discount Rule Engine
# ============================================================
# Question: Build an e-commerce order checkout calculator applying tiered discounts,
# membership perks (Bronze/Silver/Gold/Platinum), promo codes, and shipping fees.

print("\n=== Q8: E-Commerce Rule Engine ===")

def calculate_checkout_total(
    cart_total: float,
    membership: str = "regular",
    promo_code: str = "",
    is_express: bool = False
) -> dict:
    """Calculates final order total with tiered discounts and shipping rules."""
    if cart_total < 0:
        raise ValueError("Cart total cannot be negative")
        
    discount = 0.0
    membership = membership.lower()
    
    # 1. Membership discounts
    if membership == "platinum":
        discount = max(discount, 0.20)
    elif membership == "gold":
        discount = max(discount, 0.15)
    elif membership == "silver":
        discount = max(discount, 0.10)
    elif membership == "bronze":
        discount = max(discount, 0.05)
        
    # 2. Promotional code overrides or additions
    applied_promo = False
    if promo_code.upper() == "SAVE25" and cart_total >= 100.0:
        discount = max(discount, 0.25)
        applied_promo = True
    elif promo_code.upper() == "FREESHIP":
        applied_promo = True

    discounted_subtotal = cart_total * (1.0 - discount)
    
    # 3. Shipping rules
    # Free standard shipping for cart >= $50 or Platinum members or FREESHIP promo
    if promo_code.upper() == "FREESHIP" or membership == "platinum" or discounted_subtotal >= 50.0:
        shipping_fee = 0.0 if not is_express else 9.99
    else:
        shipping_fee = 5.99 if not is_express else 14.99
        
    final_total = discounted_subtotal + shipping_fee
    
    return {
        "cart_total": cart_total,
        "discount_pct": int(discount * 100),
        "discount_amount": round(cart_total * discount, 2),
        "discounted_subtotal": round(discounted_subtotal, 2),
        "shipping_fee": shipping_fee,
        "final_total": round(final_total, 2),
        "promo_applied": applied_promo
    }

orders = [
    {"cart": 45.0, "tier": "regular", "promo": "", "express": False},
    {"cart": 45.0, "tier": "regular", "promo": "FREESHIP", "express": False},
    {"cart": 150.0, "tier": "silver", "promo": "SAVE25", "express": True},
    {"cart": 200.0, "tier": "platinum", "promo": "", "express": True},
]

for o in orders:
    summary = calculate_checkout_total(o["cart"], o["tier"], o["promo"], o["express"])
    print(f"  Subtotal: ${summary['cart_total']:<5.1f} | Tier: {o['tier']:<8} | Discount: {summary['discount_pct']}% | Shipping: ${summary['shipping_fee']:<4.2f} | Final: ${summary['final_total']:.2f}")

# Explanation: Multi-stage conditional evaluation mirrors real-world business logic
# where rules can interact, override, or stack up additively.


# ============================================================
# Q9: Password Policy Strength Evaluator
# ============================================================
# Question: Evaluate a user password string against security requirements:
# length, uppercase, lowercase, numbers, special characters, and common patterns.
# Return a numerical score, category (Weak, Fair, Strong, Excellent), and advice.

print("\n=== Q9: Password Strength Evaluator ===")

def evaluate_password_strength(password: str) -> dict:
    """Evaluates password complexity and returns structured recommendations."""
    if not isinstance(password, str):
        return {"valid": False, "score": 0, "status": "INVALID_INPUT"}
    
    score = 0
    feedback = []
    
    # Criterion 1: Length
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    else:
        score += 0
        feedback.append("Increase length to at least 8 characters (12+ recommended)")
        
    # Criterion 2: Character diversity
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    has_special = any(c in special_chars for c in password)
    
    if has_upper:
        score += 1
    else:
        feedback.append("Add uppercase letters")
        
    if has_lower:
        score += 1
    else:
        feedback.append("Add lowercase letters")
        
    if has_digit:
        score += 1
    else:
        feedback.append("Add numeric digits")
        
    if has_special:
        score += 2
    else:
        feedback.append("Add special characters (!@#$...)")
        
    # Check for trivial passwords
    common_passwords = {"password", "123456", "admin", "qwerty", "letmein"}
    if password.lower() in common_passwords:
        score = 0
        feedback = ["Password is an insecure common word!"]
        
    # Strength ranking
    if score >= 7:
        rating = "EXCELLENT"
    elif score >= 5:
        rating = "STRONG"
    elif score >= 3:
        rating = "FAIR"
    else:
        rating = "WEAK"
        
    return {
        "password": password if len(password) <= 10 else password[:3] + "..." + password[-2:],
        "score": score,
        "rating": rating,
        "recommendations": feedback if feedback else ["Password meets high security standards!"]
    }

passwords_to_test = [
    "123456",
    "secret",
    "SecretPass1",
    "P@ssw0rd_Secure!2026",
]

for pwd in passwords_to_test:
    res = evaluate_password_strength(pwd)
    advice = "; ".join(res["recommendations"])
    print(f"  [{res['rating']:<9}] (Score {res['score']}/8) {res['password']:<18} -> {advice}")

# Explanation: Breaking complex multi-attribute validation into additive point scores
# and discrete feedback items is standard practice for user security audits.


# ============================================================
# Q10: Comprehensive Credit & Loan Risk Decision Tree
# ============================================================
# Question: Build an underwriting rule engine that evaluates a loan applicant's:
# Credit Score, Annual Income, Debt-To-Income (DTI) ratio, Employment Years,
# and Requested Loan Amount to yield APPROVED, CONDITIONAL_REVIEW, or REJECTED.

print("\n=== Q10: Loan Risk Decision Engine ===")

def evaluate_loan_application(
    credit_score: int,
    annual_income: float,
    monthly_debt: float,
    loan_amount: float,
    employment_years: float
) -> dict:
    """Executes a financial decision tree for loan approval."""
    rejection_reasons = []
    
    # Basic data validation
    if credit_score < 300 or credit_score > 850:
        return {"decision": "INVALID", "reasons": ["Credit score out of valid range [300, 850]"]}
    if annual_income <= 0 or loan_amount <= 0:
        return {"decision": "INVALID", "reasons": ["Income and loan amount must be positive"]}

    # Metric: Debt-to-Income (DTI) ratio = (monthly_debt * 12) / annual_income
    annual_debt = monthly_debt * 12
    dti_ratio = annual_debt / annual_income
    
    # Metric: Loan-to-Income (LTI) ratio
    lti_ratio = loan_amount / annual_income

    # Underwriting Decision Tree:
    # 1. Hard Rejection criteria
    if credit_score < 580:
        rejection_reasons.append("Credit score below minimum 580 threshold")
    if dti_ratio > 0.45:
        rejection_reasons.append(f"DTI ratio too high ({dti_ratio:.1%}, max allowed 45%)")
    if lti_ratio > 5.0:
        rejection_reasons.append(f"Loan amount exceeds 5x annual income (LTI {lti_ratio:.1f}x)")
    if employment_years < 0.5:
        rejection_reasons.append("Employment duration under 6 months")

    if rejection_reasons:
        return {
            "decision": "REJECTED",
            "credit_score": credit_score,
            "dti_ratio": round(dti_ratio * 100, 1),
            "interest_rate": None,
            "reasons": rejection_reasons
        }

    # 2. Automated Approval vs Manual / Conditional Review
    if credit_score >= 740 and dti_ratio <= 0.30 and employment_years >= 2.0:
        decision = "APPROVED (Prime Tier)"
        base_rate = 5.25
    elif credit_score >= 670 and dti_ratio <= 0.36:
        decision = "APPROVED (Standard Tier)"
        base_rate = 6.75
    elif credit_score >= 620:
        decision = "CONDITIONAL_REVIEW (Manual Underwriter Review Required)"
        base_rate = 8.50
    else:
        decision = "CONDITIONAL_REVIEW (High Risk / Requires Co-Signer)"
        base_rate = 10.25

    return {
        "decision": decision,
        "credit_score": credit_score,
        "dti_ratio": f"{round(dti_ratio * 100, 1)}%",
        "lti_ratio": f"{round(lti_ratio, 1)}x",
        "approved_rate": f"{base_rate:.2f}%",
        "reasons": ["Passed all primary risk gates"]
    }

applicants = [
    {"name": "Alice", "score": 780, "income": 120_000, "debt": 1_200, "loan": 250_000, "exp": 5.0},
    {"name": "Bob",   "score": 680, "income": 75_000,  "debt": 1_800, "loan": 150_000, "exp": 3.0},
    {"name": "Carol", "score": 640, "income": 50_000,  "debt": 1_500, "loan": 80_000,  "exp": 1.5},
    {"name": "Dave",  "score": 520, "income": 40_000,  "debt": 2_000, "loan": 100_000, "exp": 0.2},
]

for app in applicants:
    outcome = evaluate_loan_application(
        app["score"], app["income"], app["debt"], app["loan"], app["exp"]
    )
    print(f"\n  Applicant: {app['name']}")
    print(f"    Decision: {outcome['decision']}")
    if "approved_rate" in outcome:
        print(f"    Terms: Rate {outcome['approved_rate']} | DTI: {outcome['dti_ratio']}")
    else:
        print(f"    Rejection Reasons: {'; '.join(outcome['reasons'])}")

# Summary Output
print("\n" + "=" * 55)
print("  All 10 Questions for Topic 02 - Q01 executed successfully!")
print("=" * 55)
