---
name: create-pr
description: "Automated PR workflow: analyze code changes, auto-generate Issue/PR descriptions, auto-commit with DCO sign-off, auto-push, auto-create Issue + PR, and link PR to Issue."
version: 7.0.0
platform-agnostic: true
---

# Create PR Skill v7.0.0

Platform-agnostic automated PR workflow:
1. Analyze code changes and detect logic changes (functions/classes + file stats)
2. Auto-generate Issue + PR titles and descriptions
3. Auto-commit **with DCO sign-off** (`Signed-off-by`)
4. Auto-push
5. Auto-create Issue (optional, via API)
6. Auto-create PR with Issue linkage (`Fixes #id`)

## Quick Start

### 1) Configure Token (one time, for API features)

The script supports multiple platforms via configuration:

```bash
# For GitCode/GitLab
git config --global gitcode.token "your_token"

# For GitHub
git config --global github.token "your_token"

# Or use environment variables
export GITCODE_TOKEN="your_token"
export GITHUB_TOKEN="your_token"
```

Token permissions: `api`, `read_api`, `write_repository`

### 2) Run

```bash
python scripts/create-pr/full_auto_pr.py
```

## What It Does

- Deep change analysis from `git diff`
- Detects:
  - added/modified/removed functions
  - added/modified/removed classes
  - top changed files with line stats
- Generates structured Issue + PR descriptions based on real diffs
- **Auto-adds DCO sign-off** (`Signed-off-by: Name <email>`)
- Pushes to remote
- Creates Issue + PR via platform API (when configured)
- Links PR to Issue (adds `Fixes #id`)
- Falls back to web interface if API unavailable

## Usage Options

```bash
python scripts/create-pr/full_auto_pr.py --target main
python scripts/create-pr/full_auto_pr.py --no-issue
python scripts/create-pr/full_auto_pr.py --no-commit
python scripts/create-pr/full_auto_pr.py --no-push
python scripts/create-pr/full_auto_pr.py --analyze-only
```

## Output Artifacts

Generated Issue description:
- Summary + change type
- Affected components
- Added/modified/removed functions and classes
- Key file changes with +/-
- File type stats
- Commit history
- Diff stats

Generated PR description:
- Summary (from commits)
- Changes (function/class + component groups)
- Test plan
- Related Issue (`Fixes #id`)

## Files

```
create-pr/
├── SKILL.md
├── CHANGELOG.md
├── README.md
├── examples/
│   └── example-workflow.md
├── references/
│   ├── commit-message-guide.md
│   ├── pr-description-template.md
│   ├── platform-apis.md
│   └── common-issues.md
└── scripts/
    ├── repo_api.py         # Platform-agnostic API client + analyzer
    └── full_auto_pr.py     # End-to-end automation
```

## Platform Support

The script automatically detects the platform from your git remote URL:
- **GitCode/GitLab**: Uses GitLab-compatible API v4
- **GitHub**: Uses GitHub REST API v3
- **Others**: Falls back to web-based PR creation

## Notes

- **DCO (Developer Certificate of Origin)** is automatically added to commit messages
  - Requires `git config user.name` and `git config user.email` to be set
  - Adds `Signed-off-by: Name <email>` line to each commit
  - Ensures PR passes DCO validation checks
- If platform API is not configured or fails, the script opens browser for manual PR creation
- Token can be set via git config, environment variables, or `~/.platform-token` file
