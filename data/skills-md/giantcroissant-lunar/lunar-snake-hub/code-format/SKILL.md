---
name: code-format
version: 0.1.0
kind: cli
description: Format code using dotnet format, prettier, and other formatting tools. Use when task involves code style fixes, formatting consistency, or preparing code for commit.
inputs:
  target: [dotnet, prettier, all]
  files: string[]
  verify: boolean
contracts:
  success: 'Code formatted successfully; no style violations remaining'
  failure: 'Non-zero exit code or formatting errors'
---

# Code Format Skill (Entry Map)

> **Goal:** Guide agent to the exact formatting procedure needed.

## Quick Start (Pick One)

- **Format .NET code (C#)** → `references/dotnet-format.md`
- **Format JSON/YAML/Markdown** → `references/prettier-format.md`
- **Format everything** → `references/fix-all.md`

## When to Use

- Fix code style violations (indentation, spacing, line endings)
- Apply .editorconfig rules consistently
- Prepare code for commit (pre-commit hook formatting)
- Enforce team coding standards
- Format specific files or entire codebase

**NOT for:** building (dotnet-build), testing (dotnet-test), or linting (code-analyze)

## Inputs & Outputs

**Inputs:** `target` (dotnet/prettier/all), `files` (specific files or directories), `verify` (check-only mode)

**Outputs:** Formatted files (modified in-place), exit code (0=success, non-zero=violations)

**Guardrails:** Non-destructive (can run with --verify-no-changes), respects .editorconfig, integrates with pre-commit

## Navigation

**1. Format .NET Code** → [`references/dotnet-format.md`](references/dotnet-format.md)

- Format C# files (.cs), apply dotnet format rules, fix code style issues

**2. Format with Prettier** → [`references/prettier-format.md`](references/prettier-format.md)

- Format JSON, YAML, Markdown, JavaScript, TypeScript files

**3. Format All Code** → [`references/fix-all.md`](references/fix-all.md)

- Run all formatters in sequence (dotnet + prettier), comprehensive formatting

## Common Patterns

### Quick Format (.NET)

```bash
cd ./dotnet
dotnet format PigeonPea.sln
```

### Quick Format (Prettier)

```bash
npx prettier --write "**/*.{json,yml,yaml,md}"
```

### Format Everything

```bash
./.agent/skills/code-format/scripts/format-all.sh
```

### Verify Only (Check Mode)

```bash
cd ./dotnet
dotnet format PigeonPea.sln --verify-no-changes
```

### Format Specific Files

```bash
# .NET
dotnet format --include ./console-app/Program.cs

# Prettier
npx prettier --write ./README.md
```

## Troubleshooting

**Format fails:** Check error messages. See specific reference files for detailed error handling.

**Files not formatted:** Check .editorconfig rules, file extensions, ignore patterns.

**Pre-commit hook fails:** Run formatters manually first, then commit. See `references/fix-all.md`.

**Conflicting styles:** .editorconfig takes precedence. Check configuration files.

**Performance issues:** Format specific projects/files instead of entire solution.

## Success Indicators

### dotnet format

```
Format complete in X ms.
```

No files changed (if already formatted), or list of formatted files.

### prettier

```
✔ Formatted X files
```

Or no output if all files already formatted.

## Integration

**Before commit:** Use pre-commit hooks to auto-format (configured in `.pre-commit-config.yaml`)

**Manual formatting:** Run before pushing code, before PR creation

**CI/CD:** Verify formatting in CI (use --verify-no-changes / --check mode)

**With other skills:**

- Before: code-analyze (fix style first)
- After: dotnet-build (build clean code)

## Configuration Files

- **`.editorconfig`**: Defines formatting rules (indent size, line endings, etc.)
- **`.prettierrc.json`**: Prettier configuration (print width, quotes, etc.)
- **`.pre-commit-config.yaml`**: Pre-commit hook configuration
- **`.prettierignore`**: Files to exclude from prettier formatting

## Related

- [`.editorconfig`](../../../.editorconfig) - Formatting rules
- [`.prettierrc.json`](../../../.prettierrc.json) - Prettier config
- [`.pre-commit-config.yaml`](../../../.pre-commit-config.yaml) - Pre-commit hooks
- [`setup-pre-commit.sh`](../../../setup-pre-commit.sh) - Pre-commit setup script
