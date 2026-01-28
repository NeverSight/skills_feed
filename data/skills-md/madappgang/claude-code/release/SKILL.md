---
name: release
description: Plugin release process for MAG Claude Plugins marketplace. Covers version bumping, marketplace.json updates, git tagging, and common mistakes. Use when releasing new plugin versions or troubleshooting update issues.
---

# Plugin Release Process

Complete guide for releasing new versions of plugins in the MAG Claude Plugins marketplace.

## Critical Understanding

Claude Code plugin discovery works through **TWO** configuration files that **MUST BOTH BE UPDATED**:

1. **`plugins/{plugin-name}/plugin.json`** - The plugin's own version metadata
2. **`.claude-plugin/marketplace.json`** - The marketplace catalog (what users see when browsing)

**Why both?**
- `plugin.json` - Defines the plugin itself (agents, commands, version)
- `marketplace.json` - The "catalog" that Claude Code reads for plugin discovery
- Users run `/plugin marketplace update` which reads `marketplace.json`
- **If you only update `plugin.json`, users won't see the new version!**

---

## Release Checklist

### Step 1: Update Plugin Files

- [ ] `plugins/{plugin-name}/plugin.json` - Update `version` field
- [ ] `plugins/{plugin-name}/agents/*.md` - Add new agents (if any)
- [ ] `plugins/{plugin-name}/commands/*.md` - Update commands (if any)
- [ ] `plugins/{plugin-name}/skills/*/SKILL.md` - Add new skills (if any)

### Step 2: Update Documentation

- [ ] `CHANGELOG.md` - Add new version entry at the top
- [ ] `RELEASES.md` - Add detailed release notes at the top
- [ ] `CLAUDE.md` - Update ALL version references (6+ locations)

### Step 3: ⚠️ **CRITICAL** - Update Marketplace Catalog

**File:** `.claude-plugin/marketplace.json`

Update TWO fields:

1. **Marketplace metadata version** (line ~10):
   ```json
   "metadata": {
     "version": "3.3.0"  // ← Update this
   }
   ```

2. **Specific plugin version** (in plugins array):
   ```json
   "plugins": [
     {
       "name": "frontend",
       "version": "3.3.0",      // ← Update this (CRITICAL!)
       "description": "..."     // ← Update if description changed
     }
   ]
   ```

### Step 4: Commit and Tag

```bash
# Commit all changes
git add -A
git commit -m "feat({plugin}): v{X.Y.Z} - {Feature summary}"

# Create tag (format: plugins/{plugin-name}/v{X.Y.Z})
git tag -a plugins/{plugin}/v{X.Y.Z} -m "..."

# Push
git push origin main
git push origin plugins/{plugin}/v{X.Y.Z}
```

### Step 5: Verify

```bash
/plugin marketplace update mag-claude-plugins
# Should show new version ✅
```

---

## Common Mistakes

### ❌ #1: Forgot to update marketplace.json

**Symptom:** Users still see old version after `/plugin marketplace update`

**Fix:**
```bash
# Update .claude-plugin/marketplace.json
vim .claude-plugin/marketplace.json
# Update plugins[].version field

git add .claude-plugin/marketplace.json
git commit -m "fix(marketplace): Update {plugin} version to v{X.Y.Z}"
git push origin main
```

### ❌ #2: Wrong git tag format

**Wrong:** `frontend-v3.3.0`, `v3.3.0`, `frontend/v3.3.0`
**Correct:** `plugins/frontend/v3.3.0` ✅

### ❌ #3: Inconsistent versions

**Problem:** plugin.json says v3.3.0 but marketplace.json says v3.2.0

**Prevention:** Use checklist, search for old version: `grep -r "3.2.0" .`

---

## Version Numbering

**MAJOR (X.0.0):** Breaking changes (removed agents, changed behavior)
**MINOR (x.Y.0):** New features (new agents/commands, backward compatible)
**PATCH (x.y.Z):** Bug fixes (no new features, backward compatible)

---

## Quick Reference

**Minimal checklist:**

1. ✅ Update `plugins/{plugin}/plugin.json` version
2. ✅ Update `.claude-plugin/marketplace.json` plugin version ⚠️ **CRITICAL**
3. ✅ Update `CHANGELOG.md`, `RELEASES.md`, `CLAUDE.md`
4. ✅ Commit: `git commit -m "feat({plugin}): v{X.Y.Z} - {summary}"`
5. ✅ Tag: `git tag -a plugins/{plugin}/v{X.Y.Z} -m "..."`
6. ✅ Push: `git push origin main && git push origin plugins/{plugin}/v{X.Y.Z}`
7. ✅ Verify: `/plugin marketplace update` shows new version

---

## Example Release

```bash
# 1. Update versions
vim plugins/frontend/plugin.json          # version: "3.3.0"
vim .claude-plugin/marketplace.json       # plugins[0].version: "3.3.0"  ← DON'T FORGET!
vim CHANGELOG.md RELEASES.md CLAUDE.md

# 2. Commit
git add -A
git commit -m "feat(frontend): v3.3.0 - Multi-Model Plan Review"

# 3. Tag
git tag -a plugins/frontend/v3.3.0 -m "Frontend Plugin v3.3.0"

# 4. Push
git push origin main
git push origin plugins/frontend/v3.3.0

# 5. Verify
/plugin marketplace update mag-claude-plugins
# Output: frontend v3.3.0 ✅
```

---

## Troubleshooting

**Q: Users still see old version**
**A:** Check `.claude-plugin/marketplace.json` - version must match `plugin.json`

**Q: Tag already exists**
**A:** `git tag -d {tag}` then `git push origin :{tag}` then recreate

**Q: How to test locally?**
**A:** `/plugin marketplace add /path/to/claude-code`

---

**Related:** [RELEASE_PROCESS.md](../../RELEASE_PROCESS.md) - Full detailed documentation

**Last Updated:** November 13, 2025
