---
name: documentation-scraper
description: Use when needing to scrape documentation websites into markdown for AI context. Triggers on "scrape docs", "download documentation", "get docs for [library]", or creating local copies of online documentation. CRITICAL - always analyze sitemap first before scraping.
---

# Documentation Scraper with slurp-ai

## Overview

slurp-ai scrapes documentation websites and compiles them into a single markdown file optimized for AI agent context. It is lightweight, fast, and deterministic - it does NOT use AI to scrape, it is FOR AI consumption.

## CRITICAL: Run Outside Sandbox

**All commands in this skill MUST be run outside the sandbox.** Use `dangerouslyDisableSandbox: true` for all Bash commands including:
- `which slurp` (installation check)
- `node analyze-sitemap.js` (sitemap analysis)
- `slurp` (scraping)
- File inspection commands (`wc`, `head`, `cat`, etc.)

The sandbox blocks network access and file operations required for web scraping.

## Pre-Flight: Check Installation

**Before scraping, verify slurp-ai is installed:**

```bash
which slurp || echo "NOT INSTALLED"
```

If not installed, ask the user to run:
```bash
npm install -g slurp-ai
```

**Requires:** Node.js v20+

**Do NOT proceed with scraping until slurp-ai is confirmed installed.**

## Commands

| Command | Purpose |
|---------|---------|
| `slurp <url>` | Fetch and compile in one step |
| `slurp fetch <url> [version]` | Download docs to partials only |
| `slurp compile` | Compile partials into single file |
| `slurp read <package> [version]` | Read local documentation |

**Output:** Creates `slurp_compiled/compiled_docs.md` from partials in `slurp_partials/`.

## CRITICAL: Analyze Sitemap First

**Before running slurp, ALWAYS analyze the sitemap.** This reveals the complete site structure and informs your `--base-path` and `--max` decisions.

### Step 1: Run Sitemap Analysis

Use the included `analyze-sitemap.js` script:

```bash
node analyze-sitemap.js https://docs.example.com
```

This outputs:
- Total page count (informs `--max`)
- URLs grouped by section (informs `--base-path`)
- Suggested slurp commands with appropriate flags
- Sample URLs to understand naming patterns

### Step 2: Interpret the Output

Example output:
```
📊 Total URLs in sitemap: 247

📁 URLs by top-level section:
   /docs                          182 pages
   /api                            45 pages
   /blog                           20 pages

🎯 Suggested --base-path options:
   https://docs.example.com/docs/guides/     (67 pages)
   https://docs.example.com/docs/reference/  (52 pages)
   https://docs.example.com/api/             (45 pages)

💡 Recommended slurp commands:

   # Just "/docs/guides" section (67 pages)
   slurp https://docs.example.com/docs/guides/ --base-path https://docs.example.com/docs/guides/ --max 80
```

### Step 3: Choose Scope Based on Analysis

| Sitemap Shows | Action |
|---------------|--------|
| < 50 pages total | Scrape entire site: `slurp <url> --max 60` |
| 50-200 pages | Scope to relevant section with `--base-path` |
| 200+ pages | Must scope down - pick specific subsection |
| No sitemap found | Start with `--max 30`, inspect partials, adjust |

### Step 4: Frame the Slurp Command

With sitemap data, you can now set accurate parameters:

```bash
# From sitemap: /docs/api has 45 pages
slurp https://docs.example.com/docs/api/intro \
  --base-path https://docs.example.com/docs/api/ \
  --max 55
```

**Key insight:** Starting URL is where crawling begins. Base path filters which links get followed. They can differ (useful when base path itself returns 404).

## Common Scraping Patterns

### Library Documentation (versioned)
```bash
# Express.js 4.x docs
slurp https://expressjs.com/en/4x/api.html --base-path https://expressjs.com/en/4x/

# React docs (latest)
slurp https://react.dev/learn --base-path https://react.dev/learn
```

### API Reference Only
```bash
slurp https://docs.example.com/api/introduction --base-path https://docs.example.com/api/
```

### Full Documentation Site
```bash
slurp https://docs.example.com/
```

## CLI Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--max <n>` | 20 | Maximum pages to scrape |
| `--concurrency <n>` | 5 | Parallel page requests |
| `--headless <bool>` | true | Use headless browser |
| `--base-path <url>` | start URL | Filter links to this prefix |
| `--output <dir>` | `./slurp_partials` | Output directory for partials |
| `--retry-count <n>` | 3 | Retries for failed requests |
| `--retry-delay <ms>` | 1000 | Delay between retries |
| `--yes` | - | Skip confirmation prompts |

### Compile Options

| Flag | Default | Purpose |
|------|---------|---------|
| `--input <dir>` | `./slurp_partials` | Input directory |
| `--output <file>` | `./slurp_compiled/compiled_docs.md` | Output file |
| `--preserve-metadata` | true | Keep metadata blocks |
| `--remove-navigation` | true | Strip nav elements |
| `--remove-duplicates` | true | Eliminate duplicates |
| `--exclude <json>` | - | JSON array of regex patterns to exclude |

### When to Disable Headless Mode

Use `--headless false` for:
- Static HTML documentation sites
- Faster scraping when JS rendering not needed

**Default is headless (true)** - works for most modern doc sites including SPAs.

## Output Structure

```
slurp_partials/              # Intermediate files
  └── page1.md
  └── page2.md
slurp_compiled/              # Final output
  └── compiled_docs.md       # Compiled result
```

## Quick Reference

```bash
# 1. ALWAYS analyze sitemap first
node analyze-sitemap.js https://docs.example.com

# 2. Scrape with informed parameters (from sitemap analysis)
slurp https://docs.example.com/docs/ --base-path https://docs.example.com/docs/ --max 80

# 3. Skip prompts for automation
slurp https://docs.example.com/ --yes

# 4. Check output
cat slurp_compiled/compiled_docs.md | head -100
```

## Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Wrong `--max` value | Guessing page count | Run `analyze-sitemap.js` first |
| Too few pages scraped | `--max` limit (default 20) | Set `--max` based on sitemap analysis |
| Missing content | JS not rendering | Ensure `--headless true` (default) |
| Crawl stuck/slow | Rate limiting | Reduce `--concurrency 3` |
| Duplicate sections | Similar content | Use `--remove-duplicates` (default) |
| Wrong pages included | Base path too broad | Use sitemap to find correct `--base-path` |
| Prompts blocking automation | Interactive mode | Add `--yes` flag |

## Post-Scrape Usage

The output markdown is designed for AI context injection:

```bash
# Check file size (context budget)
wc -c slurp_compiled/compiled_docs.md

# Preview structure
grep "^#" slurp_compiled/compiled_docs.md | head -30

# Use with Claude Code - reference in prompt or via @file
```

## When NOT to Use

- **API specs in OpenAPI/Swagger**: Use dedicated parsers instead
- **GitHub READMEs**: Fetch directly via raw.githubusercontent.com
- **npm package docs**: Often better to read source + README
- **Frequently updated docs**: Consider caching strategy
