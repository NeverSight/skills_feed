---
name: review-cat
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
  (8) Searching the App Store for apps by name or category.
---

# ReviewCat

Analyze App Store reviews, generate intelligent replies, and extract competitive
insights using Apple's public and private APIs.

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

### Reply Strategy

| Rating | Tone | Strategy |
|--------|------|----------|
| 1–2 stars | Empathetic, solution-focused | Acknowledge frustration, offer fix/workaround, invite follow-up |
| 3 stars | Grateful, improvement-oriented | Thank for feedback, highlight upcoming improvements |
| 4–5 stars | Warm, brief | Thank the user, reinforce positive experience |

### Instructions

1. Read the review's rating, title, body, and territory
2. Identify the core issue or sentiment
3. Select reply strategy based on rating
4. Draft response following patterns in [reply-templates.md](references/reply-templates.md)
5. Post via `POST /v1/customerReviewResponses` (private API only)

### Constraints

- Max response length: 5,970 characters (Apple's limit)
- Do NOT include personal information, legal promises, or pricing details
- Always be professional — never argue or be defensive
- Reference specific issues the user raised to show the reply is not generic
- For non-English reviews, respond in the same language as the review

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
