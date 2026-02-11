---
name: building-agent-team-prompts
description: Provides a prompt template and best practices for building Claude Code agent teams. Covers team composition, teammate spawn prompts, task breakdown, file ownership, communication protocols, and delegate mode. Use when creating an agent team, spawning teammates, parallelizing work across multiple Claude Code instances, or deciding whether an agent team is the right approach.
metadata:
  author: frontboat
  version: "1.0.0"
---

# Building Agent Team Prompts

## Overview

Agent team prompts must be self-contained — teammates don't inherit your conversation history. Every piece of context a teammate needs must be in their spawn prompt or discoverable from the codebase.

**Core principle:** A good agent team prompt specifies WHO does WHAT on WHICH files, HOW they communicate, and WHEN they're done.

## Before You Build the Prompt

Verify the task actually benefits from an agent team:

- Multiple independent workstreams (review, research, non-overlapping implementation)
- Competing hypotheses that benefit from parallel investigation
- Cross-layer work where each layer is independently ownable

**Don't use agent teams for:** sequential tasks, work concentrated in a few files, or simple tasks where coordination overhead exceeds benefit. Use subagents or a single session instead.

## Prompt Template

Every agent team prompt should cover these sections. Skip sections that don't apply.

### 1. Goal

One sentence: what is the team trying to accomplish?

### 2. Team Composition

For each teammate:

- **Name**: descriptive, kebab-case (`security-reviewer`, `backend-impl`)
- **Role**: one sentence describing their focus
- **Model**: `sonnet` for routine/research tasks, `opus` for complex reasoning. Default to `sonnet` unless the task demands deep analysis.

**Right-sizing:** Prefer fewer teammates with more tasks over many single-task teammates. A team of 3 with 5 tasks each beats a team of 6 with 2 each. Only spawn a teammate when the work genuinely benefits from a separate context window.

**Heuristic:** Before spawning, estimate the work per teammate. If a teammate would have fewer than 3 tasks or less than 15 minutes of work, merge their responsibilities into another teammate's role instead.

### 3. Teammate Spawn Prompts

Each teammate gets a self-contained prompt including:

- **Full task context** — what they need to know that isn't in CLAUDE.md
- **Specific instructions** — what to investigate, build, or review
- **File ownership** — which files/directories they own exclusively
- **Hands off** — files owned by other teammates they must not modify
- **Output expectations** — format, structure, where to write results

**Critical:** Teammates can't see your conversation. If the user explained something important earlier, include it in the spawn prompt.

**Always include:** Tell each teammate to check existing codebase patterns before building or reviewing. For implementation: "Before writing new code, check how similar features are implemented in the codebase and follow those patterns." For review: "Check project conventions and existing patterns to calibrate your review."

### 4. Task Breakdown

Define concrete tasks with:

- Clear deliverable per task
- Dependencies between tasks (what blocks what)
- Assignment to a specific teammate
- **Target: 3-6 tasks per teammate**

Don't just assign roles — break work into trackable tasks with the shared task list.

### 5. Communication Protocol

Specify when teammates should message each other:

- **Share findings**: "If you discover X, message `teammate-Y`"
- **Cross-cutting concerns**: "Flag breaking changes to all teammates"
- **Adversarial challenge**: for debugging, teammates actively try to disprove each other's theories

If teammates don't need to communicate, say so explicitly — it saves tokens.

### 6. Coordination Settings

- **Delegate mode**: Use when the lead should coordinate only, not implement. Recommended for 3+ teammates or when the lead would compete for files.
- **Plan approval**: Require when teammates modify production code or make architectural decisions. Skip for read-only research/review.
- **Definition of done**: State explicitly what constitutes completion.

### 7. Deliverables

- What each teammate produces (with format)
- What the lead synthesizes from teammate outputs
- Final output (report, PR comments, implementation, etc.)

## Task Type Patterns

### Code Review

- Scope reviewers by domain, not file count
- Cross-cutting reviewers (security, testing) coordinate with domain reviewers
- Structured output per finding: `severity | file:line | description | suggestion`
- Lead synthesizes into single review summary

### Feature Implementation

- One teammate per layer (DB / API / frontend / tests)
- Define shared interfaces explicitly — one teammate defines the API contract, others consume it
- **Require plan approval** before implementation
- **Use delegate mode** for the lead
- Strict file ownership — no two teammates touch the same file

### Debugging / Investigation

- One teammate per hypothesis
- **Use adversarial structure**: teammates challenge each other's theories via messages
- Include a reproduction teammate if the bug is intermittent
- Lead tracks which hypotheses survive scrutiny and synthesizes the conclusion

### Research / Exploration

- One teammate per research angle
- Instruct teammates to ground findings in the actual codebase, not general knowledge
- Define a synthesis plan: who writes the final report and in what format
- Set scope boundaries to prevent endless research

## File Ownership Rules

File conflicts are the #1 source of wasted work in agent teams.

1. **Every modified file has exactly one owner** — if two teammates need it, one owns it and the other requests changes via messages
2. **Shared types/interfaces**: one teammate defines them, others read only
3. **Tests**: owned by whoever owns the code under test, or a dedicated test teammate who doesn't touch source
4. **Config files**: one designated teammate

## Quick Reference

| Element | Ask yourself |
|---------|-------------|
| Team size | Can fewer teammates with more tasks do this? |
| Model | Does this need Opus, or is Sonnet sufficient? |
| Delegate mode | Should the lead avoid implementing? (yes for 3+) |
| Plan approval | Are teammates modifying production code? |
| Communication | Do teammates need to share or challenge findings? |
| File ownership | Could two teammates touch the same file? |
| Scope | When is this team "done"? |
| Deliverables | What exactly does each teammate produce? |

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|------------|-----|
| No file ownership | Teammates overwrite each other | Assign every modified file to one owner |
| Vague deliverables | Inconsistent output quality | Specify format per teammate |
| All teammates on Opus | 4x cost for Sonnet-level tasks | Default to Sonnet, upgrade selectively |
| No communication plan | Silos, missed cross-cutting insights | Specify message triggers |
| Lead implements too | Competes with teammates for files | Enable delegate mode |
| No scope boundary | Research runs forever | Define "done" explicitly |
| Too many teammates | Coordination overhead exceeds benefit | Fewer teammates, more tasks each |
| No plan approval | Bad architectural decisions ship | Require for implementation tasks |
| No existing pattern check | Teammates reinvent what exists | Tell them to check how similar features work |
