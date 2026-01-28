---
name: docs-graph
description: View and query the documentation knowledge graph
version: 1.1.0
---

# /docs-graph - Documentation Graph Viewer

> **Skill Awareness**: See `skills/_registry.md` for all available skills.
> - **Auto-updated**: By Claude Code hook on Write/Edit to plans/
> - **Use before**: `/dev-specs` to see related UCs
> - **Use before**: `/debrief` change request to see impact

View and query relationships between planning documents.

## When to Use

- See overview of all plans and their relationships
- Find related documents before making changes
- Check impact of changes (what links to this?)
- Verify graph is up-to-date

## Usage

```
/docs-graph                    # Show graph summary
/docs-graph auth               # Show nodes related to "auth"
/docs-graph --regenerate       # Force regenerate graph
/docs-graph --check            # Verify all links resolve
```

## How It Works

The graph is automatically updated via Claude Code hooks whenever files in `plans/` are created or modified. This skill provides on-demand viewing and querying.

### Automatic Updates

PostToolUse hook triggers on Write/Edit to plans/:
1. Hook detects file path contains `plans/`
2. Runs `python3 scripts/graph.py --check-path <path>`
3. Graph files updated before next Claude action

### Graph Files

```
plans/
├── docs-graph.json    # Machine-readable graph data
└── docs-graph.md      # Mermaid visualization
```

## Workflow

### Phase 1: Load Graph

1. Check if `plans/docs-graph.json` exists
2. If not, run `python3 scripts/graph.py` to generate
3. Read graph data

### Phase 2: Display or Query

**Summary mode (default):**
- Show node count by type
- Show edge count
- Display mermaid diagram from docs-graph.md
- List any errors

**Query mode (with argument):**
- Filter nodes matching query
- Show incoming links (what references this)
- Show outgoing links (what this references)

**Regenerate mode (--regenerate):**
- Force full rescan of plans/
- Update docs-graph.json and docs-graph.md
- Show diff if changes detected

**Check mode (--check):**
- Verify all wikilinks resolve to existing nodes
- Report broken links
- Suggest fixes

### Phase 3: Output

Display results with:
- Mermaid diagram (if summary)
- Table of matching nodes (if query)
- Broken link report (if check)

## Wikilink Convention

Documents use `[[wikilinks]]` to reference each other:

```markdown
# UC-AUTH-001: Login

> **Feature**: [[feature-auth]]
> **Related**: [[uc-auth-002]], [[uc-auth-003]]
> **Spec**: [[spec-auth-001]]
```

**Link ID format:**
- Use cases: `[[uc-auth-001]]` (lowercase, no slug)
- Features: `[[feature-auth]]`
- Specs: `[[spec-auth-001]]`
- Change requests: `[[cr-001]]`

## Node Types

| Type | Source | Shape (Mermaid) |
|------|--------|-----------------|
| brd | `brd/README.md` | Stadium `[[]]` |
| use-case | `brd/use-cases/**/*.md` | Rectangle `[]` |
| change-request | `brd/changes/*.md` | Hexagon `{{}}` |
| feature | `features/*/README.md` | Pill `([])` |
| spec | `features/*/specs/**/*.md` | Parallelogram `[//]` |
| scout | `**/scout.md` | Cylinder `[()]` |

## Example Output

### Summary

```
Documentation Graph Summary
===========================
Nodes: 12 | Edges: 18

By Type:
  use-case: 5
  feature: 2
  spec: 4
  brd: 1

View full graph: plans/docs-graph.md
```

### Query: `/docs-graph auth`

```
Nodes matching "auth": 4

uc-auth-001 (use-case) - Login
  ← feature-auth, spec-auth-001
  → feature-auth

uc-auth-002 (use-case) - Signup
  ← feature-auth
  → uc-auth-001, feature-auth

feature-auth (feature) - Authentication
  ← uc-auth-001, uc-auth-002, uc-auth-003
  → (none)

spec-auth-001 (spec) - Login Spec
  ← (none)
  → uc-auth-001
```

### Check: `/docs-graph --check`

```
Link Check Results
==================
✓ 16 valid links
✗ 2 broken links

Broken:
  plans/brd/use-cases/auth/UC-AUTH-001-login.md:5
    [[uc-auth-004]] - node not found

  plans/features/auth/specs/UC-AUTH-001/README.md:12
    [[feature-billing]] - node not found

Suggestions:
  - uc-auth-004: Did you mean uc-auth-003?
  - feature-billing: Create plans/features/billing/README.md
```

## Tools Used

| Tool | Purpose |
|------|---------|
| `Bash` | Run graph.py script |
| `Read` | Read docs-graph.json, docs-graph.md |
| `Glob` | Find plan files |

## Integration

| Skill | Relationship |
|-------|--------------|
| `/debrief` | Creates use cases with wikilinks |
| `/dev-specs` | Creates specs linking to use cases |
| `/dev-scout` | Creates scout.md for features |

## Troubleshooting

**Graph not updating:**
- Check hook is in `.claude/settings.local.json`
- Verify `jq` is installed
- Run `/docs-graph --regenerate` to force update

**Broken links:**
- Run `/docs-graph --check` to find issues
- Update wikilinks to match node IDs
- Node IDs are lowercase, no slug (e.g., `uc-auth-001` not `UC-AUTH-001-login`)
