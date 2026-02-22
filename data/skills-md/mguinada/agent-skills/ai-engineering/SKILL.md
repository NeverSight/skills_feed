---
name: ai-engineering
description: "Build AI agents and agentic workflows. Use when designing/building/debugging agentic systems: choosing workflows vs agents, implementing prompt patterns (chaining/routing/parallelization/orchestrator-workers/evaluator-optimizer), building autonomous agents with tools, designing ACI/tool specs, or troubleshooting/optimizing implementations. **PROACTIVE ACTIVATION**: Auto-invoke when building agentic applications, designing workflows vs agents, or implementing agent patterns. **DETECTION**: Check for agent code (MCP servers, tool defs, .mcp.json configs), or user mentions of \"agent\", \"workflow\", \"agentic\", \"autonomous\". **USE CASES**: Designing agentic systems, choosing workflows vs agents, implementing prompt patterns, building agents with tools, designing ACI/tool specs, troubleshooting/optimizing agents."
author: mguinada
version: 1.0.0
tags: [agents, ai, workflows, mcp, aci, prompt-engineering, tool-design]
---

# AI Engineering

## Overview

Build effective agentic systems using proven patterns. Start simple, add complexity only when needed.

> **For specialized prompt design guidance** (techniques, patterns, examples for agentic systems), see the **prompt-engineering skill**.

## Core Principle

**Find the simplest solution first.** Agentic systems trade latency and cost for better task performance. Only increase complexity when simpler solutions fall short.

1. Start with optimized single LLM calls (retrieval, in-context examples)
2. Add workflows for predictable, multi-step tasks
3. Use agents when flexibility and autonomous decision-making are required

## When to Build an Agent

Before committing to an agent, validate that your use case truly requires agentic capabilities. Consider alternatives first—deterministic solutions are simpler, faster, and more reliable.

**Use agents when workflows involve:**

| Criteria | Description | Example |
|----------|-------------|---------|
| **Complex decision-making** | Nuanced judgment, exceptions, context-sensitive decisions | Refund approval with edge cases |
| **Brittle rule systems** | Rulesets that are unwieldy, costly to maintain, or error-prone | Vendor security reviews |
| **Unstructured data** | Interpreting natural language, documents, or conversational input | Processing insurance claims |

If your use case doesn't clearly fit these criteria, a deterministic or simple LLM solution may suffice.

## Agentic System Taxonomy

Understanding the spectrum of agentic capabilities helps you choose the right level of complexity for your use case.

| Level | Name | Description | Use Case |
|-------|------|-------------|----------|
| **Level 0** | Core Reasoning System | LM operates in isolation, responding based on pre-trained knowledge only | Explaining concepts, general knowledge |
| **Level 1** | Connected Problem-Solver | LM connects to external tools to retrieve real-time information and take actions | Answering "What's the score?", querying databases |
| **Level 2** | Strategic Problem-Solver | Agent actively curates context, plans multi-step tasks, and engineers focused queries for each step | "Find coffee shops halfway between two locations" |
| **Level 3** | Collaborative Multi-Agent System | Multiple specialized agents coordinate under a central manager or through peer handoffs | Product launch with research, marketing, and web dev agents |
| **Level 4** | Self-Evolving System | Agents can dynamically create new tools or agents to fill capability gaps | Agent creates sentiment analysis agent when needed |

**Progression guidance:** Start at Level 0 or 1. Only increase levels when the current level cannot handle your use case effectively.

## Prompt Engineering

Effective prompts are critical to agentic system performance. When designing or refining prompts for LLM calls, workflows, or agents, leverage the **prompt-engineering skill** if available. It provides specialized guidance for crafting prompts that produce reliable, high-quality outputs.

## Context Engineering

Context engineering is the practice of dynamically assembling and managing information within an LLM's context window to enable stateful, intelligent agents. It represents an evolution from prompt engineering—while prompts focus on static instructions, context engineering addresses the entire payload dynamically.

**Key principles:**
- **Curate attention:** Prevent context overload by including only relevant information for each step
- **Dynamic filtering:** Transform previous outputs into focused queries for the next step
- **Progressive refinement:** Each step should produce a distilled, actionable input for the next

**Example:** Instead of passing an entire document to summarize, extract key entities first, then retrieve only relevant context about those entities.

For comprehensive guidance on sessions, memory, and context management, see **[references/context-engineering.md](references/context-engineering.md)**.

## Agentic Problem-Solving Process

All autonomous agents operate on a continuous cyclical process. Understanding this loop is fundamental to building effective agents.

**The 5-Step Loop:**

1. **Get the Mission** - Receive a high-level goal from user or automated trigger
2. **Scan the Scene** - Gather context from available resources: instructions, session history, available tools, long-term memory
3. **Think It Through** - Analyze mission against scene, devise a plan using chain-of-reasoning
4. **Take Action** - Execute the first concrete step by invoking a tool or generating response
5. **Observe and Iterate** - Observe the outcome, add to context/memory, loop back to step 3

This "Think, Act, Observe" cycle continues until the mission is complete or an exit condition is reached.

**Code example (Think, Act, Observe with tools):**
```python
import anthropic

client = anthropic.Anthropic()

def agent_loop(mission: str, max_iterations: int = 10):
    """Run the Think-Act-Observe loop until mission complete."""
    context = f"Mission: {mission}\nAvailable tools: search, read_page, finish"

    for i in range(max_iterations):
        # THINK: LLM analyzes current state and plans next action
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            messages=[{"role": "user", "content": context}],
            tools=[search_tool, read_page_tool, finish_tool]
        )

        # Extract the model's reasoning and intended action
        for block in response.content:
            if block.type == "text":
                print(f"Thought: {block.text}")
            elif block.type == "tool_use" and block.name == "search":
                # ACT: Execute the tool
                result = search(block.input["query"])
                # OBSERVE: Add result to context, loop continues
                context += f"\nObservation: {result}"
            elif block.type == "tool_use" and block.name == "finish":
                # EXIT: Mission complete
                return block.input["summary"]

    return "Max iterations reached"
```

## Pattern Selection Guide

| Pattern | Use When | Key Benefit |
|---------|----------|-------------|
| **Augmented LLM** | Single task needing external data/tools | Retrieval, tools, memory |
| **Prompt Chaining** | Task decomposes into fixed subtasks | Trade latency for accuracy |
| **Routing** | Distinct categories need separate handling | Separation of concerns |
| **Parallelization** | Subtasks are independent OR multiple attempts needed | Speed OR confidence |
| **Orchestrator-Workers** | Subtasks unpredictable, input-dependent | Dynamic task breakdown |
| **Evaluator-Optimizer** | Clear evaluation criteria, iteration adds value | Iterative refinement |
| **Autonomous Agent** | Open-ended problems, unpredictable steps | Flexibility at scale |

## Decision Framework

```
Is the task solvable with a single well-crafted prompt?
├─ Yes → Optimize with retrieval/examples → Done
└─ No → Are subtasks fixed and predictable?
    ├─ Yes → Use Workflow (chaining/routing/parallelization)
    └─ No → Are subtasks input-dependent?
        ├─ Yes → Use Orchestrator-Workers
        └─ No → Is the problem open-ended with unpredictable steps?
            ├─ Yes → Use Autonomous Agent
            └─ No → Reconsider approach
```

## Workflow Patterns

For detailed workflow implementations with code examples, see **[references/workflows.md](references/workflows.md)**.

**When to use workflows:** Tasks with predictable, multi-step steps where subtasks are fixed or input-dependent.

**Quick reference:**
- **Prompt Chaining** - Sequential LLM calls, each processing previous output
- **Routing** - Classify input and direct to specialized handler
- **Parallelization** - Sectioning (independent subtasks) or Voting (multiple attempts)
- **Orchestrator-Workers** - Central LLM breaks down tasks, delegates to workers, synthesizes results
- **Evaluator-Optimizer** - One LLM generates, another evaluates and provides feedback in a loop

**Code example (Orchestrator-Workers):**
```python
# Orchestrator breaks down task
subtasks = llm(f"Break down: {task}")

# Workers execute in parallel
results = [execute(s) for s in subtasks]

# Orchestrator synthesizes
final = llm(f"Synthesize results: {results}")
```

**Code example (Prompt Chaining - complete):**
```python
import anthropic

client = anthropic.Anthropic()

def analyze_document(text: str) -> str:
    """Complete prompt chaining: extract → summarize → recommend."""

    # STEP 1: Extract key entities
    step1 = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{
            "role": "user",
            "content": f"Extract all entities (people, orgs, dates) from:\n{text}"
        }]
    )
    entities = step1.content[0].text

    # STEP 2: Summarize using extracted entities
    step2 = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{
            "role": "user",
            "content": f"Summarize this document using these entities: {entities}\n\nDocument: {text}"
        }]
    )
    summary = step2.content[0].text

    # STEP 3: Generate recommendations based on summary
    step3 = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        messages=[{
            "role": "user",
            "content": f"Based on this summary, provide 3 actionable recommendations:\n{summary}"
        }]
    )

    return step3.content[0].text
```

## Error Handling & Guardrails

Guardrails are a layered defense. No single layer is sufficient—combine multiple specialized checks for resilient agents.

**Layered Defense Pattern:**
```
Input → Relevance Check → Safety Filter → Agent → Tool Safeguards → Output Validation → Response
            ↓block          ↓block                  ↓risk-rating          ↓block
```

For a complete implementation with code examples and tests, see **[references/agent-design.md](references/agent-design.md#implementation-example)**.

## Agent Design

For comprehensive agent design patterns, characteristics, and best practices, see **[references/agent-design.md](references/agent-design.md)**.

**Core agent characteristics:**
1. Explicit Role & Responsibility - Clearly defined mandate
2. Single-Purpose Focus - Narrow scope, high performance
3. Minimal, Purpose-Built Tooling - Only necessary tools
4. Deterministic Orchestration - Clear execution structure
5. Cooperation & Delegation - Structured interaction
6. Self-Constraint & Guardrails - Prevents scope creep
7. State Awareness - Session memory for tasks
8. Long-Term Memory - Curated, retrievable knowledge
9. Observability - Inspectable decisions and outcomes
10. Failure Awareness - Graceful recovery

**Key topics:**
- **Autonomous Agents and the Run Loop** - The "Think, Act, Observe" cycle with exit conditions
- **Guardrails** - Layered defense: relevance classifiers, safety filters, PII filters, tool safeguards
- **Multi-Agent Patterns** - Manager (agents as tools), Decentralized (handoffs), Sequential, Iterative Refinement
- **Real-World Examples** - Customer support agents, coding agents with test verification

## Agent-Computer Interface (ACI)

Tool design matters as much as prompt engineering. For comprehensive tool design patterns, see **[references/aci.md](references/aci.md)**.

**Core principles:**
- **Give tokens to think** - Don't force the model into corners
- **Keep formats natural** - Match patterns from training data
- **Minimize overhead** - Avoid line counting, escape sequences
- **Publish tasks, not APIs** - Tools should encapsulate user-facing actions

**Key patterns:**
- **Tool Types** - Information Retrieval, Action/Execution, System/API Integration, Human-in-the-Loop
- **Output Design** - Return references for large data, descriptive error messages for recovery
- **Input Validation** - Schema validation for runtime checks and LLM guidance
- **Documentation** - Clear descriptions, examples, edge cases, parameter constraints

## Model Context Protocol (MCP)

MCP is an open standard for connecting AI applications to external tools and data sources. For comprehensive coverage, see **[references/mcp.md](references/mcp.md)**.

**What it solves:** The "N×M integration problem" - without a standard, every model-tool pairing requires custom connectors.

**Core architecture:**
- **Host** - Manages UX, orchestrates tools, enforces security
- **Client** - Maintains server connections, manages sessions
- **Server** - Advertises tools, executes commands, handles governance

**Key capabilities:**
- **Tools** - Standardized function definitions with JSON Schema
- **Resources** - Static data access (validate trusted sources only)
- **Prompts** - Reusable prompt templates (use rarely - security risk)
- **Sampling** - Server can request LLM completion from client
- **Elicitation** - Server can request user input via client UI

**When to use MCP:**
- Multi-environment deployments
- Sharing tools across applications
- Dynamic tool discovery needs
- Ecosystem participation

**Security considerations:**
- Dynamic Capability Injection, Tool Shadowing, Confused Deputy
- Requires multi-layered defense: HIL → API Gateway → SDK Allowlists → Schema Validation

## Implementation Guidance

For practical implementation guidance including model selection, task decomposition, and debugging, see **[references/implementation.md](references/implementation.md)**.

**Quick start:**
```python
# Single call with retrieval
response = claude.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": query}],
    tools=[search_tool, database_tool]
)
```

**Key topics:**
- **Start Simple** - Optimize single calls first, add complexity only when needed
- **Framework Considerations** - Claude Agent SDK, Agno, CrewAI, LangChain (or direct APIs)
- **Model Selection** - Prototype with best, optimize cost/latency with smaller models
- **Task Decomposition** - Break down until each step is automatable or human-gated
- **Performance & Scalability** - Context window management, dynamic tool loading, state management
- **Debugging** - Common issues: tool usage, loops, edge cases, compounding errors

## Operations & Security

For production operations, security, and agent learning patterns, see **[references/operations.md](references/operations.md)**.

**Agent Ops (GenAIOps):**
- **Evaluation Strategy** - Define success metrics first, use LM as Judge, metrics-driven development
- **Observability** - OpenTelemetry traces for full trajectory: prompts, reasoning, tool calls, observations
- **Human Feedback Loop** - Collect failures, convert to test cases, "close the loop" on error classes

**Agent Identity & Security:**
- **Agent as Principal** - Distinct from users and service accounts, requires verifiable identity with least privilege
- **Security Layers** - Deterministic guardrails (rules) + Reasoning-based defenses (guard models)
- **Tool Security Threats** - Dynamic Capability Injection, Tool Shadowing, Confused Deputy, Malicious Definitions

**Multi-Layered Defense:**
```
Human-in-the-Loop → API Gateway → SDK Allowlists → Schema Validation → Secure Design
```

## Quality & Evaluation

For comprehensive agent quality frameworks, evaluation strategies, and observability practices, see **[references/quality-evaluation.md](references/quality-evaluation.md)**.

**Four Pillars of Agent Quality:**
- **Effectiveness** - Goal completion, accuracy, instruction following
- **Efficiency** - Latency, cost per interaction, token usage
- **Robustness** - Edge case handling, error recovery, consistency
- **Safety** - Guardrails, content filtering, policy compliance

**Evaluation Hierarchy:**
- **End-to-End (Black Box)** - Measure final outputs against golden dataset
- **Trajectory (Glass Box)** - Inspect intermediate steps, tool calls, reasoning

**Evaluators:**
- **Automated Metrics** - Exact match, similarity scores, rule-based checks
- **LLM-as-a-Judge** - Use powerful model to assess against rubric
- **Agent-as-a-Judge** - Specialized evaluator agent critiques outputs
- **Human-in-the-Loop** - Authoritative feedback for edge cases

## Resources

- **[Workflows Reference](references/workflows.md)** - Detailed workflow patterns with code examples
- **[Context Engineering](references/context-engineering.md)** - Sessions, memory, and context management
- **[Agent Design](references/agent-design.md)** - Agent characteristics, ACI, guardrails, multi-agent patterns
- **[Implementation Guide](references/implementation.md)** - Practical implementation guidance and debugging
- **[Operations & Security](references/operations.md)** - Production operations, security, and agent learning
- **[Quality & Evaluation](references/quality-evaluation.md)** - Agent quality frameworks, evaluation strategies, observability
- **[ACI Guide](references/aci.md)** - Agent-Computer Interface deep dive with tool design patterns
- **[MCP Guide](references/mcp.md)** - Model Context Protocol for tool interoperability
- **[Examples](references/examples.md)** - Real-world implementations and case studies
