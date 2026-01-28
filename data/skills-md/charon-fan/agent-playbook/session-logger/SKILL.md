---
name: session-logger
description: Saves conversation history to session log files. Use when user says "保存对话", "保存对话信息", "记录会话", "save session", or "save conversation". Automatically creates timestamped session log in sessions/ directory.
allowed-tools: Read, Write, Edit, Bash
---

# Session Logger

A skill for automatically saving conversation history to persistent session log files.

## When This Skill Activates

This skill activates when you:
- Say "保存对话信息" or "保存对话"
- Say "记录会话内容" or "保存session"
- Say "save session" or "save conversation"
- Ask to save the current conversation

## Session File Location

All sessions are saved to: `sessions/YYYY-MM-DD-{topic}.md`

## What Gets Logged

For each session, log:

1. **Metadata**
   - Date and duration
   - Context/working directory
   - Main topic

2. **Summary**
   - What was accomplished
   - Key decisions made
   - Files created/modified

3. **Actions Taken**
   - Checklist of completed tasks
   - Pending follow-ups

4. **Technical Notes**
   - Important code snippets
   - Commands used
   - Solutions found

5. **Open Questions**
   - Issues to revisit
   - Follow-up tasks

## Session Template

```markdown
# Session: {Topic}

**Date**: {YYYY-MM-DD}
**Duration**: {approximate}
**Context**: {project/directory}

## Summary

{What was accomplished in this session}

## Key Decisions

1. {Decision 1}
2. {Decision 2}

## Actions Taken

- [x] {Completed action 1}
- [x] {Completed action 2}
- [ ] {Pending action 3}

## Technical Notes

{Important technical details}

## Open Questions / Follow-ups

- {Question 1}
- {Question 2}

## Related Files

- `{file-path}` - {what changed}
```

## How to Use

### Option 1: Automatic Logging

Simply say:
```
"保存对话信息"
```

The skill will:
1. Review the conversation history
2. Extract key information
3. Create/update the session file

### Option 2: With Topic

Specify the session topic:
```
"保存对话，主题是 skill-router 创建"
```

### Option 3: Manual Prompt

If auto-extraction misses something, provide details:
```
"保存对话，重点是：1) 创建了 skill-router，2) 修复了 front matter"
```

## File Naming

| Input | Filename |
|-------|----------|
| "保存对话" | `YYYY-MM-DD-session.md` |
| "保存对话，主题是 prd" | `YYYY-MM-DD-prd.md` |
| "保存今天的讨论" | `YYYY-MM-DD-discussion.md` |

## Session Log Structure

```
sessions/
├── README.md                      # This file
├── 2025-01-11-skill-router.md     # Session about skill-router
├── 2025-01-11-prd-planner.md      # Session about PRD planner
└── 2025-01-12-refactoring.md      # Session about refactoring
```

## Privacy Note

Session logs are stored in `sessions/` which is in `.gitignore`.
- Logs are NOT committed to git
- Logs contain your actual conversation
- Safe to include sensitive information

## Quick Reference

| You say | Skill does |
|---------|------------|
| "保存对话信息" | Creates session log with today's date |
| "保存今天的对话" | Creates session log |
| "保存session" | Creates session log |
| "记录会话" | Creates session log |

## Best Practices

1. **Save at key milestones**: After completing a feature, fixing a bug, etc.
2. **Be specific with topics**: Helps when searching later
3. **Include code snippets**: Save important solutions
4. **Track decisions**: Why did you choose X over Y?
5. **List pending items**: What to do next time

## Rich Content Extraction (for Self-Improving Agent)

When triggered by other skills via hooks, session-logger extracts structured data for learning:

### Skill Context Capture

When a skill completes, capture:

```markdown
## Skill Execution Context

**Skill**: {skill-name}
**Trigger**: {user-invoked | hook-triggered | auto-triggered}
**Status**: {completed | error | partial}
**Duration**: {approximate time}

### Input Context
- User request: {original request}
- Files involved: {list of files}
- Codebase patterns detected: {patterns}

### Output Summary
- Actions taken: {list}
- Files modified: {list with changes}
- Decisions made: {key decisions}

### Learning Signals
- What worked well: {successes}
- What could improve: {areas for improvement}
- Patterns discovered: {new patterns}
- Errors encountered: {errors and resolutions}
```

### Error Context Capture

When a skill encounters errors:

```markdown
## Error Context

**Error Type**: {type}
**Error Message**: {message}
**Stack Trace**: {if available}

### Resolution Attempted
- Approach: {what was tried}
- Result: {success/failure}
- Root cause: {if identified}

### Prevention Notes
- How to avoid: {prevention strategy}
- Related patterns: {similar issues}
```

### Pattern Extraction

Extract reusable patterns for the self-improving-agent:

```markdown
## Extracted Patterns

### Code Patterns
- Pattern name: {name}
- Context: {when to use}
- Example: {code snippet}

### Workflow Patterns
- Trigger: {what initiates}
- Steps: {sequence}
- Outcome: {expected result}

### Anti-Patterns
- Pattern: {what to avoid}
- Why: {reason}
- Alternative: {better approach}
```

### Structured Data Format

For machine-readable extraction, use YAML front matter in session logs:

```yaml
---
session_type: skill_execution
skill_name: code-reviewer
trigger_source: hook
status: completed
files_modified:
  - path: src/utils.ts
    changes: refactored error handling
patterns_learned:
  - name: error-boundary-pattern
    category: error-handling
    confidence: high
errors_encountered: []
learning_signals:
  successes:
    - "Identified code smell in utils.ts"
  improvements:
    - "Could have suggested more specific refactoring"
---
```

### Integration with Self-Improving Agent

When triggered by `self-improving-agent`:

1. **Extract episodic memory**: Capture the full context of what happened
2. **Identify semantic patterns**: Tag reusable knowledge
3. **Update working memory**: Note immediate follow-ups needed
4. **Signal completion**: Write trigger file if skill chaining is needed

### Auto-Trigger Behavior

When invoked via hooks with `mode: auto`:
- Silently create/update session log
- Extract structured data without user interaction
- Append to existing session if same day/topic
- Create new session if context differs significantly
