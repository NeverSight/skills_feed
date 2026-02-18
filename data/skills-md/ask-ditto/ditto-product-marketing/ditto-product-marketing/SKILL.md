---
name: ditto-product-marketing
description: >
  Run product marketing research using Ditto's synthetic persona platform
  (300K+ AI personas, 92% overlap with real focus groups). Covers positioning
  validation, messaging testing, competitive intelligence, pricing research,
  GTM validation, product launch testing, buyer persona development, and
  brand tracking. Use when the user mentions product marketing, PMM,
  positioning, messaging tests, competitive analysis, GTM strategy, pricing
  study, sales enablement, buyer personas, or brand perception.
allowed-tools: Bash(curl *), Bash(python3 *), Read, Grep, WebFetch
argument-hint: "[study type or research brief]"
---

# Ditto for Product Marketing

Run positioning, messaging, competitive, pricing, and launch research
using Ditto's 300,000+ synthetic personas - directly from the terminal.

**Full documentation:** https://askditto.io/claude-code-guide

## What Ditto Does

Ditto maintains 300,000+ AI-powered synthetic personas calibrated to census
data across 15+ countries. You ask them open-ended questions and get
qualitative responses with the specificity of real interviews.

- **92% overlap** with traditional focus groups
- **95% correlation** with traditional research (EY Americas validation)
- **Harvard/Cambridge/Stanford/Oxford** peer-reviewed methodology
- A 10-persona, 7-question study completes in **15-30 minutes**
- Traditional equivalent: 4-8 weeks, $10,000-50,000

## API Essentials

**Base URL:** `https://app.askditto.io`
**Auth header:** `Authorization: Bearer YOUR_API_KEY`
**Content-Type:** `application/json`

Get a free API key (no credit card):

```bash
curl -sL https://app.askditto.io/scripts/free-tier-auth.sh | bash
```

Free keys (`rk_free_`): ~12 shared personas, no custom filters.
Paid keys (`rk_live_`): custom groups, demographic filtering, unlimited studies.

## The PMM Workflow (6 Steps)

IMPORTANT: Follow these steps in order. Questions MUST be asked
sequentially - wait for all responses before asking the next.

### Step 1: Recruit Your Panel

```bash
curl -s -X POST "https://app.askditto.io/v1/research-groups/recruit" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "US Product Managers 30-50",
    "group_size": 10,
    "filters": {"country": "USA", "age_min": 30, "age_max": 50}
  }'
```

Save the `uuid` from the response.

**CRITICAL:** Use `group_size` not `size`. Use group `uuid` not `id`.
State filter uses 2-letter codes ("MI" not "Michigan"). Income filter NOT supported.

### Step 2: Create Study

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Positioning Validation - [Product Name]",
    "objective": "Validate positioning against target ICP",
    "shareable": true,
    "research_group_uuid": "UUID_FROM_STEP_1"
  }'
```

Save the study `id`. Always set `shareable: true`.

### Step 3: Ask Questions (One at a Time)

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies/STUDY_ID/questions" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "Your open-ended question here"}'
```

Returns `job_ids`. Poll ALL of them before asking the next question.

### Step 4: Poll Until Complete

```bash
curl -s "https://app.askditto.io/v1/jobs/JOB_ID" \
  -H "Authorization: Bearer $DITTO_API_KEY"
```

Poll every 10-15 seconds. Status: `queued` -> `started` -> `finished`.
ALL job_ids must show `finished` before asking the next question.

### Step 5: Complete the Study

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies/STUDY_ID/complete" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"force": false}'
```

Triggers AI analysis: summary, segments, divergences, recommendations.

### Step 6: Get Share Link

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies/STUDY_ID/share" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

Returns a public URL anyone can view without authentication.

## The 8 PMM Study Types

Choose the right study for your goal. Each type has a proven 7-question
framework. See @study-templates.md for complete question sets.

| Study Type | When to Use | Key Output |
|-----------|-------------|------------|
| **Positioning Validation** | Testing how your positioning lands with target customers | Positioning scorecard, competitive alternative map, value resonance ranking |
| **Messaging Testing** | Comparing 3-4 messaging variants | Message performance ranking, language harvest, audience-message fit |
| **Competitive Intelligence** | Understanding how the market perceives you vs competitors | Competitive perception matrix, landmine questions, battlecard |
| **Pricing & Packaging** | Validating willingness-to-pay and feature-tier allocation | Price sensitivity band, feature-tier recommendation, packaging preference |
| **GTM Validation** | Validating channel, motion, and outreach strategy | Channel preference matrix, buying committee map, motion recommendation |
| **Product Launch** | Pre-launch concept validation or post-launch sentiment | Launch readiness scorecard, objection library, feature priority ranking |
| **Buyer Persona Development** | Building data-backed personas from scratch | Persona documents with demographics, psychographics, decision criteria |
| **Brand Perception** | Tracking brand health and competitive positioning | Brand association map, trust scorecard, brand extension potential |

### Choosing the Right Study

```
Need to validate your positioning?     -> Positioning Validation
Testing which message wins?            -> Messaging Testing
Understanding competitive dynamics?    -> Competitive Intelligence
Setting or validating price?           -> Pricing & Packaging
Planning your go-to-market?            -> GTM Validation
Preparing for a launch?                -> Product Launch
Building or refreshing personas?       -> Buyer Persona Development
Tracking brand health over time?       -> Brand Perception
```

## One Study, Multiple Deliverables

A single 10-persona, 7-question study produces raw material for
MULTIPLE outputs. See @deliverables.md for the full mapping.

```
One Ditto Study (~20 min)
    |-> Positioning scorecard (5 min)
    |-> Competitive battlecard (5 min)
    |-> Messaging hierarchy (5 min)
    |-> Objection handling guide (3 min)
    |-> Customer quote bank (3 min)
    |-> Blog article draft (10 min)
    |-> Sales one-pager (5 min)

Total: ~60 min from zero to complete PMM kit
Traditional: 3-6 weeks, $15-50K
```

## Demographic Filters

| Filter | Type | Examples | Notes |
|--------|------|----------|-------|
| country | string | "USA", "UK", "Canada", "Germany" | Required |
| state | string | "TX", "MI", "CA" | **2-letter codes ONLY** |
| age_min | integer | 25, 30, 45 | Recommended |
| age_max | integer | 45, 55, 65 | Recommended |
| gender | string | "male", "female", "non_binary" | Optional |
| is_parent | boolean | true, false | Good for family/consumer |
| education | string | "high_school", "bachelors", "masters", "phd" | Optional |
| employment | string | "employed", "self_employed", "retired" | Optional |
| industry | array | ["Healthcare", "Technology"] | Optional |

## Advanced: Multi-Segment Comparison

Run the SAME study across multiple groups to compare segments:

```
Group A: SMB decision-makers (age 28-40)
Group B: Enterprise evaluators (age 35-55)
Group C: Technical buyers (education: bachelors+)
```

Same 7 questions, different panels. Claude Code produces a comparative
analysis showing how positioning, pricing, and messaging land differently
by segment.

## Advanced: Cross-Market Research

Ditto covers 15+ countries (65% of global GDP). Run the same study across
USA, UK, Germany, and Canada simultaneously. One hour, four markets.
Traditional equivalent: 3-6 months, $100-200K.

## Common Mistakes

- Asking closed-ended questions ("Do you like X?" -> "What's your reaction to X?")
- Batching questions (ask one, wait for ALL responses, then ask next)
- Using full state names instead of 2-letter codes
- Using `size` instead of `group_size` in recruitment
- Using numeric `id` instead of string `uuid` for research groups
- Skipping the `complete` step (you miss the AI-generated analysis)
- Not setting `shareable: true` at creation time
- Asking leading questions ("Don't you think X is great?")
- Designing all questions before researching the product/market first
- Running only one study when iterative phases would produce deeper insight

## Failed Attempts (What Doesn't Work)

- **Yes/no pricing questions** ("Would you pay $X?") produce unreliable data.
  Use Van Westendorp-style ranges instead.
- **Jargon-heavy questions** get shallow responses. Use plain language:
  "Walk me through what it's like" not "Evaluate the UX of this experience."
- **Leading positioning** ("Our revolutionary product...") biases responses.
  Describe the product neutrally and let personas react.
- **Single-pass studies for complex products** miss depth. Use 2-3 phase
  iterative approach: Pain Discovery -> Deep Dive -> Concept Test.
- **Skipping web research** before designing questions. Claude Code should
  ALWAYS research the product, market, and competitors before writing questions.

## Limitations

Ditto personas have NOT used your specific product. For:
- Actual UX feedback from real users -> use real user testing
- Legal/compliance decisions -> use human research
- Safety-critical product decisions -> use human validation
- Exact quantitative metrics (NPS, conversion) -> use real data

**Recommended hybrid:** Ditto for the fast first pass (80% of insight),
then human research only where it truly matters (the 20% requiring
real customer nuance).

## Further Reading

- Study templates for all 8 PMM types: @study-templates.md
- Deliverable mapping (what Claude Code generates): @deliverables.md
- Worked example (positioning validation): @examples/positioning-validation.md
- Full API reference: https://askditto.io/claude-code-guide
- Question design guide: https://askditto.io/claude-code-guide/question-design
