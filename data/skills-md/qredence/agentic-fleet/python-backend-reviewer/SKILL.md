---
name: python-backend-reviewer
description: Expert Python backend code reviewer that identifies over-complexity, duplicates, bad optimizations, and violations of best practices. Use when asked to review Python code quality, check for duplicate code, analyze module complexity, optimize backend code, identify anti-patterns, or ensure adherence to best practices. Ideal for preventing AI-generated code from creating unnecessary files instead of imports, finding repeated validation logic, and catching over-engineered solutions.
---

# Python Backend Code Reviewer

Expert analysis and refactoring of Python backend code to eliminate duplication, reduce complexity, and enforce best practices.

## Overview

This skill helps identify and fix common issues in Python backend code, particularly problems introduced by AI code generation:

- **Duplicate code** across multiple files
- **Recreated utilities** instead of imports
- **Over-engineered** solutions
- **High complexity** functions and classes
- **Anti-patterns** and code smells
- **Concurrency issues** in async code (shared state mutation)

The skill provides automated analysis tools and comprehensive refactoring guidance.

## ⚠️ Architecture-Aware Prioritization

**Static analysis finds issues, but architectural context determines priority.**

Before prioritizing fixes, identify:

1. **Critical paths**: Which code runs on every request?
   - WebSocket/HTTP handlers
   - Main workflow orchestration
   - Shared services/middleware

2. **Secondary paths**: Less critical code
   - CLI tools
   - Scripts
   - Dev-only utilities
   - One-time migrations

3. **Concurrency model**: How is state shared?
   - Are handlers concurrent?
   - Are instances shared across requests?
   - Is there mutable singleton state?

**Prioritization rule**: Correctness in critical paths > Complexity in secondary paths

| Finding               | Critical Path                | Secondary Path  |
| --------------------- | ---------------------------- | --------------- |
| Shared state mutation | 🔴 Fix immediately           | 🟡 Review       |
| High complexity (>25) | 🟡 Refactor carefully        | 🟢 Backlog      |
| Duplicates            | 🟡 Extract if >3 occurrences | 🟢 Nice to have |
| God class             | 🟡 Migrate to façade         | 🟢 Low priority |

## Pragmatic Thresholds

For **orchestration/workflow code**, use realistic thresholds:

| Metric                | Strict Threshold | Pragmatic Threshold | Notes                                        |
| --------------------- | ---------------- | ------------------- | -------------------------------------------- |
| Cyclomatic complexity | 10               | **25**              | Orchestrators naturally have decision points |
| Function length       | 50 lines         | **150 lines**       | Async flows can be longer                    |
| Nesting depth         | 4                | **5**               | Guard clauses help more than extracting      |
| God class methods     | 20               | **N/A**             | OK if it's a **façade** that delegates       |

**Hard limits (always fix):**

- No functions > 300 lines
- No nesting > 7 levels
- No shared-state mutation without synchronization guard

## Quick Start

### 1. Run Automated Analysis

Start with automated tools to identify issues:

```bash
# Detect duplicate code blocks
uv run python scripts/detect_duplicates.py <path>

# Analyze imports and utility reimplementation
uv run python scripts/analyze_imports.py <path>

# Check code complexity
uv run python scripts/complexity_analyzer.py <path>

# Check for concurrency issues (shared state mutation)
uv run python scripts/concurrency_analyzer.py <path>
```

### 2. Review Analysis Results

Each tool outputs:

- **Severity levels**: Warnings (must fix) vs Info (should review)
- **File locations**: Exact line numbers for each issue
- **Specific recommendations**: What to change and why

### 3. Apply Fixes

Use the reference guides to refactor issues:

- See [refactoring_patterns.md](references/refactoring_patterns.md) for step-by-step fixes
- See [python_antipatterns.md](references/python_antipatterns.md) for anti-pattern examples
- See [best_practices.md](references/best_practices.md) for Python conventions

## Main Workflows

### Review a Python File

When a user asks to review a specific file:

1. **Run all analysis tools** on the file:

   ```bash
   python scripts/detect_duplicates.py path/to/file.py
   python scripts/analyze_imports.py path/to/file.py
   python scripts/complexity_analyzer.py path/to/file.py
   ```

2. **Analyze results** and categorize issues:
   - Critical: Duplicates, high complexity, security issues
   - Important: Utility reimplementation, deep nesting
   - Minor: Style issues, minor inefficiencies

3. **Provide specific fixes**:
   - Quote exact code locations with line numbers
   - Show before/after examples
   - Explain why the change improves the code

4. **Offer to implement fixes** if requested

### Check Backend for Duplicates

When a user asks to check a project/module for duplicates:

1. **Run duplicate detection** on the entire directory:

   ```bash
   python scripts/detect_duplicates.py src/
   ```

2. **Group duplicates by severity**:
   - High: 10+ lines duplicated, 3+ occurrences
   - Medium: 5-10 lines, 2+ occurrences
   - Low: Helper functions that could be extracted

3. **Recommend consolidation strategy**:
   - Extract to shared utilities for cross-cutting concerns
   - Create base classes for inherited behavior
   - Use decorators for repeated patterns

### Analyze Module Over-Engineering

When code appears over-engineered:

1. **Run complexity analysis**:

   ```bash
   python scripts/complexity_analyzer.py --max-complexity 10 --max-length 50 path/
   ```

2. **Identify over-engineering patterns**:
   - Premature abstractions (base classes with one implementation)
   - Excessive configuration options
   - God classes (20+ methods)
   - Deep inheritance hierarchies

3. **Suggest simplifications**:
   - Replace abstractions with simple functions
   - Remove unused configuration
   - Split god classes by responsibility
   - Flatten inheritance

4. **Reference specific patterns** from [python_antipatterns.md](references/python_antipatterns.md)

### Optimize Following Best Practices

When asked to optimize code or ensure best practices:

1. **Run all analysis tools** to get baseline metrics

2. **Check against best practices**:
   - DRY principle violations
   - SOLID principle violations
   - Type hint coverage
   - Error handling patterns
   - Async/await consistency

3. **Prioritize optimizations**:
   - First: Correctness (bugs, security)
   - Second: Maintainability (duplicates, complexity)
   - Third: Performance (N+1 queries, inefficiencies)
   - Fourth: Style (naming, imports)

4. **Reference [best_practices.md](references/best_practices.md)** for specific guidelines

### Analyze Concurrency Safety

When reviewing async code that handles concurrent requests:

1. **Run concurrency analysis**:

   ```bash
   uv run python scripts/concurrency_analyzer.py services/ workflows/
   ```

2. **Prioritize by severity**:
   - **Critical**: Fix before production deployment
   - **Warning**: Review for actual sharing patterns
   - **Info**: Consider but often acceptable

3. **Common fixes for shared state mutation**:

   ```python
   # ❌ Before: Mutating shared instance state
   class Workflow:
       async def run(self, task):
           self.current_task = task  # Race condition!

   # ✅ After: Request-scoped state
   class Workflow:
       async def run(self, task):
           execution = ExecutionContext(task=task)
           return await self._execute(execution)
   ```

4. **Alternative patterns**:
   - Pass state through parameters (preferred)
   - Use `contextvars` for request-scoped data
   - Use `asyncio.Lock` for truly shared state
   - Create new instances per request

## Analysis Tools

### detect_duplicates.py

Finds duplicate code blocks using AST analysis.

**Usage:**

```bash
uv run python scripts/detect_duplicates.py <path>
uv run python scripts/detect_duplicates.py --min-lines 10 <path>
```

**Detects:**

- Duplicate functions (identical implementations)
- Duplicate classes
- Repeated code blocks

**Options:**

- `--min-lines N`: Minimum lines for a block to be considered (default: 5)

### analyze_imports.py

Analyzes import organization and detects recreated utilities.

**Usage:**

```bash
uv run python scripts/analyze_imports.py <path>
```

**Detects:**

- Wildcard imports (`from module import *`)
- Relative imports in non-package contexts
- Functions that look like reimplemented utilities
- Common patterns that should use libraries

**Common utilities flagged:**

- JSON serialization → use `json` or `orjson`
- Retry logic → use `tenacity` or `backoff`
- Validation → use `pydantic`
- HTTP clients → use `requests` or `httpx`

### complexity_analyzer.py

Measures cyclomatic complexity, function length, and nesting depth.

**Usage:**

```bash
uv run python scripts/complexity_analyzer.py <path>
uv run python scripts/complexity_analyzer.py --max-complexity 10 --max-length 50 <path>
```

**Metrics:**

- **Cyclomatic complexity**: Number of decision points (default threshold: 10)
- **Function length**: Lines in function (default threshold: 50)
- **Nesting depth**: Maximum levels of nested control structures (threshold: 4)
- **God classes**: Classes with 20+ methods

**Options:**

- `--max-complexity N`: Cyclomatic complexity threshold (default: 10)
- `--max-length N`: Function length threshold (default: 50)

### concurrency_analyzer.py

Detects concurrency issues in async Python code.

**Usage:**

```bash
uv run python scripts/concurrency_analyzer.py <path>
```

**Detects:**

- Shared state mutation in async methods (`self.x = y` in async def)
- Module-level mutable state (shared across requests)
- Missing synchronization patterns
- Potentially unsafe singleton patterns

**Severity levels:**

- **Critical**: Mutation of shared state like `client`, `session`, `agent`, `config`
- **Warning**: Any `self.attr` mutation in async context
- **Info**: Module-level mutable objects

**When to use:** Run on services, handlers, and workflow code that handles concurrent requests.

## Reference Documentation

### python_antipatterns.md

Comprehensive catalog of anti-patterns with examples:

- Code duplication patterns
- Over-engineering examples
- God objects
- Complexity issues
- Import problems
- Error handling mistakes
- Performance anti-patterns

**Use when:** You identify an issue but need to see the anti-pattern and solution

### refactoring_patterns.md

Step-by-step refactoring techniques:

- Extract function/variable
- Consolidate duplicates
- Simplify conditionals
- Break up god classes
- Reduce complexity
- Improve imports

**Use when:** You know what's wrong and need concrete refactoring steps

### best_practices.md

Python backend best practices and principles:

- Core principles (DRY, SOLID)
- Code organization
- Type hints
- Error handling
- Async patterns
- Database practices
- API design
- Security guidelines

**Use when:** Establishing coding standards or need authoritative guidance

## Example Reviews

### Example 1: Duplicate Validation Logic

**User request:** "Review this code for quality issues"

**Analysis:**

```bash
uv run python scripts/detect_duplicates.py api/
```

**Finding:** Email validation duplicated in 5 files

**Recommendation:**

```python
# Extract to utils/validation.py
def validate_email(email: str) -> None:
    if not email or "@" not in email:
        raise ValueError("Invalid email")

# Import everywhere
from utils.validation import validate_email
```

### Example 2: Recreated Retry Logic

**User request:** "Check if we're recreating utility functions"

**Analysis:**

```bash
uv run python scripts/analyze_imports.py services/
```

**Finding:** Custom retry logic in 3 services

**Recommendation:**

```python
# Replace with tenacity
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
async def fetch_data(url: str):
    return await client.get(url)
```

### Example 3: Complex Function

**User request:** "This function is hard to understand"

**Analysis:**

```bash
uv run python scripts/complexity_analyzer.py utils/processor.py
```

**Finding:** Complexity 23, nesting depth 6

**Recommendation:** Extract nested logic into helper functions (see [refactoring_patterns.md](references/refactoring_patterns.md#pattern-extract-nested-logic))

## When NOT to Refactor

⚠️ Avoid refactoring when:

- No tests exist and can't be added
- Close to deadline
- Code won't be modified again
- Would break public APIs without migration path

## Output Format

When reviewing code, structure feedback as:

1. **Summary**: Brief overview of findings
2. **Critical Issues**: Must-fix problems (duplicates, security)
3. **Important Issues**: Should-fix problems (complexity, utilities)
4. **Suggestions**: Nice-to-have improvements
5. **Code Examples**: Specific before/after for each issue
6. **Next Steps**: Recommended action plan

Always include:

- Exact file paths and line numbers
- Severity level for each issue
- Concrete code examples
- References to patterns/practices when applicable
