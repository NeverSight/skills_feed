---
name: update-dependencies
description: Smart dependency updates across ecosystems (npm/bun/pnpm, uv/poetry, cargo). Use when upgrading dependencies, fixing vulnerabilities, or performing proactive maintenance. Supports intelligent batching, risk assessment, and outcome tracking for continuous improvement.
license: Apache-2.0
---

# Dependency Updater

Smart dependency management with security-first prioritization, intelligent batching, and learning from outcomes.

## Ecosystem Detection

First, detect the project's ecosystem:

```bash
# Check for lockfiles (in priority order)
ls bun.lock bun.lockb pnpm-lock.yaml package-lock.json uv.lock poetry.lock Cargo.lock 2>/dev/null | head -1
```

| Lockfile | Ecosystem | Reference |
|----------|-----------|-----------|
| `bun.lock` / `bun.lockb` | npm (bun) | [npm.md](references/ecosystems/npm.md) |
| `pnpm-lock.yaml` | npm (pnpm) | [npm.md](references/ecosystems/npm.md) |
| `package-lock.json` | npm | [npm.md](references/ecosystems/npm.md) |
| `uv.lock` | Python (uv) | [python.md](references/ecosystems/python.md) |
| `poetry.lock` | Python (poetry) | [python.md](references/ecosystems/python.md) |
| `Cargo.lock` | Rust | [cargo.md](references/ecosystems/cargo.md) |

Load the appropriate ecosystem reference for detailed commands.

---

## Workflow

### Phase 1: Security Audit

Run security check first. Security issues always take priority.

See ecosystem reference for specific audit command.

Categorize by severity:
- **Critical/High**: Fix immediately, own PR
- **Moderate/Low**: Batch with related updates

### Phase 2: Outdated Analysis

Check for outdated dependencies.

Categorize by update type:
- **Patch** (x.y.Z): Usually safe, batch together
- **Minor** (x.Y.z): Review changelog, usually safe
- **Major** (X.y.z): Individual review required

### Phase 3: Check History

Before major updates, check if we've updated this package before:

```bash
grep "<package-name>" ~/.claude/skills/update-dependencies/data/outcomes.jsonl
```

Learn from past outcomes:
- Did it require migration?
- Any gotchas noted?

### Phase 4: Risk Assessment

For packages with major bumps or unknown risk, fetch changelogs.

Score each update 1-5. See [risk-assessment.md](references/risk-assessment.md) for guidelines.

### Phase 5: Smart Grouping

Group related packages together. See [grouping-strategies.md](references/grouping-strategies.md) for patterns.

Priority order:
1. Security fixes (own group, merge first)
2. Ecosystem batches (related packages together)
3. Low-risk patches (all together)
4. Individual major updates

### Phase 6: Execute Updates

For each group:

1. Create branch: `deps/<group-name>-$(date +%Y%m%d)`
2. Apply updates (see ecosystem reference)
3. Run tests
4. If tests fail: identify problematic package, exclude, continue

### Phase 7: Create PR

Use format from [pr-format.md](references/pr-format.md).

```bash
git add <lockfile> <manifest>
git commit -m "deps: <type> update <group-name>"
git push -u origin HEAD
gh pr create --title "deps: <type> update <group-name>" --body-file -
```

### Phase 8: Log Outcome

After PR is merged (or if update fails), log the outcome:

```bash
bun ~/.claude/skills/update-dependencies/scripts/log-outcome.ts
```

The script will:
1. Pre-fill: date, project, ecosystem, packages, versions
2. Prompt for: outcome (success/failed/required_migration) and notes
3. Append to `~/.claude/skills/update-dependencies/data/outcomes.jsonl`

---

## Command Options

When invoked via `/update-dependencies`:

| Option | Effect |
|--------|--------|
| `security only` | Only fix security vulnerabilities |
| `plan` | Enter plan mode - analyze and design update strategy for approval |
| `major` | Include major version updates |
| `group <name>` | Update specific ecosystem group |
| `--check-history` | Show past outcomes for packages being updated |

---

## Quick Start

```bash
# Run the analyzer first
bun ~/.claude/skills/update-dependencies/scripts/analyze.ts

# Or invoke the skill
/update-dependencies plan    # Analyze and plan
/update-dependencies         # Full execution
```

---

## Error Recovery

If update fails partway:
- If commit succeeded but push failed → `git push -u origin HEAD`
- If tests fail → identify problematic package, exclude, retry
- If PR creation failed → `gh pr create ...`
