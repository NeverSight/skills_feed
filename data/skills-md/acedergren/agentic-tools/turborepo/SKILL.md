---
name: turborepo
version: 3.0.0
license: MIT
description: |
  Turborepo monorepo architecture decisions and anti-patterns. Use when: (1) choosing
  between monorepo vs polyrepo, (2) deciding when to split packages, (3) debugging
  cache misses, (4) setting package boundaries, (5) avoiding circular dependencies.

  NOT for CLI syntax (see turbo --help). Focuses on architectural decisions that
  prevent monorepo sprawl and maintenance nightmares.

  Triggers: turborepo, monorepo, package boundaries, when to split packages, turbo
  cache miss, circular dependency, workspace organization, task dependencies.
metadata:
  version: 2.7.6
---

# Turborepo - Monorepo Architecture Expert

**Assumption**: You know `turbo run build`. This covers architectural decisions.

---

## Before Adopting Turborepo: Strategic Assessment

**Ask yourself these questions BEFORE committing to monorepo:**

### 1. Team & Coordination Analysis
- **Team size**: 1-3 engineers → Polyrepo simpler (monorepo overhead not worth it)
- **Shared code percentage**: <20% → Polyrepo, >50% → Monorepo compelling
- **Coordination pain**: Breaking changes require 3+ repos updated → Monorepo wins
- **Deployment coupling**: Services deploy together → Monorepo, Independently → Polyrepo

### 2. Technical Complexity Assessment
- **Languages**: Pure JS/TS → Turborepo works, Mixed (Go/Python) → Nx or polyrepo
- **Build time**: <5min total across all apps → Overhead not justified yet
- **Cache importance**: Long builds (>2min per package) → Turborepo caching critical
- **CI complexity**: Simple pipeline → Polyrepo easier, Complex (affected detection) → Monorepo

### 3. Maintenance Cost Analysis
- **What breaks with monorepo**: Version conflicts, build order issues, cache debugging, tooling complexity
- **What breaks with polyrepo**: API version hell, coordination overhead, code duplication, cross-repo changes
- **Break-even point**: Monorepo worth it when 3+ apps share 30%+ code + frequent coordination needed

---

## Critical Rule: Package Tasks, Not Root Tasks

**The #1 Turborepo mistake**: Putting task logic in root `package.json`.

```json
// ❌ WRONG - defeats parallelization
// Root package.json
{
  "scripts": {
    "build": "cd apps/web && next build && cd ../api && tsc",
    "lint": "eslint apps/ packages/",
    "test": "vitest"
  }
}

// ✅ CORRECT - parallel execution
// apps/web/package.json
{ "scripts": { "build": "next build", "lint": "eslint .", "test": "vitest" } }

// apps/api/package.json
{ "scripts": { "build": "tsc", "lint": "eslint .", "test": "vitest" } }

// Root package.json - ONLY delegates
{ "scripts": { "build": "turbo run build" } }
```

**Why it breaks**: Turborepo can't parallelize sequential shell commands. Package tasks enable task graph parallelization.

---

## Decision: When to Split a Package

```
Considering splitting code into package?
│
├─ Code used by 1 app only → DON'T split yet
│   └─ Keep in app until second consumer appears
│      WHY: Premature abstraction, overhead > benefit
│
├─ Code used by 2+ apps → MAYBE split
│   ├─ Stable API (rarely changes) → Split
│   ├─ Unstable (changes every sprint) → DON'T split yet
│   └─ Mixed team ownership → DON'T split (use import path instead)
│      WHY: Shared packages need stable APIs + clear owners
│
├─ Publishing to npm → MUST split
│   └─ External packages require independent versioning
│
└─ CI builds too slow (> 10min) → Split strategically
    └─ Split by stability (core vs features), not by domain
       WHY: Stable packages cache, unstable packages rebuild
```

**Anti-pattern**: Creating packages for "clean architecture" without consumers. Packages add overhead (build, test, version).

---

## Anti-Patterns

### ❌ #1: Circular Dependencies
**Problem**: Packages depend on each other, breaks task graph

```
packages/ui → imports from packages/utils
packages/utils → imports from packages/ui  // ❌ Circular
```

**Detection**:
```bash
turbo run build  # Fails with: "Could not resolve dependency graph"
```

**Fix**: Extract shared code to third package
```
packages/ui → packages/shared
packages/utils → packages/shared
```

**Why it breaks**: Turborepo builds dependencies first (topological sort). Circular deps = no valid build order.

**Why this is deceptively hard to debug**: Error message "Could not resolve dependency graph" doesn't mention the word "circular"—just lists package names. With 10+ packages, takes 15-20 minutes to manually trace imports and realize two packages reference each other. The import chain might be indirect (A → B → C → A), making it even harder to spot. Developers waste time checking turbo.json config and workspace setup before realizing it's an import cycle issue, not a Turborepo configuration problem.

### ❌ #2: Overly Granular Packages
**Problem**: 50 micro-packages, every import crosses package boundary

```
packages/button/
packages/input/
packages/checkbox/
packages/radio/
packages/select/
// ... 45 more single-component packages
```

**Symptoms**:
- Every change touches 5+ packages
- 10+ version bumps per feature
- `pnpm workspace:*` version hell

**Fix**: Group by stability/purpose
```
packages/ui/           # All components (changes often)
packages/ui-primitives/ # Headless components (stable)
packages/icons/        # Generated SVGs (rarely changes)
```

**Decision rule**: Package boundary = different change frequency

**Why this is deceptively hard to debug**: Takes weeks or months to discover the problem—not immediate. First feature seems fine (update 3 packages, publish 3 versions). Second feature touches 5 packages. Third feature hits 10 packages and you're managing workspace version conflicts for 2 hours. The pain accumulates slowly: CI gets slower (building 50 packages), version bumps become tedious (changesets for 10+ packages), developers avoid refactoring because it crosses too many boundaries. Only after 3-6 months do you realize the granularity was wrong, but by then you have 50 packages and merging them requires major migration work.

### ❌ #3: Missing Task Dependencies
**Problem**: Tests run before build completes

```json
// turbo.json
{
  "tasks": {
    "build": { "outputs": ["dist/**"] },
    "test": {}  // ❌ No dependsOn
  }
}

// Result: tests import from dist/ before it exists
```

**Fix**: Explicit dependencies
```json
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "test": { "dependsOn": ["build"] }  // ✅ Build first
  }
}
```

**Why**: `^build` = build dependencies first. `build` = build this package first.

**Why this is deceptively hard to debug**: Tests pass locally (you ran `build` manually first), fail in CI with cryptic errors like "Cannot find module './dist/index.js'" or import errors. The race condition is timing-dependent—sometimes tests start before build finishes, sometimes they start after (especially with caching). Developers waste 10-15 minutes checking import paths, package.json exports, and tsconfig before realizing it's a task ordering issue. The error message points to the symptom (missing file) not the cause (missing dependency declaration).

### ❌ #4: Cache Miss Hell
**Problem**: Cache never hits, rebuilds everything

```json
// turbo.json
{
  "tasks": {
    "build": {
      "inputs": ["src/**"]  // ❌ Too broad
    }
  }
}

// Any file change (even comments) = cache miss
```

**Fix**: Exclude non-code files
```json
{
  "tasks": {
    "build": {
      "inputs": [
        "src/**/*.{ts,tsx}",  // ✅ Only source files
        "!src/**/*.test.ts"   // Exclude tests
      ]
    }
  }
}
```

**Debug cache**:
```bash
turbo run build --dry --graph  # Shows why cache missed
```

**Why this is deceptively hard to debug**: Cache initially works (first few builds hit), then mysteriously stops. Every run shows "cache miss" but you can't tell why. The problem: you added a README.md to src/, touched a comment, or updated a test file—non-code changes that shouldn't trigger rebuild but do because inputs include `src/**`. Developers waste 20-30 minutes checking remote cache credentials, clearing local cache, restarting daemon before realizing the input glob is too broad. The `--dry --graph` flag shows hash changed but doesn't clearly indicate WHICH file caused it (need to diff file lists manually).

---

## Decision: Monorepo vs Polyrepo

```
Starting new project?
│
├─ Single team, single product → Polyrepo (simpler)
│   └─ One repo per service/app
│      WHY: Monorepo overhead not worth it for small teams
│
├─ Shared UI library → Monorepo
│   └─ Library + consumer apps in same repo
│      WHY: Develop library + test in consumers simultaneously
│
├─ Microservices (different languages) → Polyrepo
│   └─ Go service, Python service, Node service
│      WHY: Turborepo is JS/TS focused, polyrepo simpler
│
└─ Multiple teams, shared code → Monorepo
    └─ Need atomic changes across boundaries
       WHY: One PR changes API + all consumers
```

**Real-world**: Most projects should start polyrepo, migrate to monorepo when pain > tooling cost.

---

## Package Boundary Patterns

### Pattern 1: By Stability
```
packages/
  core/         # Changes quarterly (semantic versioning)
  features/     # Changes weekly (workspace protocol)
  utils/        # Changes monthly
```

**Benefit**: Stable packages cache longer, ship to npm independently.

### Pattern 2: By Consumer
```
packages/
  public-api/   # External consumers
  internal/     # Internal apps only
```

**Benefit**: Clear API surface, different versioning strategies.

### Pattern 3: By Team
```
packages/
  team-platform/
  team-growth/
  team-infra/
```

**Warning**: Only works if teams rarely share code. Otherwise creates silos.

---

## Turborepo vs Alternatives

```
Choose Turborepo when:
✅ JS/TS monorepo (React, Next.js, Node)
✅ Need remote caching (Vercel, self-hosted)
✅ Task graph parallelization important
✅ Using pnpm workspaces or npm workspaces

Choose Nx when:
✅ Need project graph visualization
✅ Polyglot (JS + Python + Go)
✅ Want opinionated project structure
✅ Need plugin ecosystem

Choose Rush when:
✅ Very large monorepo (100+ packages)
✅ Need phantom dependencies detection
✅ Publishing to npm is primary use case
```

**Real-world**: Turborepo wins for Next.js/React apps, Nx wins for complex polyglot, Rush wins for library publishers.

---

## Debugging Commands

### Visualize task graph
```bash
turbo run build --dry --graph=graph.html
# Opens browser with task dependency visualization
```

### Find cache misses
```bash
turbo run build --dry=json | jq '.tasks[] | select(.cache.status == "MISS")'
```

### Check package dependency order
```bash
turbo run build --dry --graph | grep "→"
```

### Test cache without running tasks
```bash
turbo run build --dry  # Shows what would run
```

---

## Error Recovery Procedures

### When Cache Never Hits (Cache Miss Hell)
**Recovery steps**:
1. **Diagnose**: Run `turbo run build --dry=json | jq '.tasks[0].hash'` to see current hash
2. **Identify culprit**: Add `--log-order=grouped` to see which files changed the hash
3. **Fix inputs**: Narrow glob patterns to exclude non-code files (tests, docs, configs)
4. **Fallback**: If still missing, disable cache for that task temporarily: `"cache": false` in turbo.json, then debug without cache pressure

### When Circular Dependency Error Occurs
**Recovery steps**:
1. **Visualize**: Run `turbo run build --dry --graph=graph.html` and open in browser
2. **Trace cycle**: Look for packages that appear in each other's dependency chains (A → B → ... → A)
3. **Extract shared**: Create new package (e.g., `packages/shared`) and move common code there
4. **Fallback**: If cycle is complex (3+ packages), use dependency graph tool like `madge` to visualize: `npx madge --circular --extensions ts,tsx packages/`

### When Tests Fail in CI But Pass Locally
**Recovery steps**:
1. **Check task order**: Run `turbo run test --dry --graph` to see if build runs before test
2. **Add dependencies**: Add `"dependsOn": ["build"]` to test task in turbo.json
3. **Verify**: Run `turbo run test --force` (bypass cache) to confirm tests pass when build runs first
4. **Fallback**: If still failing, check for race condition in parallel tests: add `"cache": false` to test task temporarily and see if issue persists

### When Overly Granular Packages Cause Version Hell
**Recovery steps**:
1. **Audit changes**: Run `git log --oneline --since="1 month ago" -- packages/` to count package version bumps
2. **Identify clusters**: Look for packages that always change together (5+ times in last month)
3. **Merge packages**: Combine related packages into single package with internal structure
4. **Fallback**: If merging is too risky, use `workspace:*` protocol to auto-link versions and reduce manual bumps

---

## When to Load Full Reference

**MANDATORY - READ ENTIRE FILE**: `references/cli-options.md` when:
- Encountering 3+ unknown CLI flags in error messages or commands
- Need advanced filtering across 10+ packages (--filter patterns, --affected usage)
- Setting up 5+ complex task pipeline options (--concurrency, --continue, --output-logs)
- Troubleshooting CLI behavior that's not covered in this core framework

**MANDATORY - READ ENTIRE FILE**: `references/remote-cache-setup.md` when:
- Setting up remote cache for team with 3+ developers
- Debugging 5+ cache authentication or connection errors
- Configuring self-hosted remote cache with custom storage backend
- Implementing cache security policies (signature verification, access control)

**Do NOT load references** for:
- Basic architecture decisions (use this core framework)
- Single cache miss debugging (use Error Recovery section above)
- Deciding whether to adopt monorepo (use Strategic Assessment section)

---

## Resources

- **Official Docs**: https://turbo.build/repo/docs (for CLI reference)
- **This Skill**: Architecture decisions, anti-patterns, package boundaries
