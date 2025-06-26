# PocketFlow Solution for TopCoder Travel Reimbursement Challenge

This repository contains a comprehensive solution to the TopCoder travel reimbursement challenge using the **PocketFlow** framework - a minimalist LLM framework for building robust, maintainable AI systems.

## 🎯 Challenge Overview

The challenge was to reverse-engineer a 60-year-old travel reimbursement system using:
- 1,000 historical input/output examples (`public_cases.json`)
- Employee interviews (`INTERVIEWS.md`)
- Three inputs: `trip_duration_days`, `miles_traveled`, `total_receipts_amount`

## 🏗️ PocketFlow Architecture

Our solution demonstrates proper **Agentic Coding** methodology using PocketFlow's core abstractions:

### Core Components

1. **Nodes** (`reimbursement_nodes.py`): Individual processing units
   - `LoadReimbursementData`: Load and validate input data
   - `AnalyzeInterviewInsights`: Extract business rules from interviews
   - `AnalyzeDataPatterns`: Identify patterns in historical data
   - `SegmentCasesByType`: Group similar cases for analysis
   - `ExtractSegmentRules`: Extract rules per segment
   - `CreateUnifiedCalculator`: Build the final calculator
   - `TestCalculator`: Validate against test cases
   - `RefineCalculator`: Iteratively improve accuracy

2. **Flow** (`reimbursement_flow.py`): Orchestrates the entire pipeline
   - Implements proper error handling and retry logic
   - Manages data flow between nodes
   - Provides comprehensive logging

3. **Clean Implementation** (`clean_flow.py`, `clean_reimbursement_nodes.py`):
   - Anti-overfitting methodology
   - Proper train/validation/test splits
   - Generalization gap monitoring

## 📊 Solution Performance

### Current Implementation
- **Average Error**: ~$119 on validation set
- **Methodology**: Domain knowledge from employee interviews
- **Approach**: Business rules extraction rather than pure data fitting

### Key Business Rules Discovered
1. **Base Per Diem**: ~$95-100/day with bonuses for longer trips
2. **Mileage Tiers**: Declining rates after initial miles
3. **Receipt Processing**: Optimal spending ranges with efficiency bonuses
4. **Trip Duration Effects**: 5+ day trips get additional bonuses

## 🛡️ Anti-Overfitting Measures

Our solution includes comprehensive overfitting prevention:

1. **Data Splitting**: 60% train, 20% validation, 20% test
2. **Complexity Control**: Model depth limitations and regularization
3. **Validation-Based Selection**: Choose models based on validation performance
4. **Generalization Monitoring**: Track train vs validation performance gaps

See `LESSONS_LEARNED_README.md` for detailed analysis of overfitting issues and solutions.

## 🚀 Running the Solution

### Quick Start
```bash
# Run the main solution
./run.sh 5 250 150.75

# Test against all cases
./eval.sh

# Generate submission results
./generate_results.sh
```

### PocketFlow Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the PocketFlow pipeline
python main.py

# Run clean methodology
python clean_flow.py

# Test clean solution
python test_clean_solution.py
```

## 📁 File Structure

```
├── run.sh                          # Main executable solution
├── reimbursement_flow.py           # PocketFlow pipeline
├── reimbursement_nodes.py          # Individual processing nodes
├── clean_flow.py                   # Anti-overfitting pipeline
├── clean_reimbursement_nodes.py    # Clean methodology nodes
├── final_solution.py               # Final calculator implementation
├── LESSONS_LEARNED_README.md       # Overfitting analysis & solutions
├── CLEAN_SOLUTION_SUMMARY.md       # Clean methodology documentation
└── test_clean_solution.py          # Validation scripts
```

## 🧠 Key Insights

### Domain Knowledge vs Data Fitting
- **Winning Approach**: Extract business rules from employee interviews
- **Failed Approach**: Pure data memorization and lookup tables
- **Lesson**: Domain expertise often beats sophisticated ML when data is limited

### PocketFlow Benefits
1. **Modularity**: Each node handles one specific task
2. **Testability**: Individual nodes can be tested in isolation
3. **Maintainability**: Clear separation of concerns
4. **Debuggability**: Comprehensive logging and error handling
5. **Reusability**: Nodes can be reused across different flows

### Methodology Lessons
1. **Start Simple**: Begin with basic models before adding complexity
2. **Validate Early**: Use proper train/validation splits from the beginning
3. **Monitor Generalization**: Watch for overfitting throughout development
4. **Document Everything**: Keep detailed records of experiments and results

## 🎓 Educational Value

This solution serves as a comprehensive example of:
- **Proper ML Methodology**: Avoiding overfitting through good practices
- **Agentic Coding**: Human-AI collaboration in system design
- **PocketFlow Usage**: Real-world application of the framework
- **Domain Knowledge Integration**: Using interviews and business context
- **Error Analysis**: Understanding when and why models fail

## 🤝 Contributing

This solution demonstrates best practices for:
1. Building robust AI systems with PocketFlow
2. Avoiding common ML pitfalls like overfitting
3. Integrating domain knowledge with data science
4. Creating maintainable, testable code

For more details on the methodology, see the comprehensive documentation in `LESSONS_LEARNED_README.md`.

---

**Built with PocketFlow** - A 100-line minimalist LLM framework for Agents, Task Decomposition, RAG, and more. 