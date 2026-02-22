---
name: decision-log
description: "Capture project decisions into a per-file system in a decisions/ directory. Each decision is a markdown file with YAML frontmatter (queryable metadata) and full context (rationale, options, conversation highlights, artifacts). An auto-generated _index.md provides fast scanning. Use when: (1) User invokes /DL or /DecisionLog, (2) User says 'log this decision', 'capture this decision', 'record decision', 'update the decision log', (3) User asks 'what decisions have we made', or (4) User asks for context on a past decision."
license: MIT
metadata:
  author: Blake Graham
  version: "1.0.0"
  argument-hint: "<decision description or empty to scan>"
---

# Decision Log Skill

Maintain a `decisions/` directory where each decision is a standalone markdown file with YAML frontmatter. An `_index.md` manifest is regenerated on every invocation for fast scanning.

## Critical Behavior Rule

**This skill is fully autonomous.** When invoked:
- Do NOT ask the user which decisions to log. Log all unlogged decisions found.
- Do NOT present candidates for confirmation. Just write them.
- Do NOT narrate your phases or telegraph your process. Execute silently, then show results.
- The only output the user should see is the final result: the logged entries themselves.

## Directory Structure

```
decisions/
  _index.md        # Auto-generated manifest — never hand-edit
  DEC-0001.md      # One file per decision
  DEC-0002.md
```

## Instructions

### Step 1 — Assess State

1. Check if `decisions/` directory exists. If not, create it.
2. List existing `DEC-*.md` files to determine the next ID (highest number + 1, zero-padded to 4 digits).
3. Read `_index.md` if it exists to know which decisions are already logged.
4. Scan the current conversation for any decisions not already captured.

### Step 2 — Extract and Classify

For each unlogged decision, determine:

| Field | Values |
|-------|--------|
| domain | `Product`, `Data Engineering`, `Design`, `Architecture`, `Operations`, `Strategy` |
| status | `Active`, `Proposed`, `Superseded`, `Revisited`, `Deprecated` |
| method | `analysis`, `discussion`, `constraint`, `default`, `research`, `prototype`, `stakeholder-input` |

Also capture: decision statement, options considered (with pros/cons), rationale, expected outcome, related DEC-XXXX IDs, 2-5 lowercase tags, and context (summary, conversation highlights, actions performed, artifacts).

### Step 3 — Write Decision Files

Create a file per decision using the schema in [references/templates.md](references/templates.md). File naming: `decisions/DEC-XXXX.md` (zero-padded to 4 digits). Write all files in a single pass.

### Step 4 — Regenerate Index

Read all `DEC-*.md` files in `decisions/`, extract frontmatter, regenerate `decisions/_index.md` using the index template in [references/templates.md](references/templates.md). The index is always rebuilt from disk — it self-heals.

### Step 5 — Show Results

Present a clean summary table:

**Logged 3 decisions:**

| ID | Domain | Decision | Status |
|----|--------|----------|--------|
| DEC-0001 | Architecture | Per-file decision tracking with YAML frontmatter | Active |
| DEC-0002 | Design | Card-based dashboard layout | Active |
| DEC-0003 | Operations | PostgreSQL for user data store | Active |

Updated: `./decisions/`

## Edge Cases

**Explicit single decision** ("log this decision: X"): Extract only that decision. Do not scan for others.

**Supersession**: Create new file with `supersedes: DEC-XXXX`. Edit prior file's frontmatter to `status: Superseded`. Regenerate index.

**Review request** ("what decisions have we made"): Read `_index.md`, present it.

**Context lookup** ("tell me more about DEC-0003"): Read `decisions/DEC-0003.md`, present it.

**Status update** ("mark DEC-0003 as Deprecated"): Edit frontmatter, regenerate index.
