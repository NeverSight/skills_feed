---
name: semrush-research
description: >
  SEO and competitive intelligence via the SemRush API. Use when asked to
  research competitors, analyze domains, find keyword opportunities, check
  backlinks, or estimate traffic. Trigger phrases: "competitor analysis",
  "domain overview", "keyword research", "backlink check", "traffic estimate",
  "SEO intelligence", "semrush", "competitive research".
---

# SemRush Research

Pull live SEO and competitive intelligence data from the SemRush API.

## Prerequisites

Requires `SEMRUSH_API_KEY` set in `.env`, `.env.local`, or `~/.claude/.env.global`.

```bash
# Verify the key is available
echo "SEMRUSH_API_KEY is ${SEMRUSH_API_KEY:+set}"
```

If the key is not set, instruct the user:
> You need a SemRush API key. Get one at https://www.semrush.com/api/
> Then add `SEMRUSH_API_KEY=your_key` to your `.env` file.

## API Base

All requests go to `https://api.semrush.com/` with the API key passed as `&key={SEMRUSH_API_KEY}`.

Responses are semicolon-delimited CSV. The first line is the header row. Parse accordingly.

---

## 1. Domain Overview

Get a high-level snapshot of any domain's organic and paid search performance.

### Endpoint

```
https://api.semrush.com/?type=domain_ranks&key={KEY}&export_columns=Dn,Rk,Or,Ot,Oc,Ad,At,Ac&domain={domain}
```

### Export Columns

| Column | Meaning |
|--------|---------|
| `Dn` | Domain |
| `Rk` | SemRush Rank |
| `Or` | Organic keywords count |
| `Ot` | Organic traffic estimate |
| `Oc` | Organic traffic cost ($) |
| `Ad` | Paid keywords count |
| `At` | Paid traffic estimate |
| `Ac` | Paid traffic cost ($) |

### Example curl

```bash
curl -s "https://api.semrush.com/?type=domain_ranks&key=${SEMRUSH_API_KEY}&export_columns=Dn,Rk,Or,Ot,Oc,Ad,At,Ac&domain=example.com"
```

### Parsing the Response

```bash
# Response format (semicolon-delimited):
# Dn;Rk;Or;Ot;Oc;Ad;At;Ac
# example.com;12345;8234;145000;234500;120;3400;5600

# Parse with awk
curl -s "..." | awk -F';' 'NR==2 {
  printf "Domain: %s\nSemRush Rank: %s\nOrganic Keywords: %s\nOrganic Traffic: %s\nOrganic Traffic Cost: $%s\nPaid Keywords: %s\nPaid Traffic: %s\nPaid Traffic Cost: $%s\n",
  $1,$2,$3,$4,$5,$6,$7,$8
}'
```

---

## 2. Keyword Overview

Get search volume, CPC, competition, and SERP features for a keyword.

### Endpoint

```
https://api.semrush.com/?type=phrase_all&key={KEY}&phrase={keyword}&database=us&export_columns=Ph,Nq,Cp,Co,Nr,Td
```

### Export Columns

| Column | Meaning |
|--------|---------|
| `Ph` | Keyword phrase |
| `Nq` | Search volume (monthly) |
| `Cp` | CPC (USD) |
| `Co` | Competition (0-1) |
| `Nr` | Number of results |
| `Td` | Trend (12 months, comma-separated) |

### Example curl

```bash
curl -s "https://api.semrush.com/?type=phrase_all&key=${SEMRUSH_API_KEY}&phrase=content+marketing&database=us&export_columns=Ph,Nq,Cp,Co,Nr,Td"
```

### Supported Databases

Use `&database=XX` where XX is: `us`, `uk`, `ca`, `au`, `de`, `fr`, `es`, `it`, `br`, `in`, `jp`.

---

## 3. Related Keywords

Find semantically related keywords for content planning and gap analysis.

### Endpoint

```
https://api.semrush.com/?type=phrase_related&key={KEY}&phrase={keyword}&database=us&export_columns=Ph,Nq,Cp,Co,Nr,Td&display_limit=20
```

### Example curl

```bash
curl -s "https://api.semrush.com/?type=phrase_related&key=${SEMRUSH_API_KEY}&phrase=project+management&database=us&export_columns=Ph,Nq,Cp,Co,Nr,Td&display_limit=20"
```

### Parsing Multiple Rows

```bash
curl -s "..." | awk -F';' 'NR>1 { printf "%-40s Vol: %-8s CPC: $%-6s Comp: %s\n", $1, $2, $3, $4 }'
```

---

## 4. Keyword Difficulty

Estimate how hard it is to rank for a keyword.

### Endpoint

```
https://api.semrush.com/?type=phrase_kdi&key={KEY}&phrase={keyword}&database=us&export_columns=Ph,Kd
```

| Column | Meaning |
|--------|---------|
| `Ph` | Keyword |
| `Kd` | Keyword difficulty (0-100) |

Interpretation:
- 0-29: Easy - achievable with quality content
- 30-49: Moderate - needs solid content + some backlinks
- 50-69: Hard - needs strong domain authority + backlinks
- 70-84: Very hard - requires established authority
- 85-100: Extremely hard - dominated by top-tier domains

---

## 5. Domain Organic Keywords

See which keywords a domain ranks for organically.

### Endpoint

```
https://api.semrush.com/?type=domain_organic&key={KEY}&domain={domain}&database=us&export_columns=Ph,Po,Nq,Cp,Url,Tr,Tc&display_limit=50&display_sort=tr_desc
```

| Column | Meaning |
|--------|---------|
| `Ph` | Keyword |
| `Po` | Position |
| `Nq` | Search volume |
| `Cp` | CPC |
| `Url` | Ranking URL |
| `Tr` | Traffic (%) |
| `Tc` | Traffic cost |

### Example curl

```bash
curl -s "https://api.semrush.com/?type=domain_organic&key=${SEMRUSH_API_KEY}&domain=hubspot.com&database=us&export_columns=Ph,Po,Nq,Cp,Url,Tr,Tc&display_limit=20&display_sort=tr_desc"
```

---

## 6. Backlink Overview

Get a summary of a domain's backlink profile.

### Endpoint

```
https://api.semrush.com/analytics/v1/?key={KEY}&type=backlinks_overview&target={domain}&target_type=root_domain&export_columns=total,domains_num,urls_num,ips_num,follows_num,nofollows_num,texts_num,images_num
```

### Example curl

```bash
curl -s "https://api.semrush.com/analytics/v1/?key=${SEMRUSH_API_KEY}&type=backlinks_overview&target=example.com&target_type=root_domain&export_columns=total,domains_num,urls_num,ips_num,follows_num,nofollows_num,texts_num,images_num"
```

---

## 7. Competitor Discovery

Find domains competing for the same organic keywords.

### Endpoint

```
https://api.semrush.com/?type=domain_organic_organic&key={KEY}&domain={domain}&database=us&export_columns=Dn,Cr,Np,Or,Ot,Oc,Ad&display_limit=10
```

| Column | Meaning |
|--------|---------|
| `Dn` | Competitor domain |
| `Cr` | Competition level |
| `Np` | Common keywords |
| `Or` | Organic keywords |
| `Ot` | Organic traffic |
| `Oc` | Organic traffic cost |
| `Ad` | Paid keywords |

### Example curl

```bash
curl -s "https://api.semrush.com/?type=domain_organic_organic&key=${SEMRUSH_API_KEY}&domain=notion.so&database=us&export_columns=Dn,Cr,Np,Or,Ot,Oc,Ad&display_limit=10"
```

---

## 8. Traffic Analytics (Estimates)

Estimate a domain's overall traffic sources and engagement.

### Endpoint

```
https://api.semrush.com/analytics/ta/api/v3/summary?key={KEY}&targets={domain}&display_date=2024-01-01&country=us&export_columns=target,visits,users,bounce_rate,pages_per_visit,avg_visit_duration
```

---

## Workflow: Full Competitive Analysis

When the user asks for a full competitive analysis, run these steps in order:

1. **Domain Overview** - Get the target domain's metrics
2. **Competitor Discovery** - Find top 5-10 competitors
3. **Domain Overview** for each competitor - Compare metrics
4. **Top Keywords** for each domain - Find keyword gaps
5. **Backlink Overview** for each domain - Compare link profiles

### Output Format

Present results as a comparison table:

```
| Metric              | target.com | competitor1.com | competitor2.com |
|---------------------|-----------|-----------------|-----------------|
| SemRush Rank        | ...       | ...             | ...             |
| Organic Keywords    | ...       | ...             | ...             |
| Organic Traffic     | ...       | ...             | ...             |
| Traffic Cost        | ...       | ...             | ...             |
| Backlinks           | ...       | ...             | ...             |
| Referring Domains   | ...       | ...             | ...             |
```

Then highlight:
- **Keyword gaps**: Keywords competitors rank for but target does not
- **Quick wins**: Keywords where target ranks positions 5-20 (improvement opportunities)
- **Content gaps**: Topics competitors cover but target does not
- **Backlink opportunities**: Sites linking to competitors but not target

## Rate Limits and Costs

- Each API call costs API units (check your plan)
- Use `&display_limit=` to control result count (default varies by endpoint)
- Cache results locally when doing multi-step analysis to avoid redundant calls
- Domain overview calls are cheapest; backlink and traffic analytics cost more

## Error Handling

| Error | Meaning |
|-------|---------|
| `ERROR 50 :: NOTHING FOUND` | No data for this query |
| `ERROR 120 :: WRONG KEY` | Invalid API key |
| `ERROR 130 :: LIMIT EXCEEDED` | API unit limit reached |
| Empty response | Usually means no data available for the query parameters |

When you get "NOTHING FOUND", try:
- Different database (e.g., `uk` instead of `us`)
- Root domain instead of subdomain
- Broader keyword phrase
