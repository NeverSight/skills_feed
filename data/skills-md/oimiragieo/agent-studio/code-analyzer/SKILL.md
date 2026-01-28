---
name: code-analyzer
description: Static code analysis and complexity metrics
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, Glob, Grep]
best_practices:
  - Analyze before refactoring
  - Track complexity over time
  - Focus on hotspots first
error_handling: graceful
streaming: supported
---

# Code Analyzer Skill

## Overview

Static code analysis and metrics. 90%+ context savings.

## Tools (Progressive Disclosure)

### Analysis

| Tool            | Description                  |
| --------------- | ---------------------------- |
| analyze-file    | Analyze single file          |
| analyze-project | Analyze entire project       |
| complexity      | Calculate complexity metrics |

### Metrics

| Tool            | Description           |
| --------------- | --------------------- |
| loc             | Lines of code         |
| cyclomatic      | Cyclomatic complexity |
| maintainability | Maintainability index |
| duplicates      | Find duplicate code   |

### Reporting

| Tool     | Description              |
| -------- | ------------------------ |
| summary  | Get analysis summary     |
| hotspots | Find complexity hotspots |
| trends   | Analyze metric trends    |

## Agent Integration

- **code-reviewer** (primary): Code review
- **refactoring-specialist** (primary): Tech debt analysis
- **architect** (secondary): Architecture assessment

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
