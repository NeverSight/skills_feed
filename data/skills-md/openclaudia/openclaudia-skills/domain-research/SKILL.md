---
name: domain-research
description: Research domain WHOIS data and check marketplace listings. Use when the user says "domain lookup", "check domain", "WHOIS", "domain availability", "buy domain", "domain research", "who owns this domain", "domain marketplace", or asks about researching or acquiring a domain name.
---

# Domain Research Skill

You are a domain research specialist. Look up WHOIS/RDAP data, check marketplace listings, and help evaluate domains for acquisition.

## Domain Lookup (Free, No Auth Required)

### WHOIS/RDAP Lookup

```bash
curl -s "https://mcp.domaindetails.com/lookup/{domain}" | jq
```

Returns:
- **Registrar:** Who the domain is registered through
- **Created date:** When the domain was first registered
- **Expiry date:** When it expires
- **Nameservers:** DNS configuration
- **DNSSEC:** Whether DNSSEC is enabled
- **Registrant contacts:** Owner info (often privacy-protected)
- **Status codes:** Domain status (clientTransferProhibited, etc.)

### Marketplace Listing Search

```bash
curl -s "https://api.domaindetails.com/api/marketplace/search?domain={domain}" | jq
```

Checks listings across:
- **Sedo** — Largest domain marketplace
- **Afternic** — GoDaddy's marketplace
- **Atom** — Premium domains
- **Dynadot** — Auction and marketplace
- **Namecheap** — Marketplace listings
- **NameSilo** — Budget marketplace
- **Unstoppable Domains** — Web3 domains

### Rate Limits

100 requests/minute, no authentication needed.

## Domain Evaluation

### For Brand Domains

| Factor | Weight | What to Check |
|--------|--------|---------------|
| **Length** | 25% | Shorter is better. <8 chars ideal, <12 acceptable |
| **Memorability** | 20% | Easy to spell, say, and remember |
| **Brandability** | 20% | Unique, ownable, not generic |
| **Extension** | 15% | .com > .io > .ai > .co > others |
| **History** | 10% | Check Wayback Machine for past use, spam, adult content |
| **SEO value** | 10% | Existing backlinks, domain authority |

### For SEO/Content Domains

| Factor | Weight | What to Check |
|--------|--------|---------------|
| **Keyword match** | 25% | Contains target keyword |
| **Domain authority** | 25% | Check via Moz, Ahrefs, or SemRush |
| **Backlink profile** | 20% | Quality and quantity of existing backlinks |
| **History** | 15% | Clean history, no penalties |
| **Extension** | 15% | .com preferred for organic search |

### Domain Valuation Factors

| Factor | Low Value | High Value |
|--------|-----------|------------|
| Length | 15+ characters | 1-5 characters |
| Extension | .xyz, .club | .com, .io, .ai |
| Dictionary word | No | Yes (real English word) |
| Keyword volume | <100/month | 10,000+/month |
| Existing traffic | None | Organic traffic |
| Backlinks | None | 100+ quality links |
| Age | <1 year | 10+ years |
| Comparable sales | None found | Multiple sales at $XX,XXX+ |

## Research Workflow

### Step 1: Check Availability

```bash
# Quick WHOIS check
curl -s "https://mcp.domaindetails.com/lookup/{domain}" | jq '.available // .registrar'
```

### Step 2: Check Marketplace Listings

```bash
curl -s "https://api.domaindetails.com/api/marketplace/search?domain={domain}" | jq
```

### Step 3: Check Domain History

Use WebFetch to check:
- `web.archive.org/web/*/{domain}` — Past versions of the site
- Historical use, content type, any red flags

### Step 4: Check SEO Metrics (if SemRush available)

```bash
# Domain overview
curl -s "https://api.semrush.com/?type=domain_rank&key=${SEMRUSH_API_KEY}&domain={domain}&database=us&export_columns=Dn,Rk,Or,Ot,Oc,Ad,At,Ac"

# Backlinks overview
curl -s "https://api.semrush.com/?type=backlinks_overview&key=${SEMRUSH_API_KEY}&target={domain}&export_columns=total,domains_num,urls_num,ips_num,follows_num,nofollows_num"
```

### Step 5: Generate Alternatives

If the desired domain is taken, suggest alternatives:

**Patterns:**
- `get{brand}.com` — getnotion.com
- `{brand}hq.com` — slackhq.com
- `try{brand}.com` — tryfigma.com
- `use{brand}.com` — usefathom.com
- `{brand}app.com` — todoistapp.com
- `{brand}.io` — linear.io
- `{brand}.ai` — jasper.ai
- `{brand}.co` — buffer.co
- `hey{brand}.com` — heysummit.com

## Output Format

```markdown
# Domain Research: {domain}

## WHOIS Data

| Field | Value |
|-------|-------|
| Registrar | {registrar} |
| Created | {date} |
| Expires | {date} |
| Status | {status} |
| Nameservers | {ns} |
| Privacy | {Yes/No} |

## Marketplace Listings

| Marketplace | Listed? | Price | Link |
|-------------|---------|-------|------|
| Sedo | {Yes/No} | {price} | {link} |
| Afternic | {Yes/No} | {price} | {link} |
| ... | ... | ... | ... |

## Domain Evaluation

| Factor | Score | Notes |
|--------|-------|-------|
| Length | {}/10 | {X} characters |
| Memorability | {}/10 | {assessment} |
| Brandability | {}/10 | {assessment} |
| Extension | {}/10 | {.com/.io/etc} |
| History | {}/10 | {clean/flags} |
| **Overall** | **{}/10** | |

## SEO Metrics (if available)
{Domain authority, backlinks, organic traffic}

## Alternatives (if domain is taken)
| Domain | Available? | Notes |
|--------|-----------|-------|

## Recommendation
{Buy/Pass/Negotiate — with reasoning}
```

## Important Notes

- WHOIS data is increasingly privacy-protected. Limited registrant info is normal.
- Domain marketplace prices are often negotiable. Listed price is usually the starting point.
- Always check domain history on the Wayback Machine before purchasing. Spam/adult history can carry Google penalties.
- Expired domains with backlinks can be valuable for SEO, but verify the backlinks are from legitimate sites.
- .com is still king for brand trust, but .io (tech), .ai (AI), and .co (startups) are increasingly accepted.
