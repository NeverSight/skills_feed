---
name: research-synthesis
description: >
  Synthesize user research into actionable insights using atomic research
  methods. Use when asked to synthesize research, organize user feedback,
  find patterns in interviews, summarize customer discovery, or turn raw
  notes into insights and recommendations.
---

Turn raw research into atomic insights that drive decisions. Good synthesis surfaces patterns, bad synthesis creates narrative fiction. The goal is structured evidence, not a compelling story that cherry-picks quotes.

## Atomic Research Method

Break research into four levels, bottom-up:

### 1. Nuggets (Raw Evidence)
Individual observations from a single source. Each nugget is:
- One observation per nugget (not a paragraph)
- Tagged with source (participant ID, date, method)
- Direct quotes preferred over your interpretation

Example: "[P3, Jan 12] 'I spend 30 minutes after every customer call just trying to remember what they said.'"

### 2. Patterns (Recurring Themes)
Group nuggets that point to the same phenomenon. A pattern requires evidence from 3+ independent sources.

Example: "5 of 7 PMs report spending 20-45 minutes on post-call documentation. All describe it as tedious and low-value."

### 3. Insights (Implications)
What the pattern means for the product. An insight connects a pattern to a product opportunity or risk.

Example: "Post-call documentation is a high-frequency pain point (daily for active PMs) with no satisfying solution. Current workarounds (voice memos, bullet lists) lose context and emotional nuance."

### 4. Recommendations (Actions)
Specific product actions justified by insights. Each recommendation traces back through the chain: recommendation ← insight ← pattern ← nuggets.

## Evidence Strength

Rate every pattern and insight:

| Strength | Criteria |
|----------|----------|
| **Strong** | 5+ sources, consistent behavior observed, corroborated by data |
| **Moderate** | 3-4 sources, mostly consistent, some data support |
| **Emerging** | 2 sources, needs more evidence before acting |
| **Weak** | Single source or contradictory evidence |

NEVER make product recommendations based on Weak or Emerging evidence. Flag them for further research.

## Synthesis Process

1. Extract all nuggets from raw notes — one per line, tagged with source
2. Affinity map: group nuggets by theme (not by interview)
3. Name each group as a pattern with a count ("5/7 participants...")
4. Derive insights from strong and moderate patterns only
5. Write recommendations that trace back to specific insights
6. Flag contradictions explicitly — don't smooth them over

## Guidelines

- CRITICAL: NEVER synthesize from fewer than 3 data points. Two people saying the same thing is a coincidence, not a pattern.
- ALWAYS cite specific evidence. "Users struggle with X" is worthless. "5 of 7 participants spent 20+ minutes on X, with P2 calling it 'the worst part of my week'" is evidence.
- ALWAYS weight actions over opinions. What people DO matters more than what they SAY.
- NEVER cherry-pick quotes to support a narrative. Include contradictory evidence.
- ALWAYS flag your confidence level. Distinguish "we know" from "we think."
- NEVER present synthesis without the evidence chain. Anyone reading should be able to trace a recommendation back to raw nuggets.

---

*Built on the Atomic Research method (Daniel Pidcock) and Continuous Discovery Habits (Teresa Torres). Skills from [productskills](https://github.com/assimovt/productskills).*
