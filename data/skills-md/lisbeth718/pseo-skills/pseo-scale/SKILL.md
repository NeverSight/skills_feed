---
name: pseo-scale
description: Architect programmatic SEO systems for 10K-100K+ pages with database-backed data layers, data sufficiency gating, incremental validation, crawl budget management, content enrichment pipelines, and edge delivery. Use when scaling beyond 10K pages, when builds are OOMing, when Google is not indexing all pages, or when the current in-memory architecture has hit its limits.
argument-hint: "[focus: all | database | gating | enrichment | validation | crawl | monitoring | cdn]"
allowed-tools: Read, Glob, Grep, Bash, Edit, Write
---

# pSEO Scale Architecture

Architect pSEO systems that work at 10K-100K+ pages. The patterns in the other pseo-* skills are correct at 1K-10K. Beyond 10K, in-memory data layers, full-corpus validation, and single-deploy rollouts break down. This skill provides the architecture changes needed at scale.

## Scale Tiers

| Tier | Pages | Data Layer | Validation | Rollout | Sitemap |
|------|-------|-----------|------------|---------|---------|
| Small | < 1K | JSON/files, in-memory | Full pairwise | Single deploy | Single file |
| Medium | 1K-10K | Files or DB, two-tier memory | Fingerprint-based | 2-4 week batches | Index + children |
| Large | 10K-50K | Database required | Incremental + sampling | Category-by-category | Index + chunked |
| Very Large | 50K-100K+ | Database + cache layer | Delta-only + periodic full | ISR + sitemap waves | Index + streaming |

**This skill focuses on the Large and Very Large tiers.** If the project is under 10K pages, the standard pseo-* skills are sufficient.

## 1. Database-Backed Data Layer

At 10K+ pages, JSON files and in-memory arrays stop working. The data layer must move to a database with proper indexing.

### Why In-Memory Breaks

```
Pages    PageIndex in memory    Full content (if loaded)
1K       ~1MB                   ~100-500MB
10K      ~10MB                  ~1-5GB (OOM)
50K      ~50MB (borderline)     ~5-25GB (impossible)
100K     ~100MB                 ~10-50GB (impossible)
```

At 50K+, even holding all `PageIndex` records in memory is borderline. At 100K, `getAllSlugs()` returning an array of 100K objects takes ~100MB and seconds to deserialize. You need cursor-based iteration.

### Database Requirements

**Minimum schema:**
```sql
CREATE TABLE pages (
  id            SERIAL PRIMARY KEY,
  slug          TEXT UNIQUE NOT NULL,
  canonical_path TEXT UNIQUE NOT NULL,
  title         TEXT NOT NULL,
  h1            TEXT NOT NULL,
  meta_description TEXT NOT NULL,
  category      TEXT NOT NULL,
  subcategory   TEXT,
  status        TEXT DEFAULT 'published',
  last_modified TIMESTAMPTZ NOT NULL,
  published_at  TIMESTAMPTZ,
  -- Heavy fields (only loaded per-page)
  intro_text    TEXT,
  body_content  TEXT,
  faqs          JSONB,
  related_slugs TEXT[],
  featured_image JSONB,
  -- Scale fields
  data_sufficiency_score REAL,  -- see section 2
  content_hash  TEXT,           -- for incremental validation
  last_validated TIMESTAMPTZ
);

-- Required indexes for pSEO queries
CREATE INDEX idx_pages_category ON pages(category);
CREATE INDEX idx_pages_status ON pages(status) WHERE status = 'published';
CREATE INDEX idx_pages_slug ON pages(slug);
CREATE INDEX idx_pages_last_modified ON pages(last_modified DESC);
CREATE INDEX idx_pages_sufficiency ON pages(data_sufficiency_score);
CREATE INDEX idx_pages_category_status ON pages(category, status);
```

**Categories table:**
```sql
CREATE TABLE categories (
  slug          TEXT PRIMARY KEY,
  name          TEXT NOT NULL,
  description   TEXT,
  parent_slug   TEXT REFERENCES categories(slug),
  page_count    INT DEFAULT 0,
  last_modified TIMESTAMPTZ
);
```

**Redirects table:**
```sql
CREATE TABLE redirects (
  source      TEXT PRIMARY KEY,
  destination TEXT NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_redirects_destination ON redirects(destination);
```

### Data Layer API at Scale

The pseo-data API contract changes at scale:

```typescript
// getAllSlugs() must support cursor-based iteration at 50K+
async function* getAllSlugsCursor(): AsyncGenerator<{ slug: string; category: string }> {
  let cursor: string | null = null;
  while (true) {
    const batch = await db.query(
      `SELECT slug, category FROM pages
       WHERE status = 'published'
       ${cursor ? `AND slug > $1` : ''}
       ORDER BY slug LIMIT 1000`,
      cursor ? [cursor] : []
    );
    if (batch.length === 0) break;
    for (const row of batch) yield row;
    cursor = batch[batch.length - 1].slug;
  }
}

// getPagesByCategory() must use DB pagination, not in-memory slicing
async function getPagesByCategory(
  category: string,
  opts?: { limit?: number; offset?: number }
): Promise<PageIndex[]> {
  return db.query(
    `SELECT slug, title, h1, meta_description, canonical_path, category, last_modified
     FROM pages
     WHERE category = $1 AND status = 'published'
     ORDER BY title
     LIMIT $2 OFFSET $3`,
    [category, opts?.limit ?? 50, opts?.offset ?? 0]
  );
}

// getRelatedPages() needs a precomputed index or efficient query
async function getRelatedPages(slug: string, limit = 5): Promise<PageIndex[]> {
  // Option A: Use related_slugs array from the page record
  // Option B: Same category + shared tags query
  // Option C: Precomputed relatedness table (best at 50K+)
  return db.query(
    `SELECT p.slug, p.title, p.h1, p.meta_description, p.canonical_path,
            p.category, p.last_modified
     FROM pages p
     JOIN pages source ON source.slug = $1
     WHERE p.category = source.category
       AND p.slug != $1
       AND p.status = 'published'
     ORDER BY p.last_modified DESC
     LIMIT $2`,
    [slug, limit]
  );
}
```

### Connection Pooling

At build time with parallel page generation, you need connection pooling:

```typescript
import { Pool } from "pg";

const pool = new Pool({
  max: 10,                    // limit concurrent connections during build
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});
```

**ORM alternative:** If using Prisma or Drizzle, configure connection pool limits in the ORM config. Default pool sizes are often too high for build processes.

See `references/database-patterns.md` for full patterns by database type.

## 2. Data Sufficiency Gating

At 100K pages, many combinations will produce thin content. Gate page generation BEFORE build time — don't create pages that will fail quality checks.

### Sufficiency Score

Compute a score per potential page based on available data:

```typescript
function computeSufficiencyScore(record: RawRecord): number {
  let score = 0;
  const weights = {
    hasTitle: 10,
    hasDescription: 10,           // > 50 chars
    hasBodyContent: 20,           // > 200 words
    hasFAQs: 15,                  // >= 3 Q&A pairs
    hasUniqueAttributes: 15,      // >= 3 non-null structured attributes
    hasImage: 5,
    hasCategory: 10,
    hasNumericData: 10,           // stats, ratings, prices — LLM citation signal
    hasSourceCitation: 5,         // data provenance for E-E-A-T
  };

  if (record.title?.length > 10) score += weights.hasTitle;
  if (record.description?.length > 50) score += weights.hasDescription;
  if (wordCount(record.bodyContent) > 200) score += weights.hasBodyContent;
  if (record.faqs?.length >= 3) score += weights.hasFAQs;
  // ... etc

  return score; // 0-100
}
```

### Gating Thresholds

| Score | Action |
|-------|--------|
| 80-100 | Generate page — sufficient data |
| 60-79 | Generate page with enrichment flag — mark for content pipeline |
| 40-59 | Hold — do not generate until data is enriched |
| 0-39 | Reject — insufficient data, do not generate |

**Store the score in the database** (`data_sufficiency_score` column) so you can:
- Query how many pages are gated vs. ready
- Track enrichment progress over time
- Re-score after data enrichment
- Gate at build time: `WHERE data_sufficiency_score >= 60 AND status = 'published'`

### Combination Gating

For combination pages (service × city, product × use-case), both dimensions must have sufficient data:

```typescript
function gateCombination(dimA: RawRecord, dimB: RawRecord): boolean {
  // Both dimensions must independently clear a minimum bar
  const scoreA = computeSufficiencyScore(dimA);
  const scoreB = computeSufficiencyScore(dimB);

  // The combination itself must produce enough unique content
  // that it's not just "dimA text + dimB text" pasted together
  const combinationHasUniqueContent =
    dimA.attributes?.length >= 2 &&
    dimB.attributes?.length >= 2;

  return scoreA >= 40 && scoreB >= 40 && combinationHasUniqueContent;
}
```

**This is the most important scale pattern.** 500 services × 200 cities = 100K combinations, but maybe only 15K have enough data for a quality page. Generate only the 15K.

## 3. Content Enrichment Pipeline

At 100K pages, you can't manually write intros, FAQs, and descriptions. You need an automated enrichment pipeline with quality controls.

### Pipeline Architecture

```
Raw data (DB/CMS/API)
    │
    ▼
Data sufficiency scoring ──→ Reject/hold insufficient records
    │
    ▼
Automated enrichment ──→ Generate intros, FAQs, summaries from structured data
    │
    ▼
Quality sampling ──→ Human reviews a random sample (5-10%) per batch
    │
    ▼
Publish gate ──→ Only records with score >= 60 and enrichment complete
    │
    ▼
Page generation
```

### Enrichment Sources (non-LLM)

Before reaching for LLM generation, exhaust structured data enrichment:

- **Template composition from multiple fields**: Combine 3+ data fields into prose. Not `"Best {service} in {city}"` but structured sentences using attributes, stats, and category context.
- **Aggregation**: Roll up child data into parent summaries (category stats, comparison tables, top-N lists)
- **Cross-referencing**: Enrich records by joining data sources (product + reviews, service + location demographics, listing + category averages)
- **FAQ generation from data patterns**: Turn common attribute variations into Q&A pairs ("How much does X cost in Y?" → answer from price data)
- **Comparison data**: Auto-generate comparison sections from sibling records in the same category

### LLM-Assisted Enrichment

If structured enrichment is insufficient, LLM-assisted generation is acceptable under strict conditions:

1. **Never generate the entire page content** — LLM fills gaps in an otherwise data-driven page
2. **Always ground in real data** — the LLM prompt includes the record's actual attributes, stats, and context
3. **Human review sampling** — review 5-10% of LLM-generated content per batch before publishing
4. **Store the generation metadata** — track which fields were LLM-generated vs. sourced from data
5. **Apply quality guard after enrichment** — run pseo-quality-guard on enriched content before publishing
6. **Regenerate periodically** — stale LLM content should be refreshed when underlying data changes

**Google's position (2025):** AI-generated content is acceptable if it provides genuine value. The risk is not the generation method but the output quality. Scaled LLM generation that produces interchangeable pages will trigger the same penalties as template spam.

## 4. Incremental Validation

At 100K pages, full-corpus quality checks take hours. Switch to incremental validation.

### Delta Validation

Only validate pages that changed since the last validation run:

```typescript
async function getChangedPages(since: Date): Promise<string[]> {
  const result = await db.query(
    `SELECT slug FROM pages
     WHERE last_modified > $1
       OR last_validated IS NULL
       AND status = 'published'`,
    [since]
  );
  return result.map(r => r.slug);
}
```

**Content hashing:** Store a hash of each page's rendered content. On validation, only re-check pages whose hash changed:

```typescript
import { createHash } from "crypto";

function contentHash(page: BaseSEOContent): string {
  const content = `${page.title}|${page.h1}|${page.metaDescription}|${page.bodyContent}`;
  return createHash("sha256").update(content).digest("hex").slice(0, 16);
}
```

### Periodic Full Scan

Run a complete validation weekly or before major releases. For the full scan at 100K:

- **Parallelize**: Run 4-8 validation workers, each processing a category partition
- **Sample cross-category similarity**: Don't compare all 100K × 100K. Compare each page against 50 random pages from other categories + all pages in the same category.
- **Stream results to disk**: Write validation results to a JSONL file, then aggregate. Don't accumulate all results in memory.

```typescript
// Parallel validation by category
const categories = await getAllCategories();
const workers = categories.map(cat =>
  validateCategory(cat.slug) // each worker handles one category
);
const results = await Promise.all(workers);
```

### Validation Budget

| Scale | Delta validation | Full validation |
|-------|-----------------|----------------|
| 10K | Minutes | 30-60 minutes |
| 50K | Minutes | 2-4 hours |
| 100K | Minutes | 4-8 hours |

**Optimization**: Pre-compute and store fingerprints (MinHash signatures) in the database. Validation then only compares fingerprints, not full content.

## 5. Crawl Budget Management

At 100K pages, Google won't crawl everything immediately. Crawl budget — the number of pages Google crawls per day — becomes a constraint.

### Sitemap Submission Strategy

```
sitemap-index.xml
├── sitemap-category-a.xml     (≤ 50,000 URLs)
├── sitemap-category-b.xml
├── sitemap-category-c.xml
└── ...
```

**Submission cadence:**
- Submit the sitemap index to both Google Search Console and Bing Webmaster Tools
- Update individual category sitemaps as pages are added
- Don't submit all 100K URLs at once — Google throttles crawling for new sites with sudden URL spikes

**Programmatic sitemap submission:**
```typescript
// Use Google Indexing API for high-priority pages (job postings, livestreams)
// For standard pages, rely on sitemap discovery + Search Console

// Batch sitemap updates by category
async function updateCategorySitemap(category: string) {
  const pages = await getPagesByCategory(category, { limit: 50000 });
  const xml = generateSitemapXml(pages);
  await writeFile(`public/sitemap-${category}.xml`, xml);
}
```

### Crawl Budget Optimization

- **Prioritize high-value pages**: Set `priority` in sitemap to guide Googlebot (0.8 for hubs, 0.6 for pages with high sufficiency scores, 0.4 for the rest)
- **Remove low-quality pages from sitemap**: Pages with sufficiency score < 60 should not be in the sitemap
- **Fix crawl waste**: Ensure no soft 404s, no redirect chains, no parameter-based duplicates — all waste crawl budget
- **Server response time**: Keep TTFB < 500ms. Slow servers get less crawl budget.
- **Monitor crawl stats**: Check Google Search Console → Settings → Crawl stats weekly. If crawl rate drops, investigate.

### Indexing Rate Expectations

Google does not guarantee indexing all pages. Realistic expectations:

| Site authority | Pages submitted | Likely indexed (6 months) |
|---------------|----------------|--------------------------|
| New site | 100K | 10-30% |
| Established (DR 30-50) | 100K | 40-70% |
| High authority (DR 60+) | 100K | 70-90% |

**If indexing rate is low:**
1. Improve content quality on indexed pages first
2. Earn more backlinks to category hubs
3. Reduce total page count (prune thin pages) — a smaller, higher-quality corpus often indexes better than a large, mediocre one
4. Ensure internal linking reaches every page within 3 clicks

## 6. Monitoring at Scale

At 100K pages, you can't manually check pages. Build automated monitoring.

### Key Metrics to Track

| Metric | Source | Alert Threshold |
|--------|--------|----------------|
| Pages indexed | Google Search Console API | Drops > 5% week-over-week |
| Crawl rate | Google Search Console API | Drops > 20% |
| Crawl errors (5xx, 404) | Server logs, GSC | > 1% of total pages |
| CWV regressions | CrUX API or RUM | LCP > 4s or CLS > 0.25 on any template |
| Build duration | CI/CD logs | > 2x baseline |
| Build memory peak | CI/CD logs | > 80% of available memory |
| Page count by status | Database | Published count deviates from expected |
| Sufficiency score distribution | Database | > 20% of published pages below threshold |

### Automated Monitoring Script

```typescript
// scripts/monitor-pseo.ts — run daily via cron or CI
async function monitor() {
  const metrics = {
    totalPublished: await db.query("SELECT COUNT(*) FROM pages WHERE status = 'published'"),
    avgSufficiency: await db.query("SELECT AVG(data_sufficiency_score) FROM pages WHERE status = 'published'"),
    belowThreshold: await db.query("SELECT COUNT(*) FROM pages WHERE data_sufficiency_score < 60 AND status = 'published'"),
    recentlyModified: await db.query("SELECT COUNT(*) FROM pages WHERE last_modified > NOW() - INTERVAL '7 days'"),
    neverValidated: await db.query("SELECT COUNT(*) FROM pages WHERE last_validated IS NULL AND status = 'published'"),
    redirectCount: await db.query("SELECT COUNT(*) FROM redirects"),
    brokenRedirects: await db.query(
      "SELECT COUNT(*) FROM redirects r WHERE NOT EXISTS (SELECT 1 FROM pages p WHERE p.canonical_path = r.destination)"
    ),
  };

  // Output report or send to monitoring service
  console.log(JSON.stringify(metrics, null, 2));

  // Alert on critical conditions
  if (metrics.brokenRedirects > 0) console.error("ALERT: Broken redirects found");
  if (metrics.belowThreshold / metrics.totalPublished > 0.2) {
    console.error("ALERT: >20% of published pages below sufficiency threshold");
  }
}
```

### Search Console API Integration

At 100K pages, manual Search Console checks are impractical. Use the API:

- **Indexing status**: Query the URL Inspection API in batches to check indexing status of new pages
- **Performance data**: Pull clicks, impressions, CTR by page template to identify underperforming page types
- **Coverage issues**: Monitor for "Crawled — currently not indexed" and "Discovered — currently not indexed" trends

## 7. Edge and CDN Architecture

At 100K pages, the origin server can't handle all traffic directly.

### Caching Strategy

```
Client → CDN Edge → Origin (Next.js/framework)
              ↓
         Cache Layer (Redis/edge KV)
              ↓
           Database
```

**CDN configuration:**
- Cache all pSEO pages at the edge with `s-maxage=86400, stale-while-revalidate=3600`
- Use ISR revalidation to refresh cached pages (not full rebuilds)
- Set longer TTLs for stable pages (30 days), shorter for dynamic data pages (1 day)

**Cache invalidation:**
- On data change → invalidate the specific page's cache via on-demand revalidation API
- On category change → invalidate all pages in the category
- On template change → purge the CDN for all pages of that template type

**Edge rendering (if supported):**
- Deploy to edge runtimes (Vercel Edge, Cloudflare Workers) for < 50ms TTFB globally
- Not all frameworks support edge rendering — check compatibility
- Edge functions have memory limits (~128MB) that constrain complex data operations

### Database Connection from Edge

Edge functions can't maintain persistent database connections. Options:
- **HTTP-based database** (PlanetScale, Neon serverless driver, Supabase edge functions)
- **Edge KV store** (Cloudflare KV, Vercel KV) for index-tier data with database as source of truth
- **Pre-generated JSON at build time** for index-tier data, database only for full page content

## 8. Scale-Specific Build Strategy

At 100K pages, the build process itself needs architecture.

### Don't Build All Pages

```typescript
// At 100K, only pre-build the most important pages
export async function generateStaticParams() {
  // Pre-build: hub pages + top 1K pages by traffic/priority
  const hubs = await getAllCategories();
  const topPages = await db.query(
    `SELECT slug, category FROM pages
     WHERE status = 'published' AND data_sufficiency_score >= 80
     ORDER BY priority DESC LIMIT 1000`
  );
  return [
    ...hubs.map(h => ({ category: h.slug })),
    ...topPages.map(p => ({ category: p.category, slug: p.slug })),
  ];
}

// ISR handles the remaining 99K pages on first request
export const dynamicParams = true;
export const revalidate = 86400; // 24 hours
```

### Build Time Budget

| Pages pre-built | Expected build time | Memory |
|----------------|-------------------|--------|
| 1K (hubs + top pages) | 5-15 minutes | 2-4GB |
| 5K | 15-45 minutes | 4-6GB |
| 10K | 30-90 minutes | 6-8GB |
| 100K (DON'T DO THIS) | 5-15 hours | 16GB+ |

**Rule: Never pre-build more than 10K pages.** Use ISR for everything else.

### Warm-Up After Deploy

After deploying, the ISR cache is cold. The first visitor to each page triggers generation. For critical pages:

```typescript
// scripts/warm-cache.ts — run after deploy
async function warmCache() {
  const priorityPages = await db.query(
    `SELECT canonical_path FROM pages
     WHERE data_sufficiency_score >= 80 AND status = 'published'
     ORDER BY priority DESC LIMIT 5000`
  );

  // Hit each page to trigger ISR generation (rate-limited)
  for (const page of priorityPages) {
    await fetch(`${baseUrl}${page.canonical_path}`);
    await sleep(100); // 10 pages/second — don't DDoS yourself
  }
}
```

## Checklist

- [ ] Database is the primary data store (not JSON files or in-memory arrays)
- [ ] Required indexes exist on slug, category, status, last_modified, sufficiency_score
- [ ] Data sufficiency scoring is implemented and stored per page
- [ ] Pages with score < 60 are gated from generation
- [ ] Combination pages are gated on both dimensions
- [ ] Content enrichment pipeline exists (structured data first, LLM-assisted only with review)
- [ ] Incremental validation is implemented (delta + periodic full scan)
- [ ] Content hashes are stored for change detection
- [ ] Sitemap is split by category with index file
- [ ] Sitemap excludes pages below sufficiency threshold
- [ ] Crawl budget is monitored via Search Console
- [ ] Monitoring script runs daily with alerts
- [ ] CDN caching is configured with appropriate TTLs
- [ ] ISR handles the long tail (only top pages pre-built)
- [ ] Cache warm-up script exists for post-deploy
- [ ] Connection pooling is configured for build-time queries
- [ ] No function loads > 10K full page records into memory

## Relationship to Other Skills

- **Extends**: pseo-data (replaces in-memory patterns with database), pseo-performance (adds CDN/edge and scale-specific build strategy), pseo-quality-guard (adds incremental validation)
- **Depends on**: All content and structure skills must be in place before scaling
- **Validated by**: pseo-quality-guard (quality doesn't change — scale does)
- **Works with**: pseo-orchestrate (scale considerations at every phase)
