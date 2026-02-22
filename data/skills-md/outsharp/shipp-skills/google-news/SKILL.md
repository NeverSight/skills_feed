---
name: google-news
description: >
  Google News is a free news aggregator by Google that surfaces headlines from
  thousands of publishers worldwide. Use this skill to fetch top stories, topic
  feeds, location-specific news, and keyword searches via the public Google News
  RSS feeds. No API key or authentication is required.

metadata:
  author: Outsharp Inc.
  version: 0.1.0

compatibility:
  requirements:
    - Internet access
    - Any HTTP client (curl, wget, fetch, requests, etc.)
    - An XML/RSS parser (or plain-text processing)
  notes:
    - All endpoints are fully public — no authentication, API key, or account is needed.
    - Responses are RSS 2.0 XML.
    - Google News may rate-limit aggressive polling; use reasonable intervals (≥ 60 s).
    - Article links redirect through Google; the final destination is the publisher's page.
    - Feed contents are region- and language-specific; set `hl`, `gl`, and `ceid` accordingly.

allowed-tools:
  - Bash(curl:*)
  - Bash(wget:*)
  - Bash(python*:*)
  - Bash(pip*:*)
  - Bash(node*:*)
  - Bash(npx*:*)
  - Bash(jq:*)
  - Bash(xmllint:*)

---

# Google News RSS API

[Google News](https://news.google.com) is a free news aggregator that collects headlines from thousands of publishers around the world. Google exposes its feeds via public RSS 2.0 endpoints that require **no authentication or API key**.

---

## Base URL

```
https://news.google.com/rss
```

All feed URLs are built by appending paths and query parameters to this base.

---

## Query Parameters

Every feed URL accepts the following **query parameters** to control region and language:

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `hl` | Yes | Interface language / locale code | `en-US`, `fr`, `de`, `ja`, `pt-BR`, `es-419` |
| `gl` | Yes | Country / geographic location (ISO 3166-1 alpha-2) | `US`, `GB`, `IN`, `DE`, `JP`, `BR` |
| `ceid` | Yes | Compound locale key in the form `{gl}:{language}` | `US:en`, `GB:en`, `DE:de`, `JP:ja`, `BR:pt-419` |

> **Important:** All three parameters should be consistent. Mismatched values may return unexpected or empty results.

---

## Supported Locations (Validated)

The following locations have been tested and confirmed to return valid RSS feeds (HTTP 200):

| Location | `hl` | `gl` | `ceid` | Example URL |
|----------|------|------|--------|-------------|
| 🇺🇸 United States | `en-US` | `US` | `US:en` | `https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en` |
| 🇬🇧 United Kingdom | `en-GB` | `GB` | `GB:en` | `https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en` |
| 🇮🇳 India | `en-IN` | `IN` | `IN:en` | `https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en` |
| 🇦🇺 Australia | `en-AU` | `AU` | `AU:en` | `https://news.google.com/rss?hl=en-AU&gl=AU&ceid=AU:en` |
| 🇨🇦 Canada | `en-CA` | `CA` | `CA:en` | `https://news.google.com/rss?hl=en-CA&gl=CA&ceid=CA:en` |
| 🇩🇪 Germany | `de` | `DE` | `DE:de` | `https://news.google.com/rss?hl=de&gl=DE&ceid=DE:de` |
| 🇫🇷 France | `fr` | `FR` | `FR:fr` | `https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr` |
| 🇯🇵 Japan | `ja` | `JP` | `JP:ja` | `https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja` |
| 🇧🇷 Brazil | `pt-BR` | `BR` | `BR:pt-419` | `https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419` |
| 🇲🇽 Mexico | `es-419` | `MX` | `MX:es-419` | `https://news.google.com/rss?hl=es-419&gl=MX&ceid=MX:es-419` |
| 🇮🇱 Israel | `en-IL` | `IL` | `IL:en` | `https://news.google.com/rss?hl=en-IL&gl=IL&ceid=IL:en` |

---

## Feed Types

### 1. Top Stories (Headlines)

Returns the current top stories for a given location.

**URL pattern:**
```
https://news.google.com/rss?hl={hl}&gl={gl}&ceid={gl}:{lang}
```

**Example — US top stories:**
```
https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en
```

---

### 2. Topic Feeds

Returns articles for a specific news topic / section.

**URL pattern:**
```
https://news.google.com/rss/topics/{TOPIC_ID}?hl={hl}&gl={gl}&ceid={gl}:{lang}
```

**Known Topic IDs (English, US):**

| Topic | Topic ID |
|-------|----------|
| World | `CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB` |
| Nation / U.S. | `CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjU0FtVnVLQUFQAQ` |
| Business | `CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB` |
| Technology | `CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB` |
| Entertainment | `CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB` |
| Sports | `CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB` |
| Science | `CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB` |
| Health | `CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ` |

**Example — Technology news (US):**
```
https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en
```

> **Note:** Topic IDs are base64-encoded protocol buffer strings. They can differ by language/region. The IDs above are for `en-US`. To find topic IDs for other locales, inspect the RSS link on the Google News website for that locale.

---

### 3. Keyword / Search Feeds

Returns articles matching a search query.

**URL pattern:**
```
https://news.google.com/rss/search?q={query}&hl={hl}&gl={gl}&ceid={gl}:{lang}
```

**Query modifiers:**

| Modifier | Description | Example |
|----------|-------------|---------|
| `+` or space | AND (default) | `q=artificial+intelligence` |
| `OR` | OR operator | `q=Tesla+OR+SpaceX` |
| `-` | Exclude term | `q=Apple+-fruit` |
| `"..."` | Exact phrase (URL-encode the quotes) | `q=%22climate+change%22` |
| `when:7d` | Time filter — last N days/hours | `q=Bitcoin+when:7d` |
| `when:1h` | Time filter — last 1 hour | `q=breaking+news+when:1h` |
| `after:YYYY-MM-DD` | Articles after a date | `q=Olympics+after:2024-07-01` |
| `before:YYYY-MM-DD` | Articles before a date | `q=Olympics+before:2024-08-15` |
| `site:` | Restrict to a domain | `q=AI+site:reuters.com` |

**Example — search for "artificial intelligence" in the last 7 days:**
```
https://news.google.com/rss/search?q=artificial+intelligence+when:7d&hl=en-US&gl=US&ceid=US:en
```

---

## RSS Response Format

All feeds return **RSS 2.0 XML**. Here is the general structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
  <channel>
    <generator>NFE/5.0</generator>
    <title>Top stories - Google News</title>
    <link>https://news.google.com/?hl=en-US&amp;gl=US&amp;ceid=US:en</link>
    <language>en-US</language>
    <webMaster>news-webmaster@google.com</webMaster>
    <copyright>...</copyright>
    <lastBuildDate>Wed, 18 Feb 2026 20:50:00 GMT</lastBuildDate>
    <item>
      <title>Article headline - Publisher Name</title>
      <link>https://news.google.com/rss/articles/...</link>
      <guid isPermaLink="true">https://news.google.com/rss/articles/...</guid>
      <pubDate>Wed, 18 Feb 2026 19:05:07 GMT</pubDate>
      <description>
        <!-- HTML ordered list of related articles -->
        <ol>
          <li><a href="...">Article Title</a>&nbsp;&nbsp;<font color="#6f6f6f">Publisher</font></li>
          ...
        </ol>
      </description>
      <source url="https://publisher-domain.com">Publisher Name</source>
    </item>
    <!-- more <item> elements -->
  </channel>
</rss>
```

### Key Fields per `<item>`

| Field | Description |
|-------|-------------|
| `<title>` | Headline text followed by ` - Publisher Name` |
| `<link>` | Google News redirect URL. Visiting it in a browser redirects to the actual article. |
| `<guid>` | Unique identifier (same as `<link>`) |
| `<pubDate>` | Publication date in RFC 2822 format |
| `<description>` | HTML snippet containing an ordered list (`<ol>`) of related/clustered articles with links and publisher names |
| `<source url="...">` | Publisher name and homepage URL |

---

## Common Patterns

### Fetch Top Headlines (curl + grep)

```bash
curl -s "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en" \
  | grep -oP '<title>\K[^<]+'
```

### Fetch Top Headlines (Python)

```python
import feedparser

feed = feedparser.parse(
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
)

for entry in feed.entries:
    print(f"{entry.published} — {entry.title}")
    print(f"  Link: {entry.link}")
    print()
```

### Fetch Topic Feed (curl + xmllint)

```bash
TOPIC="CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB"
curl -s "https://news.google.com/rss/topics/${TOPIC}?hl=en-US&gl=US&ceid=US:en" \
  | xmllint --xpath '//item/title/text()' -
```

### Search for Articles (Python)

```python
import feedparser
import urllib.parse

query = urllib.parse.quote("artificial intelligence when:7d")
url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

feed = feedparser.parse(url)
for entry in feed.entries[:10]:
    print(f"• {entry.title}")
```

### Fetch News for a Specific Location (Node.js)

```javascript
const https = require("https");
const { parseStringPromise } = require("xml2js");

const url =
  "https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en";

https.get(url, (res) => {
  let data = "";
  res.on("data", (chunk) => (data += chunk));
  res.on("end", async () => {
    const result = await parseStringPromise(data);
    const items = result.rss.channel[0].item || [];
    items.slice(0, 10).forEach((item) => {
      console.log(item.title[0]);
    });
  });
});
```

### Extract Related Articles from Description (Python)

```python
import feedparser
from html.parser import HTMLParser

class RelatedParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = []
        self._in_a = False
        self._href = ""
        self._text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._in_a = True
            self._href = dict(attrs).get("href", "")
            self._text = ""

    def handle_endtag(self, tag):
        if tag == "a" and self._in_a:
            self.articles.append({"title": self._text, "link": self._href})
            self._in_a = False

    def handle_data(self, data):
        if self._in_a:
            self._text += data

feed = feedparser.parse(
    "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
)

for entry in feed.entries[:3]:
    print(f"\n=== {entry.title} ===")
    parser = RelatedParser()
    parser.feed(entry.description)
    for art in parser.articles:
        print(f"  • {art['title']}")
        print(f"    {art['link']}")
```

### Build a Multi-Region News Aggregator (Python)

```python
import feedparser

REGIONS = {
    "US":  "hl=en-US&gl=US&ceid=US:en",
    "UK":  "hl=en-GB&gl=GB&ceid=GB:en",
    "DE":  "hl=de&gl=DE&ceid=DE:de",
    "JP":  "hl=ja&gl=JP&ceid=JP:ja",
    "BR":  "hl=pt-BR&gl=BR&ceid=BR:pt-419",
}

for region, params in REGIONS.items():
    feed = feedparser.parse(f"https://news.google.com/rss?{params}")
    print(f"\n--- {region} Top 3 ---")
    for entry in feed.entries[:3]:
        print(f"  • {entry.title}")
```

### Monitor a Topic with Polling (bash)

```bash
#!/usr/bin/env bash
FEED="https://news.google.com/rss/search?q=breaking+news+when:1h&hl=en-US&gl=US&ceid=US:en"
SEEN_FILE="/tmp/gnews_seen.txt"
touch "$SEEN_FILE"

while true; do
  curl -s "$FEED" | grep -oP '<guid[^>]*>\K[^<]+' | while read -r guid; do
    if ! grep -qF "$guid" "$SEEN_FILE"; then
      echo "$guid" >> "$SEEN_FILE"
      TITLE=$(curl -s "$FEED" | grep -oP "<item>.*?<guid[^>]*>${guid}.*?</item>" \
        | grep -oP '<title>\K[^<]+' | head -1)
      echo "[NEW] $TITLE"
    fi
  done
  sleep 120
done
```

---

## Resolving Google News Redirect URLs

Article links in the RSS feed point to `https://news.google.com/rss/articles/...` which redirect (HTTP 302/303) to the actual publisher URL. To resolve the final URL:

### curl

```bash
curl -Ls -o /dev/null -w '%{url_effective}' \
  "https://news.google.com/rss/articles/CBMiWkFV..."
```

### Python

```python
import requests

response = requests.head(
    "https://news.google.com/rss/articles/CBMiWkFV...",
    allow_redirects=True,
    timeout=10,
)
print(response.url)  # final publisher URL
```

---

## Rate Limits

Google does not publish official rate limits for the RSS feeds. Based on community observations:

| Guideline | Recommendation |
|-----------|----------------|
| Polling interval | ≥ 60 seconds between requests for the same feed |
| Concurrent requests | Keep below ~10 concurrent connections |
| Burst behavior | Rapid bursts may trigger HTTP 429 or CAPTCHA challenges |
| User-Agent | Use a descriptive User-Agent; empty or bot-like strings may be blocked |

If you receive an HTTP 429 response, back off exponentially (e.g., 1 min → 2 min → 4 min).

---

## Error Handling

| HTTP Status | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Parse the RSS XML |
| 301/302 | Redirect | Follow the redirect (most HTTP clients do this automatically) |
| 404 | Feed not found | Check the URL, topic ID, or locale parameters |
| 429 | Rate limited | Back off and retry after a delay |
| 5xx | Server error | Retry with exponential backoff |

---

## Tips

- **No auth needed** — all feeds are fully public. Start fetching immediately.
- **Use `feedparser` in Python** — it handles RSS parsing, date normalization, and encoding edge cases.
- **Combine search modifiers** — `q=Tesla+site:reuters.com+when:30d` for precise results.
- **Topic IDs are locale-specific** — an English topic ID may not work with `hl=de`. Inspect the Google News page in that locale to find the correct ID.
- **The `<description>` field is HTML** — it contains clustered/related articles as an `<ol>` list. Parse the HTML to extract multiple sources per story.
- **The `<title>` includes the publisher** — the format is `Headline text - Publisher Name`. Split on ` - ` (space-dash-space) from the right to separate them.
- **Feed results are limited** — Google typically returns ~100 items per feed. Use search with date filters to paginate through older results.
- **Respect the copyright notice** — Google's RSS feeds are intended for personal, non-commercial use in feed readers. Review Google's terms for other uses.
- **Resolve redirects lazily** — only resolve the Google redirect URL to the publisher URL when you actually need the final link. This saves requests.
- **Set a proper User-Agent** — e.g., `User-Agent: MyNewsBot/1.0 (contact@example.com)`. Some environments may get blocked without one.

---

## Changelog

- **0.1.0** — Initial release with top stories, topic feeds, search feeds, multi-region support, and common usage patterns.