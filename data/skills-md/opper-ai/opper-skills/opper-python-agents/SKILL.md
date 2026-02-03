---
name: opper-python-agents
description: >
  Use the Opper Python Agent SDK (opper-agents) to build AI agents with think-act reasoning loops, tool use via @tool decorator, multi-agent composition, MCP integration, persistent memory, hooks for observability, and Pydantic schema validation. Activate when building Python AI agents, autonomous systems, or tool-using reasoning loops with the Opper platform.
---

# Opper Python Agents

Build AI agents with think-act reasoning loops, typed tools, multi-agent composition, memory, and full observability.

## Installation

```bash
pip install opper-agents
```

Set your API key:

```bash
export OPPER_API_KEY="your-api-key"
```

Get your API key from [platform.opper.ai](https://platform.opper.ai).

## Core Pattern: Agent with Tools

Define tools with the `@tool` decorator, create an agent, and run it:

```python
from opper_agents import Agent, tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is 22°C and sunny"

@tool
def get_population(city: str) -> int:
    """Get the population of a city."""
    populations = {"Paris": 2_161_000, "London": 8_982_000}
    return populations.get(city, 0)

agent = Agent(
    name="CityBot",
    instructions="Help users with city information using available tools.",
    tools=[get_weather, get_population],
)

result = await agent.process("What's the weather and population of Paris?")
print(result)
# "Paris has a population of 2,161,000 and the weather is 22°C and sunny."
```

## How the Agent Loop Works

The agent follows a Think-Act-Observe loop:

1. **Think**: The LLM analyzes the goal and available tools
2. **Act**: It selects and executes a tool
3. **Observe**: Results are added to the conversation history
4. **Loop/Return**: Repeat until the goal is met, then return the final answer

The loop runs up to `max_iterations` times (default: 25).

## Structured Output

Use Pydantic models to get typed, validated results:

```python
from pydantic import BaseModel, Field
from typing import List

class CityReport(BaseModel):
    city: str
    temperature_c: float
    population: int
    summary: str = Field(description="One-sentence summary")

agent = Agent(
    name="CityReporter",
    instructions="Generate a city report using available tools.",
    tools=[get_weather, get_population],
    output_schema=CityReport,
)

result = await agent.process("Report on London")
# result is a CityReport instance
print(result.city)          # "London"
print(result.temperature_c) # 18.0
print(result.population)    # 8982000
```

## Model Selection

Specify which LLM the agent uses for reasoning:

```python
agent = Agent(
    name="SmartAgent",
    instructions="You are a helpful assistant.",
    tools=[my_tool],
    model="anthropic/claude-4-sonnet",
)

# With fallback chain
agent = Agent(
    name="ResilientAgent",
    instructions="You are a helpful assistant.",
    tools=[my_tool],
    model=["anthropic/claude-4-sonnet", "openai/gpt-4o"],
)
```

## Async Tools

For I/O-bound operations, define async tools:

```python
import httpx

@tool
async def fetch_url(url: str) -> str:
    """Fetch content from a URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text[:1000]
```

## Multi-Agent Composition

Use agents as tools within other agents for delegation:

```python
math_agent = Agent(
    name="MathAgent",
    instructions="Solve math problems step by step.",
    tools=[add, multiply],
)

research_agent = Agent(
    name="ResearchAgent",
    instructions="Answer factual questions.",
    tools=[search_web],
)

coordinator = Agent(
    name="Coordinator",
    instructions="Delegate tasks to specialist agents.",
    tools=[math_agent.as_tool(), research_agent.as_tool()],
)

result = await coordinator.process("What is 15 * 23, and who invented calculus?")
```

## MCP Integration

Connect to MCP servers for external tool access:

```python
from opper_agents import mcp, MCPServerConfig

filesystem_server = MCPServerConfig(
    name="filesystem",
    transport="stdio",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
)

agent = Agent(
    name="FileAgent",
    instructions="Use filesystem tools to manage files.",
    tools=[mcp(filesystem_server)],
)
```

## Hooks

Monitor agent lifecycle events:

```python
from opper_agents import hook
from opper_agents.base.context import AgentContext

@hook("agent_start")
async def on_start(context: AgentContext, agent):
    print(f"Agent {agent.name} starting: {context.goal}")

@hook("tool_result")
async def on_tool(context: AgentContext, tool_name: str, result):
    print(f"Tool {tool_name} returned: {result}")

agent = Agent(
    name="ObservedAgent",
    instructions="Do the task.",
    tools=[my_tool],
    hooks=[on_start, on_tool],
)
```

## Execution Stats

Access usage information after running:

```python
result = await agent.process("Solve this problem")

# Access stats from the agent context
print(f"Iterations: {agent.context.iteration}")
print(f"Total tokens: {agent.context.usage.total_tokens}")
```

## Common Mistakes

- **Forgetting `await`**: `agent.process()` is async. Always use `await`.
- **Missing tool docstrings**: The agent uses docstrings to understand what tools do. Always provide descriptive docstrings.
- **Too many tools**: Agents work best with 5-10 focused tools. Use multi-agent composition for more.
- **No `output_schema`**: Without it, results are unstructured strings. Use Pydantic models for reliable parsing.
- **Infinite loops**: Set `max_iterations` to prevent runaway agents.

## Additional Resources

- For advanced tool patterns and context, see [references/TOOLS.md](references/TOOLS.md)
- For MCP server configuration, see [references/MCP.md](references/MCP.md)
- For multi-agent composition patterns, see [references/COMPOSITION.md](references/COMPOSITION.md)
- For lifecycle hooks reference, see [references/HOOKS.md](references/HOOKS.md)
- For persistent memory, see [references/MEMORY.md](references/MEMORY.md)

## Related Skills

- **opper-python-sdk**: Use for single-shot task completion without agent loops — simpler when you don't need multi-step reasoning.
- **opper-node-agents**: Use when building agents in TypeScript instead of Python.

## Upstream Sources

If this skill's content is outdated, check the canonical sources:

- **Source code**: https://github.com/opper-ai/opperai-agent-sdk
- **Documentation**: https://docs.opper.ai
