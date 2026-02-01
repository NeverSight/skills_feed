---
name: google-search
description: MUST use when searching the web. Use for researching topics, finding discussions on Hacker News/Reddit/Stack Overflow, looking up academic papers, comparing tools or libraries, investigating error messages, or needing precise search filtering.
---

# Google Search Operators

## Overview

Use these operators to refine search queries, filter results, and find specific information quickly. Stop guessing and start searching with precision.

**Important**: Use the native `WebSearch` tool to perform searches. Do NOT use browser automation (Playwright, navigate, browser tools) for searching.

## Research Patterns by Source

Use `site:` to target specific platforms. Combine with other operators for precision.

### Developer Communities

| Source | Pattern | Example |
|--------|---------|---------|
| **Hacker News** | `site:news.ycombinator.com {topic}` | `site:news.ycombinator.com "vector database" after:2024` |
| **Stack Overflow** | `site:stackoverflow.com {error OR topic}` | `site:stackoverflow.com "Cannot read property" react hooks` |
| **Reddit** | `site:reddit.com {topic}` | `site:reddit.com "best practices" typescript monorepo` |
| **Dev.to** | `site:dev.to {topic}` | `site:dev.to "building cli tools" rust` |

### Code & Issues

| Source | Pattern | Example |
|--------|---------|---------|
| **GitHub Issues** | `site:github.com inurl:issues {topic}` | `site:github.com inurl:issues memory leak nextjs` |
| **GitHub Discussions** | `site:github.com inurl:discussions {topic}` | `site:github.com inurl:discussions "best approach" prisma` |
| **GitHub README** | `site:github.com inurl:blob {filename}` | `site:github.com inurl:blob package.json "workspaces"` |
| **Gist** | `site:gist.github.com {topic}` | `site:gist.github.com dockerfile python` |

### Documentation & Learning

| Source | Pattern | Example |
|--------|---------|---------|
| **MDN** | `site:developer.mozilla.org {api}` | `site:developer.mozilla.org IntersectionObserver` |
| **Official Docs** | `site:{library}.dev OR site:{library}.io {topic}` | `site:react.dev useEffect cleanup` |
| **Wikipedia** | `site:wikipedia.org {topic}` | `site:wikipedia.org "distributed systems" consensus` |

### Academic & Research

| Source | Pattern | Example |
|--------|---------|---------|
| **arXiv** | `site:arxiv.org {topic} {year..year}` | `site:arxiv.org "transformer architecture" 2023..2025` |
| **Google Scholar** | `site:scholar.google.com {topic}` | `site:scholar.google.com "retrieval augmented generation"` |
| **ACM** | `site:dl.acm.org {topic}` | `site:dl.acm.org "program synthesis"` |
| **IEEE** | `site:ieeexplore.ieee.org {topic}` | `site:ieeexplore.ieee.org "edge computing"` |

### Product & Tool Research

| Source | Pattern | Example |
|--------|---------|---------|
| **Product Hunt** | `site:producthunt.com {category}` | `site:producthunt.com "developer tools" api` |
| **AlternativeTo** | `site:alternativeto.net {tool}` | `site:alternativeto.net figma` |
| **G2/Capterra** | `site:g2.com OR site:capterra.com {tool}` | `site:g2.com "project management" comparison` |

### News & Analysis

| Source | Pattern | Example |
|--------|---------|---------|
| **TechCrunch** | `site:techcrunch.com {company OR topic}` | `site:techcrunch.com "series a" ai startup after:2024` |
| **The Verge** | `site:theverge.com {topic}` | `site:theverge.com apple vision pro review` |
| **Ars Technica** | `site:arstechnica.com {topic}` | `site:arstechnica.com security vulnerability` |

## Common Research Scenarios

### "What do people think about X?"

```
site:news.ycombinator.com OR site:reddit.com "{tool/library}" after:2024
```

### "How do I fix this error?"

```
site:stackoverflow.com OR site:github.com inurl:issues "{exact error message}"
```

### "What are alternatives to X?"

```
site:alternativeto.net OR site:reddit.com "{tool}" alternatives
```

### "Latest research on X"

```
site:arxiv.org "{topic}" 2024..2025
```

### "Official documentation for X"

```
site:{library}.dev OR site:{library}.io OR site:docs.{library}.com {feature}
```

### "Real-world experience with X"

```
site:reddit.com OR site:news.ycombinator.com "{tool}" "in production" OR "experience"
```

source: https://docs.google.com/document/d/1ydVaJJeL1EYbWtlfj9TPfBTE5IBADkQfZrQaBZxqXGs/edit?tab=t.0

## Content Operators

Target specific parts of a webpage (title, URL, text, or anchor links).

### Behavior of `allin...` vs `in...` prefixes

- **`allin...`** (e.g., `allintitle:`): Applies to **all** subsequent terms in the query. Do not mix with other operators.
- **`in...`** (e.g., `intitle:`): Applies **only** to the term immediately following it.

### Operators

| Operator                     | Scope       | Syntax Example                 | Description                                            |
| :--------------------------- | :---------- | :----------------------------- | :----------------------------------------------------- |
| `intitle:` / `allintitle:`   | Page Title  | `intitle:help flu shot`        | Finds "help" in the title and "flu", "shot" anywhere.  |
| `intext:` / `allintext:`     | Page Text   | `allintext:camping tent stove` | Finds "camping", "tent", and "stove" in the body text. |
| `inurl:` / `allinurl:`       | URL         | `allinurl:google faq`          | Finds "google" and "faq" in the URL path.              |
| `inanchor:` / `allinanchor:` | Anchor Text | `allinanchor:best restaurant`  | Finds pages linked to with the text "best restaurant". |

## Logic & Filtering

Refine matches using logic, exclusion, and proximity.

### Exact Match (`""`)

Forces an exact phrase match. Prevents synonym expansion (e.g., `"ca"` won't match "California").

- **Syntax**: `"search query"`
- **Example**: `"Alexander Bell"` (Excludes "Alexander G. Bell")

### Wildcard (`*`)

Placeholder for any unknown term (up to 5 words) or URL token. Works best within quotes.

- **Syntax**: `term * term`
- **Example**: `"Google * products"` or `site:www.*creative.com` (matches prefixes like `av-creative`)

### Exclusion (`-`)

Excludes pages containing a specific term or matching a specific operator. Place immediately before the term/operator.

- **Syntax**: `term -exclusion`
- **Example**: `jaguar -cars -football` or `salsa -tomatoes`

### Boolean OR (`OR`)

Matches either term. Must be uppercase.

- **Syntax**: `term1 OR term2`
- **Example**: `mesothelioma OR "lung disease"`

### Combinations

Combine operators for complex filtering.

- **Syntax**: `term OR term -exclusion site:domain`
- **Example**: `salsa recipe -tomatoes -filetype:pdf` (Salsa recipes without tomatoes, excluding PDFs)
- **Example**: `article security -site:wikipedia.org` (Security articles excluding Wikipedia)

### Proximity (`AROUND`)

Finds terms within a specified number of words of each other. Order is not preserved.

- **Syntax**: `term1 AROUND n term2`
- **Example**: `search AROUND 3 engine`

### Number Range (`..`)

Finds numbers in a range (prices, years, measurements).

- **Syntax**: `number..number`
- **Example**: `DVD player $50..$100` or `1950..1960`

## Metadata & Source Operators

Filter by domain, file type, date, or definition.

### Site (`site:`)

Restricts results to a specific domain or TLD.

- **Syntax**: `site:domain.com`
- **Example**: `tax site:.hk` (Hong Kong TLD)

### File Type (`filetype:`)

Restricts results to pages ending in a specific suffix.

- **Syntax**: `filetype:suffix query`
- **Example**: `filetype:pdf "search engine guidelines"`
- **Note**: `filetype:csv` is deindexed (use Google Dataset Search). `filetype:mp3` works via `inurl:mp3`.

### Date (`before:` / `after:`)

Finds results published before or after a date (YYYY-MM-DD). Defaults to Jan 1 if only year provided.

- **Syntax**: `after:2020-01-01`
- **Example**: `avengers after:2020`

### Definition (`define`)

Shows the dictionary definition of a word or phrase.

- **Syntax**: `define term`
- **Example**: `define peruse` or `define Hobson's choice`

## Special Characters

Google supports specific special characters in search:

- **Symbols**: `$`, `%`, `#`, `∞` (e.g., `$50`, `24%`, `#cute`).
- **Time/Verses**: `:` (e.g., `10:27`).
- **Math**: `+` at the end (e.g., `C++`, `40+`), `½` (synonymized to 0.5).
- **Emoji**: Fully searchable (e.g., `🍺 pub`, `I ❤ NY`).

## Powerful Search Idioms

Combine operators for precise extraction.

### 1. Find Subdomains

Exclude the `www` subdomain to find other hosts.

- **Query**: `site:nyc.gov -site:www.nyc.gov`

### 2. Strict Pattern Matching

Use wildcards inside quotes to enforce word order with variable gaps.

- **Query**: `"whenever * says * whenever"`

### 3. Wildcard Subdomains & Tokens

Find specific subdomain patterns. `*` matches any token or prefix string (except TLD).

- **Query**: `site:*.law.*.edu`
- **Query**: `site:www.*creative.com` (Matches `av-creative.com`)

## Nuances & Limitations

- **Parentheses**: Ignored by Google. Do not use for grouping logic (e.g., `(A OR B) C` is treated as `A OR B C`). Run separate searches instead.
- **Word Order**: Matters. `to be or not to be` yields different results than `be to not or be to`.
- **Fraction Synonyms**: Characters like `½` are synonymized (e.g., `size 7½` matches `7.5`). Use quotes for exact match: `"size 7½"`.

## Advanced Search UI

Some features are only available via the [Advanced Search page](http://www.google.com/advanced_search) and have no operator equivalents:

- **Usage Rights**: Filter by Creative Commons license.
- **Reading Level**: Filter by Basic, Intermediate, or Advanced.
- **Language**: Filter by specific language (e.g., Spanish, Chinese).

## Deprecated Operators (Do Not Use)

These operators no longer function or are unreliable:

- `related:` (Deprecated June 2023)
- `link:` (Removed 2016)
- `info:` (Removed 2017)
- `+` as a prefix (Use quotes for exact match)
- `~` (Synonym operator - now automatic)
- `daterange:` (Use `before:`/`after:`)
