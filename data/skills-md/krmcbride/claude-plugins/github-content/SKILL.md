---
name: github-content
description: Fetch GitHub issues, PRs, repo contents, and code using the gh CLI. Use when the user shares GitHub URLs (issues, PRs, repos, source files) or asks about GitHub content. The gh CLI provides complete content that web fetching often misses due to JavaScript rendering.
---

# GitHub Content Fetching

**When to activate:**

- User pastes a GitHub URL (issue, PR, repo, or source file)
- User asks about PR comments, reviews, or discussions
- User wants to browse or search code in a GitHub repository
- User references a GitHub issue or PR by number and repo

**Why use gh CLI instead of web fetching:**

GitHub's web interface relies heavily on JavaScript to load comments, reviews, and discussions. Web fetching often retrieves only partial content. The `gh` CLI accesses the API directly and returns complete data.

## Issues

View an issue with all comments:

```bash
gh issue view <number> --repo owner/repo --comments
```

## Pull Requests

View a PR with comments and review status:

```bash
gh pr view <number> --repo owner/repo --comments
```

View the diff for a PR:

```bash
gh pr diff <number> --repo owner/repo
```

View PR review comments (inline code comments):

```bash
gh api repos/owner/repo/pulls/<number>/comments
```

List files changed in a PR:

```bash
gh pr view <number> --repo owner/repo --json files --jq '.files[].path'
```

## Repository Browsing

List contents of a directory (defaults to root):

```bash
gh api repos/owner/repo/contents/path/to/dir
```

View a specific file's contents:

```bash
gh api repos/owner/repo/contents/path/to/file --jq '.content' | base64 -d
```

Get the full repository tree (all files):

```bash
gh api repos/owner/repo/git/trees/main?recursive=1 --jq '.tree[] | select(.type=="blob") | .path'
```

Replace `main` with the appropriate branch name if needed.

## Code Search

Search for code within a specific repository:

```bash
gh search code "search query" --repo owner/repo
```

Search with language filter:

```bash
gh search code "search query" --repo owner/repo --language python
```

Search with path filter:

```bash
gh search code "search query" --repo owner/repo --path "src/"
```

View search results with more context:

```bash
gh search code "search query" --repo owner/repo --json path,repository,textMatches
```

## Parsing GitHub URLs

Extract owner/repo from common URL patterns:

| URL Pattern                              | Example                         |
| ---------------------------------------- | ------------------------------- |
| `github.com/owner/repo`                  | `github.com/zed-industries/zed` |
| `github.com/owner/repo/issues/123`       | Issue #123 in that repo         |
| `github.com/owner/repo/pull/456`         | PR #456 in that repo            |
| `github.com/owner/repo/blob/branch/path` | Source file at path             |
| `github.com/owner/repo/tree/branch/path` | Directory at path               |

## Tips

- For large outputs, pipe through `head -n 100` or use `--jq` to filter
- Use `--json` flag with `gh pr view` or `gh issue view` for structured data
- For private repos, ensure `gh auth status` shows you're authenticated
- When browsing files, the API returns base64-encoded content that needs decoding
