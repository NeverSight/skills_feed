---
name: content-scoring
description: Score content against GEO optimization criteria. Triggers on "score this", "rate content", "GEO score", "how does this rank", "evaluate content", "content score".
---

# Content Scoring Skill

When scoring content for GEO optimization:

## The 10 GEO Criteria

Score each criterion 0-10:

| # | Criterion | What to Look For |
|---|-----------|------------------|
| 1 | **Ranking Emphasis** | "best", "top", "#1", superlatives, leadership claims |
| 2 | **User Intent** | Direct answers, addresses specific needs, solves problems |
| 3 | **Competitive Diff** | Unique advantages, "unlike others", differentiators |
| 4 | **Social Proof** | Stats, testimonials, reviews, customer counts, ratings |
| 5 | **Narrative** | Engaging flow, persuasive language, compelling story |
| 6 | **Authority** | Expert tone, credentials, specific knowledge, confidence |
| 7 | **USPs** | Clear unique value, what makes it special |
| 8 | **Urgency** | Time limits, scarcity, "now", limited availability |
| 9 | **Scannable** | Headers, bullets, short paragraphs, clear structure |
| 10 | **Factual** | Verifiable claims, specific numbers, accurate info |

## Scoring Guide

- **0-2**: Missing or severely lacking
- **3-4**: Present but weak
- **5-6**: Adequate, room for improvement
- **7-8**: Good, minor improvements possible
- **9-10**: Excellent, near optimal

## Output Format

```
┌─────────────────────────────────────────────────────────────┐
│  📊 GEO CONTENT SCORE                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  OVERALL SCORE: XX/100                                      │
│  ██████████████████░░░░░░░░░░  XX%                          │
│                                                             │
│  BREAKDOWN                                                  │
│  ─────────                                                  │
│  1. Ranking Emphasis    ████████░░  8/10                    │
│  2. User Intent         ██████████  10/10                   │
│  3. Competitive Diff    ████░░░░░░  4/10                    │
│  4. Social Proof        ██░░░░░░░░  2/10  ⚠️ Priority       │
│  5. Narrative           ██████░░░░  6/10                    │
│  6. Authority           ████████░░  8/10                    │
│  7. USPs                ██████░░░░  6/10                    │
│  8. Urgency             ░░░░░░░░░░  0/10  ⚠️ Priority       │
│  9. Scannable           ████████░░  8/10                    │
│  10. Factual            ██████████  10/10                   │
│                                                             │
│  TOP PRIORITIES                                             │
│  ──────────────                                             │
│  1. Add social proof (+15-20 points potential)              │
│  2. Add urgency signals (+5-10 points potential)            │
│  3. Strengthen competitive differentiation (+8 points)      │
│                                                             │
│  EVIDENCE                                                   │
│  ────────                                                   │
│  ✓ Good: "industry-leading solution" (ranking emphasis)     │
│  ✗ Missing: No customer testimonials (social proof)         │
│  ✗ Missing: No time-sensitive offers (urgency)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Rules
- Always show evidence from the actual content
- Prioritize improvements by potential impact
- Be specific about what's missing and how to fix it
- Calculate total score as sum of all criteria
