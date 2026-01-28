---
name: growth-development
version: "2.0.0"
description: Master career development, engineering ladders, IDPs, succession planning, and mentoring for engineering teams
sasmp_version: "1.3.0"
bonded_agent: 05-growth-development-agent
bond_type: PRIMARY_BOND
category: career-development
input_validation:
  required_context: ["development_goal"]
  optional_context: ["current_level", "target_level", "timeline"]
retry_config:
  max_attempts: 2
  backoff: exponential
observability:
  log_level: info
  metrics: [invocation_count, success_rate, latency]
---

# Growth & Development Skill

## Purpose
Provide engineering managers with comprehensive frameworks for career development, engineering ladders, individual development plans, succession planning, and building mentoring programs.

## Primary Bond
**Agent**: growth-development-agent
**Relationship**: This skill provides career ladder templates, IDP frameworks, and development tools that the agent uses.

---

## Templates

### Engineering Career Ladder

```yaml
engineering_ladder:
  individual_contributor_track:
    L1_junior_engineer:
      scope: "Task"
      experience: "0-2 years"
      expectations:
        - "Completes well-defined tasks with guidance"
        - "Learning codebase and practices"
        - "Asks good questions"
        - "Responds well to feedback"
      technical_skills:
        - "Fundamentals of primary language/framework"
        - "Basic debugging and testing"
        - "Version control basics"
      behaviors:
        - "Eager to learn"
        - "Communicates blockers"
        - "Follows team practices"

    L2_engineer:
      scope: "Feature"
      experience: "2-4 years"
      expectations:
        - "Owns features end-to-end"
        - "Writes production-quality code"
        - "Participates in code reviews"
        - "Mentors juniors informally"
      technical_skills:
        - "Proficient in primary stack"
        - "Understands system architecture"
        - "Writes comprehensive tests"
      behaviors:
        - "Self-directed"
        - "Proactive communication"
        - "Contributes to team discussions"

    L3_senior_engineer:
      scope: "System"
      experience: "4-7 years"
      expectations:
        - "Designs and delivers complex systems"
        - "Influences technical direction"
        - "Mentors multiple engineers"
        - "Improves team practices"
      technical_skills:
        - "Expert in primary domain"
        - "Cross-functional knowledge"
        - "Performance and scaling"
      behaviors:
        - "Technical leadership"
        - "Drives consensus"
        - "Identifies and mitigates risks"

    L4_staff_engineer:
      scope: "Multi-team"
      experience: "7-10 years"
      expectations:
        - "Leads cross-team technical initiatives"
        - "Sets technical strategy"
        - "Builds organizational capability"
        - "Influences beyond immediate team"
      technical_skills:
        - "Architectural expertise"
        - "Technology evaluation"
        - "Technical debt strategy"
      behaviors:
        - "Organizational influence"
        - "Strategic thinking"
        - "Develops other senior engineers"

    L5_principal_engineer:
      scope: "Organization"
      experience: "10+ years"
      expectations:
        - "Shapes company-wide technical direction"
        - "Solves ambiguous, high-impact problems"
        - "Represents company externally"
        - "Creates lasting organizational impact"
      technical_skills:
        - "Industry-recognized expertise"
        - "Innovation leadership"
        - "Technical vision"
      behaviors:
        - "Executive partnership"
        - "Industry influence"
        - "Develops staff engineers"

  management_track:
    M1_engineering_manager:
      scope: "Team (5-8 engineers)"
      experience: "5+ years engineering + management interest"
      expectations:
        - "Hires, develops, retains engineers"
        - "Delivers team commitments"
        - "Creates healthy team culture"
        - "Runs effective processes"
      people_skills:
        - "1-on-1s and feedback"
        - "Performance management"
        - "Hiring and interviewing"
      technical_involvement:
        - "Technical context, not coding"
        - "Architectural input"
        - "Code review occasionally"

    M2_senior_engineering_manager:
      scope: "Large team (8-12) or 2 teams"
      experience: "2+ years as EM"
      expectations:
        - "Manages managers or large team"
        - "Drives significant initiatives"
        - "Develops other managers"
        - "Partners with product leadership"
      people_skills:
        - "Coaching managers"
        - "Organizational design"
        - "Conflict resolution"

    M3_director:
      scope: "Department (20-50 engineers)"
      experience: "4+ years management"
      expectations:
        - "Sets department strategy"
        - "Manages multiple teams"
        - "Executive partnership"
        - "Org-wide influence"
      leadership_skills:
        - "Strategic planning"
        - "Budget management"
        - "Cross-functional leadership"
```

### Individual Development Plan (IDP)

```yaml
individual_development_plan:
  metadata:
    employee: "{Name}"
    current_level: "{Level}"
    target_level: "{Level}"
    manager: "{Manager name}"
    created: "{Date}"
    review_date: "{Date}"

  career_vision:
    long_term: "Where do you want to be in 5 years?"
    medium_term: "What's your 2-year goal?"
    short_term: "What's your focus this year?"

  current_assessment:
    strengths:
      - skill: "{Technical or soft skill}"
        evidence: "{How this shows up in work}"
        leverage_plan: "{How to use this more}"

    growth_areas:
      - skill: "{Skill to develop}"
        current_state: "{Where you are now}"
        target_state: "{Where you need to be}"
        gap: "{What's missing}"

  development_goals:
    goal_1:
      description: "{Specific, measurable goal}"
      category: "{technical | leadership | communication | domain}"
      success_criteria: "{How we'll know it's achieved}"
      timeline: "{By when}"
      actions:
        - action: "{Specific step}"
          deadline: "{Date}"
          resources: "{Training, mentor, project}"
          status: "{not_started | in_progress | completed}"

    goal_2:
      description: ""
      category: ""
      success_criteria: ""
      timeline: ""
      actions: []

    goal_3:
      description: ""
      category: ""
      success_criteria: ""
      timeline: ""
      actions: []

  development_methods:
    learning_mix:
      experience: "70% - stretch assignments, projects"
      exposure: "20% - mentoring, shadowing, networking"
      education: "10% - courses, reading, conferences"

    specific_opportunities:
      stretch_assignments: []
      mentors_sponsors: []
      training_courses: []
      conferences_events: []

  support_needed:
    from_manager:
      - "{Specific support}"
    from_organization:
      - "{Resources, training, opportunities}"
    from_mentors:
      - "{Guidance areas}"

  check_in_schedule:
    frequency: "Monthly"
    next_review: "{Date}"
    progress_notes: []
```

### Succession Planning Framework

```yaml
succession_planning:
  critical_roles:
    - role: "{Role title}"
      current_holder: "{Name}"
      risk_level: "{low | medium | high | critical}"
      risk_factors:
        - "{Single point of knowledge}"
        - "{Flight risk}"
        - "{Upcoming retirement}"

      succession_candidates:
        ready_now:
          - name: "{Name}"
            strengths: []
            gaps: []
            development_plan: ""

        ready_1_2_years:
          - name: "{Name}"
            strengths: []
            gaps: []
            development_plan: ""

        ready_3_5_years:
          - name: "{Name}"
            strengths: []
            gaps: []
            development_plan: ""

      knowledge_transfer:
        documented: []
        in_progress: []
        needed: []

  talent_matrix:
    dimensions:
      performance: "Current job performance (1-5)"
      potential: "Future growth potential (1-5)"

    quadrants:
      stars:
        criteria: "High performance + High potential"
        actions:
          - "Accelerated development"
          - "Visible stretch assignments"
          - "Executive exposure"
          - "Retention focus"

      solid_performers:
        criteria: "High performance + Lower potential"
        actions:
          - "Recognize and reward"
          - "Deepen expertise"
          - "Consider lateral moves"
          - "Knowledge sharing role"

      high_potentials:
        criteria: "Developing performance + High potential"
        actions:
          - "Intensive coaching"
          - "Skill development"
          - "Patience with mistakes"
          - "Clear expectations"

      core_contributors:
        criteria: "Developing performance + Lower potential"
        actions:
          - "Clear expectations"
          - "Training if gaps"
          - "Right role fit?"
          - "Support or transition"

  review_cadence:
    full_review: "Annually"
    talent_discussions: "Quarterly"
    development_check_ins: "Monthly"
```

### Skill Gap Analysis

```yaml
skill_gap_analysis:
  team_assessment:
    team: "{Team name}"
    assessment_date: "{Date}"
    assessor: "{Name}"

  skill_inventory:
    technical_skills:
      - skill: "{Programming language}"
        required_level: "{1-5}"
        team_coverage:
          - member: "{Name}"
            level: "{1-5}"
        gap_score: null
        criticality: "{low | medium | high}"

      - skill: "{Framework/Tool}"
        required_level: ""
        team_coverage: []
        gap_score: null
        criticality: ""

    domain_skills:
      - skill: "{Domain knowledge}"
        required_level: ""
        team_coverage: []
        gap_score: null
        criticality: ""

    soft_skills:
      - skill: "{Communication, leadership, etc.}"
        required_level: ""
        team_coverage: []
        gap_score: null
        criticality: ""

  gap_analysis:
    critical_gaps:
      - skill: ""
        current_state: ""
        required_state: ""
        impact: ""
        mitigation:
          short_term: "{Hire, contract, partner}"
          long_term: "{Train, develop}"

    moderate_gaps:
      - skill: ""
        development_plan: ""

    nice_to_have:
      - skill: ""
        opportunistic_development: ""

  action_plan:
    hiring_needs: []
    training_investments: []
    mentoring_pairs: []
    knowledge_sharing: []
```

### Mentoring Program Framework

```yaml
mentoring_program:
  program_structure:
    name: "{Program name}"
    duration: "{6 months recommended}"
    cadence: "Bi-weekly 30-60 min sessions"

  matching_criteria:
    mentor_requirements:
      - "2+ levels above mentee"
      - "Different reporting chain preferred"
      - "Relevant experience to goals"
      - "Commitment to development"

    mentee_requirements:
      - "Clear development goals"
      - "Commitment to process"
      - "Open to feedback"
      - "Willingness to be vulnerable"

  program_phases:
    kickoff:
      duration: "Session 1"
      activities:
        - "Get to know each other"
        - "Share backgrounds and goals"
        - "Set expectations"
        - "Agree on logistics"
      outputs:
        - "Mentoring agreement signed"
        - "Goals documented"
        - "Schedule set"

    development:
      duration: "Sessions 2-10"
      activities:
        - "Work on development goals"
        - "Share experiences and advice"
        - "Provide feedback"
        - "Connect to opportunities"
      typical_topics:
        - "Career navigation"
        - "Technical challenges"
        - "Leadership development"
        - "Organizational dynamics"

    wrap_up:
      duration: "Sessions 11-12"
      activities:
        - "Review progress on goals"
        - "Celebrate achievements"
        - "Plan for continued growth"
        - "Provide program feedback"

  success_metrics:
    mentee_outcomes:
      - "Goal achievement rate"
      - "Promotion rate"
      - "Engagement scores"
      - "Retention rate"

    program_health:
      - "Match completion rate"
      - "NPS from participants"
      - "Session attendance"
      - "Repeat participation"
```

---

## Decision Trees

### Promotion Readiness Assessment

```
Promotion consideration
|
+-- Consistently meeting current level expectations?
|   +-- No -> Not ready, focus on current level
|   +-- Yes -> Continue
|
+-- Demonstrating next-level behaviors?
|   +-- Rarely -> Not ready, create IDP
|   +-- Sometimes -> Almost ready, targeted development
|   +-- Consistently -> Continue
|
+-- Scope and impact at next level?
|   +-- No opportunities yet -> Create stretch assignments
|   +-- Has delivered at scope -> Continue
|
+-- Peer and stakeholder feedback positive?
|   +-- Concerns -> Address feedback, reassess
|   +-- Strong support -> Ready to promote
```

### IC vs Management Track Decision

```
Career direction question
|
+-- What energizes them?
|   +-- Solving hard technical problems -> IC track
|   +-- Helping others succeed -> Consider management
|   +-- Both -> Explore tech lead role first
|
+-- What's their impact style?
|   +-- Individual mastery -> IC track
|   +-- Multiplier through others -> Management track
|
+-- How do they handle ambiguity?
|   +-- Prefer well-defined problems -> IC track
|   +-- Comfortable with people complexity -> Management track
|
+-- Are they willing to let go of coding?
|   +-- No -> IC track (even at Staff+)
|   +-- Yes -> Management viable
```

---

## Anti-Patterns

```yaml
anti_patterns:
  promotion_as_retention:
    symptom: "Promoting to prevent someone from leaving"
    remedy:
      - "Separate promotion from retention discussions"
      - "Promote when ready, not when threatening"
      - "Find other retention levers if not ready"

  peter_principle:
    symptom: "Promoting until incompetent"
    remedy:
      - "Assess readiness for next level, not current performance"
      - "Trial periods for new responsibilities"
      - "Safe path back if not working"

  neglecting_solid_performers:
    symptom: "All attention on high potentials"
    remedy:
      - "Recognize and value steady contributors"
      - "Create growth within level"
      - "Don't force everyone to climb"

  one_size_fits_all:
    symptom: "Same IDP template for everyone"
    remedy:
      - "Personalize to individual goals"
      - "Multiple paths to senior levels"
      - "Accommodate different learning styles"

  mentoring_without_structure:
    symptom: "Assigned mentors but no framework"
    remedy:
      - "Provide training for mentors"
      - "Set clear expectations"
      - "Regular check-ins on progress"
```

---

## Quick Reference Cards

### Development Conversation Starters

```yaml
conversation_starters:
  aspirations:
    - "Where do you see yourself in 2-3 years?"
    - "What kind of work gives you energy?"
    - "What would your ideal role look like?"

  strengths:
    - "What are you most proud of this year?"
    - "What do others come to you for?"
    - "When do you feel most confident?"

  growth:
    - "What skills would make you more effective?"
    - "What's holding you back from the next level?"
    - "What feedback have you received that stuck with you?"

  support:
    - "What do you need from me to grow?"
    - "What opportunities would help your development?"
    - "Who else should you be learning from?"
```

### Level Transition Indicators

| From | To | Key Indicators |
|------|-----|----------------|
| Junior | Mid | Independent on features, consistent quality |
| Mid | Senior | System-level thinking, mentoring others |
| Senior | Staff | Cross-team influence, strategic thinking |
| IC | Manager | People focus, letting go of individual work |

### 70-20-10 Development Mix

```
70% - Experience (On-the-job)
  - Stretch assignments
  - New projects
  - Cross-functional work
  - Leading initiatives

20% - Exposure (Learning from others)
  - Mentoring relationships
  - Shadowing senior folks
  - Networking
  - Feedback conversations

10% - Education (Formal learning)
  - Courses and certifications
  - Books and articles
  - Conferences
  - Internal training
```

---

## Troubleshooting

| Problem | Root Cause | Solution |
|---------|-----------|----------|
| Unclear promotion criteria | Vague level expectations | Define observable behaviors per level |
| Stagnant careers | No development focus | Regular IDP discussions, stretch assignments |
| Poor mentor matches | Random pairing | Structured matching based on goals |
| High attrition of high potentials | Not developing fast enough | Accelerated development programs |
| Skill gaps not addressed | No systematic assessment | Annual skill gap analysis |

---

## Validation Rules

```yaml
input_validation:
  development_goal:
    type: string
    min_length: 10
    required: true

  current_level:
    type: enum
    values: [junior, mid, senior, staff, principal, manager, senior_manager, director]
    required: false

  target_level:
    type: enum
    values: [junior, mid, senior, staff, principal, manager, senior_manager, director]
    required: false

  timeline:
    type: enum
    values: [6_months, 1_year, 2_years, 3_years, 5_years]
    required: false
```

---

## Resources

**Books**:
- The Manager's Path - Camille Fournier
- An Elegant Puzzle - Will Larson
- Staff Engineer - Will Larson
- The Making of a Manager - Julie Zhuo

**Frameworks**:
- Engineering Ladders (various companies)
- 70-20-10 Learning Model
- 9-Box Talent Matrix
- Mentoring Best Practices (ATD)

**Research**:
- Center for Creative Leadership research
- Deloitte High-Impact Learning Culture
- Gallup strengths-based development
