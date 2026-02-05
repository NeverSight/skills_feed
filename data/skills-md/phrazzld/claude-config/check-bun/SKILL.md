---
name: check-bun
description: |
  Audit project for Bun compatibility and adoption opportunities.
  Outputs structured findings. Use fix-bun to fix issues.
  Invoke for: bun audit, bun compatibility check, bun migration assessment.
---

# /check-bun

Audit project for Bun compatibility. Output findings as structured report.

## What This Does

1. Check current package manager setup
2. Identify compatibility blockers
3. Assess migration opportunities
4. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/fix-bun` to fix issues or `/bun` for full migration.

## Process

### 1. Current State Assessment

```bash
# What package manager is in use?
[ -f "pnpm-lock.yaml" ] && echo "Current: pnpm"
[ -f "bun.lock" ] || [ -f "bun.lockb" ] && echo "Current: bun"
[ -f "package-lock.json" ] && echo "Current: npm"
[ -f "yarn.lock" ] && echo "Current: yarn"

# Check packageManager field
grep -o '"packageManager":.*' package.json 2>/dev/null || echo "No packageManager field"

# Multiple lockfiles?
ls -la *.lock* 2>/dev/null | wc -l
```

### 2. Deployment Target Check

```bash
# Vercel?
[ -f "vercel.json" ] && echo "Vercel deployment detected"

# Expo/EAS?
[ -f "app.json" ] && grep -q "expo" app.json && echo "Expo detected - Bun NOT supported"

# Netlify?
[ -f "netlify.toml" ] && echo "Netlify deployment - limited Bun support"

# Fly.io?
[ -f "fly.toml" ] && echo "Fly.io deployment - full Bun support"
```

### 3. Dependency Compatibility Check

```bash
# Native modules that may have issues
grep -E "sharp|bcrypt|canvas|puppeteer|better-sqlite3" package.json 2>/dev/null

# Check for known problematic packages
grep -E "node-gyp|node-pre-gyp" package-lock.json pnpm-lock.yaml 2>/dev/null | head -5
```

### 4. CI Configuration Check

```bash
# GitHub Actions using pnpm?
grep -l "pnpm/action-setup" .github/workflows/*.yml 2>/dev/null

# Should be using oven-sh/setup-bun?
grep -l "oven-sh/setup-bun" .github/workflows/*.yml 2>/dev/null
```

### 5. Workspace Configuration Check

```bash
# pnpm workspace file exists?
[ -f "pnpm-workspace.yaml" ] && echo "pnpm-workspace.yaml found"

# Workspaces in package.json?
grep -q '"workspaces"' package.json && echo "workspaces field in package.json"
```

### 6. Node.js API Usage Check

```bash
# Heavy Node.js API usage that may differ in Bun
grep -rE "child_process|cluster|vm|dgram" --include="*.ts" --include="*.js" src/ 2>/dev/null | head -10

# Worker threads
grep -rE "worker_threads" --include="*.ts" --include="*.js" src/ 2>/dev/null | head -5
```

## Output Format

```markdown
## Bun Compatibility Audit

### P0: Blockers (Cannot migrate)
- Expo/EAS detected - Bun runtime not supported by EAS Build
- Native module `canvas` may not work with Bun

### P1: Essential (Must fix before migration)
- Mixed lockfiles: both pnpm-lock.yaml and bun.lock present
- CI using pnpm/action-setup, needs oven-sh/setup-bun
- pnpm-workspace.yaml needs migration to package.json workspaces

### P2: Important (Should address)
- Scripts using `node` instead of `bun` for execution
- Test runner is Jest, consider Bun test runner
- No frozen-lockfile in CI

### P3: Nice to Have (Optimization opportunities)
- Could use Bun's native SQLite instead of better-sqlite3
- Build scripts could use Bun shell

## Summary
- Current: pnpm
- Deployment: Vercel (partial Bun support)
- Blockers: 0
- Migration complexity: LOW/MEDIUM/HIGH
- Recommendation: [PROCEED/HYBRID/SKIP]
```

## Priority Mapping

| Finding | Priority |
|---------|----------|
| Expo/EAS deployment | P0 (blocker) |
| Native modules incompatible | P0 (blocker) |
| Mixed lockfiles | P1 |
| CI not updated | P1 |
| Workspace config needs migration | P1 |
| Scripts using `node` | P2 |
| Test runner not optimized | P2 |
| Missed optimization opportunities | P3 |

## Migration Complexity Assessment

**LOW**: No blockers, simple dependencies, flexible deployment
- Few/no native modules
- Deployment platform supports Bun
- No pnpm-specific features used

**MEDIUM**: Some work required, compatible target
- Native modules that work with Bun
- CI needs updating
- Workspace config needs migration

**HIGH**: Significant challenges or partial adoption
- Platform limitations (Vercel serverless, etc.)
- Heavy native module usage
- Complex monorepo setup

## Recommendation Matrix

| Blockers | Deployment | Complexity | Recommendation |
|----------|------------|------------|----------------|
| 0 | Supports Bun | LOW | PROCEED |
| 0 | Supports Bun | MEDIUM | PROCEED with care |
| 0 | Partial support | Any | HYBRID setup |
| Any | Any | HIGH | SKIP or HYBRID |
| >0 | Doesn't support | Any | SKIP |

## Related

- `/fix-bun` - Fix Bun migration issues one at a time
- `/bun` - Full Bun migration orchestrator
- `/bun-best-practices` - When to use Bun (reference)
