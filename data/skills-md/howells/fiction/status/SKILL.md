---
name: status
description: Quick view of project status without suggestions.
---

Display project status. Simpler than `/fiction:next`—just the facts.

## What This Does

1. Reads project README
2. Counts chapters (drafted vs. outlined)
3. Lists character docs
4. Shows any status markers

## Usage

```
/status                    # Show project status
```

## Output

```
Project: [Name]
Type: [Standalone / Series]

Chapters: [X] drafted, [Y] outlined, [Z] total
Characters: [X] docs
World docs: [X] docs

Status: [From README or inferred]
```

No suggestions, no analysis. Just status.
