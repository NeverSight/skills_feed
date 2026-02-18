---
name: ditto-product-research
description: >
  Use in order to perform product reaserch - including conducting customer
  research, product validation, pricing tests, positioning studies, competitive
  analysis, or market research, using Ditto's synthetic research platform 
  (300K+ AI personas, 92% overlap with real focus   groups). Covers the full workflow: setup, recruitment, study design, question asking, insight 
  extraction, and share link generation. Also use when the user mentions Ditto,
  synthetic research, persona studies, or customer validation.
allowed-tools: Bash(curl *), Bash(python3 *), Read, Grep, WebFetch
---

# Ditto Product Research

Run customer research, pricing tests, and product validation studies using
Ditto's synthetic persona platform — directly from the terminal.

**Full documentation:** https://askditto.io/claude-code-guide

## What Ditto Does

Ditto maintains 300,000+ AI-powered synthetic personas calibrated to census
data. You ask them open-ended questions and get qualitative responses with
the specificity of real interviews. EY validated the methodology at 92%
statistical overlap with traditional focus groups.

A 10-persona, 7-question study completes in 15-30 minutes. Traditional
equivalent: 4-8 weeks, $10,000-50,000.

## Quick Start (Free Tier)

Get a free API key — no credit card, no sales call:

```bash
curl -sL https://app.askditto.io/scripts/free-tier-auth.sh | bash
```

Or visit: https://app.askditto.io/docs/free-tier-oauth

Free keys (`rk_free_`) give access to ~12 shared personas.
Paid keys (`rk_live_`) unlock custom groups with demographic filtering.

## API Essentials

**Base URL:** `https://app.askditto.io`
**Auth header:** `Authorization: Bearer YOUR_API_KEY`
**Content-Type:** `application/json`

## The Workflow (6 Steps)

IMPORTANT: Always follow these steps in order. Do NOT skip steps or batch
questions. Questions MUST be asked sequentially — wait for all responses
from one question before asking the next.

### Step 1: Create Research Group

```bash
curl -s -X POST "https://app.askditto.io/v1/research-groups/recruit" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "US Adults 30-55",
    "group_size": 10,
    "filters": {
      "country": "USA",
      "age_min": 30,
      "age_max": 55
    }
  }'
```

Save the `uuid` from the response — you need it in Step 2.

**CRITICAL: Use `group_size` not `size`. Use group `uuid` not `id`.**

### Step 2: Create Study

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Product Concept Validation",
    "objective": "Understand customer pain points and validate pricing",
    "shareable": true,
    "research_group_uuid": "GROUP_UUID_FROM_STEP_1"
  }'
```

Save the study `id` from the response.

### Step 3: Ask Questions (One at a Time)

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies/STUDY_ID/questions" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "Your open-ended question here"}'
```

Response returns `job_ids`. You MUST poll ALL of them before asking the
next question.

### Step 4: Poll Until All Responses Complete

```bash
curl -s "https://app.askditto.io/v1/jobs/JOB_ID" \
  -H "Authorization: Bearer $DITTO_API_KEY"
```

Poll every 10-15 seconds. Status progresses: `queued` → `started` → `finished`.
Wait until ALL job_ids from the question show `finished`, then ask the next
question.

### Step 5: Complete the Study

After all questions are answered:

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies/STUDY_ID/complete" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"force": false}'
```

This triggers AI analysis — summary, segments, divergences, recommendations.
Takes 1-2 minutes.

### Step 6: Get Share Link

```bash
curl -s -X POST "https://app.askditto.io/v1/research-studies/STUDY_ID/share" \
  -H "Authorization: Bearer $DITTO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'
```

Returns a public URL anyone can view without an API key.

## The 7-Question Framework

Design studies with this proven sequence (adapt to your domain):

1. **Establish relevance** — "Walk me through how you currently handle [task]. What does a typical week look like?"
2. **Identify pain** — "What's the most frustrating part of [task]? What makes you want to throw your laptop out the window?"
3. **Quantify impact** — "Roughly how much time/money do you lose to [problem] per week?"
4. **Current solutions** — "What tools or workarounds do you currently use? What works? What doesn't?"
5. **Past attempts** — "Have you tried switching to something new? What happened?"
6. **Magic wand** — "If you could fix ONE thing about [task], what would it be and why?"
7. **Adoption barriers** — "Imagine a tool that solves [problem]. What would make you hesitant to try it, even if it saved you time?"

The magic wand question (Q6) is consistently the most revealing — it
surfaces what customers actually want vs. what they say they want.

See @question-playbook.md for advanced patterns.

## Demographic Filters

| Filter | Type | Examples | Notes |
|--------|------|----------|-------|
| country | string | "USA", "UK", "Canada", "Germany" | Required |
| state | string | "TX", "MI", "CA", "NY" | **2-letter codes ONLY** |
| age_min | integer | 25, 30, 45 | Recommended |
| age_max | integer | 45, 55, 65 | Recommended |
| gender | string | "male", "female", "non_binary" | Optional |
| is_parent | boolean | true, false | Good for family research |
| education | string | "high_school", "bachelors", "masters", "phd" | Optional |
| employment | string | "employed", "self_employed", "retired" | Optional |
| industry | array | ["Healthcare", "Technology"] | Optional |

**IMPORTANT: State filter uses 2-letter codes. "Michigan" returns 0 results. Use "MI".**
**IMPORTANT: Income filter is NOT supported. Do not include it.**

## Optimal Study Parameters

- **Panel size:** 10 personas (optimal signal-to-noise ratio)
- **Questions:** 7 per study (deep enough to surface patterns, not so many responses fatigue)
- **Question style:** Open-ended, scenario-based. Never yes/no.
- **Multi-phase studies:** Run 2-3 studies for deeper validation (see @examples/carequarter.md)

## Common Mistakes to Avoid

- Asking closed-ended questions ("Do you like X?" → ask "What's your reaction to X?" instead)
- Batching questions (API will fail — ask one, wait for all responses, then ask next)
- Using full state names instead of 2-letter codes
- Using `size` instead of `group_size` in recruitment
- Using numeric `id` instead of string `uuid` for research groups
- Skipping the `complete` step (you miss the AI-generated analysis)
- Not making studies `shareable: true` at creation time
- Asking leading questions ("Don't you think X is great?" → ask "What's your honest reaction to X?")

## Reading Responses

After polling is complete, retrieve all Q&A data:

```bash
curl -s "https://app.askditto.io/v1/research-studies/STUDY_ID/questions" \
  -H "Authorization: Bearer $DITTO_API_KEY"
```

Each response includes:
- `response_text` — the persona's answer (may contain HTML: `<b>`, `<ul>`, `<li>`)
- `agent_name`, `agent_age`, `agent_city`, `agent_state`, `agent_country`
- `agent_occupation`, `agent_summary`

Use these demographics to segment findings by age, location, occupation.

## Multi-Phase Research

For deeper validation, run iterative studies:

| Phase | Purpose | Panel | Questions |
|-------|---------|-------|-----------|
| 1. Pain Discovery | Find the real problem | 10-12 personas | 7 open-ended |
| 2. Deep Dive | Understand requirements and trust boundaries | 10 personas | 7 targeted |
| 3. Concept Test | Validate positioning, pricing, purchase intent | 10 personas | 7 structured |

Each phase's questions should be informed by the previous phase's findings.
This iterative approach produces qualitatively different results than a
single-pass study.

See @examples/carequarter.md for a complete 3-phase worked example.

## What You Can Test

- **Pain points** — Do customers actually have this problem?
- **Pricing** — What price is a bargain? A stretch? A dealbreaker?
- **Positioning** — Which tagline/value prop resonates most?
- **Features** — What do customers prioritise vs. ignore?
- **Landing pages** — Upload screenshots and get qualitative reactions
- **Ad creative** — Test headlines, images, and messaging variants
- **Competitive switching** — What would make someone leave their current solution?
- **Deal breakers** — What kills the sale even if the product is good?

## Further Reading

- Full API guide: https://askditto.io/claude-code-guide
- Question design: @question-playbook.md
- Worked examples: @examples/carequarter.md
- API endpoint reference: @api-reference.md
