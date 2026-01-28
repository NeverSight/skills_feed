---
name: performance-management
version: "2.0.0"
description: Master performance management, goal-setting, OKRs, reviews, feedback, and metrics for engineering teams
sasmp_version: "1.3.0"
bonded_agent: 03-hiring-performance-agent
bond_type: PRIMARY_BOND
category: performance
input_validation:
  required_context: ["review_type"]
  optional_context: ["employee_level", "timeline"]
retry_config:
  max_attempts: 2
  backoff: exponential
observability:
  log_level: info
  metrics: [invocation_count, success_rate, latency]
---

# Performance Management Skill

## Purpose
Provide engineering managers with frameworks for effective performance management, goal-setting, OKRs, reviews, and continuous feedback.

## Primary Bond
**Agent**: hiring-performance-agent
**Relationship**: This skill provides review templates, OKR frameworks, and feedback models that the agent uses.

---

## Templates

### OKR Template

```yaml
okr_template:
  metadata:
    owner: "{Name}"
    quarter: "{Q1 2025}"
    created: "{Date}"
    last_reviewed: "{Date}"

  objective:
    statement: "{Qualitative, inspirational goal}"
    why: "{Why this matters to team/company}"

  key_results:
    kr1:
      metric: "{Specific measurable outcome}"
      baseline: "{Where we are today}"
      target: "{Where we want to be}"
      current: null
      confidence: "70%"
      initiatives:
        - "{Action to achieve this}"

    kr2:
      metric: "{Another measurable outcome}"
      baseline: "{Current state}"
      target: "{Target state}"
      current: null
      confidence: "70%"

    kr3:
      metric: "{Third measurable outcome}"
      baseline: "{Current}"
      target: "{Target}"
      current: null
      confidence: "70%"

  scoring:
    "0.0-0.3": "Failed to make progress"
    "0.4-0.6": "Made progress but fell short"
    "0.7-0.9": "Delivered (target zone)"
    "1.0": "Fully achieved (might not have been ambitious enough)"

  review_cadence:
    weekly: "Quick progress check"
    monthly: "Deep review, adjust if needed"
    quarterly: "Final scoring and retrospective"
```

### Performance Review Template

```yaml
performance_review:
  metadata:
    employee: "{Name}"
    level: "{Current level}"
    manager: "{Manager name}"
    review_period: "{Date range}"
    review_date: "{Date}"

  overall_rating:
    scale: "[1-5]"
    rating: null
    summary: ""

  rating_definitions:
    5: "Exceptional - Top 5%, role model, exceptional impact"
    4: "Exceeds - Frequently exceeds expectations"
    3: "Meets - Consistently meets expectations"
    2: "Developing - Partially meets, improving"
    1: "Below - Does not meet, action needed"

  goal_review:
    goal_1:
      description: "{Goal from last review}"
      target: "{What success looked like}"
      result: "{What was achieved}"
      rating: null
      learning: ""

    goal_2:
      description: ""
      target: ""
      result: ""
      rating: null

  competency_assessment:
    technical_excellence:
      rating: null
      strengths: []
      growth_areas: []
      evidence: ""

    collaboration:
      rating: null
      strengths: []
      growth_areas: []
      evidence: ""

    communication:
      rating: null
      strengths: []
      growth_areas: []
      evidence: ""

    ownership:
      rating: null
      strengths: []
      growth_areas: []
      evidence: ""

    impact:
      rating: null
      strengths: []
      growth_areas: []
      evidence: ""

  peer_feedback_summary:
    themes: []
    quotes: []

  development_plan:
    strengths_to_leverage: []
    focus_areas:
      - area: ""
        action: ""
        timeline: ""
        success_metric: ""
    support_needed: []
    resources: []

  next_period_goals:
    goal_1:
      description: ""
      success_criteria: ""
      alignment: ""

  career_discussion:
    aspirations: ""
    timeline_to_next_level: ""
    gaps_to_address: []
```

### Continuous Feedback (SBI Model)

```yaml
sbi_feedback:
  model:
    situation: "In {specific context/meeting/moment}..."
    behavior: "I observed/noticed {specific observable behavior}..."
    impact: "The impact was {effect on team/project/individual}..."

  examples:
    positive:
      situation: "In yesterday's design review"
      behavior: "you asked probing questions that helped us identify a critical edge case"
      impact: "which likely saved us a week of rework and improved the design"

    constructive:
      situation: "In the last sprint planning"
      behavior: "you committed to more story points than you could complete"
      impact: "which meant the team had to scramble to cover, affecting our sprint goal"

  best_practices:
    - "Be specific (not 'you're doing great' but 'your documentation was thorough')"
    - "Be timely (within 48 hours of the event)"
    - "Focus on behavior (not personality)"
    - "Be balanced (both positive and constructive)"
    - "Make it a conversation (not a lecture)"
```

### Performance Improvement Plan (PIP)

```yaml
performance_improvement_plan:
  metadata:
    employee: "{Name}"
    manager: "{Name}"
    hr_partner: "{Name}"
    start_date: "{Date}"
    end_date: "{Date}"
    duration: "{30/60/90 days}"

  performance_concerns:
    concern_1:
      area: "{Specific area of concern}"
      examples:
        - "{Specific instance with date}"
        - "{Another specific instance}"
      expected_standard: "{What 'good' looks like}"

    concern_2:
      area: ""
      examples: []
      expected_standard: ""

  improvement_goals:
    goal_1:
      description: "{Specific, measurable improvement}"
      success_criteria: "{How we'll know it's achieved}"
      timeline: "{When by}"
      support_provided: "{Training, mentoring, etc.}"

    goal_2:
      description: ""
      success_criteria: ""
      timeline: ""
      support_provided: ""

  check_in_schedule:
    - date: "{Week 1}"
      focus: "{Initial check-in}"
    - date: "{Week 2}"
      focus: "{Progress review}"
    - date: "{Midpoint}"
      focus: "{Formal midpoint review}"
    - date: "{Final}"
      focus: "{Final evaluation}"

  outcomes:
    successful: "Return to good standing, continue employment"
    unsuccessful: "Separation from company"

  acknowledgement:
    employee_signature: ""
    manager_signature: ""
    date: ""
```

---

## Decision Trees

### Rating Calibration

```
Individual assessment complete
|
+-- Compare to level expectations
|   +-- Exceeds level consistently? -> Consider 4 or 5
|   +-- Meets level consistently? -> 3
|   +-- Below level? -> 2 or below
|
+-- Compare to peers at same level
|   +-- Top quartile? -> Lean toward 4+
|   +-- Middle half? -> Likely 3
|   +-- Bottom quartile? -> Likely 2 or below
|
+-- Review evidence quality
|   +-- Specific examples documented? -> Trust rating
|   +-- Vague or missing? -> Reconsider, gather more
|
+-- Final calibration with peers
    +-- Adjust for consistency across org
```

### When to Start PIP

```
Performance concern identified
|
+-- Is this a new issue?
|   +-- Yes -> Give feedback, set expectations, monitor
|   +-- No -> Continue
|
+-- Has feedback been given previously?
|   +-- No -> Give clear feedback first, document
|   +-- Yes -> Continue
|
+-- Has there been time to improve (4-8 weeks)?
|   +-- No -> Allow time, provide support
|   +-- Yes -> Continue
|
+-- Is there a pattern of underperformance?
|   +-- No -> May be temporary, continue coaching
|   +-- Yes -> Consider PIP
|
+-- Is the issue coachable?
    +-- Yes -> Start PIP with clear goals
    +-- No -> May need immediate action (HR consult)
```

---

## Anti-Patterns

```yaml
anti_patterns:
  recency_bias:
    symptom: "Only remembering last month of performance"
    remedy:
      - "Keep running notes throughout period"
      - "Review goals quarterly"
      - "Collect feedback continuously"

  rating_inflation:
    symptom: "Everyone is 'exceeds expectations'"
    remedy:
      - "Calibration sessions"
      - "Distribution guidelines"
      - "Manager training"

  surprise_reviews:
    symptom: "First time hearing about issues at review"
    remedy:
      - "Continuous feedback culture"
      - "Monthly check-ins on goals"
      - "No surprises rule"

  personality_focus:
    symptom: "Rating the person, not the work"
    remedy:
      - "Evidence-based reviews"
      - "Specific examples required"
      - "Behavior focus"
```

---

## Quick Reference Cards

### Goal-Setting (SMART)

```
S - Specific: Clear and well-defined
M - Measurable: Quantifiable outcomes
A - Achievable: Realistic but challenging
R - Relevant: Aligned with team/company goals
T - Time-bound: Clear deadline

Example:
Bad: "Improve code quality"
Good: "Reduce production incidents by 30% in Q2
       by implementing automated testing for
       critical paths, measured by PagerDuty data"
```

### Feedback Frequency

| Type | Cadence | Format |
|------|---------|--------|
| Quick praise | Daily | Slack/in-person |
| Constructive | Within 48h of event | Private 1-on-1 |
| Goal progress | Weekly in 1-on-1 | Documented |
| Formal review | Semi-annual | Written + meeting |

### Distribution Guidelines

| Rating | Target % | Description |
|--------|----------|-------------|
| 5 | ~5% | Exceptional, role model |
| 4 | ~20% | Exceeds consistently |
| 3 | ~50% | Meets expectations fully |
| 2 | ~20% | Developing, improving |
| 1 | ~5% | Below, needs action |

---

## Troubleshooting

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Goals not achieved | Unclear or unrealistic | Use SMART, check in weekly |
| Surprises at review | No ongoing feedback | Continuous feedback culture |
| Rating disagreements | Different standards | Calibration sessions |
| PIP fails | Wrong fit, not coachable | Better hiring, earlier intervention |

---

## Validation Rules

```yaml
input_validation:
  review_type:
    type: enum
    values: [annual, mid_year, quarterly, pip]
    required: true

  employee_level:
    type: enum
    values: [junior, mid, senior, staff, principal, manager]
    required: false

  timeline:
    type: enum
    values: [30_day, 60_day, 90_day]
    required: false
```

---

## Resources

**Books**:
- Measure What Matters - John Doerr
- Radical Candor - Kim Scott
- High Output Management - Andy Grove
- The Effective Manager - Mark Horstman

**Frameworks**:
- OKR methodology (Google, Intel)
- SMART goals
- SBI feedback model
