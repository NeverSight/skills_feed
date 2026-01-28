---
name: reflect
description: End-of-session reflection and memory consolidation
---

# Reflect

Capture session learnings before ending. Counterpart to /hydrate.

## Workflow

1. Review what happened this session:
   - What did we work on?
   - What decisions were made?
   - What did we learn?
   - What's unfinished or needs follow-up?

2. Identify memories worth preserving:
   - **Episodic**: Significant events, breakthroughs, frustrations
   - **Semantic**: New facts learned, definitions clarified
   - **Procedural**: Patterns discovered, how-tos established
   - **Strategic**: Decisions made, approaches chosen, plans formed

3. For each memory, assess:
   - Type (which folder)
   - Importance (0.0-1.0)
   - Concepts (search keywords)

4. Create memory files in `<vault>/Areas/AI/Memory/{Type}/`:
   - Filename: `YYYY-MM-DD - Brief Title.md`
   - Use standard frontmatter format

5. Update living context if significant changes:
   - Major state change -> Update `Areas/AI/Context/Current State.md`
   - New decision -> Update `Areas/AI/Context/Decision Register.md`
   - New connections -> Update `Areas/AI/Context/Connections Map.md`

6. Optionally create session log in `Areas/AI/Collaboration/Sessions/`:
   - Use existing session log template format
   - Link to memories created

7. Summarize what was captured

## Memory File Template

```markdown
---
created: {today}
type: {episodic|semantic|procedural|strategic}
importance: {0.0-1.0}
concepts: [{keywords}]
source: session
---

# {Title}

{Content with context}

## Context

{Why this matters, when it applies}
```

## Reflection Prompts

Ask yourself:
- What would I want to know starting fresh on this topic?
- What mistakes shouldn't be repeated?
- What worked well?
- What context would be lost if not stored?

## What to Capture

**Always capture:**
- Decisions and their rationale
- Discovered patterns or processes
- Project context that took time to establish
- Unfinished work and next steps

**Consider capturing:**
- Interesting technical details
- User preferences observed
- Problems encountered and solutions found

**Skip:**
- Routine operations with no novel learning
- Information already well-documented elsewhere
- Transient details unlikely to matter later

## Example

User: `/reflect`

Response:
"Reflecting on this session...

We worked on: Obsidian-native memory system design

Key memories to store:
1. **Strategic**: Decision to replace Hexis with Obsidian files
2. **Procedural**: Memory file format with frontmatter schema
3. **Semantic**: Commands live in ~/.claude/commands/

Creating 3 memories...
-> Areas/AI/Memory/Strategic/2026-01-04 - Replace Hexis with Obsidian.md
-> Areas/AI/Memory/Procedural/2026-01-04 - Memory File Format.md
-> Areas/AI/Memory/Semantic/2026-01-04 - Command Location.md

Session context preserved. 3 memories stored."

## Parameters

If $ARGUMENTS provided, use as focus area for reflection.
Otherwise, reflect on the full session.

## Response Format

- Brief summary of session work
- List of memories being stored (with types)
- Confirmation of files created
- Any notes about context updates or unfinished items
