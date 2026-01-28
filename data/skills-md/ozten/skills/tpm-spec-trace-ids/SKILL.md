---
name: tpm-spec-trace-ids
description: Annotate a Spec/PRD with Feature IDs and generate a Coverage Index. Use when user wants to add spec tags to a vision document, create F-nnn identifiers, set up traceability, or initialize a PRD framework for phased development.
---

# PRD Vision Annotator

Annotate a narrative vision document with traceable Feature IDs and generate a Coverage Index.

## Workflow

1. **Add Goals section** (if missing) — Extract or write 3-10 business objectives as G-01, G-02, etc.
2. **Assign Feature IDs** — Add `[F-nnn]` tags to major section headers
3. **Generate Coverage Index** — Create tracking file listing all features

## Step 1: Goals Section

If the vision PRD lacks explicit goals, add them at the top:

```markdown
## Goals

G-01: [Primary business objective]
G-02: [Secondary objective]
G-03: [Quality/compliance objective]
```

Extract goals from executive summary, introduction, or ask the user.

If the document contains goals already, add goal Ids and do not modify those pieces of prose.

## Step 2: Feature ID Assignment

Add Feature IDs to major section headers. Do not modify prose.

**Before:**
```markdown
## 14. RSVP Functionality

### 14.1 Process Flow
```

**After:**
```markdown
## 14. RSVP Functionality [F-014]

### 14.1 Process Flow
```

**Rules:**
- One Feature ID per major section (H2 level typically)
- Subsections inherit parent ID unless substantial enough for their own
- Number sequentially (F-001, F-002...) or match section numbers (§14 → F-014)
- Skip sections explicitly out of scope

## Step 3: Coverage Index

Generate a Coverage Index file using the template in `assets/coverage-index-template.md`.

List every Feature ID with initial status `Planned`.

## Reference

See `references/naming-conventions.md` for ID format details.
