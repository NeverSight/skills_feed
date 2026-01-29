---
name: deploy
description: Build the project, commit all changes, and deploy directly to main. Use when deploying changes to production.
allowed-tools: Bash, Read, Glob, Write, Edit
---

# Deploy to Main

Automates the complete deployment workflow for pushing changes to production.

## Workflow

1. **Build**: Run `npm run build` to ensure no compilation errors
2. **Status Check**: Check git status for uncommitted changes
3. **Commit**: Commit changes with a descriptive message
4. **Deploy**: Push directly to main to trigger production deployment
5. **Confirm**: Provide deployment status

## Commands

```bash
# Build project
npm run build

# Check status
git status
git log --oneline -3

# Commit (if changes exist)
git add -A
git commit -m "chore: <descriptive message>"

# Push directly to main
git push origin main
```

## When to Use

- "deploy to main"
- "push changes to production"
- "deploy these changes"
- "/deploy"
