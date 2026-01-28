---
name: taskfile-automation
description: Expert guidance for using Task (taskfile.dev) automation tool to discover and execute project development commands
---

# Task Automation System

Use this skill when working with projects that use [Task](https://taskfile.dev) to provide easy-to-discover automation commands for development workflows.

## Core Principle

**IMPORTANT**: Always prefer `task` commands over direct shell/language commands when a Taskfile is present.

Task provides:
- **Discoverability**: `task --list` shows all available tasks
- **Consistency**: Standardised commands across different environments
- **Documentation**: Built-in descriptions and help
- **Automation**: Multi-step workflows (e.g., `task dev` combines testing and docs)
- **Safety**: Interactive prompts for destructive operations

## Task Discovery

### Find Available Tasks

```bash
# List all available tasks with descriptions
task --list

# Show common workflows and usage patterns
task help

# Get detailed help for specific task
task <taskname> --help
```

**Always start with discovery** when entering a new project with a Taskfile.

## Common Task Patterns

### Development Workflows

Projects typically provide these standard tasks:

```bash
# Fast development cycle (common iteration loop)
task dev          # Usually runs fast tests + fast docs

# Pre-commit workflow
task precommit    # Runs pre-commit hooks + fast tests

# Full CI simulation locally
task ci           # Complete CI pipeline locally
```

### Testing Workflows

```bash
# Full test suite including quality checks
task test

# Fast tests (skip quality checks for rapid development)
task test-fast
task test:fast    # Alternative naming

# Quality checks only (Aqua, formatting, linting)
task test-quality
task test:quality
```

### Documentation Building

```bash
# Quick docs build (recommended for development)
task docs-fast
task docs:fast

# Full documentation including slow components (notebooks, etc.)
task docs

# Interactive documentation server
task docs-pluto   # For Julia projects with Pluto notebooks
task docs:serve   # For live-reload documentation server
```

### Environment Management

```bash
# Set up development environment from scratch
task setup

# Show package/dependency status
task pkg:status
task status

# Project overview and environment information
task info
```

### Code Quality

```bash
# Linting
task lint

# Formatting
task format

# Combined quality checks
task quality
```

## Using Task vs Direct Commands

### When to Use Task

Use `task` commands when:
- A Taskfile exists in the project
- You need to run standard development operations
- You want to discover available workflows
- You need consistency across team members

### When Task Wraps Underlying Commands

Tasks are typically thin wrappers around language-specific commands:

**Example - Julia:**
```bash
# Task command
task test

# Underlying command it runs
julia --project=. -e 'using Pkg; Pkg.test()'
```

**Example - R:**
```bash
# Task command
task docs

# Underlying command it runs
Rscript -e "devtools::document()"
```

### When to Use Direct Commands

Use direct language commands when:
- No Taskfile exists
- You need advanced options not exposed by tasks
- You're doing exploratory work outside standard workflows
- Tasks don't cover your specific use case

## Task Workflow Examples

### Typical Development Cycle

```bash
# 1. Discover what's available
task --list

# 2. Run fast iteration cycle
task dev          # Fast tests + fast docs

# 3. Before committing
task precommit    # Pre-commit checks + tests

# 4. Before pushing (optional)
task ci           # Full CI simulation
```

### First-Time Setup

```bash
# 1. See what setup tasks exist
task --list | grep setup

# 2. Run setup
task setup        # Install dependencies, configure environment

# 3. Verify setup
task info         # Show project and environment status

# 4. Test everything works
task test
```

## Task Naming Conventions

Common patterns in task names:

**Prefixes:**
- `test:*` - Testing-related tasks
- `docs:*` - Documentation tasks
- `pkg:*` - Package management tasks
- `ci:*` - CI/CD related tasks

**Suffixes:**
- `*-fast` - Quick version of the task
- `*-full` - Complete version including optional steps

**Special names:**
- `dev` - Fast development iteration cycle
- `precommit` - Pre-commit validation
- `ci` - Full CI pipeline
- `setup` - Initial project setup
- `clean` - Clean build artifacts
- `help` - Show usage information

## Integration with Language Tools

### Julia Projects

```bash
# Instead of: julia --project=. -e 'using Pkg; Pkg.test()'
task test

# Instead of: julia --project=docs docs/make.jl --skip-notebooks
task docs-fast

# Instead of: julia --project=. -e 'using Pkg; Pkg.update()'
task pkg:update
```

### R Projects

```bash
# Instead of: Rscript -e "devtools::test()"
task test

# Instead of: Rscript -e "devtools::document()"
task docs

# Instead of: Rscript -e "devtools::check()"
task check
```

### Python Projects

```bash
# Instead of: pytest
task test

# Instead of: sphinx-build docs docs/_build
task docs

# Instead of: pip install -e .
task install
```

## Task Configuration Files

### Taskfile Location

Look for:
- `Taskfile.yml` in project root
- `Taskfile.yaml` in project root

### Understanding Task Definitions

When reading a Taskfile:
- `cmds:` - Commands executed by the task
- `deps:` - Dependencies run before this task
- `desc:` - Description shown in `task --list`
- `summary:` - Extended description for `task <name> --help`

## Best Practices

1. **Always discover first**: Run `task --list` when entering a project
2. **Use task help**: Check `task help` for project-specific guidance
3. **Prefer tasks for standard workflows**: Use tasks for dev, test, docs
4. **Direct commands for exploration**: Use language commands for ad-hoc work
5. **Check task definitions**: Look at Taskfile.yml to understand what tasks do
6. **Update documentation**: If tasks change workflows, note it

## When to Use This Skill

Activate this skill when:
- Working with projects that have a Taskfile.yml/Taskfile.yaml
- You see mentions of "Task" or "task commands" in project documentation
- Project CLAUDE.md mentions using `task` instead of direct commands
- You need to discover available development workflows
- Running tests, building docs, or managing project development tasks

This skill helps you leverage Task automation rather than manually running underlying commands.
Project-specific task definitions and workflows remain in project documentation.
