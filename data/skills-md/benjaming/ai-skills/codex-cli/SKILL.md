---
name: codex-cli
description: Use OpenAI Codex CLI in non-interactive mode for automated code analysis, review, and programmatic task execution. Trigger on requests like "use Codex to analyze", "run codex exec", "codex code review", or when users want AI-powered code analysis without interactive prompts. Ideal for automation workflows, code quality checks, and generating structured analysis reports.
---

# Codex CLI Non-Interactive Mode

## Overview

Execute OpenAI's Codex CLI in non-interactive mode (`codex exec`) to automate code analysis, reviews, and other development tasks without requiring user approvals. The tool operates with configurable safety modes and supports structured outputs for integration into automation pipelines.

## When to Use This Skill

Use Codex CLI when the user requests:
- Code analysis or architectural reviews using AI assistance
- Automated code quality checks or security audits
- Generating reports (changelogs, documentation, etc.) from code
- Multi-step analysis workflows that benefit from persistent context
- Integration with automation pipelines requiring structured output

**Trigger phrases:** "use Codex to...", "run codex exec", "codex analyze", "have codex review"

## Core Capabilities

### 1. Safety Mode Selection

Choose the appropriate safety mode based on task requirements:

**Read-Only (Default)** - For analysis and review tasks:
```bash
codex exec "Analyze the authentication flow and identify potential security issues"
```

**Full Automation** - When file modifications are needed:
```bash
codex exec --full-auto "Refactor the user service to follow SOLID principles"
```

**Unrestricted Mode** - Only when network access is required:
```bash
codex exec --sandbox danger-full-access "Test API endpoints and validate responses"
```

**Decision Guidelines:**
- Start with read-only for initial exploration
- Use --full-auto when the user explicitly requests code changes
- Reserve unrestricted mode for tasks requiring network operations
- Always inform the user which mode is being used and why

### 2. Output Handling

Configure output format based on downstream requirements:

**Default (Pipe-Friendly)**
```bash
codex exec "Generate changelog from last 10 commits" > changelog.md
```
Activity logs to stderr, final output to stdout.

**Save to File**
```bash
codex exec "Review code for type errors" -o review-report.txt
```

**JSON Streaming for Monitoring**
```bash
codex exec --json "Comprehensive security audit" 2>&1 | tee audit-log.jsonl
```
Captures events: `turn.started`, `command_execution`, `file_change`, etc.

**Structured Schema Output**
```bash
codex exec "Find all TODO comments with context" --output-schema todo-schema.json
```
Enforces specific JSON structure for automation pipelines.

### 3. Session-Based Workflows

Maintain context across multiple related tasks:

```bash
# Initial analysis
codex exec "Analyze the codebase architecture"
# Returns session ID, e.g., session_abc123

# Follow-up with context
codex exec resume --last "Now identify performance bottlenecks in the identified critical paths"

# Or resume specific session
codex exec resume session_abc123 "Generate refactoring recommendations"
```

**Note:** Behavior flags must be re-specified on resume (e.g., --full-auto).

### 4. Automation Integration

Integrate Codex into CI/CD or development workflows:

```bash
# Code review in PR pipeline
codex exec --json "Review uncommitted changes for bugs and style issues" \
  --output-schema review-schema.json > review.json

# Generate documentation
codex exec "Generate API documentation from comments" -o api-docs.md

# Security scanning
codex exec "Scan for OWASP Top 10 vulnerabilities" --json 2>&1 | \
  jq 'select(.type=="item.completed" and .item.type=="agent_message")'
```

## Task Execution Patterns

### Code Analysis Task
```bash
# User asks: "Use Codex to analyze our error handling patterns"
codex exec "Analyze error handling patterns across the codebase. Identify inconsistencies, anti-patterns, and suggest improvements."
```

### Code Review Task
```bash
# User asks: "Have Codex review the recent changes"
codex exec --full-auto "Review git diff for the last commit. Check for bugs, security issues, and code quality problems."
```

### Report Generation Task
```bash
# User asks: "Generate a changelog using Codex"
codex exec "Generate a changelog from commits since last release tag. Group by feature, bugfix, and breaking changes." -o CHANGELOG.md
```

### Multi-Step Investigation
```bash
# User asks: "Use Codex to investigate the performance issues"
codex exec "Profile the application and identify performance bottlenecks"
# Review results, then:
codex exec resume --last "Deep dive into the database query performance issues you identified"
```

## Important Considerations

### Git Repository Requirement
Codex requires a Git repository to track changes safely. Override only when necessary:
```bash
codex exec --skip-git-repo-check "<task>"
```

### Authentication
Use default Codex CLI credentials or override:
```bash
CODEX_API_KEY=your-key-here codex exec "<task>"
```

### Error Handling
- Check exit codes: `$?` for success/failure
- Stderr contains activity logs and errors
- JSON mode provides structured error events

### Model Selection
Codex CLI defaults to appropriate models based on platform. Explicit model selection happens in interactive mode only.

## Reference Documentation

For detailed command syntax, all available flags, and advanced use cases, consult:
- `references/codex-exec-reference.md` - Comprehensive command reference

Use `rg` to search reference documentation when specific flag information is needed:
```bash
rg "resume" references/codex-exec-reference.md
```

## Best Practices

1. **Always explain the chosen safety mode** to the user
2. **Start conservative** (read-only) and escalate permissions only when needed
3. **Capture session IDs** when planning multi-step workflows
4. **Use structured outputs** (--output-schema) for automation reliability
5. **Monitor JSON streams** for long-running tasks to provide progress updates
6. **Combine with shell tools** (jq, grep, etc.) for post-processing
7. **Preserve context** through session resume for complex investigations
