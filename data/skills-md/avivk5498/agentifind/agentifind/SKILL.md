---
name: agentifind
description: Set up codebase intelligence for AI agents. Runs the agentifind CLI to extract code structure using LSP (pyright/tsserver) with tree-sitter fallback, then synthesizes a CODEBASE.md navigation guide. Run this skill to get a complete codebase map in .claude/ directory.
---

# Agentifind: Codebase Intelligence Setup

This skill sets up codebase intelligence by:
1. Running agentifind CLI to extract code structure
2. Detecting dynamic patterns that static analysis can't fully trace
3. Synthesizing a navigation guide with staleness metadata

## Procedure

### Step 1: Check for existing guide (Staleness Detection)

If `.claude/CODEBASE.md` already exists, check if it's stale:

1. Read the metadata header from CODEBASE.md:
   ```
   Source-Hash: {sha256 of codebase.json when guide was generated}
   Commit: {git commit when generated}
   Stats: {file count, function count, class count}
   ```

2. Compare against current state:
   - Run `sha256sum .claude/codebase.json` (or equivalent)
   - Run `git rev-parse HEAD`
   - Read current stats from codebase.json

3. **If metadata matches**: Guide is fresh. Ask user if they want to regenerate anyway.
4. **If metadata differs or missing**: Guide is stale. Proceed with regeneration.
5. **If no CODEBASE.md exists**: Proceed with generation.

### Step 2: Detect repo type and install LSP (if needed)

Check if this is a Terraform/IaC repository:

```bash
# Check for .tf files
find . -name "*.tf" -type f | head -1
```

**If Terraform files are found:**

Check if `terraform-ls` is installed. If not, install it for better parsing accuracy:

```bash
# Check if terraform-ls exists
which terraform-ls || echo "NOT_INSTALLED"
```

**If NOT_INSTALLED, install terraform-ls:**

```bash
# macOS (Homebrew)
brew install hashicorp/tap/terraform-ls

# Or via Go (cross-platform)
go install github.com/hashicorp/terraform-ls@latest
```

**Why terraform-ls matters:**
- Proper HCL parsing (not regex)
- Accurate module resolution
- Cross-file reference tracking
- Provider schema awareness

If installation fails, agentifind will fall back to regex parsing (still functional but less accurate).

### Step 3: Run agentifind sync

Execute the CLI to extract code structure:

```bash
npx agentifind@latest sync
```

**Extraction Method:**
- **LSP first** (if available): Uses language servers for accurate cross-file resolution
  - Python: `pyright-langserver` (install: `npm i -g pyright`)
  - TypeScript: `tsserver` (bundled with TypeScript)
  - Terraform: `terraform-ls` (install: `brew install hashicorp/tap/terraform-ls`)
  - **Note: LSP extraction can take 5-15 minutes on large codebases** (building reference graph)
- **Regex/Tree-sitter fallback**: Fast parsing when LSP unavailable (~30 seconds)

This creates `.claude/codebase.json` with:
- Module imports/exports
- Function and class definitions
- Call graph relationships (more accurate with LSP)
- Import dependencies

**Options:**
- `--skip-validate`: Skip linting/type checks (faster)
- `--verbose`: Show extraction method and progress
- `--if-stale`: Only sync if source files changed

### Step 4: Update .gitignore

Add the generated files to `.gitignore` (if not already present):

```
# Agentifind generated files
.claude/codebase.json
.claude/CODEBASE.md
.claude/.agentifind-checksum
```

These files are:
- **Regeneratable** from source code
- **Large** (codebase.json can be several MB)
- **Machine-specific** (paths may differ)

### Step 5: Read and analyze extracted data

Read `.claude/codebase.json` and analyze:
- `stats`: File/function/class counts
- `modules`: Per-file structure (imports, exports, classes, functions)
- `call_graph`: What functions call what
- `import_graph`: Module dependencies
- `analysis_gaps`: Gaps in call graph (see Step 6)
- `validation`: Lint/type issues (if present)

### Step 6: Review analysis gaps

The CLI automatically detects gaps in the call graph that may indicate dynamic patterns. Read `analysis_gaps` from codebase.json:

```json
{
  "analysis_gaps": {
    "uncalled_exports": [...],  // Exported functions with no callers
    "unused_imports": [...],    // Imports never referenced
    "orphan_modules": [...]     // Files never imported
  }
}
```

**How to interpret gaps:**

| Gap Type | What It Means | Likely Cause |
|----------|---------------|--------------|
| `uncalled_exports` | Exported function has no detected callers | Entry point, CLI command, API handler, test fixture, plugin hook, signal receiver, decorator-invoked |
| `unused_imports` | Import never referenced in code | Side-effect import, re-export, type-only import, dynamically accessed |
| `orphan_modules` | File never imported by anything | Entry point, script, config file, dynamically loaded plugin |

**Key insight:** If something is exported but never called, or imported but never used, static analysis cannot trace it. These are the areas where the call graph is incomplete.

**No manual scanning required** - the CLI does this automatically by analyzing the call graph structure.

### Step 7: Identify key components

From the data, determine:
- **Entry points**: Files with many importers (check import_graph reverse)
- **Core modules**: High export count, central in import graph
- **Utilities**: Imported by many, import few themselves
- **Request flow**: Trace call_graph from entry to output

### Step 8: Write CODEBASE.md

**First, check `repo_type` in codebase.json:**
- If `repo_type` is `"terraform"` → Use the **Infrastructure Template** below
- If `repo_type` is missing or other → Use the **Application Template** below

---

#### Application Template (default)

Create `.claude/CODEBASE.md` with this structure:

```markdown
# Codebase Guide

<!-- STALENESS METADATA - DO NOT EDIT -->
<!--
Generated: {ISO 8601 timestamp}
Source-Hash: {sha256 of codebase.json}
Commit: {git commit hash}
Stats: {files} files, {functions} functions, {classes} classes
-->

## ⚠️ Usage Instructions

This guide provides STARTING POINTS, not absolute truth.

**Before acting on any location:**
1. Verify the file exists with a quick Read
2. Confirm the symbol/function is still there
3. If something seems wrong, the guide may be stale - regenerate with `/agentifind`

**This guide CANNOT see:**
- Runtime behavior (dynamic imports, plugins, DI)
- Configuration-driven logic
- Database queries and their relationships
- External API integrations

## Quick Reference

| Component | Location |
|-----------|----------|
| {name} | `{path}` → `{symbol}` |

## Architecture

### Module Dependencies
{Key relationships from import_graph - focus on core modules}

### Data Flow
{Trace from call_graph if clear pattern exists}

## Analysis Gaps (Potential Dynamic Patterns)

{If analysis_gaps has items, list them here grouped by type}

### Uncalled Exports
{List from analysis_gaps.uncalled_exports - these are likely entry points, API handlers, or dynamically invoked}

| Symbol | File | Reason |
|--------|------|--------|
| {name} | `{file}:{line}` | {reason} |

### Orphan Modules
{List from analysis_gaps.orphan_modules - these are likely entry points or dynamically loaded}

| File | Reason |
|------|--------|
| `{file}` | {reason} |

**What this means:**
- Call graph is incomplete for these symbols/files
- They may be invoked via plugins, signals, decorators, CLI, or configuration
- Always trace execution manually when working in these areas
- Don't assume the call graph shows all callers

{If no gaps found, write: "No analysis gaps detected. Call graph appears complete."}

## Conventions
{Infer from naming patterns, file organization, directory structure}

## Impact Map

| If you change... | Also update... |
|------------------|----------------|
| `{high-dependency file}` | {N} dependent files |

## Known Issues
{From validation.linting/formatting/types if present, otherwise omit section}
```

---

#### Infrastructure Template (for Terraform/IaC repos)

When `repo_type` is `"terraform"`, create `.claude/CODEBASE.md` with this structure:

```markdown
# Infrastructure Guide

<!-- STALENESS METADATA - DO NOT EDIT -->
<!--
Generated: {ISO 8601 timestamp}
Source-Hash: {sha256 of codebase.json}
Commit: {git commit hash}
Stats: {files} files, {resources} resources, {modules} modules
-->

## ⚠️ Usage Instructions

This guide provides STARTING POINTS for infrastructure navigation.

**Before making changes:**
1. Verify the resource/module exists
2. Check the blast radius (what depends on this?)
3. Review variable dependencies
4. Consider state implications

**This guide CANNOT see:**
- Remote state data
- Dynamic values from data sources
- Provider-specific behaviors
- Secrets in tfvars files

## Infrastructure Overview

| Provider | Resources | Modules |
|----------|-----------|---------|
{For each provider in stats.providers, count resources}

## Module Structure

{List from modules array, show source and dependencies}

```
modules/
├── {module.name}/  → {module.source}
│   └── inputs: {list key variables}
```

## Resource Inventory

{Group resources by type from resources object}

### {Provider} Resources
| Type | Name | File | Dependencies |
|------|------|------|--------------|
| {type} | {name} | `{file}:{line}` | {dependencies.length} deps |

## Variable Flow

{List from variables array}

| Variable | Type | Used By | Default |
|----------|------|---------|---------|
| {name} | {type} | {used_by.length} resources | {default or "required"} |

## Blast Radius (High Risk)

{List from blast_radius where severity is "high" or "medium"}

⚠️ **Changing these resources affects many dependents:**

| Resource | Affected | Severity |
|----------|----------|----------|
| {target} | {affected_resources.length} resources | {severity} |

**Before modifying high-risk resources:**
- Run `terraform plan` to preview changes
- Consider using `terraform state mv` for refactoring
- Check if changes will force recreation

## Outputs

{List from outputs array}

| Output | Value | Referenced |
|--------|-------|------------|
| {name} | {value} | {references} |

## Dependency Graph

{Describe key relationships from dependency_graph}

Key dependencies:
- `{resource A}` → depends on → `{resource B}`
```

### Step 9: Confirm completion

**For application repos**, report:
- Files analyzed (from stats.files)
- Symbols extracted (from stats.functions + stats.classes)
- Extraction method used (LSP or tree-sitter)
- Key entry points identified
- **Analysis gaps detected** (count of uncalled_exports, orphan_modules)
- Any validation issues found
- Guide staleness metadata recorded

**For Terraform/IaC repos**, report:
- Files analyzed (from stats.files)
- Resources extracted (from stats.resources)
- Modules detected (from stats.modules)
- Providers used (from stats.providers)
- **High-risk resources** (count from blast_radius with severity "high")
- Variables defined vs used
- Guide staleness metadata recorded

### Step 10: Offer to update agent instructions

Check if `CLAUDE.md` or `AGENTS.md` exists in the project root.

Ask the user:
> "Would you like me to add an instruction to your {CLAUDE.md/AGENTS.md} file so the agent automatically uses the CODEBASE.md for navigation?"

**If user accepts:**

Append this section to the file (or create `AGENTS.md` if neither exists):

```markdown
## Codebase Navigation

Before exploring the codebase, read `.claude/CODEBASE.md` for architecture overview, key files, and conventions. This file is auto-generated by agentifind and provides:
- Quick reference to key components
- Module dependencies and data flow
- Dynamic patterns that static analysis can't trace
- Coding conventions
- Impact map for changes

**Important:** The guide provides starting points. Always verify locations before making changes.
```

If both `CLAUDE.md` and `AGENTS.md` exist, update `CLAUDE.md` (takes precedence).

**If user declines:**

Respond with:
> "No problem! If you change your mind, add this to your CLAUDE.md or AGENTS.md file:"
>
> ```markdown
> ## Codebase Navigation
>
> Before exploring the codebase, read `.claude/CODEBASE.md` for architecture overview, key files, and conventions.
> ```

## Output

```
.claude/
├── codebase.json         # Structured extraction (CLI output)
├── CODEBASE.md           # Navigation guide (this skill's output)
└── .agentifind-checksum  # Staleness detection
```

## Notes

- Ground ALL claims in the extracted data - do not hallucinate relationships
- Keep the guide concise - focus on navigation over explanation
- Prioritize "what" and "where" over "why" and "how"
- If codebase.json already exists and is recent, skip Step 2
- LSP extraction is slower but more accurate for cross-file references
- Tree-sitter is faster but uses heuristic-based resolution
- **Always include the staleness metadata header** - it enables future freshness checks
- **Always include the analysis gaps section** - even if none found, document that the call graph is complete
