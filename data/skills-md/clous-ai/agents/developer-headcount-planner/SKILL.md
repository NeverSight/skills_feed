---
name: developer-headcount-planner
description: This skill should be used when the user asks to "plan headcount", "calculate capacity", "model team size", "plan hiring needs", "estimate engineering capacity", or "create headcount plan". Creates capacity models comparing team capacity to roadmap demands with hiring, contracting, or internal mobility recommendations.
version: 0.1.0
license: MIT
---

# Developer Headcount Planner

Model engineering capacity, compare to roadmap needs, and create data-driven headcount plans.

## Purpose

- Calculate current team capacity
- Model roadmap engineering needs
- Identify capacity gaps
- Recommend hiring vs. contract vs. internal mobility
- Plan hiring timeline and budget

## Capacity Model

### Current Capacity Calculation

```
Available capacity = Team size × Utilization rate × Weeks available

Where:
- Team size: FTE count
- Utilization rate: 0.6-0.7 (accounting for meetings, support, etc.)
- Weeks available: 52 - (PTO + holidays + on-call impact)

Example:
8 engineers × 0.65 utilization × 48 weeks = 250 engineer-weeks/year
```

### Roadmap Demand Estimation

```json
{
  "roadmap_q1_2026": [
    {
      "initiative": "API v2 migration",
      "estimated_effort": "60 engineer-weeks",
      "criticality": "high",
      "skills_required": ["Backend", "API design"]
    },
    {
      "initiative": "Mobile app launch",
      "estimated_effort": "80 engineer-weeks",
      "criticality": "high",
      "skills_required": ["Mobile", "Backend"]
    }
  ],
  "total_demand": "200 engineer-weeks",
  "current_capacity": "120 engineer-weeks",
  "gap": "80 engineer-weeks (40% under-capacity)"
}
```

### Gap Analysis

**Options to close gap:**
1. **Hire FTEs:** Longer-term, higher upfront cost, builds capability
2. **Contract:** Faster, flexible, higher hourly cost
3. **Internal mobility:** Fastest, lowest cost, may create gap elsewhere
4. **Descope:** Reduce roadmap ambition
5. **Timeline extension:** Push deadlines

**Decision Matrix:**

| Factor | Hire FTE | Contract | Internal Mobility |
|--------|----------|----------|-------------------|
| Speed | 3-6 months | 2-4 weeks | 1-2 weeks |
| Cost | $150k+/year | $100-200/hr | Transfer cost |
| Flexibility | Low | High | Medium |
| Knowledge retention | High | Low | High |
| Best for | Ongoing need | Temporary spike | Known skillset |

## Headcount Plan Output

```json
{
  "team": "Platform Engineering",
  "planning_period": "2026",
  "current_state": {
    "team_size": 8,
    "capacity_weeks": 250,
    "utilization": 0.65
  },
  "roadmap_demand": {
    "q1": 200,
    "q2": 180,
    "q3": 160,
    "q4": 140,
    "total": 680
  },
  "gap_analysis": {
    "total_gap": 180,
    "peak_quarter": "Q1",
    "skills_gaps": ["Mobile development", "DevOps"]
  },
  "recommendations": [
    {
      "action": "Hire 2 FTE backend engineers",
      "rationale": "Ongoing high demand, core capability",
      "timeline": "Start recruiting Q4 2025, onboard Q1 2026",
      "cost": "$300k/year",
      "capacity_added": "60 weeks/year"
    },
    {
      "action": "Contract 1 mobile engineer",
      "rationale": "Temporary need for mobile launch",
      "timeline": "Q1 2026, 6-month contract",
      "cost": "$80k total",
      "capacity_added": "24 weeks"
    }
  ],
  "budget": {
    "fte_hiring": "$300k",
    "contractors": "$80k",
    "total": "$380k"
  }
}
```

## Using Supporting Resources

### Templates
- **`templates/capacity-model.json`** - Capacity calculation template
- **`templates/hiring-plan.md`** - Headcount planning template

### Scripts
- **`scripts/validate-capacity.py`** - Model validation
- **`scripts/scenario-planner.py`** - What-if scenarios

---
