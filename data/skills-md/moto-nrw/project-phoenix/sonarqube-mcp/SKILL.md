---
name: sonarqube-mcp
description: Query and manage code quality using SonarQube/SonarCloud MCP tools. Use when checking quality gates, finding issues, analyzing code snippets, understanding SonarQube rules, or working with code quality metrics.
---

# SonarQube MCP

Use SonarQube/SonarCloud MCP tools to check code quality, find issues, and analyze code before pushing.

## Quick Actions

### Check Quality Gate
```
get_project_quality_gate_status
  projectKey: "org_project"
  pullRequest: "123"  # or branch: "feature-branch"
```
- `status: "OK"` = passes
- `status: "ERROR"` = fails
- Check `conditions` array for specific metrics

### Find Issues
```
search_sonar_issues_in_projects
  projects: ["org_project"]
  pullRequestId: "123"
  severities: ["BLOCKER", "CRITICAL"]  # optional filter
```

### Analyze Code Before Push
```
analyze_code_snippet
  code: "your code here"
  language: "typescript"  # or go, python, java, etc.
```
This runs analysis WITHOUT triggering CI - great for catching issues early.

### Understand a Rule
```
show_rule
  key: "typescript:S1082"  # or go:S3776, etc.
```

### Mark False Positive
```
change_sonar_issue_status
  key: "issue-key-from-search"
  status: ["falsepositive"]  # or ["accept"], ["reopen"]
```

## Tool Reference

See [TOOLS.md](TOOLS.md) for complete tool documentation.

## Severity Levels

| Level | Meaning |
|-------|---------|
| BLOCKER | Must fix immediately |
| CRITICAL | High impact |
| MAJOR | Significant problems |
| MINOR | Code smells |
| INFO | Informational |

## Common Metrics

| Key | Description |
|-----|-------------|
| `coverage` | Test coverage % |
| `duplicated_lines_density` | Duplication % |
| `reliability_rating` | Bug rating (A-E) |
| `security_rating` | Vulnerability rating |
| `sqale_rating` | Maintainability rating |
| `ncloc` | Lines of code |
| `complexity` | Cyclomatic complexity |

## Tips

1. **Pre-commit check**: Use `analyze_code_snippet` before pushing
2. **PR status**: Always check `get_project_quality_gate_status` with `pullRequest` param
3. **Understand failures**: Use `show_rule` to learn why code was flagged
4. **Triage efficiently**: Filter by `severities: ["BLOCKER", "CRITICAL"]` first
