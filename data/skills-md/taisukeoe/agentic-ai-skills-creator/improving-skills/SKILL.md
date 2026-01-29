---
name: improving-skills
description: Improve existing agent skills based on user feedback and best practices. Use when the user wants to fix, enhance, or refactor an existing skill. Gathers user feedback first, then applies technical analysis and implements improvements.
license: Apache-2.0
metadata:
  author: Softgraphy GK
  version: "0.2.0"
---

# Improving Skills

Improve existing agent skills through gathering user feedback and technical analysis.

## Workflow

### Step 1: Identify Target Skill

Ask user for the skill path if not provided (e.g., `.claude/skills/skill-name/`).

Read SKILL.md and understand current structure.

### Step 2: Gather Feedback (Required)

Ask the essential question:

> "What problems or improvements do you want for this skill?"

Based on the response, ask follow-up questions as needed:

| If user mentions... | Follow-up question |
|---------------------|-------------------|
| Vague dissatisfaction | "Can you give a specific example of when it didn't work well?" |
| Trigger issues | "When does it fail to trigger, or trigger unexpectedly?" |
| Missing features | "What should the output look like when this feature works?" |
| Too much/little output | "What level of detail do you prefer?" |
| Unclear scope | "What tasks should this skill handle vs. not handle?" |

Keep follow-ups minimal. One or two is usually enough.

### Step 3: Technical Analysis

Check against best practices (reference reviewing-skills criteria):

- **Naming**: Gerund form, descriptive
- **Description**: Third person, includes what + when
- **Size**: SKILL.md < 500 lines
- **Progressive disclosure**: Details in references
- **Single responsibility**: One clear purpose
- **Tests**: tests/scenarios.md exists (required for `/evaluating-skills-with-models`)

### Step 4: Present Improvement Plan

Organize improvements into:

**User-requested improvements**:
- Based on feedback
- Prioritize what user explicitly mentioned

**Technical improvements**:
- Issues found in analysis
- Only include if impactful

Format:
```
## Improvement Plan

### User-requested
1. [Issue from feedback] → [Proposed fix]

### Technical
1. [Issue from analysis] → [Proposed fix]

Proceed with these changes?
```

### Step 5: Implement

Execute the improvements:
1. Edit SKILL.md
2. Update/create reference files if needed
3. Adjust scripts/assets if applicable

Show diff or summary of changes made.

### Step 6: Verify

Quick check:
- Changes address user's stated problems
- No new issues introduced
- Skill still follows best practices

## Key Difference from reviewing-skills

| reviewing-skills | improving-skills |
|-----------------|------------------|
| Technical analysis only | User feedback + technical analysis |
| Provides feedback | Implements changes |
| Read-only | Read-write |

