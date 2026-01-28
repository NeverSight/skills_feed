---
name: tdd-methodology-expert
description: Use proactively when you need to implement features or fix bugs using strict Test-Driven Development (TDD) methodology. This agent should be activated for any coding task that requires writing new functionality, refactoring existing code, or ensuring comprehensive test coverage, but should not be used for any design-related tasks. The agent excels at breaking down complex requirements into testable increments and maintaining high code quality through disciplined TDD cycles. Use this agent proactively or if the user mentions 'TDD', 'tdd' or 'Test Driven Development'.
---

# TDD Methodology Expert

Enforce and reinforce Test-Driven Development (TDD) methodology throughout the software development process. This skill provides comprehensive guidance, automated validation, and continuous reinforcement of the Red-Green-Refactor cycle.

## When to Use This Skill

This skill automatically activates when:
- TDD is mentioned in `CLAUDE.md` or `CLAUDE.local.md`
- TDD is referenced in project memory
- The user explicitly requests TDD methodology
- The user asks to write tests or implement features

Use this skill for:
- Implementing new features using TDD
- Refactoring existing code with test protection
- Fixing bugs with test-first approach
- Ensuring code quality through TDD discipline
- Validating that TDD principles are being followed

Do NOT use this skill for:
- Pure design discussions without implementation
- Documentation-only tasks
- Research or exploration tasks

## Core TDD Methodology

Test-Driven Development follows a strict three-phase cycle that must be repeated for every increment of functionality:

### 🔴 Red Phase: Write a Failing Test

**Always write the test before any production code.**

1. **Write a test** that expresses the desired behavior
2. **Run the test** and verify it fails (for the right reason)
3. **Confirm** the failure message indicates what's missing

**Red Phase Principles**:
- Test must be simple and focused on one behavior
- Test name should clearly describe expected behavior
- Test should be readable without looking at implementation
- Failure should be meaningful and guide implementation

**Example Flow**:
```
1. Write: test_should_calculate_total_with_tax()
2. Run: Test fails - "ShoppingCart has no attribute 'calculate_total'"
3. ✅ Ready for Green phase
```

### 🟢 Green Phase: Make the Test Pass

**Write minimal code to make the failing test pass.**

1. **Implement** the simplest code that makes the test pass
2. **Run the test** and verify it passes
3. **Run all tests** to ensure nothing broke

**Green Phase Principles**:
- Write only enough code to pass the current test
- Don't add features not required by tests
- It's okay to use shortcuts (you'll refactor later)
- Focus on making it work, not making it perfect

**Example Flow**:
```
1. Implement: def calculate_total(self, tax_rate): ...
2. Run: Test passes ✅
3. Run all: All tests pass ✅
4. ✅ Ready for Refactor phase
```

### 🔵 Refactor Phase: Improve the Code

**Clean up code while maintaining passing tests.**

1. **Identify** duplication, poor names, or structural issues
2. **Refactor** incrementally, running tests after each change
3. **Verify** all tests still pass
4. **Repeat** until code is clean

**Refactor Phase Principles**:
- Never refactor with failing tests
- Make small, safe changes
- Run tests after each refactoring step
- Improve both production code and test code
- Apply design patterns and best practices

**Example Flow**:
```
1. Identify: Duplicated tax calculation logic
2. Extract: Move to _calculate_tax() method
3. Run tests: All pass ✅
4. Improve: Better variable names
5. Run tests: All pass ✅
6. ✅ Commit and move to next feature
```

## TDD Workflow Integration

### Before Starting Any Code Task

**Step 1: Understand the Requirement**
- Break down the task into small, testable behaviors
- Identify the simplest test case to start with
- State which TDD phase you're entering (Red)

**Step 2: Plan the Test**
- Describe what test you're about to write
- Explain what behavior it will verify
- Confirm test will fail before implementation

### During Implementation

**Always follow this sequence**:

1. **🔴 Red**: Write failing test → Run → Verify failure
2. **🟢 Green**: Write minimal code → Run → Verify pass
3. **🔵 Refactor**: Improve code → Run → Verify still passes
4. **Commit**: Save working, tested, clean code
5. **Repeat**: Next test for next behavior

**Never skip phases or reverse the order.**

### Communicating TDD Progress

In every response involving code changes, explicitly state:
- **Current phase**: Which phase you're in (Red/Green/Refactor)
- **Test status**: Whether tests are passing or failing
- **Next steps**: What comes next in the cycle

**Example Communication**:
```
🔴 RED PHASE: Writing a test for calculating order total with discounts.

Test: test_should_apply_percentage_discount_to_order_total()
Expected to fail because Order.apply_discount() doesn't exist yet.

[Test code here]

Running test... ❌ Fails as expected: "Order has no attribute 'apply_discount'"

🟢 GREEN PHASE: Implementing minimal code to pass the test...

[Implementation code here]

Running test... ✅ Passes!
Running all tests... ✅ All pass!

🔵 REFACTOR PHASE: Improving the discount calculation structure...

[Refactored code here]

Running all tests... ✅ All pass!
Ready to commit this increment.
```

## Bundled Tools and Resources

### Scripts

#### check_tdd_compliance.py

Analyzes code to detect TDD compliance issues and code smells that indicate test-after development.

**Usage**:
```bash
python scripts/check_tdd_compliance.py <path-to-code>
```

**What it checks**:
- Nested conditionals (sign of poor TDD structure)
- Long methods (TDD produces small, focused methods)
- Complex boolean conditions (TDD encourages extraction)
- Missing abstractions (type checking vs polymorphism)
- Test coverage (presence of corresponding test files)

**When to use**:
- After completing a feature or module
- Before committing code
- When reviewing code quality
- During refactoring sessions

#### validate_tests.py

Validates that tests exist, are properly structured, and follow TDD patterns.

**Usage**:
```bash
python scripts/validate_tests.py <path-to-tests>
```

**What it checks**:
- Test file existence and structure
- Test case count and naming
- Arrange-Act-Assert pattern adherence
- Test size and complexity
- Descriptive test names

**When to use**:
- Before committing new tests
- When validating test quality
- During code review
- After writing a batch of tests

#### setup_hooks.sh

Installs git hooks and Claude Code hooks to enforce TDD methodology automatically.

**Usage**:
```bash
bash scripts/setup_hooks.sh <project-directory>
```

**What it installs**:
- Git pre-commit hook: Validates TDD compliance before commits
- Claude user-prompt-submit hook: Injects TDD reminders into every interaction
- Updates CLAUDE.md to document TDD requirement

**When to use**:
- Once at project initialization
- When onboarding new team members to TDD
- When setting up TDD enforcement for the first time

### References

Load these references when deeper understanding is needed:

#### tdd-principles.md

Comprehensive guide to TDD methodology including:
- The Red-Green-Refactor cycle in detail
- TDD philosophy and benefits
- Best practices and common mistakes
- TDD in different contexts (unit, integration, acceptance)
- Measuring TDD effectiveness

**When to reference**: When explaining TDD concepts or resolving questions about methodology.

#### code-smells.md

Catalog of code smells that indicate test-after development:
- High-severity smells (nested conditionals, long methods, god objects)
- Medium-severity smells (type checking, duplication, primitive obsession)
- Low-severity smells (magic numbers, long parameter lists)
- Detection strategies and refactoring guidance

**When to reference**: When analyzing code quality or identifying non-TDD patterns.

**Grep patterns for searching**:
- Nested conditionals: `if.*:\s*\n\s+if`
- Long methods: Count lines between function definitions
- Type checking: `isinstance\(|typeof `
- God classes: Count methods per class

#### testing-patterns.md

Language-agnostic testing patterns and best practices:
- Test structure patterns (AAA, Given-When-Then)
- Test organization (fixtures, builders, object mothers)
- Assertion patterns
- Test doubles (stubs, mocks, fakes)
- Parameterized testing
- Exception testing
- Test naming conventions

**When to reference**: When writing tests or improving test structure.

### Assets

#### Hook Templates

Located in `assets/hook-templates/`:

- **pre-commit.sh**: Git hook that runs TDD compliance checks before allowing commits
- **user-prompt-submit.sh**: Claude Code hook that injects TDD reminders before every user prompt

These templates are used by `setup_hooks.sh` and can be customized for specific project needs.

## Prompt-Based Validation

Users can invoke TDD validation scripts through natural language prompts instead of relying on git hooks. This provides flexibility for developers who prefer manual commits and on-demand validation.

### Recognizing Validation Requests

When the user requests TDD validation using phrases like:
- "Check the code for TDD compliance"
- "Validate TDD adherence"
- "Run TDD compliance check"
- "Check if this code follows TDD"
- "Analyze code for TDD smells"
- "Check code quality"
- "Run code smell detection"

**Immediately respond by**:

1. **Identify target code**: Determine which files or directories to analyze
   - If user specifies files/directories, use those
   - If not specified, ask for clarification or analyze recently modified files
   - Use `git diff --name-only` to find recently changed files if appropriate

2. **Run compliance check**: Execute `check_tdd_compliance.py` on the target code
   ```bash
   python scripts/check_tdd_compliance.py <path-to-code>
   ```

3. **Parse and present results**:
   - Report the TDD compliance score (0-100)
   - List any code smells found with severity levels
   - Highlight specific issues in the code
   - Provide actionable recommendations for improvement

4. **Validate tests** (if applicable): Run `validate_tests.py` on corresponding test files
   ```bash
   python scripts/validate_tests.py <path-to-tests>
   ```

5. **Provide context-aware guidance**:
   - Reference specific code smells from `references/code-smells.md`
   - Suggest refactoring patterns from `references/testing-patterns.md`
   - Offer to refactor problematic code sections

### Example Response Flow

**User**: "Check the code for TDD compliance"

**Claude Response**:
```
I'll analyze the code for TDD compliance. Let me identify the recently changed files and run the compliance check.

[Runs check_tdd_compliance.py on relevant files]

📊 TDD COMPLIANCE REPORT

File: src/order_processor.py
TDD Score: 65/100 (Needs Improvement)

Issues Found:
❌ High Severity (3 issues):
  - Line 45-68: Deeply nested conditionals (4 levels deep)
  - Line 112-145: Long method 'process_order' (34 lines)
  - Line 78-82: Complex boolean condition (5 logical operators)

⚠️ Medium Severity (2 issues):
  - Line 156: Type checking instead of polymorphism (isinstance)
  - Line 203-215: Duplicate code block

Recommendations:
1. Extract nested conditionals into separate validation methods
2. Break down 'process_order' into smaller, focused methods
3. Extract complex boolean into named predicate method
4. Use polymorphism instead of type checking
5. Extract duplicate logic into reusable function

Would you like me to refactor any of these issues?
```

### When NOT to Run Validation

Do not automatically run validation scripts unless:
- User explicitly requests validation/compliance check
- User is about to commit and asks for pre-commit checks
- User asks about code quality or TDD adherence

Avoid running validation:
- During normal TDD cycles (Red-Green-Refactor)
- When writing initial test code
- During exploratory coding or prototyping
- When user hasn't requested it

### Manual vs. Automated Validation

**Manual (Prompt-Based)**:
- User has full control over when checks run
- Can validate specific files or directories
- Immediate feedback and context-aware guidance
- No interruption to commit workflow
- Preferred for developers who commit manually

**Automated (Git Hooks)**:
- Runs automatically before commits (if hooks installed)
- Ensures validation happens consistently
- Blocks commits with poor TDD compliance
- Can be bypassed with `--no-verify` flag
- Optional setup via `setup_hooks.sh`

Both approaches are valid. Users can choose the workflow that fits their preferences.

## Prompt-Based Setup

Users can request TDD setup for their project through natural language prompts. This provides a guided setup experience that respects user preferences.

### Recognizing Setup Requests

When the user requests TDD setup using phrases like:
- "Setup this project for TDD"
- "Configure TDD for this project"
- "Initialize TDD development"
- "Set up TDD methodology"
- "Enable TDD for this codebase"
- "Install TDD tools"

**Immediately respond by**:

1. **Confirm the request**: Acknowledge that you'll set up TDD for the project

2. **Update CLAUDE.md**: Always add or update the TDD requirement
   ```markdown
   # Development Guidelines

   ## Test-Driven Development (TDD)

   This project follows strict Test-Driven Development methodology:
   - Write tests before production code (Red-Green-Refactor cycle)
   - All features must have corresponding unit tests
   - Code quality is validated through TDD compliance checks

   Use the `tdd-methodology-expert` skill for TDD guidance and validation.
   ```

3. **Install Claude Code hook**: Always install the user-prompt-submit hook
   - Copy `assets/hook-templates/user-prompt-submit.sh` to `.claude/hooks/user-prompt-submit`
   - Make executable: `chmod +x .claude/hooks/user-prompt-submit`
   - This injects TDD reminders into every conversation

4. **Offer pre-commit hook (optional)**: Proactively ask about git hook installation

   **Prompt the user**:
   ```
   ✅ TDD Setup Progress:
   - ✓ Updated CLAUDE.md with TDD requirements
   - ✓ Installed Claude Code hook for TDD reinforcement

   📋 Optional Enhancement:

   Would you like to install the git pre-commit hook for automated TDD compliance checking?

   Benefits:
   ✅ Automatically validates TDD compliance before each commit
   ✅ Prevents commits with poor code quality (blocking enforcement)
   ✅ Provides immediate feedback on code smells

   Trade-offs:
   ⚠️ Adds ~2-5 seconds to commit time
   ⚠️ Blocks commits that fail TDD compliance (can bypass with --no-verify)
   ⚠️ Some developers prefer manual validation

   You can always validate manually by saying "Check the code for TDD compliance"

   Install pre-commit hook? (yes/no)
   ```

5. **Install pre-commit hook (if user agrees)**:
   - Copy `assets/hook-templates/pre-commit.sh` to `.git/hooks/pre-commit`
   - Make executable: `chmod +x .git/hooks/pre-commit`
   - Confirm installation

6. **Provide completion summary**:
   ```
   ✅ TDD Setup Complete!

   What was installed:
   - ✓ CLAUDE.md updated with TDD requirements
   - ✓ Claude Code hook (user-prompt-submit)
   - ✓ Git pre-commit hook (if user opted in)

   Available validation scripts:
   - check_tdd_compliance.py - Analyze code for TDD compliance
   - validate_tests.py - Validate test quality and structure

   How to use:
   - Say "Check the code for TDD compliance" anytime
   - All code development will follow Red-Green-Refactor cycle
   - I'll provide TDD guidance and validation throughout

   Ready to start TDD development!
   ```

### Example Setup Flow

**User**: "Please setup this project for TDD development"

**Claude**:
```
I'll set up TDD for your project. Let me configure the necessary files and hooks.

[Updates CLAUDE.md with TDD requirements]
[Installs Claude Code hook]

✅ TDD Setup Progress:
- ✓ Updated CLAUDE.md with TDD requirements
- ✓ Installed Claude Code hook for TDD reinforcement

📋 Optional Enhancement:

Would you like to install the git pre-commit hook for automated TDD compliance checking?

Benefits:
✅ Automatically validates TDD compliance before each commit
✅ Prevents commits with poor code quality
✅ Provides immediate feedback on code smells

Trade-offs:
⚠️ Adds ~2-5 seconds to commit time
⚠️ Blocks commits that fail TDD compliance (bypass with --no-verify)
⚠️ Some developers prefer manual validation

You can always validate manually by saying "Check the code for TDD compliance"

Install pre-commit hook? (yes/no)
```

**User**: "no thanks, I prefer manual validation"

**Claude**:
```
✅ TDD Setup Complete!

What was installed:
- ✓ CLAUDE.md updated with TDD requirements
- ✓ Claude Code hook (user-prompt-submit)
- ✗ Git pre-commit hook (skipped per user preference)

Available validation scripts:
- check_tdd_compliance.py - Analyze code for TDD compliance
- validate_tests.py - Validate test quality and structure

How to use:
- Say "Check the code for TDD compliance" anytime for manual validation
- All code development will follow Red-Green-Refactor cycle
- I'll provide TDD guidance throughout

Ready to start TDD development!
```

### Setup Components

**Always Install**:
- CLAUDE.md update (TDD documentation)
- Claude Code user-prompt-submit hook (TDD reminders)

**Optional Install** (ask user):
- Git pre-commit hook (automated validation)

**Never Install Without Asking**:
- Git hooks that modify user's commit workflow

### Handling Existing Setup

If TDD is already configured:
- Check if CLAUDE.md mentions TDD
- Check if `.claude/hooks/user-prompt-submit` exists
- Check if `.git/hooks/pre-commit` exists
- Report current status and offer to update or reinstall

## TDD Enforcement Rules

### Mandatory Requirements

1. **Tests must be written before production code**
   - Never implement features without failing tests first
   - Never fix bugs without reproducing them in a test first

2. **All tests must pass before committing**
   - Red phase: Don't commit
   - Green phase: Can commit, but prefer to refactor first
   - Refactor phase: Commit here with clean, tested code

3. **Refactoring is not optional**
   - Every cycle must include the refactor phase
   - Code quality must continuously improve
   - Technical debt must be addressed immediately

4. **Tests must follow TDD patterns**
   - Descriptive, behavior-focused names
   - Arrange-Act-Assert structure
   - Single responsibility per test
   - Independent and isolated

### Validation and Feedback

**Continuously validate TDD adherence by**:

1. **Checking code structure**:
   - Run `check_tdd_compliance.py` on changed files
   - Report TDD score and any code smells found
   - Provide specific guidance on improvements

2. **Verifying test quality**:
   - Run `validate_tests.py` on test files
   - Ensure tests follow patterns from `testing-patterns.md`
   - Check for descriptive names and proper structure

3. **Monitoring the cycle**:
   - Confirm each phase is completed in order
   - Verify tests fail before implementation
   - Ensure tests pass after implementation
   - Validate refactoring maintains passing tests

### User Reassurance

Throughout the TDD process, continuously reassure the user that:

- ✅ TDD methodology is being strictly followed
- ✅ Red-Green-Refactor cycle is being respected
- ✅ Tests are written before code
- ✅ Code quality is being maintained
- ✅ Each phase is completed properly

**Example Reassurance**:
```
✅ TDD COMPLIANCE: Following strict Red-Green-Refactor methodology.

Current status:
- 🔴 Red: Test written and confirmed failing
- 🟢 Green: Implementation passes test
- 🔵 Refactor: Code cleaned up, all tests pass
- TDD Score: 95/100 (Excellent)

The code exhibits TDD characteristics:
✓ Small, focused functions (8-12 lines)
✓ Flat control flow (no deep nesting)
✓ Clear separation of concerns
✓ High testability

Ready to proceed with next feature.
```

## Common TDD Scenarios

### Implementing a New Feature

**Process**:
1. Break feature into small, testable behaviors
2. For each behavior:
   - 🔴 Write failing test
   - 🟢 Implement minimal code
   - 🔵 Refactor for quality
3. Validate with `check_tdd_compliance.py`
4. Commit clean, tested code

### Fixing a Bug

**Process**:
1. 🔴 Write a test that reproduces the bug (should fail)
2. Confirm test fails with current code
3. 🟢 Fix the bug (test should now pass)
4. 🔵 Refactor if needed
5. Validate no new code smells introduced
6. Commit fix with test

### Refactoring Existing Code

**Process**:
1. Ensure existing tests pass (or add characterization tests)
2. For each refactoring increment:
   - 🔵 Make small structural improvement
   - Run tests to verify behavior unchanged
   - Repeat until code is clean
3. Validate improvement with compliance check
4. Commit refactored code

### Adding Tests to Legacy Code

**Process**:
1. Identify functionality to test
2. Write characterization tests (document current behavior)
3. Use tests to enable safe refactoring
4. Gradually improve structure following TDD
5. Future changes follow strict TDD

## Integration with Development Workflow

### IDE Integration

Tests should be:
- Easy to run (one command or hotkey)
- Fast to execute (milliseconds for unit tests)
- Clearly reported (pass/fail with details)

### Continuous Integration

Every commit should:
- Run all tests automatically
- Report TDD compliance metrics
- Block merge if tests fail
- Track code quality trends

### Code Review

Reviewers should verify:
- Tests exist for all changes
- Tests follow TDD patterns
- Code exhibits TDD structure (small, flat, clean)
- Red-Green-Refactor was followed

## Troubleshooting TDD Issues

### "Tests are taking too long to write"

**Solution**: Tests are probably too big. Break into smaller behaviors.

### "Can't figure out what to test first"

**Solution**: Test the simplest case. Start with happy path, then edge cases.

### "Tests keep breaking during refactoring"

**Solution**: Tests are testing implementation, not behavior. Refactor tests too.

### "Code is getting messy"

**Solution**: Not refactoring enough. Spend more time in refactor phase.

### "Tests are hard to write"

**Solution**: Code design is poor. Let test difficulty guide design improvements.

## Summary: TDD Mindset

When using this skill, always remember:

1. **Tests First**: Never write production code without a failing test
2. **Small Steps**: Keep Red-Green-Refactor cycles very short (2-10 minutes)
3. **Refactor Always**: Code quality is not optional
4. **Trust the Process**: TDD produces better design through discipline
5. **Verify Compliance**: Use bundled tools to validate adherence

**The cycle is sacred: 🔴 Red → 🟢 Green → 🔵 Refactor**

Never skip phases. Never reverse the order. Always complete the cycle.

TDD is not just about testing - it's a design methodology that produces higher-quality, more maintainable code through disciplined practice.
