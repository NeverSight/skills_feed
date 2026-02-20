---
name: self-improve
description: Use when a session produced reusable insights, when the user says "learn from this", "remember this", or "improve yourself", or after completing a complex task where patterns were discovered
---

# Self-Improve

## Overview

Session learning loop that captures reusable knowledge and routes it to the right place: project memory, global CLAUDE.md, or a new skill. Builds on skills-management methodology for skill creation (see writing-skills reference).

## Process

### 1. Identify Learnings
After a productive session, review what was learned:
- Patterns that worked well
- Mistakes that were caught and corrected
- Techniques that could be reused
- Debugging insights
- Tool usage patterns
- Project-specific conventions discovered

### 2. Classify Each Learning

Read [references/classification-routing.md](references/classification-routing.md) for the full routing table (priority 1-5) and draft format per destination. Key rule: the instinct to put things in ~/CLAUDE.md is usually wrong — route to existing skills or project CLAUDE.md first.

### 3. Confirm with User
Present all proposed changes grouped by destination. For each:
- What was learned (1 sentence)
- Where it goes and why
- Exact content to add/modify

**Never auto-apply changes.** Always get explicit approval.

### 4. Apply Approved Changes
Write changes to the approved destinations. For new skills, note that full TDD testing (per skills-management writing-skills reference) should happen in a dedicated session.

## Common Mistakes
- **Defaulting to ~/CLAUDE.md** — most learnings belong in a more focused location (existing skill, project CLAUDE.md, or memory). ~/CLAUDE.md is the last resort, not the default.
- Auto-applying changes without user confirmation
- Saving session-specific context as permanent knowledge
- Creating skills for one-off solutions
- Duplicating what's already in CLAUDE.md or existing skills
