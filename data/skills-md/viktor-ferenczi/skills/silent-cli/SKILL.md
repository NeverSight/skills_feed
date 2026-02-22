---
name: silent-cli
description: Environment variables and parameters for running command line programs reliably in non-interactive environments (unattended). Includes silent modes, color/disable TTY, and reduced output options for 155 CLI tools.
license: MIT
---

# Silent and Unattended CLI Execution Skill

## Overview

This skill provides a comprehensive reference for running command line programs in unattended/non-interactive environments.
It documents environment variables, command-line flags, and configuration options to:

- **Disable interactive prompts** - Ensure programs run without user input
- **Suppress progress indicators** - Disable spinners, progress bars, and real-time updates
- **Disable colored output** - Remove ANSI color codes and terminal formatting
- **Reduce output verbosity** - Limit output to essential information only
- **Force non-TTY mode** - Prevent programs from detecting terminal capabilities

## Coverage

- **155 programs** across Linux, macOS, and Windows
- Cloud platforms, containers, version control, build tools, databases, security, monitoring, CI/CD, IaC, and more

## Structure

```
/
├── SKILL.md              # This file - skill overview
├── INDEX_BY_NAME.md      # Program index alphabetically
├── INDEX_BY_CATEGORY.md  # Program index by category
├── PLATFORM_COVERAGE.md  # Platform coverage statistics
├── UNIX.md               # Unix/Linux usage examples
├── WINDOWS.md            # Windows-specific notes
├── programs/             # Individual program documentation (155 files)
│   ├── git.md
│   ├── curl.md
│   ├── aws.md
│   ├── docker.md
│   └── ...
└── scripts/              # Helper scripts (if needed)
```

## Quick Reference

- [INDEX_BY_NAME.md](INDEX_BY_NAME.md) - Alphabetical listing of all programs
- [INDEX_BY_CATEGORY.md](INDEX_BY_CATEGORY.md) - Programs organized by category
- [PLATFORM_COVERAGE.md](PLATFORM_COVERAGE.md) - Platform coverage statistics
- [UNIX.md](UNIX.md) - Unix/Linux usage examples
- [WINDOWS.md](WINDOWS.md) - Windows-specific notes (reserved filenames, etc.)
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute, program documentation format

## Universal Environment Variables

These environment variables affect many programs:

| Variable | Value | Effect |
|----------|-------|--------|
| `CI` | `true` | Indicates continuous integration environment, triggers non-interactive mode for many tools |
| `DEBIAN_FRONTEND` | `noninteractive` | Prevents apt/dpkg from prompting (Debian/Ubuntu) |
| `FORCE_COLOR` | `0` | Disables colored output (Node.js, some JS tools) |
| `NO_COLOR` | `1` | Disables colored output (growing standard) |
| `TERM` | `dumb` | Minimal terminal capabilities |
| `TZ` | `UTC` | Sets timezone, prevents timezone prompts |
| `PYTHONUNBUFFERED` | `1` | Unbuffered Python output |
| `NODE_NO_WARNINGS` | `1` | Suppress Node.js warnings |
