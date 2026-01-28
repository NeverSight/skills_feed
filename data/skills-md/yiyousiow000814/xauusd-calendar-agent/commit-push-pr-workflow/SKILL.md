---
name: commit-push-pr-workflow
description: Standardized commit + push + PR workflow. Use when the user asks to commit/push/open PR to ensure checks run, messages are consistent, and pushes/force-pushes are handled safely.
---

# Commit, Push & PR Workflow

Applies to this repo's conventions:
- Do not commit directly to `main`; use a feature branch and a PR.
- PR/issue titles: English. PR bodies/comments: Simplified Chinese by default (unless the request starts with `[EN]`).
- Avoid GitHub CLI `--body` with escaped newlines; prefer `--body-file` or stdin to prevent literal `\\n`.

This skill is written to work well on Windows (PowerShell 5.1+). Bash examples are optional.

## Branch

- Create a feature branch from `main` before making changes:
  - `git fetch origin --prune`
  - `git switch main`
  - `git pull --ff-only`
  - `git switch -c docs/example-change`

## Commit

- Confirm required checks have run for the current change scope before committing (record the exact commands).
- Stage intended files only (prefer `git add -p`).
- Write commit messages using a file (avoid multi-`-m` formatting pitfalls).
- Commit title: `prefix: subject` or `prefix(scope): subject`, English only, ideally <= 50 chars (hard wrap <= 72), no trailing period.
- Include a body for non-trivial changes: blank line after title, wrap at 72 columns, include risk/verification notes.

### Template (PowerShell, UTF-8 without BOM)

```powershell
$msg = @'
fix(scope): concise subject

What changed, why, how (if relevant). Wrap at 72 columns.
Risks/side effects if any.
'@

$path = Join-Path $env:TEMP 'commit_msg.txt'
[System.IO.File]::WriteAllText($path, $msg, [System.Text.UTF8Encoding]::new($false))
git commit -F $path
Remove-Item -Force $path
```

### Template (Bash, optional)

```bash
cat <<'EOF' > /tmp/commit_msg.txt
fix(scope): concise subject

What changed, why, how (if relevant). Wrap at 72 columns.
Risks/side effects if any.
EOF

git commit -F /tmp/commit_msg.txt
rm -f /tmp/commit_msg.txt
```

## Push

- Push only after checks pass.
- Prefer `git push -u origin <branch>` for a new branch.
- Avoid force-push.
  - If history rewrite is required (e.g., credential leak removal), confirm explicitly and expect branch rules (e.g., default-branch non-fast-forward) to block force-push unless temporarily adjusted.
  - If `git-filter-repo` was used: it may remove `origin` automatically; re-add it before pushing.

## Pre-push checklist

- Checks executed (exact commands recorded).
- Commit title/body comply with repo rules.
- User explicitly approved the push (especially for `--force`).

## PR

- Default to a draft PR.

### Option A: GitHub CLI (`gh`)

```powershell
gh --version
gh auth status

@'
Summary:
- ...

Verification:
- ...
'@ | gh pr create --draft --base main --title "docs: ..." --body-file -
```

### Option B: Browser (no extra tools)

- Push the branch, then open:
  - `https://github.com/<owner>/<repo>/pull/new/<branch>`

### Option C: GitHub API (PowerShell, encoding-safe)

- Prefer using an env var token (do not echo it in logs):
  - `$env:GITHUB_TOKEN = '...'`

```powershell
$headers = @{
  Authorization = "token $env:GITHUB_TOKEN"
  'User-Agent' = 'codex-cli'
  Accept = 'application/vnd.github+json'
}

$payload = @{
  title = 'docs: ...'
  head  = '<branch>'
  base  = 'main'
  body  = @"
Summary:
- ...

Verification:
- ...
"@
  draft = $true
} | ConvertTo-Json

$bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
Invoke-RestMethod -Method Post `
  -Uri 'https://api.github.com/repos/<owner>/<repo>/pulls' `
  -Headers $headers `
  -ContentType 'application/json; charset=utf-8' `
  -Body $bytes
```

### Option D: GitHub API via git credential (PowerShell, no env token)

- If `gh` is not installed and you do not have `GITHUB_TOKEN` set, you can reuse the GitHub credential that `git` already has:

```powershell
$cred = "protocol=https`nhost=github.com`n`n" | git credential fill
$token = (($cred | Select-String -Pattern '^password=').Line).Substring(9)

$headers = @{
  Authorization = "token $token"
  'User-Agent'  = 'codex-cli'
  Accept        = 'application/vnd.github+json'
}

$payloadObj = @{
  title = 'docs: ...'
  head  = '<branch>'
  base  = 'main'
  body  = "Summary:`n- ...`n"
  draft = $true
}

$json  = $payloadObj | ConvertTo-Json -Depth 5
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)

Invoke-RestMethod -Method Post `
  -Uri 'https://api.github.com/repos/<owner>/<repo>/pulls' `
  -Headers $headers `
  -ContentType 'application/json; charset=utf-8' `
  -Body $bytes
```

If editing PR bodies via GitHub API from PowerShell:
- Serialize JSON as UTF-8 bytes (no BOM) to preserve Chinese text reliably.
- Avoid printing tokens or Authorization headers.
