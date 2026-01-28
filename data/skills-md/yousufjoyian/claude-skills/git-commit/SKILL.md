---
name: git-commit
description: Smart git commit workflow with staging, message crafting, and safety checks
---

# Git Commit Skill

Smart commit workflow that stages changes, crafts commit messages, and handles edge cases safely.

## Triggers

- "commit"
- "commit changes"
- "git commit"
- "save my changes"
- "commit this"
- "commit and push" (includes automatic push to origin)

## What This Skill Does

1. **Analyzes Changes**: Shows what's modified, staged, and untracked
2. **Smart Staging**: Stages relevant files, excludes secrets
3. **Message Crafting**: Creates conventional commit messages
4. **Safety Checks**: Prevents dangerous operations
5. **Co-authoring**: Adds Claude co-author attribution
6. **Auto-Push**: If "commit and push" trigger used, pushes to origin after commit

## Workflow

### Step 1: Assess Current State

```bash
# Check working directory
git status

# See staged changes
git diff --cached --stat

# See unstaged changes
git diff --stat

# Recent commits for style reference
git log --oneline -5
```

### Step 2: Stage Changes

```bash
# Stage all modified/new files
git add -A

# Or stage specific files
git add <file1> <file2>
```

**Exclude from staging:**
- `.env`, `.env.*` - environment secrets
- `credentials.json`, `*_secret.json` - API keys
- `*.pem`, `*.key` - certificates
- `node_modules/`, `__pycache__/` - dependencies

If user tries to commit secrets, WARN:
> "Found potential secrets in staging: `.env`. Remove with `git reset HEAD .env` before committing."

### Step 3: Craft Commit Message

Use **Conventional Commits** format:

```
<type>(<scope>): <description>

[optional body]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Types:**
| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace |
| `test` | Adding/fixing tests |
| `chore` | Build, config, dependencies |
| `perf` | Performance improvement |

**Examples:**
- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null response from server`
- `refactor(utils): extract date formatting helpers`
- `docs(readme): add installation instructions`

### Step 4: Commit

```bash
git commit -m "$(cat <<'EOF'
feat(scope): short description

Optional longer explanation of what changed and why.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

### Step 5: Verify

```bash
# Confirm commit succeeded
git log -1 --stat

# Check status is clean
git status
```

### Step 6: Push (if "commit and push" trigger)

If the user said "commit and push", automatically push after successful commit:

```bash
git push origin main
```

Report the push result to user.

### Step 7: Visualize Push (if "commit and push" trigger)

**ALWAYS send A2UI visualization after a successful push.** This shows what was committed and pushed.

#### 7a. Discover Active Terminal

```bash
python3 << 'PY'
import json, urllib.request
data = json.loads(urllib.request.urlopen("http://localhost:7690/api/projects").read())
active_proj_id = data.get('activeProjectId')
for p in data.get('projects', []):
    if p.get('id') == active_proj_id:
        term_id = p.get('activeTerminalId')
        for t in p.get('terminals', []):
            if t.get('id') == term_id:
                print(f"A2UI_LOG=/home/yousuf/GoogleDrive/PROJECTS/.triclaude/runtime/terminals/{term_id}/a2ui_input.log")
PY
```

#### 7b. Gather Commit Info

```bash
# Get last commit details
COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=%s)
COMMIT_BODY=$(git log -1 --pretty=%b | head -5)
FILES_CHANGED=$(git diff-tree --no-commit-id --name-only -r HEAD | head -10)
STATS=$(git diff-tree --stat --no-commit-id HEAD | tail -1)
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "local")
```

#### 7c. Generate A2UI Visualization

```bash
cat << 'A2UI_EOF' >> $A2UI_LOG
<!-- A2UI:START -->
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f172a;color:#e2e8f0;font-family:system-ui;font-size:11px;padding:16px}
.header{display:flex;align-items:center;gap:10px;margin-bottom:16px}
.icon{font-size:24px}
h1{font-size:14px;color:#f8fafc}
.badge{background:#166534;color:#4ade80;padding:4px 10px;border-radius:12px;font-size:10px;font-weight:600}
.card{background:#1e293b;border:1px solid #334155;border-radius:8px;padding:12px;margin-bottom:12px}
.label{font-size:9px;color:#64748b;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px}
.hash{font-family:monospace;color:#22d3ee;font-size:12px}
.msg{color:#f8fafc;font-size:12px;margin-top:4px}
.body{color:#94a3b8;font-size:11px;margin-top:6px;white-space:pre-line}
.files{margin-top:8px}
.file{font-family:monospace;font-size:10px;color:#a78bfa;background:#0f172a;padding:4px 8px;border-radius:4px;margin:3px 0;display:block}
.stats{display:flex;gap:16px;margin-top:12px;padding-top:12px;border-top:1px solid #334155}
.stat{text-align:center}
.stat-val{font-size:16px;font-weight:600}
.stat-val.add{color:#4ade80}
.stat-val.del{color:#f87171}
.stat-val.files{color:#60a5fa}
.stat-label{font-size:9px;color:#64748b;margin-top:2px}
.branch{display:inline-flex;align-items:center;gap:4px;background:#1e3a5f;padding:4px 8px;border-radius:4px;font-size:10px;color:#93c5fd}
.ts{color:#64748b;font-size:10px;margin-top:12px;text-align:center}
</style>
</head>
<body>

<div class="header">
<span class="icon">🚀</span>
<h1>Push Successful</h1>
<span class="badge">✓ Pushed</span>
</div>

<div class="card">
<div class="label">Commit</div>
<span class="hash">[COMMIT_HASH]</span>
<div class="msg">[COMMIT_MSG]</div>
<div class="body">[COMMIT_BODY]</div>
</div>

<div class="card">
<div class="label">Files Changed</div>
<div class="files">
[FILES_LIST]
</div>
<div class="stats">
<div class="stat"><div class="stat-val files">[FILE_COUNT]</div><div class="stat-label">files</div></div>
<div class="stat"><div class="stat-val add">+[INSERTIONS]</div><div class="stat-label">insertions</div></div>
<div class="stat"><div class="stat-val del">-[DELETIONS]</div><div class="stat-label">deletions</div></div>
</div>
</div>

<div class="card">
<div class="label">Pushed To</div>
<span class="branch">⎇ [BRANCH]</span> → <span style="color:#94a3b8">[REMOTE]</span>
</div>

<div class="ts">[TIMESTAMP]</div>

<button id="exportBtn" onclick="exportPush()" style="
  width:100%;margin-top:12px;padding:10px;background:#f59e0b;color:#0f172a;
  border:none;border-radius:6px;font-size:11px;font-weight:600;cursor:pointer;
">📥 Export Push Summary</button>

<script>
async function exportPush() {
  const btn = document.getElementById('exportBtn');
  btn.textContent = 'Saving...';
  btn.disabled = true;
  try {
    window.parent.postMessage({
      type: 'save-synopsis',
      projectPath: '[PROJECT_PATH]',
      html: document.documentElement.outerHTML
    }, '*');
    window.addEventListener('message', function handler(e) {
      if (e.data?.type === 'save-synopsis-result') {
        window.removeEventListener('message', handler);
        btn.textContent = e.data.success ? '✓ Saved!' : 'Error';
        btn.style.background = e.data.success ? '#22c55e' : '#ef4444';
        setTimeout(() => {
          btn.textContent = '📥 Export Push Summary';
          btn.style.background = '#f59e0b';
          btn.disabled = false;
        }, 2000);
      }
    });
  } catch (e) {
    btn.textContent = 'Error';
    btn.style.background = '#ef4444';
    setTimeout(() => {
      btn.textContent = '📥 Export Push Summary';
      btn.style.background = '#f59e0b';
      btn.disabled = false;
    }, 2000);
  }
}
</script>

</body>
</html>
<!-- A2UI:END -->
A2UI_EOF
```

**Replace placeholders with actual values:**
- `[COMMIT_HASH]` → Short hash (e.g., `abc1234`)
- `[COMMIT_MSG]` → First line of commit message
- `[COMMIT_BODY]` → Body text (if any)
- `[FILES_LIST]` → Each file as `<span class="file">filename</span>`
- `[FILE_COUNT]` → Number of files changed
- `[INSERTIONS]` → Lines added
- `[DELETIONS]` → Lines deleted
- `[BRANCH]` → Branch name (e.g., `main`)
- `[REMOTE]` → Remote URL or repo name
- `[TIMESTAMP]` → Current time
- `[PROJECT_PATH]` → Absolute path to project (for export)

## Safety Rules

### NEVER Do These:
- `git commit --amend` on pushed commits
- `git push --force` without explicit user request
- Commit files matching secret patterns
- Skip pre-commit hooks (`--no-verify`)
- Commit to main/master without confirmation

### ALWAYS Do These:
- Read files before committing
- Show diff summary before committing
- Use HEREDOC for multi-line messages
- Verify commit succeeded after

## Handling Pre-Commit Hook Failures

If commit is rejected by hooks:

1. **Do NOT use `--no-verify`**
2. Read the hook output to understand the issue
3. Fix the issue (formatting, linting, tests)
4. Create a NEW commit (don't amend)
5. Stage the fixes and commit again

## Amend Rules

Only use `git commit --amend` when ALL conditions are met:
1. User explicitly requested amend
2. HEAD commit was created in this session
3. Commit has NOT been pushed to remote
4. Pre-commit hook auto-modified files that need including

## Example Session

**User**: "commit"

**Assistant**:
```
Let me check the current state...

$ git status
On branch main
Changes not staged for commit:
  modified:   src/App.tsx
  modified:   src/components/Header.tsx
Untracked files:
  src/utils/helpers.ts

$ git diff --stat
 src/App.tsx              | 15 +++++++++------
 src/components/Header.tsx |  8 +++++---

Recent commits:
abc1234 feat(ui): add dark mode toggle
def5678 fix(api): handle timeout errors

Staging all changes...
$ git add -A

Creating commit...
$ git commit -m "feat(components): improve header layout and add helpers

- Refactor App.tsx for cleaner structure
- Update Header component spacing
- Add new utility helpers module

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

[main 9a8b7c6] feat(components): improve header layout and add helpers
 3 files changed, 45 insertions(+), 12 deletions(-)
 create mode 100644 src/utils/helpers.ts

Done! Commit 9a8b7c6 created.
```

## Integration with GitHub Skill

- **"commit and push"** → This skill handles both commit AND push automatically
- **"commit"** alone → Local commit only, use "push" separately if needed
- **"push"** → triggers `github` skill for push-only operations

## Quick Reference

| Command | Action |
|---------|--------|
| "commit" | Full workflow (local only) |
| "commit and push" | Full workflow + push to origin |
| "commit these files" | Commit specific files |
| "amend" | Amend last commit (if safe) |
| "what changed" | Show diff without committing |
| "undo last commit" | `git reset --soft HEAD~1` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "nothing to commit" | Check if files are saved, or already committed |
| Pre-commit hook fails | Fix issues, stage, commit again (no amend) |
| Merge conflict | Resolve conflicts first, then commit |
| Detached HEAD | `git checkout main` first |
| Wrong branch | `git checkout <correct-branch>` |
