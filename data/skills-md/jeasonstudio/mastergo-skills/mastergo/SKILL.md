---
name: mastergo
description: Retrieve and analyze MasterGo design DSL data. Use when users provide MasterGo links (https://mastergo.com/file/xxx or /goto/xxx) to fetch design structure, component documentation, and DSL metadata.
---

# MasterGo Skill

Retrieve and analyze design data from MasterGo files using self-contained Python scripts.

## Prerequisites

**Environment variable required:**

```bash
export MASTERGO_TOKEN="mg_your_token_here"
```

Get token: MasterGo Settings > Security > Personal Access Token

**Requirements**: Team Edition account, files in Team Projects (not Drafts).

### CRITICAL: Secure Token Handling

**NEVER do this:**
- `echo $MASTERGO_TOKEN` - exposes secret in output
- `echo "Token: $MASTERGO_TOKEN"` - exposes secret
- `printenv MASTERGO_TOKEN` - exposes secret
- Any command that prints the token value

**Secure verification method:**

```bash
test -n "$MASTERGO_TOKEN" && echo "Token is set" || echo "Token is NOT set"
```

This only prints whether the token exists, never its value.

## Script Location

Scripts are in `scripts/` relative to this SKILL.md file. Use absolute path when executing:

```
{this_skill_directory}/scripts/mastergo_*.py
```

## Workflow

### Step 1: Analyze DSL Structure

**Always analyze first** to understand the page structure:

```bash
python scripts/mastergo_analyze.py "https://mastergo.com/goto/xxx"
```

Output shows:
- Node tree (type, name, size)
- Text contents
- Component doc links
- Navigation targets

### Step 2: Get Full DSL (if needed)

For detailed DSL data:

```bash
python scripts/mastergo_get_dsl.py "https://mastergo.com/goto/xxx"
```

Output: JSON with `{ dsl, componentDocumentLinks, rules }`

### Step 3: Fetch Component Docs

If `componentDocumentLinks` is non-empty, fetch relevant docs:

```bash
python scripts/mastergo_get_dsl.py URL | python scripts/mastergo_fetch_docs.py --from-dsl
```

Or fetch individually:

```bash
python scripts/mastergo_fetch_docs.py "https://example.com/button.mdx"
```

## Scripts Reference

| Script | Purpose | Output |
|--------|---------|--------|
| `mastergo_analyze.py` | Structure summary | Human-readable tree to stdout |
| `mastergo_get_dsl.py` | Full DSL data | JSON to stdout |
| `mastergo_fetch_docs.py` | Component docs | Doc content to stdout |
| `mastergo_utils.py` | Utility functions | Import as module |

## DSL Key Concepts

- **`token` fields**: Design tokens for colors, shadows, fonts (convert to CSS variables when generating code)
- **`componentInfo`**: Component metadata including documentation links
- **`interactive` fields**: User interactions including page navigation targets
- **`rules` array**: Guidelines returned with DSL response

## CRITICAL: Do NOT Pollute User Projects

**FORBIDDEN actions:**
- Creating `.temp_dsl.json` or any DSL cache file in user project
- Creating `analyze_dsl.py` or any analysis script in user project
- Creating any temporary files in user project directory
- Writing any skill-related files outside of skill directory

**ALLOWED:**
- Running scripts and capturing stdout output
- Using output directly in memory
- Reading user's existing project files for context

All script output goes to **stdout only**. Use the output directly; do not save intermediate files to user's project.

## References

- [references/dsl-types.md](references/dsl-types.md) - Complete DSL type definitions
- [references/dsl-structure.md](references/dsl-structure.md) - Key fields and patterns
- [references/multi-page-workflow.md](references/multi-page-workflow.md) - Multi-page workflow
