---
name: shareful-create
description: Guides creation of high-quality SHARE.md files for shareful.ai. Covers repo setup, frontmatter, required sections, and validation. Use when the user wants to create a share, document a coding solution, contribute to shareful.ai, or run npx shareful-ai create.
---

# Shareful Create

Create SHARE.md files that follow shareful.ai quality standards from first draft through validation.

## Reference Files

| File | Read When |
|------|-----------|
| `references/frontmatter-guide.md` | Writing or reviewing frontmatter fields |
| `references/writing-sections.md` | Writing the four body sections |
| `references/quality-examples.md` | Calibrating quality or reviewing a draft share |
| `references/validation-checklist.md` | Final validation pass before finishing |

## Creation Workflow

Copy this checklist to track progress:

```text
- [ ] Step 1: Ensure shares repo context exists
- [ ] Step 2: Classify the problem and choose solution type
- [ ] Step 3: Draft frontmatter
- [ ] Step 4: Draft the required body sections
- [ ] Step 5: Create SHARE.md
- [ ] Step 6: Validate with checklist
```

### Step 1: Ensure Shares Repo Context Exists

Check if a shares repo is configured:

1. Read `~/.shareful/config.json` for the `sharesRepo` path
2. If set, verify the path contains a `shares/` directory
3. If not set, run `npx shareful-ai init [name]` to create and configure a repo

The `init` command creates the directory structure and saves the repo path to config.

### Step 2: Classify Problem and Choose Solution Type

Determine what was solved and choose the correct `solution_type`:

| Type | Use when | Title convention |
|------|----------|-----------------|
| `fix` | Directly resolves a bug or error | "Fix ..." |
| `workaround` | Temporarily bypasses a known issue | "Workaround for ..." |
| `pattern` | Reusable coding pattern or architecture | "Use ...", "Implement ..." |
| `reference` | Lookup guide or cheat sheet | "Guide to ...", "Reference for ..." |
| `config` | Configuration change resolving a setup issue | "Configure ..." |

Most shares are `fix` type. Use `pattern` only when the solution generalizes beyond a single error.

### Step 3: Draft Frontmatter

Read [references/frontmatter-guide.md](references/frontmatter-guide.md) for the complete schema and examples.

Required fields:

```yaml
---
title: "Human-readable title"          # max 128 chars
slug: kebab-case-identifier             # max 64 chars, a-z 0-9 hyphens only
tags: [tag1, tag2, tag3]                # 1-10 tags, max 32 chars each, lowercase
problem: "One-sentence problem summary" # max 256 chars
solution_type: fix                      # fix | workaround | pattern | reference | config
created: 2026-02-08                     # YYYY-MM-DD
environment:                            # optional but recommended
  language: typescript
  framework: nextjs
  version: "15+"
---
```

Key rules:
- Slug is auto-generated from title: lowercase, strip special chars, spaces to hyphens, max 64 chars
- Slug MUST match the parent directory name
- Problem field should include the error message or symptom for searchability
- Tags should cover: primary technology, problem domain, and 1-2 descriptors

### Step 4: Draft the Required Body Sections

Read [references/writing-sections.md](references/writing-sections.md) for templates and guidance.

Optionally read [references/quality-examples.md](references/quality-examples.md) for annotated good and bad examples.

All four sections are required:

1. **## Problem** -- Show the broken state with real code and error messages
2. **## Solution** -- Provide working code with multiple options when applicable
3. **## Why It Works** -- Explain the underlying mechanism, not just "what" but "why"
4. **## Context** -- List environment requirements, gotchas, and related tools

The body must be under 300 lines total. Aim for 60-150 lines.

### Step 5: Create SHARE.md

**Option A: Use the CLI**

```bash
npx shareful-ai create --title "Fix Prisma N+1 queries" --tags "prisma,database,performance" --type fix --problem "Prisma makes hundreds of queries when loading related data"
```

Then edit the generated `shares/<slug>/SHARE.md` to replace template content with real content.

**Option B: Write directly**

Create `shares/<slug>/SHARE.md` with the complete frontmatter and body. Ensure the `shares/` directory exists (run `npx shareful-ai init` if not).

### Step 6: Validate with Checklist

Read [references/validation-checklist.md](references/validation-checklist.md) and run all checks.

Expected output after this step:

- A complete `shares/<slug>/SHARE.md` file
- Frontmatter and section structure validated
- No placeholder content

## Anti-patterns

- Writing a vague problem field ("Something is broken") instead of including the actual error message
- Using Why It Works to repeat the solution instead of explaining the underlying mechanism
- Forgetting language labels on code blocks
- Making the title too generic ("Fix TypeScript error") instead of specific ("Fix TypeScript module augmentation for third-party types")
- Slug not matching the directory name
- Exceeding 300 lines in the body
- Using `pattern` type for what is actually a `fix` (pattern is for reusable architecture, not bug fixes)

## Related Skills

- `shareful-search` for discovering existing shares on shareful.ai
