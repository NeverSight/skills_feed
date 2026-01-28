---
name: technical-decision-making
version: "2.0.0"
description: Master technical decision-making, architecture choices, technology evaluation, and technical roadmaps for engineering teams
sasmp_version: "1.3.0"
bonded_agent: 02-technical-strategy-agent
bond_type: PRIMARY_BOND
category: technical-leadership
input_validation:
  required_context: ["decision_context"]
  optional_context: ["constraints", "current_stack", "timeline"]
retry_config:
  max_attempts: 2
  backoff: exponential
observability:
  log_level: info
  metrics: [invocation_count, success_rate, latency]
---

# Technical Decision Making Skill

## Purpose
Provide engineering managers with structured frameworks for making sound technical decisions, evaluating technologies, managing technical debt, and developing technical roadmaps.

## Primary Bond
**Agent**: technical-strategy-agent
**Relationship**: This skill provides ADR templates, evaluation frameworks, and decision tools that the technical-strategy-agent uses.

---

## Templates

### Architecture Decision Record (ADR)

```markdown
# ADR-{NUMBER}: {TITLE}

## Status
{Proposed | Accepted | Deprecated | Superseded by ADR-XXX}

## Date
{YYYY-MM-DD}

## Context
{What is the issue that we're seeing that is motivating this decision?}

## Decision Drivers
- {driver 1}
- {driver 2}

## Considered Options
1. {Option 1}
2. {Option 2}
3. {Option 3}

## Decision Outcome
Chosen option: "{option X}", because {justification}.

### Positive Consequences
- {consequence 1}

### Negative Consequences
- {consequence 1}

## Pros and Cons of Options

### Option 1: {name}
| Aspect | Assessment |
|--------|------------|
| Effort | {Low/Medium/High} |
| Risk | {Low/Medium/High} |
| Team Fit | {score}/5 |
| Reversibility | {Easy/Hard} |

Good, because {argument}.
Bad, because {argument}.

## Links
- {Link to related ADR}
- {Link to documentation}
```

### Technology Evaluation Matrix

```yaml
technology_evaluation:
  template:
    candidate: "{Technology name}"
    evaluation_date: "{Date}"
    evaluator: "{Name}"

  criteria:
    technical_fit:
      weight: 25%
      factors:
        - scalability_match: "1-5"
        - performance_requirements: "1-5"
        - security_compliance: "1-5"
      score: null

    team_readiness:
      weight: 20%
      factors:
        - current_expertise: "1-5"
        - learning_curve: "1-5"
        - hiring_market: "1-5"
      score: null

    ecosystem_maturity:
      weight: 20%
      factors:
        - community_size: "1-5"
        - documentation_quality: "1-5"
        - library_availability: "1-5"
      score: null

    operational:
      weight: 20%
      factors:
        - deployment_complexity: "1-5"
        - monitoring_support: "1-5"
        - maintenance_burden: "1-5"
      score: null

    cost:
      weight: 15%
      factors:
        - licensing: "1-5"
        - infrastructure: "1-5"
        - training: "1-5"
      score: null

  interpretation:
    4.5_plus: "Strong candidate - proceed"
    3.5_to_4.4: "Viable - address concerns"
    2.5_to_3.4: "Risky - significant gaps"
    below_2.5: "Not recommended"
```

### Technical Debt Tracker

```yaml
technical_debt_item:
  id: "TD-{NUMBER}"
  title: "{Short description}"
  category: "{architecture | code | infrastructure | testing | documentation}"
  quadrant: "{deliberate_prudent | deliberate_reckless | inadvertent_prudent | inadvertent_reckless}"

  description: "{Detailed description}"
  created_date: "{Date}"
  owner: "{Team/Person}"

  impact:
    development_velocity: "{-X%}"
    reliability_risk: "{low | medium | high}"
    security_risk: "{low | medium | high}"

  effort:
    estimate: "{T-shirt: S/M/L/XL}"
    sprints: "{Number}"
    dependencies: ["{Other work}"]

  interest_rate: "{stable | increasing | decreasing}"

  recommendation:
    action: "{fix | defer | monitor | accept}"
    timeline: "{Q1 2025}"
    justification: "{Why this recommendation}"

  resolution:
    status: "{open | in_progress | resolved | wont_fix}"
    resolved_date: null
    notes: null
```

### Technical Roadmap

```yaml
technical_roadmap:
  year: 2025

  q1:
    theme: "Foundation"
    initiatives:
      - name: "Infrastructure modernization"
        priority: "P0"
        owner: "Platform team"
        dependencies: []
      - name: "Observability stack"
        priority: "P1"
        owner: "SRE"
        dependencies: ["Infrastructure modernization"]

  q2:
    theme: "Scale"
    initiatives:
      - name: "Database sharding"
        priority: "P0"
        owner: "Data team"
        dependencies: ["Infrastructure modernization"]

  q3:
    theme: "Velocity"
    initiatives:
      - name: "CI/CD improvements"
        priority: "P1"
        owner: "DevEx team"

  q4:
    theme: "Innovation"
    initiatives:
      - name: "Event-driven architecture"
        priority: "P2"
        owner: "Architecture team"
```

---

## Decision Trees

### Build vs Buy

```
Need identified
|
+-- Is this core to our business?
|   +-- Yes -> Lean toward Build
|   +-- No -> Continue
|
+-- Does a good solution exist?
|   +-- No -> Must Build
|   +-- Yes -> Continue
|
+-- Can we afford the buy option?
|   +-- No -> Must Build
|   +-- Yes -> Continue
|
+-- Is time-to-market critical?
|   +-- Yes -> Lean toward Buy
|   +-- No -> Continue
|
+-- Do we have the expertise to build?
    +-- Yes -> Evaluate total cost of ownership
    +-- No -> Buy (or hire first)
```

### Architecture Pattern Selection

```
Team size and domain complexity
|
+-- Small team (<5), Simple domain
|   +-- Monolith
|
+-- Small team, Complex domain
|   +-- Modular Monolith
|
+-- Large team (10+), Complex domain
|   +-- Microservices (with caution)
|
+-- Variable load, Event-driven
|   +-- Serverless / Event-driven
|
+-- Strong audit requirements
    +-- Event Sourcing + CQRS
```

---

## Anti-Patterns

```yaml
anti_patterns:
  resume_driven_development:
    symptoms:
      - "Let's use X because it's cool"
      - "This will look great on our blog"
    remedy:
      - "Require business case for any new tech"
      - "Evaluate with scoring matrix"

  golden_hammer:
    symptoms:
      - "We use X for everything"
      - "X worked before, it'll work now"
    remedy:
      - "Match tool to problem domain"
      - "Regular tech radar reviews"

  not_invented_here:
    symptoms:
      - "We'll build our own database"
      - "Open source isn't good enough"
    remedy:
      - "Build vs Buy analysis required"
      - "TCO comparison mandatory"

  analysis_paralysis:
    symptoms:
      - "We've been evaluating for 6 months"
      - "Let's add one more option"
    remedy:
      - "Time-box decisions"
      - "Use decision framework"
      - "Accept 'good enough'"
```

---

## Quick Reference Cards

### Decision Time-Boxing

| Decision Type | Time Box | Reversibility |
|---------------|----------|---------------|
| Tool selection | 1 week | High |
| Framework choice | 2 weeks | Medium |
| Architecture pattern | 1 month | Low |
| Platform migration | 1 quarter | Very Low |

### Tech Debt Quadrant

```
                    Reckless                Prudent
            +---------------------+---------------------+
Deliberate  | "We don't have time | "We must ship now   |
            |  for design"        |  and deal with      |
            |  -> Fix ASAP        |  consequences"      |
            |                     |  -> Plan paydown    |
            +---------------------+---------------------+
Inadvertent | "What's layering?"  | "Now we know how    |
            |  -> Training needed |  we should have     |
            |                     |  done it"           |
            |                     |  -> Refactor next   |
            +---------------------+---------------------+
```

### DORA Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | On-demand | Daily-Weekly | Weekly-Monthly | Monthly+ |
| Lead Time | <1 hour | <1 day | <1 week | 1 month+ |
| Change Failure Rate | <5% | 5-10% | 10-15% | 15%+ |
| Recovery Time | <1 hour | <1 day | <1 week | 1 month+ |

---

## Troubleshooting

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Decisions get reversed | Poor documentation | Use ADR template |
| Tech debt grows unchecked | No visibility | Track with debt template |
| Wrong tech choices | No evaluation process | Use scoring matrix |
| Roadmap not followed | Unclear priorities | P0/P1/P2 classification |

---

## Validation Rules

```yaml
input_validation:
  decision_context:
    type: string
    min_length: 20
    required: true

  constraints:
    type: object
    properties:
      budget: { type: string }
      timeline: { type: string }
      team_expertise: { type: array }
    required: false

  current_stack:
    type: array
    items: { type: string }
    required: false
```

---

## Resources

**Books**:
- Designing Data-Intensive Applications - Martin Kleppmann
- Building Evolutionary Architectures - Ford, Parsons, Kua
- Fundamentals of Software Architecture - Richards, Ford
- The Staff Engineer's Path - Tanya Reilly

**Standards**:
- Architecture Decision Records (ADR) - Michael Nygard
- DORA Metrics - Accelerate research
