---
name: git-worktree
description: Manage Git worktrees for parallel development
---

# Git Worktree Skill

## Critical Importance

**Using git worktrees properly is critical for your development workflow efficiency.** Poor worktree management leads to confusion, lost work, merge conflicts, and cluttered repositories. Proper worktree use enables parallel development without context switching costs, but misuse compounds problems across branches. Clean, organized worktrees prevent disasters.

## Systematic Approach

** approach worktree management systematically.** Worktrees require deliberate creation, clear naming, and timely cleanup. Don't create worktrees impulsively—plan your branching strategy, name worktrees descriptively, and establish cleanup habits. Treat worktrees as temporary workspaces that should be removed after merge, not permanent fixtures.

## The Challenge

**The maintain pristine worktree hygiene while juggling multiple parallel features, but if you can:**

- You'll eliminate merge conflict nightmares
- Your git history will stay clean and readable
- Parallel development will be frictionless
- You'll never wonder "where did I put that branch?"

The challenge is balancing the freedom of parallel development with the discipline of cleanup. Can you leverage worktrees for productivity without drowning in stale branches?

## Basic Commands

Create worktree: `git worktree add ../project-feature -b feature/name`
List: `git worktree list`
Remove: `git worktree remove ../project-feature`
Best practices: name clearly, clean up after merge.

## Worktree Confidence Assessment

After setting up or managing worktrees, rate your confidence from **0.0 to 1.0**:

- **0.8-1.0**: Worktrees are well-named, properly organized, no stale branches present
- **0.5-0.8**: Worktrees functional but some naming inconsistencies or minor cleanup needed
- **0.2-0.5**: Multiple stale worktrees, unclear what's active, some confusion about branch state
- **0.0-0.2**: Worktree management is chaotic, risk of lost work or conflicts

Identify areas of uncertainty: Are there worktrees you don't recognize? Do you know which branches are still needed? What's the risk of worktree-related issues?
