---
name: app-store-reviews
description: >
  App Store review analysis, competitor intelligence, and automated response
  generation for iOS/macOS apps. Use this skill when working with Apple App Store
  reviews for any of these tasks: (1) Fetching and analyzing customer reviews for
  your own apps via the App Store Connect API, (2) Fetching competitor app reviews
  via the public RSS feed or iTunes Search API, (3) Performing sentiment analysis,
  theme extraction, or bug/feature-request categorization on reviews,
  (4) Generating context-aware developer replies to customer reviews,
  (5) Comparing ratings, review sentiment, or feature gaps across competing apps,
  (6) Tracking rating trends and review volume over time,
  (7) Producing executive summaries or actionable insight reports from review data,
  (8) Searching the App Store for apps by name or category,
  (9) Setting up app-specific reply configurations through an interactive onboarding
  interview that auto-detects patterns from existing responses.
---

# App Store Reviews

Analyze App Store reviews, generate intelligent replies, and extract competitive
insights using Apple's public and private APIs.

## Workflow 0 — App Setup & Onboarding

Before generating replies, run the onboarding process to create an app-specific
configuration file. This ensures replies match your brand voice consistently.

### Quick Start

1. Ask the user: "Would you like to set up reply preferences for your app?"
2. If yes, proceed with onboarding
3. If a config file already exists, ask if they want to update it

### Onboarding Steps

1. **Fetch existing responses** (if available):
   ```
   GET /v1/apps/{appId}/customerReviews?include=response&limit=100
   ```

2. **Auto-detect patterns** from existing replies:
   - Greeting style ("Hi {name}," vs "Hello!")
   - Sign-off ("— The Team" vs none)
   - Tone (formal vs casual)
   - Emoji usage
   - Support email/URLs
   - Common phrases

3. **Present findings** to user:
   ```
   "I analyzed {n} existing replies and detected these patterns:
    - Tone: {detected_tone}
    - Sign-off: {detected_signoff}
    - Emoji usage: {detected_emoji}
    Would you like to use these as defaults?"
   ```

4. **Conduct interview** with smart defaults:
   - App identity (name, description, support email)
   - Brand voice (tone, emoji, sign-off)
   - Reply policies (escalation, restricted topics)
   - Language support

   See [onboarding-interview.md](references/onboarding-interview.md) for full question list.

5. **Generate config file**:
   - Create `{app-name}-review-config.md`
   - Save to user's preferred location
   - Confirm file location

### Output

The onboarding process generates a markdown configuration file following the
template in [app-config-template.md](references/app-config-template.md).

### Re-running Setup

Users can update their configuration at any time:
- Update specific settings
- Start fresh with new configuration
- Keep existing and continue

---

## API Access Tiers

ReviewCat works with two tiers of Apple endpoints:

| Tier | Auth | Scope | Reference |
|------|------|-------|-----------|
| **Public** | None | Any app (read-only reviews, search, lookup) | See [apple-endpoints.md](references/apple-endpoints.md) §1 |
| **Private** | JWT (App Store Connect) | Your own apps (full CRUD on reviews + responses) | See [apple-endpoints.md](references/apple-endpoints.md) §2 |

Choose the tier based on the task:

- **Own app** → prefer Private API (more data, filtering, responses, summarizations)
- **Competitor app** → must use Public API (RSS feed, iTunes Search)
- **Quick lookup / no auth available** → Public API

## Workflow 1 — Fetch & Analyze Own App Reviews

1. Generate a JWT token (see [apple-endpoints.md](references/apple-endpoints.md) §2.1)
2. Fetch reviews: `GET /v1/apps/{appId}/customerReviews`
   - Use `sort=-createdDate` for newest first
   - Use `filter[rating]=1,2` to focus on negative reviews
   - Use `filter[territory]=USA` for a specific country
   - Set `limit=200` and paginate via `links.next`
3. For version-specific reviews, first list versions with
   `GET /v1/apps/{appId}/appStoreVersions`, then query
   `GET /v1/appStoreVersions/{versionId}/customerReviews`
4. Run analysis on collected reviews (see [Workflow 5](#workflow-5--analyze-reviews))

## Workflow 2 — Fetch Competitor Reviews

1. Search for competitor: `GET https://itunes.apple.com/search?term={name}&media=software`
2. Extract `trackId` from results
3. Fetch reviews via RSS:
   ```
   GET https://itunes.apple.com/{country}/rss/customerreviews/page={1-10}/id={trackId}/sortby=mostrecent/json
   ```
4. Loop pages 1–10 (max 500 reviews per country)
5. For multi-country analysis, iterate over country codes: `us`, `gb`, `de`, `fr`, `jp`, `au`, `ca`, `br`, `kr`, `cn`
6. Parse entries from `feed.entry[]` — fields: `im:rating.label`, `title.label`, `content.label`, `author.name.label`, `im:version.label`

## Workflow 3 — Generate Replies to Reviews

Generate context-aware, professional developer responses to customer reviews.

### Pre-requisite: App Configuration

Before generating replies, check if an app configuration file exists:

1. **If config exists:** Load settings from `{app-name}-review-config.md`
2. **If no config:** Prompt user to run [Workflow 0](#workflow-0--app-setup--onboarding) first,
   or proceed with default settings

When a config file is available, apply these settings:
- **Brand voice:** Tone, emoji usage, sign-off style
- **Preferred phrases:** Use configured phrases where appropriate
- **Avoided phrases:** Never use words/phrases marked as restricted
- **Policies:** Follow escalation rules and restricted topics
- **Language:** Match supported language preferences

### Reply Strategy

| Rating | Tone | Strategy |
|--------|------|----------|
| 1–2 stars | Empathetic, solution-focused | Acknowledge frustration, offer fix/workaround, invite follow-up |
| 3 stars | Grateful, improvement-oriented | Thank for feedback, highlight upcoming improvements |
| 4–5 stars | Warm, brief | Thank the user, reinforce positive experience |

### Instructions

1. **Load app config** (if available) from `{app-name}-review-config.md`
2. Read the review's rating, title, body, and territory
3. Identify the core issue or sentiment
4. Check if topic is restricted (redirect to support if so)
5. Select reply strategy based on rating + config policies
6. Draft response following:
   - App config settings (tone, phrases, emoji, sign-off)
   - Patterns in [reply-templates.md](references/reply-templates.md)
7. Validate reply against config constraints:
   - No restricted topics mentioned
   - No avoided phrases used
   - Correct sign-off applied
   - Length within config preference
8. Post via `POST /v1/customerReviewResponses` (private API only)

### Constraints

- Max response length: 5,970 characters (Apple's limit)
- Do NOT include personal information, legal promises, or pricing details
- Always be professional — never argue or be defensive
- Reference specific issues the user raised to show the reply is not generic
- For non-English reviews, respond in the same language as the review
- **Follow all policies defined in app config file**

## Workflow 4 — Competitor Comparison

Build a competitive analysis comparing your app with competitors.

1. Fetch your app's reviews (Workflow 1) and competitor reviews (Workflow 2)
2. For each app, compute:
   - **Average rating** (overall + per version)
   - **Rating distribution** (count per star)
   - **Sentiment score** — ratio of positive (4–5) to negative (1–2) reviews
   - **Review velocity** — reviews per week/month
3. Run theme extraction on each app's reviews (see Workflow 5)
4. Identify:
   - **Your strengths** — themes praised in your reviews but criticized in competitors
   - **Your gaps** — themes praised in competitors but criticized in your reviews
   - **Common pain points** — negative themes shared across all apps
   - **Feature requests** — features users ask for across all apps
5. Output a structured comparison report (see [analysis-prompts.md](references/analysis-prompts.md) §competitor-report)

## Workflow 5 — Analyze Reviews

Perform deep analysis on a set of collected reviews. See [analysis-prompts.md](references/analysis-prompts.md) for detailed prompt patterns.

### Theme Extraction

Categorize every review into one or more themes:

- **Bug report** — crashes, errors, broken features
- **Feature request** — missing functionality users want
- **UX complaint** — confusing UI, poor navigation, design issues
- **Performance** — slow, battery drain, storage usage
- **Pricing** — subscription cost, value perception, payment issues
- **Praise** — positive feedback on specific features
- **Support** — customer service experience

For each theme, track: count, average rating, representative quotes, trend direction.

### Sentiment Analysis

Classify each review as: `positive`, `neutral`, `negative`, `mixed`.

Use the following signals:
- Rating (primary signal): 1–2 = negative, 3 = neutral/mixed, 4–5 = positive
- Body text sentiment (secondary signal): override rating when text clearly contradicts it
  (e.g., 5-star review that says "app is terrible but I accidentally tapped 5 stars")

### Actionable Insights

From the analyzed reviews, extract:

1. **Top 5 issues** — most mentioned negative themes, sorted by frequency
2. **Top 5 praised features** — most mentioned positive themes
3. **Trending issues** — themes increasing in frequency over recent reviews
4. **Quick wins** — issues that appear fixable and are frequently mentioned
5. **Feature demand** — requested features ranked by mention count

## Workflow 6 — Executive Summary Report

Generate a concise report for stakeholders.

### Report Structure

```
## Review Summary — {App Name} — {Date Range}

### Key Metrics
- Total reviews: {n}
- Average rating: {x.x}/5
- Rating distribution: ★5: {n} | ★4: {n} | ★3: {n} | ★2: {n} | ★1: {n}
- Sentiment: {x}% positive, {x}% neutral, {x}% negative

### Top Issues
1. {Issue} — {count} mentions — "{representative quote}"
2. ...

### Top Praise
1. {Feature} — {count} mentions — "{representative quote}"
2. ...

### Trending
- ↑ Increasing: {themes getting worse}
- ↓ Decreasing: {themes improving}

### Recommendations
1. {Actionable recommendation based on data}
2. ...
```

## Workflow 7 — Rating Trend Monitoring

Track how ratings change over time.

1. Fetch reviews with `sort=createdDate` to get chronological order
2. Group reviews by time period (day/week/month)
3. Compute per-period: average rating, review count, sentiment ratio
4. Identify inflection points — sudden drops/spikes in rating
5. Correlate with app version releases (use `im:version` from RSS or version endpoint from private API)
6. Flag anomalies: rating drop > 0.5 stars, negative review spike > 2x average

## Pagination Reference

### Private API (App Store Connect)

Cursor-based. Follow `links.next` URL until absent:

```python
url = f"https://api.appstoreconnect.apple.com/v1/apps/{app_id}/customerReviews?limit=200&sort=-createdDate"
all_reviews = []
while url:
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    data = resp.json()
    all_reviews.extend(data["data"])
    url = data.get("links", {}).get("next")
```

### Public API (RSS Feed)

Page-based. Iterate pages 1–10:

```python
for page in range(1, 11):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
    resp = requests.get(url)
    entries = resp.json().get("feed", {}).get("entry", [])
    if not entries:
        break
    all_reviews.extend(entries)
```

## Rate Limits

| Endpoint | Limit | Backoff Strategy |
|----------|-------|-----------------|
| App Store Connect API | Undocumented — use moderate pace | Exponential backoff on 429/503 |
| iTunes Search / Lookup | ~20 req/min | Wait 3s between calls |
| RSS Feed | Undocumented — can get 403 | Wait 5s between country iterations |

## Quick Reference — Endpoint Cheat Sheet

| Task | Method | Endpoint | Auth |
|------|--------|----------|------|
| Search apps | GET | `itunes.apple.com/search?term=...&media=software` | Public |
| Lookup app | GET | `itunes.apple.com/lookup?id=...` | Public |
| Public reviews | GET | `itunes.apple.com/{cc}/rss/customerreviews/page={p}/id={id}/sortby=mostrecent/json` | Public |
| List reviews | GET | `/v1/apps/{id}/customerReviews` | JWT |
| Version reviews | GET | `/v1/appStoreVersions/{id}/customerReviews` | JWT |
| Single review | GET | `/v1/customerReviews/{id}` | JWT |
| Get response | GET | `/v1/customerReviews/{id}/response` | JWT |
| Post response | POST | `/v1/customerReviewResponses` | JWT |
| Delete response | DELETE | `/v1/customerReviewResponses/{id}` | JWT |
| Summarizations | GET | `/v1/apps/{id}/customerReviewSummarizations` | JWT |
| List versions | GET | `/v1/apps/{id}/appStoreVersions` | JWT |

For full endpoint details, parameters, and authentication setup, see [apple-endpoints.md](references/apple-endpoints.md).

## Reference Files

| File | Purpose |
|------|---------|
| [apple-endpoints.md](references/apple-endpoints.md) | API endpoint details, authentication, parameters |
| [analysis-prompts.md](references/analysis-prompts.md) | Prompt patterns for review analysis |
| [reply-templates.md](references/reply-templates.md) | Reply templates by rating and issue type |
| [onboarding-interview.md](references/onboarding-interview.md) | Interview questions and auto-detection logic |
| [app-config-template.md](references/app-config-template.md) | Template for app-specific config files |
