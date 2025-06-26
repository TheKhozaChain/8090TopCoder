from pocketflow import Flow
from reimbursement_nodes import (
    LoadReimbursementData,
    AnalyzeInterviewInsights, 
    AnalyzeDataPatterns,
    SegmentCasesByType,
    ExtractSegmentRules,
    CreateUnifiedCalculator,
    TestCalculator,
    RefineCalculator,
    GenerateFinalSolution
)

def create_reimbursement_flow():
    """
    Create the complete reimbursement reverse-engineering flow.
    
    This flow systematically analyzes the legacy system by:
    1. Loading data and interviews
    2. Extracting patterns and insights
    3. Segmenting cases and extracting rules
    4. Creating and testing a unified calculator
    5. Iteratively refining the solution
    6. Generating the final run.sh script
    """
    
    # Create all the nodes
    load_data = LoadReimbursementData()
    analyze_interviews = AnalyzeInterviewInsights()
    analyze_patterns = AnalyzeDataPatterns()
    segment_cases = SegmentCasesByType()
    extract_rules = ExtractSegmentRules()
    create_calculator = CreateUnifiedCalculator()
    test_calculator = TestCalculator()
    refine_calculator = RefineCalculator()
    generate_solution = GenerateFinalSolution()
    
    # Connect the flow
    # Main analysis pipeline
    load_data >> analyze_interviews >> analyze_patterns >> segment_cases
    segment_cases >> extract_rules >> create_calculator >> test_calculator
    
    # Refinement loop - if accuracy is low, refine and test again
    test_calculator - "refine" >> refine_calculator
    refine_calculator - "test" >> test_calculator
    
    # Generate final solution when accuracy is good enough
    test_calculator - "generate" >> generate_solution
    
    # Create the flow starting with data loading
    return Flow(start=load_data)

if __name__ == "__main__":
    # Example usage
    print("Creating reimbursement reverse-engineering flow...")
    
    # Initialize shared store
    shared = {
        "raw_data": {},
        "analysis": {},
        "implementation": {},
        "output": {}
    }
    
    # Create and run the flow
    flow = create_reimbursement_flow()
    print("Running the flow...")
    flow.run(shared)
    
    print("\nFlow completed!")
    print("Check challenge_data/run.sh for the generated solution")
    print("Check private_results.txt for private case results") 