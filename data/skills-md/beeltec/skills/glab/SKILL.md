---
name: glab
description: Use when interacting with GitLab from the command line — creating and managing merge requests, issues, CI/CD pipelines, releases, repositories, and any other GitLab operation. Covers all glab CLI commands including mr, issue, ci, release, repo, api, variable, snippet, schedule, stack, label, milestone, incident, and auth.
---

# GitLab CLI (glab)

Manage GitLab projects entirely from the terminal using `glab`. This skill covers creating merge requests, triaging issues, running pipelines, cutting releases, and making raw API calls — all without leaving your shell.

## When to Use

- Creating, reviewing, approving, or merging merge requests
- Creating, listing, updating, or closing issues and incidents
- Running, retrying, canceling, or viewing CI/CD pipelines and jobs
- Creating releases with assets and changelogs
- Cloning, forking, or managing repositories
- Managing CI/CD variables, schedules, and snippets
- Making raw REST or GraphQL API calls to GitLab
- Working with stacked diffs (experimental)
- Managing labels, milestones, deploy keys, SSH/GPG keys
- Authenticating to GitLab instances

## Prerequisites

- `glab` installed (`brew install glab`, `apt install glab`, or see https://gitlab.com/gitlab-org/cli)
- Authenticated via `glab auth login` (minimum scopes: `api`, `write_repository`)
- Inside a Git repository with a GitLab remote (or use `-R OWNER/REPO` to target another project)

## Command Structure

```
glab <command> <subcommand> [flags]
```

All commands support `-h`/`--help` and `-R`/`--repo OWNER/REPO` (to target a different project).

## Reference Guides

| Topic | File | Load when... |
|-------|------|-------------|
| Merge requests | `references/merge-requests.md` | Creating, reviewing, approving, merging, or listing MRs |
| Issues | `references/issues.md` | Creating, listing, updating, closing, or triaging issues/incidents |
| CI/CD pipelines & jobs | `references/ci-cd.md` | Running, viewing, retrying, canceling pipelines or jobs; linting CI config |
| Releases | `references/releases.md` | Creating releases, uploading assets, managing changelogs |
| Repo, auth & config | `references/repo-and-config.md` | Cloning, forking, creating repos; authenticating; configuring glab |
| API, variables & advanced | `references/api-and-advanced.md` | Making raw API calls; managing variables, snippets, schedules, stacks, labels, milestones, aliases |
| Writing issues & MRs | `references/writing-issues-and-mrs.md` | Writing titles and descriptions for issues or merge requests; following conventional commits; structuring MR descriptions |

## Core Workflows

### Create a Merge Request

Use conventional commit prefixes in titles. See `references/writing-issues-and-mrs.md` for full guidelines.

```bash
# Interactive — prompts for title, description, target branch
glab mr create

# Non-interactive with conventional title, reviewers, and labels
glab mr create -t "feat(auth): add OAuth2 login (closes #123)" --yes -a assignee --reviewer reviewer1 --label "ready for review" -b main

# Draft MR from commit info
glab mr create -f --draft --label WIP
```

### Review and Merge

```bash
glab mr list --reviewer=@me          # MRs awaiting your review
glab mr diff 42                       # View changes
glab mr approve 42                    # Approve
glab mr merge 42                      # Merge (prompts for method)
```

### Create an Issue

Use descriptive titles with type prefixes. See `references/writing-issues-and-mrs.md` for full guidelines.

```bash
glab issue create -t "[Bug]: Login fails on iOS Safari 17 after timeout" -l bug,P1 -m v2.0
glab issue list --label bug --assignee=@me
glab issue close 99
```

### Run and Monitor CI/CD

```bash
glab ci run -b main                   # Trigger pipeline on branch
glab ci status                        # Current pipeline status
glab ci view                          # Interactive pipeline viewer
glab ci retry lint                    # Retry a specific job by name
glab ci lint                          # Validate .gitlab-ci.yml
```

### Create a Release

```bash
glab release create v1.2.0 ./dist/*.tar.gz \
  --notes "Bugfix release" \
  --milestone v1.2.0
```

### Raw API Calls

```bash
# REST
glab api projects/:fullpath/members

# GraphQL
glab api graphql -f query='{ currentUser { username } }'

# With pagination
glab api issues --paginate --output ndjson
```

### Manage Variables

```bash
glab variable list
glab variable set MY_SECRET "s3cret"
glab variable get MY_SECRET
glab variable delete MY_SECRET
```

## All Top-Level Commands

| Command | Purpose |
|---------|---------|
| `glab alias` | Create command shortcuts |
| `glab api` | Make authenticated REST/GraphQL API calls |
| `glab attestation` | Manage attestations |
| `glab auth` | Authenticate to GitLab instances |
| `glab changelog` | Generate changelogs |
| `glab check-update` | Check for glab updates |
| `glab ci` | Manage CI/CD pipelines and jobs |
| `glab cluster` | Manage cluster agents |
| `glab completion` | Generate shell completions (bash/zsh/fish/PowerShell) |
| `glab config` | Set and get glab configuration |
| `glab deploy-key` | Manage deploy keys |
| `glab duo` | Interact with GitLab Duo AI |
| `glab gpg-key` | Manage GPG keys |
| `glab incident` | Manage incidents |
| `glab issue` | Manage issues |
| `glab iteration` | Manage iterations |
| `glab job` | Manage CI/CD jobs |
| `glab label` | Manage labels |
| `glab mcp` | Model Context Protocol server |
| `glab milestone` | Manage milestones |
| `glab mr` | Manage merge requests |
| `glab opentofu` | OpenTofu integration |
| `glab release` | Manage releases |
| `glab repo` | Manage repositories |
| `glab schedule` | Manage pipeline schedules |
| `glab securefile` | Manage secure files |
| `glab snippet` | Manage snippets |
| `glab ssh-key` | Manage SSH keys |
| `glab stack` | Stacked diffs (experimental) |
| `glab token` | Manage personal access tokens |
| `glab user` | Interact with user accounts |
| `glab variable` | Manage CI/CD variables |
| `glab version` | Show glab version |

## Global Flags

| Flag | Description |
|------|-------------|
| `-h, --help` | Show help for any command |
| `-R, --repo OWNER/REPO` | Target a different repository (also accepts `GROUP/NAMESPACE/REPO` or full URL) |
| `-v, --version` | Show glab version |

## Tips

- **Title conventions**: Always use conventional commit prefixes for MR titles (`feat:`, `fix:`, `docs:`, etc.) and descriptive problem-statement titles for issues. See `references/writing-issues-and-mrs.md`.
- **Auto-detection**: glab reads your Git remotes to determine the GitLab project. No need to specify `--repo` when inside the project directory.
- **Multiple instances**: Use `glab auth login` for each GitLab host. glab picks the right credentials based on your remote URL.
- **Output formats**: Many `list` commands accept `-F json` for machine-readable output.
- **Aliases**: Create shortcuts with `glab alias set mrc 'mr create --fill --yes'` then use `glab mrc`.
- **Editor**: Set `EDITOR` or `VISUAL` env vars to control which editor opens for descriptions.
- **Recover**: Use `--recover` on `mr create` and `issue create` to save progress if creation fails.
