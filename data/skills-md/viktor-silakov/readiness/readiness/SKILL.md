---
name: readiness
description: Evaluate repository readiness for AI agents. Analyzes 81 criteria across 8 pillars, assigns maturity level 1-5, generates visual report.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Write
---

# Repository Readiness Assessment

Audit any repository to determine readiness for autonomous AI agent workflows. Produces a structured report scoring 81 distinct criteria.

**Target:** Use `$ARGUMENTS` if a GitHub URL is provided, otherwise analyze the current working directory.

## Workflow

1. **Clone if needed** — When `$ARGUMENTS` is a GitHub URL, clone to `/tmp`
2. **Discover context** — Detect languages, locate source/test/config directories
3. **Identify apps** — Count deployable units (monorepo services, libraries, etc.)
4. **Evaluate criteria** — Score all 81 criteria from [CRITERIA.md](CRITERIA.md)
5. **Calculate level** — Determine maturity level 1-5 based on thresholds
6. **Generate report** — Output visual ASCII report per [OUTPUT_FORMAT.md](OUTPUT_FORMAT.md)
7. **Ask about HTML export** — ALWAYS ask the user if they want the D3.js dashboard after the ASCII report; do not proceed until they answer

## Boundary Rules

- Stay within git repository root (where `.git` exists)
- Skip `.git`, `node_modules`, `dist`, `build`, `__pycache__`
- Never access paths outside the repository

## Language Detection

| Language | Indicators |
|----------|-----------|
| JS/TS | `package.json`, `tsconfig.json`, `.ts`/`.tsx`/`.js`/`.jsx` |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt`, `.py` |
| Rust | `Cargo.toml`, `.rs` |
| Go | `go.mod`, `.go` |
| Java | `pom.xml`, `build.gradle`, `.java` |
| Ruby | `Gemfile`, `.gemspec`, `.rb` |

## Application Discovery

An **application** is a standalone deployable unit:
- Independent build/deploy lifecycle
- Serves users or systems directly
- Could function as its own repository

**Patterns:**
- Simple repos → 1 app (root)
- Monorepos → count each deployable service
- Libraries → 1 app (the library itself)

## Scoring Rules

**Repository Scope (43 criteria):**
- Evaluated once for entire repo
- numerator: 1 (pass), 0 (fail), null (skipped)
- denominator: always 1

**Application Scope (38 criteria):**
- Evaluated per-app
- numerator: count of passing apps
- denominator: total apps (N)

## Maturity Levels

| Level | Name | Requirement |
|-------|------|-------------|
| L1 | Functional | Baseline (all repos start here) |
| L2 | Documented | ≥80% of L1 criteria pass |
| L3 | Standardized | L2 + ≥80% of L2 criteria pass |
| L4 | Optimized | L3 + ≥80% of L3 criteria pass |
| L5 | Autonomous | L4 + ≥80% of L4 criteria pass |

## Evaluation Principles

- **Deterministic**: Same repo → same output
- **Existence-based**: Prefer file/config existence over semantic analysis
- **Conservative**: Ambiguous evidence = fail
- **Concise rationales**: Max 500 characters each

## Additional Resources

- **[CRITERIA.md](CRITERIA.md)** — Full list of 81 criteria with descriptions
- **[OUTPUT_FORMAT.md](OUTPUT_FORMAT.md)** — ASCII visual report format with ANSI colors
- **[templates/report.html](templates/report.html)** — D3.js HTML dashboard template
- **[examples/sample-output.md](examples/sample-output.md)** — Example report output

## HTML Report Generation (MANDATORY)

**IMPORTANT: You MUST ask the user this question every single time after displaying the ASCII report. Do not skip this step and do not proceed until the user responds.**

Ask user:
```
Would you like to generate an interactive HTML report with D3.js charts? [yes/no]
```

Wait for user response. If yes, use template from [templates/report.html](templates/report.html) and save as `readiness-report.html`. After generation, always offer to open the report.
