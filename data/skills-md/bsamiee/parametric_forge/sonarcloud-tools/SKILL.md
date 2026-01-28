---
name: sonarcloud-tools
type: complex
depth: base
description: >-
  Executes SonarCloud API queries via unified Python CLI. Use when checking
  quality gate status, searching issues (bugs, vulnerabilities, code smells),
  retrieving metrics (coverage, complexity), or viewing analysis history.
---

# [H1][SONARCLOUD-TOOLS]
>**Dictum:** *Zero-arg defaults enable immediate code quality inspection.*

<br>

Execute SonarCloud queries through unified Python CLI.

[IMPORTANT] Commands accept zero arguments. Defaults: `project=bsamiee_Parametric_Portal`, `organization=bsamiee`. 1Password auto-injects API token.

---
## [0][SCANNER]
>**Dictum:** *Local scanner enables pre-push quality gates.*

<br>

**Run Analysis:**
```bash
pnpm sonar
```

**Requirements:**
- `SONAR_TOKEN` environment variable (1Password injection or export)<br>
- Coverage reports at `packages/*/coverage/lcov.info` (run `nx run-many -t test` first)

**Configuration:** `sonar-project.properties` at repo root.

---
## [1][API_QUERIES]

```bash
# Zero-arg invocation (most common)
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py issues
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py hotspots
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py quality-gate
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py measures
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py analyses
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py projects

# Filtered queries
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py issues --severities BLOCKER,CRITICAL
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py issues --types BUG,VULNERABILITY
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py hotspots --status TO_REVIEW
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py quality-gate --branch main
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py quality-gate --pull-request 42
uv run .claude/skills/sonarcloud-tools/scripts/sonarcloud.py measures --metrics coverage,bugs,vulnerabilities
```

---
## [2][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]          | [RESPONSE]                                      |
| :-----: | -------------- | ----------------------------------------------- |
|   [1]   | `issues`       | `{project, total, issues[], summary}`           |
|   [2]   | `hotspots`     | `{project, total, hotspots[]}`                  |
|   [3]   | `quality-gate` | `{project, status, passed: bool, conditions[]}` |
|   [4]   | `measures`     | `{project, name, metrics}`                      |
|   [5]   | `analyses`     | `{project, total, analyses[]}`                  |
|   [6]   | `projects`     | `{organization, total, projects[]}`             |
