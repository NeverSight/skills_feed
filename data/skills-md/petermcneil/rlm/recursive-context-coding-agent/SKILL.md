---
name: recursive-context-coding-agent
description: Use recursive context processing with grep/find/uv to handle large codebases. When working with codebases larger than your context window, treat the codebase as an external environment and recursively process it using symbolic execution.
---

# Recursive Context Coding Agent

## When to Use This Skill
- Working with codebases larger than your context window
- Tasks requiring dense access to code throughout a large codebase
- Multi-file refactoring or analysis tasks
- When grep/find operations would be more effective than loading everything into context

## Core Principles (from MIT RLM Paper)

1. **Treat Codebase as External Environment**
   - Don't load entire codebase into context window
   - Store codebase as a variable in a REPL environment
   - Use symbolic handles to reference code sections

2. **Symbolic Recursion**
   - Write code that can invoke itself programmatically
   - Use loops to process slices of the codebase
   - Launch sub-calls for different code sections

3. **REPL Environment**
   - Use grep, find, and other tools to examine code
   - Execute Python scripts with `uv run` to process code
   - Store intermediate results symbolically

## Workflow

### Step 1: Initialize REPL Environment
```bash
# Set up the codebase as a variable
CODEBASE=$(pwd)
Step 2: Recursive Analysis
# Use grep to find relevant code
grep -r "pattern" $CODEBASE --include="*.py" --include="*.js" --include="*.ts"

# Use find to explore directory structure
find $CODEBASE -type f -name "*.py" | head -20
```

### Step 3: Symbolic Processing with Python
# Use uv to run Python scripts for complex processing
```bash
uv run python << 'EOF'
import os
import subprocess

# Process codebase recursively
for root, dirs, files in os.walk('/path/to/codebase'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            # Process each file
            print(f"Processing: {filepath}")
EOF
```

### Step 4: Recursive Sub-Calls
When you need to focus on a specific section:

Extract the relevant code section
Create a new prompt with just that section
Invoke yourself recursively with the focused context
Aggregate results
Example: Large Codebase Refactoring
Problem: Refactor a 10,000-line codebase

RLM Approach:

Store codebase as CODEBASE variable
Use find to identify all files
Use grep to find patterns to refactor
For each file, create a focused prompt
Process files recursively
Aggregate changes
Commands:
```bash
# 1. Find all Python files
FILES=$(find $CODEBASE -name "*.py")

# 2. Process each file recursively
for file in $FILES; do
    # Extract file content
    CONTENT=$(cat $file)
    
    # Create focused prompt
    PROMPT="Refactor this code: $CONTENT"
    
    # Invoke recursively (you would call yourself here)
    # RESULT=$(recursive-call $PROMPT)
    
    # Apply changes
    # echo "$RESULT" > $file
done
```
### Tools to Use
- grep: Search for patterns across the codebase
- find: Navigate and locate files
- `uv run`: Execute Python scripts for complex processing
- sed/awk: Text processing within files
- git: Track changes and revert if needed

### Best Practices
Never load entire codebase into context window
Use symbolic handles for code sections
Process recursively - break down problems into sub-problems
Store intermediate results in variables
Use REPL environment for code execution
Test incrementally - verify changes after each recursive call

### Error Handling
If a recursive call fails, try a different code slice
Use git to revert changes if something goes wrong
Log intermediate results for debugging
Limit recursion depth to prevent infinite loops
