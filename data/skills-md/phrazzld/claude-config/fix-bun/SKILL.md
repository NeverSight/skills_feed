---
name: fix-bun
description: |
  Run /check-bun, then fix the highest priority Bun issue.
  One fix at a time, verify after each change.
  Invoke for: fix bun migration issue, migrate to bun, bun setup.
---

# /fix-bun

Fix one Bun migration issue at a time. Verify after each change.

## What This Does

1. Run `/check-bun` to get current findings
2. Pick highest priority unfixed issue
3. Apply fix
4. Verify fix worked
5. Report what was fixed

**This is a fixer.** It fixes ONE issue per invocation. Run multiple times for multiple issues.

## Priority Order

Fix issues in this order:

1. **P1: Lockfile cleanup** — Remove conflicting lockfiles
2. **P1: CI migration** — Update GitHub Actions to use Bun
3. **P1: Workspace migration** — Move workspaces to package.json
4. **P2: Script updates** — Convert scripts to use bun run
5. **P2: Test runner** — Enable Bun test runner
6. **P3: Optimizations** — Native SQLite, Bun shell scripts

## Fix Procedures

### Fix: Remove Conflicting Lockfiles

**When**: Both `pnpm-lock.yaml` and `bun.lock` exist

```bash
# Choose one lockfile (keep the target one)
rm pnpm-lock.yaml  # If migrating to Bun
# OR
rm bun.lock bun.lockb  # If staying with pnpm

# Regenerate
bun install  # OR pnpm install
```

**Verify**:
```bash
ls *.lock* | wc -l  # Should be 1
```

### Fix: Update CI to Bun

**When**: GitHub Actions using `pnpm/action-setup`

**File**: `.github/workflows/ci.yml` (or similar)

**Change**:
```yaml
# From:
- uses: pnpm/action-setup@v4
- uses: actions/setup-node@v4
  with:
    cache: 'pnpm'
- run: pnpm install --frozen-lockfile

# To:
- uses: oven-sh/setup-bun@v2
  with:
    bun-version: latest
- run: bun install --frozen-lockfile
```

**Verify**:
```bash
grep -l "oven-sh/setup-bun" .github/workflows/*.yml
```

### Fix: Migrate Workspace Configuration

**When**: `pnpm-workspace.yaml` exists but migrating to Bun

**Step 1**: Add workspaces to `package.json`
```json
{
  "workspaces": ["apps/*", "packages/*"]
}
```

**Step 2**: Remove pnpm workspace file
```bash
rm pnpm-workspace.yaml
```

**Step 3**: Update packageManager field
```json
{
  "packageManager": "bun@1.1.0"
}
```

**Step 4**: Reinstall
```bash
rm -rf node_modules
bun install
```

**Verify**:
```bash
[ ! -f "pnpm-workspace.yaml" ] && echo "✓ Workspace file removed"
grep -q '"workspaces"' package.json && echo "✓ Workspaces in package.json"
bun pm ls  # List workspaces
```

### Fix: Update npm Scripts

**When**: Scripts explicitly use `node` where `bun` would work

**Change in package.json scripts**:
```json
{
  "scripts": {
    // From:
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",

    // To:
    "start": "bun dist/index.js",
    "dev": "bun src/index.ts"
  }
}
```

**Verify**:
```bash
bun run dev  # Should work
bun run start  # Should work
```

### Fix: Enable Bun Test Runner

**When**: Using Jest but Bun test runner would work

**Step 1**: Update test script
```json
{
  "scripts": {
    "test": "bun test"
  }
}
```

**Step 2**: Verify Jest-compatible syntax works
```bash
bun test
```

**Note**: Bun test runner is Jest-compatible. Most tests work without changes.

**If Vitest**: Can use Bun runner:
```json
{
  "scripts": {
    "test": "vitest run"
  }
}
```

**Verify**:
```bash
bun test  # All tests pass
```

### Fix: Update .gitignore

**When**: Migrating lockfile format

```bash
# Add/update in .gitignore
echo "# Bun" >> .gitignore
echo "bun.lockb" >> .gitignore  # Binary lockfile (optional, some prefer text)

# Remove old lockfile from gitignore if needed
sed -i '' '/pnpm-lock.yaml/d' .gitignore
```

**Verify**:
```bash
cat .gitignore | grep -E "bun|pnpm"
```

## Verification Checklist

After any fix:

```bash
# 1. Install works
bun install

# 2. Build works (if applicable)
bun run build

# 3. Tests pass
bun test

# 4. Dev server starts (if applicable)
bun run dev &
sleep 5
curl http://localhost:3000 > /dev/null && echo "✓ Dev server works"
kill %1
```

## Output Format

```markdown
## Fixed: [Issue Title]

**What was wrong**:
[Brief description]

**What was changed**:
- [File]: [Change description]

**Verification**:
- ✓ bun install succeeds
- ✓ bun test passes
- ✓ [Other relevant checks]

**Next issue (if any)**:
Run /fix-bun again to fix: [Next P1/P2 issue]
```

## Related

- `/check-bun` - Audit for Bun compatibility
- `/bun` - Full Bun migration orchestrator
- `/bun-best-practices` - When to use Bun (reference)
