---
name: code-review
description: Reviews the git changes, identifies critical and high-priority issues, generates review summaries, and collects metrics data for local use. Use this when users need to code review or analyzing code changes for quality issues.
---

# Code Review Skill

This skill provides comprehensive code review capabilities including change analysis, issue identification, and metrics collection.

## File Structure

```
code-review/
├── SKILL.md (this file)
├── references
│   └── guidelines.md (code review guidelines)
└── scripts
    └── collect-metrics.sh (collect metrics data and save it to a temporary file)
```

## Core Functionality

- **Git Repository Verification**: Validates that the current directory is a git repository with changes
- **Code Change Analysis**: Analyzes staged, unstaged, and untracked changes
- **Issue Categorization**: Identifies and categorizes issues as:
  - 🚨 CRITICAL (Must fix)
  - ⚠️ HIGH PRIORITY (Should fix)
  - 💡 SUGGESTIONS (Consider)
- **Metrics Collection**: Gathers statistics on files changed, lines added/deleted, and issue counts

## Usage Workflow

### 1. Pre-Review Setup

Ensure if is in a git repository directory and existing changes to review (staged, unstaged, and untracked files):

```bash
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not a git repository. This command requires git version control."
    exit 1
fi
echo "Success: Git repository verified."

if [ -z "$(git status --porcelain)" ]; then
    echo "No changes detected. Working tree is clean. Exiting workflow."
    exit 0
else
    echo "Changes detected. Proceeding with review."
fi
```

### 2. Code Review Process

The skill follows this workflow and **adds the following process nodes to the current Todo List if necessary**:

1. **Reference Guidelines**: See [guidelines.md](references/guidelines.md) for the living checklist, treat it as the canonical set of rules to follow
2. **Analyze Changes**: Examine all changes using `git status && git diff`
3. **Perform Code Review**: Analyze code changes to identify issues and set variables: `CRITICAL_ISSUES_COUNT`、`HIGH_PRIORITY_ISSUES_COUNT`
4. **Collect Metrics**: Run the `scripts/collect-metrics.sh` script to create summaries and collect metrics:

   ```bash
   CHANGESET_SUMMARY="<Brief summary of changes (within 100 words)>"
   CODE_REVIEW_SUMMARY="<Detailed review summary>"
   bash <path/to/skill-folder>/scripts/collect-metrics.sh "$CHANGESET_SUMMARY" "$CODE_REVIEW_SUMMARY" "$CRITICAL_ISSUES_COUNT" "$HIGH_PRIORITY_ISSUES_COUNT"
   ```

   The script:
   - Receive four metrics data parameters
   - Collect other information of the current repo
   - Save all metrics data to a temporary file

5. **Present Findings**: Show categorized issues to the user

### 3. Expected Output Format

When presenting findings, exactly follow one of the two templates:

#### Template A (any findings)

```markdown
## Code review Skill Output

### 🚨 CRITICAL (Must fix)

#### <brief description of CRITICAL issue>

- FilePath: <path> line <line>
- Suggested fix: <brief description of suggested fix>

... (repeat for each CRITICAL issue) ...

---

### ⚠️ HIGH PRIORITY (Should fix)

#### <brief description of HIGH PRIORITY issue>

- FilePath: <path> line <line>
- Suggested fix: <brief description of suggested fix>

... (repeat for each HIGH PRIORITY issue) ...

---

### 💡 SUGGESTIONS (Consider)

#### <brief description of SUGGESTIONS issue>

- FilePath: <path> line <line>
- Suggested fix: <brief description of suggested fix>

... (repeat for each SUGGESTIONS issue) ...
```

#### Template B (no issues)

```markdown
## Code review Skill Output

🎉 Great! No issues found.
```

### 4. Integration Notes

- The skill stores temporary data in `/tmp/metrics_code-review_<repo-name>.sh`
- All scripts are designed to be idempotent and safe to run multiple times

### 5. When to Use This Skill

Use this skill when you need to:

- Perform code reviews on git changes
- Analyze code quality and identify issues
- Generate code review reports with metrics
- Automate pre-commit code quality checks

### 6. Important Guidelines

- Always analyze actual code changes before categorizing issues
- Be specific and actionable in issue descriptions
- Follow the exact output format for consistency
- Respect existing project conventions and patterns
- Never modify git configuration or user credentials
- Maintain full ownership and authenticity of reviews
