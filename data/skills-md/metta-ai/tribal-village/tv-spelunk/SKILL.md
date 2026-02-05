---
name: tv-spelunk
description: "Search codebase for a pattern and open top hits."
---

# TV Spelunk

## Workflow
- Run `rg -n "<pattern>" src` (include `docs` when needed).
- Open top 2-3 hits with `sed -n '1,240p' <file>`.
- Summarize findings.
