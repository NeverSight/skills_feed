---
name: Debugging
description: Python debugging techniques, pdb, and IDE debugging tools
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 04-testing-quality
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: issue_resolution_time
---

# Python Debugging Skill

## Overview
Master Python debugging using pdb, IDE debuggers, and advanced troubleshooting techniques.

## Topics Covered

### pdb Debugger
- Basic pdb commands
- Breakpoint() function
- Post-mortem debugging
- Remote debugging
- pdb++ enhancements

### IDE Debugging
- VS Code debugger
- PyCharm debugging
- Breakpoint conditions
- Watch expressions
- Call stack navigation

### Logging
- logging module setup
- Log levels and handlers
- Structured logging
- Log aggregation
- Debug logging strategies

### Profiling
- cProfile usage
- line_profiler
- memory_profiler
- py-spy for production
- Flame graphs

### Error Analysis
- Traceback analysis
- Exception chaining
- Context managers for debugging
- Sentry integration
- Error monitoring

## Prerequisites
- Python fundamentals
- Exception handling

## Learning Outcomes
- Debug effectively with pdb
- Profile performance issues
- Set up proper logging
- Analyze production errors
