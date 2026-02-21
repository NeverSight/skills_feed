---
name: buying-signals
description: "Detect B2B buying signals for prospect companies. Analyzes companies across web/news, landing pages, social media and scores them by buying intent (HOT/WARM/COOL/COLD). Use for: prospect scoring, lead qualification, outbound sales research, GTM signal detection. Triggers: buying signals, analyze company, score prospects, buying intent, lead scoring, signal detection, sales intelligence, prospect research, company analysis, outbound signals, GTM signals, warm leads, hot leads"
allowed-tools: Bash(alavida *)
---

# Buying Signals

Detect B2B buying signals for prospect companies via the [Alavida](https://alavida.ai) CLI.

## Quick Start

```bash
npm install -g @alavida/cli && alavida auth

# Analyze a company
alavida run buying-signals --input '{
  "companies": [{"company_id": "acme-1", "company_name": "Acme Corp", "domain": "acme.com"}]
}' --poll
```

## Setup

Install the CLI and authenticate:

```bash
npm install -g @alavida/cli
alavida auth
```

Verify you're connected:

```bash
alavida auth status
alavida credits
```

## Running Analysis

### Single Company

```bash
alavida run buying-signals --input '{
  "companies": [{
    "company_id": "stripe-1",
    "company_name": "Stripe",
    "domain": "stripe.com"
  }]
}' --poll
```

### Multiple Companies

```bash
alavida run buying-signals --input '{
  "companies": [
    {"company_id": "stripe-1", "company_name": "Stripe", "domain": "stripe.com"},
    {"company_id": "vercel-1", "company_name": "Vercel", "domain": "vercel.com"},
    {"company_id": "linear-1", "company_name": "Linear", "domain": "linear.app"}
  ]
}' --poll
```

### With People (Better Signal Detection)

Adding key people improves social signal detection (founder pain posts, conference speaking):

```bash
alavida run buying-signals --input '{
  "companies": [{
    "company_id": "acme-1",
    "company_name": "Acme Corp",
    "domain": "acme.com",
    "website_url": "https://acme.com",
    "people": [
      {
        "full_name": "Jane Doe",
        "job_title": "CEO & Founder",
        "role_type": "decision_maker",
        "twitter_handle": "@janedoe",
        "linkedin_url": "https://linkedin.com/in/janedoe"
      }
    ]
  }]
}' --poll
```

### From a JSON File

```bash
alavida run buying-signals --input companies.json --poll
```

### Submit and Check Later

Jobs run asynchronously. Submit without `--poll` and check back:

```bash
# Submit
alavida run buying-signals --input '{"companies": [...]}'
# => Job submitted: 550e8400-...

# Do other work, then check
alavida jobs status 550e8400-e29b-41d4-a716-446655440000

# Or list all jobs
alavida jobs
```

## Input Schema

View the full input/output schema anytime:

```bash
alavida schema buying-signals
```

### Company Fields

| Field | Required | Description |
|-------|----------|-------------|
| `company_id` | Yes | Unique identifier |
| `company_name` | Yes | Company name |
| `domain` | No | Domain (e.g., "acme.com") |
| `website_url` | No | Full website URL |
| `people` | No | Key people for social signal detection |

### Person Fields

| Field | Required | Description |
|-------|----------|-------------|
| `full_name` | Yes | Person's full name |
| `job_title` | Yes | Job title |
| `role_type` | No | `decision_maker` or `champion` |
| `twitter_handle` | No | Twitter handle with @ |
| `linkedin_url` | No | LinkedIn profile URL |

## Signal Types

| Signal Type | Weight | Description |
|-------------|--------|-------------|
| `founder_pain_post` | 100 | Founder expressing need for creative/marketing help |
| `job_post_creative` | 90 | Hiring designer, video editor, creative director |
| `funding_announcement` | 80 | Recent funding round (seed through Series C+) |
| `yc_batch` | 80 | Y Combinator company preparing for Demo Day |
| `stealth_launch` | 75 | Company coming out of stealth or launching |
| `job_post_marketing` | 60 | Hiring marketing roles (CMO, growth, demand gen) |
| `partnership_announced` | 50 | New partnership or integration |
| `conference_speaking` | 40 | Founder/exec speaking at conference |

## Tier System

| Tier | Score | Action |
|------|-------|--------|
| **HOT** | 150+ | Prioritize immediately |
| **WARM** | 80-149 | Good outreach candidates |
| **COOL** | 40-79 | Monitor for more signals |
| **COLD** | <40 | Lowest priority |

## CLI Reference

| Command | Description |
|---------|-------------|
| `alavida auth` | Authenticate with API key |
| `alavida auth status` | Show auth status and credit balance |
| `alavida credits` | View credit balance and usage |
| `alavida run buying-signals --input '<json>' --poll` | Run analysis and wait for results |
| `alavida run buying-signals --input file.json` | Submit from file |
| `alavida jobs` | List all jobs |
| `alavida jobs status <job_id>` | Check job status and results |
| `alavida schema buying-signals` | View input/output schema |
| `alavida registry` | Browse all available components |

## Pricing

- **Base cost:** 500 credits per run
- **Typical range:** 400-800 credits depending on signal density
- Credits are deducted after job completion

Check your balance: `alavida credits`

## Error Handling

| Error | Fix |
|-------|-----|
| Not authenticated | Run `alavida auth` |
| Invalid API key (401) | Get a new key from the dashboard |
| Insufficient credits (402) | Top up at the dashboard |
| Service unavailable (503) | Try again in a few minutes |
| Job failed | Run `alavida jobs status <job_id>` for details |

## Other Components

Browse the full registry:

```bash
alavida registry
```

| Component | Type | Description |
|-----------|------|-------------|
| `buying-signals` | workflow | B2B buying signal detection |
| `echo` | tool | Test component for sync calls |
| `echo-workflow` | workflow | Test component for async flows |

Install and run any component the same way:

```bash
alavida schema <slug>
alavida run <slug> --input '{...}' --poll
```
