---
name: bv
description: High-performance graph analysis for beads issue tracker using 9 metrics (PageRank, Betweenness, HITS, Critical Path, etc). Provides AI-driven task prioritization, dependency analysis, and architectural health monitoring via robot protocol.
version: 1.0.0
author: AI Agent Framework
tags: [project-management, graph-analysis, prioritization, dependencies, metrics, ci-cd]
triggers:
  - keywords: [prioritize, dependencies, bottleneck, critical path, graph analysis, project health, sprint planning, architectural debt, refactoring]
  - commands: [bv]
  - file_patterns: [.beads/, .bv/]
---

# bv Skill: AI-Driven Issue Tracker Analysis

## Overview

`bv` (beads_viewer) is a **high-performance Go TUI** for analyzing beads issue tracker dependency graphs. This skill enables AI agents to leverage `bv`'s **robot protocol** for intelligent task prioritization, dependency analysis, and architectural health monitoring.

**Key Principle:** **NEVER launch the interactive TUI**. Always use `--robot-*` flags for structured JSON output.

---

## When to Use This Skill

Activate this skill when:

### Task Prioritization
- "What should I work on next?"
- "Which issues are blocking the most work?"
- "What's the highest impact task?"
- Sprint planning and backlog grooming

### Dependency Analysis
- "What depends on this issue?"
- "What are the dependencies for this feature?"
- "What will this unblock?"
- Understanding sequential vs parallelizable work

### Project Health Monitoring
- "Is the project architecture healthy?"
- "Are there circular dependencies?"
- "Is the codebase too coupled?"
- Detecting architectural drift in CI/CD

### Architectural Refactoring
- "What are the bottlenecks?"
- "Which issues should we refactor first?"
- "How can we reduce coupling?"
- Identifying technical debt

### Historical Analysis
- "What changed since last sprint?"
- "Is project health improving or degrading?"
- "How has complexity evolved?"
- Release retrospectives

---

## Core Capabilities

### 1. Graph Metrics (9 Dimensions)

`bv` computes comprehensive metrics for every issue:

| Metric | Meaning | Use Case |
|--------|---------|----------|
| **PageRank** | Blocking power | Foundational dependencies |
| **Betweenness** | Bottleneck status | Bridge issues between work streams |
| **HITS (Hub/Authority)** | Dependency nature | Integration vs foundation work |
| **Critical Path** | Chain depth | Sequential dependency length |
| **Eigenvector** | Network influence | Importance of connected issues |
| **Degree** | Connection count | Direct dependencies |
| **Density** | Coupling measure | Overall graph health |
| **Cycles** | Circular dependencies | Architectural problems |
| **Topological Sort** | Valid execution order | Can work be sequenced? |

See [principles/graph-metrics.md](../bv-codebase/principles/graph-metrics.md) for detailed explanations.

---

### 2. Robot Protocol Commands

All commands return **structured JSON** for programmatic analysis:

#### Analysis Commands

```bash
# Comprehensive metrics
bv --robot-insights

# Execution plan with recommendations
bv --robot-plan

# Priority adjustment suggestions
bv --robot-priority

# Available filtering recipes
bv --robot-recipes
```

#### Historical Analysis

```bash
# Compare to historical point
bv --diff-since HEAD~10 --robot-diff
bv --diff-since v1.0.0 --robot-diff
bv --diff-since 2025-11-01 --robot-diff

# View historical state
bv --as-of v1.0.0 --robot-insights
```

#### Drift Detection

```bash
# Save baseline for future comparison
bv --save-baseline "Q4 2025 baseline - pre-refactoring"

# Check for architectural drift
bv --check-drift --robot-drift

# View baseline metadata
bv --baseline-info
```

#### Multi-Repository Support

```bash
# Aggregate multiple repositories
bv --workspace .bv/workspace.yaml --robot-insights

# Filter by repository
bv --workspace .bv/workspace.yaml --repo api --robot-plan
```

---

## Decision-Making Framework

### Priority Matrix

Use metric combinations to make intelligent recommendations:

| Scenario | Metrics | Action |
|----------|---------|--------|
| **Critical Bottleneck** | High PageRank + High Betweenness + High Critical Path | **HIGHEST PRIORITY** - blocks everything |
| **Foundational Work** | High PageRank + High Authority + Low Out-Degree | **HIGH PRIORITY** - enables downstream work |
| **Integration Point** | High Hub + High Betweenness | **COORDINATE** - needs many inputs |
| **Quick Win** | Low Degree + No dependencies | **PARALLELIZABLE** - good for side work |
| **Architectural Debt** | Part of cycle + High density | **REFACTOR** - break dependencies |
| **Isolated Feature** | Low all metrics + Degree = 0 | **INDEPENDENT** - work anytime |

### Health Indicators

**Healthy Project:**
```json
{
  "density": 0.2-0.4,
  "cycles": [],
  "topologicalSortValid": true,
  "healthTrend": "stable"
}
```

**Warning Signs:**
```json
{
  "density": 0.6-0.8,
  "cycles": [1-3],
  "highBetweennessConcentration": ">5 issues with score >0.8"
}
```

**Critical Issues:**
```json
{
  "density": ">0.8",
  "cycles": "4+",
  "topologicalSortValid": false
}
```

---

## Common Workflows

### 1. Initial Project Assessment

```bash
# Get comprehensive analysis
bv --robot-insights > insights.json

# Generate execution plan
bv --robot-plan > plan.json

# Check priority alignment
bv --robot-priority > priority.json

# Export human-readable report
bv --export-md health-report.md
```

**Decision Logic:**
```typescript
const insights = JSON.parse(fs.readFileSync('insights.json'));

if (insights.cycles.length > 0) {
  return "CRITICAL: Break cycles before other work";
} else if (insights.graphStats.density.density > 0.7) {
  return "WARNING: Over-coupled - recommend modularization";
} else {
  return `HEALTHY: Focus on ${plan.summary.recommendedNextIssue}`;
}
```

---

### 2. Sprint Planning

```bash
# Filter actionable issues (no blockers)
bv --recipe actionable --robot-plan > sprint-plan.json

# Get high-impact recommendations
bv --robot-insights | jq '.recommendations.highImpactIssues'

# Verify priorities
bv --robot-priority | jq '.recommendations[] | select(.confidence > 0.8)'
```

**Team Allocation:**
- **Senior engineers:** High impact (impactScore > 0.7)
- **Mid-level engineers:** Unblocking work (unblocks.length > 0)
- **Junior engineers:** Quick wins (no dependencies, low impact)

---

### 3. Architectural Refactoring

```bash
# Save baseline before refactoring
bv --save-baseline "Pre-refactoring baseline - $(date +%Y-%m-%d)"

# Identify refactoring targets
bv --robot-insights > current.json

# Prioritize by:
# 1. Break cycles (highest priority)
# 2. Extract bottlenecks (high betweenness)
# 3. Reduce coupling (high density)
# 4. Stabilize foundations (high PageRank)
```

---

### 4. CI/CD Health Monitoring

```yaml
# .github/workflows/architecture-health.yml
- name: Check drift
  run: bv --check-drift --robot-drift > drift-report.json

- name: Analyze results
  run: |
    EXIT_CODE=$(jq -r '.exitCode' drift-report.json)
    if [ "$EXIT_CODE" == "1" ]; then
      echo "::error::Critical drift - new cycles detected"
      exit 1
    elif [ "$EXIT_CODE" == "2" ]; then
      echo "::warning::Metrics degraded - review recommended"
    fi
```

**Exit Codes:**
- `0` = Healthy (no drift)
- `1` = Critical (new cycles)
- `2` = Warning (density increase, more blocked issues)

---

### 5. Historical Analysis

```bash
# Compare to last release
bv --diff-since v1.0.0 --robot-diff > release-diff.json

# Check health trend
jq -r '.summary.healthTrend' release-diff.json
# Output: 'improving', 'degrading', or 'stable'

# View resolved cycles
jq '.changes.resolvedCycles' release-diff.json
```

---

## TypeScript Integration

```typescript
import {
  InsightsResponse,
  PlanResponse,
  PriorityResponse,
  DiffResponse,
  DriftResponse
} from '../bv-codebase/types/core';

// Example: Check project health
async function checkProjectHealth(): Promise<void> {
  const { stdout } = await execAsync('bv --robot-insights');
  const insights: InsightsResponse = JSON.parse(stdout);

  const healthScore = calculateHealthScore(insights);

  if (healthScore < 60) {
    console.log('❌ CRITICAL: Immediate action required');
    console.log(`Cycles: ${insights.cycles.length}`);
    console.log(`Density: ${insights.graphStats.density.interpretation}`);
  } else if (healthScore < 80) {
    console.log('⚠️  WARNING: Architectural improvements recommended');
  } else {
    console.log('✅ HEALTHY: Project in good state');
  }
}

function calculateHealthScore(insights: InsightsResponse): number {
  let score = 100;

  // Deduct for cycles
  score -= insights.cycles.length * 15;

  // Deduct for high density
  if (insights.graphStats.density.density > 0.7) score -= 20;
  else if (insights.graphStats.density.density > 0.5) score -= 10;

  // Deduct for bottlenecks
  const bottlenecks = insights.metrics.betweenness.filter(m => m.score > 0.7);
  score -= bottlenecks.length * 5;

  return Math.max(0, score);
}
```

---

## Multi-Repository Support

### Workspace Configuration

```yaml
# .bv/workspace.yaml
repos:
  - name: core-api
    path: ../core-api
    prefix: api-

  - name: web-frontend
    path: ../web-frontend
    prefix: web-

  - name: mobile-app
    path: ../mobile-app
    prefix: mobile-
```

### Usage

```bash
# View all repositories together
bv --workspace .bv/workspace.yaml --robot-insights

# Filter by repository prefix
bv --workspace .bv/workspace.yaml --repo api --robot-plan

# Identify cross-repo dependencies (high betweenness)
bv --workspace .bv/workspace.yaml --robot-insights | \
  jq '.metrics.betweenness[] | select(.score > 0.7)'
```

**Namespaced Issue IDs:** `api-issue-001`, `web-issue-002`, `mobile-issue-003`

---

## Hook System

### Configuration (`.bv/hooks.yaml`)

```yaml
preExport:
  - name: validate
    command: ./scripts/validate-before-export.sh
    failOn: error

postExport:
  - name: notify-slack
    command: ./scripts/send-slack-notification.sh
    env:
      SLACK_WEBHOOK: $SLACK_WEBHOOK_URL
    failOn: never

  - name: upload-report
    command: ./scripts/upload-to-s3.sh
    failOn: never
```

### Environment Variables

Available in hook scripts:
- `BV_EXPORT_PATH` - Output file path
- `BV_EXPORT_FORMAT` - `markdown` or `json`
- `BV_ISSUE_COUNT` - Total issues
- `BV_TIMESTAMP` - Export timestamp

### Skip Hooks

```bash
bv --export-md report.md --no-hooks
```

---

## Performance Optimization

### Automatic Metric Skipping

- **Small graphs (< 100 nodes):** All 9 metrics computed (~1s)
- **Medium graphs (100-1000 nodes):** Skip betweenness unless needed (~2-5s)
- **Large graphs (> 1000 nodes):** Essential metrics only (~5-10s)

### Force Full Analysis

```bash
bv --force-full-analysis --robot-insights
```

**Use when:** Comprehensive audit required (may take 30s+ for large graphs)

### Profiling

```bash
# Human-readable
bv --profile-startup

# JSON for monitoring systems
bv --profile-startup --profile-json
```

---

## Error Handling

All robot commands return valid JSON even on error:

```json
{
  "error": true,
  "message": "No baseline found. Run --save-baseline first.",
  "code": "NO_BASELINE",
  "suggestion": "bv --save-baseline \"Initial baseline\""
}
```

**Always parse JSON safely:**
```typescript
try {
  const result = JSON.parse(stdout) as InsightsResponse;
  // Process result
} catch (error) {
  console.error('Failed to parse bv output:', error);
}
```

---

## Best Practices

### ✅ DO

1. **Always use `--robot-*` flags** - never launch the TUI
2. **Parse JSON output** - structured data for programmatic decisions
3. **Check exit codes in CI** - `0` = success, `1` = critical, `2` = warning
4. **Save baselines before major changes** - enables drift detection
5. **Combine commands for rich analysis** - layer insights for better decisions
6. **Use recipes for filtering** - `--recipe actionable` for sprint planning
7. **Track metrics over time** - use `--diff-since` for trends

### ❌ DON'T

1. **Never run `bv` without robot flags** - will block indefinitely in TUI
2. **Don't ignore cycles** - circular dependencies must be resolved
3. **Don't skip drift checks in CI** - prevents architectural degradation
4. **Don't force full analysis unnecessarily** - slow for large graphs
5. **Don't parse human-readable output** - always use JSON from robot commands
6. **Don't create baselines without descriptions** - context is critical

---

## Quick Reference

### Command Cheatsheet

```bash
# Analysis
bv --robot-insights                           # Full metrics
bv --robot-plan                               # Execution plan
bv --robot-priority                           # Priority recommendations
bv --robot-recipes                            # Available recipes

# Historical
bv --diff-since HEAD~10 --robot-diff          # Compare to 10 commits ago
bv --diff-since v1.0.0 --robot-diff           # Compare to release tag
bv --diff-since 2025-11-01 --robot-diff       # Compare to date
bv --as-of v1.0.0 --robot-insights            # View historical state

# Drift Detection
bv --save-baseline "description"              # Save current metrics
bv --check-drift --robot-drift                # Check for drift
bv --baseline-info                            # View baseline metadata

# Multi-Repo
bv --workspace .bv/workspace.yaml --robot-insights    # All repos
bv --workspace .bv/workspace.yaml --repo api --robot-plan  # Filter by repo

# Filtering
bv --recipe actionable --robot-plan           # No blockers
bv --recipe high-impact --robot-insights      # High metrics
bv --recipe blocked --robot-insights          # Issues with blockers

# Export
bv --export-md report.md                      # Markdown report
bv --export-md report.md --no-hooks           # Skip hooks

# Performance
bv --force-full-analysis --robot-insights     # Compute all metrics
bv --profile-startup --profile-json           # Performance profiling
```

### JQ Helpers

```bash
# Extract specific data
bv --robot-insights | jq '.recommendations.highImpactIssues'
bv --robot-plan | jq '.summary.recommendedNextIssue'
bv --robot-priority | jq '.recommendations[] | select(.confidence > 0.8)'

# Filter by metrics
bv --robot-insights | jq '.metrics.pageRank[] | select(.score > 0.7)'
bv --robot-insights | jq '.metrics.betweenness[] | select(.score > 0.8)'

# Check health
bv --robot-insights | jq '.cycles | length'
bv --robot-insights | jq '.graphStats.density.interpretation'
bv --check-drift --robot-drift | jq '.exitCode'
```

---

## Files & Resources

### Skill Files
- [SKILL.md](./SKILL.md) - This file
- [scripts/metrics-validator.sh](./scripts/metrics-validator.sh) - Validate metrics output
- [references/robot-commands.md](./references/robot-commands.md) - Complete command reference
- [references/graph-analysis.md](./references/graph-analysis.md) - Metric interpretation guide
- [assets/cheatsheet.md](./assets/cheatsheet.md) - Quick command reference

### Codebase Files
- [../bv-codebase/types/core.ts](../bv-codebase/types/core.ts) - TypeScript type definitions
- [../bv-codebase/principles/graph-metrics.md](../bv-codebase/principles/graph-metrics.md) - Deep dive into metrics
- [../bv-codebase/principles/robot-protocol.md](../bv-codebase/principles/robot-protocol.md) - Protocol documentation
- [../bv-codebase/templates/analysis-workflow.md](../bv-codebase/templates/analysis-workflow.md) - Common patterns
- [../bv-codebase/README.md](../bv-codebase/README.md) - Codebase overview

---

## Installation

```bash
# macOS (Homebrew)
brew install beadslabs/tap/bv

# Linux
curl -L https://github.com/beadslabs/bv/releases/latest/download/bv-linux-amd64 -o bv
chmod +x bv
sudo mv bv /usr/local/bin/

# Verify
bv --version
```

---

## Troubleshooting

**Issue:** `bv` hangs forever
- **Cause:** TUI launched without robot flag
- **Fix:** Always use `--robot-*` flags

**Issue:** Empty JSON response
- **Cause:** No issues in `.beads/` directory
- **Fix:** Verify tracker exists

**Issue:** Metrics missing in output
- **Cause:** Large graph, automatic skipping
- **Fix:** Use `--force-full-analysis`

**Issue:** Drift check always returns 0
- **Cause:** No baseline saved
- **Fix:** Run `bv --save-baseline "Initial baseline"` first

---

## Examples

### Example 1: Sprint Planning

```bash
#!/bin/bash
# Generate sprint plan

# 1. Get actionable issues
bv --recipe actionable --robot-plan > sprint-plan.json

# 2. Extract high-impact work
HIGH_IMPACT=$(jq -r '.tracks[].items[] | select(.impactScore > 0.7) | .issueId' sprint-plan.json)

# 3. Extract quick wins
QUICK_WINS=$(jq -r '.tracks[].items[] | select(.dependencies | length == 0) | select(.unblocks | length == 0) | .issueId' sprint-plan.json)

echo "High Impact Issues:"
echo "$HIGH_IMPACT"
echo ""
echo "Quick Wins:"
echo "$QUICK_WINS"
```

### Example 2: CI Health Check

```bash
#!/bin/bash
# CI pipeline drift check

bv --check-drift --robot-drift > drift-report.json
EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ]; then
  echo "❌ CRITICAL: New cycles detected"
  jq -r '.alerts[] | select(.level == "critical") | .message' drift-report.json
  exit 1
elif [ $EXIT_CODE -eq 2 ]; then
  echo "⚠️  WARNING: Metrics degraded"
  jq -r '.alerts[] | select(.level == "warning") | .message' drift-report.json
  exit 0
else
  echo "✅ HEALTHY: No drift detected"
  exit 0
fi
```

### Example 3: Priority Validation

```bash
#!/bin/bash
# Check for priority misalignments

bv --robot-priority > priority-check.json

HIGH_CONFIDENCE=$(jq '.recommendations[] | select(.confidence > 0.8)' priority-check.json)

if [ -n "$HIGH_CONFIDENCE" ]; then
  echo "⚠️  High-confidence priority adjustments recommended:"
  echo "$HIGH_CONFIDENCE" | jq -r '"\(.issueId): P\(.currentPriority) → P\(.recommendedPriority) (\(.reasoning))"'
else
  echo "✅ Priorities are well-aligned with metrics"
fi
```

---

## Version Compatibility

- **bv:** v1.0.0+
- **Robot Protocol:** v1.x (semver-stable)
- **This Skill:** v1.0.0

---

## License

This skill documentation is provided for AI agents and developers.

**bv** is developed by Beads Labs. See https://github.com/beadslabs/bv for tool licensing.
