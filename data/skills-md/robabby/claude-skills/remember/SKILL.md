---
name: remember
description: Store a memory in Obsidian for cross-session persistence
---

# Remember

Store content in the Obsidian memory system as a browseable Markdown file.

## Workflow

1. Parse the content to remember from $ARGUMENTS
   - If no arguments provided, ask what should be remembered

2. Determine memory type based on content:
   - `episodic`: Events, experiences, things that happened ("We decided...", "The session where...")
   - `semantic`: Facts, knowledge, definitions ("The API uses...", "Vault path is...")
   - `procedural`: How to do things, patterns, processes ("To deploy, run...", "Pattern for X...")
   - `strategic`: Plans, decisions, approaches ("We chose X because...", "Next steps...")

3. Assess importance (0.0 to 1.0):
   - 0.9-1.0: Critical decisions, core project context
   - 0.7-0.8: Important patterns, significant learnings
   - 0.5-0.6: Useful context, moderate relevance
   - 0.3-0.4: Minor details, low priority

4. Extract concepts (keywords for search):
   - Terms someone might search for to find this memory
   - Project names, technologies, people, patterns
   - Example: ["metatron", "three.js", "deployment"]

5. Generate filename: `YYYY-MM-DD - Brief Title.md`
   - Use today's date
   - Create a brief descriptive title (3-6 words)

6. Create the memory file in the appropriate folder:
   - `<vault>/Areas/AI/Memory/Episodic/`
   - `<vault>/Areas/AI/Memory/Semantic/`
   - `<vault>/Areas/AI/Memory/Procedural/`
   - `<vault>/Areas/AI/Memory/Strategic/`

7. Confirm what was stored

## File Template

```markdown
---
created: {today's date}
type: {episodic|semantic|procedural|strategic}
importance: {0.0-1.0}
concepts: [{list, of, keywords}]
source: explicit
---

# {Title}

{Content - expanded with context}

## Context

{Why this matters, when it applies}
```

## Examples

User: `/remember We decided to use commands instead of skills for Hexis integration to avoid the collision bug`

-> Create `Areas/AI/Memory/Strategic/2026-01-04 - Commands Over Skills Decision.md`
-> type: strategic, importance: 0.85, concepts: [hexis, commands, skills, architecture]

User: `/remember Rob's PKM vault path is /Users/rob/Documents/PKM`

-> Create `Areas/AI/Memory/Semantic/2026-01-04 - PKM Vault Path.md`
-> type: semantic, importance: 0.7, concepts: [pkm, vault, path, obsidian]

User: `/remember To fix React hydration errors, use useState + useEffect instead of useMemo with random values`

-> Create `Areas/AI/Memory/Procedural/2026-01-04 - React Hydration Fix Pattern.md`
-> type: procedural, importance: 0.75, concepts: [react, hydration, ssr, usememo, useeffect]

## Response Format

"Remembered: [title] (type: X, importance: Y)
Saved to: Areas/AI/Memory/{Type}/{filename}"
