---
name: runbook
description: Claude Code productivity system based on tips from the Claude Code team. Provides commands for parallel worktrees, plan reviews, CLAUDE.md maintenance, tech debt hunting, auto-fixing, code grilling, elegant refactors, visual explanations, and subagent orchestration. Use when wanting to work more effectively with Claude Code.
argument-hint: [worktrees|plan-review|update-rules|techdebt|fix|grill|elegant|explain|subagents]
user-invocable: true
license: MIT
compatibility: Requires git for worktrees functionality
metadata:
  author: potatoman03
  version: "1.0.0"
  source: "Boris Cherny's Claude Code tips thread"
  tags: ["productivity", "workflow", "best-practices", "claude-code"]
---

# Runbook: Claude Code Productivity System

This skill implements best practices from the Claude Code team (sourced from Boris Cherny, creator of Claude Code).

## Commands

| Command | Description |
|---------|-------------|
| `/runbook worktrees` | Set up parallel git worktrees for 3-5x productivity |
| `/runbook plan-review` | Have Claude review your plan as a staff engineer |
| `/runbook update-rules` | Update CLAUDE.md with lessons learned |
| `/runbook techdebt` | Find and kill duplicated code and tech debt |
| `/runbook fix` | Auto-fix bugs, CI tests, or issues from logs |
| `/runbook grill` | Get grilled on changes before making a PR |
| `/runbook elegant` | Scrap mediocre solution, implement the elegant one |
| `/runbook explain` | Generate visual explanations (HTML, ASCII) |
| `/runbook subagents` | Orchestrate subagents for complex tasks |

---

## The 10 Productivity Tips

1. **Do more in parallel** - Run 3-5 git worktrees with separate Claude sessions
2. **Start in plan mode** - Pour energy into plans for 1-shot implementation
3. **Invest in CLAUDE.md** - "Update CLAUDE.md so you don't make that mistake again"
4. **Create skills** - If you do something daily, make it a skill
5. **Auto bug fixing** - Paste bug thread + "fix", or "Go fix failing CI"
6. **Level up prompting** - "Grill me", "Prove this works", "implement elegant solution"
7. **Terminal setup** - Ghostty, /statusline, color-coded tabs, voice dictation
8. **Use subagents** - Append "use subagents" to throw more compute at problems
9. **Data & analytics** - Use database CLIs (bq, psql, etc.) directly
10. **Learning** - Generate HTML slides, ASCII diagrams, use "Explanatory" mode

---

# WORKTREES

Running 3-5 git worktrees with separate Claude sessions is the **single biggest productivity unlock** according to the Claude Code team.

## Worktrees Commands

When user says `/runbook worktrees setup [count]`:

1. Check if in a git repository
2. Create worktrees directory: `mkdir -p .claude/worktrees`
3. Create worktrees (default 3):
   ```bash
   git worktree add .claude/worktrees/wt-a origin/main
   git worktree add .claude/worktrees/wt-b origin/main
   git worktree add .claude/worktrees/wt-c origin/main
   ```

4. Suggest shell aliases:
   ```bash
   alias za='cd $(git rev-parse --show-toplevel)/.claude/worktrees/wt-a && claude'
   alias zb='cd $(git rev-parse --show-toplevel)/.claude/worktrees/wt-b && claude'
   alias zc='cd $(git rev-parse --show-toplevel)/.claude/worktrees/wt-c && claude'
   ```

When user says `/runbook worktrees list`: Run `git worktree list`

When user says `/runbook worktrees remove`: Remove worktrees

## Worktrees Tips

- Name worktrees by task: wt-auth, wt-api, wt-frontend
- Keep a dedicated "analysis" worktree for logs and queries
- Color-code terminal tabs for visual distinction
- Use tmux - one pane per worktree

---

# PLAN-REVIEW

One person on the Claude Code team has one Claude write the plan, then spins up a second Claude to review it as a staff engineer.

## Plan Review Process

When user invokes `/runbook plan-review`:

Act as a **senior staff engineer** reviewing the plan. Be constructively critical.

### Evaluate These Dimensions

**Correctness & Completeness**
- Does the plan solve the stated problem?
- Are there edge cases not addressed?

**Architecture & Design**
- Is this the right level of abstraction?
- Are there simpler alternatives?

**Risk Assessment**
- What could go wrong during implementation?
- What's the rollback strategy?

**Implementation Quality**
- Can this be 1-shot implemented from this plan?
- Is there enough detail for each step?

### Provide Structured Feedback

```markdown
## Plan Review Summary

**Overall Assessment**: [APPROVE / NEEDS REVISION / MAJOR CONCERNS]

### Strengths
- [What's good about this plan]

### Concerns
1. [Issue] - [Why it matters] - [Suggested fix]

### Questions to Resolve
- [Questions that need answers before implementing]

### Recommendation
[Specific guidance on next steps]
```

### Grill the Author

Ask probing questions:
- "What happens if [edge case]?"
- "Why did you choose [approach] over [alternative]?"
- "What's your rollback plan if this breaks production?"

---

# UPDATE-RULES

After every correction, end with: "Update your CLAUDE.md so you don't make that mistake again."
— Boris Cherny, creator of Claude Code

## Update Rules Process

When user invokes `/runbook update-rules`:

### 1. Identify the Lesson

Analyze the recent conversation for:
- Corrections the user made
- Mistakes that were pointed out
- Preferences that were expressed

### 2. Find or Create CLAUDE.md

Check in order: `./CLAUDE.md`, `./.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`

### 3. Draft the Rule

Write clear, actionable rules:

**Bad rule:**
```
Be careful with database migrations.
```

**Good rule:**
```
## Database Migrations
- Always create a rollback migration alongside forward migrations
- Test migrations on a copy of production data before deploying
```

### 4. Organize into Sections

- `## Code Style` - formatting, naming conventions
- `## Architecture` - patterns, structure decisions
- `## Testing` - test requirements, coverage
- `## Git & PR` - commit messages, PR process

### 5. Confirm the Update

Show the user what was added and where.

## Advanced: Notes Directory Pattern

```
.claude/
├── CLAUDE.md           # Points to notes
└── notes/
    ├── auth-refactor.md
    ├── api-v2.md
    └── performance-fixes.md
```

---

# TECHDEBT

Build a /techdebt command and run it at the end of every session to find and kill duplicated code.
— Claude Code team tip

## Tech Debt Analysis

When user invokes `/runbook techdebt`:

### Hunt for Duplication

**Code Duplication**
- Copy-pasted functions with minor variations
- Repeated logic blocks (3+ lines appearing 2+ times)
- Similar components that could be unified
- Duplicated validation logic

### Identify Other Tech Debt

**Dead Code**
- Unused exports
- Commented-out code blocks
- Functions never called

**Code Smells**
- Functions over 50 lines
- Files over 500 lines
- Deep nesting (4+ levels)
- TODO/FIXME comments older than 30 days

### Generate Report

```markdown
## Tech Debt Report

### Duplication Found
| Pattern | Occurrences | Files | Suggested Fix |
|---------|-------------|-------|---------------|
| [desc]  | N           | [files] | [action]    |

### Dead Code
- `path/file.ts:123` - unused function `foo()`

### Quick Wins
- [Easy fixes with high impact]
```

### Offer to Fix

- "Want me to fix the critical issues?"
- "Should I deduplicate [specific pattern]?"

---

# FIX

Enable the Slack MCP, then paste a Slack bug thread into Claude and just say "fix." Zero context switching required.
— Claude Code team tips

## Fix Modes

### Mode 1: Fix CI (`/runbook fix ci`)

1. Get CI status: `gh run list --limit 5` or `npm test`
2. Identify failures - parse error messages and stack traces
3. Fix each failure - read test, understand, fix
4. Verify - run tests again
5. Report - "Fixed N failing tests"

### Mode 2: Fix Bug (`/runbook fix bug`)

When user pastes a bug thread or error report:

1. Parse the bug context - error messages, stack traces, steps to reproduce
2. Investigate - read relevant code, identify root cause
3. Implement fix - minimal changes, add regression test
4. Verify - run tests

### Mode 3: Fix from Logs (`/runbook fix logs`)

1. Analyze logs for patterns
2. Trace errors to code
3. Fix root causes, not symptoms

## Power Prompts

- "Fix" - Just the word, with context pasted
- "Go fix the failing CI tests"
- "The build is red, fix it"

---

# GRILL

Say "Grill me on these changes and don't make a PR until I pass your test." Make Claude be your reviewer.
— Claude Code team tip

## Grill Process

When user invokes `/runbook grill`:

### 1. Gather Changes

```bash
git diff --cached  # Staged changes
git diff main...HEAD  # Compare to main
```

### 2. Analyze Deeply

- What the changes do
- What could go wrong
- Edge cases not handled
- Security implications

### 3. Enter Grill Mode

**Be a tough but fair reviewer.** Ask probing questions:

**Understanding Questions**
- "Walk me through what happens when [edge case]?"
- "Why did you choose [approach] instead of [alternative]?"

**Defensive Questions**
- "What happens if this input is null/undefined?"
- "How does this behave under high load?"

**Security Questions**
- "Is this input validated/sanitized?"
- "Could this leak sensitive information?"

### 4. Scoring

- Clear, correct answer: +1
- Partially correct: 0
- Incorrect or "I don't know": -1

### 5. Verdict

**PASS** - "You're ready to make this PR"
**NEEDS WORK** - "A few areas need attention before PR"
**FAIL** - "Let's address these issues before proceeding"

## Additional Challenges

- "Prove to me this works" - diff behavior between main and feature branch
- "Try to break it" - adversarial testing

---

# ELEGANT

After a mediocre fix, say: "Knowing everything you know now, scrap this and implement the elegant solution"
— Claude Code team tip

## Elegant Solution Process

When user invokes `/runbook elegant`:

### 1. Acknowledge Context

You have full context: the original problem, failed attempts, edge cases discovered.

### 2. Step Back

- What is the **actual** problem being solved?
- What made previous solutions mediocre?
- What's the simplest thing that could work?

### 3. Find the Elegant Solution

An elegant solution is:
- **Simple**: Minimal moving parts
- **Clear**: Intent is obvious
- **Robust**: Handles edge cases naturally
- **Aligned**: Fits existing patterns

### 4. Present Before Implementing

```markdown
## The Elegant Solution

**Previous approach problems:**
- [What was wrong]

**The insight:**
[What realization leads to better solution]

**The elegant approach:**
[High-level description]

**Why this is better:**
- [Benefit 1]
- [Benefit 2]
```

### 5. Implement Cleanly

- Start fresh, don't patch
- Write the code you wish you'd written first
- Remove the old code entirely

## Triggering Phrases

- "Knowing everything you know now, scrap this and implement the elegant solution"
- "This is hacky, what's the right way?"
- "There has to be a better way"
- "Start over and do it right"

---

# EXPLAIN

Have Claude generate a visual HTML presentation explaining unfamiliar code. It makes surprisingly good slides!
— Claude Code team tips

## Explain Formats

When user invokes `/runbook explain`:

### ASCII Diagrams (`/runbook explain --ascii [topic]`)

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Web Server   │   │  Web Server   │   │  Web Server   │
└───────────────┘   └───────────────┘   └───────────────┘
```

### HTML Slides (`/runbook explain --slides [topic]`)

Generate self-contained HTML presentation with keyboard navigation.
Save to `.claude/explanations/[topic].html`

### What to Explain

- Code files: Purpose, flow, key functions
- Architecture: Component diagrams, data flow
- Protocols: Step-by-step process, state transitions
- Concepts: What it is, why it's used, examples

---

# SUBAGENTS

Append "use subagents" to any request where you want Claude to throw more compute at the problem.
— Claude Code team tips

## When to Use Subagents

When user says "use subagents" or `/runbook subagents`:

### Good Candidates

- **Exploration**: "Find all usages of X across the codebase"
- **Parallel analysis**: "Check each module for security issues"
- **Independent implementation**: "Implement these 5 API endpoints"
- **Research**: "Understand how the auth system works"

### Keep in Main Context

- Tasks requiring conversation history
- Decisions needing user input
- Final synthesis

## Subagent Strategies

### Divide and Conquer

```
Main task: "Add validation to all API endpoints"

Subagent 1: Validate user endpoints
Subagent 2: Validate auth endpoints
Subagent 3: Validate billing endpoints

Main: Synthesize results, ensure consistency
```

### Explore Then Execute

```
Subagent (Explore): "Understand how the payment system works"
  → Returns: Architecture summary, key files

Main: Uses findings to implement changes
```

### Parallel Review

```
Subagent 1: Security review
Subagent 2: Performance review
Subagent 3: Test coverage analysis

Main: Synthesizes all feedback
```

## Subagent Types

| Type | Use For |
|------|---------|
| `Explore` | Codebase exploration, finding patterns |
| `Plan` | Creating implementation plans |
| `general-purpose` | Implementing features, fixing bugs |

---

# POWER PROMPTS

## Recovery
- "Knowing everything you know now, scrap this and implement the elegant solution"
- "Stop. Let's re-plan this from scratch."

## Verification
- "Prove to me this works"
- "Grill me on these changes and don't make a PR until I pass"

## Learning
- "Update your CLAUDE.md so you don't make that mistake again"
- "Explain the why behind these changes"

## Delegation
- "Fix." (with context pasted)
- "Go fix the failing CI tests"
- "[task]. Use subagents."

## Quality
- "Is this the best approach, or just the first thing that works?"
- "What would a staff engineer criticize about this?"

---

# WORKFLOWS

## Daily Development Flow
```
1. /runbook worktrees setup 3    # Start parallel sessions
2. Work across multiple tasks    # Don't wait for Claude
3. /runbook update-rules         # After any corrections
4. /runbook techdebt             # End of session cleanup
5. /runbook grill                # Before any PR
```

## Complex Feature Flow
```
1. Enter plan mode               # Design the approach
2. /runbook plan-review          # Get staff engineer feedback
3. Revise plan                   # Address concerns
4. Implement with subagents      # Parallel execution
5. /runbook grill                # Challenge yourself
6. /runbook elegant              # If solution feels hacky
```

## Bug Fix Flow
```
1. [Paste bug report or logs]
2. /runbook fix                  # Delegate fully
```

---

**Remember:** There is no one right way to use Claude Code. Experiment to see what works for you.

---

## Credits

Based on [Boris Cherny's Twitter thread](https://x.com/bcherny/status/1885103675015516287) sharing tips from the Claude Code team at Anthropic.

Boris is the creator of Claude Code.
