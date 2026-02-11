---
name: github-cli
description: GitHub CLI (gh) reference for repositories, issues, pull requests, Actions, projects, releases, gists, codespaces, and GitHub operations from the command line.
metadata:
  author: hairy
  version: "2026.2.6"
  source: Generated from sources/github (awesome-copilot), scripts at https://github.com/antfu/skills
---

# GitHub CLI (gh)

Use this skill when working with GitHub from the command line: repos, issues, PRs, Actions, projects, releases, gists, codespaces, search, secrets, and API. Content is based on gh 2.85.0 (January 2026).

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| CLI Structure | Full command tree for discovery | [core-cli-structure](references/core-cli-structure.md) |
| Install & Verify | Install on macOS, Linux, Windows; verify | [core-install](references/core-install.md) |
| Auth & Config | Login, token, config, env vars, browse, global flags, JSON/template output | [core-auth-config](references/core-auth-config.md) |
| Repos, Issues, PRs | Create/list/view/edit repo, issue, PR; merge, review, checkout | [core-repo-issues-prs](references/core-repo-issues-prs.md) |
| Repo Extras | Autolinks, deploy keys, gitignore/license, rename, archive | [core-repo-extras](references/core-repo-extras.md) |
| Issue & PR Advanced | Status, pin, lock, transfer, delete, review types, merge options | [core-issue-pr-advanced](references/core-issue-pr-advanced.md) |

## Features

### Actions & Secrets

| Topic | Description | Reference |
|-------|-------------|-----------|
| Runs, Workflows, Cache | List/watch/rerun/delete runs, run workflows, manage caches | [features-actions-secrets](references/features-actions-secrets.md) |
| Secrets & Variables | Repository, environment, org secrets/variables | [features-actions-secrets](references/features-actions-secrets.md) |

### Projects, Releases & More

| Topic | Description | Reference |
|-------|-------------|-----------|
| Projects | Fields, items, link/unlink, copy, mark-template | [features-projects-releases-gists](references/features-projects-releases-gists.md) |
| Releases | Create, upload, download, verify, verify-asset | [features-projects-releases-gists](references/features-projects-releases-gists.md) |
| Gists & Codespaces | Gist rename/multi-file; codespace cp, jupyter, logs, ports | [features-projects-releases-gists](references/features-projects-releases-gists.md) |
| Orgs | List, view, JSON output | [features-projects-releases-gists](references/features-projects-releases-gists.md) |
| Preview & Agent Tasks | gh preview, gh agent-task | [features-preview-agent-task](references/features-preview-agent-task.md) |
| Search, API, Misc | Search, labels, SSH/GPG keys, gh api, aliases, extensions, rulesets, attestation | [features-search-api-misc](references/features-search-api-misc.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Environment Setup | Shell completion, aliases, git credential helper | [best-practices-workflows](references/best-practices-workflows.md) |
| Workflows & Practices | Automation tips, bulk ops, repo setup, CI/CD, fork sync, help | [best-practices-workflows](references/best-practices-workflows.md) |

## Quick Tips

- Use `GH_TOKEN` and `GH_REPO` for non-interactive use.
- Prefer `--json` + `--jq` for scripting.
- Use `gh repo set-default owner/repo` to avoid repeating `--repo`.
