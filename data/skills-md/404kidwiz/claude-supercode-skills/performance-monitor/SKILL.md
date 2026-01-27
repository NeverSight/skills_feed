---
name: performance-monitor
description: Expert in observing, benchmarking, and optimizing AI agents. Specializes in token usage tracking, latency analysis, and quality evaluation metrics. Use when optimizing agent costs, measuring performance, or implementing evals. Triggers include "agent performance", "token usage", "latency optimization", "eval", "agent metrics", "cost optimization", "agent benchmarking".
---

# Performance Monitor

## Purpose
Provides expertise in monitoring, benchmarking, and optimizing AI agent performance. Specializes in token usage tracking, latency analysis, cost optimization, and implementing quality evaluation metrics (evals) for AI systems.

## When to Use
- Tracking token usage and costs for AI agents
- Measuring and optimizing agent latency
- Implementing evaluation metrics (evals)
- Benchmarking agent quality and accuracy
- Optimizing agent cost efficiency
- Building observability for AI pipelines
- Analyzing agent conversation patterns
- Setting up A/B testing for agents

## Quick Start
**Invoke this skill when:**
- Optimizing AI agent costs and token usage
- Measuring agent latency and performance
- Implementing evaluation frameworks
- Building observability for AI systems
- Benchmarking agent quality

**Do NOT invoke when:**
- General application performance → use `/performance-engineer`
- Infrastructure monitoring → use `/sre-engineer`
- ML model training optimization → use `/ml-engineer`
- Prompt design → use `/prompt-engineer`

## Decision Framework
```
Optimization Goal?
├── Cost Reduction
│   ├── Token usage → Prompt optimization
│   └── API calls → Caching, batching
├── Latency
│   ├── Time to first token → Streaming
│   └── Total response time → Model selection
├── Quality
│   ├── Accuracy → Evals with ground truth
│   └── Consistency → Multiple run analysis
└── Reliability
    └── Error rates, retry patterns
```

## Core Workflows

### 1. Token Usage Tracking
1. Instrument API calls to capture usage
2. Track input vs output tokens separately
3. Aggregate by agent, task, user
4. Calculate costs per operation
5. Build dashboards for visibility
6. Set alerts for anomalous usage

### 2. Eval Framework Setup
1. Define evaluation criteria
2. Create test dataset with expected outputs
3. Implement scoring functions
4. Run automated eval pipeline
5. Track scores over time
6. Use for regression testing

### 3. Latency Optimization
1. Measure baseline latency
2. Identify bottlenecks (model, network, parsing)
3. Implement streaming where applicable
4. Optimize prompt length
5. Consider model size tradeoffs
6. Add caching for repeated queries

## Best Practices
- Track tokens separately from API call counts
- Implement evals before optimizing
- Use percentiles (p50, p95, p99) not averages for latency
- Log prompt and response for debugging
- Set cost budgets and alerts
- Version prompts and track performance per version

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| No token tracking | Surprise costs | Instrument all calls |
| Optimizing without evals | Quality regression | Measure before optimizing |
| Average-only latency | Hides tail latency | Use percentiles |
| No prompt versioning | Can't correlate changes | Version and track |
| Ignoring caching | Repeated costs | Cache stable responses |
