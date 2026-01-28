---
name: pickup
description: Generate a context handoff prompt before clearing the session. Use when the user wants to preserve conversation state before running /clear, or when ending a session and wanting to resume later. Creates a summary prompt capturing task state, progress, decisions, and next steps that can be pasted into a fresh session.
---

# Pickup Prompt Generator

Generate a handoff prompt that allows resuming work in a fresh session.

## Output Format

Output the prompt in a fenced code block so the user can copy it:

```
## Session Pickup

### Goal
[One sentence: what we're trying to accomplish]

### Context
[2-3 sentences: relevant background the next session needs]

### Progress
- [Completed item 1]
- [Completed item 2]
- ...

### Key Decisions
- [Decision]: [Brief rationale]
- ...

### Current State
[What's the immediate situation? What file/task were we in the middle of?]

### Next Steps
1. [Immediate next action]
2. [Following action]
3. ...

### Open Questions
- [Any unresolved questions or blockers]
```

## Guidelines

- **Be specific**: Include file paths, function names, exact values—not vague descriptions
- **Capture rationale**: For decisions, briefly note WHY, not just what
- **Prioritize recency**: Recent context matters more than early conversation
- **Skip the obvious**: Don't include information Claude would know from the codebase
- **Include blockers**: Note anything that was blocking progress or needs investigation
- **Keep it scannable**: Use bullets and short phrases, not paragraphs

## What to Include

| Include | Skip |
|---------|------|
| Current task and subtasks | General pleasantries |
| Files modified or key files referenced | Files just briefly mentioned |
| Decisions made and their rationale | Exploratory dead-ends (unless informative) |
| Blockers or open questions | Resolved issues |
| Next concrete steps | Vague future plans |
| Error messages if debugging | Successful outputs |

## Example Output

```
## Session Pickup

### Goal
Add a `/pickup` skill to generate session handoff prompts before /clear.

### Context
Working in Rob's PKM vault. Skills live in `~/.claude/skills/`. Using the skill-creator skill as a guide for proper skill structure.

### Progress
- Clarified requirements: output to clipboard, focus on task state, name it "pickup"
- Initialized skill at `/Users/rob/.claude/skills/pickup`
- Removed unneeded example directories

### Key Decisions
- No scripts/references/assets needed: pure workflow skill
- Task-state focus over full-context: keeps prompts concise and actionable

### Current State
Writing SKILL.md content. Need to complete the instructions and package the skill.

### Next Steps
1. Finish writing SKILL.md
2. Package with package_skill.py
3. Test by invoking /pickup

### Open Questions
- None currently
```
