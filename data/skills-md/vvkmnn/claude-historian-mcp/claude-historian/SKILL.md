---
name: claude-historian
description: Find past solutions before starting work - search errors you've fixed, files you've changed, similar questions you've asked, tool workflows that succeeded. Reduces web research and prevents redundant work.
---

# Claude Historian

Search your conversation history before starting new work.

## When to Use

**I'm stuck, what have I tried before?**
- Error with no obvious cause → `get_error_solutions`
- Trying different approaches → `find_tool_patterns`
- Working on familiar file → `find_file_context`

**This might be solved already**
- Before WebSearch → `find_similar_queries`
- Starting old project → `list_recent_sessions`
- Need design reasoning → `search_plans`

**I need specific information**
- General history search → `search_conversations`
- Session summary → `extract_compact_summary`

## Best Practice

Check historian BEFORE:
- WebSearch (you may already know this)
- Asking clarifying questions (past context helps)
- Starting implementation (past approaches may apply)
