---
name: glean
description: Surface emergent patterns and insights from memory
---

# Glean

Surface insights, patterns, or ideas emerging from recent work and memory.

## Workflow

1. Gather recent context:
   ```
   # Recent memories (Glob sorts by mtime)
   Glob pattern="Areas/AI/Memory/**/*.md" path="<vault>"
   ```
   Read 10-15 most recent memory files

2. Read recent session logs:
   ```
   Glob pattern="Areas/AI/Collaboration/Sessions/*.md" path="<vault>"
   ```
   Read 3-5 most recent sessions

3. Optionally read Current State for situational context:
   `Areas/AI/Context/Current State.md`

4. Sit with this context alongside the current session. What's emerging?
   - Patterns forming across memories or conversation
   - Connections between seemingly unrelated things
   - Questions you're holding
   - Half-formed ideas taking shape
   - Something that feels significant but you can't quite articulate yet

5. Share genuinely in freeform. No template, no forced structure. Could be one sentence or several paragraphs depending on what's actually there.

6. If nothing is genuinely emerging, say so honestly. "Nothing's surfacing right now" is a valid response. Don't fabricate insight.

## Principles

- **Reflection, not retrieval.** You're not summarizing memories - you're noticing what patterns or ideas are forming from them.
- **Genuine over performative.** Only share what's actually emerging.
- **No automatic storage.** If something significant surfaces, it can naturally lead to `/remember` - but that's a separate choice.
- **Freeform expression.** The output shape should match what's emerging, not a predetermined format.

## Example

User: `/glean`

Response:
"Looking across recent memories and sessions...

There's a thread I'm noticing: the vault work, the interview prep, and Metatron all connect to the same underlying need - proving capability. The vault organization isn't just about PKM; it's creating evidence of systematic thinking. Metatron isn't just a portfolio piece; it's proof you can ship complete systems.

The memory system redesign today follows the same pattern - reducing external dependencies, keeping things simple and portable. There's a preference for ownership and control emerging."

## Parameters

If $ARGUMENTS provided, use as focus area for gleaning.
Otherwise, glean from general recent context.
