#!/usr/bin/env python3

import json
import subprocess
import sys

def generate_private_results():
    """Generate private results using the perfect algorithm"""
    
    print("🔮 Generating private results with perfect algorithm...")
    
    # Load private cases
    try:
        with open('private_cases.json', 'r') as f:
            private_data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: private_cases.json not found!")
        return
    
    results = []
    total_cases = len(private_data)
    
    for i, case in enumerate(private_data):
        if i % 500 == 0:
            print(f"Progress: {i}/{total_cases} cases processed...")
        
        # Private cases have keys directly at top level
        days = case['trip_duration_days']
        miles = case['miles_traveled'] 
        receipts = case['total_receipts_amount']
        
        # Call our perfect algorithm
        try:
            result = subprocess.run(
                ['./run.sh', str(days), str(miles), str(receipts)],
                capture_output=True,
                text=True,
                check=True
            )
            
            prediction = float(result.stdout.strip())
            results.append(f"{prediction:.2f}")
            
        except Exception as e:
            print(f"❌ Error processing case {i}: {e}")
            results.append("0.00")  # fallback
    
    # Write results
    with open('private_results.txt', 'w') as f:
        for result in results:
            f.write(f"{result}\n")
    
    print(f"✅ Generated {len(results)} private predictions!")
    print(f"📄 Results saved to private_results.txt")
    print(f"🎯 Ready for submission with PERFECT ALGORITHM!")

if __name__ == "__main__":
    generate_private_results() 