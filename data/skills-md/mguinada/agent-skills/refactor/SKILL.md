---
name: refactor
description: "TDD-based code simplification that preserves behavior through tests. Use Red-Green-Refactor cycles to simplify code one test-verified change at a time. **DISTINCT FROM**: General code review or AI rewriting—this skill requires existing tests and only proceeds when tests confirm behavior is preserved. **PROACTIVE**: Auto-invoke when test-covered code has complexity (functions >50 lines, high cyclomatic complexity, duplication) and user wants to simplify it safely. Trigger phrases: 'clean up code', 'make code simpler', 'reduce complexity', 'refactoring help'. **NOT FOR**: Adding features or fixing bugs—use /tdd skill instead."
author: mguinada
version: 1.0.0
tags: [refactoring, tdd, code-quality, simplification]
---

# Refactor Skill

## Overview

**Language Agnostic**: Examples use Python; port to your project's language.

**Core Principles:**
- Functionality preserved through tests
- Small, incremental iterations
- All checks must pass before completion

## Prerequisites

**Before starting refactoring:**

1. **Tests must exist**: If no tests exist for the code, request them first
2. **Tests must pass**: Verify `uv run pytest` passes before starting
3. **Understand the code**: Read and understand what the code does
4. **Create a backup**: Optionally commit current state before changes

## Refactoring Process

### Phase 1: Analysis

1. **Read the target code** thoroughly to understand its purpose
2. **Identify code smells** - see [code-smells.md](references/code-smells.md) for detection patterns
3. **List refactoring opportunities** (wait for user approval before implementing)

### Phase 2: TDD Cycle for Each Change

For **each discrete refactoring iteration**:

#### 🔴 RED (if applicable)
- If adding new simplified behavior, write a failing test first
- If only simplifying existing code, skip to GREEN phase
- Run tests to confirm the new test fails

#### 🟢 GREEN
- Make **minimal changes** to pass the tests
- Focus on making tests pass, not perfection
- Run `uv run pytest` after each small change
- Iterate until tests are green

#### 🔵 REFACTOR
- Apply simplification while keeping tests green
- Extract functions, improve naming, reduce complexity
- **Continuously run tests** after each small change
- Never batch multiple changes - one small step at a time

#### ✅ VERIFY
- Run `uv run pytest` to ensure all tests pass
- Run `uv run ruff check src/` for lint checks
- Run `uv run mypy src/` for type checks
- If any check fails, fix and repeat verification

### Phase 3: Final Verification

After all refactoring iterations complete:

```bash
# Run full CI pipeline until everything passes
bin/ci-local
```

This runs:
1. Lint checks (`ruff`)
2. Static type checks (`mypy`)
3. Tests with coverage (`pytest`)

**Repeat** until all checks pass with no errors.

## Refactoring Patterns

For common refactoring patterns with before/after examples, see [patterns.md](references/patterns.md).

**Includes:** Prompt refactoring patterns for code that contains prompts or prompt templates.

## Examples

### Inline: Extract Function

**Before** - complex function with embedded calculation:

```python
def generate_report(users, threshold):
    result = []
    for user in users:
        score = user.login_count * 0.3 + user.posts * 0.7
        if score >= threshold:
            result.append({"name": user.name, "score": score})
    return result
```

**After** - extracted calculation improves readability and testability:

```python
def calculate_engagement_score(user) -> float:
    return user.login_count * 0.3 + user.posts * 0.7

def generate_report(users, threshold):
    result = []
    for user in users:
        score = calculate_engagement_score(user)
        if score >= threshold:
            result.append({"name": user.name, "score": score})
    return result
```

**Single Iteration Pattern:**

1. 🔴 Write test for simplified behavior (if adding new behavior)
2. 🟢 Make minimal changes to pass tests
3. 🔵 Simplify while tests stay green
4. ✅ Run `bin/ci-local` to verify all checks pass

Repeat for each discrete improvement.
