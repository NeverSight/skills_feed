---
name: python-debugging
description: Toolkit for AI agents to debug Python code autonomously without IDE support. Use when agent needs to debug code, insert breakpoints programmatically, analyze execution state, test hypotheses, or automate debugging workflows. Supports pdb, ipdb, debugpy with programmatic breakpoint insertion, conditional breakpoints, AST-based breakpoint suggestions, and automated debugging workflows for agents.
metadata:
  short-description: Agent autonomous Python debugging - programmatic breakpoints, execution analysis
---

# Python Debugging Skill

Toolkit for AI agents to debug Python code autonomously without IDE dependencies. Enables agents to programmatically insert breakpoints, analyze execution state, test hypotheses, and automate debugging workflows.

## Agent Debugging Workflow

When debugging code, agents should:

1. **Analyze code structure** - Use AST to identify key locations
2. **Insert breakpoints programmatically** - Add breakpoints to inspect state
3. **Execute and inspect** - Run code, check variables at breakpoints
4. **Test hypotheses** - Evaluate expressions, modify variables
5. **Clean up** - Remove breakpoints after debugging

### Quick Debugging Workflow

```bash
# 1. Agent analyzes code and suggests breakpoints
python scripts/smart_breakpoint_suggester.py script.py --only functions --max 3

# 2. Agent inserts breakpoints at key locations
python scripts/insert_breakpoint.py script.py --line 10 --method pdb

# 3. Agent runs code and captures output/variables
python script.py > debug_output.txt 2>&1

# 4. Agent analyzes output and determines next steps

# 5. Agent cleans up breakpoints
python scripts/insert_breakpoint.py script.py --remove-all
```

## Core Workflows

### 1. Debugging New Code

**Workflow:**

1. Get smart suggestions for breakpoint locations
2. Insert breakpoints at suggested locations
3. Run debugging session
4. Clean up breakpoints

**Commands:**

```bash
# Get suggestions
python scripts/smart_breakpoint_suggester.py script.py --only functions --max 3

# Insert breakpoints
python scripts/insert_breakpoint.py script.py --line 10 --method pdb
python scripts/insert_breakpoint.py script.py --line 25 --method pdb

# Run debugging
python script.py

# Clean up
python scripts/insert_breakpoint.py script.py --remove-all
```

### 2. Hypothesis Testing

Agent tests specific conditions or hypotheses using conditional breakpoints.

**Agent Workflow:**
1. Form hypothesis (e.g., "error occurs when x > 100")
2. Insert conditional breakpoint with hypothesis condition
3. Run code - only pauses when condition is true
4. Inspect state when condition is met
5. Validate or refute hypothesis

**Example:**
```bash
# Agent hypothesizes: "Bug occurs when count > 100"
python scripts/conditional_breakpoint.py script.py --line 15 --condition "count > 100"

# Agent runs code - only pauses when condition is true
python script.py  # Only pauses when count > 100
# Agent inspects: (Pdb) p count, p items, pp locals()

# Agent validates hypothesis and fixes code
```

### 3. Automated Code Analysis

Agent uses AST-based analysis to automatically identify debugging points.

**Agent Workflow:**
1. Analyze code structure using AST
2. Identify key locations (function entries, loops, conditionals)
3. Insert breakpoints at strategic locations
4. Run code and collect state information
5. Analyze collected data to find issues

**Example:**
```bash
# Agent analyzes code structure
python scripts/smart_breakpoint_suggester.py script.py --only functions loops --max 5

# Agent automatically inserts breakpoints at suggested locations
python scripts/auto_debug_assistant.py script.py --focus functions --max-breakpoints 3

# Agent collects execution state at each breakpoint
# Agent analyzes collected data to identify issues
```

## Available Tools

### scripts/insert_breakpoint.py

Insert, remove, and list breakpoints in Python code.

**Usage:**

```bash
# Insert breakpoint
python scripts/insert_breakpoint.py script.py --line 10 --method pdb

# Remove breakpoint
python scripts/insert_breakpoint.py script.py --line 10 --remove

# List all breakpoints
python scripts/insert_breakpoint.py script.py --list

# Remove all breakpoints
python scripts/insert_breakpoint.py script.py --remove-all
```

**Supported debuggers:** `pdb`, `ipdb`, `debugpy`

### scripts/conditional_breakpoint.py

Insert conditional breakpoints that only pause when conditions are met.

**Usage:**

```bash
# Conditional breakpoint
python scripts/conditional_breakpoint.py script.py --line 10 --condition "x > 100"

# List conditional breakpoints
python scripts/conditional_breakpoint.py script.py --list
```

**Examples:**

- `"x > 100"` - Only pause when x exceeds 100
- `"i == 10"` - Only pause on 10th iteration
- `"x > 100 and y < 50"` - Complex conditions

### scripts/smart_breakpoint_suggester.py

AI analyzes code structure and suggests optimal breakpoint locations.

**Usage:**

```bash
# Get all suggestions
python scripts/smart_breakpoint_suggester.py script.py

# Only function entries
python scripts/smart_breakpoint_suggester.py script.py --only functions

# Functions and loops
python scripts/smart_breakpoint_suggester.py script.py --only functions loops --max 5
```

**Suggestion types:**

- `functions` - Function entry points
- `loops` - Loop start positions
- `conditionals` - If/elif/else branches
- `exceptions` - Try/except blocks
- `returns` - Return statements
- `assignments` - Key variable assignments

### scripts/auto_debug_assistant.py

Automated debugging assistant that completes entire debugging workflow.

**Usage:**

```bash
# Auto debug with smart suggestions
python scripts/auto_debug_assistant.py script.py

# Focus on specific code structures
python scripts/auto_debug_assistant.py script.py --focus functions

# Quick debug at line
python scripts/auto_debug_assistant.py script.py --quick 10

# More breakpoints
python scripts/auto_debug_assistant.py script.py --max-breakpoints 5
```

## Debugger Commands

Once in debugger (pdb/ipdb), use these commands:

### Execution Control

- `n` (next) - Execute next line
- `s` (step) - Step into function
- `c` (continue) - Continue to next breakpoint
- `q` (quit) - Quit debugger

### Inspection

- `p <variable>` - Print variable value
- `pp <variable>` - Pretty print variable
- `l` (list) - Show current code
- `w` (where) - Show call stack
- `u` (up) - Move up call stack
- `d` (down) - Move down call stack

### Expressions

- Direct variable access - Type variable name to see value
- Python expressions - Execute any Python code
- Modify variables - `x = 100` to change values
- Import modules - `import os; os.getcwd()`

## Agent Debugging Patterns

### Pattern 1: Error Location Debugging

**When:** Agent encounters error traceback

**Agent Steps:**
1. Identify error line from traceback
2. Insert breakpoint before error location
3. Run code and inspect variables at breakpoint
4. Determine root cause
5. Fix code and remove breakpoint

```bash
# Error at line 25: ZeroDivisionError
# Agent inserts breakpoint before error
python scripts/insert_breakpoint.py script.py --line 24 --method pdb
python script.py
# (Pdb) p divisor  # Agent finds divisor is 0
# Agent fixes: add zero check before division
```

### Pattern 2: Hypothesis Testing

**When:** Agent suspects specific condition causes issue

**Agent Steps:**
1. Form hypothesis (e.g., "error when count > 100")
2. Insert conditional breakpoint with hypothesis
3. Run code - only pauses when hypothesis is true
4. Inspect state to validate/refute hypothesis

```bash
# Agent hypothesizes: "Bug occurs when items > 100"
python scripts/conditional_breakpoint.py script.py --line 15 --condition "len(items) > 100"
python script.py  # Only pauses when condition met
# Agent validates hypothesis and fixes code
```

### Pattern 3: Systematic Code Analysis

**When:** Agent needs to understand code flow or find issues

**Agent Steps:**
1. Analyze code structure with AST
2. Get suggestions for key locations
3. Insert breakpoints at strategic points
4. Run and collect state information
5. Analyze collected data

```bash
# Agent systematically analyzes code
python scripts/auto_debug_assistant.py script.py --focus functions --max-breakpoints 5
# Agent collects execution state at each breakpoint
# Agent identifies issues from collected data
```

### Pattern 4: Auto Debug Workflow

```bash
# AI automatically completes debugging workflow
python scripts/auto_debug_assistant.py script.py
# AI will:
# 1. Analyze code structure
# 2. Suggest breakpoint locations
# 3. Insert breakpoints
# 4. Run debugging
# 5. Clean up breakpoints
```

## Debugger Selection for Agents

Agents should select debugger based on availability:

1. **Try `ipdb` first** - Better experience if available
2. **Fallback to `pdb`** - Always available (built-in)
3. **Use `debugpy`** - Only if remote debugging needed

**Agent Logic:**
```python
# Agent checks for ipdb, falls back to pdb
try:
    import ipdb
    debugger_method = 'ipdb'
except ImportError:
    debugger_method = 'pdb'  # Always available
```

**Recommendation:** Always default to `pdb` for maximum compatibility.

## References

See [references/debugging-guide.md](references/debugging-guide.md) for:

- Detailed debugging workflows
- Advanced debugging patterns
- Performance debugging
- Debugging session recording

See [references/debugger-commands.md](references/debugger-commands.md) for:
- Complete command reference
- Basic expression examples
- Debugger API details

See [references/expression-guide.md](references/expression-guide.md) for:
- Comprehensive expression usage guide for agents
- Hypothesis testing with expressions
- Agent debugging scenarios
- Advanced expression patterns

## Important Notes for Agents

- **Breakpoints modify code**: Inserted as code statements, so line numbers shift after insertion
- **Always clean up**: Remove all breakpoints after debugging to restore original code
- **Conditional expressions**: Must be valid Python expressions that evaluate to boolean
- **AST-based analysis**: Smart suggestions work on any valid Python code structure
- **Debugger availability**: Auto assistant detects ipdb, falls back to pdb
- **Non-interactive use**: For automated workflows, capture debugger output via subprocess
- **Error handling**: Check if breakpoint insertion succeeded before running code

