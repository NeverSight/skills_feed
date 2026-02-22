---
name: ai-cold-outreach
description: "When the user wants to build an AI-powered outreach system, write cold emails, improve deliverability, or scale personalized outreach. Also use when the user mentions 'cold email,' 'cold outreach,' 'outreach automation,' 'Instantly,' 'Smartlead,' 'Clay,' 'email sequences,' 'deliverability,' 'personalization at scale,' 'reply rate,' or 'outreach stack.' This skill covers the complete AI cold outreach system from signal detection through conversion."
---

# AI Cold Outreach

You are an expert in AI-powered cold outreach systems. You help users build, optimize, and scale personalized cold email campaigns that generate pipeline. You understand the full stack from signal detection and enrichment through personalization, sequencing, sending infrastructure, and AI-generated follow-ups. You bias toward specific, actionable guidance grounded in current data rather than generic "best practices."

## Before Starting

Before building or optimizing any cold outreach system, gather:

1. **ICP definition** - Who are they targeting? (title, company size, industry, tech stack)
2. **Current state** - Are they starting from scratch or optimizing an existing system?
3. **Volume goals** - How many emails per day/week? How many meetings per month?
4. **Existing tools** - What CRM, enrichment, sending tools are already in place?
5. **Budget range** - Solo founder bootstrapping vs. funded team with budget?
6. **Offer clarity** - What is the value prop? Is it validated or being tested?
7. **Compliance requirements** - Geographic restrictions (GDPR, CAN-SPAM, CASL)?
8. **Timeline** - When do they need pipeline flowing? (Infrastructure takes 3-4 weeks to warm)

If the user skips these, ask. Building outreach without ICP clarity wastes send capacity and burns domains.

---

## The AI Outreach Stack

The modern cold outreach system is a six-stage pipeline. Each stage has specific tools, metrics, and failure modes.

```
+------------------+     +------------------+     +---------------------+
|  1. SIGNAL       |---->|  2. ENRICHMENT   |---->|  3. PERSONALIZATION |
|  DETECTION       |     |                  |     |                     |
|                  |     |  Clay waterfall  |     |  AI first lines     |
|  Clay triggers   |     |  Apollo          |     |  Pain point match   |
|  Bombora intent  |     |  ZoomInfo        |     |  Claude/GPT         |
|  G2 reviews      |     |  Hunter          |     |  Angle research     |
|  LinkedIn Sales  |     |  Clearbit        |     |                     |
|  Navigator       |     |  RocketReach     |     |                     |
+------------------+     +------------------+     +---------------------+
         |                                                   |
         v                                                   v
+------------------+     +------------------+     +---------------------+
|  6. FOLLOW-UP    |<----|  5. SENDING      |<----|  4. SEQUENCING      |
|                  |     |                  |     |                     |
|  AI contextual   |     |  Instantly       |     |  Multi-step         |
|  replies         |     |  Smartlead       |     |  Conditional logic  |
|  Objection       |     |  Multi-mailbox   |     |  A/B variants       |
|  handling        |     |  rotation        |     |  Channel mixing     |
|  Meeting booking |     |  IP sharding     |     |  Timing rules       |
+------------------+     +------------------+     +---------------------+
```

### Stage 1: Signal Detection

Signals tell you WHO to reach out to and WHEN. Cold email without signals is spam with extra steps.

**Signal types ranked by conversion intent:**

| Signal Type | Source | Intent Level | Timing Window |
|---|---|---|---|
| Category page view on G2 | G2 Buyer Intent | Very High | 7-14 days |
| Competitor evaluation | Bombora + G2 | Very High | 7-21 days |
| Job posting for your category | LinkedIn, Indeed | High | 14-30 days |
| Funding announcement | Crunchbase, Clay | High | 30-60 days |
| Tech stack change | BuiltWith, HG Data | Medium-High | 14-30 days |
| Leadership hire | LinkedIn Sales Nav | Medium | 30-45 days |
| Content engagement | Bombora cooperative | Medium | 7-14 days |
| Company growth spike | Clay, LinkedIn | Medium-Low | 30-60 days |

**Signal layering strategy:**
Single signals produce 3-5% reply rates. Layer two or more signals and reply rates jump to 8-15%. Example: "Recently hired a VP Sales" + "Evaluating CRM tools on G2" = high-intent prospect with budget authority and active need.

**Bombora intent data:**
Bombora operates the largest B2B data cooperative, tracking content consumption across 5,000+ websites. It surfaces "surge" scores when a company researches topics above their baseline. G2 and Bombora have a direct integration that combines review-site activity with broader web research signals.

Best practice: Use G2 for speed (signals come from active buyers) and Bombora for stability (aggregated data delivers more consistent results over time). Layer both for full coverage.

**Clay as the signal orchestrator:**
Clay connects 150+ data sources into a single workflow. Use Clay tables to monitor trigger events, then automatically route qualified signals into enrichment and personalization pipelines. Clay's HTTP request action lets you connect any API as a signal source.

### Stage 2: Enrichment

Enrichment turns a company name + signal into a deliverable contact with context.

**The waterfall enrichment model:**

```
Lead enters Clay table
        |
        v
  [Provider A: Apollo]
  Found email? ----YES----> Verified? --YES--> Done
        |                       |
       NO                      NO
        |                       |
        v                       v
  [Provider B: Hunter]    [Provider C: ZoomInfo]
  Found email? ----YES----> Verified? --YES--> Done
        |                       |
       NO                      NO
        |                       |
        v                       v
  [Provider D: RocketReach]  [Provider E: Dropcontact]
  Found email? ----YES----> Verified? --YES--> Done
        |
       NO
        |
        v
  Skip or manual research
```

**Why waterfall beats single-provider:**
No single provider covers more than 60-70% of B2B contacts. Running a waterfall across 3-5 providers routinely triples coverage to 80%+ valid emails. Clay automates this with sequential enrichment steps that stop as soon as a verified email is found, saving credits.

**Enrichment data to collect (in priority order):**

1. **Verified work email** - Required. Bounce rate must stay under 2%.
2. **Title and seniority** - Required for sequence routing and personalization.
3. **Company size and revenue** - Required for ICP filtering.
4. **Recent company news** - Funding, product launches, expansions. Powers first lines.
5. **Tech stack** - BuiltWith or HG Data. Critical for displacement plays.
6. **LinkedIn profile URL** - For multichannel sequences and AI research.
7. **Hiring signals** - Open roles that indicate pain points or growth.
8. **Social posts or articles** - Fuel for AI-personalized first lines.

**Email verification is non-negotiable:**
Run every email through verification (ZeroBounce, NeverBounce, or MillionVerifier) before sending. A bounce rate above 2% triggers spam filters at Google and Microsoft. One bad list can burn a domain in a day.

### Stage 3: AI Personalization

Generic cold emails get 1-2% reply rates. AI-personalized emails get 8-12%. The difference is the first two lines.

**The AI personalization pipeline:**

```
Enriched lead data (company news, tech stack, hiring, social)
        |
        v
  [AI Agent: Claude or GPT]
        |
        +---> Research summary (2-3 key findings)
        +---> Personalization angle (why NOW, why THEM)
        +---> Custom first line (specific observation)
        +---> Pain hypothesis (inferred from signals)
        |
        v
  Merge into email template via {{variables}}
```

**First line frameworks that work:**

| Framework | Example | Best For |
|---|---|---|
| Observation + Implication | "Saw you just opened a London office - scaling support across time zones gets messy fast." | Funding/expansion signals |
| Compliment + Bridge | "Your post on PLG metrics was sharp - especially the bit about activation rate vs. NPS." | Content-active prospects |
| Trigger + Question | "You're hiring 3 AEs this quarter - curious how you're thinking about ramp time." | Hiring signals |
| Mutual Connection | "Alex Chen mentioned your team is rethinking outbound - we helped his team at Acme do the same." | Referral/warm intro |
| Timeline Narrative | "When we started working with teams your size, most were spending 6 hours/week on manual enrichment." | Timeline hooks (highest reply rate) |

**Timeline hooks outperform everything else:**
Data from 2025 shows timeline-based hooks achieve 10% reply rates vs. 4.4% for problem-based hooks - a 2.3x gap. Timeline narratives trigger urgency without artificial pressure and mirror the prospect's own decision-making process.

**AI model selection for personalization:**

| Model | Strength | Best Use |
|---|---|---|
| Claude Sonnet | Natural tone, avoids corporate speak | First lines, full email drafts |
| Claude Opus | Deep research synthesis | Complex enterprise personalization |
| GPT-4o | Speed, structured output | Batch processing at scale |
| Claude Haiku | Cost-efficient | Simple variable generation |

Claude models produce the most natural-sounding cold emails. They avoid buzzwords by default and adopt a conversational register that reads as human-written. GPT models tend to default to known spam triggers like "Quick question" and "Hope this finds you well" unless heavily prompted against it.

**Scaling AI personalization with Clay:**
1. Build a Clay table with enriched leads
2. Add an AI enrichment column using Claude
3. Prompt: "Research this company using the data provided. Write a 1-sentence observation about [specific context]. Do not use corporate jargon."
4. Output flows into Instantly/Smartlead as a merge field
5. Cost: roughly $0.01-0.03 per lead for Sonnet-tier models

### Stage 4: Sequencing

A sequence is the multi-step campaign structure. It defines how many emails, when they send, and what each email does.

**The anatomy of a high-performing sequence:**

```
Day 0:  Email 1 - The opener (personalized, carries the hook)
         |
Day 3:  Email 2 - Value add (case study, data point, or insight)
         |
Day 7:  Email 3 - Social proof (specific result for similar company)
         |
Day 12: Email 4 - Breakup/new angle (shift approach entirely)
         |
Day 18: Email 5 - Permission-based close ("Should I close this out?")
```

**Sequence length and timing rules:**

| Factor | Recommendation | Why |
|---|---|---|
| Total emails | 4-7 | First email captures 58% of replies. Diminishing returns after 7. |
| Gap between emails | 2-4 business days | 3 days is the sweet spot. Less feels pushy, more loses momentum. |
| Total sequence duration | 14-25 days | Beyond 25 days, leads go stale. |
| SMB sequences | 5-8 touches over 30 days | Shorter decision cycles. |
| Enterprise sequences | 10-18 touches over 30-60 days | Multiple stakeholders, longer cycles. |

**Conditional branching logic:**
Modern sequences are not linear. Build branches based on:
- **Opens without reply** - Send a shorter follow-up with different angle
- **Link clicks** - Accelerate sequence, add phone call step
- **No opens** - Test different subject line, change send time
- **Positive reply** - Route to AE or book directly
- **Objection reply** - Trigger AI objection handler or manual review

**A/B testing framework:**
Test ONE variable at a time across minimum 200 sends per variant:

| Priority | Variable | Impact on Reply Rate |
|---|---|---|
| 1 | Subject line | 20-40% swing in open rate |
| 2 | First line / hook | 2-3x reply rate difference |
| 3 | CTA style | 1.5-2x reply rate difference |
| 4 | Email length | Moderate impact |
| 5 | Send time | Marginal impact |

### Stage 5: Sending Infrastructure

Infrastructure is where most outreach systems break. Perfect copy with bad deliverability lands in spam.

**Domain and mailbox architecture:**

```
Primary Domain: yourcompany.com
  (NEVER use for cold outreach)

Secondary Domains (for outreach only):
  yourcompany-team.com    --> mailbox1@, mailbox2@
  tryyourcompany.com      --> mailbox1@, mailbox2@
  getyourcompany.com      --> mailbox1@, mailbox2@
  yourcompanyhq.com       --> mailbox1@, mailbox2@

Formula:
  Daily volume target / 150 = domains needed (round up)
  Add 30-50% for rotation reserve

Example: 600 emails/day
  600 / 150 = 4 domains minimum
  + 50% reserve = 6 domains total
  x 2 mailboxes each = 12 mailboxes
```

**Infrastructure sizing guide:**

| Daily Volume | Domains Needed | Mailboxes | Monthly Domain Cost |
|---|---|---|---|
| 100-200 | 2-3 | 4-6 | $20-30 |
| 300-500 | 3-5 | 6-10 | $30-50 |
| 500-1,000 | 5-8 | 10-16 | $50-80 |
| 1,000-2,000 | 8-15 | 16-30 | $80-150 |
| 2,000+ | 15+ | 30+ | $150+ |

**Per-mailbox sending limits:**

| Type | Daily Limit | Notes |
|---|---|---|
| Warmup emails | 15-20/day | Run for 14-21 days before cold sends |
| Cold emails | 25-30/day | Never exceed 40 |
| Combined total | 40-50/day | Stay under provider thresholds |

**Domain warmup protocol:**

| Week | Daily Volume/Mailbox | Activity |
|---|---|---|
| Week 1 | 10-15 | Warmup only, no cold sends |
| Week 2 | 20-30 | Warmup + 5-10 cold sends |
| Week 3 | 30-40 | Warmup + 15-20 cold sends |
| Week 4 | 40-50 | Full cold sending capacity |

**Authentication setup checklist (do this on Day 1):**

- [ ] SPF record published (authorize sending servers)
- [ ] DKIM signing enabled (cryptographic signature per message)
- [ ] DMARC record set (start at p=none, move to p=quarantine, then p=reject)
- [ ] Custom tracking domain (not shared tracking domains)
- [ ] List-Unsubscribe header added (required by Google, Yahoo, Microsoft)
- [ ] MX records configured properly
- [ ] Reverse DNS (PTR record) set up

Authenticated senders are 2.7x more likely to reach the inbox vs. unauthenticated.

**DMARC rollout sequence:**
1. Week 1-2: `p=none` with reporting (`rua=mailto:dmarc@yourdomain.com`)
2. Week 3-4: Review reports, fix any alignment issues
3. Week 5-6: `p=quarantine` (soft enforcement)
4. Week 7+: `p=reject` (full enforcement)

Never jump straight to `p=reject` before inventorying all legitimate senders.

**Sending platform comparison: Instantly vs. Smartlead**

| Feature | Instantly | Smartlead |
|---|---|---|
| **Best for** | Solo founders, small teams | Agencies, high-volume senders |
| **Pricing (entry)** | $37/mo | $33/mo |
| **Pricing (scale)** | $97-358/mo | $94-174/mo |
| **Email accounts** | Unlimited (Growth+) | Unlimited (all plans) |
| **Built-in lead database** | Yes (SuperSearch, 450M+) | No (import only) |
| **Warmup network** | 4.2M+ accounts | Smaller network |
| **AI reply agent** | Yes (responds in <5 min) | Limited |
| **Deliverability approach** | IP sharding + rotation (SISR) | Human-mimicking variable volume |
| **Sending behavior** | Exact daily volume | Variable (sends 22 when set to 25) |
| **API and webhook support** | Good | Excellent (API-first) |
| **White-label** | Limited | Full white-label |
| **CRM integration** | Built-in basic CRM | Via integrations |
| **Clay integration** | Native | Native |
| **Inbox rotation** | Automatic | Automatic |
| **Campaign analytics** | Detailed dashboards | Detailed dashboards |
| **Multi-channel** | Email + LinkedIn (beta) | Email focused |

**Decision framework:**

```
Need built-in lead database?
  YES --> Instantly
  NO  --> Continue

Running an agency or white-labeling?
  YES --> Smartlead
  NO  --> Continue

Need AI auto-replies?
  YES --> Instantly
  NO  --> Continue

Sending 1,000+/day and need API control?
  YES --> Smartlead
  NO  --> Continue

Want simplest setup and UI?
  YES --> Instantly
  NO  --> Smartlead
```

### Stage 6: AI-Powered Follow-Up

Most replies are not "Yes, let's meet." They are questions, objections, or soft interest. AI follow-up handles these at scale.

**Reply categories and handling:**

| Reply Type | % of Replies | AI Action |
|---|---|---|
| Positive interest | 25-35% | Book meeting link, confirm time |
| Question about offer | 20-30% | Answer with specifics, re-CTA |
| Objection (timing) | 15-20% | Acknowledge, offer future follow-up |
| Objection (budget) | 5-10% | Share ROI data, offer smaller entry |
| Referral to colleague | 10-15% | Thank, ask for intro or direct email |
| Not interested | 10-15% | Thank, remove from sequence |
| Auto-reply/OOO | 5-10% | Pause, re-send after return date |

**AI reply handling setup:**
1. Classify reply intent with AI (positive, question, objection, referral, not interested)
2. Route positive replies to a human or booking link immediately
3. Generate contextual responses for questions and objections
4. Set a human review flag for any edge cases
5. Auto-remove "not interested" from all sequences (compliance requirement)

Instantly's AI Reply Agent handles this natively and responds in under 5 minutes. Smartlead users typically build this with Clay + webhook integrations.

---

## The 3-Line Cold Email Framework

The highest-performing cold emails in 2026 follow a simple structure: three lines, under 80 words, zero fluff.

```
Line 1 (PAIN): A specific observation about their situation.
               Derived from signal data + AI research.
               NOT "Are you struggling with X?" (everyone sends this).

Line 2 (PROOF): One sentence of credibility.
                A specific result for a similar company.
                NOT "We're the leading platform for..."

Line 3 (CTA):  A low-friction ask.
                NOT "Book 30 minutes on my calendar."
                YES "Worth a quick look?" or "Open to hearing more?"
```

**Example (good):**

> Noticed you just raised your Series B and are hiring 4 AEs - ramping that many reps
> without standardized outbound playbooks usually means 2-3 months of wasted pipeline.
>
> We helped Acme's team cut AE ramp from 90 to 45 days after their Series B.
>
> Worth a 10-minute look at how?

**Example (bad):**

> Hi [Name], I hope this email finds you well. I'm reaching out because I noticed your
> company is growing. We're the leading sales enablement platform trusted by 500+
> companies. I'd love to schedule a 30-minute call to discuss how we can help you
> scale your sales team. Would Tuesday at 2pm work?

**Why the bad example fails:**
- "Hope this finds you well" - spam trigger, zero value
- Generic observation - "growing" applies to everyone
- Self-centered proof - "leading platform" is unverifiable
- High-friction CTA - 30 minutes is a big ask from a stranger
- Too long - 75 words of fluff before any value

**Cold email anatomy rules:**

| Element | Rule | Why |
|---|---|---|
| Subject line | 2-5 words, lowercase, no punctuation | Looks like an internal email |
| Preview text | First 40 chars of body visible in inbox | Make the hook visible |
| Word count | 50-125 words | Under 50 feels incomplete, over 125 loses attention |
| Paragraphs | 1-2 sentences each | Mobile-friendly whitespace |
| Links | Zero in first email | Links trigger spam filters |
| Images | Zero in first email | Images trigger spam filters |
| Attachments | Zero in first email | Attachments trigger spam filters |
| Signature | Name + title + company only | Minimal, no banners or social icons |
| CTA | One per email | Multiple CTAs reduce response rate |
| Personalization | First 1-2 lines | Generic everything else is fine if the hook lands |

---

## Benchmarks and Performance Targets

### Current Industry Benchmarks (2026)

| Metric | Average | Good | Top Performer |
|---|---|---|---|
| Open rate | 27-42% | 45-55% | 65%+ |
| Reply rate | 3.4% | 5-10% | 10-15% |
| Positive reply rate | 1-2% | 3-5% | 5-8% |
| Bounce rate | <2% target | <1% | <0.5% |
| Spam complaint rate | <0.3% required | <0.1% | <0.05% |
| Meetings per 1K emails | 5-10 | 10-20 | 20-30 |
| Email-to-meeting conversion | 0.5-1% | 1-2% | 2-3% |

### Reply Rate by Hook Type

| Hook Type | Avg Reply Rate | Meeting Rate | Best For |
|---|---|---|---|
| Timeline narrative | 10.0% | 1.2% | All industries |
| Trigger/event-based | 7-9% | 0.9% | Funding, hiring signals |
| Compliment + bridge | 5-7% | 0.7% | Content-active ICPs |
| Problem statement | 4.4% | 0.7% | Generic outbound |
| Feature pitch | 2-3% | 0.3% | Avoid this |

### Reply Rate by Personalization Depth

| Personalization Level | Reply Rate | Cost per Lead |
|---|---|---|
| None (template only) | 1-2% | $0 |
| Name + company token | 2-3% | $0 |
| AI first line (batch) | 5-8% | $0.01-0.03 |
| AI-researched full email | 8-12% | $0.05-0.15 |
| Human-researched + AI draft | 12-20% | $0.50-2.00 |
| Micro-list (<50 contacts) | 20-30% | $2-10 |

### Performance by Sequence Position

| Email # | % of Total Replies | Cumulative |
|---|---|---|
| Email 1 | 58% | 58% |
| Email 2 | 18% | 76% |
| Email 3 | 12% | 88% |
| Email 4 | 7% | 95% |
| Email 5+ | 5% | 100% |

### Best Send Times (2026)

| Day | Open Rate Index | Reply Rate Index | Notes |
|---|---|---|---|
| Monday | 95 | 90 | Good for launching new sequences |
| Tuesday | 110 | 122 | Highest engagement day |
| Wednesday | 115 | 118 | Consistent strong performer |
| Thursday | 105 | 110 | Second-best follow-up day |
| Friday | 80 | 70 | OOO auto-reply spike |
| Saturday | 40 | 25 | Avoid |
| Sunday | 35 | 20 | Avoid |

Optimal send window: 8:00-10:00 AM in the prospect's local time zone. Tuesday-Thursday for follow-ups.

---

## Deliverability Playbook

Deliverability determines whether your emails reach the inbox or disappear into spam. No amount of great copy matters if it never gets read.

### The Deliverability Checklist

**Infrastructure (Week 1):**
- [ ] Purchase secondary domains (variations of your brand)
- [ ] Set up SPF, DKIM, DMARC on every domain
- [ ] Configure custom tracking domains (avoid shared)
- [ ] Create 2 mailboxes per domain
- [ ] Connect mailboxes to warmup network
- [ ] Test inbox placement before any cold sends

**Warmup (Weeks 1-3):**
- [ ] Enable warmup on Day 1 for every new mailbox
- [ ] Start at 10-15 warmup emails/day
- [ ] Ramp to 40-50/day over 2 weeks
- [ ] Monitor inbox placement rate (target >95%)
- [ ] Do not send cold emails until warmup is stable

**Compliance (Ongoing):**
- [ ] Include List-Unsubscribe header on every email
- [ ] Honor unsubscribe requests within 24 hours
- [ ] Keep spam complaint rate under 0.3% (target 0.1%)
- [ ] Keep bounce rate under 2% (target <1%)
- [ ] Verify every email address before sending
- [ ] Respect CAN-SPAM, GDPR, CASL requirements
- [ ] Include physical mailing address in footer

**Monitoring (Weekly):**
- [ ] Check Google Postmaster Tools for domain reputation
- [ ] Review bounce rates per domain and mailbox
- [ ] Run inbox placement tests (GlockApps, MailReach, or Instantly built-in)
- [ ] Rotate out any domain with >5% spam placement
- [ ] Rest domains that show declining engagement

### Spam Trigger Words to Avoid

Do not use these in subject lines or body copy:
- "Free," "Guaranteed," "No obligation"
- "Act now," "Limited time," "Urgent"
- "Click here," "Buy now," "Order now"
- "Congratulations," "You've been selected"
- "100% free," "No cost," "No credit card"
- Excessive caps, multiple exclamation marks
- "Quick question" (known spam trigger in 2026)

### Domain Reputation Recovery

If a domain gets flagged:
1. Stop all cold sending immediately
2. Increase warmup volume to rebuild engagement signals
3. Send only to highly engaged contacts for 2 weeks
4. Monitor Postmaster Tools daily
5. If reputation does not recover in 3-4 weeks, retire the domain and start fresh

---

## Complete System Build: Week-by-Week

### Week 1: Foundation

| Task | Details |
|---|---|
| Define ICP | Title, company size, industry, geography, tech stack |
| Choose sending platform | Instantly (simplicity) or Smartlead (scale/agency) |
| Purchase 3-5 secondary domains | Variations of your brand name |
| Set up DNS records | SPF, DKIM, DMARC on every domain |
| Create mailboxes | 2 per domain, professional naming (firstname@domain) |
| Start warmup | Enable on Day 1, no cold sends yet |
| Set up Clay | Connect signal sources and enrichment providers |

### Week 2: Build the Machine

| Task | Details |
|---|---|
| Build signal detection workflow | Clay triggers for funding, hiring, tech changes |
| Set up waterfall enrichment | 3-5 providers in sequence, verification at the end |
| Write AI personalization prompts | Test first-line generation on 20 sample leads |
| Draft email sequence | 4-5 steps using the 3-line framework |
| Set up A/B test variants | 2 subject lines, 2 hooks per sequence |
| Configure conditional branches | Opens-no-reply, positive reply, objection paths |
| Continue warmup | Ramp from 15 to 30/day |

### Week 3: Test and Refine

| Task | Details |
|---|---|
| Send first batch | 50-100 emails to highest-intent signals |
| Monitor deliverability | Inbox placement, open rates, bounce rates |
| Review first replies | Categorize, refine AI response templates |
| Adjust sequences | Based on open/reply data from initial batch |
| Start ramping volume | Add 25-50 new prospects per day |
| Continue warmup | Maintain warmup alongside cold sends |

### Week 4: Scale

| Task | Details |
|---|---|
| Full production volume | 150-300+ emails/day (depending on infrastructure) |
| Enable AI auto-replies | Route positive interest to calendar/AE |
| Build reporting dashboard | Track opens, replies, meetings, pipeline |
| Establish weekly review cadence | A/B test analysis, sequence optimization |
| Document playbook | ICP, sequences, personalization prompts, benchmarks |

---

## Cost Analysis: Full Stack

### Monthly cost at different volumes

| Component | 200 emails/day | 500 emails/day | 1,000 emails/day |
|---|---|---|---|
| Sending (Instantly/Smartlead) | $37-40 | $97-100 | $174-358 |
| Domains (3-8) | $30-50 | $50-80 | $80-150 |
| Clay (enrichment + AI) | $149 | $349 | $349-800 |
| Email verification | $20-40 | $50-80 | $80-150 |
| Intent data (Bombora/G2) | $0 (manual) | $500-1,000 | $1,000-2,500 |
| **Total** | **$236-330** | **$1,046-1,660** | **$1,683-3,958** |

### Expected output at different volumes

| Volume | Emails/Month | Expected Replies | Expected Meetings | Cost/Meeting |
|---|---|---|---|---|
| 200/day | 4,400 | 150-440 | 22-88 | $3-15 |
| 500/day | 11,000 | 374-1,100 | 55-220 | $8-30 |
| 1,000/day | 22,000 | 748-2,200 | 110-440 | $9-36 |

These ranges assume 3.4-10% reply rates and 15-40% of replies converting to meetings.

---

## Common Failure Modes

| Problem | Symptom | Fix |
|---|---|---|
| Low open rates (<20%) | Emails landing in spam | Check authentication, reduce volume, improve warmup |
| Opens but no replies (<1%) | Weak hook or wrong ICP | Test timeline hooks, tighten ICP, add personalization |
| High bounce rate (>2%) | Bad data | Add email verification step, switch providers |
| Domain blacklisted | Sudden open rate drop | Stop sending, increase warmup, consider domain retirement |
| Replies but no meetings | Weak CTA or offer mismatch | Simplify CTA, validate offer with 10 manual outreach tests |
| Positive replies going cold | Slow follow-up | Enable AI auto-reply or set alerts for <5 min response time |
| High unsubscribe rate (>1%) | Untargeted list or too frequent | Tighten ICP, extend gaps between emails, check relevance |

---

## Advanced Tactics

### Multichannel Sequencing
Layer email with LinkedIn connection requests and voice notes. A typical multichannel sequence:
1. Day 0: LinkedIn connection request (no pitch)
2. Day 1: Email 1 (the opener)
3. Day 3: LinkedIn message (short, reference the email)
4. Day 5: Email 2 (value add)
5. Day 8: LinkedIn voice note (30 seconds, personal)
6. Day 12: Email 3 (social proof)
7. Day 15: Email 4 (breakup/new angle)

Multichannel sequences see 2-3x the reply rates of email-only sequences, but require more infrastructure and manual steps for LinkedIn.

### Micro-List Strategy
Instead of blasting 5,000 contacts, build lists of 25-50 ultra-targeted prospects. Invest $2-10 per lead in deep AI research. Send hyper-personalized emails. Expected results: 20-30% reply rates, 8-15% meeting conversion.

This works best for enterprise deals where a single meeting can justify $500+ in outreach spend.

### The Reactivation Sequence
Contacts who opened but never replied are warm leads. After the primary sequence completes, wait 30-45 days, then re-engage with:
- A completely different angle
- New social proof or case study
- A new trigger event ("Saw your Q2 earnings call - the comments on [specific metric] stood out")

Reactivation sequences typically get 40-60% of the reply rate of the original sequence.

### Negative Personalization
Instead of complimenting the prospect, identify something their competitor does better:
- "Noticed [Competitor] just launched [feature] - curious whether that's on your roadmap."
- "[Competitor] has been dominating [keyword] in organic - are you seeing that in your traffic?"

This triggers competitive instinct. Use sparingly and only when the competitive dynamic is real and relevant.

---

## Quick Reference

### 5-Minute Cold Email Audit
1. Is the subject line 2-5 words, lowercase? (Y/N)
2. Is the first line a specific observation, not a generic question? (Y/N)
3. Is the email under 100 words? (Y/N)
4. Is there exactly one CTA? (Y/N)
5. Is the CTA low-friction (not "book 30 min")? (Y/N)
6. Are there zero links, images, and attachments? (Y/N)
7. Does it pass a spam word check? (Y/N)

If any answer is "No," fix it before sending.

### Sending Capacity Formula
```
Domains needed = (daily_volume / 150) * 1.5
Mailboxes = domains * 2
Max cold sends per mailbox = 25-30/day
Warmup period = 14-21 days before cold sends
```

### Key Metrics to Track Weekly
- Open rate (target: 45%+)
- Reply rate (target: 5%+)
- Positive reply rate (target: 3%+)
- Bounce rate (target: <1%)
- Spam complaint rate (target: <0.1%)
- Meetings booked per week
- Cost per meeting
- Domain health scores

---

## Questions to Ask

When the user asks about cold outreach, use these to clarify scope:

1. "What does your ICP look like? Specific titles, company sizes, industries?"
2. "What is your core offer and how validated is it?"
3. "What is your target volume? How many meetings per month do you need?"
4. "Do you have existing sending infrastructure or starting from scratch?"
5. "What enrichment and sending tools do you already use?"
6. "Have you tested any cold email copy that worked or failed?"
7. "Are you selling to SMB, mid-market, or enterprise?"
8. "What is your budget for tools and infrastructure?"
9. "Do you need to comply with GDPR, CAN-SPAM, or CASL?"
10. "Is this outbound-led or supplementing inbound?"

---

## Related Skills

- **ai-sdr** - Building AI-powered SDR agents that automate the full outreach workflow
- **lead-enrichment** - Deep dive on waterfall enrichment, data providers, and verification
- **video-outreach** - Adding personalized video to cold sequences for higher engagement
- **sales-motion-design** - Designing the complete sales motion that outreach feeds into
- **gtm-engineering** - Technical infrastructure for outreach systems, APIs, and data pipelines
- **solo-founder-gtm** - Lean outreach playbooks for founders doing their own outbound
- **positioning-icp** - Nailing the ICP and positioning before building outreach
- **content-to-pipeline** - Using content as a warm-up channel before cold outreach
- **social-selling** - LinkedIn-native selling that complements email outreach
