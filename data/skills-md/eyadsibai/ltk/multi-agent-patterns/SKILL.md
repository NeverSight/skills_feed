---
name: multi-agent-patterns
description: Use when designing multi-agent systems, implementing supervisor patterns, coordinating multiple agents, or asking about "multi-agent", "supervisor pattern", "swarm", "agent handoffs", "orchestration", "parallel agents"
version: 1.0.0
---

# Multi-Agent Architecture Patterns

Multi-agent architectures distribute work across multiple LLM instances, each with its own context window. The critical insight: sub-agents exist primarily to isolate context, not to anthropomorphize role division.

## Why Multi-Agent?

**Context Bottleneck**: Single agents fill context with history, documents, and tool outputs. Performance degrades via lost-in-middle effect and attention scarcity.

**Token Economics**:

| Architecture | Token Multiplier |
|--------------|------------------|
| Single agent chat | 1× baseline |
| Single agent + tools | ~4× baseline |
| Multi-agent system | ~15× baseline |

**Parallelization**: Research tasks can search multiple sources simultaneously. Total time approaches longest subtask, not sum.

## Architectural Patterns

### Pattern 1: Supervisor/Orchestrator

```
User Query -> Supervisor -> [Specialist, Specialist] -> Aggregation -> Output
```

**Use when**: Clear decomposition, coordination needed, human oversight important.

**The Telephone Game Problem**: Supervisors paraphrase sub-agent responses incorrectly.

**Fix**: `forward_message` tool lets sub-agents respond directly:

```python
def forward_message(message: str, to_user: bool = True):
    """Forward sub-agent response directly to user."""
    if to_user:
        return {"type": "direct_response", "content": message}
```

### Pattern 2: Peer-to-Peer/Swarm

```python
def transfer_to_agent_b():
    return agent_b  # Handoff via function return

agent_a = Agent(name="Agent A", functions=[transfer_to_agent_b])
```

**Use when**: Flexible exploration, rigid planning counterproductive, emergent requirements.

### Pattern 3: Hierarchical

```
Strategy Layer -> Planning Layer -> Execution Layer
```

**Use when**: Large-scale projects, enterprise workflows, clear separation of concerns.

## Context Isolation

Primary purpose of multi-agent: context isolation.

**Mechanisms**:

- **Full context delegation**: Complex tasks needing full understanding
- **Instruction passing**: Simple, well-defined subtasks
- **File system memory**: Shared state without context bloat

## Consensus and Coordination

**Weighted Voting**: Weight by confidence or expertise.

**Debate Protocols**: Agents critique each other's outputs. Adversarial critique often yields higher accuracy than collaborative consensus.

**Trigger-Based Intervention**:

- Stall triggers: No progress detection
- Sycophancy triggers: Mimicking without reasoning

## Failure Modes

| Failure | Mitigation |
|---------|------------|
| Supervisor Bottleneck | Output schema constraints, checkpointing |
| Coordination Overhead | Clear handoff protocols, batch results |
| Divergence | Objective boundaries, convergence checks |
| Error Propagation | Output validation, retry with circuit breakers |

## Example: Research Team

```text
Supervisor
├── Researcher (web search, document retrieval)
├── Analyzer (data analysis, statistics)
├── Fact-checker (verification, validation)
└── Writer (report generation)
```

## Best Practices

1. Design for context isolation as primary benefit
2. Choose pattern based on coordination needs, not org metaphor
3. Implement explicit handoff protocols with state passing
4. Use weighted voting or debate for consensus
5. Monitor for supervisor bottlenecks
6. Validate outputs before passing between agents
7. Set time-to-live limits to prevent infinite loops
