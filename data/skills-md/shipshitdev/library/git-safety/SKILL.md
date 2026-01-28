---
name: git-safety
description: Scan git history for sensitive files, clean leaked credentials, and set up prevention measures. Use when asked to "check for secrets", "scan git history", "remove .env from history", "secure my repo", or "clean sensitive files".
---

# Git Safety Skill

Comprehensive security scanning, cleaning, and prevention for git repositories.

## CRITICAL WARNING

**Removing secrets from git history does NOT make them safe!**

Even after cleaning git history:

- GitHub is scraped by bots within seconds of a push
- Archive services may have captured snapshots
- Forks retain the original history
- CI/CD logs may contain the values

**ALWAYS rotate leaked credentials immediately.** Cleaning history is NOT enough.

## Modes of Operation

### 1. `/git-safety scan` - Detect Sensitive Files

Scan repository for sensitive files in current state and git history.

### 2. `/git-safety clean` - Remove from History

Remove sensitive files using git-filter-repo or BFG.

### 3. `/git-safety prevent` - Set Up Prevention

Configure .gitignore and pre-commit hooks.

### 4. `/git-safety full` - Complete Audit

Run all three operations in sequence.

## Sensitive File Patterns

```
.env, .env.*, credentials.json, service-account*.json
*.pem, *.key, id_rsa*, secrets.*, .npmrc, *.secret
```

## Quick Commands

**Scan for sensitive files in history:**

```bash
git log --all --pretty=format: --name-only --diff-filter=A | sort -u | grep -iE 'env|secret|credential|key'
```

**Remove .env from all history:**

```bash
git filter-repo --path .env --invert-paths --force
git push origin --force --all
```

**Add to .gitignore:**

```bash
echo -e "\n.env\n.env.*\n*.pem\n*.key\ncredentials.json" >> .gitignore
```

## Emergency Response

If you've leaked credentials:

1. **IMMEDIATELY rotate the credential**
2. Check access logs
3. Run `/git-safety clean`
4. Force push cleaned history
5. Notify team to re-clone
6. Update .gitignore
7. Set up pre-commit hooks

---

**For complete scan commands, cleaning process with git-filter-repo/BFG, pre-commit hook setup, .gitignore templates, platform-specific guidance, and detailed emergency checklist, see:** `references/full-guide.md`
