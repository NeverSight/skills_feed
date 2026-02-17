---
name: context-optimization
description: Use when optimizing agent context, reducing token costs, implementing KV-cache optimization, or asking about "context optimization", "token reduction", "context limits", "observation masking", "context budgeting", "context partitioning"
version: 1.0.0
---

# Context Optimization Techniques

Extend effective context capacity through compression, masking, caching, and partitioning. Effective optimization can 2-3x effective context capacity without larger models.

## Optimization Strategies

| Strategy | Token Reduction | Use Case |
|----------|-----------------|----------|
| Compaction | 50-70% | Message history dominates |
| Observation Masking | 60-80% | Tool outputs dominate |
| KV-Cache Optimization | 70%+ cache hits | Stable workloads |
| Context Partitioning | Variable | Complex multi-task |

## Compaction

Summarize context when approaching limits:

```python
if context_tokens / context_limit > 0.8:
    context = compact_context(context)
```

**Priority for compression**:

1. Tool outputs → replace with summaries
2. Old turns → summarize early conversation
3. Retrieved docs → summarize if recent versions exist
4. **Never compress** system prompt

**Summary generation by type**:

- **Tool outputs**: Preserve findings, metrics, conclusions
- **Conversational**: Preserve decisions, commitments, context shifts
- **Documents**: Preserve key facts, remove supporting evidence

## Observation Masking

Tool outputs can be 80%+ of tokens. Replace verbose outputs with references:

```python
if len(observation) > max_length:
    ref_id = store_observation(observation)
    return f"[Obs:{ref_id} elided. Key: {extract_key(observation)}]"
```

**Masking rules**:

- **Never mask**: Current task critical, most recent turn, active reasoning
- **Consider**: 3+ turns old, key points extractable, purpose served
- **Always mask**: Repeated outputs, boilerplate, already summarized

## KV-Cache Optimization

Cache Key/Value tensors for requests with identical prefixes:

```python
# Cache-friendly ordering: stable content first
context = [
    system_prompt,      # Cacheable
    tool_definitions,   # Cacheable
    reused_templates,   # Reusable
    unique_content      # Unique
]
```

**Design for cache stability**:

- Avoid dynamic content (timestamps)
- Use consistent formatting
- Keep structure stable across sessions

## Context Partitioning

Split work across sub-agents with isolated contexts:

```python
# Each sub-agent has clean, focused context
results = await gather(
    research_agent.search("topic A"),
    research_agent.search("topic B"),
    research_agent.search("topic C")
)
# Coordinator synthesizes without carrying full context
synthesized = await coordinator.synthesize(results)
```

## Budget Management

```python
context_budget = {
    "system_prompt": 2000,
    "tool_definitions": 3000,
    "retrieved_docs": 10000,
    "message_history": 15000,
    "reserved_buffer": 2000
}
# Monitor and trigger optimization at 70-80%
```

## When to Optimize

| Signal | Action |
|--------|--------|
| Utilization >70% | Start monitoring |
| Utilization >80% | Apply compaction |
| Quality degradation | Investigate cause |
| Tool outputs dominate | Observation masking |
| Docs dominate | Summarization/partitioning |

## Performance Targets

- Compaction: 50-70% reduction, <5% quality loss
- Masking: 60-80% reduction in masked observations
- Cache: 70%+ hit rate for stable workloads

## Best Practices

1. Measure before optimizing
2. Apply compaction before masking
3. Design for cache stability
4. Partition before context becomes problematic
5. Monitor effectiveness over time
6. Balance token savings vs quality
7. Test at production scale
8. Implement graceful degradation
