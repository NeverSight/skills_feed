---
name: openai-agents-sdk-guidelines
description: OpenAI Agents SDK (Python) implementation guidelines. Use when building, reviewing, or troubleshooting agent workflows including tools, handoffs, guardrails, context management, streaming, MCP integration, and Runner configuration. Triggers on requests like "build an agent", "add handoffs", "set up guardrails", "configure tools", or "implement streaming".
license: MIT
metadata:
  author: local
  version: "1.0.0"
---

# OpenAI Agents SDK Guidelines

Comprehensive implementation guide for the OpenAI Agents Python SDK, designed for AI agents and LLMs. Contains 30+ rules across 8 categories, prioritized by impact from critical (agent design, multi-agent patterns) to incremental (streaming, advanced patterns). Each rule includes detailed explanations, code examples comparing incorrect vs. correct implementations, and specific guidance for automated code generation and review.

## When to Apply

Reference these guidelines when:
- Creating new agents with the OpenAI Agents SDK
- Implementing multi-agent workflows (manager pattern or handoffs)
- Adding tools (function tools, hosted tools, agents-as-tools)
- Configuring guardrails for input/output validation
- Managing context and conversation state
- Setting up streaming for real-time updates
- Integrating MCP servers

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Agent Design | CRITICAL | `agent-` |
| 2 | Multi-Agent Patterns | CRITICAL | `multi-agent-` |
| 3 | Tools | HIGH | `tool-` |
| 4 | Guardrails | MEDIUM-HIGH | `guardrail-` |
| 5 | Context Management | MEDIUM | `context-` |
| 6 | Running Agents | MEDIUM | `runner-` |
| 7 | Conversation Management | MEDIUM | `conversation-` |
| 8 | Streaming & Advanced | LOW-MEDIUM | `streaming-` |

## Quick Reference

### 1. Agent Design (CRITICAL)

- `agent-basic-config` - Configure name, instructions, model, and tools
- `agent-output-type` - Use Pydantic models for structured outputs
- `agent-dynamic-instructions` - Use functions for context-aware prompts
- `agent-tool-choice` - Force specific tool usage with ModelSettings
- `agent-tool-use-behavior` - Control how tool outputs are processed
- `agent-reset-tool-choice` - Prevent infinite tool loops

### 2. Multi-Agent Patterns (CRITICAL)

- `multi-agent-manager-pattern` - Use agents-as-tools for centralized orchestration
- `multi-agent-handoffs` - Use handoffs for decentralized delegation
- `multi-agent-handoff-description` - Add handoff descriptions for routing
- `multi-agent-handoff-inputs` - Capture LLM-provided data during handoffs
- `multi-agent-input-filter` - Filter conversation history on handoffs

### 3. Tools (HIGH)

- `tool-function-decorator` - Use @function_tool for automatic schema
- `tool-docstrings` - Write clear docstrings for tool descriptions
- `tool-context-parameter` - Access RunContextWrapper in tools
- `tool-error-handling` - Handle errors with failure_error_function
- `tool-agents-as-tools` - Expose agents as callable tools
- `tool-conditional-enabling` - Dynamically enable/disable tools

### 4. Guardrails (MEDIUM-HIGH)

- `guardrail-input-validation` - Validate user input with input guardrails
- `guardrail-output-validation` - Validate agent output with output guardrails
- `guardrail-tripwire` - Use tripwires to halt execution on failure
- `guardrail-execution-mode` - Choose parallel vs blocking execution
- `guardrail-tool-guardrails` - Wrap function tools with guardrails

### 5. Context Management (MEDIUM)

- `context-local-context` - Use RunContextWrapper for dependencies
- `context-type-consistency` - Keep context type consistent across agents
- `context-llm-visibility` - Make data available to LLMs via instructions/tools
- `context-tool-context` - Use ToolContext for tool metadata

### 6. Running Agents (MEDIUM)

- `runner-async-vs-sync` - Choose run() vs run_sync() appropriately
- `runner-max-turns` - Set max_turns to prevent infinite loops
- `runner-run-config` - Configure global settings with RunConfig
- `runner-exception-handling` - Handle SDK exceptions properly

### 7. Conversation Management (MEDIUM)

- `conversation-manual-history` - Use to_input_list() for manual management
- `conversation-sessions` - Use Sessions for automatic history
- `conversation-server-managed` - Use conversation_id for server-side state

### 8. Streaming & Advanced (LOW-MEDIUM)

- `streaming-run-streamed` - Use run_streamed() for real-time updates
- `streaming-raw-events` - Handle raw LLM response events
- `streaming-item-events` - Handle high-level run item events

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/agent-basic-config.md
rules/multi-agent-handoffs.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
