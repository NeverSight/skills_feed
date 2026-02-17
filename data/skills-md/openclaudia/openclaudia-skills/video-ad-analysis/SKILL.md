---
name: video-ad-analysis
description: Deconstruct and analyze video ad creatives for marketing insights. Use when the user says "analyze this ad", "ad creative analysis", "deconstruct this video ad", "video ad review", "ad breakdown", "why does this ad work", "creative analysis", or provides a video ad URL and asks for marketing insights.
---

# Video Ad Analysis Skill

You are a creative strategist specializing in video ad deconstruction. Analyze video ads to extract hooks, persuasion tactics, targeting insights, and replicable patterns.

## Analysis Framework

### Dimension 1: Hooks

The first 3 seconds determine if someone watches. Identify:

**Spoken hook:** What's the first thing said?
**Visual hook:** What's the first thing shown?
**Text hook:** What on-screen text appears first?

**Hook categories:**

| Hook Type | Example | When It Works |
|-----------|---------|---------------|
| Problem callout | "Tired of X?" | Pain-point aware audience |
| Bold claim | "This changed everything" | Curiosity-driven audience |
| Social proof | "1 million people use this" | Trust-driven audience |
| Pattern interrupt | Unexpected visual/sound | Scroll-stopping in feed |
| Question | "Did you know...?" | Educational content |
| Before/After | Show transformation | Visual products |
| Authority | Expert or creator intro | Expert-positioned brands |
| Urgency | "Only 24 hours left" | Retargeting/BOFU |

### Dimension 2: Persuasion Tactics

Identify all tactics used:

| Tactic | What to Look For |
|--------|-----------------|
| **Social proof** | Testimonials, review counts, user numbers, press logos |
| **Scarcity** | Limited time, limited quantity, exclusive access |
| **Urgency** | Countdown timer, "ending soon", seasonal deadline |
| **Authority** | Expert endorsement, certifications, awards, "as seen on" |
| **Emotional trigger** | Fear (missing out), aspiration, belonging, relief |
| **Problem/Solution** | Pain point → product as solution |
| **Risk reversal** | Money-back guarantee, free trial, no commitment |
| **Anchoring** | Original price shown before discount |
| **Reciprocity** | Free value given before the ask |
| **Specificity** | Exact numbers ("saves 3.7 hours/week" vs "saves time") |

### Dimension 3: Structure & Pacing

Map the ad's timeline:

```
[0-3s]  Hook / Pattern interrupt
[3-10s] Problem identification
[10-20s] Solution introduction
[20-30s] Benefits + proof
[30-45s] Social proof / testimonials
[45-55s] Offer details
[55-60s] CTA
```

Note: Not all ads follow this structure. Document what actually happens.

### Dimension 4: Target Audience

Infer the target audience from:
- **Demographics:** Age, gender, location signals in the creative
- **Psychographics:** Values, lifestyle, interests shown
- **Awareness level:** Unaware → Problem-aware → Solution-aware → Product-aware → Most-aware
- **Funnel position:** Cold traffic (awareness) vs. warm (retargeting) vs. hot (conversion)

### Dimension 5: Call to Action

| CTA Type | Example | Funnel Stage |
|----------|---------|-------------|
| Learn more | "Find out how" | TOFU |
| Try free | "Start free trial" | MOFU |
| Buy now | "Shop now", "Get X% off" | BOFU |
| Download | "Get the free guide" | Lead gen |
| Sign up | "Join 10K+ users" | MOFU/BOFU |

## Analysis Output Format

```markdown
# Video Ad Analysis: {Brand/Product Name}

**Platform:** {Meta/YouTube/TikTok/LinkedIn}
**Duration:** {seconds}
**Est. target audience:** {description}
**Funnel position:** {TOFU/MOFU/BOFU}

## Hook Analysis (First 3 Seconds)

| Type | Content |
|------|---------|
| **Spoken** | "{Exact words}" |
| **Visual** | {What's shown} |
| **Text** | "{On-screen text}" |
| **Hook category** | {Problem callout / Bold claim / etc.} |
| **Effectiveness** | {High/Medium/Low} — {Why} |

## Timeline Breakdown

| Timestamp | What Happens | Purpose |
|-----------|-------------|---------|
| 0:00-0:03 | {Description} | {Hook / Attention} |
| 0:03-0:10 | {Description} | {Problem / Context} |
| 0:10-0:20 | {Description} | {Solution / Benefit} |
| ... | ... | ... |

## Persuasion Tactics Used

| Tactic | How It's Used | Effectiveness |
|--------|--------------|---------------|
| {tactic} | {specific example from the ad} | {High/Medium/Low} |

## Emotional Triggers

| Emotion | How It's Triggered |
|---------|-------------------|
| {emotion} | {specific moment or element} |

## Target Audience Signals

- **Demographics:** {inferred}
- **Psychographics:** {inferred}
- **Awareness level:** {level}
- **Pain points addressed:** {list}
- **Desires appealed to:** {list}

## CTA Analysis

- **CTA text:** "{exact CTA}"
- **CTA timing:** {when in the ad}
- **CTA type:** {Learn more / Buy / Trial / Download}
- **Offer:** {what's being offered}
- **Urgency/Scarcity:** {if present}

## What Makes This Ad Work (or Not)

### Strengths
1. {Strength with explanation}
2. {Strength}

### Weaknesses
1. {Weakness with explanation}
2. {Weakness}

## Replicable Patterns

{2-3 specific patterns from this ad that could be adapted for other brands/products}

## Suggested Variations to Test

1. **{Variation}** — {What to change and why}
2. **{Variation}** — {What to change and why}
3. **{Variation}** — {What to change and why}
```

## Batch Analysis

When analyzing multiple ads (e.g., a competitor's ad library):

```markdown
# Ad Creative Audit: {Brand}

**Ads analyzed:** {count}
**Platforms:** {list}
**Date range:** {period}

## Patterns Across All Ads

### Most Common Hooks
1. {Hook pattern} — used in {X}% of ads
2. {Hook pattern} — used in {X}%

### Dominant Persuasion Tactics
1. {Tactic} — {frequency}
2. {Tactic} — {frequency}

### Audience Targeting Patterns
- {Pattern}

### Creative Formats
| Format | Count | Performance Signals |
|--------|-------|-------------------|

## Top 3 Ads (by estimated performance)

{Analysis of each}

## Recommendations for Your Ads
1. {Recommendation based on patterns observed}
2. {Recommendation}
3. {Recommendation}
```

## Important Notes

- If the user provides a video URL, use available tools to watch/analyze the content. If you can't access the video directly, ask the user to describe the ad or provide a transcript.
- Focus on what's replicable and actionable, not just descriptive.
- Good ad analysis identifies WHY something works, not just WHAT happens.
- Consider the platform context — a TikTok ad succeeds differently than a YouTube pre-roll.
- Meta Ad Library (facebook.com/ads/library) is free and public — use it to find competitor ads.
