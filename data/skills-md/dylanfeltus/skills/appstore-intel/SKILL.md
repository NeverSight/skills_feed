---
name: appstore-intel
description: Look up app details, ratings, reviews, and search the iOS App Store, Mac App Store, and Google Play. Use when the user asks about app ratings, wants to compare apps, or research a competitor's app store presence. No API key required.
---

# App Store Intelligence

Look up app details, ratings, reviews, and search the iOS App Store and Mac App Store using Apple's free iTunes Search & Lookup APIs. No API key required.

For Google Play, use web scraping via `web_search` and `web_fetch`.

## When to Use

- User asks about an app's ratings or reviews
- User wants to compare apps in a category
- User wants to find apps by keyword
- User asks about a competitor's app store presence
- User wants app metadata (price, size, version, release notes)

## API Overview — Apple iTunes Search API

**Free. No authentication. No API key.**

Two endpoints:
- **Search:** `https://itunes.apple.com/search`
- **Lookup:** `https://itunes.apple.com/lookup`

**Rate Limit:** ~20 calls per minute. Cache results for heavy usage.

## Searching for Apps

### Basic Search

```
https://itunes.apple.com/search?term=QUERY&country=COUNTRY&entity=software&limit=N
```

Use `web_fetch` to call this URL. Response is JSON.

### Parameters

| Parameter | Description | Required | Values |
|-----------|-------------|----------|--------|
| `term` | Search query (URL-encoded, `+` for spaces) | Yes | Any text |
| `country` | Two-letter country code | Yes | `us`, `gb`, `de`, etc. |
| `entity` | App type | No | `software` (iPhone), `iPadSoftware`, `macSoftware` |
| `media` | Media type | No | `software` (default for apps) |
| `limit` | Max results | No | 1–200 (default 50) |
| `lang` | Language | No | `en_us`, `ja_jp` |

### Example

```
https://itunes.apple.com/search?term=fitness+tracker&country=us&entity=software&limit=10
```

## Looking Up Specific Apps

### By App ID (Track ID)

```
https://itunes.apple.com/lookup?id=APP_ID&country=us
```

### By Bundle ID

```
https://itunes.apple.com/lookup?bundleId=com.example.app&country=us
```

### Multiple Apps at Once

```
https://itunes.apple.com/lookup?id=ID1,ID2,ID3&country=us
```

## Response Format

Each result contains:

```json
{
  "trackId": 553834731,
  "trackName": "App Name",
  "bundleId": "com.example.app",
  "sellerName": "Company Name",
  "artistName": "Developer Name",
  "price": 0.00,
  "formattedPrice": "Free",
  "currency": "USD",
  "averageUserRating": 4.5,
  "userRatingCount": 125000,
  "averageUserRatingForCurrentVersion": 4.3,
  "userRatingCountForCurrentVersion": 5000,
  "contentAdvisoryRating": "4+",
  "trackContentRating": "4+",
  "primaryGenreName": "Health & Fitness",
  "genres": ["Health & Fitness", "Lifestyle"],
  "description": "Full app description...",
  "releaseNotes": "What's new in this version...",
  "version": "3.2.1",
  "currentVersionReleaseDate": "2024-01-10T00:00:00Z",
  "releaseDate": "2020-06-15T00:00:00Z",
  "fileSizeBytes": "52428800",
  "minimumOsVersion": "15.0",
  "trackViewUrl": "https://apps.apple.com/us/app/...",
  "artworkUrl512": "https://is1-ssl.mzstatic.com/...",
  "screenshotUrls": ["url1", "url2"],  // ⚠️ Can be 10+ URLs — summarize count, don't dump all
  "supportedDevices": ["iPhone15,2", "iPad14,1"],  // ⚠️ Can be 100+ items — omit from output to save context
  "languageCodesISO2A": ["EN", "FR", "DE"]
}
```

The response wrapper:
```json
{
  "resultCount": 10,
  "results": [...]
}
```

## Google Play Lookup

There's no free public Google Play API. Use these approaches:

### Web Search

```
web_search: "site:play.google.com/store/apps QUERY"
```

### Direct App Page Scraping

```
web_fetch: https://play.google.com/store/apps/details?id=PACKAGE_ID&hl=en&gl=us
```

⚠️ **Google Play pages may return limited content or block automated requests.** If `web_fetch` returns incomplete data, fall back to `web_search` results which typically include rating, download count, and developer info in the snippet.

Extract from the fetched HTML (when available):
- Title, developer, rating, review count, downloads
- Description, what's new, screenshots

### Google Play Package ID

The package ID is in the URL: `play.google.com/store/apps/details?id=com.example.app`

## Step-by-Step Instructions

### Search for Apps by Keyword

1. URL-encode the search term
2. Fetch: `https://itunes.apple.com/search?term=ENCODED_QUERY&country=us&entity=software&limit=10`
3. Parse JSON response
4. For each result, present: name, developer, rating, review count, price, and App Store link

### Get Detailed Info for a Specific App

1. Find the app's Track ID (from a search, or from the App Store URL — the number after `/id`)
2. Fetch: `https://itunes.apple.com/lookup?id=TRACK_ID&country=us`
3. Present full details: rating, reviews, version, release notes, price, size, description

### Compare Two Apps

1. Look up both apps: `https://itunes.apple.com/lookup?id=ID1,ID2&country=us`
2. Present side-by-side comparison of key metrics

### Check an App's Rating Across Countries

1. Look up the same ID with different country codes:
   - `https://itunes.apple.com/lookup?id=APP_ID&country=us`
   - `https://itunes.apple.com/lookup?id=APP_ID&country=gb`
   - `https://itunes.apple.com/lookup?id=APP_ID&country=de`
2. Compare ratings and review counts by region

### Find Both iOS and Android Versions

1. Search iOS: iTunes Search API with the app name
2. Search Android: `web_search "site:play.google.com/store/apps APP_NAME"`
3. Fetch the Google Play page with `web_fetch` for details
4. Present both platforms' data

## Finding App IDs

- **From App Store URL:** `apps.apple.com/us/app/app-name/id553834731` → ID is `553834731`
- **From search results:** The `trackId` field
- **From bundle ID lookup:** If you know the bundle ID (e.g., `com.spotify.client`)

## Output Format

### Single App

```
### App Name
⭐ 4.5/5 (125K ratings) · Free
By Developer Name · Health & Fitness
Version 3.2.1 (Jan 10, 2024)

📝 What's New: Latest release notes summary...

📱 iOS: https://apps.apple.com/...
🤖 Android: https://play.google.com/...
```

### Search Results

```
### App Store Results for "query" (N found)

1. **App Name** ⭐ 4.5 (125K) · Free
   By Developer · Category
   📱 https://apps.apple.com/...

2. **App Name** ⭐ 4.2 (50K) · $4.99
   By Developer · Category
   📱 https://apps.apple.com/...
```

### Comparison

```
### App Comparison

| Metric | App A | App B |
|--------|-------|-------|
| Rating | ⭐ 4.5 | ⭐ 4.2 |
| Reviews | 125K | 50K |
| Price | Free | $4.99 |
| Size | 50 MB | 120 MB |
| Last Updated | Jan 10, 2024 | Dec 5, 2023 |
```

## Error Handling

- **No results:** The search term may be too specific. Try broader terms or check spelling.
- **API error / timeout:** Retry once. The iTunes API is generally reliable.
- **Rate limited:** Wait 60 seconds. Consider caching results for batch lookups.
- **Country not found:** Verify the two-letter ISO country code.
- **App removed from store:** The lookup will return `resultCount: 0`. Inform the user the app may have been removed.
- **Google Play scraping fails:** The page structure may have changed. Fall back to `web_search` results.

## Examples

### Example 1: "How's the Spotify app rated?"

```
Fetch: https://itunes.apple.com/lookup?bundleId=com.spotify.client&country=us
```

### Example 2: "Find fitness apps with good ratings"

```
Fetch: https://itunes.apple.com/search?term=fitness&country=us&entity=software&limit=20
```
Then filter results where `averageUserRating >= 4.5` and sort by `userRatingCount`.

### Example 3: "Compare Notion and Obsidian on the App Store"

Look up both apps and present a comparison table.

## Data Sources

- **iOS / Mac:** [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/) — Free, no auth
- **Android:** Google Play Store web pages via `web_fetch` — Free, no auth, scraping
