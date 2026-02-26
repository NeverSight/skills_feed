---
name: slicing-elephant-carpaccio
description: "Breaks features into ultra-thin vertical slices using Elephant Carpaccio methodology. Use when planning new features, breaking down epics, slicing work across layers, or when a task spans multiple components. Produces an ordered backlog of thin slices, each independently working, testable, and demoable. Handles single-repo, monorepo, and multi-repo architectures."
allowed-tools:
  - AskUserQuestion
---

# Slicing Elephant Carpaccio

Break features into the thinnest possible vertical slices — each one cutting across all necessary layers (UI, logic, data) to produce an independently working, testable, demoable increment. The output is an ordered slice backlog, not implementation.

## Quick Start

Given a feature description, produce an ordered list of 10-20 thin vertical slices:

```markdown
## Slice Backlog: [Feature Name]

1. **Walking skeleton** — [thinnest end-to-end path]. Value: proves architecture connects.
2. **[Next slice]** — [description]. Value: [what stakeholder can now see/do].
3. ...
```

## When This Skill Applies

- Planning a new feature that spans multiple layers or components
- Breaking down an epic or large story into deliverable increments
- User asks to "slice", "thin-slice", or "carpaccio" a feature
- Work spans frontend, backend, and data layers
- Multi-repo coordination is needed for a feature
- A story feels too large but isn't ready for task decomposition yet

## Workflow

```
Detect Architecture  -->  Understand Scope  -->  Produce Slice Backlog
Repo structure            Components/layers       Ordered thin slices
```

---

## Step 1: Detect the Architecture

Before slicing, determine the repository structure.

1. **Examine the project layout.** Look at the current working directory, any monorepo workspace configurations (package.json workspaces, nx.json, turbo.json, Cargo.toml workspace, go.work), and any sibling directories the user references.

2. **Classify the architecture:**

   | Type | Description | Slice atomicity |
   |------|-------------|-----------------|
   | **Single repo** | All layers in one repository | Slices are atomic |
   | **Monorepo** | Multiple packages/apps in one repo | Slices can touch multiple packages but are atomic |
   | **Multi-repo** | Separate repos with independent CI/deploy | Slices are coordinated across repos |

3. **If multi-repo, identify:**
   - Which repo you are currently operating in
   - Location of other repo(s), if accessible
   - Contract surface between repos (REST API, GraphQL schema, RPC definitions, shared types, OpenAPI specs)
   - Which repo deploys first in practice (typically backend)
   - Whether a shared types/contract package exists

4. **State findings** to the user and confirm before slicing.

---

## Step 2: Understand the Full Feature Scope

Read all relevant files, specs, and existing code. Identify every component, layer, and integration point involved. Ask clarifying questions if the scope is ambiguous.

Use the `codebase-navigator` agent to find relevant files and entry points when the feature touches existing code.

---

## Step 3: Produce the Slice Backlog

Create a numbered, ordered list of 10-20 slices. Each slice gets a one-line description and a note on what value it delivers.

For multi-repo slices, indicate which repo(s) each slice touches.

### Slice Validity Rules

Every slice MUST pass ALL of these tests:

- **Vertical** — Cuts through all necessary layers, not just backend or just frontend in isolation.
- **Working** — After this slice, the system is in a testable, demoable state. Tests pass.
- **Distinct** — A stakeholder can see something changed compared to the previous slice.
- **Valuable** — Delivers more user value or reduces more risk than the last slice.
- **Small** — Implementable in a single focused coding pass (or a small coordinated pair in multi-repo setups).

### Ordering Principles

- **Slice 1 is always a walking skeleton** — the thinnest possible end-to-end path proving the architecture connects. Hard-code values if needed. Its value is pure risk reduction.
- Core happy-path functionality comes next, one thin layer at a time.
- Prefer simpler implementations that deliver value faster (e.g., accept user input directly before building lookup tables).
- Legal/compliance requirements before nice-to-haves.
- All core paths before any single path is polished.
- Validation, error handling, and edge cases LAST.
- UI polish and optimization LAST.

### Slicing Heuristics

When a slice feels too large, split it further using these patterns:

| Heuristic | Strategy |
|-----------|----------|
| **By workflow path** | One user flow end-to-end before the next |
| **By data variation** | Start with one data type or category, add others as separate slices |
| **By business rule** | Simplest rule first, add complexity in later slices |
| **By interface** | One platform, device, or UI variant first |
| **Simple before complex** | Happy path across all paths before edge cases on any single path |
| **Hardcode then generalize** | Hardcode a value in slice N, replace with dynamic logic in slice N+1 |

### Multi-Repo Slicing

When slicing across repository boundaries:

- **Contract-first** — Each slice that crosses a repo boundary defines the API contract (endpoint shape, types, schema fragment) as its first sub-step, before either side is built.
- **Thinnest crossing** — Minimize the API surface introduced per slice. One endpoint, one field, one query — not a batch.
- **Upstream before downstream** — Note the deployment order. The side that provides the contract is built first.
- **Mock strategy** — When the upstream won't be deployed before the downstream is built, note that a temporary mock of the agreed contract shape should be used and replaced within the same slice.

### Blocked Repo Planning

If you only have access to one repo in a multi-repo setup, still plan full vertical slices. For each slice, note what the inaccessible repo needs to do as a companion task.

---

## Anti-Patterns

If you catch yourself producing any of these, re-slice:

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| **Horizontal slices** | Backend-only or frontend-only chunks deliver no user-visible value until a later slice integrates them |
| **Build all endpoints then all UI** | The most common multi-repo anti-pattern — horizontal slicing in disguise |
| **Gold-plating early slices** | Adding validation/error handling/polish to slice 2 when core paths in slices 8-12 don't exist yet |
| **Speculative infrastructure** | Abstractions or frameworks beyond what the current slice requires |
| **Task decomposition as slices** | "Set up the database" and "write the migration" are tasks within a slice, not slices themselves — each slice must have user-visible value |

---

## Output Format

Present the backlog as a numbered list:

```markdown
## Slice Backlog: [Feature Name]

Architecture: [single-repo | monorepo | multi-repo]

1. **Walking skeleton** — [thinnest end-to-end path].
   Value: Proves architecture connects end-to-end.
   [Repos: backend, frontend]  <!-- only for multi-repo -->

2. **[Slice name]** — [one-line description of what changes].
   Value: [what a stakeholder can now see or do].

3. ...
```

After presenting the backlog, ask the user to confirm or adjust before any implementation begins.

Use **AskUserQuestion**:
- Header: "Slice backlog"
- Question: "Does this slice ordering look right?"
- Options: "Looks good" | "Adjust ordering" | "Slices too thick — split further" | "Slices too thin — combine some"

---

## Integration with Other Skills

### Upstream — Defining what to slice
- `writing-prds` — Start here if you need a PRD first; features from the use case compendium are ideal slicing inputs
- `writing-agile-stories` — If you already have a BDD story that's too large, slice it here before writing sub-stories

### Downstream — Detailing each slice
- `writing-agile-stories` — Flesh out each slice into a BDD story with acceptance criteria
- `breaking-down-stories` — Decompose slices or stories into implementation tasks
- `implementation-planning` — Create a detailed implementation plan for a slice
