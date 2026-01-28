---
name: agents
description: "Agent Skill: Generate and maintain AGENTS.md files following the public agents.md convention. Use when creating AI agent documentation, onboarding guides, or standardizing agent patterns. By Netresearch."
---

# AGENTS.md Generator Skill

Generate and maintain AGENTS.md files following the public agents.md convention.

## When to Use This Skill

When creating new projects, use this skill to establish baseline AGENTS.md structure.

When standardizing existing projects, use this skill to generate consistent agent documentation.

When ensuring multi-repo consistency, use this skill to apply the same standards across repositories.

When checking if AGENTS.md files are up to date, use the freshness checking scripts to compare file timestamps with git commits.

## CRITICAL: Full Verification Required

**NEVER trust existing AGENTS.md content as accurate.** Always verify documented information against the actual codebase:

### Mandatory Verification Steps

1. **Extract actual state from source files:**
   - List all modules/files with their actual docstrings
   - List all scripts and their actual purposes
   - Extract actual Makefile/package.json commands
   - List actual test files and structure

2. **Compare extracted state against documented state:**
   - Check if documented files actually exist
   - Check if documented commands actually work
   - Check if module descriptions match actual docstrings
   - Check if counts (modules, scripts, tests) are accurate

3. **Identify and fix discrepancies:**
   - Remove documentation for non-existent files
   - Add documentation for undocumented files
   - Correct inaccurate descriptions
   - Update outdated counts and references

4. **Preserve unverifiable content:**
   - Keep manually-written context that can't be extracted
   - Keep subjective guidance and best practices
   - Mark preserved content appropriately

### What to Verify

| Category | Verification Method |
|----------|---------------------|
| Module list | `ls <dir>/*.py` + read docstrings |
| Script list | `ls scripts/*.sh` + read headers |
| Commands | `grep` Makefile targets |
| Test files | `ls tests/*.py` |
| Data files | `ls *.json` in project root |
| Config files | Check actual existence |

### Example Verification Commands

```bash
# Extract actual module docstrings
for f in cli_audit/*.py; do head -20 "$f" | grep -A5 '"""'; done

# List actual scripts
ls scripts/*.sh

# Extract Makefile targets
grep -E '^[a-z_-]+:' Makefile*

# List actual test files
ls tests/*.py tests/**/*.py
```

### Anti-Patterns to Avoid

- **WRONG:** Updating only dates and counts based on git commits
- **WRONG:** Trusting that existing AGENTS.md was created correctly
- **WRONG:** Copying file lists without verifying they exist
- **WRONG:** Using extracted command output without running it
- **RIGHT:** Extract → Compare → Fix discrepancies → Validate

## Capabilities

- **Thin root files** (~30 lines) with precedence rules and global defaults
- **Scoped files** for subsystems (backend/, frontend/, internal/, cmd/)
- **Auto-extracted commands** from Makefile, package.json, composer.json, go.mod
- **Language-specific templates** for Go, PHP, TypeScript, Python, hybrid projects
- **Freshness checking** - Detects if AGENTS.md files are outdated by comparing their "Last updated" date with git commits
- **Automatic timestamps** - All generated files include creation/update dates in the header
- **Documentation extraction** - Parses README.md, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md
- **Platform file extraction** - Parses .github/, .gitlab/ templates, CODEOWNERS, dependabot.yml
- **IDE settings extraction** - Parses .editorconfig, .vscode/, .idea/, .phpstorm/
- **AI agent config extraction** - Parses .cursor/, .claude/, .windsurf/, copilot-instructions.md
- **Extraction summary** - Verbose mode shows all detected settings and their sources

## Running Scripts

### Generating AGENTS.md Files

To generate AGENTS.md files for a project:

```bash
scripts/generate-agents.sh /path/to/project
```

Options:
- `--dry-run` - Preview changes without writing files
- `--verbose` - Show detailed output
- `--style=thin` - Use thin root template (~30 lines, default)
- `--style=verbose` - Use verbose root template (~100-200 lines)
- `--update` - Update existing files only

### Validating Structure

To validate AGENTS.md structure compliance:

```bash
scripts/validate-structure.sh /path/to/project
```

Options:
- `--check-freshness, -f` - Also check if files are up to date with git commits
- `--verbose, -v` - Show detailed output

### Checking Freshness

To check if AGENTS.md files are up to date with recent git commits:

```bash
scripts/check-freshness.sh /path/to/project
```

This script:
- Extracts the "Last updated" date from the AGENTS.md header
- Checks git commits since that date for files in the relevant scope
- Reports if there are commits that might require AGENTS.md updates

Options:
- `--verbose, -v` - Show commit details and changed files
- `--threshold=DAYS` - Days threshold to consider stale (default: 7)

Example with full validation:
```bash
scripts/validate-structure.sh /path/to/project --check-freshness --verbose
```

### Detecting Project Type

To detect project language, version, and build tools:

```bash
scripts/detect-project.sh /path/to/project
```

### Detecting Scopes

To identify directories that should have scoped AGENTS.md files:

```bash
scripts/detect-scopes.sh /path/to/project
```

### Extracting Commands

To extract build commands from Makefile, package.json, composer.json, or go.mod:

```bash
scripts/extract-commands.sh /path/to/project
```

### Extracting Documentation

To extract information from README.md, CONTRIBUTING.md, SECURITY.md, and other documentation:

```bash
scripts/extract-documentation.sh /path/to/project
```

### Extracting Platform Files

To extract information from .github/, .gitlab/, CODEOWNERS, dependabot.yml, etc.:

```bash
scripts/extract-platform-files.sh /path/to/project
```

### Extracting IDE Settings

To extract information from .editorconfig, .vscode/, .idea/, etc.:

```bash
scripts/extract-ide-settings.sh /path/to/project
```

### Extracting AI Agent Configs

To extract information from .cursor/, .claude/, copilot-instructions.md, etc.:

```bash
scripts/extract-agent-configs.sh /path/to/project
```

### Verifying Content Accuracy

**CRITICAL: Always run this before considering AGENTS.md files complete.**

To verify that AGENTS.md content matches actual codebase state:

```bash
scripts/verify-content.sh /path/to/project
```

This script:
- Checks if documented files actually exist
- Verifies Makefile targets are real
- Compares module/script counts against actual files
- Reports undocumented files that should be added
- Reports documented files that don't exist

Options:
- `--verbose, -v` - Show detailed verification output
- `--fix` - Suggest fixes for common issues

**This verification step is MANDATORY when updating existing AGENTS.md files.**

## Using Reference Documentation

### AGENTS.md Analysis

When understanding best practices and patterns, consult `references/analysis.md` for analysis of 21 real-world AGENTS.md files.

### Directory Coverage

When determining which directories need AGENTS.md files, consult `references/directory-coverage.md` for guidance on PHP/TYPO3, Go, and TypeScript project structures.

### Real-World Examples

When needing concrete examples of AGENTS.md files, consult `references/examples/`:

| Project | Files | Description |
|---------|-------|-------------|
| `coding-agent-cli/` | Root + scripts scope | CLI tool example |
| `ldap-selfservice/` | Root + internal scopes | Go web app with multiple scopes |
| `simple-ldap-go/` | Root + examples scope | Go library example |
| `t3x-rte-ckeditor-image/` | Root + Classes scope | TYPO3 extension example |

## Using Asset Templates

### Root Templates

When generating root AGENTS.md files, the scripts use these templates:

- `assets/root-thin.md` - Minimal root template (~30 lines) with precedence rules and scope index
- `assets/root-verbose.md` - Detailed root template (~100 lines) with architecture overview and examples

### Scoped Templates

When generating scoped AGENTS.md files, the scripts use language-specific templates:

- `assets/scoped/backend-go.md` - Go backend patterns (packages, error handling, testing)
- `assets/scoped/backend-php.md` - PHP backend patterns (PSR, DI, security)
- `assets/scoped/cli.md` - CLI patterns (flags, output, error codes)
- `assets/scoped/frontend-typescript.md` - TypeScript frontend patterns (components, state, testing)

## Supported Project Types

| Language | Project Types |
|----------|---------------|
| Go | Libraries, web apps (Fiber/Echo/Gin), CLI (Cobra/urfave) |
| PHP | Composer packages, TYPO3, Laravel/Symfony |
| TypeScript | React, Next.js, Vue, Node.js |
| Python | pip, poetry, Django, Flask, FastAPI |
| Hybrid | Multi-language projects (auto-creates scoped files per stack) |

## Output Structure

### Root File

Root AGENTS.md (~30 lines) contains:
- Precedence statement
- Global rules
- Pre-commit checks
- Scope index

### Scoped Files

Scoped AGENTS.md files contain 9 sections:
1. Overview
2. Setup
3. Build/tests
4. Code style
5. Security
6. PR checklist
7. Examples
8. When stuck
9. House Rules

## Directory Coverage

When creating AGENTS.md files, create them in ALL key directories:

| Directory | Purpose |
|-----------|---------|
| Root | Precedence, architecture overview |
| `Classes/` or `src/` | Source code patterns |
| `Configuration/` or `config/` | Framework config |
| `Documentation/` or `docs/` | Doc standards |
| `Resources/` or `assets/` | Templates, assets |
| `Tests/` | Testing patterns |

---

> **Contributing:** https://github.com/netresearch/agents-skill
