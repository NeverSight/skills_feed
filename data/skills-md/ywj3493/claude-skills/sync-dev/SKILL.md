---
name: sync-dev
description: Audits docs/specifications/, docs/issue/, and docs/policy/ for English documents that are missing a Korean translation in docs/dev/, or where the Korean version appears out of date compared to the English source, then creates or updates those translations. Use this to keep docs/dev/ in sync. Triggered by "sync docs", "번역 동기화", "update translations", "sync dev", or "mirror docs".
---

# sync-dev

Keeps the `docs/dev/` Korean mirror synchronized with the English source documents.

## When to Use

- User says "sync docs", "update translations", "sync dev", "번역 동기화", "mirror docs"
- After a batch of documentation updates where Korean mirrors may be missing
- Periodically to audit translation completeness across the project

## Directories in Scope

| English source | Korean mirror |
|---|---|
| `docs/specifications/` | `docs/dev/specifications/` |
| `docs/issue/` | `docs/dev/issue/` |
| `docs/policy/` | `docs/dev/policy/` |

`docs/reference/` is **excluded** — user-managed, no mirroring needed.

## Step-by-Step Instructions

### Step 1: Audit — Find Missing Translations

List all English source files in the three mirrored directories:

```bash
find docs/specifications docs/issue docs/policy \
  -name "*.md" ! -name "*.ko.md" ! -name ".gitkeep" 2>/dev/null | sort
```

For each file found (e.g., `docs/issue/issue003.md`), check whether the
corresponding mirror exists (e.g., `docs/dev/issue/issue003.ko.md`).

Build a **Missing** list of files with no Korean mirror.

### Step 2: Audit — Find Stale Translations

For files where a Korean mirror exists, compare modification times using git:

```bash
git log --follow -1 --format="%ai" -- docs/issue/issue003.md
git log --follow -1 --format="%ai" -- docs/dev/issue/issue003.ko.md
```

If the English source has a more recent commit than the Korean mirror, add it
to a **Stale** list.

### Step 3: Report and Confirm

Tell the user:

> Sync audit complete:
>
> **Missing translations** (<N> files):
> - docs/issue/issue004.md
> - docs/specifications/architecture.md
>
> **Potentially stale** (<N> files):
> - docs/policy/policy.md (English updated 2025-11-01, Korean updated 2025-10-15)
>
> Shall I create/update all of them?

Wait for confirmation before writing any files.

### Step 4: Create or Update Translations

For each file in the Missing or Stale lists:

1. Read the English source file completely
2. Translate all prose content into Korean
3. Write the `.ko.md` file to the corresponding `docs/dev/` path

**Naming rule**: Replace the directory prefix and append `.ko`:
- `docs/issue/issue003.md` → `docs/dev/issue/issue003.ko.md`
- `docs/specifications/requirements.md` → `docs/dev/specifications/requirements.ko.md`
- `docs/policy/commit-message-rule.md` → `docs/dev/policy/commit-message-rule.ko.md`

### Step 5: Report Results

List every file created or updated with their paths.

## Translation Rules

**Translate to Korean:**
- All prose paragraphs and sentences
- Section headings
- List item descriptions
- Table cell text

**Keep in English:**
- Code blocks (``` ... ```) — never translate the content inside
- File paths (`docs/issue/issue001.md`)
- Function names, variable names, class names
- Branch names and command-line examples
- Technical acronyms: API, URL, HTTP, JSON, Git, etc.
- Checkbox markers: `- [ ]`, `- [x]`

**For technical acronyms on first use**, optionally add a brief Korean
explanation in parentheses, then use the acronym alone thereafter.

**Preserve markdown structure exactly:**
- Same heading levels (`#`, `##`, `###`)
- Same list and checkbox formatting
- Same bold/italic markers
- Same horizontal rules and table structure
