---
name: code-hardcode-audit
description: Detect hardcoded values, magic numbers, and leaked secrets. TRIGGERS - hardcode audit, magic numbers, PLR2004, secret scanning.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Code Hardcode Audit

## When to Use This Skill

Use this skill when the user mentions:

- "hardcoded values", "hardcodes", "magic numbers"
- "constant detection", "find constants"
- "duplicate constants", "DRY violations"
- "code audit", "hardcode audit"
- "PLR2004", "semgrep", "jscpd", "gitleaks"
- "secret scanning", "leaked secrets", "API keys"
- "passwords in code", "credential leaks"

## Quick Start

```bash
# Full audit (all tools, both outputs)
uv run --script scripts/audit_hardcodes.py -- src/

# Python magic numbers only (fastest)
uv run --script scripts/run_ruff_plr.py -- src/

# Pattern-based detection (URLs, ports, paths)
uv run --script scripts/run_semgrep.py -- src/

# Copy-paste detection
uv run --script scripts/run_jscpd.py -- src/

# Secret scanning (API keys, tokens, passwords)
uv run --script scripts/run_gitleaks.py -- src/
```

## Tool Overview

| Tool             | Detection Focus                 | Language Support | Speed  |
| ---------------- | ------------------------------- | ---------------- | ------ |
| **Ruff PLR2004** | Magic value comparisons         | Python           | Fast   |
| **Semgrep**      | URLs, ports, paths, credentials | Multi-language   | Medium |
| **jscpd**        | Duplicate code blocks           | Multi-language   | Slow   |
| **gitleaks**     | Secrets, API keys, passwords    | Any (file-based) | Fast   |

## Output Formats

### JSON (--output json)

```json
{
  "summary": {
    "total_findings": 42,
    "by_tool": { "ruff": 15, "semgrep": 20, "jscpd": 7 },
    "by_severity": { "high": 5, "medium": 25, "low": 12 }
  },
  "findings": [
    {
      "id": "MAGIC-001",
      "tool": "ruff",
      "rule": "PLR2004",
      "file": "src/config.py",
      "line": 42,
      "column": 8,
      "message": "Magic value used in comparison: 8123",
      "severity": "medium",
      "suggested_fix": "Extract to named constant"
    }
  ],
  "refactoring_plan": [
    {
      "priority": 1,
      "action": "Create constants/ports.py",
      "finding_ids": ["MAGIC-001", "MAGIC-003"]
    }
  ]
}
```

### Compiler-like Text (--output text)

```
src/config.py:42:8: PLR2004 Magic value used in comparison: 8123 [ruff]
src/probe.py:15:1: hardcoded-url Hardcoded URL detected [semgrep]
src/client.py:20-35: Clone detected (16 lines, 95% similarity) [jscpd]

Summary: 42 findings (ruff: 15, semgrep: 20, jscpd: 7)
```

## CLI Options

```
--output {json,text,both}  Output format (default: both)
--tools {all,ruff,semgrep,jscpd,gitleaks}  Tools to run (default: all)
--severity {all,high,medium,low}  Filter by severity (default: all)
--exclude PATTERN  Glob pattern to exclude (repeatable)
--parallel  Run tools in parallel (default: true)
```

## References

- [Tool Comparison](./references/tool-comparison.md) - Detailed tool capabilities
- [Output Schema](./references/output-schema.md) - JSON schema specification
- [Troubleshooting](./references/troubleshooting.md) - Common issues and fixes

## Related

- ADR-0046: Semantic Constants Abstraction
- ADR-0047: Code Hardcode Audit Skill
- `code-clone-assistant` - PMD CPD-based clone detection (DRY focus)

---

## Troubleshooting

| Issue                    | Cause                       | Solution                                                     |
| ------------------------ | --------------------------- | ------------------------------------------------------------ |
| Ruff PLR2004 not found   | Ruff not installed or old   | `uv tool install ruff` or upgrade                            |
| Semgrep timeout          | Large codebase scan         | Use `--exclude` to limit scope                               |
| jscpd memory error       | Too many files              | Increase Node heap: `NODE_OPTIONS=--max-old-space-size=4096` |
| gitleaks false positives | Test data flagged           | Add patterns to `.gitleaks.toml` allowlist                   |
| No findings in output    | Wrong directory specified   | Verify path exists and contains source files                 |
| JSON parse error         | Tool output malformed       | Run tool individually with `--output text`                   |
| Missing tool in PATH     | Tool not installed globally | Install via mise, homebrew, or npm                           |
| Severity filter empty    | No findings at that level   | Use `--severity all` to see all findings                     |
