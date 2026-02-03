---
name: intel
description: Market intelligence in seconds. Research gaps, competitors, sentiment, pricing, trends, and pain points for any market or product. For builders who need business decisions, not just information.
argument-hint: "[mode] [topic]" — modes: gaps, competitors, sentiment, pricing, trends, pain, full
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: WebSearch, Read, Write, AskUserQuestion
---

# /intel — Market Intelligence in Seconds

Research any market, competitor, or product. Get actionable business intelligence with evidence.

## Quick Start Examples
```
/intel gaps AI video editing
/intel competitors Notion
/intel sentiment Claude Code
/intel pricing email marketing SaaS
/intel trends no-code 2026
/intel pain project management
/intel full personal finance apps
```

---

## Step 1: Parse Input

Parse the user's input: `/intel [MODE] [TOPIC]`

**MODES:**
| Mode | Purpose |
|------|---------|
| `gaps` | Find market gaps and unmet needs |
| `competitors` | Map competitive landscape |
| `sentiment` | Quantify love/hate ratio |
| `pricing` | Research pricing strategies |
| `trends` | Analyze direction and velocity |
| `pain` | Find top frustrations |
| `validate` | Quick idea validation (gaps + competitors + pain combined) |
| `full` | Complete report (all modes) |

**If no mode specified**, default to `full`.

**Store:**
- `MODE = [extracted mode]`
- `TOPIC = [extracted topic]`

---

## Step 2: Execute Searches

Run **5-8 searches per mode**. Keep queries SIMPLE — complex boolean often fails.

### Search Templates by Mode

**GAPS MODE** — Find unmet needs:
```
Search 1: {TOPIC} "I wish" site:reddit.com
Search 2: {TOPIC} frustrating OR annoying site:reddit.com  
Search 3: {TOPIC} "would pay for" site:reddit.com
Search 4: {TOPIC} feature request site:news.ycombinator.com
Search 5: {TOPIC} problems complaints 2025 2026
Search 6: {TOPIC} missing features gaps
```

**COMPETITORS MODE** — Map landscape:
```
Search 1: {TOPIC} vs alternative site:reddit.com
Search 2: {TOPIC} competitors comparison 2026
Search 3: best {TOPIC} alternatives
Search 4: {TOPIC} review site:producthunt.com
Search 5: {TOPIC} pricing plans comparison
Search 6: "switched from" {TOPIC} to site:reddit.com
```

**SENTIMENT MODE** — Quantify opinions:
```
Search 1: {TOPIC} love OR amazing site:reddit.com
Search 2: {TOPIC} hate OR terrible site:reddit.com
Search 3: {TOPIC} honest review 2025 2026
Search 4: {TOPIC} worth it site:reddit.com
Search 5: {TOPIC} overrated OR underrated
Search 6: {TOPIC} complaints site:twitter.com
```

**PRICING MODE** — Research pricing:
```
Search 1: {TOPIC} pricing cost 2026
Search 2: {TOPIC} free tier freemium
Search 3: {TOPIC} expensive OR cheap site:reddit.com
Search 4: {TOPIC} pricing comparison
Search 5: {TOPIC} "how much does" cost
Search 6: {TOPIC} pricing strategy SaaS
```

**TRENDS MODE** — Analyze direction:
```
Search 1: {TOPIC} trending growing 2026
Search 2: {TOPIC} declining dying site:reddit.com
Search 3: {TOPIC} future prediction 2026
Search 4: {TOPIC} news announcement 2026
Search 5: {TOPIC} hype OR bubble
Search 6: {TOPIC} market size growth
```

**PAIN MODE** — Find frustrations:
```
Search 1: {TOPIC} frustrating painful site:reddit.com
Search 2: {TOPIC} biggest problem site:reddit.com
Search 3: {TOPIC} workaround hack site:reddit.com
Search 4: {TOPIC} rant vent site:reddit.com
Search 5: {TOPIC} broken buggy unreliable
Search 6: {TOPIC} complaints issues 2026
```

**VALIDATE MODE** — Quick idea validation (run in sequence):
```
# Pain check
Search 1: {TOPIC} frustrating problem site:reddit.com
Search 2: {TOPIC} "I wish" OR "would pay for" site:reddit.com
# Competition check  
Search 3: {TOPIC} vs alternatives comparison
Search 4: best {TOPIC} tools 2026
# Gap check
Search 5: {TOPIC} missing features gaps complaints
Search 6: {TOPIC} "doesn't exist" OR "no good" site:reddit.com
```

**FULL MODE** — Run 2-3 searches from EACH mode above.

---

## Step 3: Extract & Synthesize

For each result, extract:
- **Source URL** (required)
- **Platform** (Reddit, HN, Twitter, blog)
- **Key quote** (most relevant 1-2 sentences)
- **Engagement hint** (if URL contains /comments/ or shows votes in snippet)

### Weighting Rules
1. **Reddit/HN** → Highest weight (real discussions)
2. **Twitter/X** → High (real-time sentiment)
3. **Product Hunt** → Medium (launch feedback)
4. **Blogs** → Medium (detailed but may be biased)
5. **Company sites** → Lowest (facts only, not opinions)

### Pattern Detection
- What appears in **3+ sources**? → Strong signal
- What has **engagement hints** (comments, upvotes mentioned)? → Validated
- **Contradictions** between sources? → Note them
- **Data gaps**? → Acknowledge low confidence

---

## Step 4: Output Format

**CRITICAL: Follow this exact format.**

```markdown
## /intel {MODE}: {TOPIC}

### TL;DR
[One paragraph — THE key insight a founder needs. Be specific. Be actionable.]

### Key Findings

**1. [Finding title]**
[2-3 sentences with SPECIFIC evidence]
> "[Direct quote from source]" — [Source: platform/url]

**2. [Finding title]**  
[2-3 sentences with evidence]
> "[Direct quote]" — [Source]

**3. [Finding title]**
[Evidence and quotes]

[3-5 findings total]

### Data Summary

| Metric | Value | Notes |
|--------|-------|-------|
| Sources analyzed | {n} | Reddit: {n}, HN: {n}, Other: {n} |
| Strong signals | {n} | Appeared in 3+ sources |
| Confidence | {HIGH/MED/LOW} | Based on source quality |

{MODE-SPECIFIC SECTION — see below}

### Strategic Implications

**If building in this space:**
- [Specific advice for founders/builders]

**If investing/evaluating:**
- [Specific advice for investors/analysts]

**Contrarian take:**
- [What the data might be missing or getting wrong]

### Confidence Breakdown

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Source diversity | {1-10} | {n} independent sources |
| Data recency | {1-10} | {%} from last 90 days |
| Signal strength | {1-10} | {n} findings in 3+ sources |
| **Overall** | **{1-10}** | |

### Limitations & Blind Spots
- [Data gaps — what's NOT represented]
- [Bias warnings — who's overrepresented]
- [Recency issues — old data flagged]

---
📊 /intel {MODE} complete
├─ Topic: {TOPIC}
├─ Sources: {n} total
└─ Confidence: {HIGH/MED/LOW}

Want deeper analysis? Ask about any finding.
```

---

## Mode-Specific Sections

### GAPS Mode Output
```markdown
### Market Opportunities

| Rank | Gap | Signal Strength | Evidence |
|------|-----|-----------------|----------|
| 1 | [Gap description] | {n} mentions | "[quote]" |
| 2 | [Gap] | {n} mentions | "[quote]" |
| 3 | [Gap] | {n} mentions | "[quote]" |

### Recommended Action
[1-2 sentences: Which gap to pursue and why]
```

### COMPETITORS Mode Output
```markdown
### Competitive Landscape

| Competitor | Positioning | Mentioned | Sentiment |
|------------|-------------|-----------|-----------|
| [Name] | [1-line] | {n}x | 👍/👎/😐 |
| [Name] | [1-line] | {n}x | 👍/👎/😐 |

### Positioning Gap
[Where is there room in the market?]
```

### SENTIMENT Mode Output
```markdown
### Sentiment Analysis

**Score: {1-10}/10** (estimated from {n} sources)

| Aspect | Positive | Negative |
|--------|----------|----------|
| [Aspect 1] | {n} mentions | {n} mentions |
| [Aspect 2] | {n} | {n} |

**Most Loved:** [Feature] — "[quote]"
**Most Hated:** [Feature] — "[quote]"
**Trend:** {Improving/Stable/Declining}
```

### PRICING Mode Output
```markdown
### Pricing Landscape

| Tier | Range | Model | Examples |
|------|-------|-------|----------|
| Entry | $X-Y | [model] | [products] |
| Mid | $X-Y | [model] | [products] |
| Premium | $X-Y | [model] | [products] |

**Premium Justifiers:** [What features command higher prices]
**Common Mistakes:** [Pricing errors to avoid]
```

### TRENDS Mode Output
```markdown
### Trend Analysis

**Direction:** {📈 Growing | 📊 Stable | 📉 Declining}
**Velocity:** {Rapid | Moderate | Slow}

| Signal | Evidence |
|--------|----------|
| [Trend signal] | "[quote]" |
| [Signal] | "[quote]" |

**Forecast:** [1-2 sentences on where this is heading]
```

### PAIN Mode Output
```markdown
### Pain Point Rankings

| Rank | Pain Point | Frequency | Severity |
|------|------------|-----------|----------|
| 1 | [Pain] | {n} mentions | High/Med/Low |
| 2 | [Pain] | {n} mentions | High/Med/Low |
| 3 | [Pain] | {n} mentions | High/Med/Low |
```

### VALIDATE Mode Output
Quick idea validation — combines gaps, competitors, and pain into a decision framework.
```markdown
### Idea Validation: {TOPIC}

#### 1. Is There a Real Problem? 
**Verdict:** {YES/MAYBE/NO}
- Pain points found: {n}
- Top pain: [description] — "[quote]"
- Severity: {High/Med/Low}

#### 2. Are There Existing Solutions?
**Verdict:** {CROWDED/SOME/EMPTY}
- Competitors found: {n}
- Top players: [list]
- User satisfaction: {High/Med/Low}

#### 3. Is There Room for You?
**Verdict:** {YES/MAYBE/NO}
- Gaps identified: {n}
- Biggest gap: [description]
- Differentiation opportunity: [specific angle]

### Overall Validation Score

| Criteria | Score | Notes |
|----------|-------|-------|
| Problem exists | {1-10} | |
| Market not saturated | {1-10} | |
| Clear differentiation | {1-10} | |
| **BUILD/DONT BUILD** | **{verdict}** | |

### Recommendation
[2-3 sentences: Should they build this? Why or why not? What angle?]

**Current Workarounds:** 
- [Pain 1]: People do [workaround]

**Biggest Opportunity:** [Which pain to solve first]
```

### FULL Mode Output
Include ALL sections in order:
1. TL;DR (synthesis)
2. Market Gaps
3. Competitive Landscape
4. Sentiment Overview
5. Pricing Intel
6. Trend Direction
7. Pain Points
8. Overall Recommendation

---

## Error Handling

**If search returns few/no results:**
```markdown
## /intel {MODE}: {TOPIC}

### Limited Data Available

Only {n} relevant sources found. This could mean:
- Niche/emerging topic with sparse coverage
- Try broader search terms
- Topic may not have significant online discussion

**What I found:**
[List whatever was found]

**Suggestions:**
- Try: /intel {MODE} [broader term]
- Try: /intel {MODE} [related term]
```

**If topic is ambiguous:**
Ask clarifying question before searching:
```
The topic "{TOPIC}" could mean several things:
1. [Interpretation 1]
2. [Interpretation 2]

Which should I research?
```

---

## Quality Checklist

Before outputting, verify:
- [ ] Every finding has a source URL
- [ ] Numbers are specific ("12 mentions" not "many")
- [ ] Direct quotes are actual quotes from sources
- [ ] Confidence level matches data quality
- [ ] Format matches templates exactly
- [ ] Actionable — founder can decide something

---

## Context Memory

After research, remember:
- `MODE`: {mode}
- `TOPIC`: {topic}  
- `KEY_FINDINGS`: Top 3-5 insights
- `SOURCES`: URLs you found

**You are now an expert on this topic.**

For follow-ups:
- Answer from your research (don't re-search)
- Cite the sources you found
- Offer to dive deeper on any finding

Only new research if user asks about DIFFERENT topic.

---

## Anti-Patterns to Avoid

❌ **Don't hallucinate sources** — If you didn't find it, don't cite it
❌ **Don't use vague numbers** — "Several" "Many" "Some" → Use actual counts
❌ **Don't skip the format** — Follow templates exactly
❌ **Don't over-promise** — Low data = say "low confidence"
❌ **Don't re-search on follow-ups** — Use what you already found

---

## Reference Examples

See the `examples/` folder for complete output examples:
- `examples/gaps-example.md` — AI video editing gaps analysis
- `examples/competitors-example.md` — Notion competitive landscape  
- `examples/sentiment-example.md` — Claude Code sentiment analysis

Use these as templates for consistent output formatting.

---

**/intel** — Stop guessing. Start knowing.
