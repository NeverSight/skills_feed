---
name: quality-gate
description: Quality verification before commits and deployments. Use for quality checks, running tests, checking coverage, validating changes.
allowed-tools: Bash, Read, Grep, Glob
---

# Quality Gate Skill (Bun-Only)

Verify code quality before commits and deployments using **Bun exclusively**.

## ⚠️ CRITICAL: Bun-Only Approach (MANDATORY)

**ALL commands MUST use `bun` - NEVER use `pnpm`, `npm`, or `npx`.**

Why:
- `pnpm run X` spawns: pnpm (node) + command (node) = 2 processes
- `bun run X` spawns: bun only = 1 process (6x lighter than node)
- With `--smol` flag: 54MB vs 343MB memory footprint

```bash
# ❌ NEVER USE THESE
pnpm run typecheck    # Spawns extra node process
npm run test          # Spawns extra node process
npx tsc               # Spawns node

# ✅ ALWAYS USE THESE
bun run typecheck     # Direct bun execution
bun test              # Native bun test runner (17x faster)
bun run lint          # Single process
```

---

## ⚠️ CRITICAL: Serialized Execution (MANDATORY)

**Quality gates MUST run serially, never in parallel.**

Multiple agents running quality gates simultaneously causes system crash:
- 3 agents × 3 commands = resource exhaustion
- Result: Load 500+, kernel_task spike, system freeze

**Use flock to enforce serialization:**

```bash
LOCK_FILE="/tmp/rad-engineer-quality-gate.lock"
```

---

## ⚠️ CRITICAL: JIT Resource Check (MANDATORY)

**BEFORE running any quality gate, check system resources:**

```bash
# Quick inline resource check (embedded in skill)
check_resources() {
    local load kernel_cpu
    load=$(sysctl -n vm.loadavg | awk '{print $2}')
    kernel_cpu=$(ps -Ao %cpu,comm | grep kernel_task | head -1 | awk '{print $1}')
    kernel_cpu=${kernel_cpu:-0}

    if (( $(echo "$load > 8.0" | bc -l) )); then
        echo "BLOCKED: Load too high ($load). Wait 30 seconds."
        return 1
    fi
    if (( $(echo "$kernel_cpu > 40" | bc -l) )); then
        echo "BLOCKED: kernel_task too high (${kernel_cpu}%). Wait 30 seconds."
        return 1
    fi
    return 0
}

# Use before quality gates
check_resources || { sleep 30; check_resources; } || exit 1
```

**Full resource check script:** `.claude/hooks/check-system-resources.sh`

---

## Quality Stages

### Stage 1: Static Analysis

```bash
LOCK="/tmp/rad-engineer-quality-gate.lock"
cd rad-engineer

# Check resources first
.claude/hooks/check-system-resources.sh || { sleep 30; .claude/hooks/check-system-resources.sh; } || exit 1

# TypeScript check - MUST pass with 0 errors (SERIALIZED)
flock -w 300 "$LOCK" bun run typecheck

# Lint check - MUST pass (SERIALIZED)
flock -w 300 "$LOCK" bun run lint
```

**Failure Actions:**

- List all TypeScript errors with file:line
- Separate lint errors into auto-fixable vs manual

### Stage 2: Tests

```bash
LOCK="/tmp/rad-engineer-quality-gate.lock"
cd rad-engineer

# Check resources first
.claude/hooks/check-system-resources.sh || { sleep 30; .claude/hooks/check-system-resources.sh; } || exit 1

# Run all tests (SERIALIZED) - uses --smol from bunfig.toml
flock -w 300 "$LOCK" bun test

# Coverage (run separately when needed - NOT by default)
# flock -w 300 "$LOCK" bun test --coverage
```

**Requirements:**

- All tests must pass
- Coverage ≥ 80% (when explicitly checked)

### Stage 3: Build (if applicable)

```bash
LOCK="/tmp/rad-engineer-quality-gate.lock"
cd rad-engineer

# Verify build succeeds (SERIALIZED)
flock -w 300 "$LOCK" bun run build
```

---

## One-Liner for All Quality Gates

**Use this single command that runs all gates serially with resource check:**

```bash
cd rad-engineer && \
LOCK="/tmp/rad-engineer-quality-gate.lock" && \
( ../.claude/hooks/check-system-resources.sh || { sleep 30; ../.claude/hooks/check-system-resources.sh; } ) && \
flock -w 300 "$LOCK" sh -c 'bun run typecheck && bun run lint && bun test'
```

This ensures:
1. Resources are checked BEFORE spawning processes
2. Only one quality gate runs at a time across ALL agents
3. Typecheck → Lint → Test run sequentially
4. Early exit on first failure
5. All processes use Bun (no node overhead)

---

## Bun Configuration (bunfig.toml)

The project is configured with memory optimization:

```toml
[test]
smol = true              # Reduces memory from 343MB to 54MB
coverage = false         # Disabled by default (run explicitly when needed)
timeout = 300000         # 5 min timeout for integration tests
coverageSkipTestFiles = true
```

---

## Output Format

### All Passing

```
✓ TypeScript: 0 errors
✓ Lint: Clean
✓ Tests: XX passed
✓ Coverage: XX% (if explicitly run)
✓ Build: Success
━━━━━━━━━━━━━━━━━━━━━━
Ready to commit!
```

### Failures

```
✗ TypeScript: X errors
  - src/file.ts:42 - Error message

✗ Tests: X failed
  - test/file.test.ts - Test name
    Expected: X
    Received: Y

━━━━━━━━━━━━━━━━━━━━━━
BLOCKED: Fix issues before commit
```

---

## Quality Standards

| Metric            | Minimum | Target |
| ----------------- | ------- | ------ |
| TypeScript Errors | 0       | 0      |
| Lint Errors       | 0       | 0      |
| Test Pass Rate    | 100%    | 100%   |
| Coverage          | 80%     | 90%    |
| Build             | Pass    | Pass   |

---

## Why Bun-Only Matters

**Process comparison per quality gate run:**

| Command                | Processes Spawned | Memory    |
|------------------------|-------------------|-----------|
| `pnpm run typecheck`   | pnpm + tsc = 2    | ~200MB    |
| `bun run typecheck`    | bun only = 1      | ~54MB     |
| `pnpm run test`        | pnpm + bun = 2    | ~400MB    |
| `bun test`             | bun only = 1      | ~54MB     |

**With 3 agents running quality gates:**

| Approach       | Total Processes | Total Memory |
|----------------|-----------------|--------------|
| pnpm (old)     | 3 × 6 = 18     | ~1.8GB       |
| bun (new)      | 3 × 3 = 9      | ~162MB       |

**Result: 90% memory reduction, 50% fewer processes**

---

## Why Serialization Matters

**Without flock (BROKEN):**
```
Agent 1: bun run typecheck  → runs immediately
Agent 2: bun run typecheck  → runs in PARALLEL!
Agent 3: bun run lint       → runs in PARALLEL!
Result: 3+ heavy processes, potential overload
```

**With flock (CORRECT):**
```
Agent 1: flock ... bun run typecheck  → runs, holds lock
Agent 2: flock ... bun run typecheck  → WAITS for lock
Agent 3: flock ... bun run lint       → WAITS for lock
Result: Only 1 quality gate at a time
```

---

## Quick Reference Card

```
# ALWAYS CHECK RESOURCES FIRST
.claude/hooks/check-system-resources.sh || sleep 30

# ALWAYS USE FLOCK
LOCK="/tmp/rad-engineer-quality-gate.lock"

# ALWAYS USE BUN
flock -w 300 "$LOCK" bun run typecheck   # NOT pnpm
flock -w 300 "$LOCK" bun run lint        # NOT npm
flock -w 300 "$LOCK" bun test            # NOT npx

# ONE-LINER (copy-paste ready)
cd rad-engineer && LOCK="/tmp/rad-engineer-quality-gate.lock" && flock -w 300 "$LOCK" sh -c 'bun run typecheck && bun run lint && bun test'
```

---

**Version**: 3.0.0 (Bun-Only + JIT Resource Check)
**Last Updated**: 2026-01-13
