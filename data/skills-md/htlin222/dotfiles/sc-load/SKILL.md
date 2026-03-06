---
name: sc-load
description: Load and analyze project context, configurations, and dependencies. Use when starting work on a project, understanding configurations, or analyzing dependencies.
---

# Project Context Loading

Load and analyze project context, configurations, dependencies, and environment setup.

## When to use

- Starting work on a new or unfamiliar project
- Understanding project configurations
- Analyzing project dependencies
- Setting up development environment
- Refreshing context after changes

## Instructions

### Usage

```
/sc:load [target] [--type project|config|deps|env] [--cache]
```

### Arguments

- `target` - Project directory or specific configuration to load
- `--type` - Loading type (project, config, deps, env)
- `--cache` - Cache loaded context for faster subsequent access
- `--refresh` - Force refresh of cached context

### Execution

1. Discover and analyze project structure and configuration files
2. Load dependencies, environment variables, and settings
3. Parse and validate configuration consistency
4. Create comprehensive project context map
5. Cache context for efficient future access

### Claude Code Integration

- Uses Glob for comprehensive project discovery
- Leverages Read for configuration analysis
- Applies Bash for environment validation
- Maintains efficient context caching mechanisms
