---
name: code-review
description: Capable of performing comprehensive code reviews on git commits. Analyzes commit changes, investigates side effects in the codebase, and categorizes findings by severity levels (critical, major, minor, nit).
---

# Code Review Capabilities

This skill enables the agent to perform structured code reviews on git commits by analyzing changes, tracing side effects, and providing categorized feedback.

## Core Capabilities

- **Git Commit Analysis**: Retrieves commit metadata, messages, and diffs from git hash
- **Change Classification**: Categorizes modified files by type (source, test, config, new, modified, deleted)
- **Side Effect Detection**: Traces function/class usage across the codebase to identify potential impacts
- **Severity Classification**: Categorizes review findings into four severity levels

## Review Flow

| Phase | Capability | Output |
|-------|-----------|--------|
| 1. Context Collection | Git hash lookup, diff statistics | Commit metadata, change scope |
| 2. Change Analysis | File-by-file diff inspection | Categorized file changes |
| 3. Impact Analysis | Dependency tracing, test coverage check | Side effect report |
| 4. Review Execution | Code inspection with severity classification | Categorized findings |
| 5. Result Summary | Formatted output generation | Structured review report |

## Severity Levels

| Level | Scope |
|-------|-------|
| **Critical** | Security vulnerabilities, data loss risks, service outage potential |
| **Major** | Bugs, performance issues, incorrect logic |
| **Minor** | Code quality, readability, duplication |
| **Nit** | Style, naming conventions, comment improvements |

## Domain Knowledge

- **Git Operations**: Commands for retrieving commit information and diffs. See [./references/git_operations.md](./references/git_operations.md)
- **Change Analysis**: File categorization and diff interpretation methods. See [./references/change_analysis.md](./references/change_analysis.md)
- **Impact Detection**: Side effect tracing and dependency analysis techniques. See [./references/impact_detection.md](./references/impact_detection.md)
- **Severity Criteria**: Detailed classification criteria for each severity level. See [./references/severity_criteria.md](./references/severity_criteria.md)
- **Output Format**: Review result structure and formatting specification. See [./references/output_format.md](./references/output_format.md)

## Supported Analysis Types

- **Single Commit**: Review changes in a specific commit hash
- **Commit Range**: Review changes across multiple commits
- **File-Scoped**: Review specific files within a commit

## Constraints

- **Read-Only Operations**: Uses only non-destructive git commands
- **Local Repository**: Operates on locally available git history
