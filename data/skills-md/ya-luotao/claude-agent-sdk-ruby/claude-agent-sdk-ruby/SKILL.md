---
name: claude-agent-sdk-ruby
description: Use when writing or refactoring Ruby code that integrates Claude Code via the claude-agent-sdk gem (ClaudeAgentSDK.query, ClaudeAgentSDK::Client, streaming input, ClaudeAgentOptions configuration, tools/permissions, MCP servers, hooks, structured output, budgets, sandboxing, session resumption/rewind, and Rails patterns like jobs or ActionCable).
---

# Claude Agent SDK for Ruby

## Quick start

- Use `ClaudeAgentSDK.query` for one-shot prompts (unidirectional streaming).
- Use `ClaudeAgentSDK::Client` for interactive sessions (multiple turns, interrupt, hooks, permission callbacks, custom tools).
- Install prerequisites: Ruby 3.2+, Node.js, and Claude Code CLI.

```ruby
require 'claude_agent_sdk'

ClaudeAgentSDK.query(prompt: "What is 2 + 2?") do |message|
  puts message.inspect
end
```

## Workflow

1. Choose an interface:
   - Use `ClaudeAgentSDK.query` for simple, stateless calls.
   - Use `ClaudeAgentSDK::Client` when you need bidirectional control (send multiple prompts, interrupt, change model/permissions, rewind files) or when using hooks/permission callbacks/custom tools.
2. Configure `ClaudeAgentSDK::ClaudeAgentOptions` (only what you need).
3. Handle messages:
   - Parse assistant text from content blocks.
   - Stop on `ClaudeAgentSDK::ResultMessage` (final result, cost, session_id, structured output).

## Use these references

- Read `references/message-handling.md` to extract text/tool blocks, capture `UserMessage#uuid` for rewind, and use `ResultMessage` fields.
- Read `references/options.md` to configure `ClaudeAgentOptions` (tools, permissions, output formats, budgets, sandbox, sessions).
- Read `references/mcp-servers.md` to define in-process SDK MCP tools/resources/prompts or configure external MCP servers.
- Read `references/rails.md` for background jobs, ActionCable streaming, and session resumption patterns.
- Read `references/troubleshooting.md` for common setup and runtime errors.
