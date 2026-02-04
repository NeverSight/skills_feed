---
name: code-clone-assistant
description: Detect and refactor code duplication with PMD CPD. TRIGGERS - code clones, DRY violations, duplicate code.
allowed-tools: Read, Grep, Bash, Edit, Write
---

# Code Clone Assistant

Detect code clones and guide refactoring using PMD CPD (exact duplicates) + Semgrep (patterns).

## Tools

- **PMD CPD v7.17.0+**: Exact duplicate detection
- **Semgrep v1.140.0+**: Pattern-based detection

**Tested**: October 2025 - 30 violations detected across 3 sample files
**Coverage**: ~3x more violations than using either tool alone

---

## When to Use This Skill

Use this skill when:

- Finding duplicate code in a codebase
- Detecting DRY violations
- Refactoring similar code patterns
- Identifying copy-paste code

---

## Why Two Tools?

PMD CPD and Semgrep detect different clone types:

| Aspect       | PMD CPD                          | Semgrep                          |
| ------------ | -------------------------------- | -------------------------------- |
| **Detects**  | Exact copy-paste duplicates      | Similar patterns with variations |
| **Scope**    | Across files ✅                  | Within/across files (Pro only)   |
| **Matching** | Token-based (ignores formatting) | Pattern-based (AST matching)     |
| **Rules**    | ❌ No custom rules               | ✅ Custom rules                  |

**Result**: Using both finds ~3x more DRY violations.

### Clone Types

| Type   | Description                     | PMD CPD         | Semgrep     |
| ------ | ------------------------------- | --------------- | ----------- |
| Type-1 | Exact copies                    | ✅ Default      | ✅          |
| Type-2 | Renamed identifiers             | ✅ `--ignore-*` | ✅          |
| Type-3 | Near-miss with variations       | ⚠️ Partial      | ✅ Patterns |
| Type-4 | Semantic clones (same behavior) | ❌              | ❌          |

---

## Quick Start Workflow

```bash
# Step 1: Detect exact duplicates (PMD CPD)
pmd cpd -d . -l python --minimum-tokens 20 -f markdown > pmd-results.md

# Step 2: Detect pattern violations (Semgrep)
semgrep --config=clone-rules.yaml --sarif --quiet > semgrep-results.sarif

# Step 3: Analyze combined results (Claude Code)
# Parse both outputs, prioritize by severity

# Step 4: Refactor (Claude Code with user approval)
# Extract shared functions, consolidate patterns, verify tests
```

---

---

## Reference Documentation

For detailed information, see:

- [Detection Commands](./references/detection-commands.md) - PMD CPD and Semgrep command details
- [Complete Workflow](./references/complete-workflow.md) - Detection, analysis, and presentation phases
- [Refactoring Strategies](./references/refactoring-strategies.md) - Approaches for addressing violations

---

## Troubleshooting

| Issue                      | Cause                        | Solution                                         |
| -------------------------- | ---------------------------- | ------------------------------------------------ |
| PMD CPD not found          | Not installed or not in PATH | `brew install pmd` or download from PMD releases |
| Semgrep timeout            | Large codebase scan          | Use `--exclude` to limit scope                   |
| No duplicates detected     | minimum-tokens too high      | Lower `--minimum-tokens` value (try 15)          |
| Too many false positives   | minimum-tokens too low       | Increase `--minimum-tokens` (try 30+)            |
| Language not recognized    | Wrong `-l` flag              | Check PMD CPD supported languages list           |
| SARIF parse error          | Semgrep output malformed     | Upgrade Semgrep to latest version                |
| Memory error on large repo | Java heap too small          | Set `PMD_JAVA_OPTS=-Xmx4g`                       |
| Missing clone rules file   | Custom rules not created     | Create `clone-rules.yaml` or use default config  |
