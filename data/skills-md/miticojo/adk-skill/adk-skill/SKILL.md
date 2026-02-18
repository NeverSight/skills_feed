---
name: adk-skill
description: "Build single-agent and multi-agent systems using Google's Agent Development Kit (ADK) in Python, Java, Go, or TypeScript. Use when user says 'build an agent with ADK', 'create a Gemini agent', 'multi-agent pipeline', 'agent orchestration with Google', or mentions ADK, google-adk, google agent development kit, sequential/parallel/loop agents, agent tools, callbacks, state management, agent testing, or agent deployment with Gemini. Do NOT use for LangChain, CrewAI, AutoGen, or non-ADK agent frameworks."
license: MIT
compatibility: "Requires Python 3.10+ (or Java 17+, Go 1.22+, Node 18+). Needs google-adk package. Requires GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT env var."
metadata:
  author: community
  version: "1.1"
  mcp-server: adk-docs
---

# Google Agent Development Kit (ADK) Guide

## Overview

ADK is Google's open-source framework for building AI agents powered by Gemini models. It supports single-agent and multi-agent architectures with built-in tool integration, state management, callbacks, guardrails, and deployment options.

## Critical Rules

1. **Every agent package MUST have `__init__.py`** that imports the agent module: `from . import agent`
2. **Entry point MUST be `root_agent`** -- a module-level variable in `agent.py` (Python). Not `agent`, not `my_agent`.
3. **Set `GOOGLE_API_KEY` in `.env`** or configure Vertex AI credentials before running.
4. **Always set `max_iterations` on `LoopAgent`** to prevent unbounded execution.
5. **One agent = one responsibility.** Split agents with 5+ tools into specialists.
6. **Use `output_key` + `output_schema`** for reliable data flow between agents -- not free text.

## Documentation & Resources

For up-to-date API references and detailed guides beyond this skill, always consult:
- **ADK Docs Index**: https://google.github.io/adk-docs/llms.txt
- **Official Samples**: https://github.com/google/adk-samples (Python, Java, TypeScript)

## Supported Languages

| Language | Package | Install |
|----------|---------|---------|
| Python | `google-adk` | `pip install google-adk` |
| Java | `com.google.adk:google-adk` | Maven/Gradle |
| Go | `google.golang.org/adk` | `go get` |
| TypeScript | `@google/adk` | `npm install @google/adk` |

This guide shows Python examples. For Java, Go, and TypeScript patterns, see [references/multi-language.md](references/multi-language.md).

## Quick Reference

| Task | Approach |
|------|----------|
| Single agent | `Agent` or `LlmAgent` with tools and instructions |
| Sequential pipeline | `SequentialAgent` with ordered sub_agents |
| Parallel execution | `ParallelAgent` with independent sub_agents |
| Iterative refinement | `LoopAgent` with max_iterations or checker agent |
| Agent-as-tool | Wrap agent with `AgentTool` for on-demand delegation |
| Remote agent (A2A) | `RemoteA2aAgent` + `to_a2a()` for cross-service agents |
| Custom tools | Python functions with type hints + docstrings |
| Structured output | Pydantic model via `output_schema` + `output_key` |
| State management | `callback_context.state` and `tool_context.state` |
| MCP integration | `MCPToolset` with connection params |
| Testing | `pytest` with `InMemoryRunner` |
| Evaluation | EvalSet with `.test.json`, `adk eval` CLI, pytest |

---

## Project Structure

Every ADK project follows this layout:

```
my_agent/
├── my_agent/
│   ├── __init__.py          # Must import agent module
│   ├── agent.py             # Defines root_agent (entry point)
│   ├── prompts.py           # Instruction strings (optional)
│   ├── tools.py             # Custom tool functions (optional)
│   ├── sub_agents/          # Sub-agent packages (optional)
│   └── shared_libraries/    # Callbacks, utilities (optional)
├── tests/
│   └── test_agent.py
├── pyproject.toml
└── .env                     # GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT
```

### Critical: __init__.py

```python
# my_agent/__init__.py
from . import agent
```

### Critical: root_agent

The `root_agent` variable at module level is the framework entry point:

```python
# my_agent/agent.py
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.5-flash",
    description="Brief description for agent discovery",
    instruction="Detailed system prompt...",
    tools=[...],
)
```

### pyproject.toml

Minimal config: `requires-python = ">=3.10"`, `dependencies = ["google-adk"]`, build-backend `setuptools`. For full example and environment config, see [references/advanced-patterns.md](references/advanced-patterns.md).

---

## Agent Types

### 1. LlmAgent (Single Agent)

The fundamental building block. Wraps a single LLM call with tools and instructions.

```python
from google.adk.agents import LlmAgent

agent = LlmAgent(
    name="assistant",
    model="gemini-2.5-flash",
    description="General assistant",
    instruction="""You are a helpful assistant.
    Use the search tool when you need current information.""",
    tools=[search_tool],
    output_schema=ResponseModel,   # Optional structured output
    output_key="response",         # State key for output
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
    ),
)
```

### 2. SequentialAgent

Runs sub-agents in order. Output of each flows to the next via shared state.

```python
from google.adk.agents import SequentialAgent

pipeline = SequentialAgent(
    name="research_pipeline",
    description="Research then summarize",
    sub_agents=[
        researcher_agent,    # Step 1: writes to state["research"]
        summarizer_agent,    # Step 2: reads state["research"]
    ],
)
```

### 3. ParallelAgent

Runs sub-agents concurrently. Use for independent tasks.

```python
from google.adk.agents import ParallelAgent

parallel = ParallelAgent(
    name="multi_channel",
    description="Send to all channels simultaneously",
    sub_agents=[
        email_agent,
        slack_agent,
        calendar_agent,
    ],
)
```

### 4. LoopAgent

Repeats sub-agents until termination. Two termination patterns:

**Pattern A: Fixed iterations**
```python
from google.adk.agents import LoopAgent

loop = LoopAgent(
    name="refinement_loop",
    description="Iteratively refine output",
    sub_agents=[writer_agent, critic_agent],
    max_iterations=3,
)
```

**Pattern B: Checker agent with escalate**
```python
# The checker agent uses tool_context.actions.escalate = True to stop
def check_quality(score: float, tool_context: ToolContext) -> str:
    """Check if quality meets threshold."""
    if score >= 0.9:
        tool_context.actions.escalate = True
        return "Quality threshold met, stopping loop."
    return "Quality below threshold, continuing refinement."

checker = Agent(
    name="checker",
    model="gemini-2.5-flash",
    instruction="Evaluate the output quality and call check_quality.",
    tools=[check_quality],
)

loop = LoopAgent(
    name="quality_loop",
    sub_agents=[generator_agent, checker],
)
```

### 5. Composing Agent Types

Nest agent types freely for complex workflows. Example: `SequentialAgent` containing a `ParallelAgent` containing `LlmAgent`s. See [references/advanced-patterns.md](references/advanced-patterns.md) for hierarchical workflow examples.

---

## Tools

### Function Tools

Any Python function with type hints and a docstring becomes a tool:

```python
def get_weather(city: str, units: str = "celsius") -> dict:
    """Get current weather for a city.

    Args:
        city: The city name to look up weather for.
        units: Temperature units - 'celsius' or 'fahrenheit'.

    Returns:
        dict with temperature, conditions, and humidity.
    """
    # Implementation
    return {"temperature": 22, "conditions": "sunny", "humidity": 45}

agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    instruction="Help users check the weather.",
    tools=[get_weather],
)
```

**Requirements:**
- Type hints on all parameters
- Docstring with description and Args section
- Return type annotation

### Tools with State Access

Use `ToolContext` to read/write session state:

```python
from google.adk.tools import ToolContext

def add_to_cart(item: str, quantity: int, tool_context: ToolContext) -> dict:
    """Add an item to the shopping cart."""
    cart = tool_context.state.get("cart", [])
    cart.append({"item": item, "quantity": quantity})
    tool_context.state["cart"] = cart
    return {"status": "added", "cart_size": len(cart)}
```

### AgentTool (Agent-as-Tool)

Wrap an agent to use it as a tool for another agent:

```python
from google.adk.tools.agent_tool import AgentTool

specialist = Agent(
    name="code_reviewer",
    model="gemini-2.5-pro",
    instruction="Review code for bugs and best practices.",
)

coordinator = Agent(
    name="coordinator",
    model="gemini-2.5-flash",
    instruction="Coordinate tasks. Use code_reviewer for code reviews.",
    tools=[AgentTool(agent=specialist)],
)
```

### Built-in Tools

```python
from google.adk.tools import google_search

agent = Agent(
    name="researcher",
    tools=[google_search],
)
```

### MCP Tools

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from mcp import StdioServerParameters

agent = Agent(
    name="db_agent",
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "some-mcp-server"],
                ),
            ),
        ),
    ],
)
```

For advanced tool patterns (FunctionTool, ToolboxToolset, long-running tools), see [references/tools-reference.md](references/tools-reference.md).

---

## Callbacks

Callbacks intercept the agent lifecycle. Return `None` to proceed, return a value to short-circuit.

| Callback | Signature | Use Case |
|----------|-----------|----------|
| `before_agent_callback` | `(CallbackContext)` | Initialize state |
| `before_tool_callback` | `(BaseTool, dict, CallbackContext) -> dict\|None` | Validate inputs, auto-approve |
| `after_tool_callback` | `(BaseTool, dict, ToolContext, dict) -> dict\|None` | Post-process results |
| `before_model_callback` | `(CallbackContext, LlmRequest)` | Rate limit, safety filter |

```python
def before_tool(tool, args, tool_context) -> dict | None:
    """Return dict to skip tool execution with that response."""
    if tool.name == "approve_discount" and args.get("value", 0) > 50:
        return {"status": "rejected", "reason": "Discount too large"}
    return None  # Proceed normally

agent = Agent(
    name="guarded_agent",
    model="gemini-2.5-flash",
    instruction="...",
    before_tool_callback=before_tool,
)
```

For rate limiting, input validation, and safety callbacks, see [references/advanced-patterns.md](references/advanced-patterns.md).

---

## State Management

State is a shared dictionary across agents, tools, and callbacks. Scopes: `state["key"]` (session), `app:key` (app-wide), `user:key` (user-wide).

**Passing data between agents:** Use `output_key` to write to state, read in next agent's instruction:

```python
researcher = Agent(name="researcher", output_key="findings", output_schema=ResearchOutput, ...)
writer = Agent(name="writer", instruction="Write report based on state['findings'].", ...)
pipeline = SequentialAgent(name="pipeline", sub_agents=[researcher, writer])
```

---

## Structured Output

Use Pydantic models for typed, validated agent output:

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    key_findings: list[str]
    confidence: float
    recommendations: list[str]

agent = Agent(
    name="analyzer",
    model="gemini-2.5-flash",
    instruction="Analyze the provided data and return structured results.",
    output_schema=AnalysisResult,
    output_key="analysis",  # Stored in state["analysis"]
)
```

---

## Running and Testing

### Local Development

```bash
# Install
pip install google-adk

# Set API key
export GOOGLE_API_KEY="your-key"

# Run interactively
adk run my_agent

# Run with web UI
adk web my_agent
```

### Testing with InMemoryRunner

```python
import pytest
from google.adk.runners import InMemoryRunner
from google.genai import types

@pytest.mark.asyncio
async def test_agent():
    runner = InMemoryRunner(agent=root_agent, app_name="test")
    session = await runner.session_service.create_session(
        user_id="test_user", app_name="test",
    )
    content = types.Content(
        role="user", parts=[types.Part.from_text(text="Hello")],
    )
    events = []
    async for event in runner.run_async(
        user_id="test_user", session_id=session.id, new_message=content,
    ):
        events.append(event)
    assert "expected" in events[-1].content.parts[0].text.lower()
```

### Evaluation

ADK provides built-in evaluation for tool correctness, response quality, and safety. Define eval cases in `.test.json` files and run with `adk eval`, `pytest`, or the web UI. See [references/evaluation.md](references/evaluation.md) for eval data formats, all 8 metrics, and patterns.

---

## Model Selection

Use `gemini-2.5-flash` for most agents (fast, cost-effective). Use `gemini-2.5-pro` for complex reasoning. Configure via `generate_content_config=types.GenerateContentConfig(temperature=0.2)`.

---

## Design Patterns

| Pattern | When to Use | ADK Implementation |
|---------|------------|-------------------|
| Sequential pipeline | Multi-step tasks with dependencies | `SequentialAgent` with ordered sub-agents |
| Fan-out / Fan-in | Independent tasks then synthesis | `ParallelAgent` → merger `Agent` |
| Reflection loop | Quality matters more than speed | `LoopAgent` with producer + critic agents |
| Dynamic routing | Diverse inputs need different handling | Parent `Agent` with `sub_agents` (Auto-Flow) |
| Layered fallback | Tool failures need graceful recovery | `SequentialAgent`: primary → fallback → response |
| Guardrailed agent | Safety/compliance requirements | `before_model_callback` + `before_tool_callback` |
| Resource tiering | Cost optimization under constraints | Different `model` per agent (Pro vs Flash) |

**Key design rules:**
- Split agents with 5+ tools into focused specialists. One agent = one responsibility.
- Pass data between agents via `output_key` + `output_schema` (Pydantic) -- never rely on free text.
- Set `max_iterations` on every `LoopAgent`. No exceptions.
- Separate generation from evaluation -- use a different agent to critique (avoids self-review bias).
- Write precise sub-agent `description` fields -- they drive Auto-Flow routing decisions.
- Embed reasoning steps in instructions: "1. Analyze 2. Plan 3. Execute 4. Verify".
- Include a fallback route for unclear inputs -- ambiguous requests must not be silently misrouted.

For hierarchical workflows, agent transfer, and deployment patterns, see [references/advanced-patterns.md](references/advanced-patterns.md).
For comprehensive design patterns (chaining, reflection, planning, memory, error handling, HITL, guardrails, RAG, resource optimization, reasoning, evaluation, prompting), see [references/design-patterns.md](references/design-patterns.md).
For A2A (Agent-to-Agent) protocol patterns -- exposing agents as A2A servers, consuming remote agents with `RemoteA2aAgent`, agent cards, and cross-service communication -- see [references/a2a-protocol.md](references/a2a-protocol.md).
For common errors, debugging, and performance tips, see [references/troubleshooting.md](references/troubleshooting.md).

---

## Decision Guide

**When to use which agent type:**

```
Single task, one LLM call? → Agent / LlmAgent
Steps must run in order? → SequentialAgent
Steps are independent? → ParallelAgent
Need iteration/refinement? → LoopAgent
Need on-demand delegation? → AgentTool
Remote agent, different service? → RemoteA2aAgent (A2A)
Complex multi-stage? → Compose agent types
```

**When to use which tool type:**

```
Simple function? → Python function with type hints
Need state access? → Add ToolContext parameter
Delegate to another agent? → AgentTool
Remote agent over network? → RemoteA2aAgent (A2A protocol)
External MCP server? → MCPToolset
Database access? → ToolboxToolset
Web search? → google_search (built-in)
```
