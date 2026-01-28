---
name: multi-tool-pipeline
description: Advanced MCP skill demonstrating multi-tool orchestration with git repository analysis
---

# Multi-Tool Pipeline Skill

## When to Use This Skill

Use this Skill to:
- Learn multi-tool orchestration patterns
- Analyze git repositories
- Chain multiple MCP tools together
- Use as a template for complex workflows

This is a **demonstration skill** showing how to chain multiple MCP tools.

## What This Skill Does

Demonstrates advanced skill patterns:
1. Accept multiple CLI arguments
2. Chain multiple MCP tool calls sequentially
3. Process and combine results
4. Return structured output

**Pipeline:**
1. Get repository status (git__git_status)
2. Fetch recent commits (git__git_log)
3. Get branch information (git__git_branch)
4. Combine into summary

## Instructions

When you need to analyze a git repository, execute:

```bash
cd /home/khitomer/Projects/mcp-code-execution-enhanced

uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
    --repo-path "." \
    --max-commits 5
```

### Parameters

- `--repo-path`: Path to git repository (default: ".")
- `--max-commits`: Maximum number of commits to analyze (default: 10)

### Example Usage

```bash
# Analyze current repository
uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
    --repo-path "." \
    --max-commits 20

# Analyze different repository
uv run python -m runtime.harness scripts/multi_tool_pipeline.py \
    --repo-path "/path/to/repo" \
    --max-commits 5
```

## Expected Output

The skill returns structured data containing:
- Repository status
- Recent commits (up to max-commits)
- Branch information
- Summary metadata

Progress is printed during execution:
```
[1/3] Getting repository status...
[2/3] Fetching last N commits...
[3/3] Getting branch information...
✓ Pipeline complete
```

## MCP Servers Required

Configure a git-capable MCP server in `mcp_config.json`:

```json
{
  "mcpServers": {
    "git": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "."]
    }
  }
}
```

## Technical Notes

- **Pattern**: Sequential tool chaining with error handling
- **Token cost**: ~110 tokens (discovery + execution)
- **Time**: ~30 seconds for 3 tool calls
- **Demonstrates**:
  - Multiple CLI arguments
  - Tool orchestration
  - Result processing
  - Error handling

Use this as a template for creating custom multi-tool workflows.

## Creating Custom Workflows

Based on this pattern, you can create workflows that:
1. Accept CLI arguments (any parameters you need)
2. Call multiple MCP tools in sequence or parallel
3. Process intermediate results
4. Return final structured output

The CLI argument pattern keeps skills immutable while allowing flexible execution.
