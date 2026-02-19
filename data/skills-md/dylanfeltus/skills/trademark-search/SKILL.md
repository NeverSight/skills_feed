---
name: trademark-search
description: Search the USPTO trademark database to check name availability and get registration details. Use when the user wants to check if a name is trademarked, research trademark availability, or look up registration status. No API key required.
---

# USPTO Trademark Search

Search the United States Patent and Trademark Office (USPTO) database to check trademark availability and get registration details. Uses web search as the primary method — most USPTO and trademark database sites block automated requests.

## When to Use

- User wants to check if a name/brand is trademarked
- User is researching trademark availability before naming a product
- User wants details on an existing trademark registration
- User asks "is [name] trademarked?" or "can I use [name]?"

## Important Disclaimer

**This skill provides informational data only — not legal advice.** Always recommend the user consult a trademark attorney for definitive guidance. Trademark availability depends on many factors beyond exact-match searches (similarity, likelihood of confusion, goods/services classes, etc.).

## Known Limitations

Direct `web_fetch` calls to trademark databases **will not work** — they block automated requests:

| Source | Direct Fetch | Status |
|--------|-------------|--------|
| tmsearch.uspto.gov | ❌ JS-rendered, no useful content | Blocked |
| tsdr.uspto.gov | ❌ Returns 403 | Blocked |
| trademarkia.com | ❌ Returns 403 | Blocked |
| branddb.wipo.int | ❌ JS-rendered | Blocked |

**Web search is the primary (and reliable) approach.** Search engines index these databases, so you can find trademark records through `web_search` queries with `site:` filters.

## Step 1: Web Search for Trademark Records (Primary Method)

Use `web_search` to find trademark registrations. This is the most reliable approach.

### Search USPTO Records

```
web_search: "BRAND_NAME" trademark site:tsdr.uspto.gov
```

```
web_search: "BRAND_NAME" trademark site:uspto.gov
```

### Search Trademarkia (Indexed by Search Engines)

```
web_search: "BRAND_NAME" site:trademarkia.com
```

Trademarkia results typically include: mark name, serial/registration number, status (LIVE/DEAD), owner, filing date, and Nice Classification class.

### Search Broadly

```
web_search: "BRAND_NAME" trademark registered
```

```
web_search: "BRAND_NAME" site:tmdn.org
```

### What to Look For in Results

- **TSDR links** (tsdr.uspto.gov/statusview/sn... or rn...) → existing trademark record with serial/registration number
- **Trademarkia listings** → status, owner, class, filing/registration dates
- **Company websites** claiming "®" or "™" → claimed/registered marks
- **Nice Classification class** for goods/services — critical for determining if a mark conflicts with your intended use

## Step 2: Extract Details from Search Results

Search results from Trademarkia and USPTO typically contain enough detail in the snippet:

- **Mark name** and any design description
- **Serial number** (application) or **Registration number**
- **Status:** LIVE (active) or DEAD (abandoned/cancelled/expired)
- **Owner name**
- **Class(es)** of goods/services
- **Filing and registration dates**

If you need more detail, try fetching the specific Trademarkia result URL — some individual pages may load, though the search pages are blocked.

### Key Status Values

| Status | Meaning |
|--------|---------|
| **LIVE** | Active trademark — registered or pending |
| **DEAD** | Abandoned, cancelled, or expired |
| **Registered** | Fully registered and active |
| **Published for Opposition** | Pending — 30-day window for objections |
| **Abandoned** | Application was abandoned |
| **Cancelled** | Registration was cancelled |
| **Expired** | Registration expired (not renewed) |

## Step 3: Check International Marks (Optional)

For products with international reach, also search:

```
web_search: "BRAND_NAME" trademark site:branddb.wipo.int
```

```
web_search: "BRAND_NAME" trademark international WIPO
```

## Trademark Classes (Nice Classification)

When reporting results, include the goods/services class:

| Class | Category |
|-------|----------|
| 9 | Software, apps, electronics |
| 25 | Clothing, footwear |
| 35 | Advertising, business management |
| 36 | Financial services, insurance |
| 41 | Education, entertainment |
| 42 | Software design, SaaS, tech services |

A trademark only protects within its registered class(es). A name can be registered by different entities in different classes.

## Output Format

### Availability Check

```
### Trademark Search: "BRAND NAME"

**⚠️ Disclaimer:** This is an informational search only, not legal advice. Consult a trademark attorney before making business decisions.

#### Findings

**Exact Matches Found:** Yes/No

1. **BRAND NAME** — Registration #1234567
   Status: 🟢 LIVE / Registered
   Owner: Company Name, Inc.
   Filed: Jan 15, 2020 · Registered: Aug 3, 2020
   Class: 9 (Software), 42 (SaaS)
   Goods/Services: "Computer software for project management..."
   🔗 https://tsdr.uspto.gov/statusview/rn1234567

2. **BRAND NAME** — Serial #90123456
   Status: 🔴 DEAD / Abandoned
   Owner: Other Company LLC
   Filed: Mar 1, 2019 · Abandoned: Sep 15, 2019
   Class: 35 (Business services)

#### Similar Marks Found
- BRAND NAYME — Reg #2345678 (Class 9, LIVE)
- BRANDNAME — Reg #3456789 (Class 42, LIVE)

#### Assessment
- [Summary of what was found]
- [Note relevant classes vs user's intended use]
- [Recommend next steps]
```

### Quick Check

```
### Trademark: "BRAND NAME"

✅ No exact matches found in USPTO database.
⚠️ Similar marks exist: [list]
📋 Recommended classes to check: 9, 42 (if software)

**Next steps:** Consider a comprehensive search with a trademark attorney before filing.
```

## Error Handling

- **No results from web search:** This doesn't mean the name is available — it may not be indexed yet, or it may be too new. Note this uncertainty.
- **Conflicting info across sources:** Trademarkia may lag behind USPTO. When in doubt, note the discrepancy and recommend checking the official USPTO site directly.
- **Too many results:** Narrow with class filters or add the specific goods/services category to the search query.

## Important Caveats to Always Mention

1. **Common law trademarks** exist without registration — a name can be "taken" even if not in the USPTO database
2. **State registrations** are separate from federal (USPTO) registrations
3. **International marks** may conflict — check WIPO if relevant
4. **Likelihood of confusion** matters — similar (not just identical) marks can conflict
5. **Class matters** — same name can coexist in different goods/services classes
6. **This is not legal advice** — always recommend consulting a trademark attorney

## Examples

### Example 1: "Is 'Stellar' trademarked?"

1. `web_search: "Stellar" trademark site:tsdr.uspto.gov`
2. `web_search: "Stellar" site:trademarkia.com`
3. Review search result snippets for serial/registration numbers, status, class
4. Present findings with class info and assessment

### Example 2: "Can I use 'NovaPay' for a fintech app?"

1. `web_search: "NovaPay" trademark`
2. `web_search: "NovaPay" site:trademarkia.com`
3. Check results for marks in Class 9 (software) and Class 36 (financial services)
4. Present findings and note relevant classes for fintech

### Example 3: "Check trademark status for registration number 5678901"

1. `web_search: USPTO trademark registration 5678901`
2. Look for TSDR or Trademarkia links in results with status details
3. Present the current status, owner, and class information

## Data Sources

All accessed via `web_search` (direct fetch is blocked by these sites):

- **USPTO Trademark Search:** [tmsearch.uspto.gov](https://tmsearch.uspto.gov/) — Official US trademark database
- **USPTO TSDR:** [tsdr.uspto.gov](https://tsdr.uspto.gov/) — Status and document retrieval
- **Trademarkia:** [trademarkia.com](https://www.trademarkia.com/) — User-friendly trademark search
- **WIPO Global Brand Database:** [branddb.wipo.int](https://branddb.wipo.int/) — International trademarks
