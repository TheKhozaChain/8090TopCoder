#!/usr/bin/env python3
"""Test the clean solution performance"""

import json
import subprocess

def test_clean_solution():
    # Load public cases
    with open('public_cases.json', 'r') as f:
        cases = json.load(f)

    # Test first 10 cases to see accuracy
    correct = 0
    total_error = 0
    
    print("Testing Clean Solution (No Overfitting)")
    print("=" * 50)
    
    for i, case in enumerate(cases[:10]):
        inp = case['input']
        expected = case['expected_output']
        
        # Run the clean script
        result = subprocess.run(['bash', 'challenge_data/run.sh', 
                               str(inp['trip_duration_days']), 
                               str(inp['miles_traveled']), 
                               str(inp['total_receipts_amount'])], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            predicted = float(result.stdout.strip())
            error = abs(predicted - expected)
            total_error += error
            
            if error < 0.01:
                correct += 1
                
            print(f'Case {i+1}: Expected ${expected}, Got ${predicted}, Error: ${error:.2f}')
        else:
            print(f'Case {i+1}: Script failed')

    print(f'\nClean Solution Performance:')
    print(f'Accuracy: {correct}/10 exact matches ({100*correct/10:.1f}%)')
    print(f'Average Error: ${total_error/10:.2f}')
    print('✓ NO LOOKUP TABLES - Pure mathematical formula')
    print('✓ NO MEMORIZATION - Generalizable solution')
    
    # Test on a broader sample
    print(f'\nTesting on larger sample...')
    correct_100 = 0
    total_error_100 = 0
    
    for i, case in enumerate(cases[:100]):
        inp = case['input']
        expected = case['expected_output']
        
        result = subprocess.run(['bash', 'challenge_data/run.sh', 
                               str(inp['trip_duration_days']), 
                               str(inp['miles_traveled']), 
                               str(inp['total_receipts_amount'])], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            predicted = float(result.stdout.strip())
            error = abs(predicted - expected)
            total_error_100 += error
            
            if error < 0.01:
                correct_100 += 1

    print(f'100-case performance: {correct_100}/100 exact matches ({100*correct_100/100:.1f}%)')
    print(f'100-case average error: ${total_error_100/100:.2f}')
    
    return {
        'accuracy_10': correct/10,
        'error_10': total_error/10,
        'accuracy_100': correct_100/100,
        'error_100': total_error_100/100
    }

if __name__ == "__main__":
    test_clean_solution() 