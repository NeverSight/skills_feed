---
name: context-compression
description: Use when compressing agent context, implementing conversation summarization, reducing token usage in long sessions, or asking about "context compression", "conversation history", "token optimization", "context limits", "summarization strategies"
version: 1.0.0
---

# Context Compression Strategies

When agent sessions generate millions of tokens, compression becomes mandatory. Optimize for tokens-per-task (total tokens to complete a task), not tokens-per-request.

## Compression Approaches

### 1. Anchored Iterative Summarization (Recommended)

- Maintain structured summaries with explicit sections
- On compression, summarize only newly-truncated content
- Merge with existing summary instead of regenerating
- Structure forces preservation of critical info

### 2. Opaque Compression

- Highest compression ratios (99%+)
- Sacrifices interpretability
- Cannot verify what was preserved

### 3. Regenerative Full Summary

- Generate detailed summary on each compression
- Readable but may lose details across cycles
- Full regeneration rather than merging

## Structured Summary Format

```markdown
## Session Intent
[What the user is trying to accomplish]

## Files Modified
- auth.controller.ts: Fixed JWT token generation
- config/redis.ts: Updated connection pooling

## Decisions Made
- Using Redis connection pool instead of per-request
- Retry logic with exponential backoff

## Current State
- 14 tests passing, 2 failing
- Remaining: mock setup for session service tests

## Next Steps
1. Fix remaining test failures
2. Run full test suite
3. Update documentation
```

## Compression Triggers

| Strategy | Trigger | Trade-off |
|----------|---------|-----------|
| Fixed threshold | 70-80% context | Simple but may compress early |
| Sliding window | Last N turns + summary | Predictable size |
| Importance-based | Low-relevance first | Complex but preserves signal |
| Task-boundary | At task completions | Clean but unpredictable |

## The Artifact Trail Problem

File tracking is the weakest dimension (2.2-2.5/5.0 in evaluations). Coding agents need:

- Which files were created
- Which files were modified and what changed
- Which files were read but not changed
- Function names, variable names, error messages

**Solution**: Separate artifact index or explicit file-state tracking.

## Probe-Based Evaluation

Test compression quality with probes:

| Probe Type | Tests | Example |
|------------|-------|---------|
| Recall | Factual retention | "What was the original error?" |
| Artifact | File tracking | "Which files have we modified?" |
| Continuation | Task planning | "What should we do next?" |
| Decision | Reasoning chain | "What did we decide about Redis?" |

## Compression Ratios

| Method | Compression | Quality | Trade-off |
|--------|-------------|---------|-----------|
| Anchored Iterative | 98.6% | 3.70 | Best quality |
| Regenerative | 98.7% | 3.44 | Moderate |
| Opaque | 99.3% | 3.35 | Best compression |

The 0.7% extra tokens buys 0.35 quality points—worth it when re-fetching costs matter.

## Three-Phase Workflow (Large Codebases)

1. **Research Phase**: Explore and compress into structured analysis
2. **Planning Phase**: Convert to implementation spec (~2,000 words for 5M tokens)
3. **Implementation Phase**: Execute against the spec

## Best Practices

1. Optimize for tokens-per-task, not tokens-per-request
2. Use structured summaries with explicit file sections
3. Trigger compression at 70-80% utilization
4. Implement incremental merging over regeneration
5. Test with probe-based evaluation
6. Track artifact trail separately if critical
7. Monitor re-fetching frequency as quality signal
