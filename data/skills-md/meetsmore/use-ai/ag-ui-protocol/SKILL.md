---
name: ag-ui-protocol
description: AG-UI (Agent-User Interaction) protocol reference for building AI agent frontends. Use when implementing AG-UI events (RUN_STARTED, TEXT_MESSAGE_*, TOOL_CALL_*, STATE_*), building agents that communicate with frontends, implementing streaming responses, state management with snapshots/deltas, tool call lifecycles, or debugging AG-UI event flows.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Edit
  - Bash
---

# AG-UI Protocol

The Agent-User Interaction (AG-UI) Protocol is an open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications.

## When to Use This Skill

Use this skill when:
- Implementing AG-UI protocol events in your code
- Building agents that communicate with frontends via AG-UI
- Understanding the event types and their structure
- Implementing state management, tool calls, or message streaming
- Debugging AG-UI event flows

## Documentation

See the `docs/2025-11-27/` directory for complete AG-UI protocol documentation:

- `introduction.md` - Protocol overview and integrations
- `concepts/architecture.md` - Core architecture and design
- `concepts/events.md` - Event types and patterns
- `concepts/messages.md` - Message structure and types
- `concepts/state.md` - State management and synchronization
- `concepts/tools.md` - Tool definitions and lifecycle
- `concepts/agents.md` - Agent implementation
- `concepts/middleware.md` - Middleware patterns
- `concepts/serialization.md` - Event serialization and compaction
- `quickstart/introduction.md` - Getting started guide
- `quickstart/server.md` - Server implementation
- `quickstart/clients.md` - Client implementation

## Quick Reference

### Event Types

```typescript
enum EventType {
  // Lifecycle
  RUN_STARTED = "RUN_STARTED",
  RUN_FINISHED = "RUN_FINISHED",
  RUN_ERROR = "RUN_ERROR",
  STEP_STARTED = "STEP_STARTED",
  STEP_FINISHED = "STEP_FINISHED",

  // Text Messages
  TEXT_MESSAGE_START = "TEXT_MESSAGE_START",
  TEXT_MESSAGE_CONTENT = "TEXT_MESSAGE_CONTENT",
  TEXT_MESSAGE_END = "TEXT_MESSAGE_END",

  // Tool Calls
  TOOL_CALL_START = "TOOL_CALL_START",
  TOOL_CALL_ARGS = "TOOL_CALL_ARGS",
  TOOL_CALL_END = "TOOL_CALL_END",

  // State
  STATE_SNAPSHOT = "STATE_SNAPSHOT",
  STATE_DELTA = "STATE_DELTA",
  MESSAGES_SNAPSHOT = "MESSAGES_SNAPSHOT",

  // Custom
  RAW = "RAW",
  CUSTOM = "CUSTOM",
}
```

### Event Patterns

1. **Start-Content-End**: Streams content incrementally (text, tool arguments)
2. **Snapshot-Delta**: State synchronization using complete snapshots + JSON Patch updates
3. **Lifecycle**: Run monitoring with mandatory start/end events

### Message Roles

- `user` - User messages (text and multimodal)
- `assistant` - AI responses (text and tool calls)
- `system` - Instructions or context
- `tool` - Tool execution results
- `activity` - Progress updates
- `developer` - Internal debugging

### Tool Definition Structure

```typescript
interface Tool {
  name: string;           // Unique identifier
  description: string;    // Purpose explanation
  parameters: JSONSchema; // Accepted arguments
}
```

### Tool Call Lifecycle

1. `TOOL_CALL_START` - Initiates with unique ID
2. `TOOL_CALL_ARGS` - Streams JSON arguments
3. `TOOL_CALL_END` - Marks completion

### State Synchronization

- **STATE_SNAPSHOT** - Complete state replacement
- **STATE_DELTA** - Incremental JSON Patch (RFC 6902) updates

## Source

Documentation downloaded from: https://github.com/ag-ui-protocol/ag-ui/tree/main/docs
