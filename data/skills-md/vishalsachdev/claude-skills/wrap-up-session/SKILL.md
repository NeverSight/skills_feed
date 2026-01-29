---
name: wrap-up-session
description: Use when user says "let's wrap up", "close shop", "done for today", or wants to end a session. Handles session wrap-up including git operations, documentation updates, roadmap updates, and preparing for next session. Works across all repo types.
---

# Close Shop

Wrap up a work session cleanly. This skill launches the wrap-up-session agent for comprehensive session wrap-up, adapting behavior based on repo type.

## Execution

The wrap-up process has two parts:

### Part 1: Session Wrap-up (Agent)

Launch the `wrap-up-session` agent using the Task tool:

```
Use Task tool with subagent_type: "wrap-up-session" and model: "opus"
```

**Important:** Always specify `model: "opus"` — currently only Opus 4.5 is deployed in Azure AI Foundry.

The agent will handle the wrap-up process autonomously.

### Part 2: Sync to Remote Machine

After the agent completes, push changes to the other machine:

```bash
unison folders -batch -terse
```

- `-batch` — non-interactive, skips conflicts (won't hang waiting for input)
- `-terse` — minimal output

This ensures all commits, roadmap updates, and logs are synced before you switch machines.

## Behavior by Repo Type

Before launching the agent, check CLAUDE.md for `type:` declaration to guide the agent.

### Code Repos (default)

The wrap-up-session agent will:
- Run linting and fix issues automatically
- Execute tests and report failures
- Review modified files and stage changes
- Generate commit messages based on work done
- **Update roadmap sections in CLAUDE.md** (see below)
- Create TODO items for next session
- Push if requested

### Research/Writing Repos

When `type: research` is detected, the agent should:
- **Skip** linting and testing (no code)
- Commit document changes with descriptive messages
- Update word count or progress tracking if present
- Note current section/chapter for next session
- **Update roadmap sections in CLAUDE.md** (see below)
- Optionally export to other formats (PDF, etc.)

### Mixed Repos

Apply relevant aspects from both code and research workflows.

## Roadmap Updates

The wrap-up-session agent MUST update the roadmap sections in CLAUDE.md:

### 1. Update `## Session Log`

Add a new entry with today's date:

```markdown
### YYYY-MM-DD
- Completed: [list of completed items]
- Next: [what to focus on next session]
```

### 2. Update `## Roadmap`

- Check off completed items: change `- [ ]` to `- [x]`
- Infer completions from:
  - Git commits made during session
  - User's stated accomplishments
  - Files modified

### 3. Update `## Current Focus`

- Move to the next incomplete roadmap item
- Or ask user: "What should be the focus for next session?"

### 4. Prompt User (if unclear)

If completions are ambiguous, ask:
- "What did you complete this session?"
- "What should be the focus for next session?"

## Pre-Launch Checklist

Before launching the agent, briefly check:
1. Is there uncommitted work? (`git status`)
2. What type of repo is this? (Check CLAUDE.md)
3. Any specific wrap-up-session instructions in CLAUDE.md?
4. Does CLAUDE.md have roadmap sections to update?

## Example Invocation

```
I'll wrap up this session using the wrap-up-session agent.

Based on CLAUDE.md, this is a [code/research] repo.
Roadmap sections [found/not found] in CLAUDE.md.

[Launch Task tool with wrap-up-session agent]
```

## Notes

- This skill provides symmetric UX with `/start-session`
- Heavy lifting is delegated to the wrap-up-session agent
- Repo-specific behavior is guided by CLAUDE.md
- If no CLAUDE.md exists, default to code repo behavior
- If no roadmap sections exist, skip roadmap updates (but suggest adding them)
