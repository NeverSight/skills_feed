---
name: dotnet-inspect
description: Inspect .NET assemblies and NuGet packages. Use when you need to understand package contents, view public API surfaces, compare APIs between versions, or audit assemblies for SourceLink/determinism. Essential for .NET development tasks involving package exploration or API discovery.
---

# dotnet-inspect

A CLI tool for inspecting .NET assemblies and NuGet packages.

## Requirements

- .NET 10+ SDK

## Installation

Use `dnx` to run without global installation (like `npx` for Node):

```bash
dnx dotnet-inspect -y -- <command>
```

**Important**:
- Always use `-y` to skip the interactive confirmation prompt (which breaks LLM tool use). New package versions also trigger this prompt.
- Always use `--` to separate dnx options from tool arguments. Without it, `--help` shows dnx help, not dotnet-inspect help.

## Quick Patterns

Start with these common workflows:

```bash
# Understand a type's API shape (start here - most useful for learning APIs)
dnx dotnet-inspect -y -- type JsonSerializer --package System.Text.Json

# Compare API changes between versions (essential for migrations)
dnx dotnet-inspect -y -- diff Command --package System.CommandLine@2.0.0-beta4.22272.1..2.0.2
dnx dotnet-inspect -y -- diff JsonSerializer --package System.Text.Json@9.0.0..10.0.0

# Search for types by pattern (single or batch with comma-separated patterns)
dnx dotnet-inspect -y -- find "*Handler*" --package System.CommandLine
dnx dotnet-inspect -y -- find "Option*,Argument*,Command*" --package System.CommandLine --terse

# Package metadata and versions
dnx dotnet-inspect -y -- package System.Text.Json
dnx dotnet-inspect -y -- package System.Text.Json --versions

# Get XML documentation for a type
dnx dotnet-inspect -y -- type Option --package System.CommandLine --docs
```

## Key Flags

| Flag | Purpose | Commands |
|------|---------|----------|
| `-v:d` | Detailed output (full signatures, more info) | all commands |
| `--docs` | Include XML documentation from source | `type`, `api` |
| `-m Name` | Filter to specific member(s) | `type`, `api` |
| `-n 10` | Limit results | `find`, `package --versions` |
| `--terse`, `-t` | One line per pattern (for batch find) | `find` |
| `--prerelease` | Include prerelease versions | `package --versions` |

**Generic types:** Use quotes around generic types: `'Option<T>'`, `'IEnumerable<T>'`

## Command Reference

| Command | Purpose |
|---------|---------|
| `type <type>` | **Start here.** Type shape with hierarchy and members (tree view) |
| `diff <type>` | Compare API surfaces between package versions |
| `api <type>` | View public API surface (table format) |
| `find <pattern>` | Search for types across packages, assemblies, or frameworks |
| `package <name>` | Package metadata, files, versions, dependencies |
| `assembly <path>` | Assembly info, SourceLink/determinism audit |
| `llmstxt` | Complete usage examples for all commands |

## Full Documentation

For comprehensive examples and edge cases:

```bash
dnx dotnet-inspect -y -- llmstxt
```

## When to Use This Skill

- Exploring what types/APIs a NuGet package provides
- Searching for types by pattern across packages or frameworks
- Understanding method signatures and overloads
- Comparing API changes between package versions
- Auditing assemblies for SourceLink and determinism
- Finding types matching a pattern (`--filter "Progress*"`)
- Getting documentation from source (`--docs`)
