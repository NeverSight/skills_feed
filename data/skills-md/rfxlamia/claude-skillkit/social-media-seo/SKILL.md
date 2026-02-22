---
name: social-media-seo
description: >
  Optimize social media content for maximum discoverability and engagement using 2025-proven SEO strategies. 
  Includes comprehensive CSV databases with 100+ caption formulas, thread structures, viral patterns, and 
  platform-specific optimization playbooks for Instagram, X/Twitter, and Threads. Works with seo-manager 
  subagent for intelligent content generation.
---

# Social Media SEO (2025)

Transform social media posts into discoverable, engaging content using research-backed SEO strategies and extensive formula databases.

## What This Skill Solves

**The 2025 Social Media Landscape Problem:**
- Instagram pivoted from hashtag-based discovery to **keyword-based SEO** (Google/Bing now index captions)
- X/Twitter prioritizes first 100 characters for search visibility
- Generic content gets lost (zero-click searches at 60%, users find answers on platform)
- 70% of Gen Z use TikTok/Instagram as primary search engines, not Google

**This skill provides:**
1. **Platform-specific optimization playbooks** (Instagram, X/Twitter, Threads)
2. **CSV databases** with 100+ proven formulas (captions, threads, hooks, viral patterns)
3. **Data-driven selection** (includes avg_engagement, conversion_rate metrics)
4. **Non-monotonous variety** (dozens of styles instead of static templates)

## When to Use This Skill

**Trigger patterns:**
- "Optimize my Instagram caption for SEO"
- "Create viral Twitter thread structure"
- "Best hashtag strategy for [platform]"
- "Write engaging social media post about [topic]"
- "Improve discoverability on [platform]"
- "Generate multiple caption variations"

**Use with seo-manager subagent** for intelligent querying of databases and customized recommendations.

## Core Methodology

### 2025 Social Media SEO Principles

**1. Keyword-First Approach** (Instagram/Threads)
- 3-5 highly relevant hashtags (not 30)
- Keywords in first 15 characters of caption
- Alt text optimization for Google/Bing indexing
- Profile optimization (name, username, bio)

**2. First-100-Characters Rule** (X/Twitter)
- Critical keywords front-loaded
- Hook formula in opening
- Bio optimization (160 chars with primary keyword)
- Thread architecture matters

**3. E-E-A-T for Social** (All Platforms)
- Experience: Show, don't tell
- Expertise: Cite sources, use data
- Authoritativeness: Consistent expertise
- Trust: Authentic voice, no manipulation

**4. Viral + SEO Integration**
- Emotion (surprise/joy/curiosity) + Keywords
- Relatability + Search intent
- Utility/Shareability + Semantic optimization
- Timeliness + Trending keywords

### Platform-Specific Optimizations

**Instagram (Keyword-Based Discovery)**
- Caption keywords > Hashtags (2025 shift)
- Alt text = Google/Bing SEO opportunity
- Reel optimization: 30-90 sec, on-screen text, captions
- Name field searchable (not just username)

**X/Twitter (Real-Time Relevance)**
- Thread first tweet = hook + keywords (first 50 chars)
- Engagement drives distribution (replies > retweets > likes)
- Bio formula: [Who] + [What] + [Keyword]
- Fresh content boosted (post timing matters)

**Threads (Meta's Discovery Algorithm)**
- Cross-promotion with Instagram
- Topic clarity (last 9-12 posts influence categorization)
- Connected reach (existing followers) vs Unconnected reach (discovery)

## How to Use The Databases

This skill includes **7 CSV databases** with proven formulas:

### Database Structure

```csv
# Example: caption-styles.csv
num,platform,style_name,goal,structure,example,avg_engagement,character_count,keyword_placement
1,instagram,Educational Hook,"teach + engage","[Question] + [Answer] + [CTA]","Did you know...",8.2%,145,"first 15 chars"
```

### Querying Pattern

**Manual Search:**
1. Open relevant CSV (e.g., `databases/caption-styles.csv`)
2. Filter by: platform, goal, avg_engagement threshold
3. Select 2-3 matching formulas
4. Adapt structure to your content

**With seo-manager subagent:**
```
User: "Instagram caption for educational content, high engagement"
→ Subagent queries: platform=instagram, goal=teach, avg_engagement>8%
→ Returns: Top 3 formulas with reasoning
→ Generates: 3 customized variations
```

### Available Databases (P0-P2)

**P0 (Core):**
- `caption-styles.csv` - 30+ caption formulas by platform/goal
- `hook-formulas.csv` - 25+ first-3-second hooks

**P1 (Advanced):**
- `thread-structures.csv` - 25+ thread architectures
- `hashtag-strategies.csv` - 20+ platform-specific strategies
- `viral-patterns.csv` - 20+ proven viral triggers

**P2 (Intelligence):**
- `engagement-tactics.csv` - 15+ CTA formulas
- `keyword-clusters.csv` - 10+ semantic keyword groups

## Quick Start Guide

### For Instagram Posts

1. **Profile optimization** (one-time):
   - Name field: Include primary keyword (e.g., "Sarah | SEO Expert")
   - Username: Relevant to niche if possible
   - Bio: 2-3 keywords naturally woven
   - Enable "Website Embeds" (Settings → Sharing)

2. **Caption creation**:
   - Query `caption-styles.csv`: filter by goal (educate/entertain/convert)
   - Front-load keyword in first 15 characters
   - Use 3-5 relevant hashtags (micro + mid + broad mix)
   - Add descriptive alt text with keywords

3. **Reel optimization**:
   - Length: 30-90 seconds (higher completion rate)
   - On-screen text: Include keywords
   - Captions: Always enable
   - Trending audio: When relevant to brand

### For X/Twitter Threads

1. **Bio optimization**:
   - Formula: `[Role/Expertise] helping [audience] with [value]`
   - Example: "SEO strategist helping creators with discoverability"
   - 160 chars, primary keyword included

2. **Thread structure**:
   - Query `thread-structures.csv`: select thread type
   - Tweet 1: Hook + keyword (first 50 chars critical)
   - Tweets 2-9: Value delivery
   - Tweet 10: Summary + CTA
   - Alt text on all images

3. **Engagement optimization**:
   - Post timing: Use analytics for audience peak
   - First hour critical (80% of viral potential decided)
   - Reply to comments within 1 hour
   - Quote-tweet relevant content

### For Threads

1. **Cross-promote with Instagram**:
   - Share Threads posts to Instagram Stories
   - Similar content themes (algorithm recognizes)
   
2. **Topic clarity**:
   - Last 9-12 posts influence categorization
   - Stay focused on niche topics
   - Avoid random off-topic posts

3. **Two-tier distribution**:
   - Connected reach: Engagement quality matters
   - Unconnected reach: Topic relevance + freshness

## Integration with seo-manager Subagent

The **seo-manager subagent** (separate file) provides intelligent orchestration:

**Capabilities:**
1. Multi-database querying (combines patterns from multiple CSVs)
2. Goal-based recommendations (awareness/engagement/conversion)
3. Platform-specific optimization
4. A/B test variation generation
5. Evidence-based reasoning (cites avg_engagement data)

**Example workflow:**
```
User: "Create Instagram post about AI tools for designers"

seo-manager:
1. Queries caption-styles.csv: platform=instagram, goal=educate
2. Queries hook-formulas.csv: emotion_trigger=curiosity
3. Queries keyword-clusters.csv: category=ai+design
4. Combines patterns into 3 variations
5. Explains: "Pattern #12 (12.1% avg engagement) + Hook #5 (curiosity gap)"
```

## Best Practices

**Content Creation:**
- ✅ Front-load keywords (first 15-50 chars depending on platform)
- ✅ Use proven formulas from databases (not guessing)
- ✅ Add alt text to EVERY image (accessibility + SEO)
- ✅ Track performance (A/B test different formulas)
- ❌ Don't keyword stuff (natural integration only)
- ❌ Don't use 30 hashtags (3-5 relevant ones better)
- ❌ Don't ignore platform-specific features

**Database Usage:**
- ✅ Filter by proven metrics (avg_engagement >7%)
- ✅ Adapt formulas to your voice (don't copy verbatim)
- ✅ Combine multiple patterns for uniqueness
- ✅ Update with your winning formulas
- ❌ Don't use every formula blindly
- ❌ Don't ignore platform column (Instagram ≠ Twitter)

**SEO Optimization:**
- ✅ Research semantic keywords (not just primary)
- ✅ Optimize for both platform search AND Google
- ✅ Build topic authority (consistent niche focus)
- ✅ Engage authentically (quality > quantity)
- ❌ Don't sacrifice readability for keywords
- ❌ Don't neglect analytics (track what works)

## Notes and Limitations

**Algorithm Changes:**
- Databases reflect 2025 best practices (Instagram Dec 2025, X/Twitter Nov 2025)
- Mark deprecated patterns when algo updates
- Add new winning formulas as discovered

**Not a Magic Bullet:**
- SEO improves discoverability, NOT quality
- Bad content with good SEO = still bad content
- Authenticity > Optimization (humans detect manipulation)

**Platform Constraints:**
- Instagram: Only public professional accounts (18+) eligible for Google indexing
- X/Twitter: Nofollow links (but still valuable for visibility)
- Threads: Young platform, SEO features evolving

**Quality Over Quantity:**
- 1 optimized post > 10 generic posts
- Sustained engagement > viral spike
- Community building > vanity metrics

## References

**Detailed Playbooks:**
- `references/instagram-seo.md` - Comprehensive Instagram optimization
- `references/x-twitter-seo.md` - X/Twitter strategies
- `references/threads-seo.md` - Threads best practices
- `references/analytics-guide.md` - What to track & optimize

**CSV Databases:**
- `databases/caption-styles.csv`
- `databases/hook-formulas.csv`
- `databases/thread-structures.csv`
- `databases/hashtag-strategies.csv`
- `databases/viral-patterns.csv`
- `databases/engagement-tactics.csv`
- `databases/keyword-clusters.csv`

**Helper Scripts:**
- `scripts/query_database.py` - Search/filter CSVs programmatically
