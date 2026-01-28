---
name: developer-performance-diagnostic
description: This skill should be used when the user asks to "diagnose performance issues", "analyze team performance", "investigate underperformance", "identify performance patterns", or "assess team health". Analyzes performance data to detect patterns, systemic issues, and individual concerns with data-driven recommendations.
version: 0.1.0
license: MIT
---

# Developer Performance Diagnostic

Systematically diagnose team and individual performance issues using data-driven analysis.

## Purpose

- Detect performance patterns (systemic vs. individual)
- Identify root causes (not just symptoms)
- Distinguish performance issues from external factors
- Recommend targeted interventions
- Track performance trends over time

## Diagnostic Framework

### Data Collection

**Quantitative Signals:**
- Velocity/throughput (stories/sprint, PRs/month)
- Quality (bug rates, incident frequency)
- Code review metrics (time to review, feedback quality)
- On-time delivery (deadline adherence)
- Availability (attendance, responsiveness)

**Qualitative Signals:**
- Peer feedback
- Stakeholder satisfaction
- 1:1 notes
- Code review comments
- Meeting participation

### Pattern Analysis

**Individual Underperformance:**
- Isolated to one person
- Peer feedback identifies specific behaviors
- Manager has documented concerns
- Performance gaps vs. level expectations

**Systemic Issues:**
- Multiple team members affected
- External factors (org changes, unclear priorities)
- Resource constraints (tooling, access)
- Process problems (inefficient workflows)

### Root Cause Identification

**Common Root Causes:**
1. Skill gaps (training needed)
2. Unclear expectations (communication issue)
3. Personal issues (health, family, burnout)
4. Poor management (lack of feedback, support)
5. Role misfit (wrong level or role type)
6. External blockers (dependencies, priorities)

## Diagnostic Output

```json
{
  "team": "Platform",
  "period": "Q4 2025",
  "findings": [
    {
      "type": "individual",
      "employee": "Name",
      "pattern": "Consistently missing sprint commitments",
      "evidence": [
        "Missed 4 of last 6 sprint goals",
        "Peer feedback: unclear communication about blockers"
      ],
      "root_cause": "Skill gap in task estimation + reluctance to ask for help",
      "recommendation": "Mentorship on estimation, explicit encouragement to surface blockers early",
      "urgency": "medium"
    },
    {
      "type": "systemic",
      "pattern": "Team velocity down 30% this quarter",
      "evidence": [
        "Average velocity: 45 → 32 story points",
        "All engineers report similar drop"
      ],
      "root_cause": "Increased on-call load (2x incidents) + unclear Q4 priorities",
      "recommendation": "Reduce scope, clarify priorities, investigate incident root causes",
      "urgency": "high"
    }
  ]
}
```

## Using Supporting Resources

### Templates
- **`templates/metrics-template.json`** - Performance metrics to track
- **`templates/diagnostic-framework.md`** - Root cause analysis guide

### Scripts
- **`scripts/analyze-patterns.py`** - Auto-detect performance anomalies

---
