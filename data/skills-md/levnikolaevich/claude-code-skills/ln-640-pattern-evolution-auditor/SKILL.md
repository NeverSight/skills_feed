---
name: ln-640-pattern-evolution-auditor
description: "Audits architectural patterns against best practices (MCP Ref, Context7, WebSearch). Maintains patterns catalog, calculates 4 scores, creates refactor Stories via ln-220. Use when user asks to: (1) Check architecture health, (2) Audit patterns before refactoring, (3) Find undocumented patterns in codebase."
---

# Pattern Evolution Auditor

L2 Coordinator that analyzes implemented architectural patterns against current best practices, tracks evolution over time, and creates Stories for improvements.

## Purpose & Scope

- Maintain `docs/project/patterns_catalog.md` with implemented patterns
- Research best practices via MCP Ref, Context7, WebSearch
- Audit layer boundaries via ln-642 (detect violations, check coverage)
- Calculate 4 scores per pattern via ln-641
- Create Stories for patterns with score < 70% via ln-220
- Track quality trends over time (improving/stable/declining)

## 4-Score Model

| Score | What it measures | Threshold |
|-------|------------------|-----------|
| **Compliance** | Industry standards, ADR/Guide, naming, layer boundaries | 70% |
| **Completeness** | All components, error handling, tests, docs | 70% |
| **Quality** | Readability, maintainability, no smells, SOLID, no duplication | 70% |
| **Implementation** | Code exists, production use, integrated, monitored | 70% |

## Worker Invocation

> **CRITICAL:** All delegations use Task tool with `subagent_type: "general-purpose"` for context isolation.

| Worker | Purpose | Phase |
|--------|---------|-------|
| ln-641-pattern-analyzer | Calculate 4 scores per pattern | Phase 4 |
| ln-642-layer-boundary-auditor | Detect layer violations | Phase 3 |
| ln-643-api-contract-auditor | Audit API contracts, DTOs, layer leakage | Phase 4 |
| ln-220-story-coordinator | Create refactor Stories | Phase 6 |

**Prompt template:**
```
Task(description: "[Audit/Create] via ln-6XX",
     prompt: "Execute {skill-name}. Read skill from {skill-name}/SKILL.md. Pattern: {pattern}",
     subagent_type: "general-purpose")
```

**Anti-Patterns:**
- ❌ Direct Skill tool invocation without Task wrapper
- ❌ Any execution bypassing subagent context isolation

## Workflow

### Phase 1: Discovery

```
1. Load docs/project/patterns_catalog.md
   IF missing → create from shared/templates/patterns_template.md

2. Load docs/reference/adrs/*.md → link patterns to ADRs
   Load docs/reference/guides/*.md → link patterns to Guides

3. Auto-detect undocumented patterns
   Use patterns from common_patterns.md "Pattern Detection" table
   IF found but not in catalog → add as "Undocumented"
```

### Phase 2: Best Practices Research

```
FOR EACH pattern WHERE last_audit > 30 days OR never:

  # MCP Ref + Context7 + WebSearch
  ref_search_documentation("{pattern} best practices {tech_stack}")
  IF pattern.library: query-docs(library_id, "{pattern}")
  WebSearch("{pattern} implementation best practices 2026")

  → Store: contextStore.bestPractices[pattern]
```

### Phase 3: Layer Boundary Audit

```
Task(ln-642-layer-boundary-auditor)
  Input: architecture_path, codebase_root, skip_violations
  Output: violations[], coverage{}

# Apply deductions to affected patterns (per scoring_rules.md)
FOR EACH violation IN violations:
  affected_pattern = match_violation_to_pattern(violation)
  affected_pattern.issues.append(violation)
  affected_pattern.compliance_deduction += get_deduction(violation)
```

### Phase 4: Pattern Analysis Loop

```
# Analyze individual patterns
FOR EACH pattern IN catalog:
  Task(ln-641-pattern-analyzer)
    Input: pattern, locations, adr_reference, bestPractices
    Output: scores{}, issues[], gaps{}

# Analyze API contracts (always, in parallel with patterns)
Task(ln-643-api-contract-auditor)
  Input: pattern="API Contracts", locations=[service_dirs, api_dirs], bestPractices
  Output: scores{}, issues[], gaps{}

  **Worker Output Contract:**
  - ln-641 returns: `{overall_score: X.X, scores: {compliance, completeness, quality, implementation}, issues: [], gaps: {}}`
  - ln-642 returns: `{category, score, total_issues, critical, high, medium, low, findings: []}`
  - ln-643 returns: `{overall_score: X.X, scores: {compliance, completeness, quality, implementation}, issues: [], gaps: {}}`

  # Merge layer violations from Phase 3
  pattern.issues += layer_violations.filter(v => v.pattern == pattern)
  pattern.scores.compliance -= compliance_deduction
  pattern.scores.quality -= quality_deduction
```

### Phase 5: Gap Analysis

```
gaps = {
  undocumentedPatterns: found in code but not in catalog,
  implementationGaps: ADR decisions not implemented,
  layerViolations: code in wrong architectural layers,
  consistencyIssues: conflicting patterns
}
```

### Phase 6: Story Creation (via ln-220)

**REFACTORING PRINCIPLE (MANDATORY):**
> Stories MUST include: **"Zero Legacy / Zero Backward Compatibility"** — no compatibility hacks, clean architecture is priority.

```
refactorItems = patterns WHERE any_score < 70%

IF refactorItems.length > 0:
  # Auto-detect Epic (Architecture/Refactoring/Technical Debt)
  targetEpic = find_epic(["Architecture", "Refactoring", "Technical Debt"])
  IF not found → AskUserQuestion

  FOR EACH pattern IN refactorItems:
    Task(ln-220-story-coordinator)
      Create Story with AC from issues list
      MANDATORY AC: Zero Legacy principle
```

### Aggregation Algorithm

```
# Step 1: Get all worker scores (0-10 scale)
pattern_scores = [p.overall_score for p in ln641_results]  # Each 0-10
layer_score = ln642_result.score                            # 0-10
api_score = ln643_result.overall_score                      # 0-10

# Step 2: Calculate architecture_health_score
all_scores = pattern_scores + [layer_score, api_score]
architecture_health_score = round(average(all_scores) * 10)  # 0-100 scale

# Status mapping:
# >= 80: "healthy"
# 70-79: "warning"
# < 70: "critical"
```

### Phase 7: Report + Trend Analysis

```
1. Update patterns_catalog.md:
   - Pattern scores, dates, Story links
   - Layer Boundary Status section
   - Quick Wins section
   - Patterns Requiring Attention section

2. Calculate trend: compare current vs previous scores

3. Output summary (see Return Result below)
```

### Phase 7: Return Result

```json
{
  "audit_date": "2026-02-04",
  "architecture_health_score": 78,
  "trend": "improving",
  "patterns_analyzed": 5,
  "layer_audit": {
    "architecture_type": "Layered",
    "violations_total": 5,
    "violations_by_severity": {"high": 2, "medium": 3, "low": 0},
    "coverage": {"http_abstraction": 85, "error_centralization": true}
  },
  "patterns": [
    {
      "name": "Job Processing",
      "scores": {"compliance": 72, "completeness": 85, "quality": 68, "implementation": 90},
      "avg_score": 79,
      "status": "warning",
      "issues_count": 3,
      "story_created": "LIN-123"
    }
  ],
  "quick_wins": [
    {"pattern": "Caching", "issue": "Add TTL config", "effort": "2h", "impact": "+10 completeness"}
  ],
  "requires_attention": [
    {"pattern": "Event-Driven", "avg_score": 58, "critical_issues": ["No DLQ", "No schema versioning"]}
  ],
  "stories_created": ["LIN-123", "LIN-124"]
}
```

## Critical Rules

- **MCP Ref first:** Always research best practices before analysis
- **Layer audit first:** Run ln-642 before ln-641 pattern analysis
- **4 scores mandatory:** Never skip any score calculation
- **Layer deductions:** Apply scoring_rules.md deductions for violations
- **ln-220 for Stories:** Create Stories, not standalone tasks
- **Zero Legacy:** Refactor Stories must include "no backward compatibility" AC
- **Auto-detect Epic:** Only ask user if cannot determine automatically

## Definition of Done

- Pattern catalog loaded or created
- Best practices researched for all patterns needing audit
- Layer boundaries audited via ln-642 (violations detected, coverage calculated)
- All patterns analyzed via ln-641 (4 scores with layer deductions applied)
- Gaps identified (undocumented, unimplemented, layer violations, inconsistent)
- Stories created via ln-220 for patterns with score < 70%
- Catalog updated with scores, dates, Layer Boundary Status, Story links
- Trend analysis completed
- Summary report output

## Reference Files

- Pattern catalog template: `shared/templates/patterns_template.md`
- Common patterns detection: `references/common_patterns.md`
- Scoring rules: `references/scoring_rules.md`
- Pattern analysis: `../ln-641-pattern-analyzer/SKILL.md`
- Layer boundary audit: `../ln-642-layer-boundary-auditor/SKILL.md`
- API contract audit: `../ln-643-api-contract-auditor/SKILL.md`
- Story creation: `../ln-220-story-coordinator/SKILL.md`

---
**Version:** 1.1.0
**Last Updated:** 2026-01-29
