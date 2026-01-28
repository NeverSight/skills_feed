---
name: hiring-recruitment
version: "2.0.0"
description: Master hiring processes, interviewing, candidate assessment, and building strong engineering teams
sasmp_version: "1.3.0"
bonded_agent: 03-hiring-performance-agent
bond_type: PRIMARY_BOND
category: talent-acquisition
input_validation:
  required_context: ["role_level"]
  optional_context: ["urgency", "team_context"]
retry_config:
  max_attempts: 2
  backoff: exponential
observability:
  log_level: info
  metrics: [invocation_count, success_rate, latency]
---

# Hiring & Recruitment Skill

## Purpose
Provide engineering managers with comprehensive hiring frameworks, interview templates, and assessment tools for building strong engineering teams.

## Primary Bond
**Agent**: hiring-performance-agent
**Relationship**: This skill provides the hiring templates, scorecards, and evaluation frameworks that the agent uses.

---

## Templates

### Job Description Template

```markdown
# {Role Title} - {Team}

## About the Role
{2-3 sentences on impact and scope - what will they accomplish?}

## What You'll Do
- {Responsibility 1 - outcome focused, not task focused}
- {Responsibility 2 - include collaboration aspects}
- {Responsibility 3 - include growth opportunities}
- {Responsibility 4 - include impact on users/business}

## What We're Looking For

### Must Have
- {Years of experience or equivalent demonstrated ability}
- {Core technical skill 1}
- {Core technical skill 2}
- {Key soft skill}

### Nice to Have
- {Bonus technical skill}
- {Domain experience}
- {Leadership experience}

## Our Interview Process
1. **Recruiter Screen** (30 min) - Background and mutual fit
2. **Technical Screen** (60 min) - Coding and problem-solving
3. **System Design** (60 min) - Architecture thinking
4. **Team Fit** (45 min) - Collaboration and values
5. **Hiring Manager** (45 min) - Final discussion

Expected timeline: 2-3 weeks

## What We Offer
- {Compensation range if public}
- {Key benefits}
- {Growth opportunities}
- {Culture highlights}
```

### Interview Scorecard

```yaml
interview_scorecard:
  candidate: "{Name}"
  role: "{Role}"
  interviewer: "{Name}"
  date: "{Date}"
  interview_type: "{Technical | Design | Behavioral | Final}"

  competencies:
    technical_skills:
      weight: 30%
      score: null  # 1-5
      evidence: ""
      strong_signals: []
      concerns: []

    problem_solving:
      weight: 25%
      score: null
      evidence: ""
      strong_signals: []
      concerns: []

    communication:
      weight: 15%
      score: null
      evidence: ""
      strong_signals: []
      concerns: []

    collaboration:
      weight: 15%
      score: null
      evidence: ""
      strong_signals: []
      concerns: []

    growth_mindset:
      weight: 15%
      score: null
      evidence: ""
      strong_signals: []
      concerns: []

  overall:
    weighted_score: null
    recommendation: null  # Strong Hire | Hire | No Hire | Strong No Hire
    summary: ""
    next_steps: ""

  scoring_guide:
    5: "Exceptional - top 5% of candidates seen"
    4: "Strong - clearly above bar"
    3: "Meets bar - solid hire"
    2: "Below bar - significant concerns"
    1: "Far below bar - clear no hire"
```

### Behavioral Interview Guide (STAR)

```yaml
star_framework:
  situation:
    prompt: "Tell me about a time when..."
    look_for:
      - "Specific, real example"
      - "Clear context setting"
      - "Relevant to competency"

  task:
    prompt: "What was your specific responsibility?"
    look_for:
      - "Personal ownership"
      - "Clear scope understanding"
      - "Appropriate level of challenge"

  action:
    prompt: "What steps did you take?"
    look_for:
      - "Specific actions (not 'we' but 'I')"
      - "Logical approach"
      - "Problem-solving demonstrated"

  result:
    prompt: "What was the outcome? What did you learn?"
    look_for:
      - "Measurable impact"
      - "Self-reflection"
      - "Learning demonstrated"

sample_questions:
  problem_solving:
    - "Tell me about a time you solved a problem with incomplete information"
    - "Describe a situation where you had to make a difficult trade-off"
    - "Tell me about a technical decision you later regretted"

  collaboration:
    - "Tell me about a time you had a conflict with a teammate"
    - "Describe a situation where you had to influence without authority"
    - "Tell me about receiving critical feedback"

  leadership:
    - "Tell me about a time you mentored someone"
    - "Describe a situation where you drove a significant change"
    - "Tell me about a time you had to make an unpopular decision"
```

### Hiring Pipeline Metrics

```yaml
hiring_metrics:
  funnel_metrics:
    applications_to_screen: "{X}%"
    screen_to_interview: "{X}%"
    interview_to_offer: "{X}%"
    offer_to_accept: "{X}%"

  time_metrics:
    time_to_first_response: "{X} days"
    time_to_offer: "{X} days"
    time_to_hire: "{X} days"

  quality_metrics:
    new_hire_90_day_retention: "{X}%"
    new_hire_performance_rating: "{X}/5"
    hiring_manager_satisfaction: "{X}/5"

  targets:
    time_to_hire: "<45 days"
    offer_acceptance: ">80%"
    90_day_retention: ">95%"
    diversity_pipeline: ">40%"

  red_flags:
    time_to_hire: ">60 days"
    offer_acceptance: "<60%"
    90_day_retention: "<85%"
```

---

## Decision Trees

### Hire / No-Hire Decision

```
Scorecard Complete
|
+-- Any Strong No Hire?
|   +-- Yes -> No Hire (single strong no is veto)
|   +-- No -> Continue
|
+-- Weighted score >= 3.0?
|   +-- No -> No Hire
|   +-- Yes -> Continue
|
+-- Any critical competency < 3?
|   +-- Yes -> Discuss in debrief, likely No Hire
|   +-- No -> Continue
|
+-- All interviewers Hire or Strong Hire?
|   +-- Yes -> Make offer
|   +-- No -> Debrief discussion, address concerns
```

### Offer Negotiation

```
Candidate requests higher comp
|
+-- Within approved range?
|   +-- Yes -> Can approve, consider value
|   +-- No -> Continue
|
+-- Top candidate for role?
|   +-- Yes -> Escalate for exception
|   +-- No -> Continue
|
+-- Can we offer other value?
|   +-- Yes -> Negotiate (signing bonus, equity, title, start date)
|   +-- No -> Explain our position, give time to decide
```

---

## Anti-Patterns

```yaml
anti_patterns:
  culture_fit_trap:
    symptom: "Hiring people just like us"
    remedy:
      - "Define 'culture add' not 'culture fit'"
      - "Diverse interview panels"
      - "Structured evaluation criteria"

  halo_effect:
    symptom: "One great answer overshadows all else"
    remedy:
      - "Structured scorecards for each competency"
      - "Multiple interviewers for same competency"
      - "Calibration before debrief"

  urgency_hire:
    symptom: "We need someone NOW"
    remedy:
      - "Bad hire costs more than waiting"
      - "Consider contractors for immediate needs"
      - "Never lower the bar"

  confirmation_bias:
    symptom: "Looking for evidence to confirm first impression"
    remedy:
      - "Document evidence before scoring"
      - "Score independently before debrief"
      - "Assign devil's advocate in debrief"
```

---

## Quick Reference Cards

### Interview Debrief Structure

```
1. Scores submitted independently (before meeting)
2. Go around - each interviewer shares (2 min each)
   - Overall recommendation
   - Key evidence (specific examples)
   - Top concern
3. Discussion of disagreements
4. Hiring manager makes final call
5. Document decision and reasoning
```

### Red Flags to Watch

```yaml
red_flags:
  technical:
    - "Cannot explain their own code"
    - "No questions about the codebase"
    - "Blames others for past failures"

  behavioral:
    - "Uses 'we' exclusively (no personal ownership)"
    - "No examples of learning from mistakes"
    - "Dismissive of questions"

  cultural:
    - "Badmouths previous employers"
    - "No interest in team dynamics"
    - "Unwilling to receive feedback"
```

### Candidate Experience Checklist

```yaml
candidate_experience:
  before:
    - "Clear job description"
    - "Fast initial response (<48h)"
    - "Interview prep materials sent"

  during:
    - "Interviewers prepared and on time"
    - "Candidate can ask questions"
    - "Respectful, welcoming atmosphere"

  after:
    - "Timeline communicated"
    - "Feedback provided (if rejected)"
    - "Offer delivered promptly"
```

---

## Troubleshooting

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Not enough candidates | Poor JD, wrong channels | Revise JD, expand sourcing |
| High drop-off after screen | Process too slow, poor experience | Speed up, improve communication |
| Offers declined | Comp, culture, opportunity | Exit survey, adjust offer |
| Bad hires | Weak interview process | Structured interviews, calibration |

---

## Validation Rules

```yaml
input_validation:
  role_level:
    type: enum
    values: [junior, mid, senior, staff, principal, manager, director]
    required: true

  urgency:
    type: enum
    values: [low, medium, high, critical]
    default: medium

  team_context:
    type: object
    properties:
      size: { type: integer }
      current_gaps: { type: array }
    required: false
```

---

## Resources

**Books**:
- Who: The A Method for Hiring - Geoff Smart
- The Effective Hiring Manager - Mark Horstman
- Work Rules! - Laszlo Bock

**Tools**:
- Structured interview training
- Unconscious bias training
- Calibration session templates
