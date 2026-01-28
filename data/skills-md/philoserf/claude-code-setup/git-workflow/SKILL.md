---
name: git-workflow
description: Automates git workflows with branch management, atomic commits, history cleanup, and PRs. Use when committing, pushing, creating PRs, cleaning up commits, or organizing git changes with best practices.
allowed-tools: [Read, Bash, AskUserQuestion, TodoWrite]
# model: inherit
---

## Reference Files

Detailed git workflow guidance:

- [workflow-phases.md](workflow-phases.md) - Step-by-step instructions for each workflow phase (0-6) with specific commands, safety checks, and decision points
- [commit-format.md](commit-format.md) - Comprehensive commit message formatting guide with rules, examples, templates, and common mistakes
- [rebase-guide.md](rebase-guide.md) - Interactive rebase safety guidelines, commands, conflict resolution, and recovery techniques
- [examples.md](examples.md) - Real-world workflow scenarios showing the skill in action across different situations

---

# Git Workflow Skill

This skill provides intelligent, end-to-end Git workflow automation. It analyzes repository changes, organizes them into atomic commits with well-formatted messages, manages branches, cleans up commit history, and helps create pull requests.

## Contents

- [Workflow Overview](#workflow-overview)
- [Phase 0: Branch Management](#phase-0-branch-management)
- [Phase 1: Repository Analysis](#phase-1-repository-analysis)
- [Phase 2: Organize into Atomic Commits](#phase-2-organize-into-atomic-commits)
- [Phase 3: Create Commits](#phase-3-create-commits)
- [Phase 4: Commit History Cleanup (Optional)](#phase-4-commit-history-cleanup-optional)
- [Phase 4.5: Pre-Push Quality Review (Mandatory)](#phase-45-pre-push-quality-review-mandatory)
- [Phase 5: Push with Confirmation](#phase-5-push-with-confirmation)
- [Phase 6: Pull Request Creation (Optional)](#phase-6-pull-request-creation-optional)
- [Safety Checks](#safety-checks)
- [Common Edge Cases](#common-edge-cases)
- [Tool Usage Examples](#tool-usage-examples)
- [User Interaction Patterns](#user-interaction-patterns)
- [Reference Documentation](#reference-documentation)
- [Summary](#summary)

## Workflow Overview

The skill follows a 7-phase workflow:

0. **Branch Management** - Ensure work is on appropriate branch
1. **Repository Analysis** - Understand current state and changes
2. **Organize into Atomic Commits** - Group related changes logically
3. **Create Commits** - Generate well-formatted commit messages
4. **Commit History Cleanup** - Optionally reorganize commits before push
   4.5. **Pre-Push Quality Review** - Analyze commit quality and run tests (MANDATORY)
5. **Push with Confirmation** - Push changes to remote after approval
6. **Pull Request Creation** - Optionally create PR with generated description

## Phase 0: Branch Management

**Goal**: Prevent accidental work on protected branches and ensure proper isolation.

If the user is on a protected branch (main/master/develop/production/staging) with uncommitted changes, BLOCK and require creating a feature branch. If working directory is clean, proactively suggest branching. Provides 3 options: auto-suggested branch (recommended), custom branch name, or override with confirmation.

Skip this phase if the user is already on a feature branch, hotfix branch, or release branch.

**For detailed steps, see [phase-0-protocol.md](phase-0-protocol.md) and [workflow-phases.md#phase-0-branch-management](workflow-phases.md#phase-0-branch-management).**

## Phase 1: Repository Analysis

**Goal**: Thoroughly understand the current repository state and changes.

Run git commands to see changed files, diffs, and recent history. Analyze to identify types of changes, affected files, logical groupings, and untracked files.

Perform safety checks for merge conflicts and rebase-in-progress before proceeding.

**For detailed steps, see [workflow-phases.md#phase-1-repository-analysis](workflow-phases.md#phase-1-repository-analysis).**

## Phase 2: Organize into Atomic Commits

**Goal**: Group changes into logical, atomic commits that each represent a single coherent change.

Apply atomic commit principles: one logical change per commit, self-contained and compilable, related changes together.

Group changes by priority: bug fixes → tests → refactoring → features → documentation → configuration.

Create a commit plan and present to user for approval. Use TodoWrite to track commits if there are 3+.

**For detailed steps and grouping strategy, see [workflow-phases.md#phase-2-organize-into-atomic-commits](workflow-phases.md#phase-2-organize-into-atomic-commits).**

## Phase 3: Create Commits

**Goal**: Create each commit with a properly formatted commit message.

For each commit: stage files, generate well-formatted commit message (≤72 chars, imperative mood, explains WHY), execute commit using heredoc, and verify success.

**Key commit message rules**:

- Imperative mood: "Add feature" not "Added"
- Be specific: "Fix null pointer in login" not "Fix bug"
- Explain WHY, not WHAT
- Summary ≤72 characters, body wrapped at 72

**For detailed formatting rules, examples, and templates, see [commit-format.md](commit-format.md).**

**For detailed steps, see [workflow-phases.md#phase-3-create-commits](workflow-phases.md#phase-3-create-commits).**

## Phase 4: Commit History Cleanup (Optional)

**Goal**: Optionally reorganize recent commits for a cleaner history before pushing.

Offer cleanup when multiple commits could be squashed, messages need improvement, or better ordering would help. Skip if commits are already pushed (unless explicit force push approval), on shared branch, or only one commit.

**IMPORTANT**: NEVER use `git rebase -i` (requires interactive input). Instead, explain manual commands to user or use non-interactive alternatives like `git reset --soft`.

**For detailed rebase safety guidelines, commands, and examples, see [rebase-guide.md](rebase-guide.md).**

**For detailed steps, see [workflow-phases.md#phase-4-commit-history-cleanup-optional](workflow-phases.md#phase-4-commit-history-cleanup-optional).**

## Phase 4.5: Pre-Push Quality Review (Mandatory)

**Goal**: Ensure commit quality and verify tests before pushing to remote.

**This phase is MANDATORY** - it always runs before Phase 5 to catch quality issues early.

Performs automated analysis of commits including generic message detection, squash opportunity identification, format compliance verification, and offers test execution.

Shows push preview with commit list, stats, and quality report. If issues found, provides clear options to fix or override with justification.

**Quality checks performed**:

- **Generic message detection** - Flags "WIP", "fix", "update", "temp" and other vague messages
- **Squash opportunity detection** - Identifies related commits that could be combined
- **Format compliance** - Verifies 72-char limit, imperative mood, capitalization
- **Test integration** - Detects and offers to run npm, pytest, go test, cargo test, make test

**User options when issues detected**:

- **Fix issues** - Return to Phase 3 or 4 to reword or squash commits
- **Run tests** - Execute test suite before push (optional)
- **Override** - Push anyway with justification (required for blockers)
- **Cancel** - Exit workflow to investigate

**For detailed quality checks, test detection, and user interaction patterns, see [phase-4.5-protocol.md](phase-4.5-protocol.md).**

**For detailed steps, see [workflow-phases.md#phase-45-pre-push-quality-review-mandatory](workflow-phases.md#phase-45-pre-push-quality-review-mandatory).**

## Phase 5: Push with Confirmation

**Goal**: Push commits to remote safely after user approval.

**CRITICAL**: Before allowing push, check if current branch is protected (main/master/develop/production/staging). If protected, **BLOCK the push** and enter the Protected Branch Push Protocol.

Show summary of commits to be pushed (number, branch, commit messages), ask for confirmation, then push. Use `-u` flag for new branches.

Perform safety checks: verify remote exists, detect and block protected branch pushes, prevent force pushes to protected branches, handle failures gracefully.

**For protected branch handling, see [protected-branch-protocol.md](protected-branch-protocol.md).**

**For detailed steps, see [workflow-phases.md#phase-5-push-with-confirmation](workflow-phases.md#phase-5-push-with-confirmation).**

## Phase 6: Pull Request Creation (Optional)

**Goal**: Optionally create a pull request after successful push.

After successful push, ask if user wants a PR. Verify `gh` CLI is available, detect base branch, generate title and description from commits, show for review, then create PR and show URL.

If `gh` not available, provide GitHub web URL for manual PR creation.

**For detailed steps, see [workflow-phases.md#phase-6-pull-request-creation-optional](workflow-phases.md#phase-6-pull-request-creation-optional).**

## Safety Checks

Always perform these checks during the workflow:

1. **Before any operation**:
   - Check for merge conflicts in files
   - Check for rebase/merge in progress
   - Alert user and stop if found

2. **Before committing**:
   - Verify files are actually changed
   - Check commit message meets format requirements

3. **Before rebasing**:
   - Verify commits haven't been pushed (or get explicit force-push approval)
   - Check not on protected branch
   - Ensure working directory is clean

4. **Before pushing**:
   - Verify remote exists
   - **CRITICAL**: Check if current branch is protected - if yes, BLOCK and enter Protected Branch Push Protocol
   - Detect force push requirement - if pushing to protected branch, BLOCK absolutely
   - Confirm with user (only if not blocked)

5. **Before creating PR**:
   - Verify push succeeded
   - Check branch exists on remote
   - Verify gh CLI or provide alternative

## Common Edge Cases

**No changes to commit**:

- Inform user repository is clean
- Exit gracefully

**Untracked files found**:

- List untracked files
- Ask if any should be included
- Identify files that should be .gitignored (.env, debug logs, etc.)
- Add to .gitignore if appropriate

**Large changesets** (10+ files or 500+ lines):

- May need user guidance for grouping
- Suggest reviewing changes carefully
- Consider breaking into multiple PRs

**Detached HEAD state**:

- Alert user
- Explain situation
- Offer to create branch from current commit

**Merge conflicts**:

- Do not proceed with commits
- Alert user to resolve conflicts first
- Show conflicted files and suggest resolution steps

**No remote configured**:

- Detect with `git remote -v`
- Ask if user wants to add remote
- Help set up origin if needed

**Protected branch** (working on main/master/develop/production/staging):

- **Phase 0**: Blocks if uncommitted changes exist, requires branching
- **Phase 5**: Blocks if trying to push commits, requires migration
- See [phase-0-protocol.md](phase-0-protocol.md) for start-of-work protocol
- See [protected-branch-protocol.md](protected-branch-protocol.md) for push-time protocol

**Rebase in progress**:

- Detect state
- Alert user
- Ask if they want to continue or abort:
  - Continue: User must resolve manually
  - Abort: Run `git rebase --abort`

## Tool Usage Examples

**Check current state**:

```bash
git status --short
git branch --show-current
git log --oneline -n 10
```

**Analyze changes**:

```bash
git diff
git diff --staged
git diff --stat
```

**Create commits**:

```bash
git add file1.js file2.js
git commit -m "$(cat <<'EOF'
Add user authentication feature

Implement JWT-based authentication to secure API endpoints.

- Add login/logout endpoints
- Implement JWT token generation and validation
- Add authentication middleware
EOF
)"
```

**Push changes**:

```bash
# New branch
git push -u origin feature/user-auth

# Existing branch
git push
```

**Create PR**:

```bash
gh pr create --title "Add user authentication" --body "$(cat <<'EOF'
## Summary
Implements JWT-based authentication for API security.

## Changes
- Add login/logout endpoints
- JWT token generation and validation
- Authentication middleware

## Testing
- Added unit tests for auth functions
- Manual testing with Postman
EOF
)"
```

## User Interaction Patterns

Use **AskUserQuestion** for:

- Branch creation confirmation
- Commit plan approval
- Modifications to commit grouping
- Push confirmation
- PR creation confirmation
- Force push warnings
- Protected branch warnings

Use **TodoWrite** for:

- Tracking multiple commits to create (3+ commits)
- Long workflow with many steps
- Keeping user informed of progress

Use **Bash** for:

- All git commands
- All gh commands
- Repository state inspection

## Reference Documentation

For detailed information, see supporting files:

- **[workflow-phases.md](workflow-phases.md)** - Detailed step-by-step instructions for each workflow phase (0-6). Read this when you need the complete procedure for any phase including specific commands, safety checks, and decision points.

- **[commit-format.md](commit-format.md)** - Comprehensive commit message formatting guide with detailed rules, examples, templates, and common mistakes. Read this when you need specific guidance on commit message format, character limits, imperative mood examples, or want to see good vs. bad examples.

- **[rebase-guide.md](rebase-guide.md)** - Interactive rebase safety guidelines, commands, conflict resolution, and recovery techniques. Read this when planning commit history cleanup, before rebasing, or when handling rebase conflicts.

- **[protected-branch-protocol.md](protected-branch-protocol.md)** - Protected branch push prevention protocol with detection logic, 3-option handling (feature branch migration, branch rename, emergency override), force push blocking, and edge cases. Read this when Phase 5 detects a push to protected branch, or when implementing protected branch safety checks.

- **[examples.md](examples.md)** - Real-world workflow scenarios showing the skill in action across different situations: simple features, bug fixes, large refactorings, messy history cleanup, edge cases, and more. Read this to understand how to apply the workflow in practice.

## Summary

This skill automates the entire Git workflow from analyzing changes to creating a PR. It emphasizes:

- **Quality** over speed - well-formatted commits are important
- **Safety** first - always check state and confirm destructive operations
- **User control** - ask for approval at key decision points
- **Education** - explain what's happening and why

The goal is to help users maintain clean, professional Git history with minimal effort while teaching best practices along the way.
