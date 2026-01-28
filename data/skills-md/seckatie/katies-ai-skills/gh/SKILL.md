---
name: gh
description: GitHub CLI (gh) for repository management, rulesets, releases, PRs, and issues. This skill is triggered when the user says things like "create a GitHub PR", "list GitHub issues", "set up branch protection", "create a ruleset", "configure GitHub rulesets", "create a GitHub release", "clone this repo", or "manage GitHub repository settings".
---

# GitHub CLI (gh)

The GitHub CLI brings GitHub to your terminal for seamless workflows.

## Repository Rulesets

Rulesets protect branches and tags with configurable rules.

### Create a Branch Protection Ruleset

```bash
gh api repos/{owner}/{repo}/rulesets --method POST --input - <<'EOF'
{
  "name": "Protect main",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "pull_request", "parameters": {"required_approving_review_count": 1, "dismiss_stale_reviews_on_push": false, "require_code_owner_review": false, "require_last_push_approval": false, "required_review_thread_resolution": false}},
    {"type": "deletion"},
    {"type": "non_fast_forward"}
  ],
  "bypass_actors": [
    {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
  ]
}
EOF
```

### Create a Tag Protection Ruleset

```bash
gh api repos/{owner}/{repo}/rulesets --method POST --input - <<'EOF'
{
  "name": "Protect tags",
  "target": "tag",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["~ALL"],
      "exclude": []
    }
  },
  "rules": [
    {"type": "creation"},
    {"type": "update"},
    {"type": "deletion"}
  ],
  "bypass_actors": [
    {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
  ]
}
EOF
```

### Bypass Actors

Add `bypass_actors` to allow certain roles to bypass rules:

```json
"bypass_actors": [
  {"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}
]
```

**Repository Role IDs:**
| ID | Role |
|----|------|
| 1 | Read |
| 2 | Triage |
| 3 | Write |
| 4 | Maintain |
| 5 | Admin |

**Bypass Modes:**
- `always` - Can always bypass the rules
- `pull_request` - Can only bypass via pull request

### View Rulesets

```bash
# List all rulesets
gh ruleset list

# View a specific ruleset
gh api repos/{owner}/{repo}/rulesets/{ruleset_id}

# View in browser
gh ruleset view {ruleset_id} --web
```

### Update a Ruleset

```bash
gh api repos/{owner}/{repo}/rulesets/{ruleset_id} --method PUT --input - <<'EOF'
{
  "name": "Updated name",
  "enforcement": "active",
  ...
}
EOF
```

### Delete a Ruleset

```bash
gh api repos/{owner}/{repo}/rulesets/{ruleset_id} --method DELETE
```

## Available Rule Types

### Branch Rules
- `pull_request` - Require pull requests before merging
- `required_status_checks` - Require status checks to pass
- `commit_message_pattern` - Enforce commit message format
- `commit_author_email_pattern` - Enforce author email format
- `committer_email_pattern` - Enforce committer email format
- `branch_name_pattern` - Enforce branch naming conventions
- `non_fast_forward` - Prevent force pushes
- `deletion` - Prevent branch deletion
- `creation` - Restrict branch creation
- `update` - Restrict branch updates
- `required_linear_history` - Require linear history
- `required_signatures` - Require signed commits

### Tag Rules
- `creation` - Restrict tag creation
- `update` - Prevent moving tags
- `deletion` - Prevent tag deletion

## Releases

```bash
# Create a release
gh release create v1.0.0 --title "v1.0.0" --notes "Release notes here"

# Create release with auto-generated notes
gh release create v1.0.0 --generate-notes

# Create a draft release
gh release create v1.0.0 --draft

# List releases
gh release list

# View a release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0
```

## Pull Requests

```bash
# Create a PR
gh pr create --title "Title" --body "Description"

# Create PR with template
gh pr create --fill

# List PRs
gh pr list

# View PR
gh pr view 123

# Checkout a PR locally
gh pr checkout 123

# Merge a PR
gh pr merge 123 --squash
```

## Issues

```bash
# Create an issue
gh issue create --title "Bug" --body "Description"

# List issues
gh issue list

# View issue
gh issue view 123

# Close an issue
gh issue close 123
```

## Repository

```bash
# Clone a repo
gh repo clone owner/repo

# Create a repo
gh repo create my-repo --public

# Fork a repo
gh repo fork owner/repo

# View repo in browser
gh repo view --web
```
