---
name: ux-journey
description: Comprehensive UX analysis coordinating design, accessibility, and gamification agents for user flow and interaction evaluation.
version: 1.0.0
---

# UX Journey Analysis

You are conducting a comprehensive user experience analysis. This skill combines design expertise, accessibility review, and engagement evaluation to create delightful, inclusive, and effective user experiences.

## UX Analysis Domains

### 1. Design System & Visual Hierarchy (@geepers_design / design-system-architect)

**Swiss Design Principles:**
- Grid systems and mathematical precision
- Typography hierarchy (size, weight, color)
- Whitespace and rhythm
- Color application (purposeful, not decorative)
- Consistency across components

**Evaluation Criteria:**
- Does the eye flow naturally through the interface?
- Is importance clearly communicated?
- Are patterns repeated predictably?
- Is contrast sufficient (4.5:1 text, 3:1 UI)?

### 2. Accessibility & Inclusive Design (@geepers_a11y / accessibility-ux-reviewer)

**WCAG 2.1 AA Compliance:**
- Keyboard navigation
- Screen reader support
- Touch targets (44x44px minimum)
- Color independence
- Motion sensitivity (prefers-reduced-motion)
- Cognitive accessibility

**AAC-Specific Considerations (if applicable):**
- Symbol clarity
- Large touch targets for motor accessibility
- Predictable navigation
- High-frequency word prioritization

### 3. Engagement & Gamification (@geepers_game / gameifier-ux-enhancer)

**Core Loop Analysis:**
- What is the fundamental interaction pattern?
- Is there clear progression?
- Are loops satisfying and complete?

**Feedback Systems:**
- How does the system communicate success/failure?
- Is feedback immediate and satisfying?
- Are there visual, auditory cues?

**Reward Structures:**
- What rewards does the system offer?
- Are rewards frequent enough?
- Is there variety (intrinsic/extrinsic)?

### 4. Interaction Patterns (@geepers_design)

**User Flow Analysis:**
- Navigation clarity
- Form interactions
- Error handling and recovery
- Loading states and feedback
- Mobile considerations

## Execution Strategy

**Launch agents in PARALLEL:**

```
1. @geepers_design - Visual design and hierarchy review
2. @geepers_a11y - Accessibility audit
3. @geepers_design - Interaction pattern analysis
4. @geepers_game - Engagement and gamification opportunities
```

## Output Format

```
🎨 UX JOURNEY ANALYSIS

Project: {name}
Interface: {specific page/component}
Date: {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
           EXPERIENCE SCORE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall UX Grade: [A-F]

🎨 Visual Design:    [★★★★☆] 4/5
♿ Accessibility:     [★★★☆☆] 3/5
🎮 Engagement:       [★★☆☆☆] 2/5
🔄 Interaction Flow: [★★★★☆] 4/5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          USER JOURNEY MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Entry] → [Discovery] → [Action] → [Feedback] → [Completion]
   ✓         ⚠️            ✓          ❌           ⚠️

Pain Points Identified:
1. Discovery: {description of friction}
2. Feedback: {missing or poor feedback}

Moments of Delight:
1. {positive experience}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         DESIGN EVALUATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Visual Hierarchy: [CLEAR/MODERATE/CONFUSED]
- Primary CTA visibility: {assessment}
- Information architecture: {assessment}
- Typography system: {assessment}

Swiss Design Compliance:
✓ Grid alignment
✓ Consistent spacing (8px base)
⚠️ Typography scale could be more pronounced
❌ Color used decoratively in {location}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      ACCESSIBILITY FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WCAG Status: [AA COMPLIANT/PARTIALLY/NON-COMPLIANT]

Critical Issues:
- [A11Y] {description}

Keyboard Navigation: [FULL/PARTIAL/BROKEN]
Screen Reader: [EXCELLENT/GOOD/POOR]
Color Contrast: [PASSING/FAILING]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       ENGAGEMENT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Loop Satisfaction: [HIGH/MEDIUM/LOW]

Gamification Opportunities:
1. 🏆 {achievement system suggestion}
2. 📈 {progress indicator suggestion}
3. 🎯 {goal/milestone suggestion}
4. ✨ {micro-interaction suggestion}

Feedback System Quality:
- Success feedback: {rating}
- Error feedback: {rating}
- Progress indication: {rating}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
         RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick Wins (High Impact, Low Effort):
1. {immediate improvement}
2. {easy fix}

Strategic Improvements:
1. {medium-term enhancement}
2. {design system update}

Engagement Enhancements:
1. {gamification addition}
2. {feedback improvement}
```

## UX Evaluation Framework

### The 5 E's of UX

1. **Effective** - Can users accomplish their goals?
2. **Efficient** - How quickly can they do it?
3. **Engaging** - Is the experience enjoyable?
4. **Error-tolerant** - How gracefully does it handle mistakes?
5. **Easy to learn** - Can new users figure it out?

### Emotional Journey Mapping

Track user emotions through the flow:
- 😊 Delight - Exceeds expectations
- 😐 Neutral - Meets expectations
- 😕 Frustration - Below expectations
- 😤 Abandonment - Complete failure

## When to Use UX Journey

- **New feature design** - Before building
- **Post-implementation review** - After building
- **User feedback analysis** - When users report issues
- **Competitive analysis** - Comparing to alternatives
- **Periodic review** - Quarterly UX health checks

## Key Principles

1. **User-centered** - Always start with user goals
2. **Inclusive** - Accessibility is not optional
3. **Delightful** - Good UX creates joy
4. **Measurable** - Define success metrics
5. **Iterative** - UX improves through feedback

## Related Skills

- `/quality-audit` - Includes accessibility as part of broader audit
- `/scout` - Quick check may surface obvious UX issues
- `/data-artist` - For data visualization UX specifically
