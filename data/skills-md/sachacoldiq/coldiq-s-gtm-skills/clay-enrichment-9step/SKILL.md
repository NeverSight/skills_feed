---
name: clay-enrichment-9step
description: Complete 9-step Clay enrichment workflow for 90%+ data coverage plus 58 Clay templates across 8 categories. Use when building enrichment workflows, setting up Clay tables, or maximizing data quality.
---

# Clay 9-Step Enrichment Workflow (90%+ Coverage)

For detailed templates, see [references/templates.md](references/templates.md).

## Quick Reference

| Step | Action | Tools |
|------|--------|-------|
| 1 | Upload & Clean | CSV import |
| 2 | Company Enrichment | Apollo, Ocean.io, LinkedIn |
| 3 | People Enrichment | Sales Navigator, Apollo |
| 4 | Email Waterfall | Apollo, Prospeo, LeadMagic, Findymail |
| 5 | Email Verification | MillionVerifier |
| 6 | Phone Numbers | LeadMagic, BetterContact |
| 7 | Custom Data | Claygent |
| 8 | Scoring | Lead scoring (100 pts) |
| 9 | Export | Instantly, LemList, CRM |

## Step 4: Email Waterfall (The Money Step)

**Single finder = 40% coverage**
**Waterfall = 85%+ coverage**

Sequence: Apollo → Prospeo → LeadMagic → Findymail → Clay patterns

## Step 8: Scoring & Segmentation

**Lead Score (100 points):**
- Company size match: 25 pts
- Recent signals: 25 pts
- Email deliverability: 25 pts
- ICP fit: 25 pts

**Tiers:**
- Tier 1 (80-100): Immediate outreach
- Tier 2 (60-79): Nurture sequence
- Tier 3 (<60): Long-term nurture

## Pro Tips

- Run in batches of 250 (optimizes Clay credits)
- Test with 50 records first before full run
- Timeline: 1,000 prospects = 2-3 hours vs 40+ hours manual

---

## Combines with

| Skill | Why |
|-------|-----|
| `clay-buying-signals-5` | Add signal detection to workflow |
| `lead-sources-guide` | Know where to source initial data |
| `ai-personalization-prompts` | Use Claygent for AI personalization |
| `buying-signals-6` | Understand which signals to track |

## Example prompts

```
Set up a Clay workflow for job change signals with email waterfall.
```

```
How do I configure Step 4 (Email Waterfall) to maximize coverage?
```

```
Create a scoring model for SaaS companies targeting enterprise accounts.
```
