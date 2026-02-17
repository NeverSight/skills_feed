---
name: lead-magnet
description: >
  Create lead magnets and gated content to capture email subscribers and leads.
  Use when asked to design checklists, templates, calculators, mini-courses,
  whitepapers, or other downloadable content offers. Trigger phrases: "lead magnet",
  "gated content", "email capture", "content offer", "free download", "checklist",
  "template", "whitepaper", "swipe file", "content upgrade", "opt-in offer".
---

# Lead Magnet Creation

Design and build lead magnets that convert visitors into email subscribers and qualified leads.

---

## 1. Lead Magnet Types

### Checklists

**Best for:** Actionable topics, step-by-step processes
**Effort to create:** Low (1-2 hours)
**Conversion rate:** High (30-50% on dedicated landing pages)

Template structure:
```
Title: The Complete [Topic] Checklist

[ ] Step 1: [Action item]
    Why: [Brief explanation]
    Tool: [Recommended tool if applicable]

[ ] Step 2: [Action item]
    ...

[ ] Step 3: [Action item]
    ...

[Continue for 10-25 items]

Bonus: [Extra tip or resource link]
```

Example titles:
- "The 47-Point Website Launch Checklist"
- "Pre-Publish Blog Post Checklist (Never Miss a Step)"
- "The Complete SEO Audit Checklist for 2025"

### Templates

**Best for:** Saving time, providing structure
**Effort to create:** Medium (2-4 hours)
**Conversion rate:** Very high (35-60%)

Types of templates:
- Spreadsheet templates (Google Sheets, Excel)
- Document templates (Google Docs, Notion)
- Design templates (Canva, Figma)
- Code templates (GitHub repos, code snippets)
- Email templates (copy-paste ready)

Template packaging:
```
[Template Name]

INSTRUCTIONS
1. Make a copy of this template (File > Make a Copy)
2. [Customization step 1]
3. [Customization step 2]

SECTIONS
- Section 1: [Purpose]
- Section 2: [Purpose]
- Section 3: [Purpose]

EXAMPLE (filled in)
[Show one complete example so users understand how to use it]
```

### Calculators / Interactive Tools

**Best for:** Quantifiable outcomes, ROI justification
**Effort to create:** High (1-2 weeks with a developer)
**Conversion rate:** Very high (40-60%)

Calculator ideas:
- ROI calculator for your product
- Cost savings estimator
- "How much are you losing?" audit tool
- Salary/pricing benchmark calculator
- Carbon footprint / impact calculator

Implementation notes:
- Can be built as a simple HTML/JS page
- Gate the results (not the calculator itself) behind email
- Show a preview of results, require email for full report
- Save results as a PDF sent to their email

### Mini-Courses (Email or Video)

**Best for:** Complex topics, building authority, nurture sequences
**Effort to create:** High (1-2 weeks)
**Conversion rate:** Medium-high (25-40%)

Structure:
```
Course: [Title] -- [X]-Day [Topic] Course

Day 1: [Foundation topic]
  - Email subject: "[Course Name] Day 1: [Topic]"
  - Content: [500-800 words or 5-10 min video]
  - Action item: [Homework]

Day 2: [Building on Day 1]
  ...

Day 3: [Advanced topic]
  ...

Day 4: [Application / case study]
  ...

Day 5: [Summary + next steps + soft pitch]
  - Recap key learnings
  - "If you want to go further, [Product] can help with..."
```

### Whitepapers / Reports

**Best for:** B2B, thought leadership, data-driven audiences
**Effort to create:** High (1-3 weeks)
**Conversion rate:** Medium (15-30%)

Structure:
```
Title: [The State of / The Complete Guide to / X Trends in] [Topic]

Executive Summary (1 page)
- Key findings
- Why this matters

Section 1: [Current State]
- Data point 1
- Data point 2
- Analysis

Section 2: [Challenges]
- Challenge 1 with data
- Challenge 2 with data

Section 3: [Solutions / Trends]
- Trend 1 with examples
- Trend 2 with examples

Section 4: [Recommendations]
- Actionable takeaways
- Implementation roadmap

Methodology (if original research)
About [Company]
```

### Swipe Files

**Best for:** Marketers, copywriters, designers
**Effort to create:** Medium (curate over time)
**Conversion rate:** High (30-50%)

Swipe file types:
- Email subject line swipe file (100+ proven subjects)
- Ad copy swipe file (best-performing ads by industry)
- Landing page swipe file (screenshots + analysis)
- Cold email swipe file (templates for outreach)
- Social media post swipe file (viral post formulas)

Structure:
```
[Swipe File Title]: [X] Proven [Type] You Can Steal

Category 1: [Theme]
  Example 1:
    Original: "[Exact copy]"
    Source: [Brand/campaign]
    Why it works: [Analysis]
    Template: "[Fill-in-the-blank version]"

  Example 2:
    ...

Category 2: [Theme]
  ...
```

---

## 2. Landing Page Structure

Every lead magnet needs a dedicated landing page optimized for conversion.

### Above the Fold

```html
<!-- Hero Section -->
<section>
  <h1>[Benefit-driven headline]</h1>
  <p>[1-2 sentence description of what they'll get and why it matters]</p>

  <!-- Lead Magnet Preview -->
  <img src="[mockup of the lead magnet]" />

  <!-- Opt-in Form -->
  <form>
    <input type="email" placeholder="Your email address" />
    <button>Download Free [Type]</button>
    <p class="privacy">No spam. Unsubscribe anytime.</p>
  </form>
</section>
```

### Below the Fold

```html
<!-- What's Inside -->
<section>
  <h2>Here's what you'll get:</h2>
  <ul>
    <li>[Specific deliverable 1]</li>
    <li>[Specific deliverable 2]</li>
    <li>[Specific deliverable 3]</li>
  </ul>
</section>

<!-- Social Proof -->
<section>
  <p>"[Testimonial about the lead magnet]" -- [Name, Title]</p>
  <p>[X] people have downloaded this [type]</p>
</section>

<!-- About the Author -->
<section>
  <h2>Created by [Name]</h2>
  <p>[1-2 sentences of credibility]</p>
</section>

<!-- FAQ -->
<section>
  <h2>Questions?</h2>
  <details>
    <summary>Is this really free?</summary>
    <p>Yes, 100% free. We just ask for your email so we can send it to you.</p>
  </details>
  <details>
    <summary>What format is it in?</summary>
    <p>[PDF / Google Sheet / Video / etc.]</p>
  </details>
</section>
```

### Headline Formulas

1. "The [Adjective] [Type] to [Desired Outcome]"
   - "The Ultimate Checklist to Launch Your Podcast"
2. "[Number] [Things] Every [Audience] Needs to [Goal]"
   - "7 Templates Every Startup Founder Needs to Raise Funding"
3. "How to [Desired Outcome] (Free [Type])"
   - "How to Double Your Email Open Rate (Free Swipe File)"
4. "Get Our [Type] That [Social Proof]"
   - "Get Our SEO Template That 10,000+ Marketers Use"
5. "Stop [Pain Point]. Download Our Free [Type]."
   - "Stop Guessing Your Pricing. Download Our Free Calculator."

---

## 3. Email Gate Setup

### Simple Email Gate (HTML + API)

```html
<form id="lead-form" action="/api/subscribe" method="POST">
  <input type="email" name="email" required placeholder="you@example.com" />
  <input type="hidden" name="lead_magnet" value="seo-checklist" />
  <button type="submit">Get Free Checklist</button>
</form>
```

### Integration Options

| Provider | Method |
|----------|--------|
| Mailchimp | Embed form or API (`POST /3.0/lists/{list_id}/members`) |
| ConvertKit | API (`POST /v3/forms/{form_id}/subscribe`) |
| Resend | API (`POST /emails` for delivery + webhook for list) |
| SendGrid | API for delivery + contacts API for list management |
| HubSpot | Forms API or embed form |

### Double Opt-In Flow

1. User submits email on landing page
2. Show "Check your email" confirmation page
3. Send confirmation email with "Confirm your email" button
4. On confirmation, redirect to download page and deliver lead magnet
5. Add to email nurture sequence

### Single Opt-In Flow (Higher Conversion)

1. User submits email on landing page
2. Immediately redirect to download/thank-you page
3. Simultaneously send email with download link (backup delivery)
4. Add to email nurture sequence

---

## 4. Delivery Automation

### Immediate Delivery Email

```
Subject: Your [Lead Magnet Name] is ready

Hi [Name],

Thanks for downloading [Lead Magnet Name]. Here's your copy:

[Download Button/Link]

A few tips to get the most out of it:
1. [Quick tip 1]
2. [Quick tip 2]
3. [Quick tip 3]

Questions? Just reply to this email.

[Signature]

P.S. If you found this helpful, you might also like [related resource].
```

### Post-Download Nurture Sequence

**Email 2 (Day 2):** "Did you get a chance to use [Lead Magnet]?"
- Quick tip or walkthrough
- Ask if they have questions

**Email 3 (Day 4):** "Here's how [Customer] used [Lead Magnet] to [Result]"
- Case study or success story
- Social proof

**Email 4 (Day 7):** "[Related valuable content]"
- Blog post, video, or additional resource
- Build authority

**Email 5 (Day 10):** "The next step after [Lead Magnet topic]"
- Introduce your product/service as the logical next step
- Soft pitch with value framing

**Email 6 (Day 14):** "[Direct offer]"
- Special offer for lead magnet downloaders
- Clear CTA to product/service
- Urgency element (limited time, limited spots)

---

## 5. Content Upgrade Strategy

A content upgrade is a lead magnet specific to an individual blog post.

### How It Works

1. Write a high-traffic blog post
2. Create a bonus resource that complements the post
3. Embed an opt-in within the post to download the bonus

### Content Upgrade Ideas by Post Type

| Post Type | Content Upgrade |
|-----------|----------------|
| How-to guide | Printable checklist of all steps |
| Listicle | Spreadsheet with all items + bonus items |
| Case study | Template to replicate the results |
| Data/research | Raw data spreadsheet or infographic |
| Tutorial | Code snippets or starter template |
| Comparison | Decision-making scorecard |

### In-Post CTA Template

```html
<div class="content-upgrade">
  <h3>Free Bonus: [Upgrade Name]</h3>
  <p>[1 sentence description]. Download it free below.</p>
  <form>
    <input type="email" placeholder="Your email" />
    <button>Send Me the [Type]</button>
  </form>
</div>
```

Place content upgrades:
- After the introduction (for skimmers)
- At the midpoint (for engaged readers)
- At the end (for completionists)

---

## 6. Lead Magnet Selection Framework

Choose the right lead magnet based on your goals:

### By Funnel Stage

| Stage | Best Lead Magnets | Goal |
|-------|------------------|------|
| Top of Funnel | Checklists, quizzes, cheat sheets | Maximum volume |
| Middle of Funnel | Templates, calculators, webinars | Qualification |
| Bottom of Funnel | Free trials, demos, consultations | Conversion |

### By Audience Type

| Audience | Best Formats |
|----------|-------------|
| Time-poor executives | 1-page cheat sheets, executive summaries |
| Hands-on practitioners | Templates, tools, code snippets |
| Data-driven analysts | Reports, benchmarks, calculators |
| Visual learners | Infographics, video courses |
| Beginners | Step-by-step guides, glossaries |

### By Budget

| Budget | Lead Magnet Options |
|--------|-------------------|
| $0 | Checklists, cheat sheets, email courses (text only) |
| $100-500 | Designed PDFs, simple calculators, slide decks |
| $500-2000 | Video courses, interactive tools, original research |
| $2000+ | Software tools, comprehensive platforms, multi-format |

---

## 7. Conversion Benchmarks

| Landing Page Type | Expected Conversion Rate |
|-------------------|------------------------|
| Dedicated lead magnet page | 30-50% |
| Content upgrade (in-post) | 5-15% |
| Sidebar widget | 1-3% |
| Exit-intent popup | 3-8% |
| Homepage email capture | 1-5% |
| Webinar registration | 20-40% |

### Optimization Levers

1. **Headline**: Test benefit-driven vs curiosity-driven
2. **Form fields**: Email-only vs email + name (fewer fields = higher conversion)
3. **CTA button text**: "Download" vs "Get Instant Access" vs "Send Me the [Type]"
4. **Social proof**: Add download count or testimonial
5. **Preview**: Show a mockup/preview of the lead magnet
6. **Urgency**: "Limited time" or "Updated for [current year]"
