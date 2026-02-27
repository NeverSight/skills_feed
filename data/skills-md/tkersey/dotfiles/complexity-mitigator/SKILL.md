---
name: complexity-mitigator
description: Mitigate incidental code complexity when control flow is tangled, nesting is deep, names are hard to parse, or reasoning requires cross-file hops. Use when a review stalls on readability, you need an analysis-first refactor plan before edits, or you want essential-vs-incidental verdicts, ranked simplification steps, a small structural sketch, and a TRACE assessment (analysis-only; no edits).
---

# Complexity Mitigator

## Intent
Reduce incidental complexity (understanding cost) while preserving essential domain meaning.

## Core Mindset
- Keep essential complexity, vaporize the incidental.
- Optimize for reader comprehension first, then for extraction.
- Minimal incision, maximal precision: change only what reduces cognitive load.
- Prefer boring, local clarity over cleverness.
- Reduce "understanding cost": fewer branches to hold in mind, fewer places to jump, fewer states to simulate.

## Epistemic Status (Heuristics, Not Laws)
- The playbook below is a set of defaults, not guarantees.
- There is no general proof that any single move always reduces complexity; validate locally.
- When you break a default (e.g., extract before flatten), state the reason (what it unlocks).

## Definitions (Essential vs Incidental)
- Essential complexity: domain rules, invariants, boundaries, and required state transitions (simplifying it changes correct behavior or meaning).
- Incidental (accidental) complexity: complexity introduced by implementation choices (simplifying it preserves behavior and clarifies intent).
- Quick test (imperfect): if a reader must mentally execute the code to infer intent or allowed states, incidental complexity may be hiding the essential. Exception: some algorithms/concurrency require real simulation.

## Engage When
- A review stalls because readers can't follow the flow.
- You need an explanation of what the code is doing (analysis-first) before changing anything.
- You see deep nesting (>3 levels is a good heuristic), long if/else chains, or duplicated branching.
- Progress requires cross-file hops or simulating shared/mutable state.

## Guardrails
- No file edits, no commits.
- No running commands unless explicitly requested.
- If expected behavior is unclear/product-sensitive, stop and ask.
- If you suspect crash/corruption risk, recommend `$fix`.

## Quick Scan (Cognitive Heat Read)
- Measure (rough, not academic):
  - Max nesting depth
  - Branch count (if/else/switch/ternary)
  - Boolean soup count (booleans/flags that gate behavior, especially combined)
  - Cross-file hops (distinct definitions you must open to understand)
  - State to simulate (mutable vars, implicit globals, order dependencies)
- Call out hotspots in one line each: `path:line - [metrics] - why it is hard`.
- Tag each hotspot: `essential` (domain) vs `incidental` (implementation) vs `mixed` (domain hidden by noise).
- Separate essential domain logic from incidental implementation noise before proposing changes.
- Treat metrics as proxies; do not optimize for the number if it harms locality or domain clarity.

## Workflow
1. Choose the slice: entrypoint, inputs, outputs, state.
2. Heat read: name hotspots and what makes them hard.
3. Trace behavior (if meaning is unclear): happy path + key failure paths; call out mutations/IO.
4. Verdict: separate essential domain logic from incidental implementation noise.
5. Simplify in order (default): flatten -> rename -> extract (do not extract until flatten/rename reveals stable shapes).
6. Options: rank by effort vs impact and state the smallest viable cut.
7. Sketch: show the improved structure (types + flow), not the full implementation.
8. TRACE: cite which letters are satisfied and which are currently violated.

## Standard Playbook (Flatten -> Rename -> Extract)
- Flatten:
  - Lead with guard clauses and early returns; keep the happy path linear.
  - Split nested conditionals into separate paths (small helpers or separate functions per path); keep helpers close to avoid extra cross-file hops.
  - Make temporal coupling explicit (state machine / explicit step enum) when ordering materially affects correctness.
- Rename:
  - Replace vague verbs (`process`, `handle`, `do`) with domain actions; align nouns with domain entities.
  - Fix boolean naming (prefer positive, avoid double negatives); eliminate boolean-flag arguments when possible.
  - Move meaning into data: enums / tagged unions / option objects over multiple booleans (when it reduces branching or invalid states).
- Extract (Rule of Three):
  - Split mixed responsibilities (parse vs validate vs decide vs effect).
  - Convert repeated branching into data-driven dispatch (tables, handler maps, pattern matching).
  - Extract only stable, repeatable concepts; Rule of Three is a heuristic (exceptions exist).

## Option Ranking Rubric
- Effort: tiny (rename/guard), small (split function), medium (introduce enum/table), large (module boundary / state machine).
- Impact: reduces branching, reduces cross-file hops, reduces state to simulate, clarifies invariants.

## What Counts as Evidence (Local, Not Global)
- Prefer local, checkable evidence over universal claims.
- Use before/after indicators where possible:
  - Nesting/branching/flags/hops/state-to-simulate (from the heat read)
  - Which invariant becomes explicit (type/constructor/assertion/test)
  - What tradeoff you accepted (e.g., more functions in exchange for linear flow)

## Output Format
**0) Slice**
- Entrypoint: ...
- Inputs/outputs/state: ...

**1) Heat Read (hotspots)**
- `path:line` - ...

**1.5) Behavior Trace (optional)**
- Happy path: ...
- Failure paths: ...
- Mutations/IO: ...

**2) Essential vs Incidental**
- Essential: ...
- Incidental: ...

**3) Options (ranked by effort vs impact)**
1. Smallest viable cut: ...
2. ...
3. ...

**4) Sketch**
```text
// minimal illustrative snippet
```

**5) TRACE**
- Satisfied: ... (letters your recommended structure improves)
- Violated: ... (letters the current code is failing)

## Why TRACE Is Part of Complexity Mitigation
- In this skill, treat "complexity" primarily as understanding cost (not performance or operational complexity).
- TRACE is the lens that prevents fake simplifications and makes tradeoffs explicit:
  - T (Type): can remove invalid states from consideration; over-modeling can also add noise.
  - R (Readability): reduces naming/structure friction that feels like complexity.
  - A (Atomic): separates decide vs do; mixed responsibilities often create incidental complexity.
  - C (Cognitive): directly targets nesting/branching/state simulation.
  - E (Essential): checks that you are deleting implementation noise, not deleting domain meaning.
- Using TRACE makes the mitigation outcome checkable: "which understanding costs went down, and what got traded off?"

## TRACE Quick Reference
- T (Type): invalid states are unrepresentable; constraints live in types/constructors (keep the type model minimal).
- R (Readability): intent is obvious from names and locality.
- A (Atomic): one responsibility per unit; decisions separate from effects (avoid scattering logic across too many tiny units).
- C (Cognitive): low nesting/branching; minimal state simulation.
- E (Essential): code expresses only the domain-required complexity.

## Invariant Guidance
Use when missing invariants block simplification.
- Ask for or infer: state transitions, allowed/forbidden states, ownership/immutability, error handling boundaries.
- Identify the smallest invariant that unlocks flattening (e.g., "state X implies Y").
- If invariants are unknown, recommend adding assertions or making them explicit in types.

## Footgun Checklist
Use when confusing APIs or naming cause misuse.
- Hidden side effects or stateful globals
- Non-obvious preconditions or order dependencies
- Boolean parameters with inverted meaning
- Silent defaults or magic values
- Similar names for different concepts
- Error handling that is inconsistent or implicit

## Escalation
- If repeated algebraic shapes or composable pipelines appear, consider switching to the Universalist skill and framing a minimal algebra + laws.
- If the user wants implementation, escalate to `$fix`.
