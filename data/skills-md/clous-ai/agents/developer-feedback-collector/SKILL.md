---
name: developer-feedback-collector
description: This skill should be used when the user asks to "collect feedback", "gather peer feedback", "create feedback prompts", "synthesize feedback themes", "run 360 review", or "compile performance feedback". Creates structured feedback collection processes with synthesis of themes, examples, and actionable items.
version: 0.1.0
license: MIT
---

# Developer Feedback Collector

Design structured feedback collection processes that generate actionable, specific, and balanced input for performance reviews and growth conversations.

## Purpose

Create feedback systems that:
- Generate specific, example-based feedback
- Identify themes across multiple inputs
- Balance positive and constructive feedback
- Protect psychological safety
- Enable data-driven performance discussions

## Core Process

### 1. Design Feedback Prompts

**Structured Question Framework:**

```markdown
## Technical Excellence
- What technical contributions has [Name] made that stand out?
- Where could [Name] improve technically?
- Specific example: [Describe situation]

## Collaboration & Communication
- How effectively does [Name] work with others?
- Example of strong collaboration: [Describe]
- Area for growth in collaboration: [Describe]

## Leadership & Impact
- How does [Name] influence beyond their immediate work?
- Example of leadership: [Describe]
- Growth opportunity in leadership: [Describe]

## Overall
- What should [Name] continue doing?
- What should [Name] start/stop doing?
- One specific development suggestion: [Describe]
```

**Prompt Design Principles:**
- Ask for specific examples, not generalizations
- Balance positive and constructive
- Frame constructively (growth opportunities, not failures)
- Use behavioral language (observable actions)
- Avoid leading questions

### 2. Collect Feedback

**Who to Ask:**
- Direct manager (required)
- Peers (3-5 engineers at similar level)
- Cross-functional partners (PM, design, etc.)
- Skip-level manager (for senior+)
- Mentees (if applicable)

**Collection Methods:**
- Written surveys (async, allows reflection)
- 1:1 conversations (deeper context)
- Anonymous (for honest constructive feedback)
- Attributed (for accountability and follow-up)

**Best Practice:** Mix of attributed and anonymous for balanced input

### 3. Synthesize Themes

**Synthesis Process:**
1. Read all feedback inputs
2. Identify recurring themes (3+ mentions = pattern)
3. Group examples by theme
4. Note outlier feedback (1-off mentions)
5. Look for contradictions (investigate causes)

**Output Structure:**

```json
{
  "employee": "Name",
  "feedback_period": "Q4 2025",
  "respondents": 8,
  "themes": [
    {
      "category": "Technical Excellence",
      "theme": "Strong system design skills",
      "frequency": 6,
      "examples": [
        "Designed scalable caching architecture for API - reduced latency 60%",
        "Led database migration with zero downtime"
      ],
      "type": "strength"
    },
    {
      "category": "Collaboration",
      "theme": "Could improve communication in PRs",
      "frequency": 4,
      "examples": [
        "PR comments sometimes terse, hard to understand reasoning",
        "Could explain design decisions more clearly in code review"
      ],
      "type": "growth_area"
    }
  ],
  "actionable_items": [
    "Continue driving architectural initiatives",
    "Work on PR communication: explain *why* in code review comments"
  ]
}
```

### 4. Deliver Feedback

**Delivery Framework (Manager → Employee):**

```markdown
## Feedback Summary: [Name] - [Period]

### Key Strengths
[Theme 1 with examples]
[Theme 2 with examples]

### Growth Opportunities
[Theme 1 with examples and specific suggestions]
[Theme 2 with examples and specific suggestions]

### Action Plan
1. [Specific action]: [Why] → [How to measure success]
2. [Specific action]: [Why] → [How to measure success]

### Next Steps
- [Discuss in 1:1 on DATE]
- [Set goals for next period]
```

**Delivery Best Practices:**
- Start with strengths (build confidence)
- Be specific (examples, not vague criticisms)
- Focus on behaviors (changeable) not traits (fixed)
- Collaborative tone (partner in growth)
- Forward-looking (action plan, not dwelling on past)

## Using Supporting Resources

### Templates
- **`templates/feedback-prompts.json`** - Question bank by competency
- **`templates/synthesis-template.md`** - Theme identification framework

### Scripts
- **`scripts/synthesize-feedback.py`** - Auto-detect themes from responses
- **`scripts/anonymize.py`** - Remove identifying information

---

**Progressive Disclosure:** Advanced synthesis techniques, difficult feedback scenarios in references/.
