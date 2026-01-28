---
name: developer-skills-inventory
description: This skill should be used when the user asks to "assess team skills", "create skills matrix", "identify skill gaps", "plan team training", "map skills to roadmap", or "build capability assessment". Creates team skills inventory with gap analysis against product roadmap and structured training plans.
version: 0.1.0
license: MIT
---

# Developer Skills Inventory

Map team skills, identify gaps against roadmap needs, and create targeted training plans.

## Purpose

- Inventory current team capabilities
- Identify skill gaps vs. product roadmap
- Prioritize training and hiring
- Plan knowledge transfer and documentation
- Reduce key person dependencies

## Skills Matrix Template

```json
{
  "team": "Platform Engineering",
  "assessment_date": "2026-01-22",
  "skills": [
    {
      "category": "Backend",
      "skills": [
        {
          "name": "Python",
          "team_coverage": {
            "expert": ["Alice", "Bob"],
            "proficient": ["Carol", "Dave"],
            "learning": ["Eve"],
            "none": []
          },
          "criticality": "high",
          "roadmap_need": "high"
        },
        {
          "name": "Go",
          "team_coverage": {
            "expert": [],
            "proficient": ["Alice"],
            "learning": ["Bob"],
            "none": ["Carol", "Dave", "Eve"]
          },
          "criticality": "medium",
          "roadmap_need": "high",
          "gap": "Need 2 experts for Q2 microservices rewrite"
        }
      ]
    }
  ],
  "training_plan": [
    {
      "skill": "Go",
      "priority": "high",
      "action": "2 engineers to complete Go training by Q2",
      "budget": "$2,000",
      "timeline": "12 weeks"
    }
  ]
}
```

## Gap Analysis Process

1. Map current skills (self-assessment + manager review)
2. Map roadmap requirements
3. Identify gaps (skill needed but lacking)
4. Prioritize (criticality × timeline)
5. Plan mitigation (training, hiring, vendors)

## Using Supporting Resources

### Templates
- **`templates/skills-matrix.json`** - Team skills inventory
- **`templates/training-plan.md`** - Structured training roadmap

### Scripts
- **`scripts/gap-analysis.py`** - Auto-identify skill gaps

---
