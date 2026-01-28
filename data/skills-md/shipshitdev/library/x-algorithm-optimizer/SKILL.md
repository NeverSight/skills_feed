---
name: x-algorithm-optimizer
description: Optimize X/Twitter content for algorithm engagement signals. Based on xai-org/x-algorithm's Grok transformer model that predicts 15 user-specific engagement signals. Activates for tweet optimization, thread strategy, X growth, or algorithm-aligned content.
version: 1.0.0
tags:
  - twitter
  - x
  - algorithm
  - engagement
  - growth
  - social-media
  - content-optimization
auto_activate: true
---

# X Algorithm Optimizer

Optimize content for X's algorithm based on actual engagement signal prediction (from xai-org/x-algorithm).

**Core Insight:** X's algorithm uses Grok-based transformers to predict 15 user-specific engagement signals. It optimizes for user relevance, not broad popularity.

## When This Activates

- User asks to optimize tweets for X algorithm
- User wants to improve X/Twitter engagement
- User asks about thread strategy
- User mentions X growth or algorithm optimization
- User wants to maximize reach or engagement on X

## The 15 Engagement Signals

X's algorithm predicts these signals per-user:

### Positive Signals (Maximize)

| Signal | Weight | Optimization Strategy |
|--------|--------|----------------------|
| **Favorites** | High | Relatable insights, contrarian takes, save-worthy content |
| **Replies** | Very High | Questions, open loops, controversial hooks |
| **Reposts** | Very High | Frameworks, data, templates, quotable insights |
| **Quotes** | High | Hot takes people want to add to |
| **Shares** | High | Actionable value, resources, tools |
| **Profile Clicks** | High | Credibility signals, mysterious bio hooks |
| **Video Views** | Medium | Hook in first 3s, text overlay, no slow intros |
| **Photo Expansions** | Medium | Intriguing cropped previews, charts, screenshots |
| **Dwell Time** | Very High | Long-form hooks, formatting, open loops |
| **Follows** | Very High | Consistent niche value, credibility proof |

### Negative Signals (Minimize)

| Signal | Trigger | Avoidance Strategy |
|--------|---------|-------------------|
| **Not Interested** | Irrelevant content | Stay on-niche, clear topic signals |
| **Blocks** | Aggressive/spam behavior | No mass mentions, no DM spam |
| **Mutes** | Posting frequency overload | Space out content, quality > quantity |
| **Reports** | Policy violations | Clean content, no engagement bait |

## Hook Formulas (Maximize Dwell Time)

Dwell time is critical. Stop the scroll with these patterns:

### The Contrarian Hook

```
Most people think [common belief].

They're wrong.

Here's why:
```

### The Credibility Hook

```
I've [impressive credential].

Here's what I learned:
```

### The Data Hook

```
[Surprising statistic].

That's [comparison that makes it shocking].
```

### The Story Hook

```
In [year], I was [relatable situation].

[Unexpected outcome] changed everything.
```

### The Question Hook

```
Why do [successful people] always [behavior]?

I studied [number] of them. Here's the pattern:
```

### The Scarcity Hook

```
[Number]% of people will never know this.

[Valuable insight]:
```

## Reply Triggers (Maximize Replies)

Replies signal high engagement value to the algorithm.

### Open-Ended Questions

- "What would you add to this?"
- "Unpopular opinion: [take]. Agree or disagree?"
- "What's stopping you from [desired outcome]?"

### Controversial Takes (Use Sparingly)

- Challenge industry assumptions
- Disagree with popular figures (respectfully)
- Reframe common advice

### Engagement Prompts

- "Reply '[keyword]' if you want [resource]"
- "Tag someone who needs to see this"
- "What's your biggest challenge with [topic]?"

### Open Loops

End tweets without full resolution:

- "The real reason? I'll share in the thread below."
- "But that's not the interesting part..."
- "Here's what nobody talks about:"

## Repost Patterns (Maximize Reposts)

Content people save and share:

### Frameworks

```
The [Name] Framework for [Outcome]:

1. [Step with benefit]
2. [Step with benefit]
3. [Step with benefit]

Steal this.
```

### Templates

```
Here's the exact [template/script/email] I used to [outcome]:

[Template]

Copy and use it.
```

### Data/Stats

```
I analyzed [number] [things].

Here's what the data shows:

[Insight 1]
[Insight 2]
[Insight 3]

Bookmark this.
```

### Resource Lists

```
[Number] [tools/resources/tips] that [benefit]:

1. [Name] - [1-line description]
2. [Name] - [1-line description]
...

Save for later.
```

## Thread Architecture

Threads cascade engagement across tweets.

### Structure

```
Tweet 1 (Hook): Stop the scroll, promise value
Tweet 2-6 (Body): Deliver value, one point per tweet
Tweet 7 (CTA): Follow, engage, or take action
```

### Thread Rules

1. Each tweet must stand alone (algorithm scores individually)
2. Use "Thread" or number notation (1/7)
3. End each tweet with curiosity for the next
4. Put best content in tweets 2-3 (highest visibility)
5. Include bookmarkable value (images, lists, frameworks)

### Thread Hook Formula

```
I [credibility signal].

Here's [what I learned / my framework / the breakdown]:

(Thread)
```

## Signal-Specific Optimization

### Maximize Favorites

- Relatable struggles + insights
- "Finally someone said it" content
- Save-worthy resources
- Contrarian takes with evidence

### Maximize Profile Clicks

- Hint at more value in bio
- Demonstrate niche expertise
- Create curiosity about background
- Strong credibility signals in content

### Maximize Dwell Time

- Long-form formatting (line breaks)
- Numbered lists
- Multiple scroll-stopping sections
- Strategic use of images/video

### Minimize Negative Signals

- Stay consistent with niche
- Don't post more than 3-5x/day
- Avoid engagement bait ("Like if you agree")
- No mass tagging or DM spam

## Algorithm Mechanics

### Author Diversity

The algorithm attenuates repeated creators in feeds. Implications:

- Getting retweeted by diverse accounts > one mega account
- Build relationships with different communities
- Cross-pollination beats concentrated reach

### User-Specific Relevance

Content is scored per-user, not globally. Implications:

- Target your specific audience's interests
- Build engagement patterns with your followers
- Consistency matters more than virality

### No Hand-Engineered Features

The model is pure ML prediction. Implications:

- Gaming specific metrics doesn't work long-term
- Focus on genuine engagement quality
- Create content people actually want to engage with

## Timing Guidance

| Audience Type | Best Times | Why |
|--------------|------------|-----|
| B2B/Tech | 8-10am, 12-1pm EST | Work hours, lunch breaks |
| B2C/Lifestyle | 7-9am, 7-10pm EST | Before/after work |
| Global | Varies | Test and measure |

**Note:** Timing matters less than content quality. A great tweet at 2am beats a mediocre tweet at peak time.

## Quick Optimization Checklist

- [ ] Hook stops the scroll in first line
- [ ] Content delivers specific value
- [ ] At least one engagement trigger (question, CTA)
- [ ] Formatted for dwell time (line breaks, lists)
- [ ] On-niche to avoid "not interested" signals
- [ ] No engagement bait or spam patterns
- [ ] Clear credibility signals where relevant

## Integration

| Skill | When to Use |
|-------|-------------|
| `content-creator` | Generate tweet/thread content |
| `copywriter` | Brand voice consistency |
| `prompt-engineer` | Content generation prompts |
| `youtube-video-analyst` | Apply hook patterns from video |

---

**For detailed signal tactics and examples:** `references/engagement-signals.md`
