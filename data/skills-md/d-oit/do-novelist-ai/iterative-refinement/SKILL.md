---
name: iterative-refinement
description: Execute iterative refinement workflows with validation loops until quality criteria are met. Use for test-fix cycles, code quality improvement, performance optimization, or any task requiring repeated action-validate-improve cycles.
---

# Iterative Refinement

Execute workflows iteratively with systematic validation, progress tracking, and intelligent termination.

## When to Use

Use for tasks requiring iterative refinement:
- Test-fix-validate cycles: Fix failures → retest → repeat until passing
- Code quality improvement: Review → fix → review until standards met
- Performance optimization: Profile → optimize → measure until targets achieved
- Progressive enhancement: Iterative improvements until diminishing returns

Don't use for single-pass tasks, purely parallel work, or simple linear workflows.

## Pre-Usage Research (Optional)

Before starting iterations, consider researching:
- Current best practices for your validation tools (search "[tool] best practices 2025")
- Known issues with your tech stack (search "[language] [tool] common issues")
- Optimal configuration for your validators (search "[tool] configuration production")
- Recent improvements or alternatives (search "[tool] vs alternatives 2025")

Benefits:
- Better validators from the start
- Avoid known issues
- Use current best practices
- Save iteration cycles

When to research first:
- Unfamiliar validation tools
- New tech stack
- Complex quality criteria
- High-stakes optimization

## Core Loop Pattern

Every iteration follows:

1. Execute action (fix, optimize, improve)
2. Validate result (test, measure, check)
3. Assess progress (compare to criteria)
4. Decide (continue or stop)

## Instructions

### Step 1: Define Configuration

Establish before starting:

**Success Criteria** (specific and measurable):
- Criterion 1: [Example: "All 50 tests passing"]
- Criterion 2: [Example: "Zero linter warnings"]
- Criterion 3: [Example: "Response time < 100ms"]

**Loop Limits**:
- Max iterations: 5-15 (justify if >20)
- Min iterations: (optional)

**Termination Mode**:
- Fixed: Run exactly N iterations
- Criteria: Stop when success criteria met
- Convergence: Stop when improvements < threshold (e.g., <10% over 3 iterations)
- Hybrid: Combine multiple conditions

### Step 2: Execute Iteration

For each iteration:

1. **Take action** - Apply fixes or implement changes
2. **Run validator** - Execute tests, linters, or measurements
3. **Record progress**:
   ```
   Iteration N:
   - Action: [what was done]
   - Results: [metrics/outcomes]
   - Issues remaining: [count/description]
   - Decision: [Continue/Success/Stop]
   ```
4. **Assess termination**:
   - All criteria met? → SUCCESS
   - Improvement < threshold? → CONVERGED
   - Reached max iterations? → STOP
   - Otherwise → CONTINUE

### Step 3: Pass Context Between Iterations

Each iteration needs:
- Previous results
- Current metrics
- Remaining issues
- Progress trend

This prevents repeating failed approaches.

### Step 4: Handle Stuck States

If no progress for 2-3 iterations:
1. Analyze why progress stopped
2. Try different approach
3. Consider manual intervention
4. Stop if truly stuck

### Step 5: Report Results

```
Loop Summary:
- Iterations: N
- Termination: [Success/Converged/Max/Stuck]
- Initial state: [metrics]
- Final state: [metrics]
- Improvement: [percentage/delta]
- Remaining issues: [list if any]
```

## Validation Best Practices

### Make Validators Specific

Bad: "Check if code is better"
Good: "Run linter and count warnings"

Bad: "See if it's faster"
Good: "Run benchmark: average response time over 100 requests"

### Use Automated Validation

Prefer scripts/tools over manual inspection:
- Test frameworks over reading test code
- Linters over manual code review
- Benchmarks over estimated performance
- Coverage tools over counting tests

### Capture Concrete Metrics

Track measurable progress:
- Test pass rate: 42/50 → 48/50 → 50/50
- Warning count: 23 → 8 → 2 → 0
- Response time: 320ms → 180ms → 95ms → 48ms
- Code coverage: 65% → 78% → 85% → 92%

## Examples

### Example 1: Test Fixing

Task: Fix all failing tests

Configuration:
- Success: 100% tests passing
- Max iterations: 8

Execution:
```
I1: 42/50 → Fix 8 failures → Continue
I2: 48/50 → Fix 2 failures → Continue
I3: 50/50 → SUCCESS ✓
```

### Example 2: Linter Cleanup

Task: Remove all linter warnings

Configuration:
- Success: 0 warnings
- Max iterations: 5

Execution:
```
I1: 15 warnings → Fix → 6 warnings
I2: 6 warnings → Fix → 1 warning
I3: 1 warning → Fix → 0 warnings ✓
```

### Example 3: Performance Loop

Task: Optimize response time

Configuration:
- Success: <50ms OR converged
- Max iterations: 15
- Convergence: <10% over 3 iterations

Execution:
```
I1: 320ms → Optimize → 180ms (44%)
I2: 180ms → Optimize → 95ms (47%)
I3: 95ms → Optimize → 48ms (49%)
SUCCESS (target met)
```

### Example 4: Coverage Improvement

Task: Increase test coverage to 90%

Configuration:
- Success: Coverage ≥ 90%
- Max iterations: 12

Execution:
```
I1: 65% → Write tests → 72%
I2: 72% → Write tests → 81%
I3: 81% → Write tests → 88%
I4: 88% → Write tests → 91% ✓
```

## Language-Specific Tools

For validation tools and commands for your language:
- Python: See tools/python.md
- JavaScript/TypeScript: See tools/javascript.md
- Rust: See tools/rust.md
- Java: See tools/java.md
- Go: See tools/go.md
- C/C++: See tools/cpp.md
- Ruby: See tools/ruby.md
- PHP: See tools/php.md
- C#/.NET: See tools/dotnet.md

## Advanced Usage

For complex workflows, convergence detection, and advanced patterns:
See patterns.md

## Best Practices

### DO:
✓ Define clear, measurable success criteria
✓ Set reasonable max limits (5-15)
✓ Use automated validators
✓ Pass context between iterations
✓ Track concrete metrics
✓ Stop early when criteria met
✓ Detect convergence
✓ Document changes

### DON'T:
✗ Use loops for single-pass tasks
✗ Set high limits (>20) without justification
✗ Skip validation between iterations
✗ Lose context between iterations
✗ Continue after success/convergence
✗ Ignore stuck signals
✗ Use vague criteria
✗ Miss early termination