---
name: bun-best-practices
description: |
  When to use Bun, patterns, and anti-patterns. Covers Bun as package manager
  vs runtime, workspace configuration, compatibility considerations.
  Invoke for: bun adoption decision, bun vs pnpm, bun migration planning.
user-invocable: false
---

# Bun Best Practices

Foundational knowledge for Bun adoption decisions. Bun serves two distinct roles—understand when each applies.

## Two Distinct Roles

### Bun as Package Manager

Replaces pnpm/npm/yarn for dependency management:
- `bun install` — Install dependencies (fast, binary lockfile)
- `bun add <pkg>` — Add dependency
- `bun remove <pkg>` — Remove dependency
- `bun --filter <workspace>` — Run in specific workspace

**Key differences from pnpm:**
- Lockfile: `bun.lock` (binary) vs `pnpm-lock.yaml` (YAML)
- Workspaces: Defined in root `package.json`, no separate `pnpm-workspace.yaml`
- Speed: Significantly faster installs due to binary lockfile and caching

### Bun as Runtime

Replaces Node.js for executing JavaScript/TypeScript:
- `bun run script.ts` — Execute TypeScript directly (no tsc)
- `bun test` — Built-in test runner (Jest-compatible API)
- `bun build` — Bundle for production
- Native SQLite, file I/O, HTTP server optimizations

**Key differences from Node.js:**
- TypeScript: Transpilation, not full tsc checking (use `tsc --noEmit` for types)
- APIs: Some Node.js APIs missing or behave differently
- Performance: Often 2-10x faster for I/O-heavy workloads

## Decision Tree: When to Use Bun

```
┌─────────────────────────────────────────────────────────┐
│                   Consider Bun When:                    │
├─────────────────────────────────────────────────────────┤
│ ✅ CLI tools (fast startup, no cold boot)               │
│ ✅ Edge functions (lightweight runtime)                 │
│ ✅ Internal dev tools (team controls deployment)        │
│ ✅ New greenfield projects (no legacy constraints)      │
│ ✅ Scripts/automation (fast execution)                  │
│ ✅ Projects with simple dependency trees                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Prefer pnpm When:                     │
├─────────────────────────────────────────────────────────┤
│ ⚠️ Expo/EAS builds (Node.js required)                  │
│ ⚠️ Vercel serverless (limited Bun support)             │
│ ⚠️ Complex native module dependencies                   │
│ ⚠️ Team unfamiliar with Bun quirks                     │
│ ⚠️ Production apps needing maximum stability           │
│ ⚠️ Projects with extensive Node.js API usage           │
└─────────────────────────────────────────────────────────┘
```

## Hybrid Setup Pattern

Many projects benefit from using both:

```
monorepo/
├── apps/
│   ├── web/          # Next.js app → pnpm (Vercel deployment)
│   └── mobile/       # Expo app → pnpm (EAS requires Node)
├── packages/
│   └── shared/       # Shared utilities → either works
├── tools/
│   └── cli/          # Internal CLI → Bun (fast startup)
└── scripts/          # Build/deploy scripts → Bun (fast execution)
```

**Rule of thumb:**
- External-facing production apps → pnpm (stability)
- Internal tools and scripts → Bun (speed)

## Workspace Configuration

### pnpm (separate file)
```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

### Bun (in package.json)
```json
{
  "workspaces": ["apps/*", "packages/*"]
}
```

**Migration note:** Remove `pnpm-workspace.yaml` when switching to Bun; add `workspaces` to root `package.json`.

## Anti-Patterns

### 1. Assuming Full Node.js Compatibility

**Wrong:**
```typescript
// Assuming all Node.js APIs work identically
import { fork } from 'child_process';
fork('./worker.js'); // May behave differently in Bun
```

**Right:**
```typescript
// Test critical Node.js API usage before migration
// Check: https://bun.sh/docs/runtime/nodejs-apis
```

### 2. Mixing Lockfiles

**Wrong:**
```
project/
├── bun.lock
├── pnpm-lock.yaml    # Both present = confusion
└── package.json
```

**Right:**
```
project/
├── bun.lock          # OR pnpm-lock.yaml, not both
└── package.json
```

### 3. Skipping CI Migration

**Wrong:**
```yaml
# Still using pnpm in CI
- uses: pnpm/action-setup@v4
- run: pnpm install
```

**Right:**
```yaml
# Match local tooling
- uses: oven-sh/setup-bun@v2
- run: bun install
```

### 4. Ignoring Platform Support

**Wrong:**
```typescript
// Deploying to platform that doesn't support Bun runtime
export default async function handler(req, res) {
  // Assumes Bun runtime features
}
```

**Right:**
```typescript
// Verify deployment target supports Bun
// Vercel: experimental Bun runtime flag
// Netlify: Node.js only (as of 2025)
// Fly.io: Full Bun support
```

## Performance Benchmarking

Before migrating, benchmark your specific workflows:

```bash
# Install time comparison
time pnpm install
time bun install

# Script execution comparison
time pnpm run build
time bun run build

# Test runner comparison
time pnpm test
time bun test
```

Only migrate if Bun provides measurable benefit for YOUR project.

## Related References

- `references/workspace-config.md` — Workspace migration details
- `references/compatibility-matrix.md` — Framework/tool compatibility
- `references/ci-cd-patterns.md` — CI/CD configuration patterns
- `references/hybrid-setup.md` — Running Bun + pnpm together

## Related Skills

- `/check-bun` — Audit project for Bun compatibility
- `/fix-bun` — Fix Bun migration issues
- `/bun` — Full Bun migration orchestrator
