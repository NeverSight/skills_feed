---
name: mutation-testing
description: Validates test suite quality through mutation testing. Generates intelligent code mutations, runs tests to verify they catch the changes, and identifies gaps in test coverage. Use when evaluating test effectiveness, validating newly written tests, or improving test quality for mission-critical code.
---

# Mutation Testing

Mutation testing evaluates test quality by introducing small, deliberate bugs (mutations) into code and checking if tests catch them. This provides a behavioral measure of test effectiveness beyond simple coverage metrics.

## Core Concept

**Mutation testing workflow**:
1. Generate mutations (small code changes)
2. Run test suite against each mutation
3. Classify results:
   - **Killed**: Test fails (good - test caught the bug)
   - **Survived**: Test passes (bad - test missed the bug)
   - **Timeout**: Test hangs or exceeds time limit
4. Calculate mutation score: `killed / (total - timeouts)`
5. For survived mutants, generate targeted tests

**Why mutation testing matters**: Tests can achieve 100% line coverage while missing critical bugs. Mutation testing reveals if tests actually verify behavior or just execute code.

## When to Use Mutation Testing

Use mutation testing proactively for:

- **After test generation**: Validate that newly written tests are effective
- **Mission-critical code**: Ensure financial, consensus, or security-critical code has thorough tests
- **PR reviews**: Quality gate to prevent merging code with weak tests
- **Refactoring**: Verify tests catch regressions before changing code
- **Complex logic**: Validate tests for boundary conditions, error handling, state machines

**Target mutation scores**:
- Mission-critical code: 90%+
- Core business logic: 80-90%
- General code: 70-80%
- Low-risk code: 60-70%

## AST-Based Mutation Generation

This skill uses Go's `go/ast` and `go/parser` packages to generate intelligent mutations by analyzing code structure.

**Standard Go mutations**:
- Arithmetic operators: +, -, *, /, %
- Relational operators: <, <=, >, >=, ==, !=
- Logical operators: &&, ||, negation
- Conditional boundaries: off-by-one errors
- Statement removal: delete return, assignment, defer
- Constant changes: 0, 1, true, false, nil

See [mutation_operators.md](references/mutation_operators.md) for complete catalog.

## Using the Scripts

All scripts are executable Go programs invoked via shell wrappers.

### 1. Generate Mutations

```bash
~/.claude/skills/mutation-testing/scripts/generate-mutations.sh --file wallet.go --output mutations.json
```

Analyzes Go source file and generates mutation plan with AST node locations.

### 2. Run Mutation Tests

```bash
~/.claude/skills/mutation-testing/scripts/run-mutation-test.sh --mutation-file mutations.json --mutation-id M0 --package ./internal/wallet --output results/M0.json
```

Applies specific mutation, runs tests, reports if mutant was killed or survived.

### 3. Parse Results

```bash
~/.claude/skills/mutation-testing/scripts/parse-results.sh --results 'results/*.json' --output report.json
```

Aggregates mutation results and calculates mutation score.

## Integration with Agents

### mutation-tester Agent

The `mutation-tester` agent orchestrates the mutation testing workflow:
1. Analyzes target code (from git diff or specified files)
2. Generates intelligent mutations using AST analysis
3. Runs tests for each mutation in parallel when possible
4. Identifies surviving mutants and analyzes why tests didn't catch them
5. Generates targeted tests to kill survivors
6. Re-runs mutations to verify improvements
7. Produces detailed mutation report in `.reviews/mutations/`

### test-engineer Integration

After `test-engineer` generates tests, use mutation testing to validate effectiveness:

```
User: "Generate tests for CalculateFee function"
[test-engineer creates comprehensive tests]
User: "Run mutation testing to validate"
[mutation-tester verifies test quality]
```

### code-reviewer Integration

Include mutation scores in PR reviews:

```
User: "/code-review owner/repo#123"
[code-reviewer analyzes changes, invokes mutation-tester]
Review includes: "Mutation score: 82% (18/22 killed), recommend 3 additional tests"
```

## Interpreting Results

### High mutation score (>85%)
Tests are thorough and catch most bugs. Focus on surviving mutants if any are high-impact.

### Medium mutation score (70-85%)
Tests cover major paths but miss edge cases. Review survivors and add boundary tests.

### Low mutation score (<70%)
Significant test gaps. Tests may only verify happy paths. Add error handling, boundary, and negative tests.

### Surviving mutants
For each survivor, consider:
- **Equivalent mutant**: Mutation doesn't change behavior (can ignore)
- **Missing test**: Need test for that code path
- **Weak assertion**: Test runs code but doesn't verify output
- **Boundary condition**: Need edge case test

## Best Practices

**Focus on high-impact code**: Run mutation testing on critical paths, not trivial getters/setters.

**Interpret in context**: Mutation score is a signal, not a goal. A 75% score with good tests covering critical paths may be better than 95% with superficial tests.

**Handle equivalent mutants**: Some mutations don't change behavior (e.g., i++ vs ++i in some contexts). Flag and ignore these.

**Mutation testing is not fuzzing**: Mutations test if existing tests catch changes. Fuzzing tests if code handles unexpected inputs. Both are valuable but different.

**Iterate**: Use mutation testing to guide test improvement, not as one-time audit.

**Performance**: For large codebases, run mutation testing on changed files only (from git diff). Full mutation testing can be done nightly.

## Example Workflow

```go
// Original code in wallet.go
func CalculateFee(amount int64) int64 {
    if amount > 1000 {
        return amount / 100
    }
    return 10
}

// Generated mutations:
// M1: amount >= 1000 (boundary condition)
// M2: amount < 1000 (relational flip)
// M3: amount == 1000 (boundary)
// M4: return amount / 10 (arithmetic change)
// M5: return 0 (constant change)

// Existing test
func TestCalculateFee(t *testing.T) {
    fee := CalculateFee(2000)
    assert.Equal(t, 20, fee)
}

// Mutation results:
// M1: SURVIVED - test doesn't check boundary at 1000
// M2: KILLED - test with 2000 fails
// M3: SURVIVED - test doesn't check exact boundary
// M4: KILLED - wrong calculation detected
// M5: KILLED - wrong result detected

// Score: 60% (3/5 killed)
// Generate tests for M1 and M3:

func TestCalculateFee_Boundary(t *testing.T) {
    // Test exact boundary
    assert.Equal(t, 10, CalculateFee(1000))
    // Test just above boundary
    assert.Equal(t, 10, CalculateFee(1001))
}

// Re-run: 100% (5/5 killed)
```

## Troubleshooting

**"No mutations generated"**: Check that file contains mutatable code (not just type definitions or constants).

**"All mutants timeout"**: Tests may be running too slowly or hanging. Check test implementation.

**"Mutation score very low"**: Tests may only check happy paths. Add error cases, boundary tests, and assertions on actual behavior.

**"Cannot compile mutated code"**: Mutation may have violated type constraints. This is a bug in mutation generation - report it.

## Further Reading

- [references/mutation_operators.md](references/mutation_operators.md) - Complete mutation operator catalog
- [references/best_practices.md](references/best_practices.md) - Advanced mutation testing patterns
- Academic paper: "Are Mutants a Valid Substitute for Real Faults in Software Testing?" (Just et al.)
