---
name: mcp-development
description: Use when building "MCP server", "Model Context Protocol", creating "Claude tools", "MCP tools", or asking about "FastMCP", "MCP SDK", "tool development for LLMs", "external API integration for Claude"
version: 1.0.0
---

# MCP Server Development Guide

Build high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services.

---

## Core Design Principles

### Build for Workflows, Not Just APIs

| Principle | Why |
|-----------|-----|
| Consolidate operations | Single tool for complete tasks |
| Return high-signal data | Agents have limited context |
| Provide format options | "concise" vs "detailed" modes |
| Use human-readable IDs | Not technical codes |
| Make errors actionable | Guide toward correct usage |

**Key concept**: Don't just wrap API endpoints. Design tools that enable complete workflows agents actually need.

---

## Development Phases

### Phase 1: Research

| Step | Action |
|------|--------|
| Study MCP Protocol | Read `modelcontextprotocol.io/llms-full.txt` |
| Study SDK docs | Python or TypeScript SDK README |
| Study target API | Read ALL available documentation |
| Create implementation plan | Before writing code |

### Phase 2: Design

| Decision | Options |
|----------|---------|
| **Language** | Python (FastMCP) or TypeScript |
| **Tool granularity** | Atomic vs workflow-oriented |
| **Response format** | JSON, Markdown, or both |
| **Error handling** | What errors can occur, how to recover |

### Phase 3: Implementation

| Component | Purpose |
|-----------|---------|
| **Input validation** | Pydantic (Python) or Zod (TypeScript) |
| **Tool descriptions** | Clear, with examples |
| **Error messages** | Include suggested next steps |
| **Response formatting** | Consistent across tools |

### Phase 4: Testing

**Critical**: MCP servers are long-running processes. Never run directly in main process.

| Approach | How |
|----------|-----|
| Evaluation harness | Recommended |
| tmux session | Run server separately |
| Timeout wrapper | `timeout 5s python server.py` |
| MCP Inspector | Official debugging tool |

---

## Tool Annotations

| Annotation | Meaning | Default |
|------------|---------|---------|
| **readOnlyHint** | Doesn't modify state | false |
| **destructiveHint** | Can cause damage | true |
| **idempotentHint** | Repeated calls safe | false |
| **openWorldHint** | Interacts externally | true |

**Key concept**: Annotations help the LLM decide when and how safely to use tools.

---

## Input Design

### Validation Patterns

| Pattern | Use Case |
|---------|----------|
| Required fields | Core parameters |
| Optional with defaults | Convenience parameters |
| Enums | Limited valid values |
| Min/max constraints | Numeric bounds |
| Pattern matching | Format validation (email, URL) |

### Parameter Naming

| Good | Bad | Why |
|------|-----|-----|
| `user_email` | `e` | Self-documenting |
| `limit` | `max_results_to_return` | Concise but clear |
| `include_archived` | `ia` | Descriptive boolean |

---

## Response Design

### Format Options

| Format | Use Case |
|--------|----------|
| **JSON** | Programmatic use, structured data |
| **Markdown** | Human readability, reports |
| **Hybrid** | JSON in markdown code blocks |

### Response Guidelines

| Guideline | Why |
|-----------|-----|
| ~25,000 token limit | Context constraints |
| Truncate with indicator | Don't silently cut |
| Support pagination | `limit` and `offset` params |
| Include metadata | Total count, has_more |

---

## Error Handling

### Error Message Structure

| Element | Purpose |
|---------|---------|
| What failed | Clear description |
| Why it failed | Root cause if known |
| How to fix | Suggested next action |
| Example | Correct usage |

**Key concept**: Error messages should guide the agent toward correct usage, not just diagnose problems.

---

## Quality Checklist

### Code Quality

| Check | Description |
|-------|-------------|
| No duplicated code | Extract shared logic |
| Consistent formats | Similar ops return similar structure |
| Full error handling | All external calls wrapped |
| Type coverage | All inputs/outputs typed |
| Comprehensive docstrings | Every tool documented |

### Tool Quality

| Check | Description |
|-------|-------------|
| Clear descriptions | Model knows when to use |
| Good examples | In docstring |
| Sensible defaults | Reduce required params |
| Consistent naming | Group related with prefixes |

---

## Best Practices

| Practice | Why |
|----------|-----|
| One tool = one purpose | Clear mental model |
| Comprehensive descriptions | LLM selection accuracy |
| Include examples in docstrings | Show expected usage |
| Return actionable errors | Enable self-correction |
| Test with actual LLM | Real-world validation |
| Version your server | Track compatibility |

## Resources

- MCP Protocol: <https://modelcontextprotocol.io/>
- Python SDK: <https://github.com/modelcontextprotocol/python-sdk>
- TypeScript SDK: <https://github.com/modelcontextprotocol/typescript-sdk>
