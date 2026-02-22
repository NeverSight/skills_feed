---
name: property-test-generator
description: >
  Design and generate property-based tests (PBT) for changed files in the
  current git branch. Extracts specifications, designs properties (invariants,
  round-trip, idempotence, metamorphic, monotonicity, reference model), builds
  generator strategies, implements tests, and self-scores against a rubric
  (24/30+ required). Supports fast-check (TS/JS), hypothesis (Python), and
  proptest (Rust).
  Use when: (1) "write property tests for my changes", (2) "add PBT",
  (3) "property-based test", (4) after implementing pure functions, validators,
  parsers, or formatters to verify invariants.
---

# Property-Based Test Generator

Design and generate property-based tests for changed files, with self-scoring
to ensure quality (24/30+ on the evaluation rubric).

## Constraints

- Black-box only — never depend on internal implementation details.
- No trivial properties (type-check-only, no-exception-only are forbidden).
- Minimize `assume`/`filter` — express constraints in generators instead.
- Always ensure seed + minimal counterexample reproducibility.

## Workflow

1. **Detect changed files** — identify PBT candidates from git diff
2. **Extract specifications** — read each file, document inputs/outputs/constraints
3. **Design properties** — minimum 5 per function, following the property type hierarchy
4. **Build generators** — express input domains with edge cases and good shrinking
5. **Implement tests** — write test files in the project's framework
6. **Self-score** — evaluate against rubric, improve if below 24/30
7. **Report** — present results to user

## Step 1 — Detect Changed Files

Identify PBT candidates from the current branch diff:

```bash
git diff --name-only --diff-filter=ACMR $(git merge-base main HEAD) HEAD
```

Filter to source files (`.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.rs`), excluding
test files, config, styles, and assets.

**Good PBT candidates** (prioritize these):
- Pure functions (no side effects, deterministic)
- Validators / type guards (`is*`, `validate*`)
- Parsers / serializers (encode/decode, parse/stringify)
- Formatters (data → string transformations)
- Reducers / state transitions
- Sorting / filtering / transformation utilities

**Poor PBT candidates** (skip these):
- React components (use integration tests instead)
- Side-effectful functions (API calls, file I/O)
- Simple getters/setters with no logic

## Step 2 — Extract Specifications

For each candidate function, document:

1. **Inputs** — types, ranges, constraints
2. **Outputs** — types, expected relationships to inputs
3. **State** — mutable state involved, if any
4. **Requirements** — business rules as bullet points
5. **Preconditions** — what must be true about inputs

## Step 3 — Design Properties (min 5)

Design properties in this priority order:

| Type | Description | When to use |
|------|-------------|-------------|
| Invariant | Output always satisfies a condition | Length preservation, range bounds, type guarantees |
| Round-trip | `decode(encode(x)) === x` | Parsers, serializers, codecs |
| Idempotence | `f(f(x)) === f(x)` | Normalizers, formatters, canonicalizers |
| Metamorphic | Relationship between `f(x)` and `f(transform(x))` | Sort, filter, math operations |
| Monotonicity | `x ≤ y → f(x) ≤ f(y)` | Scoring, ranking, pricing |
| Reference model | `optimized(x) === naive(x)` | Optimized reimplementations |

Each property MUST include:
- Natural-language description
- Corresponding requirement from Step 2
- One buggy implementation example that this property would catch

## Step 4 — Build Generators

Determine the project language and select the library:
- **TypeScript/JavaScript** → fast-check — see [references/fast-check.md](references/fast-check.md)
- **Python** → hypothesis — see [references/hypothesis.md](references/hypothesis.md)
- **Rust** → proptest — see [references/proptest.md](references/proptest.md)

Generator design rules:
- Express constraints via generator composition, not `filter`/`assume`.
- Target filter rejection rate < 10%.
- Explicitly include edge cases: empty, zero, boundary, max-size, duplicates, skewed distributions.
- Prefer base Arbitrary/Strategy combinations for natural shrinking.
- Set explicit size limits to control generation cost.

## Step 5 — Implement Tests

Write test files following project conventions:
- Read existing `*.property.test.*` files for style reference.
- Read test config and setup files.
- File naming: `*.property.test.ts` (TS/JS), `test_*_property.py` (Python), or `#[cfg(test)] mod tests` / `tests/` (Rust). Follow project convention.

Each test must include:
1. Descriptive property name
2. Generator definition
3. Test body (arrange/act/assert)
4. Seed output on failure
5. Reproduction instructions (as comment)

## Step 6 — Self-Score

After implementation, evaluate against the rubric in
[references/evaluation.md](references/evaluation.md).

Score 15 criteria (A1-A5, B1-B6, C1-C4) at 0-2 points each.

- **24+ points**: proceed to report.
- **< 24 points**: identify weak criteria, improve properties/generators/diagnostics, re-score. Repeat up to 2 times.

## Step 7 — Report

Output in this order:

1. **Requirements summary** — extracted specifications
2. **Property list** — natural language + requirement mapping + buggy impl example
3. **Generator strategies** — with edge case rationale
4. **Test implementation** — actual test code (not pseudocode)
5. **Reproduction instructions** — how to re-run with seed
6. **Score table + improvement log** — final self-assessment
