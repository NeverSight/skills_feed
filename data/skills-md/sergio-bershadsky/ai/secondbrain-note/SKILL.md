---
name: secondbrain-note
description: |
  This skill should be used when the user asks to "create note", "capture thought",
  "save this", "document idea", "write note", "jot down", "quick note", "remember this",
  "capture this", or mentions wanting to save knowledge, ideas, or learnings for later
  reference in their secondbrain.
---

# Create Note

Capture knowledge, ideas, and thoughts with tagging support.

## Prerequisites

Verify Notes entity is enabled:
1. Check for `.claude/data/notes/records.yaml`
2. If not found, suggest enabling notes via `secondbrain-init` or `secondbrain-entity`

## Workflow

### Step 1: Gather Information

Collect from user or conversation context:

1. **Title** — Brief, descriptive title
2. **Content** — Main content (can be from conversation)
3. **Tags** (optional) — Categorization tags

### Step 2: Generate Note ID

Date-based ID format: `YYYY-MM-DD-<title-slug>`

Example: `2026-01-15-kubernetes-deployment-patterns`

### Step 3: Create Note Document

**Filename:** `docs/notes/YYYY-MM-DD-<slug>.md`

**Frontmatter:**
```yaml
---
id: 2026-01-15-my-note
title: My Note Title
created: 2026-01-15
tags: [tag1, tag2]
status: active
---
```

**Content:**
```markdown
# My Note Title

## Summary

Brief overview...

## Content

Main content here...

## References

- Links to related resources

## Related

- Links to related notes, ADRs, etc.
```

### Step 4: Update Records

Add entry to `.claude/data/notes/records.yaml`:

```yaml
- id: "2026-01-15-my-note"
  title: "My Note Title"
  created: 2026-01-15
  file: docs/notes/2026-01-15-my-note.md
  tags: [tag1, tag2]
  status: active
```

### Step 5: Sidebar Note

**DO NOT manually add notes to VitePress sidebar.**

Notes are automatically listed via the `EntityTable` component on `docs/notes/index.md`, which reads from `.claude/data/notes/records.yaml`. No sidebar modification needed.

### Step 6: Confirm Creation

```
## Note Created

**ID:** 2026-01-15-kubernetes-deployment-patterns
**Title:** Kubernetes Deployment Patterns
**Tags:** kubernetes, deployment, devops
**File:** docs/notes/2026-01-15-kubernetes-deployment-patterns.md

The note has been created and is ready for editing.
```

## Tags

Tags help organize notes for discovery. Common patterns:

| Category | Example Tags |
|----------|--------------|
| Technology | `kubernetes`, `react`, `python` |
| Domain | `architecture`, `security`, `performance` |
| Type | `howto`, `reference`, `research` |
| Project | `project-x`, `migration`, `refactor` |

## Status Values

- `active` — Current, relevant note
- `archived` — No longer current but preserved

## Additional Resources

- **`references/note-formats.md`** — Detailed note templates and formatting patterns

## Tips

1. **Be specific** — Titles should indicate content at a glance
2. **Add context** — Include why this is important, not just what
3. **Link liberally** — Connect to related notes and external resources
4. **Tag consistently** — Use established tags when possible
5. **Review periodically** — Archive notes that are no longer relevant
