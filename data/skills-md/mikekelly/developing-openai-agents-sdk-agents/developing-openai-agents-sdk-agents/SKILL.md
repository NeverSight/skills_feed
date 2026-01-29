---
name: developing-openai-agents-sdk-agents
description: Build, create, debug, review, implement, and optimize agentic AI applications using the OpenAI Agents SDK for TypeScript. Use when creating new agents, defining tools, implementing handoffs between agents, adding guardrails, debugging agent behavior, reviewing agent code, or orchestrating multi-agent systems with the @openai/agents package.
---

# Developing OpenAI Agents SDK Agents

Comprehensive workflow-driven skill for building production-ready agentic AI applications with the OpenAI Agents SDK.

<essential_principles>

## Core Concepts

**Agents are LLMs with structure**: An agent combines an LLM with instructions (system prompt), tools (functions it can call), handoffs (delegation targets), and optional guardrails (validators).

**Minimal abstractions**: The SDK provides primitives (Agent, tool, run) rather than heavyweight frameworks. You compose behavior through code, not configuration.

**Context injection**: Tools and instructions receive RunContext, enabling dependency injection of user data, database connections, or other runtime context without global state.

**Handoffs transfer ownership**: When one agent hands off to another, the target agent becomes the active conversational participant. This differs from tools (manager pattern) where the calling agent maintains control.

**Guardrails run in parallel**: Input guardrails can validate user input concurrently with the LLM call, reducing latency. Output guardrails check responses before returning them.

**Structured output is typed**: Using Zod schemas for outputType gives you compile-time type safety and runtime validation of agent responses.

**Human-in-the-loop is first-class**: Tools with needsApproval create interruptions that your code handles explicitly, enabling approval workflows without special infrastructure.

## Design Principles

**Start simple, add complexity as needed**: Begin with a single agent and basic tools. Add handoffs, guardrails, and orchestration only when requirements justify them.

**Test with real LLM calls**: Mocking LLMs hides emergent behavior. Use small models (gpt-4.1-mini) or cached prompts for fast iteration, but always test end-to-end.

**Make instructions specific**: Vague prompts ("be helpful") produce vague behavior. Specify the agent's role, available information, decision criteria, and output format.

**Tools are for actions, not data**: Don't create tools just to return static information. Put reference data in instructions or context. Tools should execute side effects or retrieve dynamic data.

**Fail explicitly**: Return error strings from tools rather than throwing exceptions. This lets the LLM see what went wrong and potentially retry with different parameters.

**Trace everything**: Enable tracing in development to understand agent decision-making. The SDK's built-in tracing shows tool calls, handoffs, and model reasoning.

</essential_principles>

<intake>

What would you like to do with OpenAI Agents SDK?

Common activities:
- Build a new agent or multi-agent system
- Add tools (functions) to an existing agent
- Implement agent handoffs (delegation)
- Add guardrails (validation)
- Debug agent behavior (unexpected actions, loops, errors)
- Review or optimize existing agent code
- Set up tracing and observability
- Implement human-in-the-loop approval flows
- Integrate with MCP servers
- Structure agent output with Zod schemas

</intake>

<routing>

| User wants to... | Route to workflow |
|-----------------|-------------------|
| Create a new agent from scratch | [workflows/build-new-agent.md](workflows/build-new-agent.md) |
| Add a tool (function) to an agent | [workflows/add-tool.md](workflows/add-tool.md) |
| Set up handoffs between agents | [workflows/implement-handoff.md](workflows/implement-handoff.md) |
| Add validation (guardrails) | [workflows/add-guardrails.md](workflows/add-guardrails.md) |
| Debug agent behavior | [workflows/debug-agent.md](workflows/debug-agent.md) |
| Review agent code quality | [workflows/review-agent-code.md](workflows/review-agent-code.md) |
| Set up structured output | [workflows/add-structured-output.md](workflows/add-structured-output.md) |
| Implement approval workflows | [workflows/implement-human-approval.md](workflows/implement-human-approval.md) |
| Add tracing/observability | [workflows/enable-tracing.md](workflows/enable-tracing.md) |
| Choose orchestration pattern | [workflows/choose-orchestration.md](workflows/choose-orchestration.md) |
| Integrate MCP servers | [workflows/integrate-mcp.md](workflows/integrate-mcp.md) |
| Optimize agent performance | [workflows/optimize-agent.md](workflows/optimize-agent.md) |

</routing>

<reference_index>

## Domain Knowledge References

- [references/architecture.md](references/architecture.md) - SDK architecture and design philosophy
- [references/agents.md](references/agents.md) - Agent configuration and lifecycle
- [references/tools.md](references/tools.md) - Tool definition patterns and best practices
- [references/handoffs.md](references/handoffs.md) - Delegation patterns and handoff mechanics
- [references/guardrails.md](references/guardrails.md) - Input/output validation strategies
- [references/orchestration.md](references/orchestration.md) - Multi-agent coordination patterns
- [references/context.md](references/context.md) - RunContext and dependency injection
- [references/structured-output.md](references/structured-output.md) - Typed responses with Zod
- [references/tracing.md](references/tracing.md) - Observability and debugging
- [references/model-configuration.md](references/model-configuration.md) - Model settings and parameters
- [references/anti-patterns.md](references/anti-patterns.md) - Common mistakes and how to avoid them
- [references/testing-strategies.md](references/testing-strategies.md) - How to test agentic systems

</reference_index>

<workflows_index>

## Step-by-Step Workflows

**Building**
- [workflows/build-new-agent.md](workflows/build-new-agent.md) - Create agent from scratch
- [workflows/add-tool.md](workflows/add-tool.md) - Add functions to agents
- [workflows/implement-handoff.md](workflows/implement-handoff.md) - Set up agent delegation
- [workflows/add-guardrails.md](workflows/add-guardrails.md) - Add validation
- [workflows/add-structured-output.md](workflows/add-structured-output.md) - Type-safe responses
- [workflows/implement-human-approval.md](workflows/implement-human-approval.md) - HITL workflows

**Architecting**
- [workflows/choose-orchestration.md](workflows/choose-orchestration.md) - Pick the right pattern
- [workflows/integrate-mcp.md](workflows/integrate-mcp.md) - MCP server integration

**Operating**
- [workflows/enable-tracing.md](workflows/enable-tracing.md) - Set up observability
- [workflows/debug-agent.md](workflows/debug-agent.md) - Fix misbehavior
- [workflows/review-agent-code.md](workflows/review-agent-code.md) - Code quality review
- [workflows/optimize-agent.md](workflows/optimize-agent.md) - Performance tuning

</workflows_index>
