---
name: developer-onboarding-30-60-90
description: This skill should be used when the user asks to "create 30/60/90 plan", "design onboarding plan", "build new hire roadmap", "create onboarding milestones", "plan first 90 days", or "structure new engineer onboarding". Generates comprehensive, role-specific onboarding plans with measurable outcomes, stakeholder mapping, and risk mitigation for new engineering hires.
version: 0.1.0
license: MIT
---

# Developer Onboarding 30/60/90

Create structured onboarding plans that set new engineers up for success through clear milestones, measurable outcomes, and stakeholder engagement.

## Purpose

Design 30/60/90 day onboarding plans that:
- Define clear, measurable success criteria for each phase
- Map key stakeholders and relationships
- Identify risks and mitigation strategies
- Balance learning with early contributions
- Set expectations aligned with role level

## When to Use

Invoke when:
- New hire accepted offer, start date approaching
- Redesigning engineering onboarding process
- Onboarding contractor-to-FTE conversion
- Creating role-specific onboarding tracks
- Manager preparing for new team member

## Core Plan Structure

### 30-Day Plan: Foundation

**Goals:**
- Understand codebase, architecture, development workflow
- Complete environment setup and access provisioning
- Ship first small contribution
- Meet key stakeholders
- Understand team mission and current priorities

**Measurable Outcomes:**
- [ ] Development environment fully configured
- [ ] Successfully merged 1-2 small PRs (bug fixes, docs)
- [ ] Completed codebase onboarding (architecture walkthrough)
- [ ] Met 1:1 with manager, onboarding buddy, 3-5 teammates
- [ ] Attended team rituals (standups, sprint planning, retros)

**Activities:**
- Week 1: Setup, documentation, shadowing
- Week 2: First contributions (low-risk tickets)
- Week 3: Domain deep-dive, stakeholder meetings
- Week 4: Checkpoint with manager, reflection

**Stakeholders:**
- Onboarding buddy (day-to-day questions)
- Hiring manager (expectations, feedback)
- Tech lead (architecture, technical decisions)
- Cross-functional partners (PM, design, data)

**Risks:**
- Environment setup blockers → Mitigation: Pre-provision access
- Slow ramp due to codebase complexity → Mitigation: Pair programming
- Isolation (remote) → Mitigation: Daily check-ins, virtual coffee chats

### 60-Day Plan: Contribution

**Goals:**
- Own end-to-end features independently
- Demonstrate technical competency for level
- Build relationships across org
- Understand product roadmap and business context
- Begin mentoring/knowledge sharing

**Measurable Outcomes:**
- [ ] Shipped 1-2 medium-sized features independently
- [ ] Participated in on-call rotation (if applicable)
- [ ] Presented technical topic at team meeting
- [ ] Received peer feedback (formal or informal)
- [ ] Contributed to team processes (docs, tooling, best practices)

**Activities:**
- Week 5-6: Ramp up feature ownership
- Week 7: On-call shadowing or first shift
- Week 8: Mid-point review with manager

**Stakeholders:**
- Expanded team (other squads, adjacent teams)
- Product manager (roadmap context)
- Customers (user research, support tickets)

**Risks:**
- Overconfidence → moving too fast → Mitigation: Code review rigor
- Underconfidence → not asking for help → Mitigation: Explicit "ask questions" norm
- Misalignment on expectations → Mitigation: Clear rubrics, frequent feedback

### 90-Day Plan: Impact

**Goals:**
- Operate autonomously at level expectations
- Drive initiatives beyond assigned work
- Demonstrate ownership and leadership (for level)
- Receive positive performance feedback
- Successfully complete probation/trial period

**Measurable Outcomes:**
- [ ] Led design and implementation of significant feature
- [ ] Proactively identified and solved problem
- [ ] Positive feedback from peers and stakeholders
- [ ] Met all competency expectations for level (technical, leadership, collaboration)
- [ ] Manager recommendation to continue employment

**Activities:**
- Week 9-11: Full autonomy, larger projects
- Week 12: 90-day review with manager (formal feedback)
- Week 13+: Transition to regular performance cycle

**Stakeholders:**
- Leadership (skip-level, org leaders)
- Hiring panel (feedback loop for interview process)

**Risks:**
- Not meeting bar → Mitigation: Early intervention (week 4, 8 checkpoints)
- Burnout from over-achievement → Mitigation: Sustainable pace expectations
- Lack of feedback → Mitigation: Structured checkpoints

## Level-Specific Customization

### Junior Engineer (L3)
- **30 days:** Focus on setup, learning codebase, small tickets
- **60 days:** Ship 1 feature with heavy guidance
- **90 days:** Independently ship features, minimal guidance

### Mid Engineer (L4)
- **30 days:** Setup + small features independently
- **60 days:** Own medium features, some tech lead support
- **90 days:** Fully autonomous, begin mentoring juniors

### Senior Engineer (L5)
- **30 days:** Quick ramp, already contributing meaningfully
- **60 days:** Leading features, influencing technical direction
- **90 days:** Driving initiatives, mentoring team, improving processes

### Staff+ Engineer (L6+)
- **30 days:** Context gathering, relationship building
- **60 days:** Proposing strategic initiatives, cross-team influence
- **90 days:** Executing on strategic vision, org-level impact

## Output Template

```json
{
  "new_hire": {
    "name": "string",
    "role": "string",
    "level": "string",
    "start_date": "YYYY-MM-DD",
    "manager": "string",
    "onboarding_buddy": "string"
  },
  "plan_30_days": {
    "goals": ["array of strings"],
    "outcomes": ["array of measurable outcomes"],
    "activities": [
      {
        "week": 1,
        "focus": "string",
        "deliverables": ["array"]
      }
    ],
    "stakeholders": [
      {
        "name": "string",
        "role": "string",
        "interaction": "1:1|meeting|shadowing"
      }
    ],
    "risks": [
      {
        "risk": "string",
        "mitigation": "string"
      }
    ]
  },
  "plan_60_days": { /* similar structure */ },
  "plan_90_days": { /* similar structure */ },
  "checkpoints": [
    {
      "day": 7,
      "type": "informal",
      "focus": "Setup complete? Blockers?"
    },
    {
      "day": 30,
      "type": "formal",
      "focus": "Foundation laid? Ready for more ownership?"
    },
    {
      "day": 60,
      "type": "formal",
      "focus": "Contributing well? Feedback?"
    },
    {
      "day": 90,
      "type": "formal",
      "focus": "Performance review, probation decision"
    }
  ],
  "success_criteria": {
    "technical": "string - level-appropriate technical performance",
    "collaboration": "string - working well with team",
    "ownership": "string - taking initiative",
    "growth": "string - learning and adapting"
  }
}
```

## Using Supporting Resources

### Templates
- **`templates/30-60-90-template.json`** - Complete plan schema by level
- **`templates/stakeholder-map.md`** - Key relationships to build
- **`templates/checkpoint-agenda.md`** - Checkpoint meeting template

### References
- **`references/onboarding-best-practices.md`** - Research-backed approaches
- **`references/remote-onboarding.md`** - Remote-specific strategies

### Scripts
- **`scripts/validate-plan.py`** - Check plan completeness, measurability
- **`scripts/generate-calendar.py`** - Create checkpoint calendar invites

---

**Progressive Disclosure:** Detailed onboarding best practices, remote strategies, and role-level expectations in references/.
