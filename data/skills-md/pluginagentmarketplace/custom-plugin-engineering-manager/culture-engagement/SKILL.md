---
name: culture-engagement
version: "2.0.0"
description: Master team culture, psychological safety, engagement, communication, and inclusion for engineering teams
sasmp_version: "1.3.0"
bonded_agent: 04-culture-engagement-agent
bond_type: PRIMARY_BOND
category: culture
input_validation:
  required_context: ["situation"]
  optional_context: ["team_size", "remote_percentage"]
retry_config:
  max_attempts: 2
  backoff: exponential
observability:
  log_level: info
  metrics: [invocation_count, success_rate, latency]
---

# Culture & Engagement Skill

## Purpose
Provide engineering managers with frameworks for building healthy team cultures, fostering psychological safety, driving engagement, and creating inclusive environments.

## Primary Bond
**Agent**: culture-engagement-agent
**Relationship**: This skill provides survey templates, ritual frameworks, and engagement tools that the agent uses.

---

## Templates

### Psychological Safety Pulse

```yaml
psychological_safety_pulse:
  metadata:
    team: "{Team name}"
    date: "{Date}"
    participants: "{X/Y responded}"
    response_rate: "{X}%"

  dimensions:
    inclusion_safety:
      questions:
        - "I feel like I belong on this team"
        - "My unique perspective is valued"
        - "I can be myself at work"
      average_score: null
      trend: null

    learner_safety:
      questions:
        - "It's safe to ask questions, even obvious ones"
        - "Mistakes are treated as learning opportunities"
        - "I can admit when I don't know something"
      average_score: null
      trend: null

    contributor_safety:
      questions:
        - "My contributions make a real difference"
        - "I can use my skills effectively"
        - "My work is valued by the team"
      average_score: null
      trend: null

    challenger_safety:
      questions:
        - "I can challenge ideas without negative consequences"
        - "Speaking up is encouraged, even with bad news"
        - "Disagreement is handled constructively"
      average_score: null
      trend: null

  interpretation:
    4.5_plus: "Excellent - maintain and reinforce"
    4.0_to_4.4: "Good - minor improvements needed"
    3.5_to_3.9: "Concerning - targeted intervention"
    below_3.5: "Critical - immediate action needed"

  action_planning:
    top_strength: ""
    top_concern: ""
    committed_actions: []
    follow_up_date: ""
```

### Engagement Survey

```yaml
engagement_survey:
  metadata:
    team: "{Team name}"
    quarter: "{Q1 2025}"
    response_rate: "{X}%"

  categories:
    basic_needs:
      - "I know what's expected of me"
      - "I have the tools and resources to do my work"

    individual:
      - "I can do what I do best every day"
      - "I receive recognition for good work"
      - "Someone at work cares about me as a person"
      - "Someone encourages my development"

    team:
      - "My opinions seem to count"
      - "The mission makes my work feel important"
      - "My co-workers are committed to quality"
      - "I have a best friend at work"

    growth:
      - "I've had conversations about my progress"
      - "I have opportunities to learn and grow"

  eNPS:
    question: "How likely are you to recommend this team as a place to work?"
    scale: "0-10"
    calculation: "Promoters (9-10) - Detractors (0-6)"
    target: ">40"

  interpretation:
    engagement_score:
      excellent: ">4.5"
      good: "4.0-4.4"
      needs_attention: "3.5-3.9"
      critical: "<3.5"

    eNPS:
      excellent: ">50"
      good: "30-50"
      needs_attention: "0-30"
      critical: "<0"
```

### Team Culture Canvas

```yaml
team_culture_canvas:
  values:
    - name: "{Value 1 - e.g., Ownership}"
      definition: "{What it means to us}"
      behaviors:
        do:
          - "{Observable behavior we encourage}"
          - "{Another behavior}"
        dont:
          - "{Behavior that violates this value}"

    - name: "{Value 2 - e.g., Transparency}"
      definition: ""
      behaviors:
        do: []
        dont: []

  norms:
    communication:
      - "Default to async, sync when needed"
      - "Respond within 4 hours during work hours"
      - "Use public channels unless confidential"

    meetings:
      - "Agenda required for all meetings"
      - "Start and end on time"
      - "Notes shared within 24 hours"
      - "Camera on for video calls (optional for listeners)"

    feedback:
      - "Direct and kind"
      - "Timely (within 48 hours)"
      - "In private for constructive"
      - "In public for praise"

    work_life:
      - "No messages after 6pm local time"
      - "Vacation is vacation"
      - "Core hours: 10am-4pm local"

  rituals:
    daily:
      - name: "Standup"
        time: "{Time}"
        format: "{Async/Sync}"
        purpose: "Alignment and blockers"

    weekly:
      - name: "Team sync"
        time: "{Day/Time}"
        duration: "30 min"
        purpose: "Strategic alignment"

      - name: "Social time"
        time: "{Day/Time}"
        duration: "30 min"
        purpose: "Connection"

    monthly:
      - name: "All-hands"
        purpose: "Company updates"

      - name: "Recognition"
        purpose: "Celebrate wins"

    quarterly:
      - name: "Retrospective"
        purpose: "Continuous improvement"

      - name: "Planning"
        purpose: "Align on goals"
```

### Stay Interview Guide

```yaml
stay_interview:
  purpose: "Understand what keeps people engaged and identify retention risks"
  frequency: "Quarterly for all, monthly for high-risk"

  questions:
    engagement:
      - "What keeps you here?"
      - "What do you look forward to when you come to work?"
      - "When was the last time you thought about leaving?"

    concerns:
      - "What might tempt you to leave?"
      - "What frustrates you most about working here?"
      - "What would you change if you could?"

    value:
      - "Do you feel valued? Why or why not?"
      - "Is your work recognized appropriately?"
      - "Do you feel you're paid fairly?"

    growth:
      - "Do you see a future for yourself here?"
      - "What skills would you like to develop?"
      - "Is your career progressing as you'd like?"

    manager:
      - "How can I better support you?"
      - "Is there feedback you haven't shared?"
      - "What do you need from me?"

  action_planning:
    immediate_actions: []
    longer_term_changes: []
    follow_up_date: ""
    commitment_made: ""
```

---

## Decision Trees

### Psychological Safety Intervention

```
Safety score below 4.0
|
+-- Which dimension is lowest?
|   |
|   +-- Inclusion Safety
|   |   +-- New team members struggling?
|   |   +-- Cliques forming?
|   |   +-- Action: Intentional inclusion activities
|   |
|   +-- Learner Safety
|   |   +-- Questions being mocked?
|   |   +-- Mistakes punished?
|   |   +-- Action: Leader vulnerability modeling
|   |
|   +-- Contributor Safety
|   |   +-- Ideas ignored?
|   |   +-- Credit not given?
|   |   +-- Action: Recognition program
|   |
|   +-- Challenger Safety
|       +-- Bad news hidden?
|       +-- Dissent suppressed?
|       +-- Action: Explicitly invite challenge
|
+-- Is there a specific incident?
|   +-- Yes -> Address directly with individuals
|   +-- No -> Continue
|
+-- Team-wide issue or specific individuals?
    +-- Team-wide -> Team retrospective, new norms
    +-- Specific -> 1-on-1 coaching, potential consequences
```

### Retention Risk Response

```
Retention risk identified
|
+-- Risk level?
|   +-- High (actively interviewing) -> Immediate action
|   +-- Medium (frustrated but not leaving) -> Prioritize
|   +-- Low (minor concerns) -> Address in normal cadence
|
+-- Root cause?
|   +-- Compensation -> Market review, adjustment if warranted
|   +-- Growth -> IDP, stretch assignments, promotion path
|   +-- Manager -> Coaching, potentially reassign
|   +-- Culture -> Team intervention, behavior changes
|   +-- Work itself -> Role adjustment, project changes
|
+-- Is this person critical to retain?
|   +-- Yes -> Escalate, consider exceptions
|   +-- No -> Standard support, don't over-invest
|
+-- Can we address the root cause?
    +-- Yes -> Create action plan, timeline
    +-- No -> Be honest, help them succeed elsewhere
```

---

## Anti-Patterns

```yaml
anti_patterns:
  culture_theater:
    symptom: "Values on the wall but not in actions"
    remedy:
      - "Define observable behaviors for each value"
      - "Call out violations (kindly but firmly)"
      - "Celebrate values in action"

  survey_fatigue:
    symptom: "Low response rates, cynicism about surveys"
    remedy:
      - "Reduce frequency, increase impact"
      - "Share results and actions publicly"
      - "Close the loop on previous feedback"

  brilliant_jerk:
    symptom: "High performer with toxic behavior tolerated"
    remedy:
      - "Behavior is a performance dimension"
      - "Address immediately, no exceptions"
      - "Impact on team is measurable"

  forced_fun:
    symptom: "Mandatory team building that people dread"
    remedy:
      - "Make social activities optional"
      - "Offer variety (not everyone likes happy hours)"
      - "Focus on genuine connection"
```

---

## Quick Reference Cards

### Recognition Best Practices

```yaml
recognition:
  public:
    format: "I want to recognize {name} for {specific action}.
             This demonstrated our value of {value}
             and resulted in {impact}."
    when: "Weekly in team channel or meeting"

  private:
    format: "I noticed you {specific action}.
             This showed great {skill/value}
             and made a real difference in {outcome}."
    when: "As it happens, within 48 hours"

  peer:
    format: "Shoutout to {name} for helping me with {task}.
             Really appreciated your {specific contribution}."
    when: "Encourage regularly, model it yourself"

  guidelines:
    - "Be specific (not just 'great job')"
    - "Be timely (within 48 hours)"
    - "Tie to values when possible"
    - "Balance public and private"
    - "Recognize effort, not just outcomes"
```

### Meeting Inclusion Checklist

```yaml
meeting_inclusion:
  before:
    - "Is everyone who should be there invited?"
    - "Is the time zone fair for all participants?"
    - "Is the agenda shared in advance?"

  during:
    - "Are all voices heard (not just the loudest)?"
    - "Are there multiple ways to participate (verbal, chat)?"
    - "Are we avoiding side conversations?"
    - "Are we crediting ideas to originators?"

  after:
    - "Are notes shared with all stakeholders?"
    - "Are action items clear and assigned?"
    - "Is there a way to give feedback on the meeting?"
```

### Remote/Hybrid Best Practices

```yaml
remote_practices:
  connection:
    - "Camera on as default (but respect opt-out)"
    - "Virtual coffee chats scheduled"
    - "Team rituals adapted for remote"

  communication:
    - "Over-communicate (2x what feels necessary)"
    - "Write things down (tribal knowledge shared)"
    - "Async-first, sync when needed"

  inclusion:
    - "Same experience for remote and in-office"
    - "No hallway decisions (document everything)"
    - "Time zone rotation for recurring meetings"
```

---

## Troubleshooting

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Silent meetings | Low psychological safety | Invite input explicitly, wait for answers |
| Survey scores low | Real problems or survey fatigue | Act on feedback, show progress |
| High turnover | Multiple possible causes | Exit interviews, stay conversations |
| Cliques forming | Natural but needs management | Mix up teams, cross-functional projects |

---

## Validation Rules

```yaml
input_validation:
  situation:
    type: string
    min_length: 10
    required: true

  team_size:
    type: integer
    min: 1
    max: 100
    required: false

  remote_percentage:
    type: integer
    min: 0
    max: 100
    required: false
```

---

## Resources

**Books**:
- The Fearless Organization - Amy Edmondson
- Culture Code - Daniel Coyle
- Radical Candor - Kim Scott
- No Rules Rules - Reed Hastings

**Research**:
- Google's Project Aristotle
- Gallup Q12 engagement research
- Amy Edmondson's psychological safety research
