---
name: mcp-converter
description: Converts MCP servers to Claude Skills to save tokens. Runs the introspection tool to generate skill wrappers.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, Write]
best_practices:
  - Use introspection to analyze MCP servers
  - Generate skill wrappers with progressive disclosure
  - Test converted skills before use
error_handling: graceful
streaming: supported
---

# MCP-to-Skill Converter

## 🚀 Usage

### 1. List Available MCP Servers

See which servers are configured in your `.mcp.json`:

```bash
python .claude/tools/mcp-converter/mcp_analyzer.py --list
```

### 2. Convert a Server

Convert a specific MCP server to a Skill:

```bash
python .claude/tools/mcp-converter/mcp_analyzer.py --server <server_name>
```

### 3. Batch Conversion (Catalog)

Convert multiple servers based on rules:

```bash
python .claude/tools/mcp-converter/batch_converter.py
```

## ℹ️ How it Works

1.  **Introspect**: Connects to the running MCP server.
2.  **Analyze**: Estimates token usage of tool schemas.
3.  **Generate**: Creates a `SKILL.md` wrapper that creates dynamic tool calls only when needed.

## 🔧 Dependencies

Requires `mcp` python package:

```bash
pip install mcp
```

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
