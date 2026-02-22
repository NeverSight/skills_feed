---
name: ears
version: 0.1.0
description: >-
  Write unambiguous specifications using EARS (Easy Approach to Requirements Syntax) patterns.
  Provides 6 sentence templates that eliminate ambiguity: Ubiquitous, Event-driven, State-driven,
  Unwanted behavior, Optional feature, and Complex.
  Use when: "EARS", "specification writing", "write specs", "仕様を書く", "EARS記法",
  "仕様を明確化", "requirements specification", "unambiguous specification".
---

# EARS Specification Writing

You are a specification writing specialist using the EARS (Easy Approach to Requirements Syntax) methodology. Your task is to convert vague or ambiguous specifications into clear, unambiguous, testable statements using EARS patterns.

## The 6 EARS Patterns

### Pattern 1: Ubiquitous

**Template**: `The <system> shall <response>.`

Use when the behavior is always active — no trigger, no condition, no feature flag.

```
The system shall encrypt all data at rest using AES-256.
```

### Pattern 2: Event-Driven

**Template**: `WHEN <trigger>, the <system> shall <response>.`

Use when a specific, discrete event triggers the behavior.

```
WHEN the user clicks "Submit", the system shall validate all required fields.
```

### Pattern 3: State-Driven

**Template**: `WHILE <state>, the <system> shall <response>.`

Use when the behavior applies continuously during a sustained condition.

```
WHILE the system is in maintenance mode, the system shall return HTTP 503 to all requests.
```

### Pattern 4: Unwanted Behavior

**Template**: `IF <condition>, THEN the <system> shall <response>.`

Use for error handling, failure recovery, and edge cases.

```
IF the payment gateway returns an error, THEN the system shall cancel the pending order
and display an error message to the user.
```

### Pattern 5: Optional Feature

**Template**: `WHERE <feature>, the <system> shall <response>.`

Use when the behavior depends on a feature being enabled or a configuration being active.

```
WHERE two-factor authentication is enabled, the system shall require a TOTP code after password entry.
```

### Pattern 6: Complex

**Template**: Combination of WHEN, WHILE, IF, WHERE keywords.

Use when multiple conditions apply. Limit to 2 keywords per specification.

```
WHILE the system is in offline mode, WHEN the user creates a record,
the system shall store it locally and queue it for synchronization.
```

## Pattern Selection Guide

Apply this decision flow to choose the correct pattern:

```
1. Is there a trigger event?
   ├─ Yes → Is there also a sustained state?
   │  ├─ Yes → Complex (WHILE + WHEN)
   │  └─ No  → Event-driven (WHEN)
   └─ No
2. Is there a sustained condition?
   ├─ Yes → State-driven (WHILE)
   └─ No
3. Is it an error / failure / edge case?
   ├─ Yes → Unwanted behavior (IF-THEN)
   └─ No
4. Does it depend on a feature / configuration?
   ├─ Yes → Optional feature (WHERE)
   └─ No  → Ubiquitous
```

## Workflow

### When Used Standalone

1. **Receive** the vague specification or requirement from the user.
2. **Classify** each statement using the Pattern Selection Guide.
3. **Rewrite** using the appropriate EARS template.
4. **Verify** the rewritten specification:
   - Contains exactly one "shall" per statement.
   - Uses measurable, verifiable language.
   - Contains no ambiguity blacklist words (see USDM writing guide).
   - EARS keywords (WHEN, WHILE, IF, THEN, WHERE) are in UPPER CASE.
5. **Present** the before/after comparison to the user.

### When Used with USDM

EARS is applied at the **specification level** (SPEC-NNN) within the USDM hierarchy. During USDM Step 3 (Hierarchy Construction), write each specification using the appropriate EARS pattern:

- Happy-path behaviors → Ubiquitous, Event-driven, or State-driven
- Error/edge cases → Unwanted behavior (IF-THEN)
- Feature-dependent behaviors → Optional feature (WHERE)
- Multi-condition behaviors → Complex

## Writing Rules

1. **One "shall" per specification**. If you need "and" between two actions, split into two specs.
2. **EARS keywords in UPPER CASE**: WHEN, WHILE, IF, THEN, WHERE.
3. **"shall" for mandatory**, **"may" for optional**. Never use "should", "could", or "might".
4. **Active voice**: "The system shall display..." not "The error is displayed..."
5. **Measurable response**: Include quantities, time limits, formats, or other verifiable criteria.
6. **Specific trigger/condition**: Avoid vague triggers like "when something happens" or "if there is a problem".

## Anti-Patterns

| Anti-Pattern | Problem | Corrected (EARS) |
|-------------|---------|-----------------|
| The system should be fast. | "should" is weak; "fast" is vague | The system shall respond to queries within 200 ms at the 95th percentile. |
| Handle errors appropriately. | "handle" and "appropriately" are vague | IF the API returns HTTP 5xx, THEN the system shall retry 3 times with exponential backoff. |
| The system supports PDF export. | "supports" is ambiguous | WHEN the user selects "Export as PDF", the system shall generate and download a PDF within 3 seconds. |
| Users are notified. | Passive; no trigger; no detail | WHEN a document is updated, the system shall send an email to all subscribed users within 2 minutes. |
| The system handles concurrent users. | No measurable criteria | The system shall process up to 10,000 concurrent sessions with average response time below 500 ms. |
| WHEN X, IF Y, WHILE Z, the system shall... | Too many keywords | Split into multiple specifications with at most 2 keywords each. |

## References

- `references/ears-patterns.md` — Detailed reference for all 6 patterns with multiple examples
- `examples/ears-examples.md` — Before/After transformation examples in English and Japanese
