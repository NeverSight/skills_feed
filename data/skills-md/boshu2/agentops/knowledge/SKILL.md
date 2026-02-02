---
name: knowledge
description: 'Query knowledge artifacts across all locations. Triggers: "find learnings", "search patterns", "query knowledge", "what do we know about", "where is the plan".'
---

# Knowledge Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Find and retrieve knowledge from past work.

## Execution Steps

Given `/knowledge <query>`:

### Step 1: Search with ao CLI (if available)

```bash
ao forge search "<query>" --limit 10 2>/dev/null
```

If results found, read the relevant files.

### Step 2: Search .agents/ Directory

```bash
# Search learnings
grep -r "<query>" .agents/learnings/ 2>/dev/null | head -10

# Search patterns
grep -r "<query>" .agents/patterns/ 2>/dev/null | head -10

# Search research
grep -r "<query>" .agents/research/ 2>/dev/null | head -10

# Search retros
grep -r "<query>" .agents/retros/ 2>/dev/null | head -10
```

### Step 3: Search Plans

```bash
# Local plans
grep -r "<query>" .agents/plans/ 2>/dev/null | head -10

# Global plans
grep -r "<query>" ~/.claude/plans/ 2>/dev/null | head -10
```

### Step 4: Use Semantic Search (if MCP available)

```
Tool: mcp__smart-connections-work__lookup
Parameters:
  query: "<query>"
  limit: 10
```

### Step 5: Read Relevant Files

For each match found, use the Read tool to get full content.

### Step 6: Synthesize Results

Combine findings into a coherent response:
- What do we know about this topic?
- What learnings are relevant?
- What patterns apply?
- What past decisions were made?

### Step 7: Report to User

Present the knowledge found:
1. Summary of findings
2. Key learnings (with IDs)
3. Relevant patterns
4. Links to source files
5. Confidence level (how much we know)

## Knowledge Locations

| Type | Location | Format |
|------|----------|--------|
| Learnings | `.agents/learnings/` | Markdown |
| Patterns | `.agents/patterns/` | Markdown |
| Research | `.agents/research/` | Markdown |
| Retros | `.agents/retros/` | Markdown |
| Plans | `.agents/plans/` | Markdown |
| Global Plans | `~/.claude/plans/` | Markdown |

## Key Rules

- **Search multiple locations** - knowledge may be scattered
- **Use ao CLI first** - semantic search is better
- **Fall back to grep** - if ao not available
- **Read full files** - don't just report matches
- **Synthesize** - combine findings into useful answer

## Example Queries

```bash
/knowledge authentication    # Find auth-related learnings
/knowledge "rate limiting"   # Find rate limit patterns
/knowledge kubernetes        # Find K8s knowledge
/knowledge "what do we know about caching"
```
