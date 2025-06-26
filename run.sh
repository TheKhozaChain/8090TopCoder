#!/bin/bash

# Business Logic-Based Reimbursement Calculator
# Based on employee interviews and actual business rules discovered
# Implements the real 60-year-old system logic with calibrated parameters

python3 -c "
import json
import sys
import math
import random
import hashlib

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    '''
    Calculate reimbursement using business logic discovered from employee interviews.
    
    This implements the actual legacy system patterns:
    - Per-diem base system with 5-day bonus (Lisa from Accounting)
    - Mileage tiers with declining curve (Lisa's analysis)
    - Receipt processing with optimal ranges (Kevin's research)
    - Efficiency bonuses for 180-220 miles/day (Kevin's findings)
    - Trip category spending rules (Kevin's analysis)
    - System quirks and bugs (rounding .49/.99, small receipt penalties)
    '''
    
    days = int(trip_duration_days)
    miles = float(miles_traveled)
    receipts = float(total_receipts_amount)
    
    # Calculate derived metrics
    efficiency = miles / days if days > 0 else 0
    daily_spending = receipts / days if days > 0 else 0
    
    # === 1. PER-DIEM BASE SYSTEM ===
    # Lisa: \"$100 a day seems to be the base. But 5-day trips almost always get a bonus\"
    base_per_diem = 100.0
    
    if days == 5:
        base_per_diem = 108.0  # 5-day bonus (confirmed by Lisa)
    elif days == 4 or days == 6:
        base_per_diem = 102.0  # Sweet spot range bonus
    elif days >= 8:
        base_per_diem = 95.0   # Long trip penalty
    
    per_diem_amount = base_per_diem * days
    
    # === 2. MILEAGE TIER SYSTEM ===
    # Lisa: \"First 100 miles... you get the full rate—like 58 cents per mile. After that, it drops\"
    if miles <= 100:
        mileage_amount = miles * 0.58
    else:
        # First 100 miles at full rate
        mileage_amount = 100 * 0.58
        
        # Remaining miles on declining curve (Lisa: \"some kind of curve\")
        remaining_miles = miles - 100
        # Logarithmic decline as Lisa suspected
        decline_rate = 0.52 * math.log(1 + remaining_miles / 100) / math.log(11)
        mileage_amount += remaining_miles * decline_rate
    
    # === 3. EFFICIENCY BONUS SYSTEM ===
    # Kevin: \"sweet spot around 180-220 miles per day where the bonuses are maximized\"
    efficiency_multiplier = 1.0
    
    if 180 <= efficiency <= 220:
        efficiency_multiplier = 1.15  # Kevin's optimal efficiency bonus
    elif 150 <= efficiency < 180:
        efficiency_multiplier = 1.05  # Good efficiency bonus
    elif efficiency > 300:
        efficiency_multiplier = 0.90  # Kevin: \"system thinks you're not actually doing business\"
    elif efficiency < 50:
        efficiency_multiplier = 0.95  # Low efficiency penalty
    
    mileage_amount *= efficiency_multiplier
    
    # === 4. RECEIPT PROCESSING RULES ===
    # Lisa: \"Medium-high amounts—like $600-800—seem to get really good treatment\"
    # Dave: \"if I just have a parking receipt for $12... reimbursement is usually worse\"
    
    if receipts < 30:
        # Very small receipts: worse than submitting nothing
        receipt_amount = 0
        if receipts > 0:
            per_diem_amount *= 0.90  # Dave's small receipt penalty
    elif receipts < 100:
        # Small receipts get poor treatment
        receipt_amount = receipts * 0.40
    elif 600 <= receipts <= 800:
        # Lisa's optimal range: \"really good treatment\"
        receipt_amount = receipts * 0.85
    elif receipts < 600:
        # Medium range: decent treatment
        receipt_amount = receipts * 0.70
    elif receipts <= 1200:
        # High range: diminishing returns (Lisa's observation)
        base_optimal = 600 * 0.85
        excess = receipts - 600
        receipt_amount = base_optimal + excess * 0.55
    else:
        # Very high receipts: significant penalties
        base_amount = 600 * 0.85 + 600 * 0.55
        excess = receipts - 1200
        receipt_amount = base_amount + excess * 0.30
    
    # === 5. TRIP CATEGORY SPENDING ADJUSTMENTS ===
    # Kevin: \"Short trips, keep it under $75 per day. Medium trips... up to $120 per day\"
    if days <= 3:  # Short trips
        if daily_spending > 75:
            receipt_amount *= 0.85  # Overspending penalty
    elif 4 <= days <= 6:  # Medium trips (sweet spot)
        if daily_spending > 120:
            receipt_amount *= 0.80  # Overspending penalty
        elif daily_spending < 40:
            receipt_amount *= 0.90  # Underspending penalty
    else:  # Long trips
        if daily_spending > 90:
            receipt_amount *= 0.70  # Kevin's \"vacation penalty\"
    
    # === 6. COMBINATION BONUSES/PENALTIES ===
    # Kevin: \"5-day trips with 180+ miles per day and under $100 per day—that's a guaranteed bonus\"
    if days == 5 and efficiency >= 180 and daily_spending < 100:
        per_diem_amount *= 1.10  # Kevin's \"sweet spot combo\"
    
    # Kevin: \"High mileage with low spending—usually good\"
    if efficiency > 150 and daily_spending < 60:
        mileage_amount *= 1.08
    
    # Kevin: \"Low mileage with high spending—usually bad\"
    if efficiency < 80 and daily_spending > 100:
        receipt_amount *= 0.85
    
    # === 7. SYSTEM QUIRKS AND BUGS ===
    # Lisa: \"if your receipts end in 49 or 99 cents, you often get a little extra money\"
    receipt_cents = int(round((receipts % 1) * 100))
    if receipt_cents == 49 or receipt_cents == 99:
        receipt_amount *= 1.05  # Lisa's \"rounding bug\"
    
    # === 8. ANTI-GAMING VARIATION ===
    # Marcus: \"I can do the exact same trip twice and get completely different reimbursements\"
    # Lisa: \"5-10%—but it's consistent\"
    
    # Use deterministic seed for consistency in testing
    seed_str = f\"{days}-{miles:.1f}-{receipts:.2f}\"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    random.seed(seed)
    
    variation = random.uniform(0.95, 1.05)  # ±5% variation
    
    # === FINAL CALCULATION ===
    total_reimbursement = (per_diem_amount + mileage_amount + receipt_amount) * variation
    
    # Apply business constraints
    total_reimbursement = max(50.0, total_reimbursement)   # Minimum reimbursement
    total_reimbursement = min(5000.0, total_reimbursement) # Maximum reimbursement
    
    return round(total_reimbursement, 2)

# Parse command line arguments
if len(sys.argv) != 4:
    print('Usage: script.py <days> <miles> <receipts>')
    sys.exit(1)

days = int(sys.argv[1])
miles = float(sys.argv[2])
receipts = float(sys.argv[3])

# Calculate and output result
result = calculate_reimbursement(days, miles, receipts)
print(result)
" "$@"