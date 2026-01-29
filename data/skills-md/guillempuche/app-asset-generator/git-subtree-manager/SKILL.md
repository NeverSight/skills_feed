---
name: git-subtree-manager
description: Manages git subtrees for external library references. Use when adding new library sources or updating existing subtrees in docs/.
---

# Git Subtree Manager

Manages git subtrees in the `docs/` directory for AI agents to reference external library source code.

## Current Subtrees

| Library | Directory | Repository | Branch |
|---------|-----------|------------|--------|
| Effect | `docs/effect/` | `https://github.com/Effect-TS/effect.git` | `main` |
| Tamagui | `docs/tamagui/` | `https://github.com/tamagui/tamagui.git` | `master` |
| Better Auth | `docs/better-auth/` | `https://github.com/better-auth/better-auth.git` | `main` |
| Effect Atom | `docs/effect-atom/` | `https://github.com/tim-smart/effect-atom.git` | `main` |

## Adding a New Subtree

### Prerequisites - CRITICAL

**Working directory must be clean.** Git subtree commands will fail or behave unexpectedly with uncommitted changes.

**Before ANY subtree operation:**

1. Check for uncommitted changes:
   ```bash
   git status
   ```

2. If there are staged or unstaged changes, stash them:
   ```bash
   git stash --include-untracked
   ```

3. Verify working directory is clean:
   ```bash
   git status
   # Should show "nothing to commit, working tree clean"
   ```

### Add Command

```bash
git subtree add --prefix=docs/<name> <repo-url> <branch> --squash
```

**Example:**
```bash
git subtree add --prefix=docs/better-auth https://github.com/better-auth/better-auth.git main --squash
```

### Post-Add Updates

After adding a subtree, update these configuration files:

1. **`biome.json`** - Add to `files.includes`:
   ```json
   "!docs/<name>",
   ```

2. **`.github/dependabot.yml`** - Add to `exclude-paths`:
   ```yaml
   - "docs/<name>/**"
   ```

3. **`eslint.config.mjs`** - Add to `ignores`:
   ```javascript
   'docs/<name>/**',
   ```

4. **`AGENTS.md`** - Add entry to the subtrees table

5. **Relevant skills** - Update `.claude/skills/*/SKILL.md` files that should reference the new subtree

### Restore Stashed Changes - DON'T FORGET

After completing subtree operations and config updates:

```bash
git stash pop
```

**Always verify** the user's original changes are restored:
```bash
git status
```

## Updating an Existing Subtree

### Prerequisites - CRITICAL

Same as adding: stash any uncommitted changes first (see above).

To pull latest changes from upstream:

```bash
git subtree pull --prefix=docs/<name> <repo-url> <branch> --squash
```

**Example:**
```bash
git subtree pull --prefix=docs/effect https://github.com/Effect-TS/effect.git main --squash
```

## Configuration Files Checklist

When adding/updating subtrees, ensure these files exclude the subtree directory:

- [ ] `biome.json` - `files.includes` array
- [ ] `.github/dependabot.yml` - `exclude-paths` array
- [ ] `eslint.config.mjs` - `ignores` array
- [ ] `AGENTS.md` - subtrees documentation table
- [ ] Relevant `.claude/skills/*/SKILL.md` files

## Troubleshooting

### "working tree has modifications" Error

This means you forgot to stash changes. **Do not proceed without stashing:**

```bash
# 1. Stash all changes (including untracked files)
git stash --include-untracked

# 2. Run your subtree command
git subtree add/pull ...

# 3. IMPORTANT: Restore the user's changes
git stash pop

# 4. Verify changes are back
git status
```

### Subtree Already Exists

If the directory already exists, remove it first (losing local changes):
```bash
rm -rf docs/<name>
git add docs/<name>
git commit -m "chore: remove docs/<name> for re-add"
```

Then run the add command again.
