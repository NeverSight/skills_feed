---
name: dotnet-dependency
description: This skill should be used when investigating .NET project dependencies, understanding why packages are included, listing references, or auditing for outdated/vulnerable packages.
allowed-tools: Bash(dotnet nuget why:*), Bash(dotnet list:*), Bash(dotnet outdated:*), Bash(dotnet package search:*), Bash(dotnet add package:*), Bash(dotnet remove package:*), Bash(dotnet tool:*), Read, Grep, Glob
---

# .NET Dependencies

Investigate and manage .NET project dependencies using built-in dotnet CLI commands.

## When to Use This Skill

Invoke when the user needs to:

- Search for NuGet packages or find latest versions
- Add, update, or remove package references
- Understand why a specific NuGet package is included
- List all project dependencies (NuGet packages or project references)
- Find outdated or vulnerable packages
- Trace transitive dependencies
- Manage dotnet tools (search, install, update)

## Quick Reference

| Command                                     | Purpose                                |
| ------------------------------------------- | -------------------------------------- |
| `dotnet package search <term>`              | Search NuGet for packages              |
| `dotnet package search <name> --exact-match`| List all versions of a package         |
| `dotnet add package <id>`                   | Add/update package to latest version   |
| `dotnet add package <id> -v <ver>`          | Add/update package to specific version |
| `dotnet remove package <id>`                | Remove package reference               |
| `dotnet nuget why <package>`                | Show dependency graph for a package    |
| `dotnet list package`                       | List NuGet packages                    |
| `dotnet list package --include-transitive`  | Include transitive dependencies        |
| `dotnet list reference --project <project>` | List project-to-project references     |
| `dotnet list package --outdated`            | Find packages with newer versions      |
| `dotnet list package --vulnerable`          | Find packages with security issues     |
| `dotnet outdated`                           | (Third-party) Check outdated packages  |
| `dotnet outdated -u`                        | (Third-party) Auto-update packages     |
| `dotnet tool search <term>`                 | Search for dotnet tools                |
| `dotnet tool update <id>`                   | Update local tool to latest            |
| `dotnet tool update --all`                  | Update all local tools                 |

## Search NuGet Packages

Find packages and check latest versions directly from CLI:

```bash
# Search for packages by keyword
dotnet package search Serilog --take 5

# Find latest version of a specific package
dotnet package search Aspire.Hosting.AppHost --take 1

# Include prerelease versions
dotnet package search ModelContextProtocol --prerelease --take 3

# List ALL available versions of a package (version history)
dotnet package search Newtonsoft.Json --exact-match

# JSON output for scripting
dotnet package search Serilog --format json --take 3
```

## Add and Update Packages

```bash
# Add package (installs latest stable version)
dotnet add package Serilog

# Add specific version
dotnet add package Serilog -v 4.0.0

# Add prerelease version
dotnet add package ModelContextProtocol --prerelease

# Add to specific project
dotnet add src/MyProject/MyProject.csproj package Serilog

# Update existing package to latest (same command as add)
dotnet add package Serilog

# Remove package
dotnet remove package Serilog
```

**Note**: `dotnet add package` both adds new packages and updates existing ones to the specified (or latest) version.

## Manage Dotnet Tools

```bash
# Search for tools
dotnet tool search dotnet-outdated --take 3

# Update a local tool (from manifest)
dotnet tool update cake.tool

# Update with prerelease
dotnet tool update aspire.cli --prerelease

# Update all local tools
dotnet tool update --all

# Update global tool
dotnet tool update -g dotnet-ef
```

## Investigate Package Dependencies

To understand why a package is included in your project:

```bash
# Why is this package included?
dotnet nuget why Newtonsoft.Json

# For a specific project
dotnet nuget why path/to/Project.csproj Newtonsoft.Json

# For a specific framework
dotnet nuget why Newtonsoft.Json --framework net8.0
```

Output shows the complete dependency chain from your project to the package.

## List NuGet Packages

```bash
# Direct dependencies only
dotnet list package

# Include transitive (indirect) dependencies
dotnet list package --include-transitive

# For a specific project
dotnet list package --project path/to/Project.csproj

# JSON output for scripting
dotnet list package --format json
```

## List Project References

```bash
# List project-to-project references
dotnet list reference --project path/to/Project.csproj
```

### Transitive Project References

No built-in command shows transitive project dependencies. To find if Project A depends on Project B transitively:

1. **Recursive approach**: Run `dotnet list reference` on each referenced project
2. **Parse .csproj files**: Search for `<ProjectReference>` elements recursively:

```bash
# Find all ProjectReference elements
grep -r "ProjectReference" --include="*.csproj" .
```

## Update Dependencies

### Using dotnet outdated (Third-party)

If installed (`dotnet tool install -g dotnet-outdated-tool`):

```bash
# Check for outdated packages
dotnet outdated

# Auto-update to latest versions
dotnet outdated -u

# Update only specific packages
dotnet outdated -u -inc PackageName
```

### Using built-in commands

```bash
# Check for outdated packages
dotnet list package --outdated

# Include prerelease versions
dotnet list package --outdated --include-prerelease
```

## Progressive Disclosure

For security auditing (vulnerable, deprecated, outdated packages), load **references/security-audit.md**.

## References

- [dotnet package search](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-package-search)
- [dotnet add package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-add-package)
- [dotnet remove package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-remove-package)
- [dotnet nuget why](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-nuget-why)
- [dotnet list reference](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-reference-list)
- [dotnet list package](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-list-package)
- [dotnet tool](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool)
