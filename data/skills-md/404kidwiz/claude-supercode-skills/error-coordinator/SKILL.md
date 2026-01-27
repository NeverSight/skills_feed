---
name: error-coordinator
description: Expert in making multi-agent systems resilient. Specializes in detecting loops, hallucinations, and failures, and implementing self-healing workflows. Use when designing error handling for agent systems, implementing retry strategies, or building resilient AI workflows.
---

# Error Coordinator

## Purpose
Provides expertise in building resilient multi-agent systems with robust error handling, failure detection, and recovery mechanisms. Covers loop detection, hallucination mitigation, and self-healing agent workflows.

## When to Use
- Designing error handling for agent systems
- Implementing retry and recovery strategies
- Building self-healing AI workflows
- Detecting agent loops and infinite recursion
- Mitigating hallucinations in agent outputs
- Implementing circuit breakers for agents
- Coordinating failure recovery across agents

## Quick Start
**Invoke this skill when:**
- Designing error handling for agent systems
- Implementing retry and recovery strategies
- Building self-healing AI workflows
- Detecting agent loops and infinite recursion
- Coordinating failure recovery across agents

**Do NOT invoke when:**
- Organizing agent teams (use agent-organizer)
- Debugging application errors (use debugger)
- Handling production incidents (use incident-responder)
- Detecting code error patterns (use error-detective)

## Decision Framework
```
Error Type Handling:
├── Transient failure → Retry with backoff
├── Rate limiting → Backoff + queue
├── Invalid output → Validation + retry with feedback
├── Loop detected → Break + escalate
├── Hallucination → Ground with context, retry
├── Agent timeout → Cancel + fallback
└── Cascading failure → Circuit breaker

Recovery Strategy:
├── Idempotent operation → Simple retry
├── Stateful operation → Checkpoint + resume
├── Critical path → Fallback agent
└── Best effort → Log + continue
```

## Core Workflows

### 1. Loop Detection System
1. Track agent invocation history
2. Detect repeated state patterns
3. Set maximum iteration limits
4. Implement escape hatch triggers
5. Log loop occurrences for analysis
6. Escalate to supervisor or human

### 2. Hallucination Mitigation
1. Ground responses with source data
2. Implement output validation
3. Cross-check with retrieval
4. Add confidence scoring
5. Flag low-confidence outputs
6. Provide feedback for retry

### 3. Circuit Breaker Implementation
1. Track failure rates per agent
2. Define failure threshold
3. Open circuit on threshold breach
4. Provide fallback behavior
5. Implement half-open state for testing
6. Close circuit on recovery
7. Monitor and alert on breaker state

## Best Practices
- Implement timeouts for all agent calls
- Use exponential backoff with jitter
- Log all failures with full context
- Design for graceful degradation
- Test failure scenarios explicitly
- Monitor error rates and patterns

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Infinite retries | Resource exhaustion | Max retry limits |
| Silent failures | Hidden problems | Log and alert |
| No timeouts | Hung processes | Always set timeouts |
| Same retry interval | Thundering herd | Exponential backoff |
| No fallbacks | Complete failure | Graceful degradation |
