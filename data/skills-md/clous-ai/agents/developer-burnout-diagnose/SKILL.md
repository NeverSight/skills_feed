---
name: developer-burnout-diagnose
description: This skill should be used when the user asks to "detect burnout", "analyze workload patterns", "check team health", "investigate after-hours work", "analyze on-call load", or "assess burnout risk". Analyzes workload, after-hours activity, incident patterns, and other burnout indicators with actionable recommendations.
version: 0.1.0
license: MIT
---

# Developer Burnout Diagnosis

Detect and diagnose engineering burnout through data analysis of workload patterns, after-hours activity, and incident load.

## Purpose

- Identify burnout warning signs early
- Analyze workload distribution
- Detect unsustainable patterns
- Recommend interventions
- Prevent attrition

## Burnout Indicators

### Git Activity Analysis

**Metrics to analyze:**
```bash
# Commits by hour (detect after-hours work)
git log --author="Name" --date=format:'%H' --pretty=format:'%ad' | sort | uniq -c

# Commits by day of week (weekend work)
git log --author="Name" --date=format:'%u' --pretty=format:'%ad' | sort | uniq -c

# Commit velocity trend
git log --author="Name" --since="6 months ago" --pretty=format:'%ad' --date=short | uniq -c
```

**Warning Signs:**
- >20% commits outside 9am-6pm
- Regular weekend commits (>10% of total)
- Declining commit volume over time
- Late-night activity spikes (after 10pm)

### On-Call Analysis

**Metrics:**
- Incidents per on-call shift
- After-hours pages
- Time to resolve
- Rotation frequency

**Warning Signs:**
- >3 incidents per week on-call
- >5 after-hours pages per shift
- Uneven rotation (same person always on-call)
- Long incident resolution times (>4 hours)

### Workload Distribution

**Metrics:**
- PR review load per engineer
- Number of concurrent projects
- Meeting hours per week
- Context switches (number of different projects/repos)

**Warning Signs:**
- >10 PRs to review per week
- Working on >3 projects simultaneously
- >20 hours meetings per week
- Frequent context switches (>5 different areas)

## Burnout Risk Assessment

```json
{
  "employee": "Name",
  "assessment_date": "2026-01-22",
  "risk_level": "high",
  "indicators": [
    {
      "category": "After-hours work",
      "severity": "high",
      "evidence": "35% of commits between 8pm-1am",
      "trend": "increasing"
    },
    {
      "category": "On-call load",
      "severity": "medium",
      "evidence": "4.2 incidents per on-call week (team avg: 2.1)",
      "trend": "stable"
    }
  ],
  "recommendations": [
    {
      "action": "Reduce on-call frequency",
      "details": "Currently 1 week per month, reduce to 1 week per 6 weeks",
      "timeline": "immediate"
    },
    {
      "action": "Audit workload",
      "details": "Working on 4 projects - consolidate to 2 max",
      "timeline": "next sprint"
    },
    {
      "action": "Investigate after-hours work drivers",
      "details": "1:1 to understand: deadline pressure? personal preference? timezone issues?",
      "timeline": "this week"
    }
  ]
}
```

## Intervention Strategies

**Immediate (High Risk):**
- Reduce workload (remove from projects)
- Pause on-call rotation
- Encourage PTO
- 1:1 check-in

**Medium-term:**
- Redistribute work more evenly
- Address systemic issues (too many incidents)
- Improve tooling/processes
- Add headcount if needed

**Long-term:**
- Build sustainable practices
- Improve incident prevention
- Cross-train team (reduce dependencies)
- Establish work-life boundaries

## Using Supporting Resources

### Templates
- **`templates/burnout-indicators.json`** - Metrics checklist
- **`templates/recommendations.md`** - Intervention playbook

### Scripts
- **`scripts/analyze-workload.py`** - Git activity analysis
- **`scripts/on-call-metrics.py`** - On-call load calculator

---
