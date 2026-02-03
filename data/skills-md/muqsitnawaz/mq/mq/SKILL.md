---
name: mq
description: Query markdown files efficiently with mq CLI. Use when exploring documentation structure, extracting specific sections, or reducing token usage when reading .md files.
---

# mq Skill: Efficient Document Querying

`mq` doesn't compute answers - it externalizes document structure into your context so you can reason to answers yourself.

```
Documents → mq query → Structure enters your context → You reason → Results
```

## The Pattern

```
1. See structure    →  mq <path> .tree           → Map enters your context
2. Find relevant    →  mq <path> '.search("x")'  → Locations enter your context
3. Extract content  →  mq <path> '.section("Y") | .text'  → Content enters your context
4. Reason           →  You compute the answer from what's now in your context
```

Your context accumulates structure. You do the final reasoning.

## Quick Reference

```bash
# Structure (your working index)
mq file.md .tree                    # Document structure
mq file.md '.tree("preview")'       # Structure + content previews
mq dir/ .tree                       # Directory overview
mq dir/ '.tree("full")'             # All files with sections + previews

# Search
mq file.md '.search("term")'        # Find sections containing term
mq dir/ '.search("term")'           # Search across all files

# Extract
mq file.md '.section("Name") | .text'   # Get section content
mq file.md '.code("python")'            # Get code blocks by language
mq file.md .links                       # Get all links
mq file.md .metadata                    # Get YAML frontmatter
```

## Efficient Workflow

### Starting: Get the Map

```bash
# For a single file
mq README.md .tree

# For a directory (start here for multi-file exploration)
mq docs/ '.tree("full")'
```

Output shows you the territory:
```
docs/ (7 files, 42 sections)
├── API.md (234 lines, 12 sections)
│   ├── # API Reference
│   │        "Complete reference for all REST endpoints..."
│   ├── ## Authentication
│   │        "All requests require Bearer token..."
```

Now you know: API.md has auth info, 234 lines, section called "Authentication".

### Finding: Narrow Down

If you need something specific but don't know where:

```bash
mq docs/ '.search("OAuth")'
```

Output points you to exact locations:
```
Found 3 matches for "OAuth":

docs/auth.md:
  ## Authentication (lines 34-89)
     "...OAuth 2.0 authentication flow..."
  ## OAuth Flow (lines 45-67)
```

Now you know: auth.md, section "OAuth Flow", lines 45-67.

### Extracting: Get Only What You Need

Don't read the whole file. Extract the section:

```bash
mq docs/auth.md '.section("OAuth Flow") | .text'
```

This returns just that section's content.

## Anti-Patterns

**Bad**: Reading entire files
```bash
cat docs/auth.md  # Wastes tokens on irrelevant content
```

**Good**: Query then extract
```bash
mq docs/auth.md .tree                           # See structure
mq docs/auth.md '.section("OAuth Flow") | .text'  # Get only what's needed
```

**Bad**: Re-querying structure you already have
```bash
mq docs/ .tree    # First time - good
mq docs/ .tree    # Again - wasteful, you already have this in context
```

**Good**: Use what's in your context
```bash
mq docs/ .tree    # Once - now you know the structure
# Use the structure you learned to make targeted queries
mq docs/auth.md '.section("OAuth") | .text'
```

## Context as Working Memory

Every mq output enters your context. Your context becomes a working index that grows as you explore:

```
Query 1: mq docs/ .tree
→ You now see: file list, line counts, section counts
→ You can reason: "auth.md looks relevant to my question"

Query 2: mq docs/auth.md .tree
→ You now see: auth.md's full section hierarchy
→ You can reason: "OAuth Flow section has what I need"

Query 3: mq docs/auth.md '.section("OAuth Flow") | .text'
→ You now have: the actual content
→ You can reason: compute the final answer
```

mq externalizes structure. You do the thinking. Don't re-query what you already see.

## Examples by Task

### "Find how authentication works"
```bash
mq docs/ '.search("auth")'           # Find relevant files/sections
mq docs/auth.md '.section("Overview") | .text'  # Read the overview
```

### "Get all Python examples"
```bash
mq docs/ '.tree("full")'             # Find files with examples
mq docs/examples.md '.code("python")'  # Extract all Python code
```

### "Understand the API structure"
```bash
mq docs/api.md .tree                 # See all endpoints/sections
mq docs/api.md '.section("Endpoints") | .tree'  # Drill into endpoints
mq docs/api.md '.section("POST /users") | .text'  # Get specific endpoint
```

### "Find configuration options"
```bash
mq . '.search("config")'             # Search entire project
mq config.md '.section("Options") | .text'  # Extract options
```
