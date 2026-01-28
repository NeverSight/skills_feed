---
name: build-my-context7
description: Build local Context7 documentation by downloading and filtering docs from manifests. Use when setting up or updating local documentation reference.
---

# Build My Context7

Download and filter documentation from manifests for Context7 integration.

## Quick Start

```
/build-my-context7              # Process ALL manifests
/build-my-context7 zod-docs     # Process only zod-docs manifest
```

Output goes to `output/`.

## Workflow

### Phase 1: Check Arguments

Check if `$ARGUMENTS` is provided:
- If **argument provided**: Process only that specific manifest
- If **no argument**: Process all manifests

### Phase 2: Discovery

**If processing a specific manifest:**
- Verify the manifest exists at `.claude/skills/download-docs/scripts/manifests/{argument}.json`
- If not found, list available manifests and ask user to choose

**If processing all manifests:**
- List all manifests:
```bash
ls .claude/skills/download-docs/scripts/manifests/*.json
```
- Extract manifest names (without .json extension)

### Phase 3: Processing

Spawn `manifest-processor` sub-agent(s):

```
Task tool call:
- subagent_type: manifest-processor
- prompt: "{manifest-name}"
```

The sub-agent handles everything:
- Downloads files from the manifest source
- Detects source type (URL vs GitHub)
- Applies AI filtering for GitHub sources (skips for URL sources)
- Returns a summary

**For multiple manifests**: Spawn ALL sub-agents in a SINGLE message for maximum parallelism.

### Phase 4: Summary

After sub-agent(s) complete, compile results into a summary table:

| Manifest | Source | Downloaded | Filtered | Final | Status |
|----------|--------|------------|----------|-------|--------|
| name     | url/github | N | N/N/A | N | ✅/❌ |

Remind user to run `/generate-agent-skills` if needed.

## Requirements

- `jq` - JSON parsing
- `git` - GitHub cloning
- `curl` - URL downloads
