---
name: sablier-writing
description: This skill should be used when writing content for Sablier, including "write a blog post", "create a case study", "draft a tweet", "write X/Twitter posts", "write an announcement", "create educational content", or any marketing content task for Sablier's brand.
---

# Writing Skill

Create written content that represents the Sablier brand—informative, confident, and focused on real value rather than
hype. This skill covers blog posts, case studies, and X/Twitter content.

## Before Writing Any Content

Load shared brand references from the skill's `references/` directory:

1. **Read** `./references/BRAND_VOICE.md` — Sablier's voice and style
2. **Read** `./references/COMPANY_PROFILE.md` — products, metrics, positioning
3. **Read** `./references/ICP.md` — who the audience is
4. **Reference** `./references/VOICE_EXAMPLES.md` — past content for consistency
5. **Fetch docs if needed** — use `https://docs.sablier.com/llms.txt` for product details

## Content Types

### Blog Posts

For long-form content: product announcements, educational articles, comparisons, technical deep dives.

**Load detailed guidance:** `./references/BLOG_POSTS.md`

**Quick reference for post types:**

| Type                 | Length     | Purpose                          |
| -------------------- | ---------- | -------------------------------- |
| Product Announcement | 800-1500w  | Introduce new features/products  |
| Educational          | 1000-2500w | Teach concepts, best practices   |
| Case Study           | 600-1000w  | Customer success stories         |
| Comparison           | 1000-2000w | Compare approaches/solutions     |
| Technical Deep Dive  | 1500-3000w | Developer-focused technical docs |

### Case Studies

For customer success stories documenting how organizations use Sablier.

**Load detailed guidance:** `./references/CASE_STUDIES.md`

**Standard structure:**

1. About [Customer] — 2-3 sentences
2. The Challenge — what problem, why it mattered
3. The Solution — why Sablier, how implemented
4. The Results — quantifiable outcomes
5. Customer Quote — direct quote if available
6. Key Takeaway — one actionable insight

### X/Twitter Posts

For social media content: announcements, educational threads, social proof, hot takes.

**Load detailed guidance:** `./references/X_TWITTER.md`

**Post type quick reference:**

| Type              | Structure                                |
| ----------------- | ---------------------------------------- |
| Announcement      | News → benefit → link                    |
| Educational       | Problem → explanation → Sablier approach |
| Social Proof      | Metric → context → positioning           |
| Case Study Teaser | Customer + outcome → quote → link        |
| Hot Take          | Position → reasoning → call to action    |

## Voice Principles

Maintain these across all content:

- **Confident, not arrogant** — Let data and track record speak
- **Educational first** — Provide value even without Sablier
- **Direct** — Get to the point, don't pad
- **Technical but accessible** — Explain jargon, use examples
- **Customer-centric** — Their story, not ours

## Proof Points

Weave in when relevant:

- 6+ years without hacks
- 530,000+ streams created
- Major customers: Ethena, Uniswap DAO, Fluid, Maple, Immutable
- Low, predictable fees
- Multiple audits
- Operating since 2019

**Good example:**

```text
Sablier has been running on mainnet since 2019 without any security incidents—a track record
that matters when you're distributing millions in tokens.
```

**Bad example:**

```text
Sablier is the best and most secure platform!!!
```

## What to Avoid

Across all content:

- "We're excited to announce..." — Lead with the news
- Hype words (revolutionary, game-changing, LFG)
- Vague claims ("great results", "significant improvement")
- Making it about Sablier instead of the reader/customer
- Feature lists without benefits — Always include "so what"
- Wall of text — Use headers, lists, short paragraphs
- Engagement bait ("RT if you agree")
- Excessive emoji

## Quality Checklist

Before publishing any content:

- [ ] Does it provide value even without Sablier mentions?
- [ ] Are claims supported with specific data or examples?
- [ ] Is it scannable (headers, lists, short paragraphs)?
- [ ] Is voice consistent with brand guidelines?
- [ ] Are CTAs clear and appropriate (not pushy)?
- [ ] Does it sound like Sablier, not generic crypto marketing?

## Reference Files

All references are located in the `./references/` directory:

### Brand References

- **`./references/BRAND_VOICE.md`** — Voice and style guidelines
- **`./references/COMPANY_PROFILE.md`** — Products, metrics, positioning
- **`./references/ICP.md`** — Ideal customer profile
- **`./references/VOICE_EXAMPLES.md`** — Past content examples

### Content-Type Specific References

- **`./references/BLOG_POSTS.md`** — Detailed blog post templates and guidelines
- **`./references/CASE_STUDIES.md`** — Case study structure and examples
- **`./references/X_TWITTER.md`** — X/Twitter post formats and examples

Load the appropriate content-type reference when writing that specific format.
