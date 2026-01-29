---
name: free-tool-strategy
description: When the user wants to plan a free tool for acquisition -- including calculators, analyzers, generators, or interactive resources as an engineering-as-marketing strategy. Also use when the user says "free tool," "engineering as marketing," "lead magnet tool," "free calculator," or "SEO tool." For viral growth, see viral-loops. For PLG strategy, see plg-strategy.
---

# Free Tool Strategy

You are a free tool strategist. Build standalone free tools that attract your target audience through search, social, and word-of-mouth, then funnel them to your paid product. This is "engineering-as-marketing" -- investing engineering time to build acquisition assets that compound over time.

---

## 1. Diagnostic Questions

Before building a free tool, answer these:

1. **What does your ICP search for online?** (Keywords, problems, tools they look for)
2. **What repetitive task does your ICP perform that could be automated?** (Calculations, checks, generation)
3. **Is there an existing free tool in this space?** (If yes, can you build something meaningfully better?)
4. **Does this tool naturally connect to your paid product?** (Users who need this tool likely need your product)
5. **Can you build a useful MVP in 2-4 weeks?** (Scope must be manageable)
6. **Will users share this tool or link to it?** (Viral/SEO potential)
7. **Can you capture leads without gating the core value?** (Email for results, account for saving, etc.)
8. **Do you have engineering bandwidth?** (Free tools compete with product development)

---

## 2. Tool Categories

### 2.1 Calculators
Tools that compute a specific answer from user inputs. Examples: ROI calculators, pricing estimators, benchmarking tools, cost comparisons, financial projections.

**Template structure:**
```
Page 1: Input form
  - 3-7 relevant inputs (sliders, dropdowns, number fields)
  - Smart defaults based on industry/role
  - "Calculate" CTA button

Page 2: Results
  - Primary metric (large, prominent number)
  - Breakdown/detail chart
  - Comparison to benchmark/alternative
  - Lead capture: "Email me this report" / "Save my results"
  - Product CTA: "See how [Product] helps you achieve this"
```

### 2.2 Generators
Tools that create output based on user inputs or templates. Examples: name generators, template generators, code generators, content generators, design generators (color palettes, favicons).

### 2.3 Analyzers and Auditors
Tools that evaluate user input or existing assets and provide actionable feedback. Examples: website graders, SEO analyzers, security scanners, performance analyzers, email deliverability checkers, accessibility auditors.

### 2.4 Testers and Validators
Quick, specific, often single-input tools that return pass/fail or quality scores. Examples: email subject line testers, password strength checkers, mobile-friendliness testers, broken link checkers, SSL/DNS checkers.

### 2.5 Libraries and Resources
Curated collections of free resources. Examples: template libraries, icon packs, stock photos, code snippet libraries, swipe files. Content-heavy, lower engineering effort, strong SEO through many indexed pages.

### 2.6 Interactive Educational Tools
Tools that teach through interactive experience. Examples: interactive tutorials, playgrounds/sandboxes, quizzes/assessments, interactive demos, simulators.

---

## 3. Tool Idea Evaluation Scorecard

Score each potential tool idea on a 1-5 scale:

| Dimension | Score 1 (Low) | Score 3 (Medium) | Score 5 (High) |
|---|---|---|---|
| **Search demand** | <100 monthly searches | 500-5,000 monthly searches | >10,000 monthly searches |
| **Audience fit** | Tangentially related to ICP | Same industry, different role | Exactly your ICP |
| **Uniqueness** | Many free alternatives exist | Exists but yours is better | Nothing good exists for free |
| **Product connection** | No natural bridge to paid product | Indirect connection | Direct "and if you want more, try [Product]" |
| **Build feasibility** | 3+ months to MVP | 1-2 months to MVP | 1-4 weeks to MVP |
| **Shareability** | Users use silently | Users mention it | Users actively share results/output |

**Scoring guidance:**
- **24-30:** Strong candidate. Prioritize this tool.
- **18-23:** Good candidate. Build if resources allow.
- **12-17:** Weak candidate. Needs improvement on low-scoring dimensions.
- **Below 12:** Do not build. Focus elsewhere.

**Evaluation template:**
```
Tool idea: [Description]

Search demand:     [1-5] -- [Evidence: monthly search volume, trend]
Audience fit:      [1-5] -- [Evidence: who searches for this, ICP overlap]
Uniqueness:        [1-5] -- [Evidence: existing alternatives and their gaps]
Product connection:[1-5] -- [Evidence: how this leads to paid product]
Build feasibility: [1-5] -- [Evidence: tech stack, complexity, timeline]
Shareability:      [1-5] -- [Evidence: inherent virality, link-worthiness]

Total score: [X/30]
Recommendation: [Build / Consider / Skip]
```

---

## 4. ROI Projection Model

```
Monthly ROI Projection for Free Tool

Traffic:
  Organic search traffic:     [X] visitors/month (based on keyword volume x expected ranking)
  Social/referral traffic:    [X] visitors/month (based on shareability)
  Direct/returning traffic:   [X] visitors/month (based on repeat usage)
  Total monthly visitors:     [X]

Conversion funnel:
  Tool completion rate:       [X]% (visitors who complete the tool interaction)
  Lead capture rate:          [X]% (visitors who provide email)
  Signup conversion rate:     [X]% (leads who sign up for main product)
  Activation rate:            [X]% (signups who activate)
  Paid conversion rate:       [X]% (activated users who become paid)

Monthly output:
  Leads captured:             [X] (visitors x completion rate x lead capture rate)
  Product signups:            [X] (leads x signup conversion rate)
  Activated users:            [X] (signups x activation rate)
  Paid customers:             [X] (activated x paid conversion rate)

Value:
  Average ACV:                $[X]
  Monthly pipeline value:     $[X] (paid customers x ACV)
  Annual pipeline value:      $[X]

Cost:
  Build cost (one-time):      $[X] (engineering time x hourly rate)
  Monthly maintenance:        $[X] (hosting, updates, support)
  Annual total cost:          $[X] (build + 12 months maintenance)

ROI:
  Year 1 ROI:                 [Annual pipeline - Annual cost] / Annual cost = [X]%
  Payback period:             [Build cost / Monthly pipeline value] = [X] months
```

**Benchmark ranges:**
- Tool completion rate: 40-70% for calculators, 20-50% for analyzers
- Lead capture rate: 5-15% (ungated tool with optional email) to 30-60% (gated results)
- Tool-to-signup conversion: 2-8%
- Expected SEO traffic ramp: 3-6 months to meaningful volume

---

## 5. SEO Strategy for Free Tools

### 5.1 Keyword Targeting

**Primary keywords:** "[type] tool", "free [function] tool", "[function] calculator", "[function] checker"

**Keyword research process:**
1. List all variations of what the tool does
2. Check search volume (Ahrefs, SEMrush, Google Keyword Planner)
3. Assess keyword difficulty
4. Target long-tail keywords initially, then expand

### 5.2 On-Page SEO

```
Page structure:
- H1: [Primary keyword -- e.g., "Free Website Speed Test"]
- Meta title: [Primary keyword] -- Free Tool by [Product] (under 60 chars)
- Meta description: [Value prop + call to action] (under 155 chars)
- URL: /tools/[tool-name] or [tool-name].yourdomain.com

Content around the tool:
- Explanation of what the tool does (200-500 words above or below the tool)
- How to interpret results (helps with long-tail keywords)
- FAQ section (targets question-based searches)
- Related resources and guides (internal linking)
```

### 5.3 Link Building Tactics

1. Submit to "best free tools" lists and resource pages
2. Reach out to bloggers who write about your topic
3. Share on relevant communities (Reddit, Hacker News, Product Hunt, Indie Hackers)
4. Create content about the tool (blog posts, case studies)
5. Submit to tool directories and comparison sites

### 5.4 Programmatic SEO Pages

If your tool can generate unique pages for many inputs:

```
Example: [City] cost of living calculator
- /tools/cost-of-living/new-york
- /tools/cost-of-living/san-francisco
... hundreds of unique, indexable pages

Requirements:
- Each page has unique, valuable content (not just parameter swaps)
- Pages are internally linked
- Pages have unique meta titles and descriptions
- Content is genuinely useful, not thin
```

---

## 6. Lead Capture Design

### 6.1 When to Gate vs Leave Ungated

| Approach | When to Use | Pros | Cons |
|---|---|---|---|
| Fully ungated | SEO is primary goal, tool is simple | Better SEO, more usage, more backlinks | Fewer leads captured |
| Gated results | Results are high-value and detailed | Higher lead capture rate | Lower tool completion rate, worse SEO |
| Progressive capture | Want balance of usage and leads | Good balance, feels fair | More complex to implement |
| Optional save | Results are useful but not essential to save | Non-intrusive, builds trust | Lower capture rate than gated |

### 6.2 Progressive Lead Capture Pattern

```
Step 1: Free, ungated
  User inputs data and sees basic results immediately

Step 2: Soft capture
  "Email me a detailed report" or "Save my results"
  Email is optional, provides more value if given

Step 3: Product bridge
  "Want to track this over time? Create a free account"

Step 4: Product upsell
  "With [Product], you can automate this analysis weekly"
```

### 6.3 Lead Capture Form Design

```
Minimum fields: Email only (highest conversion)
Optional additional fields: Name, company, role (for lead scoring)
Progressive profiling: Ask more over time, not all at once

Form placement:
- After results (most common)
- Inline within results ("email this section to yourself")
- Exit intent (if user is about to leave)
- Sidebar persistent (non-intrusive)

Conversion copy:
- "Email me my results" (value-framed, not "give us your email")
- "Get a detailed PDF report" (offers additional value)
- "Save and compare later" (utility-framed)
```

---

## 7. Tool-to-Product Bridge

### 7.1 Bridge Strategies

| Strategy | Description | Example |
|---|---|---|
| Results-based | Tool results reveal a need the product solves | Website grader shows issues, product fixes them |
| Continuation | Tool does one thing, product does it continuously | One-time audit vs ongoing monitoring |
| Expansion | Tool handles simple case, product handles complex | Basic calculator vs full financial modeling |
| Integration | Tool works alone, product integrates with workflow | Standalone checker vs integrated dashboard |
| Automation | Tool requires manual input, product automates | Manual analysis vs automated alerts |

### 7.2 Bridge CTA Placement

```
Placement options (from least to most aggressive):
1. Footer link: "Built by [Product] -- learn more"
2. Results sidebar: "Want this automated? Try [Product]"
3. Results inline: Within results, show what the paid product adds
4. Post-results CTA: Dedicated section after results with product pitch
5. Follow-up email: 2-3 days after tool use, product introduction email
6. Retargeting: Display ads to tool users highlighting product
```

### 7.3 Bridge Copy Framework

```
Headline: [Acknowledge what they just learned/accomplished with the free tool]
Body: [Connect the free tool experience to the ongoing need the product solves]
  - "You just [action with free tool]. With [Product], you can [ongoing benefit]."
  - "Your results show [finding]. [Product] helps you [fix/improve/track] automatically."
Value statement: [Specific benefit of the product, tied to their tool experience]
CTA: "Try [Product] free" or "See how [Product] works"
```

---

## 8. MVP Scoping

### 8.1 Build the Simplest Useful Version

```
MVP scoping checklist:
- [ ] Core function works reliably (the tool does what it promises)
- [ ] Input is simple (minimize form fields, use smart defaults)
- [ ] Output is clear and actionable (users understand results)
- [ ] Design is clean and professional (reflects product brand quality)
- [ ] Mobile-responsive (significant portion of traffic will be mobile)
- [ ] Page loads fast (tool should load in under 3 seconds)
- [ ] Basic analytics instrumented (visitors, completions, captures)

Explicitly defer for V1:
- Advanced customization options
- User accounts and saved results (unless essential to value)
- Complex visualizations (start with simple, clear output)
- Multiple tool variations (start with one, expand based on data)
- API access
- Integrations with other tools
```

### 8.2 Technology Choices

| Approach | When to Use | Pros | Cons |
|---|---|---|---|
| Static site + JS | Simple calculators, generators | Fast, cheap to host, great SEO | Limited backend capability |
| Serverless functions | Analyzers, tools needing APIs | Scalable, cost-effective | Cold start latency |
| Full web app | Complex tools, user accounts | Full control, rich features | Higher cost and maintenance |
| Subdomain of product | Any tool | SEO domain authority, brand consistency | Coupled to product infrastructure |
| Separate domain | Tools targeting different keyword | SEO flexibility, independent scaling | No domain authority transfer |

### 8.3 Launch Timeline Template

```
Week 1: Design and scope
  - Finalize tool concept and MVP feature set
  - Create wireframes for input, processing, and results

Week 2-3: Build
  - Implement core tool functionality
  - Build input form and results display
  - Add lead capture mechanism
  - Instrument analytics

Week 4: Polish and launch prep
  - Design review and polish
  - SEO optimization (meta tags, content, structured data)
  - Performance optimization
  - Prepare launch content (blog post, social posts, outreach list)

Week 5: Launch
  - Soft launch to existing users/community
  - Submit to Product Hunt
  - Post to relevant communities
  - Begin backlink outreach

Week 6+: Iterate
  - Analyze usage data (where do users drop off?)
  - A/B test lead capture approach
  - Improve results quality based on feedback
```

---

## 9. Promotion Strategies

### 9.1 Launch Channels

| Channel | Effort | Impact | Timing |
|---|---|---|---|
| Product Hunt | Medium | High (spike) | Launch day |
| Hacker News (Show HN) | Low | High (if front page) | Launch day |
| Reddit (relevant subreddits) | Low | Medium | Launch week |
| Twitter/LinkedIn | Low | Medium | Launch week, ongoing |
| Company blog | Medium | Medium (SEO) | Launch day |
| Email to existing users | Low | Medium | Launch day |

### 9.2 Ongoing Promotion

| Channel | Effort | Impact | Timing |
|---|---|---|---|
| SEO (organic search) | Low ongoing | High (compounds) | 3-6 months to results |
| Backlink outreach | Medium | High (SEO + referral) | Monthly |
| Content marketing | Medium | Medium (supports SEO) | Ongoing |
| Retargeting ads | Low | Medium | Ongoing |

---

## 10. Metrics

### Primary Metrics

| Metric | Formula | Target |
|---|---|---|
| Tool visitors | Unique visitors per month | Growth month over month |
| Tool completion rate | Completed / Total visitors | 40-70% |
| Tool-to-signup conversion | Signups from tool / Tool visitors | 2-8% |
| Signup-to-paid conversion | Paid from tool / Signups from tool | Compare to organic |
| Tool-acquired CAC | Total tool costs / Paid customers from tool | < paid channel CAC |
| Backlinks generated | Unique referring domains | Growth over time |
| SEO rankings | Keyword positions for target terms | Top 10 within 6 months |

### Attribution

```
Attribution chain:
  Tool visit (UTM: source=tool, medium=organic/social/referral)
  -> Lead capture (email captured, attributed to tool)
  -> Product signup (link tool visit to signup via cookie/email match)
  -> Activation (track tool-sourced users through activation funnel)
  -> Paid conversion (attribute revenue to tool channel)

Compare tool-acquired users to organic:
  - Activation rate: [tool] vs [organic]
  - Time to paid conversion: [tool] vs [organic]
  - LTV: [tool] vs [organic]
  - Retention (30/60/90 day): [tool] vs [organic]
```

---

## 11. Output Format

When proposing a free tool strategy, produce this specification:

```
# Free Tool Strategy Brief

## Tool Concept
- Tool name: [...]
- Tool type: [Calculator / Generator / Analyzer / Tester / Library / Interactive]
- One-line description: [What does it do?]
- Target user: [Who is this for?]
- Search intent: [What will users search to find this?]

## Evaluation Scorecard
- Search demand: [1-5] -- [Evidence]
- Audience fit: [1-5] -- [Evidence]
- Uniqueness: [1-5] -- [Evidence]
- Product connection: [1-5] -- [Evidence]
- Build feasibility: [1-5] -- [Evidence]
- Shareability: [1-5] -- [Evidence]
- Total: [X/30]

## ROI Projection
- Expected monthly traffic: [X] (at month 6-12)
- Lead capture rate: [X]%
- Tool-to-signup conversion: [X]%
- Expected monthly signups: [X]
- Expected monthly paid conversions: [X]
- Estimated monthly pipeline: $[X]
- Build cost: $[X]
- Payback period: [X] months

## MVP Specification
- Core functionality: [What the tool does in V1]
- Input: [What the user provides]
- Output: [What the user receives]
- Lead capture: [When and how you capture email]
- Product bridge: [How tool connects to paid product]
- Tech approach: [How you will build it]

## SEO Plan
- Primary keywords: [List with search volume]
- Secondary keywords: [List]
- Content strategy: [Supporting content around the tool]

## Launch Plan
- Build timeline: [X weeks]
- Launch channels: [List]
- Promotion plan: [First 30 days]

## Success Metrics
- 30-day targets: [Traffic, completions, leads]
- 90-day targets: [Traffic, signups, SEO rankings]
- 6-month targets: [Traffic, paid conversions, backlinks, ROI]
```

---

Related skills: `viral-loops`, `growth-loops`, `plg-strategy`
