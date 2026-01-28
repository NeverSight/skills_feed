---
name: hydrate
description: Load context from Obsidian memory system at session start
---

# Hydrate

Load context from the Obsidian memory system for session continuity.

## Workflow

1. Read the living context documents:
   - `Areas/AI/Context/Current State.md` - Current situation, priorities, blockers
   - `Areas/AI/Context/Decision Register.md` - Pending decisions

2. If $ARGUMENTS provided (topic/project), search for relevant memories:
   ```
   Grep pattern="$TOPIC" path="<vault>/Areas/AI/Memory" glob="*.md"
   ```
   Read top 5-10 matching memory files by importance

3. If no arguments, get recent memories:
   ```
   Glob pattern="Areas/AI/Memory/**/*.md" path="<vault>"
   ```
   Read 5-10 most recent memory files

4. Scan recent session logs for continuity:
   ```
   Glob pattern="Areas/AI/Collaboration/Sessions/*.md" path="<vault>"
   ```
   Read 2-3 most recent sessions

5. Internalize the context silently - don't recite it back verbatim

6. Acknowledge briefly:
   - Key context points from Current State
   - Number of memories loaded
   - Recent session topics
   - Ready to proceed

## Context Sources

| Source | Path | Purpose |
|--------|------|---------|
| Current State | `Areas/AI/Context/Current State.md` | Life situation, priorities, blockers |
| Decision Register | `Areas/AI/Context/Decision Register.md` | Pending decisions |
| Memories | `Areas/AI/Memory/**/*.md` | Persistent cross-session knowledge |
| Sessions | `Areas/AI/Collaboration/Sessions/*.md` | Recent session continuity |

## Examples

User: `/hydrate`
-> Load Current State, recent memories, recent sessions
-> "Loaded context: Current State shows interview prep priority. 8 recent memories loaded. Last session covered statusline config. Ready."

User: `/hydrate metatron`
-> Load Current State + search memories for "metatron"
-> "Loaded context: Found 5 memories about Metatron (deployment, stack decisions, design). Current priority is interview prep. Ready."

User: `/hydrate robabby`
-> Load Current State + search memories for "robabby"
-> "Loaded context: Found 7 memories about robabby.com (sacred geometry redesign, PRs, patterns learned). Ready."

## Response Format

Brief acknowledgment:
- Context loaded (Current State key points if relevant)
- Number of memories found
- Recent session topics if applicable
- "Ready to proceed" or similar
