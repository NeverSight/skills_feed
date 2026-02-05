---
name: pr-screenshot
description: Add screenshots to a PR using browser automation. Captures UI, saves to docs/screenshot/, and updates PR body with GitHub CDN URLs.
license: MIT
metadata:
  author: madeyexz
  version: "1.0.0"
---

# PR Screenshot Skill

Add screenshots to a pull request using browser automation and GitHub CDN.

## Arguments

- `$ARGUMENTS` - PR number and optional description of what to screenshot

## Execution Steps

### 1. Parse Arguments & Get Repo Info

```bash
# Get current repo info (works in any repo)
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Get PR info
gh pr view <PR_NUMBER> --json headRefName,title,body

# Checkout the PR branch
git checkout <branch-name>
```

### 2. Start Dev Server

```bash
pnpm dev &
sleep 5
# Note the port (usually 3000 or 3001 if 3000 is in use)
```

### 3. Take Screenshots with agent-browser

```bash
# Open the page
agent-browser open "http://localhost:3000/path/to/feature"

# Wait for page load
sleep 2

# Get interactive elements
agent-browser snapshot -i

# Login if needed (check CLAUDE.md for credentials)
agent-browser fill @e1 "email"
agent-browser fill @e2 "password"
agent-browser click @e3

# Navigate to the feature
agent-browser click @eN

# For expandable sections, use JavaScript
agent-browser eval "document.querySelector('details summary').click()"

# Scroll to show relevant content
agent-browser eval "document.querySelector('selector').scrollIntoView({ block: 'start' })"

# Take screenshot
agent-browser screenshot docs/screenshot/feature-name.png
```

### 4. Save Screenshots

All screenshots must be saved to `docs/screenshot/`:

```bash
mkdir -p docs/screenshot
# Screenshot directly to: docs/screenshot/<descriptive-name>.png
```

Naming convention:
- `feature-overview.png` - main view
- `feature-expanded.png` - expanded/detailed view
- `feature-empty.png` - empty state
- `feature-loading.png` - loading state

### 5. Commit & Push

```bash
git add docs/screenshot/
git commit -m "$(cat <<'EOF'
docs: add screenshots for [feature]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
git push
```

### 6. Update PR Body with Screenshots

**IMPORTANT**: Use GitHub CDN URL format with `?raw=true`:

```
https://github.com/<REPO>/blob/<BRANCH>/docs/screenshot/<filename>.png?raw=true
```

Where `<REPO>` is the `nameWithOwner` from step 1 (e.g., `owner/repo-name`).

Update PR body:

```bash
gh pr edit <PR_NUMBER> --body "$(cat <<'EOF'
# PR Title

## Summary
[existing summary]

## Screenshots

### Feature Overview
![Overview](https://github.com/<REPO>/blob/<BRANCH>/docs/screenshot/feature-overview.png?raw=true)

### Expanded View
![Expanded](https://github.com/<REPO>/blob/<BRANCH>/docs/screenshot/feature-expanded.png?raw=true)

[rest of PR body]
EOF
)"
```

### 7. Clean Up

```bash
agent-browser close
pkill -f "next dev" || true
git checkout main
```

## GitHub CDN URL Format

Always use this exact format for images to render in GitHub:

```
https://github.com/OWNER/REPO/blob/BRANCH/path/to/image.png?raw=true
```

- **OWNER/REPO**: Get from `gh repo view --json nameWithOwner -q .nameWithOwner`
- **BRANCH**: The PR branch name (get from `gh pr view`)
- **?raw=true**: Required suffix for images to display

## Authentication

If the app requires login, check the project's `CLAUDE.md` for test credentials.

## Tips

- Take multiple screenshots showing different states
- Use `agent-browser tab list` to see all open tabs
- Use `agent-browser tab N` to switch tabs
- For elements not in snapshot, use CSS selectors: `agent-browser click "button.submit"`
- Scroll with: `agent-browser scroll down 500`
