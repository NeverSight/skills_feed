---
name: developer-career-ladder
description: This skill should be used when the user asks to "create career ladder", "define engineering levels", "build competency framework", "design promotion criteria", or "create leveling guide". Defines engineering levels with competencies, promotion packet templates, and evidence examples.
version: 0.1.0
license: MIT
---

# Developer Career Ladder

Design comprehensive engineering career ladders with clear competency frameworks, promotion criteria, and evidence templates.

## Purpose

Create career ladders that:
- Define expectations for each engineering level
- Provide transparent promotion pathways
- Establish consistent evaluation criteria
- Guide career development conversations
- Support fair, evidence-based promotions

## Career Ladder Structure

### Level Definitions

**Individual Contributor (IC) Track:**

| Level | Title | Years Exp | Scope | Impact |
|-------|-------|-----------|-------|--------|
| L3 | Junior Engineer | 0-2 | Individual tasks | Team |
| L4 | Engineer | 2-5 | Features | Team |
| L5 | Senior Engineer | 5-8 | Projects | Multiple teams |
| L6 | Staff Engineer | 8-12 | Initiatives | Org/Product |
| L7 | Senior Staff | 12-15 | Strategic | Company |
| L8 | Principal | 15+ | Vision | Industry |

**Management Track:**

| Level | Title | Years Exp | Team Size | Scope |
|-------|-------|-----------|-----------|-------|
| M4 | Engineering Manager | 5+ | 4-8 ICs | Single team |
| M5 | Senior EM | 8+ | 8-12 | Multiple teams |
| M6 | Director | 10+ | 15-30 | Department |
| M7 | Senior Director | 12+ | 30-60 | Large org |
| M8 | VP Engineering | 15+ | 60+ | Engineering org |

### Competency Framework

**Three Core Competencies:**
1. **Technical Excellence** (varies by level)
2. **Leadership & Influence** (increases with level)
3. **Collaboration & Impact** (increases with level)

**Senior Engineer (L5) Example:**

```json
{
  "level": "L5",
  "title": "Senior Engineer",
  "competencies": {
    "technical": {
      "weight": 0.60,
      "expectations": [
        "Designs and implements complex systems independently",
        "Makes sound architectural decisions for team's domain",
        "Debugs issues across stack/services",
        "Writes high-quality, maintainable code",
        "Considers scale, performance, reliability"
      ],
      "evidence_examples": [
        "Led migration to new database with zero downtime",
        "Designed caching layer that reduced latency 70%",
        "Implemented monitoring that caught 3 production issues before customer impact"
      ]
    },
    "leadership": {
      "weight": 0.25,
      "expectations": [
        "Mentors 2-3 junior/mid engineers",
        "Leads technical design for medium-large projects",
        "Influences technical decisions beyond own team",
        "Improves team processes and practices"
      ],
      "evidence_examples": [
        "Mentored 2 engineers who were promoted",
        "Led design review process improvement, reduced time 30%",
        "Presented technical deep-dive at engineering all-hands"
      ]
    },
    "collaboration": {
      "weight": 0.15,
      "expectations": [
        "Partners effectively with PM, design, data",
        "Communicates technical concepts to non-technical stakeholders",
        "Drives consensus on technical decisions",
        "Contributes to engineering culture"
      ],
      "evidence_examples": [
        "Led cross-functional project with PM and design",
        "Wrote technical blog post (external or internal)",
        "Organized engineering book club"
      ]
    }
  }
}
```

## Promotion Packet Template

```markdown
# Promotion Packet: [Name] → [Target Level]

## Summary
[1 paragraph: why this person is ready for next level]

## Competency Evidence

### Technical Excellence
**Expectation for [Target Level]:** [Paste from ladder]

**Evidence:**
1. [Project/accomplishment with impact]
   - What: [Description]
   - Impact: [Quantified outcome]
   - Level indicator: [Why this demonstrates next-level work]

2. [Project/accomplishment]
   [Same structure]

### Leadership & Influence
[Same structure]

### Collaboration & Impact
[Same structure]

## Peer Feedback

"[Quote from peer feedback highlighting next-level work]" - [Peer Name, Role]

"[Quote from peer feedback]" - [Peer Name, Role]

## Growth & Trajectory

- [Example of taking on next-level work proactively]
- [Example of consistent performance over time]
- [Example of learning and adaptation]

## Recommendation

[Manager's recommendation: Ready now / Ready in X months / Not yet ready]
[Justification]

## Approval

- [ ] Manager: [Name]
- [ ] Skip-level: [Name]
- [ ] Director: [Name]
- [ ] Calibration committee (if applicable)
```

## Using Supporting Resources

### Templates
- **`templates/levels-competencies.json`** - Full ladder definition
- **`templates/promotion-packet.md`** - Promotion case template

### References
- **`references/level-examples.md`** - Real-world promotion examples
- **`references/calibration.md`** - Promotion calibration process

### Scripts
- **`scripts/validate-ladder.py`** - Check ladder completeness

---

**Progressive Disclosure:** Detailed level expectations, calibration processes, and edge cases in references/.
