---
name: pr-assistant
description: Analyzes git changes and assists with creating comprehensive pull requests. Use when user wants to create a PR, review changes before PR, or needs help drafting PR descriptions. Triggers on phrases like 'create PR', 'make a pull request', 'draft PR description', 'what changed in this branch', 'prepare PR'.
---

# PR Assistant

Assists with creating well-structured pull requests by analyzing changes and generating comprehensive PR descriptions.

## Core Philosophy

**Human-in-the-loop**: This skill generates PR drafts that MUST be reviewed and approved by the user before submission. Never auto-create PRs without explicit confirmation.

## Workflow

### 1. Analyze Changes

First, gather context about the current branch:

```bash
# Get current branch and target branch
CURRENT_BRANCH=$(git branch --show-current)
TARGET_BRANCH=${TARGET_BRANCH:-main}

# Get diff summary
git diff $TARGET_BRANCH...$CURRENT_BRANCH --stat

# Get commit messages
git log $TARGET_BRANCH...$CURRENT_BRANCH --oneline

# Get detailed changes by category
git diff $TARGET_BRANCH...$CURRENT_BRANCH --name-status
```

Use `scripts/analyze_changes.py` to categorize changes into:
- Backend changes (apis/, requirements.txt)
- Frontend changes (ui/)
- Database changes (supabase/)
- DevOps changes (docker-compose.yml, Dockerfile, etc.)
- Documentation (doc/, *.md)

### 2. Determine PR Type

Based on the analysis, select the appropriate template:
- **Feature**: New functionality or enhancements
- **Bugfix**: Bug fixes or corrections
- **Docs**: Documentation updates
- **Refactor**: Code restructuring without behavior change
- **Chore**: Dependencies, config, tooling updates

### 3. Generate PR Draft

Use `scripts/generate_pr_body.py` with the appropriate template from `assets/templates/`.

Auto-fill sections:
- **Summary**: Generated from commit messages and file changes
- **Changes breakdown**: Categorized list of modified files
- **Related issues**: Parse commit messages for `#123`, `fixes #456` patterns
- **Checklist**: Auto-populate based on change types

### 4. Quality Checks

Run `scripts/quality_checks.sh` to check for:
- Uncommitted changes
- Merge conflicts
- TODO/FIXME comments in changed files
- Missing test files (for significant code changes)
- Large file additions (>1MB)

Present warnings to user but don't block PR creation.

### 5. Present Draft for Review

**CRITICAL**: Present the generated PR body in a clear, editable format and explicitly ask the user to review and approve it.

Example presentation:
```
I've prepared a PR draft. Please review the content below and let me know if you'd like any changes:

---
[Generated PR body here]
---

Would you like me to:
1. Create the PR with this content
2. Make edits to the description
3. Change the target branch (currently: main)
4. Add/remove reviewers
```

### 6. Create PR Only After Approval

Once the user approves, use `gh` CLI:

```bash
gh pr create \
  --title "PR Title" \
  --body-file /tmp/pr-body.md \
  --base main \
  --head current-branch \
  [--reviewer user1,user2] \
  [--label label1,label2]
```

## Project-Specific Configuration

For this repository (tomodachi/srms):

**Categories**:
- Backend: `apis/`, `requirements.txt`
- Frontend: `ui/src/`, `ui/package.json`
- Database: `supabase/`
- DevOps: `docker-compose.yml`, `Dockerfile`, `nginx.conf`, `supervisord.conf`
- Docs: `doc/`, `README.md`, `CLAUDE.md`

**Default reviewers** (suggest based on changes):
- Backend changes → Backend team
- Frontend changes → Frontend team
- Database changes → DBA/Backend team

**Branch naming conventions**:
- `feature/*` → Feature template
- `bugfix/*` or `fix/*` → Bugfix template
- `docs/*` → Docs template
- Other → Feature template (default)

## Best Practices

See `references/pr-best-practices.md` for detailed guidelines.

Key points:
- Keep PRs focused (single concern)
- Write clear, descriptive titles
- Explain the "why" not just "what"
- Include testing evidence
- Link to related issues
- Self-review before requesting review

## Interactive Editing

If the user wants to edit the draft:
1. Ask which section to modify
2. Update the specific section
3. Re-present the full draft
4. Repeat until approved

## Common Commands

User might say:
- "Create a PR" → Full workflow
- "What changed?" → Just analysis (step 1)
- "Draft PR description" → Steps 1-3, present draft
- "Update PR description" → Edit existing draft
- "Check if ready for PR" → Run quality checks

## Error Handling

If issues arise:
- No commits ahead of target → Inform user, suggest checking branch
- Merge conflicts → Show conflicts, suggest resolving first
- No GitHub CLI → Inform user, offer to create PR body for manual submission
- API rate limits → Suggest waiting or manual creation

## Output Format

Always save the generated PR body to a temporary file for easy editing:
```bash
PR_BODY_FILE=".tmp/outputs/pr-body-$(date +%s).md"
```

This allows the user to edit it manually if needed before submission.
