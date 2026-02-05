---
name: simplisticate
description: V1.0 - Identifies complexity in code and proposes targeted simplifications with risk assessment. Use when reducing code complexity.
license: MIT
---

# Simplisticate

> *"Simplisticate"* — The art of making complex things simple.

## Core Philosophy

- **Less is more**: Fewer lines, dependencies, abstractions — when appropriate.
- **Clarity over cleverness**: Code should be obvious, not impressive.
- **Pragmatic simplicity**: Simplify where it adds value, not for the sake of it.

## Workflow

### 1. Identify Target

**With user hint**: Focus on specified area, explore related code.
**No hint**: Scan for complexity, rank by impact, present top candidates.

### 2. Complexity Signals

| Signal | Description |
|--------|-------------|
| Deep nesting | >3 levels of indentation |
| Long methods | Functions >30 lines |
| Too many parameters | 4+ parameters |
| Excessive abstractions | Interfaces with single implementations |
| Duplicated logic | Similar code in multiple places |
| Complex conditionals | Nested if/else, long switches |
| Over-engineering | Patterns where simpler solutions exist |
| Dead code | Unused variables, methods, files |
| Tangled dependencies | Circular or convoluted chains |
| Magic values | Hardcoded numbers/strings |

### 3. Propose Simplification

Present findings with:

1. **What**: Description of complexity
2. **Where**: Exact location(s)
3. **Why**: Impact on readability/maintainability
4. **Proposed change**: Specific approach
5. **Risk assessment**: See below

### 4. Risk Assessment (MANDATORY)

| Level | Description | Action |
|-------|-------------|--------|
| 🟢 Low | Cosmetic/isolated, no functional impact | User acknowledgment |
| 🟡 Medium | Touches shared code or slight behavior change | User approval + testing |
| 🔴 High | Structural change, affects multiple components | User approval + comprehensive testing |

**Evaluate**: Test coverage, usage scope, breaking changes, behavioral changes, rollback difficulty.

### 5. Wait for User Decision

**STOP AND WAIT** — Never change code without approval.

Present options:

1. **Approve** — Proceed with simplification
2. **Refine** — Modify approach (request feedback)
3. **Reject** — Skip this simplification
4. **Explore more** — Find other candidates

### 6. Execute (After Approval Only)

- Implement simplification
- Verify no breakage
- Summarize changes
- Offer to find next target

## Simplification Techniques

| Technique | When to Use |
|-----------|-------------|
| Extract method | Long functions with logical sections |
| Inline method | Trivial methods adding no clarity |
| Replace conditional with polymorphism | Complex type-based switching |
| Simplify conditional | Nested/complex boolean logic |
| Remove dead code | Unused variables, methods, imports |
| Consolidate duplicates | Repeated logic patterns |
| Flatten nesting | Early returns, guard clauses |
| Use language features | Modern syntax improving clarity |
| Reduce parameters | Parameter objects, builders |
| Remove unnecessary abstraction | Single-use interfaces |

## Output Format

```text
**Location**: `{file}` (lines {start}-{end})

**Complexity Found**: 
- {bullet points}

**Proposed Simplification**:
1. {numbered steps}

**Risk Assessment**: {🟢|🟡|🔴} {Level}
- Test coverage: {status}
- Usage scope: {description}
- Breaking changes: {yes/no + detail}
- Recommendation: {action}

**Your Options:**
1. Approve
2. Refine
3. Reject
4. Explore more
```

---

*"Perfection is achieved not when there is nothing more to add, but when there is nothing left to take away."* — Antoine de Saint-Exupéry
