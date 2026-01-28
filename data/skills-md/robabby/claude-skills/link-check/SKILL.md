---
name: link-check
description: Validate wiki-links in an Obsidian vault. Finds broken links that don't resolve to real files, orphaned notes with no incoming links, and link health statistics. Use for vault maintenance and cleanup. Works with or without Obsidian MCP.
---

# Link Check

Validate wiki-links and find orphaned notes.

## What It Checks

| Issue | Description | Impact |
|-------|-------------|--------|
| **Broken links** | `[[Note]]` where Note.md doesn't exist | Navigation fails |
| **Orphaned notes** | Files with no incoming links | Hard to discover |
| **Ambiguous links** | Multiple files match the link | Unpredictable resolution |

## Workflow

1. Scan for all wiki-links
   - Find `[[...]]` patterns in all .md files
   - Extract link targets

2. Validate each link
   - Check if target file exists
   - Check for ambiguous matches
   - Track which files link to what

3. Find orphaned notes
   - Files that no other file links to
   - Exclude expected orphans (CLAUDE.md, templates, etc.)

4. Generate report
   - Broken links with source files
   - Orphaned notes list
   - Link statistics

## Search Patterns

```bash
# Find all wiki-links
Grep pattern="\[\[[^\]]+\]\]" path="{vault}" glob="*.md"

# Find links to specific note
Grep pattern="\[\[Note Name\]\]" path="{vault}" glob="*.md"
```

## Output Format

```
## Link Check Report

### Summary
- Total links: {count}
- Broken links: {count}
- Orphaned notes: {count}

### Broken Links
| Source File | Broken Link |
|-------------|-------------|
| {file} | [[{target}]] |

### Orphaned Notes
Files with no incoming links:
- {file}
- {file}

### Recommendations
- {actionable suggestion}
```

## Parameters

- `$ARGUMENTS` (optional):
  - No args: Full vault scan
  - `{folder}`: Scan specific folder only
  - `--orphans-only`: Only check for orphaned notes
  - `--broken-only`: Only check for broken links

## Example

User: `/link-check`

Response:
"## Link Check Report

### Summary
- Total links: 1,247
- Broken links: 8
- Orphaned notes: 23

### Broken Links
| Source File | Broken Link |
|-------------|-------------|
| `Projects/Active/Website.md` | [[Design System]] |
| `Areas/Career/Resume.md` | [[Portfolio]] |
| `Resources/Books/Atomic Habits.md` | [[Book Notes Template]] |

### Orphaned Notes
Files with no incoming links:
- `Inbox/Quick thought 2024-03-15.md`
- `Resources/Snippets/bash-aliases.md`
- `Archive/Old Project/notes.md`
(20 more in Archive/)

### Recommendations
1. Create `Design System.md` or update link in Website.md
2. Review Inbox/ items for processing or deletion
3. Orphans in Archive/ may be intentional - consider excluding from future checks"
