---
name: team-dynamics
version: "2.0.0"
description: Master team dynamics, leadership principles, delegation, 1-on-1s, mentoring, and people management for engineering managers
sasmp_version: "1.3.0"
bonded_agent: 01-team-leadership-agent
bond_type: PRIMARY_BOND
category: people-management
input_validation:
  required_context: ["team_size", "situation"]
  optional_context: ["urgency", "history"]
retry_config:
  max_attempts: 2
  backoff: exponential
observability:
  log_level: info
  metrics: [invocation_count, success_rate, latency]
---

# Team Dynamics & Leadership Skill

## Purpose
Provide engineering managers with actionable frameworks, templates, and guidance for building high-performing teams, running effective 1-on-1s, delegating effectively, and developing psychological safety.

## Primary Bond
**Agent**: team-leadership-agent
**Relationship**: This skill provides the foundational templates and frameworks that the team-leadership-agent uses to guide managers.

---

## Templates

### 1-on-1 Meeting Template

```yaml
one_on_one_meeting:
  duration: "30-60 min"
  frequency: "Weekly recommended"

  structure:
    opening:
      duration: "5 min"
      focus:
        - "Personal check-in"
        - "Energy/mood assessment"
        - "Their agenda items"

    their_agenda:
      duration: "15-20 min"
      questions:
        - "What's on your mind?"
        - "What's blocking you?"
        - "What wins to celebrate?"
        - "What do you need from me?"

    development:
      duration: "10 min"
      topics:
        - "Progress on goals"
        - "Skill development"
        - "Career conversation"

    feedback:
      duration: "5-10 min"
      bidirectional:
        - "Manager to report"
        - "Report to manager"

    closing:
      duration: "5 min"
      outputs:
        - "Action items documented"
        - "Next meeting focus"
        - "Support committed"
```

### Delegation Framework (RACI)

```yaml
delegation_levels:
  L1_direct:
    authority: "Full decision authority"
    support: "Available on request"
    check_in: "Weekly"
    use_when: "Experienced, proven track record"

  L2_coach:
    authority: "Decision authority with input"
    support: "Proactive guidance"
    check_in: "Bi-weekly"
    use_when: "Growing, needs development"

  L3_supervise:
    authority: "Recommendation only"
    support: "Active supervision"
    check_in: "Daily"
    use_when: "New to task, learning"

  L4_control:
    authority: "Execution only"
    support: "Continuous oversight"
    check_in: "Real-time"
    use_when: "Critical task, new team member"

delegation_handoff_checklist:
  - "Define outcome clearly (what done looks like)"
  - "Explain context and why"
  - "Clarify authority level (L1-L4)"
  - "Set check-in schedule"
  - "Confirm understanding"
  - "Document decision rights"
```

### Team Health Assessment

```yaml
team_health_pulse:
  dimensions:
    psychological_safety:
      questions:
        - "I can speak up without fear"
        - "Mistakes are learning opportunities"
        - "I can ask 'dumb' questions"
      scale: "1-5"
      target: ">4.0"

    clarity:
      questions:
        - "I know what's expected of me"
        - "Team goals are clear"
        - "My role is well-defined"
      scale: "1-5"
      target: ">4.0"

    collaboration:
      questions:
        - "Team members help each other"
        - "Information flows freely"
        - "Conflicts are resolved constructively"
      scale: "1-5"
      target: ">4.0"

    engagement:
      questions:
        - "I feel valued"
        - "My work is meaningful"
        - "I have growth opportunities"
      scale: "1-5"
      target: ">4.0"

  interpretation:
    excellent: ">4.5"
    good: "4.0-4.4"
    concerning: "3.5-3.9"
    critical: "<3.5"

  cadence: "Monthly pulse, Quarterly deep-dive"
```

### Conflict Resolution Protocol

```yaml
conflict_resolution:
  step_1_assess:
    - "Identify conflict type (interpersonal vs task)"
    - "Determine urgency and impact"
    - "Gather facts (not opinions)"

  step_2_individual:
    - "Meet with each party separately"
    - "Listen without judgment"
    - "Understand interests (not positions)"
    - "Document key points"

  step_3_joint:
    - "Facilitate joint session"
    - "Establish ground rules"
    - "Focus on interests, not positions"
    - "Generate options together"

  step_4_resolve:
    - "Agree on solution"
    - "Document commitments"
    - "Set follow-up date"
    - "Communicate to team if needed"

  escalation_triggers:
    - "No progress after 2 joint sessions"
    - "Policy or legal concerns"
    - "Harassment or discrimination"
    - "Safety concerns"
```

---

## Decision Trees

### When to Delegate

```
Task arrives
|
+-- Is this strategic/confidential?
|   +-- Yes -> Keep it
|   +-- No -> Continue
|
+-- Does someone else have better skills?
|   +-- Yes -> Delegate to them
|   +-- No -> Continue
|
+-- Is this a growth opportunity?
|   +-- Yes -> Delegate with L2/L3 support
|   +-- No -> Continue
|
+-- Do I have capacity?
    +-- Yes -> Consider keeping, but still evaluate delegation
    +-- No -> Must delegate, find right person
```

### 1-on-1 Frequency Decision

```
Team Member Situation
|
+-- New to role (<3 months)
|   +-- Weekly, 45-60 min
|
+-- Struggling or PIP
|   +-- Weekly or bi-weekly, 45 min
|
+-- Solid performer
|   +-- Bi-weekly, 30 min
|
+-- High performer, autonomous
    +-- Bi-weekly or monthly, 30 min
    +-- But always available on request
```

---

## Anti-Patterns

```yaml
anti_patterns:
  micromanagement:
    symptoms:
      - "Checking in multiple times daily"
      - "Redoing delegated work"
      - "Requiring approval for small decisions"
    remedy:
      - "Focus on outcomes, not tasks"
      - "Set clear success criteria upfront"
      - "Trust and verify, don't hover"

  absentee_manager:
    symptoms:
      - "Skipping 1-on-1s regularly"
      - "Not knowing team's blockers"
      - "Surprised by performance issues"
    remedy:
      - "Protect 1-on-1 time as sacred"
      - "Weekly team check-ins"
      - "Daily async standups"

  conflict_avoidance:
    symptoms:
      - "Letting issues fester"
      - "Not giving tough feedback"
      - "Hoping problems resolve themselves"
    remedy:
      - "Address within 48 hours"
      - "Use SBI feedback model"
      - "Document and follow up"
```

---

## Quick Reference Cards

### SBI Feedback Model
```
Situation: "In yesterday's standup..."
Behavior: "When you interrupted Sarah..."
Impact: "It made her hesitant to share ideas..."
```

### GROW Coaching Model
```
Goal: "What do you want to achieve?"
Reality: "Where are you now?"
Options: "What could you do?"
Will: "What will you do?"
```

### Tuckman's Stages
```
Forming -> Storming -> Norming -> Performing -> Adjourning
   |          |           |           |            |
 Polite    Conflict    Standards   High-perf   Transition
```

---

## Troubleshooting

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| 1-on-1s feel awkward | No agenda, manager talks too much | Use template, listen 80% |
| Delegation fails | Unclear expectations | Use handoff checklist |
| Team silent in meetings | Low psychological safety | Leader vulnerability, invite input |
| Constant escalations | Over-delegation to wrong level | Match task to L1-L4 level |

---

## Validation Rules

```yaml
input_validation:
  team_size:
    type: integer
    min: 1
    max: 50
    required: false

  situation:
    type: string
    min_length: 10
    required: true

  urgency:
    type: enum
    values: [low, medium, high, critical]
    default: medium
```

---

## Resources

**Books**:
- The Manager's Path - Camille Fournier
- Radical Candor - Kim Scott
- Turn the Ship Around - David Marquet
- High Output Management - Andy Grove

**Research**:
- Google's Project Aristotle (psychological safety)
- Gallup Q12 engagement research
