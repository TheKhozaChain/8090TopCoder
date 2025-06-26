from pocketflow import Node, BatchNode
import json
import os
from utils.call_llm import call_llm
from utils.load_cases import load_cases, get_case_statistics
from utils.pattern_detector import analyze_data_patterns, segment_cases_by_patterns, find_mathematical_relationships

class LoadReimbursementData(Node):
    """Load and parse the challenge data files."""
    
    def prep(self, shared):
        return {
            "public_cases_path": "challenge_data/public_cases.json",
            "private_cases_path": "challenge_data/private_cases.json",
            "interviews_path": "challenge_data/INTERVIEWS.md"
        }
    
    def exec(self, file_paths):
        # Load test cases
        public_cases = load_cases(file_paths["public_cases_path"])
        private_cases = load_cases(file_paths["private_cases_path"])
        
        # Load interviews
        with open(file_paths["interviews_path"], 'r') as f:
            interviews_text = f.read()
        
        # Get basic statistics
        public_stats = get_case_statistics(public_cases)
        private_stats = get_case_statistics(private_cases)
        
        return {
            "public_cases": public_cases,
            "private_cases": private_cases,
            "interviews": interviews_text,
            "public_stats": public_stats,
            "private_stats": private_stats
        }
    
    def post(self, shared, prep_res, exec_res):
        shared["raw_data"] = exec_res
        print(f"Loaded {len(exec_res['public_cases'])} public cases")
        print(f"Loaded {len(exec_res['private_cases'])} private cases")
        print(f"Loaded interviews ({len(exec_res['interviews'])} characters)")
        return "default"

class AnalyzeInterviewInsights(Node):
    """Extract key insights from employee interviews using LLM."""
    
    def prep(self, shared):
        return shared["raw_data"]["interviews"]
    
    def exec(self, interviews_text):
        prompt = f"""
Analyze these employee interviews about a legacy reimbursement system. Extract key insights about how the system works.

{interviews_text}

Provide structured insights in YAML format:

```yaml
key_insights:
  per_diem_rules:
    base_rate: <estimated base daily rate>
    special_bonuses: <any special day-count bonuses>
    
  mileage_rules:
    tier_structure: <description of mileage tiers>
    rates: <estimated rates per tier>
    efficiency_bonuses: <bonuses for high miles/day>
    
  receipt_processing:
    treatment: <how receipts are processed>
    caps_and_penalties: <any caps or penalties>
    sweet_spots: <optimal receipt amounts>
    
  quirks_and_bugs:
    rounding_issues: <any rounding quirks>
    seasonal_variations: <quarterly or time-based changes>
    historical_artifacts: <suspected legacy bugs>
    
  employee_theories:
    marcus_sales: <key insights from Marcus>
    lisa_accounting: <key insights from Lisa>
    other_patterns: <other mentioned patterns>
```
"""
        
        response = call_llm(prompt)
        
        # Try to parse YAML
        try:
            import yaml
            yaml_content = response.split('```yaml')[1].split('```')[0].strip()
            insights = yaml.safe_load(yaml_content)
        except:
            insights = {"raw_analysis": response, "parsed": False}
        
        return insights
    
    def post(self, shared, prep_res, exec_res):
        shared["raw_data"]["interview_insights"] = exec_res
        print("Extracted interview insights")
        return "default"

class AnalyzeDataPatterns(Node):
    """Use LLM to identify patterns in the numerical data."""
    
    def prep(self, shared):
        return shared["raw_data"]["public_cases"]
    
    def exec(self, public_cases):
        patterns = analyze_data_patterns(public_cases, sample_size=200)
        return patterns
    
    def post(self, shared, prep_res, exec_res):
        shared["analysis"] = {"patterns": exec_res}
        print("Completed pattern analysis")
        return "default"

class SegmentCasesByType(Node):
    """Group cases into segments for detailed analysis."""
    
    def prep(self, shared):
        return {
            "cases": shared["raw_data"]["public_cases"],
            "patterns": shared["analysis"]["patterns"]
        }
    
    def exec(self, data):
        segments = segment_cases_by_patterns(data["cases"], data["patterns"])
        
        # Print segment sizes
        print("Case segmentation:")
        for name, cases in segments.items():
            print(f"  {name}: {len(cases)} cases")
        
        return segments
    
    def post(self, shared, prep_res, exec_res):
        shared["analysis"]["segments"] = exec_res
        return "default"

class ExtractSegmentRules(BatchNode):
    """Extract mathematical rules for each segment."""
    
    def prep(self, shared):
        segments = shared["analysis"]["segments"]
        # Return list of (segment_name, cases) tuples
        return [(name, cases) for name, cases in segments.items() if len(cases) > 5]
    
    def exec(self, segment_data):
        segment_name, cases = segment_data
        relationships = find_mathematical_relationships(cases, segment_name)
        return (segment_name, relationships)
    
    def post(self, shared, prep_res, exec_res_list):
        # Convert list of tuples to dictionary
        rules = {name: relationships for name, relationships in exec_res_list}
        shared["analysis"]["rules"] = rules
        print(f"Extracted rules for {len(rules)} segments")
        return "default"

class CreateUnifiedCalculator(Node):
    """Create a unified calculation engine based on all discovered rules."""
    
    def prep(self, shared):
        return {
            "patterns": shared["analysis"]["patterns"],
            "rules": shared["analysis"]["rules"],
            "insights": shared["raw_data"]["interview_insights"]
        }
    
    def exec(self, analysis_data):
        prompt = f"""
Create a unified reimbursement calculation function based on this analysis:

PATTERNS: {json.dumps(analysis_data['patterns'], indent=2)}

SEGMENT RULES: {json.dumps(analysis_data['rules'], indent=2)}

INTERVIEW INSIGHTS: {json.dumps(analysis_data['insights'], indent=2)}

Create Python code for a calculate_reimbursement function that takes:
- trip_duration_days (int)
- miles_traveled (int) 
- total_receipts_amount (float)

And returns the reimbursement amount (float, rounded to 2 decimal places).

The function should implement the discovered patterns and rules. Include:
1. Base per diem calculation
2. Mileage tier calculations
3. Receipt processing logic
4. Special bonuses (5-day trips, efficiency, etc.)
5. Any quirks or bugs discovered

Provide the code in this format:

```python
def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Implementation here
    return round(reimbursement, 2)
```
"""
        
        response = call_llm(prompt)
        
        # Extract Python code
        try:
            code_start = response.find('```python')
            code_end = response.find('```', code_start + 10)
            if code_start != -1 and code_end != -1:
                calculator_code = response[code_start + 9:code_end].strip()
            else:
                calculator_code = response
        except:
            calculator_code = response
        
        return calculator_code
    
    def post(self, shared, prep_res, exec_res):
        shared["implementation"] = {"calculator_code": exec_res}
        print("Created unified calculator")
        return "default"

class TestCalculator(Node):
    """Test the calculator against known cases."""
    
    def prep(self, shared):
        return {
            "calculator_code": shared["implementation"]["calculator_code"],
            "test_cases": shared["raw_data"]["public_cases"][:100]  # Test on first 100 cases
        }
    
    def exec(self, data):
        # Execute the calculator code
        local_scope = {}
        exec(data["calculator_code"], local_scope)
        calculate_reimbursement = local_scope['calculate_reimbursement']
        
        # Test against cases
        results = []
        exact_matches = 0
        close_matches = 0
        total_error = 0
        
        for case in data["test_cases"]:
            inp = case['input']
            expected = case['expected_output']
            
            try:
                calculated = calculate_reimbursement(
                    inp['trip_duration_days'],
                    inp['miles_traveled'],
                    inp['total_receipts_amount']
                )
                
                error = abs(calculated - expected)
                total_error += error
                
                if error <= 0.01:
                    exact_matches += 1
                if error <= 1.00:
                    close_matches += 1
                
                results.append({
                    "input": inp,
                    "expected": expected,
                    "calculated": calculated,
                    "error": error
                })
                
            except Exception as e:
                results.append({
                    "input": inp,
                    "expected": expected,
                    "error": f"Exception: {e}"
                })
        
        accuracy_stats = {
            "total_tests": len(data["test_cases"]),
            "exact_matches": exact_matches,
            "close_matches": close_matches,
            "exact_accuracy": exact_matches / len(data["test_cases"]) * 100,
            "close_accuracy": close_matches / len(data["test_cases"]) * 100,
            "average_error": total_error / len(data["test_cases"]),
            "calculator_function": calculate_reimbursement
        }
        
        return {
            "results": results,
            "stats": accuracy_stats
        }
    
    def post(self, shared, prep_res, exec_res):
        shared["implementation"]["test_results"] = exec_res
        stats = exec_res["stats"]
        print(f"Test Results:")
        print(f"  Exact matches: {stats['exact_matches']}/{stats['total_tests']} ({stats['exact_accuracy']:.1f}%)")
        print(f"  Close matches: {stats['close_matches']}/{stats['total_tests']} ({stats['close_accuracy']:.1f}%)")
        print(f"  Average error: ${stats['average_error']:.2f}")
        
        # Track refinement attempts to prevent infinite loops
        if "refinement_count" not in shared["implementation"]:
            shared["implementation"]["refinement_count"] = 0
        
        # Determine if we need refinement (max 3 attempts)
        if stats['exact_accuracy'] < 50 and shared["implementation"]["refinement_count"] < 3:
            return "refine"
        else:
            return "generate"

class RefineCalculator(Node):
    """Improve the calculator based on test results."""
    
    def prep(self, shared):
        test_results = shared["implementation"]["test_results"]
        
        # Find the worst errors
        worst_cases = sorted(
            [r for r in test_results["results"] if isinstance(r.get("error"), float)],
            key=lambda x: x["error"],
            reverse=True
        )[:10]
        
        return {
            "current_code": shared["implementation"]["calculator_code"],
            "worst_cases": worst_cases,
            "stats": test_results["stats"]
        }
    
    def exec(self, data):
        worst_cases_text = ""
        for case in data["worst_cases"]:
            inp = case["input"]
            worst_cases_text += f"Input: {inp} | Expected: {case['expected']} | Got: {case['calculated']} | Error: ${case['error']:.2f}\n"
        
        prompt = f"""
Improve this reimbursement calculator. Current accuracy: {data['stats']['exact_accuracy']:.1f}%

CURRENT CODE:
{data['current_code']}

WORST PERFORMING CASES:
{worst_cases_text}

Analyze the errors and improve the calculation logic. Look for:
1. Missing rules or conditions
2. Incorrect coefficients or thresholds
3. Rounding issues
4. Special cases not handled

Provide the improved code in the same format:

```python
def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    # Improved implementation here
    return round(reimbursement, 2)
```
"""
        
        response = call_llm(prompt)
        
        # Extract improved code
        try:
            code_start = response.find('```python')
            code_end = response.find('```', code_start + 10)
            if code_start != -1 and code_end != -1:
                improved_code = response[code_start + 9:code_end].strip()
            else:
                improved_code = response
        except:
            improved_code = response
        
        return improved_code
    
    def post(self, shared, prep_res, exec_res):
        shared["implementation"]["calculator_code"] = exec_res
        shared["implementation"]["refinement_count"] += 1
        print(f"Refined calculator based on errors (attempt {shared['implementation']['refinement_count']})")
        return "test"  # Go back to testing

class GenerateFinalSolution(Node):
    """Generate the final run.sh script and test on private cases."""
    
    def prep(self, shared):
        return {
            "calculator_code": shared["implementation"]["calculator_code"],
            "test_stats": shared["implementation"]["test_results"]["stats"],
            "private_cases": shared["raw_data"]["private_cases"]
        }
    
    def exec(self, data):
        # Create the run.sh script
        calculator_function = data["test_stats"]["calculator_function"]
        
        # Generate results for private cases
        private_results = []
        for case in data["private_cases"]:
            # Handle different format for private cases
            if 'input' in case:
                inp = case['input']
            else:
                inp = case
            try:
                result = calculator_function(
                    inp['trip_duration_days'],
                    inp['miles_traveled'],
                    inp['total_receipts_amount']
                )
                private_results.append(str(result))
            except Exception as e:
                private_results.append("ERROR")
        
        # Create run.sh script content
        run_script = f'''#!/bin/bash

# Reimbursement Calculator - Generated by PocketFlow
# Final accuracy on public cases: {data["test_stats"]["exact_accuracy"]:.1f}%

python3 -c "
{data["calculator_code"]}

import sys
days = int(sys.argv[1])
miles = int(sys.argv[2])
receipts = float(sys.argv[3])

result = calculate_reimbursement(days, miles, receipts)
print(result)
" "$@"
'''
        
        return {
            "run_script": run_script,
            "private_results": private_results
        }
    
    def post(self, shared, prep_res, exec_res):
        shared["output"] = exec_res
        
        # Write the run.sh script
        with open("challenge_data/run.sh", "w") as f:
            f.write(exec_res["run_script"])
        
        # Make it executable
        os.chmod("challenge_data/run.sh", 0o755)
        
        # Write private results
        with open("private_results.txt", "w") as f:
            for result in exec_res["private_results"]:
                f.write(f"{result}\n")
        
        print(f"Generated run.sh script")
        print(f"Generated results for {len(exec_res['private_results'])} private cases")
        print(f"Final accuracy: {shared['implementation']['test_results']['stats']['exact_accuracy']:.1f}%")
        
        return "default" 