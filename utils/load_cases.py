import json
import os
from typing import List, Dict, Any

def load_cases(file_path: str) -> List[Dict[str, Any]]:
    """
    Load test cases from JSON file.
    
    Args:
        file_path: Path to the JSON file containing test cases
        
    Returns:
        List of test case dictionaries
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Test cases file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        cases = json.load(f)
    
    return cases

def extract_inputs_outputs(cases: List[Dict[str, Any]]) -> tuple:
    """
    Separate inputs and outputs from test cases.
    
    Args:
        cases: List of test case dictionaries
        
    Returns:
        Tuple of (inputs_list, outputs_list)
    """
    inputs = []
    outputs = []
    
    for case in cases:
        inputs.append(case['input'])
        if 'expected_output' in case:
            outputs.append(case['expected_output'])
        else:
            outputs.append(None)
    
    return inputs, outputs

def get_case_statistics(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate basic statistics about the test cases.
    
    Args:
        cases: List of test case dictionaries
        
    Returns:
        Dictionary with statistics
    """
    if not cases:
        return {}
    
    # Handle both public format (with 'input' wrapper) and private format (direct fields)
    if 'input' in cases[0]:
        # Public cases format
        days = [case['input']['trip_duration_days'] for case in cases]
        miles = [case['input']['miles_traveled'] for case in cases]
        receipts = [case['input']['total_receipts_amount'] for case in cases]
    else:
        # Private cases format
        days = [case['trip_duration_days'] for case in cases]
        miles = [case['miles_traveled'] for case in cases]
        receipts = [case['total_receipts_amount'] for case in cases]
    
    # Only include outputs if they exist
    outputs = [case['expected_output'] for case in cases if 'expected_output' in case]
    
    stats = {
        'total_cases': len(cases),
        'days': {
            'min': min(days),
            'max': max(days),
            'avg': sum(days) / len(days)
        },
        'miles': {
            'min': min(miles),
            'max': max(miles),
            'avg': sum(miles) / len(miles)
        },
        'receipts': {
            'min': min(receipts),
            'max': max(receipts),
            'avg': sum(receipts) / len(receipts)
        }
    }
    
    if outputs:
        stats['outputs'] = {
            'min': min(outputs),
            'max': max(outputs),
            'avg': sum(outputs) / len(outputs)
        }
    
    return stats

if __name__ == "__main__":
    # Test the functions
    public_cases = load_cases("challenge_data/public_cases.json")
    print(f"Loaded {len(public_cases)} public cases")
    
    stats = get_case_statistics(public_cases)
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show a few sample cases
    print("\nSample cases:")
    for i, case in enumerate(public_cases[:3]):
        print(f"  Case {i+1}: {case}") 