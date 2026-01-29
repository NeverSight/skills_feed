---
name: mcp-builder
description: This skill guides building high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services. Use when creating MCP servers, designing tool interfaces, or implementing protocol handlers.
---

# MCP Server Builder

## Overview

Build MCP servers that enable LLMs to interact with external services through thoughtfully designed tools.

**Key Principle**: Don't simply wrap API endpoints—build thoughtful, high-impact workflow tools.

## Four-Phase Development

### Phase 1: Research & Planning
- Study agent-centric design principles
- Review MCP protocol documentation
- Study target API documentation exhaustively
- Create detailed implementation plan

### Phase 2: Implementation
- Set up project structure
- Build core infrastructure (auth, request helpers, formatters)
- Implement tools with JSON Schema validation
- Follow language-specific best practices

### Phase 3: Review & Refine
- Code quality review (DRY, consistency, error handling)
- Test safely using evaluation harness
- Verify against quality checklist

### Phase 4: Create Evaluations
- Design 10 complex, realistic test questions
- Create XML-formatted evaluation files
- Verify answers independently

## Server Types

| Type | Transport | Use Case |
|------|-----------|----------|
| **stdio** | Process pipes | Local custom servers |
| **HTTP** | REST | Cloud-hosted servers |
| **SSE** | Server-Sent Events | Real-time updates |
| **WebSocket** | Bidirectional | Real-time communication |

## Tool Design

```typescript
// Good: Workflow-oriented
async function analyzeAndSummarize(url: string) {
  // Fetches, parses, and summarizes in one call
}

// Avoid: Simple API wrapper
async function fetchPage(url: string) {
  // Just wraps fetch()
}
```

## Implementation Standards

### TypeScript
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});
```

### Python (FastMCP)
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description."""
    return result
```

## Best Practices

1. **JSON Schema validation** on all inputs/outputs
2. **Comprehensive error handling** with meaningful messages
3. **Logging to stderr** (stdout reserved for protocol)
4. **Security-first** - validate inputs, manage sessions
5. **Configurable detail levels** for context efficiency
6. **Tool annotations** - mark read-only, destructive, idempotent
