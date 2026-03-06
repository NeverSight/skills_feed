---
name: sc-analyze
description: Analyze code quality, security, performance, and architecture. Use when user asks to analyze code, review codebase health, or identify issues.
---

# Code Analysis

Execute comprehensive code analysis across quality, security, performance, and architecture domains.

## When to use

- User asks to analyze code quality or technical debt
- Security audit or vulnerability assessment needed
- Performance analysis or bottleneck identification required
- Architecture review or structural analysis requested
- Code health check or quality metrics needed

## Instructions

### Usage

```
/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep]
```

### Arguments

- `target` - Files, directories, or project to analyze
- `--focus` - Analysis focus area (quality, security, performance, architecture)
- `--depth` - Analysis depth (quick, deep)
- `--format` - Output format (text, json, report)

### Execution

1. Discover and categorize files for analysis
2. Apply appropriate analysis tools and techniques
3. Generate findings with severity ratings
4. Create actionable recommendations with priorities
5. Present comprehensive analysis report

### Claude Code Integration

- Uses Glob for systematic file discovery
- Leverages Grep for pattern-based analysis
- Applies Read for deep code inspection
- Maintains structured analysis reporting
