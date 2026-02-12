---
name: linkup-search
description: "Use this skill whenever the agent has access to Linkup web search or fetch tools. Teaches the agent how to reason about query construction, choose search depth, write effective queries, select the right output type, use the fetch endpoint, and apply advanced techniques like sequential search and multi-query coverage. Applicable to any task involving web search, content extraction, company research, news retrieval, data enrichment, or real-time information gathering via Linkup."
---

This skill teaches you how to use Linkup's search and fetch tools effectively. Linkup is an agentic web search API — it interprets natural language instructions and executes retrieval steps to return accurate, real-time web data. Read this skill before making any Linkup search or fetch call.

---

## 1. How to Construct a Query

Your Linkup query should focus on **data retrieval**, not answer generation. Tell Linkup what to find and where to look. Do the reasoning and synthesis yourself after receiving the results.

Before writing your query, reason through three questions in order. Each answer constrains the next.

### Step 1: What inputs do I already have?

| I have... | Then... |
| --- | --- |
| A specific URL | Scrape it directly — don't waste a search finding it |
| A company name, topic, or question (no URL) | You'll need to search |
| Both a URL and a broader question | Combine: scrape the known URL + search for the rest |

### Step 2: Where does the data I need live?

| The data I need is... | Example | Then... |
| --- | --- | --- |
| In search snippets (titles, short excerpts, factual claims) | A funding amount, a launch date, a job title | `standard` is enough — snippets will contain the answer |
| On full web pages (tables, detailed specs, long-form content) | A pricing table, a job listing, an article's body text | You need to **scrape** the page |
| I'm not sure | — | Default to `deep` |

### Step 3: Do I need to chain steps sequentially?

| Scenario | Sequential? | Depth |
| --- | --- | --- |
| All the information can be gathered in parallel searches | No | `standard` |
| I have one URL and just need to scrape it | No | `standard` (one URL) or `/fetch` |
| I need to find URLs first, then scrape them | Yes | `deep` |
| I need to scrape a page, then search again based on what I found | Yes | `deep` |
| I need to scrape multiple known URLs | Yes | `deep` |

When uncertain, default to `deep`.

### Worked Examples

```
Inputs: company name only, no URL
Data needed: pricing details (lives on a full page, not in snippets)
Sequential: yes — need to find the pricing page first, then scrape it
→ depth="deep"
→ query: "Find the pricing page for {company}. Scrape it. Extract plan names, prices, and features."
```

```
Inputs: company name only, no URL
Data needed: latest funding round amount (lives in search snippets)
Sequential: no
→ depth="standard"
→ query: "Find {company}'s latest funding round amount and date"
```

```
Inputs: a specific URL (https://example.com/pricing)
Data needed: pricing details from that page
Sequential: no — I already have the URL
→ depth="standard" or /fetch
→ query: "Scrape https://example.com/pricing. Extract plan names, prices, and included features."
```

```
Inputs: a company name
Data needed: the company's ICP, inferred from homepage + blog + case studies
Sequential: yes — need to find pages, then scrape them, then synthesize
→ depth="deep"
→ query: "Find and scrape {company}'s homepage, use case pages, and 2-3 recent blog posts. Extract: industries mentioned, company sizes referenced, job titles targeted, and pain points addressed."
```

---

## 2. Choosing Search Depth

Linkup supports two search depths. Your answers from Section 1 determine which to use.

### Standard (`depth="standard"`) — €0.005/call

- Can run multiple parallel web searches if instructed
- Can scrape **one** URL if provided in the prompt
- Cannot scrape multiple URLs
- Cannot use URLs discovered in search results to scrape them

### Deep (`depth="deep"`) — €0.05/call

- Executes up to 10 iterative retrieval passes, each aware of prior context
- Can scrape multiple URLs
- Can use URLs discovered in search results to scrape them
- Supports sequential instructions (outputs from one step feed the next)

> **When uncertain, default to `deep`.**

**Cost tip:** 3–5 parallel `standard` calls with focused sub-queries is often faster and cheaper than one `deep` call. Reserve `deep` for when you need to scrape multiple URLs or chain search → scrape.

---

## 3. Choosing Output Type

| Output Type | Returns | Use When |
| --- | --- | --- |
| `searchResults` | Array of `{name, url, content}` | You need raw sources to reason over, filter, or synthesize yourself |
| `sourcedAnswer` | Natural language answer + sources | The answer will be shown directly to a user (chatbot, Q&A) |
| `structured` | JSON matching a provided schema | Results feed into automated pipelines, CRM updates, data enrichment |

**Default choice:** Use `searchResults` when you will process the results. Use `sourcedAnswer` when the user needs a direct answer. Use `structured` when downstream code needs to parse the output.

---

## 4. Writing Effective Queries

Rule of thumb: The level of complexity and the choice of depth of your query ofen depends on the use case:
- Conversational chatbot where low latency is important: keep prompts simples, keyword style, standard depth
- Deep researcher: more detailed more, leverage scraping, deep depth

### Be specific

| Bad | Good |
| --- | --- |
| "Tell me about the company" | "Find {company}'s annual revenue and employee count" |
| "Microsoft revenue" | "Microsoft fiscal year 2024 total revenue" |
| "React hooks" | "React useEffect cleanup function best practices" |
| "AI news" | "OpenAI product announcements January 2026" |

**Add context:** dates ("Q4 2025"), locations ("French company Total"), versions ("since React 19"), domains ("on sec.gov").

### Keyword-style for simple lookups

Short keyword queries work fine for straightforward facts:

```
"Bitcoin price today"
"NVIDIA Q4 2024 revenue"
"Anthropic latest funding round"
```

### Instruction-style for complex extraction

When you need specific extraction or multi-step retrieval, write your query as a natural language instruction — what to find, where to look, what to extract:

```
"Find Datadog's current pricing page. Extract plan names, per-host prices, and included features for each tier."
```

```
"Find Acme Corp's investor relations page on acme.com. Extract the most recent quarterly revenue figure and year-over-year growth rate."
```

### Request parallel searches for breadth

For broad research, explicitly ask for multiple passes. This works even in `standard`:

```
"Find recent news about OpenAI. Run several searches with adjacent keywords including 'OpenAI funding', 'OpenAI product launch', and 'OpenAI partnership announcements'."
```

Or issue 3–5 separate `standard` calls from your agent, each with a focused sub-query:
```
Query 1: "Datadog current annual recurring revenue from latest earnings"
Query 2: "Datadog number of customers over $100k ARR"
Query 3: "Datadog net revenue retention rate from investor presentations"
```

### Sequential instructions (deep only)

When you need to discover a URL then extract from it, be explicit about the sequence:

```
"First, find the LinkedIn company page for Snowflake. Then scrape the page and extract: employee count, headquarters, industry, and company description."
```

### Scrape a known URL (standard: one URL max)

If you already have a URL, include it in the prompt. In `standard`, this is limited to **one URL per call**:

```
"Scrape https://example.com/pricing. Extract all plan names, prices, and feature lists."
```

You can combine one scrape + search in a single `standard` call:

```
"Scrape https://linkup.so. Also search for articles mentioning Linkup clients. Return a list of known clients with the source of each."
```

To scrape **multiple URLs**, or to scrape URLs discovered during search, use `deep`.

---

## 5. Using the `/fetch` Endpoint

When your agent already knows the exact URL, use `/fetch` instead of `/search`. It's faster, cheaper, and purpose-built for single-page extraction.

| Use `/fetch` when... | Use `/search` when... |
| --- | --- |
| You have a specific URL and want its content as markdown | You don't know which URL has the answer |
| You're scraping a known page (pricing, article, docs) | You need results from multiple pages |
| Your agent found a URL in a previous step and needs to read it | You need Linkup's agentic retrieval to find and extract |

**Default to `renderJs: true`.** Many sites load content via JavaScript. The latency tradeoff is almost always worth the reliability gain.

---

## 6. Advanced Techniques

### LinkedIn extraction (if you have the LinkedIn URL of the person/company/post -> standard)

- return the linkedin profile details of {{linkedin_url}} 
- return the last 10 linkedin posts of {{linkedin_url}} 
- return the last 10 linkedin comments of {{linkedin_url}}
- extracts the comments from {{linkedin_post_url}}

### LinkedIn extraction (if you need to search for the LinkedIn URL first -> deep)

```
First find LinkedIn posts about context engineering.
Then, for each URL, extract the post content and comments.
Return the LinkedIn profile URL of each commenter.
```

### Date filtering and domain filtering

Use `fromDate` and `toDate` to limit results to a time window:

```
Query: "Find news about Anthropic product launches"
fromDate: "2025-01-01"
toDate: "2025-03-31"
```

Use `includeDomains` to focus on specific sources, or `excludeDomains` to remove noise:

```
Query: "Find Tesla's latest quarterly earnings data"
includeDomains: ["tesla.com", "sec.gov"]
```

Instructions: for both domain filtering and date filtering, only use if implicitly or explicitly instructed to do so.

## 7. MCP Setup

Two tools: `linkup-search` (query, depth) and `linkup-fetch` (url, renderJs).

| Client | Setup |
|--------|-------|
| **VS Code / Cursor** | Add to MCP config: `{"servers":{"linkup":{"url":"https://mcp.linkup.so/mcp?apiKey=YOUR_API_KEY","type":"http"}}}` |
| **Claude Code** | `claude mcp add --transport http linkup https://mcp.linkup.so/mcp?apiKey=YOUR_API_KEY` |
| **Claude Desktop** | Download [MCPB bundle](https://github.com/LinkupPlatform/linkup-mcp-server/releases/latest/download/linkup-mcp-server.mcpb), double-click to install |

Auth format (v2.x): `apiKey=YOUR_API_KEY` in args. Old v1.x `env` format no longer works.

---

## Quick Reference

```
STANDARD:  €0.005. Parallel searches ✓  Scrape one provided URL ✓  Scrape multiple URLs ✗  Chain search→scrape ✗
DEEP:      €0.05.  Iterative searches ✓  Scrape multiple URLs ✓   Chain search→scrape ✓
UNCERTAIN: Default to deep.
OUTPUT:    searchResults (raw sources)  |  sourcedAnswer (natural language)  |  structured (JSON schema)
FETCH:     Single known URL → /fetch with renderJs: true
QUERIES:   Keyword for simple lookups. Instruction-style for complex extraction. Be specific.
COVERAGE:  "Run several searches with adjacent keywords" for breadth (works in standard).
CHAINING:  "First find X, then scrape X" — deep only.
```
