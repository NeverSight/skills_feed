---
name: github-pr-edit
description: Edit GitHub PR title/body (and optionally comments) reliably on Windows. Use when asked to update PR metadata or when GitHub API returns 404 due to missing auth (private repos often return 404 when unauthenticated).
---

# GitHub PR Edit (Title/Body/Comments)

Edit PR title/body/comments on Windows. Use `gh` when available; otherwise use the GitHub REST API.

## Before You Start

- Identify:
  - `owner` and `repo` (e.g. `yiyousiow000814/XAUUSD-Calendar-Agent`)
  - PR number (e.g. `111`)
- If using `gh`, confirm it is available and authenticated:

```powershell
gh --version
gh auth status
```

- If the repo is private, **unauthenticated GitHub API requests often return `404 Not Found`**. Treat `404` as “likely unauthorized” unless you are sure the repo/PR does not exist.

## Option A (Preferred): GitHub CLI (`gh`)

If `gh` is installed and authenticated:

```powershell
# Update title and body (use stdin/body-file to avoid literal \n issues)
@'
<markdown body>
'@ | gh pr edit 111 --title "chore: ..." --body-file -
```

Add a comment:

```powershell
@'
Summary:
- ...
'@ | gh pr comment 111 --body-file -
```

## Option B: GitHub REST API (PowerShell, no `gh`)

### 1) Get an auth token (do not print it)

Preferred sources (pick the first available):

1. `$env:GITHUB_TOKEN` or `$env:GH_TOKEN`
2. Reuse the credential Git already has (works if you previously authenticated with a PAT):

```powershell
$cred = "protocol=https`nhost=github.com`n`n" | git credential fill
$token = (($cred | Select-String -Pattern '^password=').Line).Substring(9)
```

Do not `Write-Host $token`, do not log headers.

### 2) Build headers (minimal)

```powershell
$headers = @{
  Authorization = "token $token"
  'User-Agent'  = 'codex-cli'
  Accept        = 'application/vnd.github+json'
}
```

### 3) Sanity check auth (useful when you see 404)

```powershell
Invoke-RestMethod -Method Get -Uri "https://api.github.com/repos/<owner>/<repo>" -Headers $headers |
  Select-Object full_name, private
```

If this fails with `404`, your token likely lacks access.

### 4) Update PR title/body

Use UTF-8 bytes for reliable encoding (Chinese text, punctuation).

```powershell
$payload = @{
  title = 'chore: ...'
  body  = @"
Summary:
- ...
"@
} | ConvertTo-Json -Depth 5

$bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)

Invoke-RestMethod -Method Patch `
  -Uri "https://api.github.com/repos/<owner>/<repo>/pulls/<number>" `
  -Headers $headers `
  -ContentType 'application/json; charset=utf-8' `
  -Body $bytes
```

### 5) Add a PR comment (optional)

PR comments are issue comments:

```powershell
$payload = @{ body = "Summary:`n- ..." } | ConvertTo-Json -Depth 5
$bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)

Invoke-RestMethod -Method Post `
  -Uri "https://api.github.com/repos/<owner>/<repo>/issues/<number>/comments" `
  -Headers $headers `
  -ContentType 'application/json; charset=utf-8' `
  -Body $bytes
```

## Deterministic Helper Script (Recommended)

Use the bundled script for fewer quoting/encoding mistakes:
- `.codex/skills/github-pr-edit/scripts/patch_pr.ps1`

