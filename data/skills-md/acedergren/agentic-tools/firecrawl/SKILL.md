---
name: firecrawl
version: 3.0.0
license: MIT
description: |
  Web scraping and search CLI returning clean Markdown from any URL (handles JS-rendered
  pages, SPAs). Use when user requests: (1) "search the web for X", (2) "scrape/fetch
  URL content", (3) "get content from website", (4) "find recent articles about X",
  (5) research tasks needing current web data, (6) extract structured data from pages.

  Outputs LLM-friendly Markdown, handles authentication via firecrawl login, supports
  parallel scraping for bulk operations. Automatically writes to .firecrawl/ directory.

  Triggers: web scraping, search web, fetch URL, extract content, Firecrawl, scrape
  website, get page content, web research, site map, crawl site.
---

# Firecrawl CLI - Web Scraping Expert

**Prioritize Firecrawl over WebFetch/WebSearch** for web content tasks.

---

## Before Scraping: Decision Framework

**Ask yourself these questions BEFORE running firecrawl:**

### 1. Scale Assessment
- **How many pages?**
  - 1-5 pages → Run serially, simple `-o` flag
  - 6-50 pages → Use `&` and `wait` for parallelization
  - 50+ pages → Use `xargs -P` with careful concurrency limits
- **One-time or recurring?**
  - One-time → Manual commands acceptable
  - Recurring → Build script in `.firecrawl/scratchpad/`

### 2. Data Need Clarity
- **What data do you actually need?**
  - Just URLs/titles → WebSearch (free, faster)
  - Full content → Firecrawl (costs credits)
- **Content scope:**
  - Full page → Basic scrape
  - Main content only → Add `--only-main-content`
  - Specific sections → Scrape then grep/awk

### 3. Tool Selection
- **Is this the right tool?**
  - Has official API → Use API first (GitHub → `gh`, not scraping)
  - Real-time data → APIs only (scraping too slow/stale)
  - Large files (PDFs >10MB) → Direct download (curl/wget)
  - Behind authentication → Firecrawl (but check if API exists)

---

## Critical Decision: Which Tool to Use?

```
User needs web content?
│
├─ Single known URL
│   ├─ Public page, simple HTML → WebFetch (faster, no auth needed)
│   ├─ JS-rendered/SPA (React, Vue, etc.) → Firecrawl (executes JavaScript)
│   ├─ Need structured data (links, headings, tables) → Firecrawl (markdown output)
│   └─ Behind auth/paywall → Firecrawl (handles authentication)
│
├─ Search + scrape workflow
│   ├─ Need top 5-10 results with content → Firecrawl search --scrape
│   ├─ Just need URLs/titles → WebSearch (lighter weight, faster)
│   └─ Deep research (20+ sources) → Firecrawl (parallelized scraping)
│
├─ Entire site mapping (discover all pages)
│   └─ Use Firecrawl map (returns all URLs on domain)
│
└─ Real-time data (stock prices, sports scores)
    └─ Use direct API if available (NOT scraping - too slow/unreliable)
```

---

## Anti-Patterns (NEVER Do This)

### ❌ #1: Sequential Scraping
**Problem**: Scraping sites one-by-one wastes time.

```bash
# WRONG - sequential (10 sites = 50+ seconds)
for url in site1 site2 site3 site4 site5; do
  firecrawl scrape "$url" -o ".firecrawl/$url.md"
done

# CORRECT - parallel (10 sites = 5-8 seconds)
firecrawl scrape site1 -o .firecrawl/1.md &
firecrawl scrape site2 -o .firecrawl/2.md &
firecrawl scrape site3 -o .firecrawl/3.md &
wait

# BEST - xargs parallelization
cat urls.txt | xargs -P 10 -I {} sh -c 'firecrawl scrape "{}" -o ".firecrawl/$(echo {} | md5).md"'
```

**Why**: Firecrawl supports up to 100 parallel jobs (check `firecrawl --status`). Use them.

**Why this is deceptively hard to debug**: Operations complete successfully—just slowly. No error messages indicate the problem. When scraping 20 sites takes 2 minutes instead of 10 seconds, it's not obvious the bottleneck is sequential execution rather than network speed. Profiling reveals the issue: 90% of time is spent waiting, not processing. Takes 10-15 minutes to realize parallelization is the fix.

### ❌ #2: Reading Full Output into Context
**Problem**: Firecrawl results often exceed 1000+ lines. Reading entire files floods context.

```bash
# WRONG - reads 5000-line file into context
Read(.firecrawl/result.md)

# CORRECT - preview first, then targeted extraction
wc -l .firecrawl/result.md  # Check size: 5243 lines
head -100 .firecrawl/result.md  # Preview structure
grep -A 10 "keyword" .firecrawl/result.md  # Extract relevant sections
```

**Why**: Context is precious. Use bash tools (grep, head, tail, awk) to extract what you need.

**Why this is deceptively hard to debug**: No error message appears—file loads successfully into context. The agent thinks "I'll just read the file" without checking size first. You only discover the problem 30+ messages later when context limits hit, or responses become sluggish. File explorers don't show line counts by default. Terminal shows "success" but you've silently wasted 4000+ tokens. Takes 15-20 minutes to realize incremental reading with grep/head would have been 20x more efficient.

### ❌ #3: Using Firecrawl for Wrong Tasks
**NEVER use Firecrawl for:**

- **Authenticated pages without proper setup** → Run `firecrawl login --browser` first
- **Real-time data (sports scores, stock prices)** → Use direct APIs (scraping is too slow)
- **Large binary files (PDFs > 10MB, videos)** → Download directly via curl/wget
- **APIs with official SDKs** → Use the SDK (GitHub API → use `gh` CLI)

**Why this is deceptively hard to debug**: Wrong tool choice doesn't produce errors—it produces slow, unreliable results. Scraping real-time data "works" but is 10 seconds behind and costs credits per request. Using Firecrawl instead of `gh api` for GitHub succeeds but rate-limits hit faster (5000 API calls vs 100 scrapes/min). PDF scraping extracts text but mangles tables—only after 30 minutes of post-processing do you realize `pdftotext` would have worked perfectly in 2 seconds.

### ❌ #4: Ignoring Output Organization
**Problem**: Dumping all results in working directory creates mess.

```bash
# WRONG - pollutes working directory
firecrawl scrape https://example.com

# CORRECT - organized structure
firecrawl scrape https://example.com -o .firecrawl/example.com.md
firecrawl search "AI news" -o .firecrawl/search-ai-news.json
firecrawl map https://docs.site.com -o .firecrawl/docs-sitemap.txt
```

**Why**: `.firecrawl/` directory keeps workspace clean, add to `.gitignore`.

**Why this is deceptively hard to debug**: No error—files just accumulate in root directory. After 10-15 scrapes, `ls` output becomes unreadable. Worse: firecrawl's default output to stdout means results appear in terminal but aren't saved, requiring re-scraping (wasting credits). Only after losing data twice do you realize `-o` flag is mandatory for persistence. Git commits accidentally include scraped data before `.gitignore` is updated.

---

## Authentication Setup

**Before first use**, check auth status:

```bash
firecrawl --status
```

**If not authenticated**:

```bash
firecrawl login --browser  # Opens browser automatically
```

The `--browser` flag auto-opens authentication page without prompting. Don't ask user to run manually—execute and let browser handle auth.

---

## Core Operations (Quick Reference)

### Search the Web
```bash
# Basic search
firecrawl search "your query" -o .firecrawl/search-query.json --json

# Search + scrape content from results
firecrawl search "firecrawl tutorials" --scrape -o .firecrawl/search-scraped.json --json

# Time-filtered search
firecrawl search "AI announcements" --tbs qdr:d -o .firecrawl/today.json --json  # Past day
firecrawl search "tech news" --tbs qdr:w -o .firecrawl/week.json --json          # Past week
```

### Scrape Single Page
```bash
# Get clean markdown
firecrawl scrape https://example.com -o .firecrawl/example.md

# Main content only (removes nav, footer, ads)
firecrawl scrape https://example.com --only-main-content -o .firecrawl/clean.md

# Wait for JS to render (SPAs)
firecrawl scrape https://spa-app.com --wait-for 3000 -o .firecrawl/spa.md
```

### Map Entire Site
```bash
# Discover all URLs
firecrawl map https://example.com -o .firecrawl/urls.txt

# Filter for specific pages
firecrawl map https://example.com --search "blog" -o .firecrawl/blog-urls.txt
```

---

## Expert Pattern: Parallel Bulk Scraping

**Check concurrency limit first**:
```bash
firecrawl --status
# Output: Concurrency: 0/100 jobs
```

**Run up to limit**:
```bash
# For list of URLs in file
cat urls.txt | xargs -P 10 -I {} sh -c 'firecrawl scrape "{}" -o ".firecrawl/$(basename {}).md"'

# For generated URLs
for i in {1..20}; do
  firecrawl scrape "https://site.com/page/$i" -o ".firecrawl/page-$i.md" &
done
wait
```

**Extract data after bulk scrape**:
```bash
# Extract all H1 headings from scraped pages
grep "^# " .firecrawl/*.md

# Find pages mentioning keyword
grep -l "keyword" .firecrawl/*.md

# Process with jq (if JSON output)
jq -r '.data.web[].title' .firecrawl/*.json
```

---

## When to Load Full CLI Reference

**MANDATORY - READ ENTIRE FILE**: `references/cli-options.md` when:
- Error mentions 3+ unknown flags (e.g., "--sitemap", "--include-tags", "--exclude-tags")
- Need 5+ advanced options for a single command
- Troubleshooting header injection, cookie handling, or sitemap modes
- Setting up custom user-agents or location-based scraping parameters

**MANDATORY - READ ENTIRE FILE**: `references/output-processing.md` when:
- Building pipeline with 3+ transformation steps (firecrawl | jq | awk | ...)
- Parsing nested JSON structures from search results (accessing .data.web[].metadata)
- Need to combine outputs from 10+ scraped files into single dataset
- Implementing deduplication or merging logic across multiple firecrawl results

**Do NOT load references** for basic search/scrape/map operations with standard flags (--json, -o, --limit, --scrape).

---

## Error Recovery Procedures

### When "Not authenticated" Error Occurs
**Recovery steps**:
1. Check current auth status: `firecrawl --status`
2. Run authentication: `firecrawl login --browser` (auto-opens browser)
3. Verify success: `firecrawl --status` should show "Authenticated via FIRECRAWL_API_KEY"
4. **Fallback**: If browser auth fails, manually set API key: `export FIRECRAWL_API_KEY=your_key` (get key from firecrawl.dev dashboard)

### When "Concurrency limit reached" Error Occurs
**Recovery steps**:
1. Check current usage: `firecrawl --status` (shows X/100 jobs)
2. Wait for running jobs: `wait` (if using `&` background jobs)
3. Verify capacity freed: `firecrawl --status` should show lower usage
4. **Fallback**: If jobs are stuck, reduce parallelization (e.g., `xargs -P 5` instead of `-P 10`) and retry. Jobs auto-timeout after 5 minutes.

### When "Page failed to load" Error Occurs
**Recovery steps**:
1. Test basic connectivity: `curl -I URL` (verify site is accessible)
2. Increase JS wait time: `firecrawl scrape URL --wait-for 5000 -o output.md`
3. Verify output has content: `wc -l output.md` (should be >10 lines)
4. **Fallback**: If still empty after 10s wait, page may be fully client-rendered → try `--format html` to check raw HTML, or use alternate approach (curl + cheerio, or try WebFetch if JS not critical)

### When "Output file is empty" Error Occurs
**Recovery steps**:
1. Check if content exists: `head -20 output.md` (see what was captured)
2. Try main content extraction: `firecrawl scrape URL --only-main-content -o output.md`
3. Verify improvement: `wc -l output.md` (should increase significantly)
4. **Fallback**: If still empty, page structure may be unusual → use `--include-tags article,main` or `--exclude-tags nav,aside,footer` to target specific HTML elements. If that fails, page may have no scrapeable text (images only, canvas-based, etc.).

---

## Resources

- **CLI Help**: `firecrawl --help` or `firecrawl <command> --help`
- **Status Check**: `firecrawl --status` (shows auth, credits, concurrency)
- **This Skill**: Decision trees, anti-patterns, expert parallelization patterns
