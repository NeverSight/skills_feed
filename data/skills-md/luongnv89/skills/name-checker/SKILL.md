---
name: name-checker
description: Check product/brand names for trademark, domain, and social media conflicts. Use when users ask to "check this name", "validate a product name", "is this name available", or need to assess naming risks. Provides risk assessment and alternative suggestions.
---

# Name Checker

Check product and brand names for conflicts across trademarks, domains, and social media.

## Input

Name to analyze provided in `$ARGUMENTS`. If empty, ask user for the name.

Optionally check for `prd.md` in project to understand product context.

## Analysis Protocol

**CRITICAL: STOP immediately if any exact social handle is taken.**

### Step 1: Social Media Check (First Priority)

Use WebSearch to check handles on:
- X/Twitter: `"@[NAME]" site:twitter.com OR site:x.com`
- Instagram: `"@[NAME]" site:instagram.com`
- Facebook: `"[NAME]" site:facebook.com`
- LinkedIn: `"[NAME]" site:linkedin.com/company`
- YouTube: `"[NAME]" site:youtube.com`
- TikTok: `"@[NAME]" site:tiktok.com`

**If exact handle taken:** Return `NEGATIVE: Exact social handle taken (@platform)` and STOP. Suggest different name.

### Step 2: Domain Check (if Step 1 clear)

Use WebSearch to check:
- `.com` (highest priority)
- `.io`, `.app`, `.co`
- Regional: `.eu`, `.fr`

Search: `site:[NAME].com` and `"[NAME].com" domain availability`

**Status:**
- Available: No active site
- Parked: Domain exists but for-sale/parking
- Active: In use (flag if same industry)

### Step 3: Trademark Check (if Step 1 clear)

Use WebSearch for trademark databases:

| Database | Search Query |
|----------|--------------|
| WIPO | `"[NAME]" site:branddb.wipo.int` |
| EUIPO | `"[NAME]" site:euipo.europa.eu` |
| INPI (France) | `"[NAME]" site:inpi.fr` |

Focus on Nice Classes 9, 35, 42 (software/technology). Note if marks are live or expired.

### Step 4: Risk Assessment

| Risk Level | Criteria |
|------------|----------|
| **Low** | Social handles available, .com available/parked, no trademark conflicts |
| **Moderate** | Some handles taken (not exact), .com taken but alternatives available, similar trademarks exist |
| **High** | Multiple handles taken, .com active in same industry, active trademarks in classes 9/35/42 |

### Step 5: Recommendation

- **Proceed**: Low risk - name is viable
- **Modify**: Moderate risk - suggest 1-2 variants addressing conflicts
- **Abandon**: High risk - suggest completely different alternatives

## Output Format

```
SOCIAL: Clear | NEGATIVE: [reason]
DOMAIN: .com (status) | .io (status) | .app (status)
TM: WIPO (status) | EUIPO (status) | INPI (status)
RISK: [Low/Moderate/High] - [reason]
RECOMMEND: [Proceed/Modify/Abandon] (+ variants if needed)
```

## PRD Integration

If `prd.md` found, add:

**Name Fit Assessment:**
- Alignment with product vision
- Memorability, pronunciation, spelling
- Target audience fit

**Alternative Suggestions:**

| Name | Rationale | Quick Risk |
|------|-----------|------------|
| Name1 | Why it fits | Availability |
| Name2 | Why it fits | Availability |
| Name3 | Why it fits | Availability |

## Final Action

- **Proceed**: Confirm safe to use, suggest registration order (domain first, then socials)
- **Modify**: Recommend best variant with explanation
- **Abandon**: Recommend best alternative from suggestions
