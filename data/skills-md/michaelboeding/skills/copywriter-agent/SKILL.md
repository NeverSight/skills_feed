---
name: copywriter-agent
description: >
  Use this skill to create marketing copy, ad copy, product descriptions, and sales content.
  Triggers: "write copy", "marketing copy", "ad copy", "product description", "sales page",
  "landing page copy", "email copy", "tagline", "headline", "slogan", "brand copy",
  "website copy", "social copy", "campaign copy"
  Outputs: Copy variations, headlines, body copy, CTAs across multiple formats.
---

# Copywriter Agent

Create compelling marketing copy for products, brands, and campaigns.

**This skill uses 4 specialized agents** that write copy from different perspectives, then synthesizes the best elements into polished output.

## What It Produces

| Output | Description |
|--------|-------------|
| **Headlines** | Multiple headline variations (10+) |
| **Body Copy** | Long-form and short-form versions |
| **Ad Copy** | Platform-specific ad variations |
| **CTAs** | Call-to-action variations |
| **Full Package** | Complete copy kit for campaigns |

## Prerequisites

- No API keys required
- Works better with brand profile (use `brand-research-agent` first)

## Workflow

### Step 1: Gather Copy Brief (REQUIRED)

⚠️ **DO NOT skip this step. Use interactive questioning — ask ONE question at a time.**

#### Question Flow

⚠️ **Use the `AskUserQuestion` tool for each question below.** Do not just print questions in your response — use the tool to create interactive prompts with the options shown.

**Q1: Product**
> "I'll write compelling copy for you! First — **what's the product or service?**
> 
> *(What are you promoting?)*"

*Wait for response.*

**Q2: Audience**
> "Who's the **target audience**?
> 
> *(Describe your ideal customer)*"

*Wait for response.*

**Q3: Goal**
> "What's the **goal** of this copy?
> 
> - Brand awareness
> - Clicks/traffic
> - Sales/conversions
> - Signups/leads
> - Or describe"

*Wait for response.*

**Q4: Message**
> "What's the **key message** or value proposition?
> 
> *(The main benefit you want to communicate)*"

*Wait for response.*

**Q5: Format**
> "What **format(s)** do you need?
> 
> - Headlines
> - Ad copy (Facebook, Google, etc.)
> - Email copy
> - Landing page
> - Product descriptions
> - All of the above
> - Or specify"

*Wait for response.*

**Q6: Voice**
> "Do you have **brand voice guidelines**?
> 
> - Yes (describe or share)
> - No — I can run brand-research first
> - No — just use best practices"

*Wait for response.*

#### Quick Reference

| Question | Determines |
|----------|------------|
| Product | What we're writing about |
| Audience | Tone and messaging approach |
| Goal | CTA and persuasion strategy |
| Message | Core theme across all copy |
| Format | Which copy types to generate |
| Voice | Style and tone guidelines |

---

### Step 2: Run Specialized Copywriting Agents in Parallel

Deploy 4 agents, each writing from a different angle:

#### Agent 1: Headlines Writer
Focus: Attention-grabbing headlines and hooks
```
Write:
- Benefit-driven headlines
- Curiosity-driven headlines
- Problem-agitation headlines
- Social proof headlines
- Urgency headlines
- Question headlines
- "How to" headlines
- Number/list headlines
```

#### Agent 2: Body Copy Writer
Focus: Persuasive long-form copy
```
Write:
- Opening hooks
- Problem agitation
- Solution presentation
- Benefit bullets
- Proof/credibility
- Objection handling
- Emotional appeals
- Logical arguments
```

#### Agent 3: Ad Copy Writer
Focus: Platform-specific short-form ads
```
Write for:
- Facebook/Instagram ads
- Google Search ads
- LinkedIn ads
- TikTok/Reels captions
- Twitter/X posts
- YouTube ad scripts
```

#### Agent 4: CTA Specialist
Focus: Conversion-focused calls to action
```
Write:
- Button text variations
- Link text variations
- Urgency CTAs
- Value-focused CTAs
- Low-commitment CTAs
- High-commitment CTAs
```

---

### Step 3: Synthesize into Copy Package

Combine the best elements into a structured package:

```json
{
  "project": {
    "product": "Product/Service name",
    "audience": "Target audience",
    "goal": "Campaign goal",
    "key_message": "Core value proposition"
  },
  "headlines": {
    "primary": "Best headline for main use",
    "variations": [
      {"headline": "Headline 1", "type": "benefit"},
      {"headline": "Headline 2", "type": "curiosity"},
      {"headline": "Headline 3", "type": "problem"},
      {"headline": "Headline 4", "type": "social-proof"},
      {"headline": "Headline 5", "type": "urgency"}
    ]
  },
  "taglines": [
    "Short memorable phrase 1",
    "Short memorable phrase 2",
    "Short memorable phrase 3"
  ],
  "body_copy": {
    "long_form": {
      "hook": "Opening paragraph that grabs attention...",
      "problem": "Paragraph agitating the problem...",
      "solution": "Paragraph presenting the solution...",
      "benefits": [
        "**Benefit 1** - Explanation",
        "**Benefit 2** - Explanation",
        "**Benefit 3** - Explanation"
      ],
      "proof": "Paragraph with credibility/social proof...",
      "cta": "Closing paragraph with call to action..."
    },
    "short_form": "Concise version for limited space (100 words)...",
    "micro_copy": "Ultra-short version (25 words)..."
  },
  "ad_copy": {
    "facebook": {
      "primary_text": "Main ad copy...",
      "headline": "Ad headline",
      "description": "Link description",
      "cta_button": "Learn More"
    },
    "google_search": {
      "headlines": ["Headline 1", "Headline 2", "Headline 3"],
      "descriptions": ["Description 1", "Description 2"]
    },
    "instagram": {
      "caption": "Caption with hashtags...",
      "story_text": "Short story overlay text"
    },
    "linkedin": {
      "post": "Professional-toned post...",
      "ad": "LinkedIn ad copy..."
    }
  },
  "ctas": {
    "primary": "Get Started Free",
    "variations": [
      "Start Your Free Trial",
      "See How It Works",
      "Try It Now",
      "Get Instant Access",
      "Book a Demo"
    ]
  },
  "email_subject_lines": [
    "Subject line 1",
    "Subject line 2",
    "Subject line 3"
  ]
}
```

---

### Step 4: Deliver and Iterate

**Delivery message:**

"✅ Copy package complete!

**Project:** [Product] - [Goal]
**Audience:** [Target]

**Top Headlines:**
1. [Best headline]
2. [Second best]
3. [Third best]

**Primary Tagline:** [Tagline]

**Ready for:**
- Landing pages
- Ad campaigns
- Email marketing
- Social media

**Want me to:**
- Generate more headline variations?
- Write full landing page copy?
- Adapt for specific platform?
- A/B test variations?
- Match specific brand voice?"

---

## Copy Frameworks Used

The agents apply proven copywriting frameworks:

| Framework | Use |
|-----------|-----|
| **AIDA** | Attention, Interest, Desire, Action |
| **PAS** | Problem, Agitate, Solution |
| **BAB** | Before, After, Bridge |
| **4Ps** | Picture, Promise, Prove, Push |
| **FOMO** | Fear of Missing Out |
| **Social Proof** | Testimonials, numbers, logos |

---

## Integration with Other Agents

| Agent | Use Case |
|-------|----------|
| `brand-research-agent` | Match brand voice/tone |
| `image-generation` | Create visuals for ads |
| `video-producer-agent` | Write video scripts |
| `social-producer-agent` | Create social content |

---

## Agents

| Agent | File | Focus |
|-------|------|-------|
| Headlines Writer | `headlines-writer.md` | Headlines, hooks |
| Body Copy Writer | `body-copy-writer.md` | Long-form copy |
| Ad Copy Writer | `ad-copy-writer.md` | Platform ads |
| CTA Specialist | `cta-specialist.md` | Calls to action |

---

## Example Prompts

**Product launch:**
> "Write copy for our new fitness app that helps busy professionals work out at home"

**Ad campaign:**
> "Create Facebook ad copy for our Black Friday sale - 50% off all products"

**Landing page:**
> "Write landing page copy for our B2B SaaS that automates invoicing"

**Rebrand:**
> "We're rebranding from corporate to friendly. Rewrite our website copy"

**Specific format:**
> "Write 10 email subject lines for our abandoned cart sequence"
