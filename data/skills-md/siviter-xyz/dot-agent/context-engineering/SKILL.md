---
name: context-engineering
description: Master context engineering for AI agent systems. Use when designing agent architectures, debugging context failures, optimizing token usage, implementing memory systems, building multi-agent coordination, evaluating agent performance, or developing LLM-powered pipelines. Covers context fundamentals, degradation patterns, optimization techniques, compression strategies, memory architectures, multi-agent patterns, evaluation, tool design, and project development.
license: MIT
---

# Context Engineering

Context engineering curates the smallest high-signal token set for LLM tasks. The goal: maximize reasoning quality while minimizing token usage.

## When to Activate

- Designing/debugging agent systems
- Context limits constrain performance
- Optimizing cost/latency
- Building multi-agent coordination
- Implementing memory systems
- Evaluating agent performance
- Developing LLM-powered pipelines

## Core Principles

1. **Context quality > quantity** - High-signal tokens beat exhaustive content
2. **Attention is finite** - U-shaped curve favors beginning/end positions
3. **Progressive disclosure** - Load information just-in-time
4. **Isolation prevents degradation** - Partition work across sub-agents
5. **Measure before optimizing** - Know your baseline

## Key Metrics

- **Token utilization**: Warning at 70%, trigger optimization at 80%
- **Token variance**: Explains 80% of agent performance variance
- **Multi-agent cost**: ~15x single agent baseline
- **Compaction target**: 50-70% reduction, <5% quality loss
- **Cache hit target**: 70%+ for stable workloads

## Four-Bucket Strategy

1. **Write**: Save context externally (scratchpads, files)
2. **Select**: Pull only relevant context (retrieval, filtering)
3. **Compress**: Reduce tokens while preserving info (summarization)
4. **Isolate**: Split across sub-agents (partitioning)

## Anti-Patterns

- Exhaustive context over curated context
- Critical info in middle positions
- No compaction triggers before limits
- Single agent for parallelizable tasks
- Tools without clear descriptions

## Guidelines

1. Place critical info at beginning/end of context
2. Implement compaction at 70-80% utilization
3. Use sub-agents for context isolation, not role-play
4. Design tools with clear descriptions (what, when, inputs, returns)
5. Optimize for tokens-per-task, not tokens-per-request
6. Validate with probe-based evaluation
7. Monitor token usage in production
8. Start minimal, add complexity only when proven necessary

## Skill Coordination

When multiple skills are active:
- Load only relevant skill content
- Use skill metadata for discovery
- Avoid loading full skill definitions unless needed
- Reference skills by pattern detection, not direct names

## References

For detailed guidance, see:
- `references/fundamentals.md` - Context anatomy, attention mechanics
- `references/degradation.md` - Debugging failures, lost-in-middle, poisoning
- `references/optimization.md` - Compaction, masking, caching, partitioning
- `references/compression.md` - Long sessions, summarization strategies
- `references/memory.md` - Cross-session persistence, knowledge graphs
- `references/multi-agent.md` - Coordination patterns, context isolation
- `references/evaluation.md` - Testing agents, LLM-as-Judge, metrics
- `references/tool-design.md` - Tool consolidation, description engineering
