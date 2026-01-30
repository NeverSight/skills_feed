---
name: multi-agent-thinker
description:
  This skill is the "Heavy Lifting Engine" for complex problem solving. 
  
  **CRITICAL TRIGGER LOGIC - READ CAREFULLY:**
  The IDE must evaluate the user's request description to decide whether to invoke this skill.
  
  **INVOKE THIS SKILL IF:**
  - The request involves **Ambiguity** (e.g., "Design a system...", "Analyze this...", "What do you think about...").
  - The request requires **Reasoning** or **Planning** before coding (e.g., architecture design, trade-off analysis, root cause analysis).
  - The request implies **Multiple Perspectives** (e.g., "debate", "critique", "comprehensive review").
  - The request explicitly asks for **Cognitive Strategies** (Socratic questioning, Devil's Advocate, Pre-mortem, Reverse Engineering).
  
  **DO NOT INVOKE IF:**
  - The request is a simple, deterministic action (e.g., "Fix the typo in line 10", "Read file X", "Run command Y").
  - The request is a direct code generation for a well-defined function without need for architectural thought.
  
  When invoked, this skill triggers a multi-agent cognitive process to handle the complexity.
---

# Multi-Agent Architecture Patterns

Multi-agent architectures distribute work across multiple language model instances, each with its own context window. When designed well, this distribution enables capabilities beyond single-agent limits. When designed poorly, it introduces coordination overhead that negates benefits. The critical insight is that sub-agents exist primarily to isolate context, not to anthropomorphize role division.

## When to Activate

## Triggers
This skill activates on semantic intent, NOT keywords. 

**Active Signals:**
- "Help me think through..."
- "Design a..."
- "Critique my..."
- "What if..."
- "Why did this fail?"

**Passive Signals:**
- Any request where the solution path is not immediately obvious.
- Any request requiring context beyond a single file.

## Core Concepts

Multi-agent systems address single-agent context limitations through distribution. Three dominant patterns exist: supervisor/orchestrator for centralized control, peer-to-peer/swarm for flexible handoffs, and hierarchical for layered abstraction. The critical design principle is context isolation—sub-agents exist primarily to partition context rather than to simulate organizational roles.

Effective multi-agent systems require explicit coordination protocols, consensus mechanisms that avoid sycophancy, and careful attention to failure modes including bottlenecks, divergence, and error propagation.

## Detailed Topics

### Why Multi-Agent Architectures

**The Context Bottleneck**
Single agents face inherent ceilings in reasoning capability, context management, and tool coordination. As tasks grow more complex, context windows fill with accumulated history, retrieved documents, and tool outputs. Performance degrades according to predictable patterns: the lost-in-middle effect, attention scarcity, and context poisoning.

Multi-agent architectures address these limitations by partitioning work across multiple context windows. Each agent operates in a clean context focused on its subtask. Results aggregate at a coordination layer without any single context bearing the full burden.

**The Token Economics Reality**
Multi-agent systems consume significantly more tokens than single-agent approaches. Production data shows:

| Architecture | Token Multiplier | Use Case |
|--------------|------------------|----------|
| Single agent chat | 1× baseline | Simple queries |
| Single agent with tools | ~4× baseline | Tool-using tasks |
| Multi-agent system | ~15× baseline | Complex research/coordination |

Research on the BrowseComp evaluation found that three factors explain 95% of performance variance: token usage (80% of variance), number of tool calls, and model choice. This validates the multi-agent approach of distributing work across agents with separate context windows to add capacity for parallel reasoning.

Critically, upgrading to better models often provides larger performance gains than doubling token budgets. Claude Sonnet 4.5 showed larger gains than doubling tokens on earlier Sonnet versions. GPT-5.2's thinking mode similarly outperforms raw token increases. This suggests model selection and multi-agent architecture are complementary strategies.

**The Parallelization Argument**
Many tasks contain parallelizable subtasks that a single agent must execute sequentially. A research task might require searching multiple independent sources, analyzing different documents, or comparing competing approaches. A single agent processes these sequentially, accumulating context with each step.

Multi-agent architectures assign each subtask to a dedicated agent with a fresh context. All agents work simultaneously, then return results to a coordinator. The total real-world time approaches the duration of the longest subtask rather than the sum of all subtasks.

**The Specialization Argument**
Different tasks benefit from different agent configurations: different system prompts, different tool sets, different context structures. A general-purpose agent must carry all possible configurations in context. Specialized agents carry only what they need.

Multi-agent architectures enable specialization without combinatorial explosion. The coordinator routes to specialized agents; each agent operates with lean context optimized for its domain.

### Architectural Patterns

**Pattern 1: Supervisor/Orchestrator**
The supervisor pattern places a central agent in control, delegating to specialists and synthesizing results. The supervisor maintains global state and trajectory, decomposes user objectives into subtasks, and routes to appropriate workers.

```
User Query -> Supervisor -> [Specialist, Specialist, Specialist] -> Aggregation -> Final Output
```

When to use: Complex tasks with clear decomposition, tasks requiring coordination across domains, tasks where human oversight is important.

Advantages: Strict control over workflow, easier to implement human-in-the-loop interventions, ensures adherence to predefined plans.

Disadvantages: Supervisor context becomes bottleneck, supervisor failures cascade to all workers, "telephone game" problem where supervisors paraphrase sub-agent responses incorrectly.

**The Telephone Game Problem and Solution**
LangGraph benchmarks found supervisor architectures initially performed 50% worse than optimized versions due to the "telephone game" problem where supervisors paraphrase sub-agent responses incorrectly, losing fidelity.

The fix: implement a `forward_message` tool allowing sub-agents to pass responses directly to users:

```python
def forward_message(message: str, to_user: bool = True):
    """
    Forward sub-agent response directly to user without supervisor synthesis.
    
    Use when:
    - Sub-agent response is final and complete
    - Supervisor synthesis would lose important details
    - Response format must be preserved exactly
    """
    if to_user:
        return {"type": "direct_response", "content": message}
    return {"type": "supervisor_input", "content": message}
```

With this pattern, swarm architectures slightly outperform supervisors because sub-agents respond directly to users, eliminating translation errors.

Implementation note: Implement direct pass-through mechanisms allowing sub-agents to pass responses directly to users rather than through supervisor synthesis when appropriate.

**Pattern 2: Peer-to-Peer/Swarm**
The peer-to-peer pattern removes central control, allowing agents to communicate directly based on predefined protocols. Any agent can transfer control to any other through explicit handoff mechanisms.

```python
def transfer_to_agent_b():
    return agent_b  # Handoff via function return

agent_a = Agent(
    name="Agent A",
    functions=[transfer_to_agent_b]
)
```

When to use: Tasks requiring flexible exploration, tasks where rigid planning is counterproductive, tasks with emergent requirements that defy upfront decomposition.

Advantages: No single point of failure, scales effectively for breadth-first exploration, enables emergent problem-solving behaviors.

Disadvantages: Coordination complexity increases with agent count, risk of divergence without central state keeper, requires robust convergence constraints.

Implementation note: Define explicit handoff protocols with state passing. Ensure agents can communicate their context needs to receiving agents.

**Pattern 3: Hierarchical**
Hierarchical structures organize agents into layers of abstraction: strategic, planning, and execution layers. Strategy layer agents define goals and constraints; planning layer agents break goals into actionable plans; execution layer agents perform atomic tasks.

```
Strategy Layer (Goal Definition) -> Planning Layer (Task Decomposition) -> Execution Layer (Atomic Tasks)
```

When to use: Large-scale projects with clear hierarchical structure, enterprise workflows with management layers, tasks requiring both high-level planning and detailed execution.

Advantages: Mirrors organizational structures, clear separation of concerns, enables different context structures at different levels.

Disadvantages: Coordination overhead between layers, potential for misalignment between strategy and execution, complex error propagation.

### Context Isolation as Design Principle

The primary purpose of multi-agent architectures is context isolation. Each sub-agent operates in a clean context window focused on its subtask without carrying accumulated context from other subtasks.

**Isolation Mechanisms**
Full context delegation: For complex tasks where the sub-agent needs complete understanding, the planner shares its entire context. The sub-agent has its own tools and instructions but receives full context for its decisions.

Instruction passing: For simple, well-defined subtasks, the planner creates instructions via function call. The sub-agent receives only the instructions needed for its specific task.

File system memory: For complex tasks requiring shared state, agents read and write to persistent storage. The file system serves as the coordination mechanism, avoiding context bloat from shared state passing.

**Isolation Trade-offs**
Full context delegation provides maximum capability but defeats the purpose of sub-agents. Instruction passing maintains isolation but limits sub-agent flexibility. File system memory enables shared state without context passing but introduces latency and consistency challenges.

The right choice depends on task complexity, coordination needs, and acceptable latency.

### Consensus and Coordination

**The Voting Problem**
Simple majority voting treats hallucinations from weak models as equal to reasoning from strong models. Without intervention, multi-agent discussions devolve into consensus on false premises due to inherent bias toward agreement.

**Weighted Voting**
Weight agent votes by confidence or expertise. Agents with higher confidence or domain expertise carry more weight in final decisions.

**Debate Protocols**
Debate protocols require agents to critique each other's outputs over multiple rounds. Adversarial critique often yields higher accuracy on complex reasoning than collaborative consensus.

**Trigger-Based Intervention**
Monitor multi-agent interactions for specific behavioral markers. Stall triggers activate when discussions make no progress. Sycophancy triggers detect when agents mimic each other's answers without unique reasoning.

### Framework Considerations

Different frameworks implement these patterns with different philosophies. LangGraph uses graph-based state machines with explicit nodes and edges. AutoGen uses conversational/event-driven patterns with GroupChat. CrewAI uses role-based process flows with hierarchical crew structures.

## Practical Guidance

### Failure Modes and Mitigations

**Failure: Supervisor Bottleneck**
The supervisor accumulates context from all workers, becoming susceptible to saturation and degradation.

Mitigation: Implement output schema constraints so workers return only distilled summaries. Use checkpointing to persist supervisor state without carrying full history.

**Failure: Coordination Overhead**
Agent communication consumes tokens and introduces latency. Complex coordination can negate parallelization benefits.

Mitigation: Minimize communication through clear handoff protocols. Batch results where possible. Use asynchronous communication patterns.

**Failure: Divergence**
Agents pursuing different goals without central coordination can drift from intended objectives.

Mitigation: Define clear objective boundaries for each agent. Implement convergence checks that verify progress toward shared goals. Use time-to-live limits on agent execution.

**Failure: Error Propagation**
Errors in one agent's output propagate to downstream agents that consume that output.

Mitigation: Validate agent outputs before passing to consumers. Implement retry logic with circuit breakers. Use idempotent operations where possible.

## Cognitive Strategies Layer

To handle diverse interaction scenarios and improve model performance, this skill implements a "Cognitive Strategies" layer.

### 1. Basic Scenario: Prompt Enhancement
**Trigger:** All user instructions.
**Mechanism:** "Prompt Repetition" (CV Method) to improve non-reasoning model performance.
**Logic:**
- Length < 100 chars: Repeat 3 times (Total 4 segments).
- Length 100-500 chars: Repeat 2 times (Total 3 segments).
- Length > 500 chars: Repeat 1 time (Total 2 segments).
**Format:** Segments separated by two newlines (`\n\n`).

### 2. Extended Scenarios (Strategy Layer)
Expert Agents select one of these strategies based on context.

#### A. Socratic Questioning (追问场景)
**Trigger:** Vague requirements, uncertainty, or need for deep clarification.
**Behavior:**
- Ask one question at a time.
- Iterate until 95% confidence in understanding is reached.
- Do not provide solution until requirements are clear.

#### B. Dialectical Discussion (辩证场景)
**Trigger:** Critical decision making, need for robust solutions, or user request for critique.
**Behavior:**
- Play "Devil's Advocate" or "Opposer".
- Challenge assumptions, logic, and evidence.
- Attack the user's idea from multiple angles to find loopholes.

#### C. Pre-mortem Analysis (失败预想)
**Trigger:** Project planning, risk assessment, or high-stakes execution.
**Behavior:**
- Assume the plan has already failed.
- Analyze: "What decision was wrong?", "Fatal error?", "Ignored risk?", "First thing to fix?".
- Based on real-world failure cases.

#### D. Reverse Engineering (反向提示)
**Trigger:** Product design, feature brainstorming (e.g., "I want a shopping app").
**Behavior:**
- Analyze mature products (e.g., Amazon, Taobao) in the domain.
- Deduce necessary features and requirements from these finished products.
- Output the inferred spec.

#### E. Multi-dimensional Explanation (多维解释)
**Trigger:** Educational requests, complex concept explanation, or mixed-audience reporting.
**Behavior:**
- **Beginner Version:** Analogies, simple language.
- **Expert Version:** Technical precision, no factual errors.

## Examples

**Example 1: Research Team Architecture**
```text
Supervisor
├── Researcher (web search, document retrieval)
├── Analyzer (data analysis, statistics)
├── Fact-checker (verification, validation)
```

### Expert Persona Definition

A powerful pattern for high-performance agents is to define them not just by *role* (e.g., "Researcher") but by *specific expert persona* (e.g., "Marie Curie"). This anchors the LLM's latent knowledge about that person's thinking style, expertise, and standards.

**The "Persona-First" Approach**

Instead of generic instructions, use a 3-step definition process:
1.  **Select the Best Mind**: Identify a specific top-tier expert (living or historical) for the problem.
2.  **Justify the Choice**: Explicitly state *why* this person is the right fit (domain match, thinking style).
3.  **Inject the Persona**: Configure the system prompt to *be* that person.

**Helper: Expert Selector**

Use the provided `scripts/personas.py` to facilitate this:

```python
from scripts.personas import ExpertSelector, ExpertPersona

# 1. Get the prompt to ask an LLM for a recommendation
prompt = ExpertSelector.get_selection_prompt("Analyze the future of quantum computing")

# 2. (After getting LLM response) Create the persona
turing = ExpertSelector.create_persona(
    name="Alan Turing",
    domain="Foundational Computing & Cryptography",
    reason="Father of theoretical computer science; best suited to analyze fundamental computational limits.",
    style="Rigorous, mathematical, first-principles thinking."
)

# 3. Register with Supervisor
supervisor.register_expert("quantum_analyst", turing)
```
