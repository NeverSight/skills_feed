---
name: bmad-performance-optimization
description: Diagnoses bottlenecks and designs performance optimization plans.
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "performance budget"
      - "optimize speed"
      - "slow response"
      - "profiling results"
      - "latency regression"
      - "load testing"
      - "capacity planning"
    keywords:
      - performance
      - latency
      - throughput
      - optimize
      - scaling
      - profiling
      - benchmarking
  capabilities:
    - performance-audits
    - load-testing-plans
    - profiling-analysis
    - optimization-roadmaps
    - capacity-planning
  prerequisites:
    - bmad-architecture-design
    - bmad-test-strategy
  outputs:
    - performance-brief
    - benchmark-plan
    - optimization-backlog
---

# BMAD Performance Optimization Skill

## When to Invoke

Trigger this skill when the user:
- Reports latency, throughput, or resource regressions.
- Requests load/performance testing guidance or results interpretation.
- Needs to set or validate performance budgets and SLAs.
- Wants to plan scaling strategies ahead of a launch or marketing event.
- Asks how to tune code, queries, caching, or infrastructure for speed.

If the user only needs to implement a specific optimization already defined, delegate to `bmad-development-execution`.

## Mission

Deliver actionable insights, testing strategies, and prioritized optimizations that keep the product within agreed performance budgets while balancing cost and complexity.

## Inputs Required

- Current architecture diagrams and deployment topology.
- Observability data: metrics dashboards, traces, profiling dumps, load test reports.
- Performance requirements (SLAs/SLOs, budgets, target response times).
- Workload assumptions and peak usage scenarios.

Gather missing telemetry by coordinating with `bmad-observability-readiness` if instrumentation is lacking.

## Outputs

- **Performance brief** summarizing current state, key bottlenecks, and risks.
- **Benchmark and load test plan** aligning tools, scenarios, and success criteria.
- **Optimization backlog** ranked by impact vs. effort with owner and verification plan.
- Updated performance budget recommendations or SLO adjustments when necessary.

## Process

1. Validate inputs and ensure instrumentation coverage. Escalate gaps to observability skill.
2. Analyze telemetry to pinpoint hotspots (CPU, memory, I/O, DB, network, frontend paint times).
3. Assess architecture decisions for scalability (caching, asynchronous workflows, data partitioning).
4. Define performance goals and acceptance thresholds with stakeholders.
5. Create load/benchmark plans covering baseline, stress, soak, and spike scenarios.
6. Recommend optimizations across code, database, infrastructure, and CDN layers.
7. Produce backlog with measurable acceptance criteria and regression safeguards.

## Quality Gates

- Recommendations trace back to observed data or projected workloads.
- Each backlog item includes measurement approach (before/after metrics).
- Performance budgets and SLAs updated or reaffirmed.
- Risks communicated when goals require major architectural change.

## Error Handling

- If telemetry contradicts assumptions, schedule hypothesis-driven experiments rather than guessing.
- Flag when performance targets are unrealistic within constraints; propose trade-offs.
- When required tooling is unavailable, document blockers and coordinate with observability & dev skills.
