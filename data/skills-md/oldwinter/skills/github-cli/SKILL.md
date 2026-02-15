---
name: github-cli
description: This skill should be used when users need to interact with GitHub via the gh CLI. It covers repository management (create, delete, clone, fork), CI/CD workflows (GitHub Actions), Issues, Pull Requests, Releases, and other GitHub operations. Triggers on requests mentioning GitHub, repos, PRs, issues, actions, or workflows.
---

# GitHub CLI Skill

This skill provides comprehensive guidance for using the GitHub CLI (`gh`) to manage repositories, CI/CD workflows, issues, pull requests, and releases.

## Prerequisites

- `gh` CLI installed and authenticated
- Run `gh auth status` to verify authentication

## Core Operations

### Repository Management

```bash
# List repositories
gh repo list [owner] --limit 50
gh repo list --source                    # Only source repos (not forks)
gh repo list --fork                      # Only forks

# View repository
gh repo view [repo]
gh repo view --web                       # Open in browser

# Create repository
gh repo create <name> --public           # Public repo
gh repo create <name> --private          # Private repo
gh repo create <name> --clone            # Create and clone locally
gh repo create <name> --template <repo>  # From template

# Clone repository
gh repo clone <repo>
gh repo clone <repo> -- --depth 1        # Shallow clone

# Fork repository
gh repo fork <repo>
gh repo fork <repo> --clone              # Fork and clone

# Delete repository
gh repo delete <repo> --yes              # Requires confirmation

# Archive/Unarchive
gh repo archive <repo>
gh repo unarchive <repo>

# Edit repository settings
gh repo edit --default-branch main
gh repo edit --visibility public
gh repo edit --enable-issues=false
```

### Pull Requests

```bash
# List PRs
gh pr list
gh pr list --state all                   # All states
gh pr list --author @me                  # My PRs
gh pr list --search "is:open draft:false"

# View PR
gh pr view [number]
gh pr view --web                         # Open in browser
gh pr view --comments                    # Show comments

# Create PR
gh pr create                             # Interactive
gh pr create --title "Title" --body "Description"
gh pr create --draft                     # Create as draft
gh pr create --base main --head feature  # Specify branches
gh pr create --fill                      # Auto-fill from commits

# Review PR
gh pr review [number] --approve
gh pr review [number] --request-changes --body "Comments"
gh pr review [number] --comment --body "LGTM"

# Merge PR
gh pr merge [number]
gh pr merge --merge                      # Merge commit
gh pr merge --squash                     # Squash and merge
gh pr merge --rebase                     # Rebase and merge
gh pr merge --auto                       # Enable auto-merge
gh pr merge --delete-branch              # Delete branch after merge

# Other PR operations
gh pr checkout [number]                  # Checkout PR locally
gh pr ready [number]                     # Mark as ready for review
gh pr close [number]
gh pr reopen [number]
gh pr diff [number]
gh pr checks [number]                    # View CI status
```

### Issues

```bash
# List issues
gh issue list
gh issue list --state all
gh issue list --label "bug"
gh issue list --assignee @me
gh issue list --search "is:open label:urgent"

# View issue
gh issue view [number]
gh issue view --web
gh issue view --comments

# Create issue
gh issue create                          # Interactive
gh issue create --title "Title" --body "Description"
gh issue create --label "bug,urgent"
gh issue create --assignee "@me,user2"
gh issue create --milestone "v1.0"

# Edit issue
gh issue edit [number] --title "New title"
gh issue edit [number] --add-label "priority"
gh issue edit [number] --remove-label "wontfix"
gh issue edit [number] --add-assignee "user"

# Close/Reopen
gh issue close [number]
gh issue close [number] --reason "not planned"
gh issue reopen [number]

# Transfer issue
gh issue transfer [number] <destination-repo>

# Pin/Unpin issue
gh issue pin [number]
gh issue unpin [number]
```

### GitHub Actions (Workflows)

```bash
# List workflows
gh workflow list
gh workflow list --all                   # Include disabled

# View workflow
gh workflow view [workflow-id|name]
gh workflow view --web

# Run workflow manually
gh workflow run [workflow]
gh workflow run [workflow] --ref branch-name
gh workflow run [workflow] -f param1=value1 -f param2=value2

# Enable/Disable workflow
gh workflow enable [workflow]
gh workflow disable [workflow]

# List workflow runs
gh run list
gh run list --workflow [workflow]
gh run list --branch main
gh run list --status failure
gh run list --user @me

# View run details
gh run view [run-id]
gh run view --web
gh run view --log                        # Full logs
gh run view --log-failed                 # Only failed job logs

# Watch run in progress
gh run watch [run-id]

# Rerun workflow
gh run rerun [run-id]
gh run rerun [run-id] --failed           # Only failed jobs
gh run rerun [run-id] --debug            # With debug logging

# Cancel run
gh run cancel [run-id]

# Download artifacts
gh run download [run-id]
gh run download [run-id] -n artifact-name
```

### Releases

```bash
# List releases
gh release list
gh release list --exclude-drafts

# View release
gh release view [tag]
gh release view --web

# Create release
gh release create <tag>                  # Interactive
gh release create <tag> --title "Title" --notes "Notes"
gh release create <tag> --generate-notes # Auto-generate notes
gh release create <tag> --draft          # Create as draft
gh release create <tag> --prerelease     # Mark as pre-release
gh release create <tag> ./dist/*         # Upload assets

# Edit release
gh release edit <tag> --title "New title"
gh release edit <tag> --draft=false      # Publish draft

# Delete release
gh release delete <tag>
gh release delete <tag> --cleanup-tag    # Also delete tag

# Download assets
gh release download <tag>
gh release download <tag> -p "*.zip"     # Pattern match

# Upload additional assets
gh release upload <tag> ./file.zip
```

### Gists

```bash
# List gists
gh gist list
gh gist list --public
gh gist list --secret

# View gist
gh gist view [gist-id]
gh gist view --web

# Create gist
gh gist create file.txt                  # Single file
gh gist create file1.txt file2.txt       # Multiple files
gh gist create --public file.txt         # Public gist
gh gist create -d "Description" file.txt

# Edit gist
gh gist edit [gist-id]
gh gist edit [gist-id] -a newfile.txt    # Add file

# Delete gist
gh gist delete [gist-id]

# Clone gist
gh gist clone [gist-id]
```

### GitHub API Direct Access

```bash
# GET request
gh api repos/{owner}/{repo}
gh api /user
gh api orgs/{org}/repos --paginate

# POST request
gh api repos/{owner}/{repo}/issues -f title="Bug" -f body="Description"

# With JSON
gh api repos/{owner}/{repo}/labels --input data.json

# GraphQL
gh api graphql -f query='{ viewer { login } }'

# Output formatting
gh api repos/{owner}/{repo} --jq '.name'
gh api repos/{owner}/{repo} -t '{{.name}}'
```

### Labels

```bash
# List labels
gh label list

# Create label
gh label create "priority:high" --color FF0000 --description "High priority"

# Edit label
gh label edit "old-name" --name "new-name"
gh label edit "bug" --color 00FF00

# Delete label
gh label delete "label-name"

# Clone labels from another repo
gh label clone source-repo
```

### SSH Keys & GPG Keys

```bash
# List SSH keys
gh ssh-key list

# Add SSH key
gh ssh-key add ~/.ssh/id_rsa.pub --title "My Key"

# Delete SSH key
gh ssh-key delete [key-id]

# List GPG keys
gh gpg-key list

# Add GPG key
gh gpg-key add key.gpg
```

## Common Patterns

### Batch Operations

```bash
# Close all issues with specific label
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {}

# Delete all draft releases
gh release list --json tagName,isDraft --jq '.[] | select(.isDraft) | .tagName' | \
  xargs -I {} gh release delete {} --yes

# Approve and merge all dependabot PRs
gh pr list --author "app/dependabot" --json number --jq '.[].number' | \
  xargs -I {} sh -c 'gh pr review {} --approve && gh pr merge {} --squash'
```

### JSON Output and Filtering

```bash
# Get specific fields
gh pr list --json number,title,author
gh issue list --json number,title,labels --jq '.[] | {num: .number, title: .title}'

# Filter with jq
gh pr list --json number,title,mergeable --jq '.[] | select(.mergeable == "MERGEABLE")'
```

### Cross-Repository Operations

```bash
# Specify repository explicitly
gh pr list -R owner/repo
gh issue create -R owner/repo --title "Title"
gh workflow run -R owner/repo workflow.yml
```

## Troubleshooting

```bash
# Check authentication
gh auth status

# Refresh authentication
gh auth refresh

# Login with specific scopes
gh auth login --scopes "repo,workflow,admin:org"

# Debug mode
GH_DEBUG=1 gh <command>

# Check rate limit
gh api rate_limit
```

## Reference

For detailed command reference including all flags and options, see `references/gh-commands.md`.
