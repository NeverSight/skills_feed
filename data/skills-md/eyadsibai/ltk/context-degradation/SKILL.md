---
name: context-degradation
description: Use when diagnosing agent failures, debugging lost-in-middle issues, understanding context poisoning, or asking about "context degradation", "lost in middle", "context poisoning", "attention patterns", "context clash", "agent performance drops"
version: 1.0.0
---

# Context Degradation Patterns

Language models exhibit predictable degradation as context grows. Understanding these patterns is essential for diagnosing failures and designing resilient systems.

## Degradation Patterns

| Pattern | Cause | Symptoms |
|---------|-------|----------|
| Lost-in-Middle | Attention mechanics | 10-40% lower recall for middle content |
| Context Poisoning | Errors compound | Tool misalignment, persistent hallucinations |
| Context Distraction | Irrelevant info | Uses wrong information for decisions |
| Context Confusion | Mixed tasks | Responses address wrong aspects |
| Context Clash | Conflicting info | Contradictory guidance derails reasoning |

## Lost-in-Middle

Information at beginning and end receives reliable attention. Middle content suffers dramatically reduced recall.

**Mitigation**:

```markdown
[CURRENT TASK]                      # At start (high attention)
- Goal: Generate quarterly report
- Deadline: End of week

[DETAILED CONTEXT]                  # Middle (less attention)
- 50 pages of data
- Supporting evidence

[KEY FINDINGS]                      # At end (high attention)
- Revenue up 15%
- Growth in Region A
```

## Context Poisoning

Once errors enter context, they compound through repeated reference.

**Entry pathways**:

1. Tool outputs with errors
2. Retrieved docs with incorrect info
3. Model-generated summaries with hallucinations

**Symptoms**:

- Tool calls with wrong parameters
- Strategies that take effort to undo
- Hallucinations that persist despite correction

**Recovery**:

- Truncate to before poisoning point
- Explicitly note poisoning and re-evaluate
- Restart with clean context

## Context Distraction

Even a single irrelevant document reduces performance. Models must attend to everything—they cannot "skip" irrelevant content.

**Mitigation**:

- Filter for relevance before loading
- Use namespacing for organization
- Access via tools instead of context

## Degradation Thresholds

| Model | Degradation Onset | Severe Degradation |
|-------|-------------------|-------------------|
| GPT-5.2 | ~64K tokens | ~200K tokens |
| Claude Opus 4.5 | ~100K tokens | ~180K tokens |
| Claude Sonnet 4.5 | ~80K tokens | ~150K tokens |
| Gemini 3 Pro | ~500K tokens | ~800K tokens |

## The Four-Bucket Approach

| Strategy | Purpose |
|----------|---------|
| **Write** | Save context outside window |
| **Select** | Pull relevant context in |
| **Compress** | Reduce tokens, preserve info |
| **Isolate** | Split across sub-agents |

## Counterintuitive Findings

1. **Shuffled haystacks outperform coherent** - Coherent context creates false associations
2. **Single distractors have outsized impact** - Step function, not proportional
3. **Needle-question similarity matters** - Dissimilar content degrades faster

## When Larger Contexts Hurt

- Performance degrades non-linearly after threshold
- Cost grows exponentially with context length
- Cognitive bottleneck remains regardless of size

## Best Practices

1. Monitor context length and performance correlation
2. Place critical information at beginning or end
3. Implement compaction triggers before degradation
4. Validate retrieved documents for accuracy
5. Use versioning to prevent outdated info clash
6. Segment tasks to prevent confusion
7. Design for graceful degradation
8. Test with progressively larger contexts
