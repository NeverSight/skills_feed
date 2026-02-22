---
name: python-refactor
description: Systematic code refactoring skill that transforms complex, hard-to-understand code into clear, well-documented, maintainable code while preserving correctness. Use when users request "readable", "maintainable", or "clean" code, during code reviews flagging comprehension issues, for legacy code modernization, or in educational/onboarding contexts. Applies structured refactoring patterns with validation.
---

# Python Refactor

## Purpose

Transform complex, hard-to-understand Python code into clear, well-documented, maintainable code while preserving correctness. This skill guides systematic refactoring that prioritizes human comprehension without sacrificing correctness or reasonable performance.

## When to Invoke

Invoke this skill when:
- User explicitly requests "human", "readable", "maintainable", "clean", or "refactor" code improvements
- Code review processes flag comprehension or maintainability issues
- Working with legacy code that needs modernization
- Preparing code for team onboarding or educational contexts
- Code complexity metrics exceed reasonable thresholds
- Functions or modules are difficult to understand or modify
- RED FLAG indicators: file >500 lines with scattered functions and global state, multiple `global` statements, no clear module/class organization, configuration mixed with business logic

Do NOT invoke this skill when:
- Code is performance-critical and profiling shows optimization is needed first
- Code is scheduled for deletion or replacement
- External dependencies require upstream contributions instead
- User explicitly requests performance optimization over readability

## Core Principles

Follow these principles in priority order:

1. **Prefer structured OOP for complex code** - Code with shared state, multiple concerns, or scattered global functions should be restructured into well-organized classes and modules. Script-like code with global state and tangled dependencies benefits most from OOP. However, simple modules with pure functions, CLI tools using click/argparse, and functional data pipelines don't need to be forced into classes.
2. **Clarity over cleverness** - Explicit, obvious code beats implicit, clever code
3. **Preserve correctness** - All tests must pass; behavior must remain identical
4. **Single Responsibility** - Each class and function should do one thing well (SOLID principles)
5. **Self-documenting structure** - Code structure tells what, comments explain why
6. **Progressive disclosure** - Reveal complexity in layers, not all at once
7. **Reasonable performance** - Never sacrifice >2x performance without explicit approval

## Key Constraints

ALWAYS observe these constraints:

- **SAFETY BY DESIGN** - Use mandatory migration checklists for destructive changes. Create new structure, search all usages, migrate all, verify, only then remove old code. NEVER remove code before 100% migration verified.
- **STATIC ANALYSIS FIRST** - Run `flake8 --select=F821,E0602` before tests to catch NameErrors immediately
- **PRESERVE BEHAVIOR** - All existing tests must pass after refactoring
- **NO PERFORMANCE REGRESSION** - Never degrade performance >2x without explicit user approval
- **NO API CHANGES** - Public APIs remain unchanged unless explicitly requested and documented
- **NO OVER-ENGINEERING** - Simple code stays simple; don't add unnecessary abstraction
- **NO MAGIC** - No framework magic, no metaprogramming unless absolutely necessary
- **VALIDATE CONTINUOUSLY** - Run static analysis + tests after each logical change

## Regression Prevention (MANDATORY)

**Refactoring must NEVER introduce technical, logical, or functional regressions.**

Read and apply `references/REGRESSION_PREVENTION.md` before any refactoring session.

**Before each refactoring session:**
- Test suite passes at 100%
- Coverage >= 80% on target code (if not, write tests FIRST)
- Golden outputs captured for critical edge cases
- Static analysis baseline saved

**After each micro-change (not at the end, EVERY SINGLE ONE):**
- `flake8 --select=F821,E999` -> 0 errors
- `pytest -x` -> all passing
- Spot check 1 edge case for unchanged behavior

**If ANY check fails:** STOP -> REVERT -> ANALYZE -> FIX APPROACH -> RETRY

ANY REGRESSION = TOTAL FAILURE OF THE REFACTORING

## Refactoring Workflow

Execute refactoring in four phases with validation at each step.

### Phase 1: Analysis

Before making any changes, analyze the code comprehensively:

1. **Read the entire codebase section** being refactored to understand context
2. **Identify readability issues** using the anti-patterns reference (see `references/anti-patterns.md`):
   - Check for script-like/procedural code (global state, scattered functions, no clear structure)
   - Check for God Objects/Classes (classes doing too much)
   - Complex nested conditionals, long functions, magic numbers, cryptic names, etc.
3. **Assess architecture** (see `references/oop_principles.md`):
   - Is code organized in proper classes and modules?
   - Is there global state that should be encapsulated?
   - Are responsibilities properly separated?
   - Are SOLID principles followed?
   - Is dependency injection used instead of hard-coded dependencies?
4. **Measure current metrics** using `scripts/measure_complexity.py` or `scripts/analyze_multi_metrics.py`
5. **Run linting analysis** (see Tooling Recommendations below for which tool to use)
6. **Check test coverage** - Identify gaps that need filling before refactoring
7. **Document findings** using the analysis template (see `assets/templates/analysis_template.md`)

**Output:** Prioritized list of issues by impact and risk.

### Phase 2: Planning

Plan the refactoring approach systematically with **safety-by-design**:

1. **Identify changes by type:**
   - **Non-destructive:** Renames, documentation, type hints -> Low risk
   - **Destructive:** Removing globals, deleting functions, replacing APIs -> High risk

2. **For DESTRUCTIVE changes - CREATE MIGRATION PLAN (MANDATORY):**
   - Search for ALL usages of each element to be removed
   - Document every found usage with file, line number, and usage type
   - If you cannot create a complete migration plan, you CANNOT proceed with the destructive change

3. **Risk assessment** for each proposed change (Low/Medium/High)
4. **Dependency identification** - What else depends on this code?
5. **Test strategy** - What tests are needed? What might break?
6. **Change ordering** - Sequence changes from safest to riskiest
7. **Expected outcomes** - Document what metrics should improve and by how much

**Output:** Refactoring plan with sequenced changes, migration plans for destructive changes, test strategy, and rollback plan.

### Phase 3: Execution

Apply refactoring patterns using **safety-by-design workflow**.

#### For NON-DESTRUCTIVE changes (safe to do anytime):
1. Rename variables/functions for clarity
2. Extract magic numbers/strings to named constants
3. Add/improve documentation and type hints
4. Add guard clauses to reduce nesting

#### For DESTRUCTIVE changes (removing/replacing code) - STRICT PROTOCOL:

1. **CREATE** new structure (no removal yet) - write new classes/functions, add tests
2. **SEARCH** comprehensively for ALL usages of the element being removed
3. **CREATE** migration checklist documenting every found usage
4. **MIGRATE** one usage at a time, checking off the list, running static analysis + tests after each
5. **VERIFY** complete migration - re-run original searches, should find zero old references
6. **REMOVE** old code only after 100% migration verified

#### Execution Rules

1. **NEVER skip the migration checklist** for destructive changes
2. **Run static analysis BEFORE tests** - Catch NameErrors immediately
3. **One pattern at a time** - Never mix multiple refactoring patterns in one change
4. **Atomic commits** - Each migration step gets its own commit
5. **Stop on ANY error** - Static analysis errors OR test failures require immediate fix/revert

#### Refactoring order (recommended sequence):

1. **Transform script-like code to proper architecture** (if code has global state and scattered functions). See `references/examples/script_to_oop_transformation.md`
2. Rename variables/functions for clarity
3. Extract magic numbers/strings to named constants (as class constants or enums)
4. Add/improve documentation and type hints
5. Extract methods to reduce function length
6. Simplify conditionals with guard clauses
7. Reduce nesting depth
8. Final review: Ensure separation of concerns is clean

**Output:** Refactored code passing all tests with clear commit history.

### Phase 4: Validation

Validate improvements objectively:

1. **Run static analysis FIRST** (catch errors before tests):
   ```bash
   flake8 <file> --select=F821,E0602  # Undefined names/variables
   flake8 <file> --select=F401        # Unused imports
   flake8 <file>                       # Full quality check
   ```
   **MANDATORY:** Zero F821 and E0602 errors required

2. **Run full test suite** - 100% pass rate required

3. **Validate architecture improvements**:
   - Confirm global state has been eliminated or properly encapsulated
   - Verify code is organized in proper modules/classes
   - Check that responsibilities are properly separated
   - Validate against SOLID principles (see `references/oop_principles.md`)

4. **Compare before/after metrics** using `scripts/measure_complexity.py` or `scripts/analyze_multi_metrics.py`

5. **Performance regression check** - Run `scripts/benchmark_changes.py` for hot paths

6. **Generate summary report** using format from `assets/templates/summary_template.md`

7. **Flag for human review** if:
   - Performance degraded >10%
   - Public API signatures changed
   - Test coverage decreased
   - Significant architectural changes were made

**Output:** Comprehensive validation report with test results, metrics comparison, performance benchmarks, and quality summary.

## Refactoring Patterns

Apply these patterns systematically. See `references/patterns.md` for full catalog with examples.

### Key Patterns (summary)

- **Guard Clauses** - Replace nested conditionals with early returns. See `references/patterns.md`
- **Extract Method** - Split large functions into focused units. Resets nesting counter (most powerful for cognitive complexity)
- **Dictionary Dispatch** - Eliminate if-elif chains with lookup tables
- **Match Statement** (Python 3.10+) - switch counts as +1 total, not per branch
- **Named Boolean Conditions** - Extract complex boolean expressions into named variables
- **Encapsulate Global State** - Move globals into classes with proper encapsulation
- **Group Related Functions** - Organize scattered functions into classes by responsibility
- **Create Domain Models** - Replace primitive dicts with dataclasses and enums
- **Apply Dependency Injection** - Replace hard-coded dependencies with injected ones

See `references/cognitive_complexity_guide.md` for cognitive complexity calculation rules and reduction patterns.

### Naming Conventions

- **Variables:** Descriptive names, booleans as `is_active`/`has_permission`/`can_edit`, collections as plurals
- **Functions:** Verb + object (`calculate_total`, `validate_email`), boolean queries as `is_valid()`/`has_items()`
- **Constants:** `UPPERCASE_WITH_UNDERSCORES`, replace magic numbers/strings
- **Classes:** PascalCase nouns (`UserAccount`, `PaymentProcessor`)

### Documentation Patterns

- **Function Docstrings** - Document purpose, args, returns, raises (Google style preferred)
- **Module Documentation** - Purpose and key dependencies
- **Inline Comments** - Only for non-obvious "why"
- **Type Hints** - All public APIs and complex internals

### OOP Transformation Patterns

For transforming script-like code to structured OOP. See `references/examples/script_to_oop_transformation.md` for a complete guide and `references/oop_principles.md` for SOLID principles.

## Anti-Patterns to Fix

See `references/anti-patterns.md` for the full catalog. Priority order:

**Critical:** Script-like/procedural code with global state, God Object/God Class
**High:** Complex nested conditionals (>3 levels), long functions (>30 lines), magic numbers, cryptic names, missing type hints, missing docstrings
**Medium:** Duplicate code, primitive obsession, long parameter lists (>5)
**Low:** Inconsistent naming, redundant comments, unused imports

## Tooling Recommendations

### Primary Stack: Ruff + Complexipy (recommended for new projects)

```bash
pip install ruff complexipy radon wily

ruff check src/                              # Fast linting (Rust, replaces flake8+plugins)
complexipy src/ --max-complexity-allowed 15  # Cognitive complexity (Rust)
radon mi src/ -s                             # Maintainability Index
```

See `references/cognitive_complexity_guide.md` for complete configuration (pyproject.toml, pre-commit hooks, GitHub Actions, CLI usage).

### Alternative: Flake8 (for projects already using it)

The `scripts/analyze_with_flake8.py` and `scripts/compare_flake8_reports.py` scripts use flake8. See `references/flake8_plugins_guide.md` for the curated plugin list.

### Multi-Metric Analysis

Use `scripts/analyze_multi_metrics.py` to combine cognitive complexity (complexipy), cyclomatic complexity (radon), and maintainability index in a single report.

| Metric | Tool | Use |
|--------|------|-----|
| Cognitive Complexity | **complexipy** | Human comprehension |
| Cyclomatic Complexity | **ruff** (C901), radon | Test planning |
| Maintainability Index | radon | Overall code health |

### Metric Targets

- Cyclomatic complexity: <10 per function (warning at 15, error at 20)
- Cognitive complexity: <15 per function (SonarQube default, warning at 20)
- Function length: <30 lines (warning at 50)
- Nesting depth: <=3 levels
- Docstring coverage: >80% for public functions
- Type hint coverage: >90% for public APIs

### Historical Tracking with Wily

Monitor trends over time, not just thresholds. See `references/cognitive_complexity_guide.md` for setup and CI integration.

## Common Refactoring Mistakes

See `references/REGRESSION_PREVENTION.md` for the full guide. Key traps:

1. **Incomplete Migration** - Removing old code before ALL usages are migrated (causes NameErrors)
2. **Partial Pattern Application** - Applying refactoring to some functions but not others
3. **Breaking Public APIs** - Changing function signatures used by external code
4. **Assuming Tests Cover Everything** - Tests pass but runtime errors occur (run static analysis!)

## Output Format

Structure refactoring output using the template from `assets/templates/summary_template.md`. Include:
- Changes made with rationale and risk level
- Before/after metrics comparison table
- Test results and performance impact
- Risk assessment and human review recommendation

## Integration with Same-Package Skills

- **python-testing-patterns** - Set up tests before refactoring, validate coverage after
- **python-performance-optimization** - Deep profiling before/after refactoring
- **python-packaging** - If refactoring a library, handle pyproject.toml and distribution
- **uv-package-manager** - Use `uv run ruff`, `uv run complexipy` for tool execution
- **async-python-patterns** - Reference async patterns when refactoring async code

## Edge Cases and Limitations

**When NOT to Refactor:** Performance-critical optimized code (profile first), code scheduled for deletion, external dependencies (contribute upstream), stable legacy code nobody needs to modify.

**Limitations:** Cannot improve algorithmic complexity (that's algorithm change, not refactoring). Cannot add domain knowledge not in code/comments. Cannot guarantee correctness without tests. Code style preferences vary - adjust based on team conventions.

## Examples

See `references/examples/` for before/after examples:
- `script_to_oop_transformation.md` - Complete transformation from script-like code to clean OOP architecture
- `python_complexity_reduction.md` - Nested conditionals and long functions
- `typescript_naming_improvements.md` - Variable and function naming patterns (cross-language reference)

## Success Criteria

Refactoring is successful when:
1. ZERO regressions - All existing tests pass, behavior unchanged
2. Golden master match - Identical output for documented critical cases
3. Complexity metrics improved (documented in summary)
4. No performance regression >10% (or explicit approval obtained)
5. Documentation coverage improved
6. Code is easier for humans to understand
7. No new security vulnerabilities introduced
8. Changes are atomic and well-documented in git history
9. Wily trend - Complexity not increased compared to previous commit
10. Static analysis shows improvement
