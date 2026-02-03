---
name: test-driven-development
description: Enforce Test-Driven Development (TDD) as the default workflow for code changes. Use this skill for feature implementation, bug fixes, refactoring, and any changes requiring correctness verification. Guides agents through Red-Green-Refactor cycles with proper test-first discipline. Triggers on requests like "implement feature," "fix bug," "refactor code," or any task mentioning tests, correctness, or behavior verification.
---

# Test-Driven Development Skill

This skill enforces TDD as the baseline practice for nearly all code changes. TDD is a programming workflow where tests are written before implementation code, ensuring that every change is verified, intentional, and produces clean, maintainable code.

## Core Philosophy

**"Clean code that works"** — Ron Jeffries, summarizing TDD's goal

TDD is not about testing. It's about **design**, **confidence**, and **sustainable pace**. The tests guide you toward better interfaces, simpler implementations, and code that's ready for the next change.

---

## The Canon TDD Workflow

Based on Kent Beck's authoritative definition:

### 1. Write a Test List
Before touching any code, list all expected behavioral variants:
- The basic/happy path case
- Edge cases and boundary conditions  
- Error conditions and invalid inputs
- Integration points with other components

**Mistake to avoid**: Mixing implementation design decisions into this phase. Focus purely on *what* the code should do, not *how*.

### 2. Pick One Test and Write It
Convert exactly one item from your list into a concrete, runnable test with:
- Clear setup (arrange)
- Specific action (act)  
- Meaningful assertion (assert)

The test MUST fail initially — this proves the test is actually testing something.

**Mistakes to avoid**:
- Writing tests without assertions (just for coverage)
- Converting all test list items to tests before making any pass
- Copying computed values into expected values (defeats double-checking)

### 3. Make It Pass (Green)
Write the **minimum code** necessary to make the test pass. This is not the time for:
- Perfect architecture
- Optimization
- Handling cases not yet tested

Commit whatever sins necessary to get green. The goal is to reach a safe, passing state quickly.

**Mistake to avoid**: Mixing refactoring into this phase. Make it work, *then* make it right.

### 4. Refactor (Optional but Encouraged)
Now you may improve the implementation design:
- Remove duplication
- Improve naming and readability
- Extract methods/functions
- Apply design patterns where appropriate

All tests must remain green throughout refactoring.

**Mistakes to avoid**:
- Refactoring further than necessary
- Abstracting too soon (duplication is a hint, not a command)
- Changing behavior while refactoring

### 5. Repeat
Go back to step 2 until the test list is empty.

---

## The Three Laws of TDD (Nano-Cycle)

For fine-grained, second-by-second discipline:

1. **You must write a failing test before you write any production code.**
2. **You must not write more of a test than is sufficient to fail** (or fail to compile).
3. **You must not write more production code than is sufficient to make the currently failing test pass.**

These laws enforce the line-by-line granularity that prevents scope creep and keeps you in flow.

---

## TDD Cycles

TDD operates at multiple time scales, each with distinct rhythms. See [references/cycles.md](references/cycles.md) for detailed guidance on:

- **Nano-cycle** (seconds): Three Laws
- **Micro-cycle** (minutes): Red-Green-Refactor  
- **Milli-cycle** (10 min): Specific/Generic and test ordering
- **Primary cycle** (hourly): Architecture checkpoints

---

## When to Apply TDD

### Always Use TDD For:
- New feature implementation
- Bug fixes (write a failing test that reproduces the bug first)
- Refactoring existing code (characterization tests first if tests don't exist)
- Any code where correctness matters
- Complex business logic
- API endpoints and contracts
- Data transformations and calculations

### Acceptable Exceptions:
- Pure exploratory spikes (but throw away the code or add tests after)
- Trivial configuration changes
- Generated code (test the generator or the output, not both)
- Pure UI layout tweaks with no logic (though visual regression tests help)
- Emergency hotfixes (add tests immediately after)
- Code that truly cannot be tested (extremely rare)

**Important**: When skipping TDD, document WHY and create a follow-up task to add tests.

---

## TDD for Bug Fixes

The most reliable bug-fix workflow:

1. **Write a failing test** that reproduces the exact bug
2. **Verify it fails** for the right reason
3. **Fix the bug** with minimal code changes
4. **Verify the test passes**
5. **Refactor** if the fix introduced code smells
6. **Run the full test suite** to catch regressions

This proves the bug existed, proves it's fixed, and prevents regression forever.

---

## TDD with Legacy Code

Working with untested existing code is common. See [references/legacy-code.md](references/legacy-code.md) for comprehensive guidance on:

- Writing **characterization tests** to document current behavior
- Using the **Strangler Fig** pattern to grow tested code around legacy code
- Creating **seams** via dependency injection or method extraction
- **Approval testing** for complex code behavior
- **Sprouting** methods to create testable units

Key principle: Don't retrofit TDD to all legacy code. Instead, test what you change and extract new logic into testable units.

---

## Test Quality Guidelines

### Good Tests Are:
- **Fast**: Unit tests should run in milliseconds
- **Isolated**: No test depends on another test's state
- **Repeatable**: Same result every time, in any environment
- **Self-validating**: Pass or fail with no manual interpretation
- **Timely**: Written before or alongside the production code

### Test Naming
Use descriptive names that document behavior:
```
✓ should return empty list when no items match filter
✓ should throw ValidationError when email format is invalid
✓ should apply discount when cart total exceeds threshold
✗ testCalculate (too vague)
✗ test1, test2 (meaningless)
```

### One Assertion Per Test (Conceptually)
Each test should verify one logical concept. Multiple assertions are fine if they verify the same behavior.

### Test the Interface, Not Implementation
- Test inputs and outputs, not internal state
- Avoid testing private methods directly
- If refactoring breaks tests, the tests were too coupled to implementation

---

## Implementation Strategies

When making a test pass, choose your strategy based on confidence and clarity. See [references/implementation-strategies.md](references/implementation-strategies.md) for detailed guidance on:

- **Obvious Implementation**: When the solution is clear
- **Fake It ('Til You Make It)**: When uncertain, hardcode then generalize
- **Triangulation**: When you need multiple examples to find the pattern

You can shift between strategies mid-feature based on feedback. Start with Obvious Implementation, downshift to Fake It if you hit unexpected complexity, then upshift again as clarity returns.

---

## Common Mistakes to Avoid

1. **Skipping the red step**: Always see the test fail first. This proves the test works and you're not testing dead code.

2. **Writing too much test at once**: One test, one behavior. Keep tests small and focused.

3. **Writing too much code to pass**: Only write enough to pass the current test. Resist "while I'm here" additions.

4. **Skipping refactoring**: Refactor continuously during the green phase. This prevents code rot and is not optional.

5. **Testing implementation details**: Test behavior (inputs/outputs), not how it's achieved. If refactoring breaks tests, they were too coupled.

6. **Over-mocking**: Mock at system boundaries, not for everything. Too many mocks make tests brittle and hard to read.

7. **Ignoring the test list**: Keep a visible list of what you're building. Add to it as you discover new cases.

8. **Gold-plating**: Don't add features that aren't driven by a test. Let tests pull the design.

---

## TDD with AI Agents

TDD is especially powerful with AI assistance:

### Why TDD + AI Works
- **Tests act as precise prompts**: A failing test is an unambiguous specification
- **Reduces hallucination**: AI has a concrete, verifiable target
- **Enables autonomous iteration**: AI can run tests, see failures, and self-correct
- **Builds confidence**: Every generated change is immediately validated

### Recommended AI-TDD Workflow
1. **Plan tests first**: Generate a test list from requirements
2. **Write one test**: Make it concrete and specific
3. **Let AI implement**: With a clear failing test as the target
4. **Verify green**: Run the test suite
5. **AI refactors**: Ask for cleanup while keeping tests green
6. **Repeat**: Next test from the list

### Pre-commit Validation
Always run the test suite before committing. Configure pre-commit hooks to:
- Run unit tests
- Check code formatting/linting
- Verify type checking (if applicable)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                     TDD CYCLE                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐      ┌─────────┐      ┌──────────┐           │
│   │  RED    │ ───► │  GREEN  │ ───► │ REFACTOR │ ──┐       │
│   │  Write  │      │  Make   │      │  Clean   │   │       │
│   │  Test   │      │  Pass   │      │  Up      │   │       │
│   └─────────┘      └─────────┘      └──────────┘   │       │
│        ▲                                           │       │
│        └───────────────────────────────────────────┘       │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  RED:      Write a test. Watch it fail.                    │
│  GREEN:    Write minimum code to pass. No more.            │
│  REFACTOR: Clean up. All tests stay green.                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Checklist Before Starting

- [ ] Do I understand the requirements/behavior I'm implementing?
- [ ] Have I written a test list of expected scenarios?
- [ ] Have I picked the simplest test to start with?
- [ ] Is my test environment set up and running?
- [ ] Am I prepared to commit frequently?

## Checklist After Each Cycle

- [ ] Did I see the test fail for the expected reason?
- [ ] Did I write only enough code to make it pass?
- [ ] Did I consider refactoring opportunities?
- [ ] Are all tests still passing?
- [ ] Is my code ready for the next test?

---

## References

- Kent Beck, *Test-Driven Development by Example* (2003)
- Kent Beck, "Canon TDD" (2023) — tidyfirst.substack.com
- Robert C. Martin, "The Three Laws of TDD" and "The Cycles of TDD"
- Martin Fowler, "TestDrivenDevelopment" — martinfowler.com/bliki
- Michael Feathers, *Working Effectively with Legacy Code* (2004)