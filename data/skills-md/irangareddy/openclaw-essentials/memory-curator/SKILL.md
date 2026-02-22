---
name: memory-curator
description: Manage agent memory through daily logs, session preservation, and knowledge extraction. Use when (1) logging work at end of day, (2) preserving context before /new or /reset, (3) extracting patterns from daily logs to MEMORY.md, (4) searching past decisions and learnings, (5) organizing knowledge for long-term retention. Essential for continuous improvement and avoiding repeated mistakes.
---

# Memory Curator

Systematic memory management for agents through daily logging, session preservation, and knowledge extraction.

## Quick Start

### Log Today's Work

```bash
# Append to today's log
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --entry "Implemented user authentication with JWT" \
  --category "Key Activities"

# Show today's log
python scripts/daily_log.py --workspace ~/.openclaw/workspace --show
```

### Search Memory

```bash
# Search all memory files
python scripts/search_memory.py \
  --workspace ~/.openclaw/workspace \
  --query "GraphQL"

# Search recent logs only (last 7 days)
python scripts/search_memory.py \
  --workspace ~/.openclaw/workspace \
  --query "authentication" \
  --days 7

# Show recent logs
python scripts/search_memory.py \
  --workspace ~/.openclaw/workspace \
  --recent 5
```

### Extract Session Summary

```bash
# Generate summary from current session
python scripts/extract_session.py \
  --session ~/.openclaw/agents/<agent-id>/sessions/<session-id>.jsonl \
  --output session-summary.md
```

## Core Workflows

### End of Day: Log Activities

**When:** Before ending work session or switching contexts

**Steps:**

1. **Review what was accomplished:**
   - Features implemented
   - Bugs fixed
   - Decisions made
   - Learnings discovered

2. **Append to daily log:**
   ```bash
   python scripts/daily_log.py \
     --workspace ~/.openclaw/workspace \
     --entry "Fixed race condition in payment processing - added mutex lock"
   ```

3. **Add structured entries for important work:**
   ```markdown
   ## Key Activities

   - [14:30] Implemented user profile dashboard with GraphQL
   - [16:00] Fixed infinite re-render in UserContext - memoized provider value

   ## Decisions Made

   - Chose Apollo Client over React Query - better caching + type generation
   - Decided to use JWT in httpOnly cookies instead of localStorage

   ## Learnings

   - Apollo requires `__typename` field for cache normalization
   - React.memo doesn't prevent re-renders from context changes
   ```

**See:** [patterns.md](references/patterns.md) for what to log in different scenarios

### Before Context Switch: Preserve Session

**When:** Before running `/new`, `/reset`, or ending conversation

**Steps:**

1. **Extract session summary:**
   ```bash
   # Get current session ID from system prompt or openclaw status
   python scripts/extract_session.py \
     --session ~/.openclaw/agents/<agent-id>/sessions/<session-id>.jsonl \
     --output ~/session-summary.md
   ```

2. **Review summary and edit Key Learnings section**

3. **Save to daily log:**
   ```bash
   # Append key points to today's log
   cat ~/session-summary.md >> ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
   ```

4. **Extract critical context to MEMORY.md if needed:**
   - Non-obvious solutions
   - Important decisions
   - Patterns worth remembering

### Weekly Review: Extract Knowledge

**When:** End of week (Friday/Sunday) or monthly

**Steps:**

1. **Search for patterns in recent logs:**
   ```bash
   python scripts/search_memory.py \
     --workspace ~/.openclaw/workspace \
     --recent 7
   ```

2. **Look for extraction signals:**
   - Repeated issues (3+ occurrences)
   - High-cost learnings (>1 hour to solve)
   - Non-obvious solutions
   - Successful patterns worth reusing

3. **Extract to MEMORY.md:**
   - Add new sections or update existing ones
   - Use problem-solution format
   - Include code examples
   - Add context for when to use

4. **Clean up MEMORY.md:**
   - Remove outdated information
   - Consolidate duplicate entries
   - Update code examples
   - Improve organization if needed

**See:** [extraction.md](references/extraction.md) for detailed extraction patterns

### Daily: Quick Logging

**For rapid context capture during work:**

```bash
# Quick note
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --entry "TIL: DataLoader batches requests into single query"

# Decision
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --entry "Using Zustand for client state - simpler than Redux" \
  --category "Decisions Made"

# Problem solved
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --entry "CORS + cookies: Enable credentials on client + server, Allow-Origin can't be *"
```

## Memory Structure

### Daily Logs (`memory/YYYY-MM-DD.md`)

**Purpose:** Chronological activity tracking

**Content:**
- What was done (timestamped)
- Decisions made
- Problems solved
- Learnings discovered

**Retention:** Keep recent logs accessible, optionally archive logs >90 days

**When to use:**
- "What did I do on [date]?"
- "When did I implement X?"
- Session history
- Activity tracking

### MEMORY.md

**Purpose:** Curated long-term knowledge

**Content:**
- Patterns and best practices
- Common solutions
- Mistakes to avoid
- Useful references

**Organization:** Topic-based, not chronological

**When to use:**
- "How do I solve X?"
- "What's the pattern for Y?"
- Best practices
- Reusable solutions

**See:** [organization.md](references/organization.md) for structure patterns

## Memory Logging Patterns

### What to Log

**Always log:**
- Key implementation decisions (why approach X over Y)
- Non-obvious solutions
- Root causes of bugs
- Architecture decisions with rationale
- Patterns discovered
- Mistakes and how they were fixed

**Don't log:**
- Every file changed (git has this)
- Obvious implementation details
- Routine commits
- Project-specific hacks

**See:** [patterns.md](references/patterns.md) for comprehensive logging guidance

### When to Log

**During work:**
- Quick notes with `daily_log.py --entry`
- Capture decisions as made
- Log problems when solved

**End of day:**
- Review what was accomplished
- Structure important entries
- Add context for tomorrow

**End of week:**
- Extract patterns to MEMORY.md
- Consolidate learnings
- Clean up outdated info

## Knowledge Extraction

### Extraction Criteria

**Extract to MEMORY.md when:**
- Pattern appears 3+ times
- Solution took >1 hour to find
- Solution is non-obvious
- Will save significant time in future
- Applies across multiple projects
- Mistake was costly to debug

**Don't extract:**
- One-off fixes
- Project-specific hacks
- Obvious solutions
- Rapidly changing APIs

### Extraction Format

**Problem-Solution Structure:**

```markdown
## [Technology/Domain]

### [Problem Title]

**Problem:** [Clear description]
**Cause:** [Root cause]
**Solution:** [How to fix]

**Code:**
```js
// Example implementation
```

**Prevention:** [How to avoid]
**Context:** [When this applies]
```

**See:** [extraction.md](references/extraction.md) for detailed extraction workflow

## Scripts Reference

### daily_log.py

Create or append to today's daily log.

```bash
# Append entry
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --entry "Your log entry" \
  [--category "Section Name"]

# Create from template
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --template

# Show today's log
python scripts/daily_log.py \
  --workspace ~/.openclaw/workspace \
  --show
```

### extract_session.py

Extract summary from session JSONL.

```bash
python scripts/extract_session.py \
  --session ~/.openclaw/agents/<id>/sessions/<session>.jsonl \
  [--output summary.md]
```

Outputs:
- User requests summary
- Tools used
- Files touched
- Template for key learnings

### search_memory.py

Search across all memory files.

```bash
# Search with query
python scripts/search_memory.py \
  --workspace ~/.openclaw/workspace \
  --query "search term" \
  [--days 30]

# Show recent logs
python scripts/search_memory.py \
  --workspace ~/.openclaw/workspace \
  --recent 5
```

## Best Practices

### Daily Discipline

1. **Start of day:** Review yesterday's log, plan today
2. **During work:** Quick notes for decisions and learnings
3. **End of day:** Structure important entries, add context
4. **End of week:** Extract patterns, clean up MEMORY.md

### Context Preservation

**Before `/new` or `/reset`:**
1. Extract session summary
2. Add to daily log
3. Preserve critical context in MEMORY.md

**After major work:**
1. Document what was accomplished
2. Note key learnings
3. Record next steps

### Knowledge Organization

1. **Topic-based structure** - Group by domain, not date
2. **Problem-first titles** - Lead with the problem being solved
3. **Searchable language** - Use specific, findable terms
4. **Flat hierarchy** - Maximum 2 levels deep
5. **Code examples** - Include working examples

**See:** [organization.md](references/organization.md) for detailed structure guidance

## Troubleshooting

### Can't find past decision

1. **Search daily logs first:**
   ```bash
   python scripts/search_memory.py --workspace ~/.openclaw/workspace --query "decision keyword"
   ```

2. **Search MEMORY.md:**
   ```bash
   grep -i "keyword" ~/.openclaw/workspace/MEMORY.md
   ```

3. **Search session logs:**
   ```bash
   rg "keyword" ~/.openclaw/agents/<id>/sessions/*.jsonl
   ```

### Memory files getting too large

1. **Archive old daily logs** (>90 days):
   ```bash
   mkdir -p memory/archive/2025-Q1
   mv memory/2025-01-*.md memory/archive/2025-Q1/
   ```

2. **Split MEMORY.md by domain** if >1000 lines:
   ```
   memory/domains/
   ├── react.md
   ├── graphql.md
   └── database.md
   ```

3. **Link from main MEMORY.md:**
   ```markdown
   ## Domain Knowledge
   - [React Patterns](memory/domains/react.md)
   - [GraphQL Patterns](memory/domains/graphql.md)
   ```

### Not sure what to log

**See:** [patterns.md](references/patterns.md) for comprehensive logging patterns

**Quick rule:** If you spent >15 minutes on it or learned something non-obvious, log it.

## Templates

### Daily Log Template

Located at: `assets/templates/daily-log.md`

Structure:
- Key Activities
- Decisions Made
- Learnings
- Challenges & Solutions
- Context for Tomorrow
- References

### MEMORY.md Template

Located at: `assets/templates/MEMORY-template.md`

Structure:
- Patterns & Best Practices
- Common Solutions
- Learnings
- Mistakes to Avoid
- Useful References

## Tips

1. **Be consistent** - Log every day, extract every week
2. **Be concise** - Future you needs facts, not stories
3. **Be specific** - "Apollo cache normalization" > "cache issue"
4. **Use code** - Examples > explanations
5. **Search first** - Before asking, search your memory
6. **Extract ruthlessly** - If it repeats 3x, extract it
7. **Clean regularly** - Remove outdated info monthly
8. **Version control** - Git commit MEMORY.md changes

## Integration with OpenClaw

### Auto-logging with Hooks

Create a hook to auto-log major events:

```js
// ~/.openclaw/hooks/memory-logger/index.js
export default {
  name: 'memory-logger',
  async onToolCall({ tool, agent }) {
    if (tool === 'write' || tool === 'edit') {
      // Log file modifications
      await exec(`python scripts/daily_log.py --workspace ${agent.workspace} --entry "Modified ${tool.input.file_path}"`)
    }
  }
}
```

### Session Preservation

Add to `AGENTS.md`:

```markdown
## Before /new or /reset

Always preserve context:
1. Extract session summary
2. Add to daily log
3. Save critical decisions to MEMORY.md
```

### Weekly Review Cron

```bash
openclaw cron add \
  --name "weekly-memory-review" \
  --at "Sunday 18:00" \
  --system-event "Time for weekly memory review and knowledge extraction"
```
