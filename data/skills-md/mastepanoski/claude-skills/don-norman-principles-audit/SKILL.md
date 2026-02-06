---
name: don-norman-principles-audit
description: Evaluate UX/UI using Don Norman's 7 fundamental design principles from The Design of Everyday Things. Audit discoverability, affordances, signifiers, feedback, mapping, constraints and conceptual models.
---

# Don Norman Principles UX Audit

This skill enables AI agents to perform a **human-centered evaluation** of usability and intuitiveness for apps, websites, or digital interfaces using **Don Norman's 7 fundamental design principles** from *The Design of Everyday Things*.

The principles emphasize discoverability, natural perception, and cognitive load reduction. Use this skill to detect intuitive frustrations (like digital "Norman doors"), improve user experience, and propose redesigns.

Combine with "Nielsen Heuristics UX Audit" or "UX Audit and Rethink" skills for comprehensive audits.

## When to Use This Skill

Invoke this skill when:
- Evaluating the intuitiveness of an interface
- Identifying usability problems from a human-centered perspective
- Assessing how naturally users can discover and use features
- Auditing digital products for cognitive friction
- Planning UX improvements based on fundamental design principles

## Inputs Required

When executing this audit, gather:

- **interface_description**: Detailed interface description (purpose, users, key flows, platform: web/mobile) [REQUIRED]
- **screenshots_or_links**: URLs of screenshots, wireframes, or live site/app [OPTIONAL]
- **user_tasks**: Representative user tasks (e.g., "log in", "add to cart", "navigate menu") [OPTIONAL]
- **existing_feedback**: User comments or pain points [OPTIONAL]

## The 7 Principles (Standard Edition)

Evaluate against these principles from Don Norman's revised edition:

### 1. Discoverability
**Can users determine what actions are possible and the current system state just by looking?**
- The design must make action possibilities visible from the start
- Users shouldn't need to hunt for features or guess what's possible

### 2. Affordance
**Do elements naturally suggest their possible use?**
- Buttons should look pressable
- Sliders should invite sliding
- Physical or perceived properties that determine use

### 3. Signifiers
**Are there clear signals (icons, labels, colors) indicating where and how to act?**
- Explicit cues that complement affordances
- Visual, auditory, or tactile indicators of what actions to take

### 4. Feedback
**Does the system respond immediately to each action, informing what happened and the new state?**
- Must be complete, continuous, and understandable
- Users should never wonder "did that work?"

### 5. Mapping
**Do controls logically correspond with their effects?**
- Natural relationships (spatial, analogical) between actions and results
- Intuitive layout that matches mental models

### 6. Constraints
**Are possible actions limited to prevent errors?**
- Physical, logical, semantic, or cultural constraints
- Guide users toward correct actions by eliminating wrong ones

### 7. Conceptual Models
**Does the design support a coherent and consistent mental model of the system?**
- Users should form intuitive understanding of how it works
- Align with user expectations and prior experiences

## Audit Procedure

Follow these steps iteratively, simulating real user interaction:

### Step 1: Preparation
1. Analyze `interface_description`, `screenshots_or_links`, and `user_tasks` to understand context and flows
2. Define 3-5 key tasks if not provided
3. Review the 7 principles listed above

### Step 2: Principle-by-Principle Evaluation

For each of the 7 principles:

1. **Examine** the interface and tasks thoroughly
2. **Identify** compliance or violations with evidence:
   - Specific screens, steps, or behaviors
   - Quote or screenshot problematic areas
3. **Assign severity**:
   - **Catastrophic**: Prevents intuitive use or causes severe errors
   - **High**: Significant friction or frequent confusion
   - **Medium**: Annoying but surmountable
   - **Low**: Minor or cosmetic issue
4. **Propose** 1-3 concrete recommendations (e.g., "Add magnifying glass icon as signifier for search")

### Step 3: Synthesis and Prioritization

1. Group related problems (e.g., lack of feedback + poor mapping)
2. Prioritize by: severity + frequency + impact on critical tasks
3. Calculate overall score (approximate % of principles well-met)
4. Suggest next steps: user testing, Design Thinking iteration

### Step 4: Final Report Structure

Provide a clear, structured report:

#### Executive Summary
- Main strengths
- Key weaknesses
- Overall human-centered score (1-10 or qualitative)

#### Detailed Evaluation by Principle
For each principle:
- **Compliance level**: Excellent / Good / Fair / Poor
- **Evidence**: Specific examples with screenshots/descriptions
- **Violations found**: Detailed description
- **Severity**: Catastrophic / High / Medium / Low
- **Recommendations**: Actionable improvements

#### Prioritized Issues List
1. Most critical issues first
2. Include: principle violated, severity, affected tasks, recommendation

#### Redesign Suggestions
- Concrete design improvements
- Quick wins vs. long-term changes
- Alternative interaction patterns

#### Limitations
- Note this is an expert evaluation simulation
- Recommend validation with real users
- Suggest follow-up user testing methods

## Example Violations to Watch For

### Classic "Norman Doors" in Digital Interfaces:
- **Discoverability**: Hidden navigation, invisible buttons, features users can't find
- **Affordance**: Links that don't look clickable, buttons that look disabled when active
- **Signifiers**: Missing icons, unclear labels, no visual cues for interactivity
- **Feedback**: Actions with no confirmation, loading without indicators, silent errors
- **Mapping**: Controls far from their effects, illogical groupings, counter-intuitive layouts
- **Constraints**: Allowing invalid inputs, no prevention of destructive actions, unclear boundaries
- **Conceptual Models**: Inconsistent behavior, breaking conventions, confusing metaphors

## Output Format

Structure your audit report as:

```markdown
# Don Norman Principles UX Audit Report

## Executive Summary
[Overall assessment]

**Overall Score**: [X/10]
**Critical Issues**: [number]
**High Priority Issues**: [number]

## Principle Evaluations

### 1. Discoverability
**Score**: [rating]
**Violations**: [list]
**Recommendations**: [list]

[Repeat for all 7 principles]

## Prioritized Issues
1. [Issue] - [Severity] - [Principle]
   - **Impact**: [description]
   - **Recommendation**: [action]

## Redesign Suggestions
[Concrete improvements organized by impact]

## Next Steps
[Recommended actions for validation and improvement]
```

## Best Practices

1. **Be Specific**: Use concrete examples, not vague statements
2. **Show Evidence**: Reference specific UI elements, flows, or interactions
3. **Prioritize Ruthlessly**: Focus on issues that truly impact usability
4. **Propose Solutions**: Don't just identify problems—suggest fixes
5. **Consider Context**: Mobile vs. desktop, novice vs. expert users
6. **Stay Objective**: Base findings on principles, not personal preference
7. **Validate**: Recommend user testing to confirm findings

## Combining with Other Audits

- **Nielsen Heuristics**: For comprehensive usability evaluation
- **WCAG Accessibility**: For inclusive design compliance
- **7 UX Factors (IxDF)**: For holistic experience assessment
- **Cognitive Walkthrough**: For task-specific deep dives

## Reference

Based on **Don Norman's "The Design of Everyday Things" (Revised Edition)**
Principles: Discoverability, Affordance, Signifiers, Feedback, Mapping, Constraints, Conceptual Models

Adapted for digital interface evaluation in alignment with modern UX standards (2026).

## Version

1.0 - Initial release

---

**Remember**: This is a simulated expert evaluation. Always validate findings with real users through usability testing, interviews, and analytics.
