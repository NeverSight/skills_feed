---
name: learning-design-review
description: Review educational content against the Four Learning Design Pillars framework. Use when users want to evaluate course materials, lessons, tutorials, e-learning modules, or any instructional content for alignment with evidence-based learning design principles. Provides structured feedback with specific principle references (e.g., 1.1.1, 2.3.4) and actionable recommendations.
---

# Learning Design Review

Evaluate educational content against the Four Learning Design Pillars - an evidence-based framework synthesized from multimedia learning research, cognitive load theory, and UX best practices.

## Skill Purpose

This skill provides structured reviews of educational content by evaluating it against 46 research-based principles organized into four pillars:

1. **Pillar 1: Clear, Purposeful Structure** - Content organization, design consistency, learning path clarity, adaptive design
2. **Pillar 2: Active, Engaging Learning Content** - Content design, multimedia elements, engagement techniques, quality standards
3. **Pillar 3: Continuous Practice & Feedback** - Practice variety, feedback mechanisms, metacognition support
4. **Pillar 4: Simple, Intuitive UX** - Navigation, accessibility, media controls

## Usage

Invoke this skill when users say things like:
- "Review this course against learning design principles"
- "Evaluate my lesson plan"
- "Check if my tutorial follows best practices"
- "Analyze this e-learning module"
- "Review this educational content"

## Workflow

### Step 1: Gather the Content

Ask the user to provide the educational content in one of these formats:

```
To review your content against the Four Learning Design Pillars, please provide it in one of these ways:

1. **File path** - Path to a document, HTML file, or course export
2. **URL** - Link to a publicly accessible course page or lesson
3. **Pasted text** - Copy and paste the content directly
4. **Description** - Describe the course structure and key elements

What would you like me to review?
```

### Step 2: Load the Principles

Read the principles file to ensure access to all current principle definitions:

```
{SKILL_DIR}/../principles/learning-design-pillars.yaml
```

Note: `{SKILL_DIR}` refers to this skill's directory. When installed at `~/.claude/skills/learning-design-pillars/`, the principles file is at `~/.claude/skills/learning-design-pillars/principles/`.

This file contains the complete framework with 4 pillars, 13 categories, and 46 principles.

### Step 3: Analyze Content Against Each Pillar

Evaluate the content systematically against each pillar. For each pillar, identify:
- **Strengths**: What the content does well (cite specific principle IDs)
- **Areas for Improvement**: Where the content falls short (cite specific principle IDs)
- **Evidence**: Specific examples from the content supporting your assessment

#### Pillar 1: Clear, Purposeful Structure (Principles 1.1.1-1.4.2)

Evaluate:
- Content segmentation and organization (1.1.x)
- Design consistency and formatting (1.2.x)
- Learning objectives and alignment (1.3.x)
- Adaptive and learner-controlled elements (1.4.x)

#### Pillar 2: Active, Engaging Learning Content (Principles 2.1.1-2.4.4)

Evaluate:
- Content presentation and visual design (2.1.x)
- Multimedia and interactive elements (2.2.x)
- Engagement and relevance techniques (2.3.x)
- Quality, accuracy, and accessibility (2.4.x)

#### Pillar 3: Continuous Practice & Feedback (Principles 3.1.1-3.3.4)

Evaluate:
- Practice variety and authenticity (3.1.x)
- Feedback quality and timeliness (3.2.x)
- Metacognition and reflection support (3.3.x)

#### Pillar 4: Simple, Intuitive UX (Principles 4.1.1-4.3.2)

Evaluate:
- Navigation and orientation (4.1.x)
- Accessibility and device optimization (4.2.x)
- Media controls and time estimates (4.3.x)

### Step 4: Calculate Scores

Score each pillar on a 1-5 scale:

| Score | Rating | Description |
|-------|--------|-------------|
| 5 | Exemplary | Consistently demonstrates best practices across all principles |
| 4 | Strong | Good alignment with most principles, minor gaps |
| 3 | Developing | Meets basic requirements, notable improvement areas |
| 2 | Emerging | Significant gaps, limited alignment with principles |
| 1 | Beginning | Major redesign needed across most principles |

Calculate an overall weighted score (equal weight per pillar).

### Step 5: Generate the Review Report

Produce a structured report using this format:

```markdown
# Learning Design Review

**Content Reviewed:** [Name/description of content]
**Review Date:** [Date]
**Overall Score:** [X.X/5.0] - [Rating]

---

## Executive Summary

[2-3 sentence overview of key findings]

---

## Pillar 1: Clear, Purposeful Structure
**Score: X/5**

### Strengths
- [Strength 1] (Principle X.X.X)
- [Strength 2] (Principle X.X.X)

### Areas for Improvement
- [Gap 1] (Principle X.X.X): [Specific recommendation]
- [Gap 2] (Principle X.X.X): [Specific recommendation]

---

## Pillar 2: Active, Engaging Learning Content
**Score: X/5**

### Strengths
- [Strength 1] (Principle X.X.X)
- [Strength 2] (Principle X.X.X)

### Areas for Improvement
- [Gap 1] (Principle X.X.X): [Specific recommendation]
- [Gap 2] (Principle X.X.X): [Specific recommendation]

---

## Pillar 3: Continuous Practice & Feedback
**Score: X/5**

### Strengths
- [Strength 1] (Principle X.X.X)
- [Strength 2] (Principle X.X.X)

### Areas for Improvement
- [Gap 1] (Principle X.X.X): [Specific recommendation]
- [Gap 2] (Principle X.X.X): [Specific recommendation]

---

## Pillar 4: Simple, Intuitive UX
**Score: X/5**

### Strengths
- [Strength 1] (Principle X.X.X)
- [Strength 2] (Principle X.X.X)

### Areas for Improvement
- [Gap 1] (Principle X.X.X): [Specific recommendation]
- [Gap 2] (Principle X.X.X): [Specific recommendation]

---

## Priority Recommendations

Ranked by impact and effort:

1. **[High Priority]** [Recommendation] (Addresses: X.X.X, X.X.X)
   - Why: [Rationale]
   - How: [Specific action steps]

2. **[Medium Priority]** [Recommendation] (Addresses: X.X.X)
   - Why: [Rationale]
   - How: [Specific action steps]

3. **[Lower Priority]** [Recommendation] (Addresses: X.X.X)
   - Why: [Rationale]
   - How: [Specific action steps]

---

## Quick Wins

Small changes with immediate impact:
- [ ] [Quick win 1]
- [ ] [Quick win 2]
- [ ] [Quick win 3]
```

## Principle Reference Quick Guide

When citing principles, use the hierarchical ID system:

- **1.x.x** = Structure (Organization, Consistency, Learning Path, Adaptive)
- **2.x.x** = Content (Design, Multimedia, Engagement, Quality)
- **3.x.x** = Practice (Variety, Feedback, Metacognition)
- **4.x.x** = UX (Navigation, Accessibility, Media Control)

Example citations:
- "Clear learning objectives at module start (1.3.1)"
- "Short, focused video segments under 5 minutes (2.2.3)"
- "Low-stakes practice quizzes with unlimited attempts (3.1.6)"
- "Mobile-responsive layout (4.2.3)"

## Notes

- Always reference specific principle IDs to make feedback actionable
- Prioritize recommendations by impact on learning outcomes
- Consider the content's context (audience, constraints, platform)
- Focus on actionable suggestions, not just critique
- When in doubt about a rating, err toward constructive feedback
