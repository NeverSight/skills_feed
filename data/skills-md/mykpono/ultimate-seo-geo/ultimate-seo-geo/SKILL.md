---
name: ultimate-seo-geo
description: Audits and optimizes websites for search engine visibility (SEO) and AI search citation (GEO), covering technical health, E-E-A-T content scoring, domain authority, structured data, rich results, and entity signals. Use when running SEO audits, diagnosing traffic drops or ranking losses, generating Schema.org JSON-LD, checking Core Web Vitals, crawlability, robots.txt, sitemaps, hreflang, backlinks, planning content strategy or site migrations, fixing indexing issues, or optimizing for AI Overviews, ChatGPT, and Perplexity. NOT for paid ads (PPC/SEM), social media strategy, email marketing, or general web development unrelated to search.
version: 1.12.8
---

# Ultimate SEO + GEO — LLM-Agnostic SEO Agent

| Attribute | Details |
| --- | --- |
| **Version** | 1.12.8 |
| **Updated** | 2026-08-12 |
| **License** | MIT |
| **Author** | Myk Pono |
| **Lab** | [lab.mykpono.com](https://lab.mykpono.com) |
| **Homepage** | [lab.mykpono.com](https://lab.mykpono.com) |
| **LinkedIn** | [Profile](https://www.linkedin.com/in/mykolaponomarenko/) |
| **Platforms** | Claude Code, Cursor, Copilot, Gemini CLI, Codex, Windsurf, Cline, Aider, Devin |

The definitive SEO and Generative Engine Optimization agent. LLM-agnostic — works on any
platform that reads `AGENTS.md`. Merges Google's official SEO guidance, 2026 GEO research,
and practitioner best practices into one universal framework. Every finding comes with a
clear fix directive — not just diagnosis.

**This file is the routing shell.** Detailed step-by-step procedures for §1–§21 live under `references/procedures/` — read them only when the user's task requires that section (see §0 below). Domain knowledge tables live in `references/*.md` as before.

## 0. Before You Start

### Routing index (read only what you need)

| Goal | Procedure file(s) | Also read / run |
|------|-------------------|-----------------|
| Full scored audit | `references/procedures/02-full-site-audit.md`, `references/procedures/21-script-toolbox.md` | `references/audit-script-matrix.md`, `references/thinking-framework.md`, `generate_report.py` |
| AI citations / GEO | `references/procedures/03-geo-ai-search.md` | `references/ai-search-geo.md`, `entity_checker.py`, `llms_txt_checker.py`, `robots_checker.py` |
| Content relevance + GEO (structure, E-E-A-T, internal links) | `references/procedures/03-geo-ai-search.md`, `references/procedures/06-content-eeat-and-pruning.md` | `references/eeat-framework.md`, `article_seo.py`, `readability.py`, `internal_links.py`, `generate_report.py` |
| AI-drafted content review (artifacts, generated-text tells) | `references/procedures/06-content-eeat-and-pruning.md` | `references/ai-generated-content-artifacts.md`, `content_quality.py`, `readability.py` |
| Schema only | `references/procedures/05-schema-structured-data.md` | `references/schema-types.md`, `validate_schema.py` |
| Local | `references/procedures/12-local-seo.md` | `references/local-seo.md`, `local_signals_checker.py` |
| Crawl / index / performance | `references/procedures/04-technical-seo.md`, `references/procedures/11-crawl-indexation.md` | Matrix scripts (`robots_checker`, `sitemap_checker`, `pagespeed.py` if API works) |
| Migration | `references/procedures/20-site-migration.md` | `references/site-migration.md`, `redirect_checker.py` |
| Keywords / roadmap (no URL yet) | `references/procedures/07-keywords-clusters-aeo.md`, `references/procedures/16-strategy-roadmap.md` | **Do not** invent a live-site `/100` score |
| SEO drift / change tracking | `references/procedures/22-drift-monitoring.md` | `drift_monitor.py` |
| Semantic topic clustering | `references/procedures/23-semantic-clustering.md` | `topic_cluster.py` |
| Content brief generation | `references/procedures/07-keywords-clusters-aeo.md` | `content_brief.py` |
| E-commerce SEO | `references/procedures/24-ecommerce-seo.md` | `ecommerce_schema.py`, `validate_schema.py` |
| Advanced local / maps | `references/procedures/25-maps-intelligence.md` | `maps_checker.py`, `local_signals_checker.py` |
| Google API credentials | `references/procedures/21-script-toolbox.md` | `google_api_tier.py`, `crux_history.py`, `gsc_query.py`, `ga4_report.py` |

Section numbers **§1–§25** match `AGENTS.md` and the filenames in `references/procedures/`. Full index: [`references/procedures/README.md`](references/procedures/README.md).

### Reference Reading Guide

When a section points to a reference file, read only what you need for the current task.

**Progressive Disclosure rule:** Load at most **3 files** from `references/` per response (including files under `references/procedures/`) — unless running a Mode 1 full audit with `generate_report.py`, which implicitly covers all dimensions. For single-topic Mode 2 or Mode 3 tasks (e.g., "fix my schema", "write an llms.txt"), the routing tables identify 1–2 topical `references/*.md` files plus **at most one** `references/procedures/*.md` file when procedural detail is required. Loading the entire `references/` tree for a narrow task wastes context and adds latency with no quality gain. This pattern follows Anthropic's [Skills progressive disclosure architecture](https://github.com/anthropics/claude-cookbooks/tree/main/skills).

| Task | Read | Run |
|------|------|-----|
| Full audit (any type) | `references/audit-script-matrix.md` | `generate_report.py` |
| GEO / AI citations | `references/ai-search-geo.md`, `references/entity-optimization.md` | `robots_checker.py`, `entity_checker.py`, `llms_txt_checker.py` |
| Schema markup | `references/schema-types.md` | `validate_schema.py` |
| Technical / CWV | `references/technical-checklist.md` | `pagespeed.py`, `robots_checker.py`, `security_headers.py` |
| Content / E-E-A-T | `references/eeat-framework.md`, `references/core-eeat-framework.md` | `readability.py`, `article_seo.py` |
| AI-drafted content artifacts | `references/ai-generated-content-artifacts.md` | `content_quality.py`, `readability.py` |
| CITE domain audit | `references/cite-domain-rating.md` | `link_profile.py` |
| Keywords / clusters | `references/keyword-strategy.md` | — |
| Links | `references/link-building.md` | `internal_links.py`, `broken_links.py`, `link_profile.py` |
| Local SEO | `references/local-seo.md` | `local_signals_checker.py` |
| Images | `references/image-seo.md` | `image_checker.py` |
| International / hreflang | `references/international-seo.md` | `hreflang_checker.py` |
| Programmatic SEO | `references/programmatic-seo.md` | `programmatic_seo_auditor.py` |
| Migration | `references/site-migration.md` | `redirect_checker.py` |
| Analytics / myths | `references/analytics-reporting.md` | — |
| Crawl / indexation | `references/crawl-indexation.md` | `sitemap_checker.py`, `duplicate_content.py`, `canonical_checker.py`, `broken_links.py`, `internal_links.py` |

### When *not* to run Mode 1 (full audit)

| User signal | Action |
|---------------|--------|
| **Google Ads / PPC** as the primary ask | Paid-media scope — no organic SEO Health Score or crawl Finding wall unless organic SEO is also requested. |
| Employer branding only, **pure** press/PR distribution, **email-only** marketing | Narrow guidance; no implied full technical + content audit. |
| **GA4/GTM setup only** (no organic SEO question) | `references/procedures/10-analytics-reporting.md` — **no** fabricated domain-wide numeric score. |
| **Social** community management only | Out of scope unless tied to organic discovery (e.g. `sameAs`, entity signals). |
| **Explicitly scoped** task (e.g. “only robots.txt + sitemap”) | Stay in that scope — no domain-wide E-E-A-T essay or `/100` score unless the user asks. |

### Audit Context: Internal vs. Competitive Mode

Before routing, determine which audit context applies. This controls what outputs are valid.

| Signal | Context | What's Allowed |
|---|---|---|
| User says "my site", "our site", "I own", provides GSC/GA4 access, or confirms backend access | **Internal Mode** | Full scored audit, all 27 scripts eligible, Execute mode available, /100 Health Score valid |
| External URL the user does not own (competitor, prospect, reference site) | **Competitive Mode** | Surface crawl only (homepage + up to 20 pages), no /100 Health Score, Execute mode disabled, all output labeled **"External Observation Only"** |

**When in doubt, ask:** "Is this your site, or are you analyzing a competitor?"

This skill operates in three modes. Identify which mode applies before touching anything else.

### The Three Modes

**Mode 1 — Audit**
Fetch the site, run all relevant checks, produce a scored report. Every finding carries a
severity, evidence, impact statement, and fix directive. Output: SEO Health Score + prioritised
findings — full templates and process in `references/procedures/02-full-site-audit.md`.

**Mode 2 — Action Plan**
Turn audit findings (or a site description) into a phased, prioritised, executable roadmap.
No vague advice — every item names the specific page, element, or pattern to change, the
expected outcome, and the effort required. Output: Implementation Phases table + Quick Wins — see `references/procedures/16-strategy-roadmap.md` and Mode 2 format in `references/procedures/02-full-site-audit.md`.

**Mode 3 — Execute**
Do the work. Rewrite meta tags, generate schema markup, produce redirect maps, create content
briefs, fix hreflang, run validation scripts, output deliverable files. Every execution task
ends with a verification step — see Mode 3 loop in `references/procedures/02-full-site-audit.md`.

Most requests involve all three in sequence: **Audit → Plan → Execute**. Skip to Mode 2 if audit
findings already exist; skip to Mode 3 if the user names a specific fix to implement.

### Intake Checklist

Three questions only — skip any already answered in the user's message.

| # | Question | Why It Matters |
|---|---|---|
| 1 | **What is the URL?** | Required for all three modes |
| 2 | **What is the primary goal?** (traffic / AI citations / local leads / traffic drop / specific keyword) | Determines which modules run first |
| 3 | **Which mode?** Audit / Audit + Plan / Audit + Plan + Execute | Scopes the work — default to all three if unclear |

Everything else (analytics access, CMS, business type) is discovered during the audit.

### Mode Routing

```
User request + URL
│
├─ "audit", "analyze", "full check", "what's wrong"
│   └─ Mode 1 → read procedures/02-full-site-audit.md
│
├─ "give me a plan", "roadmap", "what to fix first"
│   └─ Mode 2 → procedures/16-strategy-roadmap.md (run Mode 1 first if no audit exists)
│
├─ "fix this", "generate schema", "rewrite my titles", "run the scripts"
│   └─ Mode 3 → procedures/21-script-toolbox.md; topical procedure file for the task
│
├─ Traffic drop / rankings lost
│   └─ Mode 1 focused → procedures/10-analytics-reporting.md first, then procedures/06-content-eeat-and-pruning.md / procedures/04-technical-seo.md
│
├─ AI citations / GEO question
│   └─ Mode 1 focused → procedures/03-geo-ai-search.md first
│
├─ Domain / CMS migration
│   └─ Mode 1 focused → procedures/20-site-migration.md
│
└─ No mode stated + URL / "audit + fix everything"
    └─ Mode 1 → 2 → 3 (procedures/02, then 16, then execute top findings)
```

Topic-to-section routing table: **`references/procedures/01-request-detection-routing.md`** (same content as former SKILL §1).

### What "Done" Looks Like per Mode

**Audit complete** when: SEO Health Score delivered, all Critical and High findings documented in
Finding/Evidence/Impact/Fix/Confidence/Falsifiability/Leading Indicator format (with First-Principle Observation and Dependency for Critical/High), Assumptions Audit section present, no section skipped without reason stated.

**Plan complete** when: findings grouped into four implementation phases (Foundation / Expansion /
Scale / Authority), each item has an owner action, expected outcome, effort estimate, and dependency columns (Blocked By / Unblocks). Plan is topologically sorted by dependencies.

**Execute complete** when: every fix implemented AND verified — run the relevant validation script,
review the output, confirm it resolves the original finding.

### Context Budget Awareness

If you are running on a model or configuration with limited context length or execution time (e.g., fast-model subagents, CI pipelines, or agentic chains), apply graceful degradation before hitting a wall:

1. **Estimate before executing.** A full Mode 1 audit with `generate_report.py` and all scripts can produce 50k+ tokens of output. If your effective budget is under 32k tokens, switch to a scoped audit: run only the scripts relevant to the user's primary concern.
2. **Prefer partial delivery over timeout.** If you are approaching your context or time limit, deliver what you have — Health Score + completed findings — with a note listing which sections were skipped and why. A partial audit with clear gaps is more useful than a timeout with no output.
3. **Web fetches are expensive.** Each site fetch adds latency and tokens. For scoped tasks (schema only, robots.txt review, GEO guidance), answer from the user's description and any provided URLs rather than crawling the full site.
4. **Compaction fallback.** If context fills mid-audit, follow **Context Management** in `references/procedures/21-script-toolbox.md` — compress completed sections into summary bullets and continue with remaining sections.

This is a **fallback**, not a default. When context budget allows, always prefer the full audit pipeline.

---

## Global guardrails (always apply)

These rules apply to every mode. **Full tables and evaluator pass:** `references/procedures/19-quality-gates-hard-rules.md`.

### Evidence integrity (do not claim without data)

| Claim | Only state if |
|---|---|
| LCP / INP / CLS / performance score | `pagespeed.py` ran successfully, or user pasted PageSpeed Insights / CrUX output |
| Backlink count or referring domains | `link_profile.py` ran and returned data |
| Organic traffic or impression numbers | GSC / GA4 access confirmed and data retrieved |
| Health Score /100 | Internal Mode + minimum 5 scripts ran with data |
| Schema errors or validation status | `validate_schema.py` ran against the page |
| Schema "not found" on a CMS site | Confirmed via Rich Results Test or browser JS — raw HTML cannot detect JS-injected schema |

**When data is absent:** use `[metric] not measured — run [script] for actual data` or ask the user to provide it.

### Finding format (mandatory)

Every finding: **Finding** / **Evidence** / **Impact** / **Fix** / **Confidence** (Confirmed / Likely / Hypothesis) / **Falsifiability** (what would prove this wrong) / **Leading Indicator** (what to monitor post-fix). Critical and High findings also require **First-Principle Observation** and **Dependency**. Apply the PERCEIVE → ANALYZE → VALIDATE → ACT framework from `references/thinking-framework.md`. Example report excerpt: `references/audit-output-example.md`.

### High-Risk execute gate

**High-Risk** changes (robots.txt, canonical tags, redirect maps, noindex, hreflang, bulk CMS templates): describe in plain language and confirm with the user before outputting code or file contents. **Safe** changes (meta, alt text, most schema, content rewrites, llms.txt): may output directly. Full classification table: `references/procedures/02-full-site-audit.md` (Mode 3).

### Before delivering any Mode 1 audit

Run the internal self-evaluation pass in `references/procedures/19-quality-gates-hard-rules.md` (Evaluator-Optimizer checklist).

---

## Procedure file index (§1–§21)

| § | File |
|---|------|
| 1 | [`references/procedures/01-request-detection-routing.md`](references/procedures/01-request-detection-routing.md) |
| 2 | [`references/procedures/02-full-site-audit.md`](references/procedures/02-full-site-audit.md) |
| 3 | [`references/procedures/03-geo-ai-search.md`](references/procedures/03-geo-ai-search.md) |
| 4 | [`references/procedures/04-technical-seo.md`](references/procedures/04-technical-seo.md) |
| 5 | [`references/procedures/05-schema-structured-data.md`](references/procedures/05-schema-structured-data.md) |
| 6–6b | [`references/procedures/06-content-eeat-and-pruning.md`](references/procedures/06-content-eeat-and-pruning.md) |
| 7–7c | [`references/procedures/07-keywords-clusters-aeo.md`](references/procedures/07-keywords-clusters-aeo.md) |
| 8 | [`references/procedures/08-competitor-analysis.md`](references/procedures/08-competitor-analysis.md) |
| 9 | [`references/procedures/09-link-building-internal.md`](references/procedures/09-link-building-internal.md) |
| 10 | [`references/procedures/10-analytics-reporting.md`](references/procedures/10-analytics-reporting.md) |
| 11 | [`references/procedures/11-crawl-indexation.md`](references/procedures/11-crawl-indexation.md) |
| 12 | [`references/procedures/12-local-seo.md`](references/procedures/12-local-seo.md) |
| 13 | [`references/procedures/13-image-seo.md`](references/procedures/13-image-seo.md) |
| 14 | [`references/procedures/14-international-hreflang.md`](references/procedures/14-international-hreflang.md) |
| 15 | [`references/procedures/15-programmatic-seo.md`](references/procedures/15-programmatic-seo.md) |
| 16 | [`references/procedures/16-strategy-roadmap.md`](references/procedures/16-strategy-roadmap.md) |
| 17 | [`references/procedures/17-monthly-maintenance.md`](references/procedures/17-monthly-maintenance.md) |
| 18 | [`references/procedures/18-myths.md`](references/procedures/18-myths.md) |
| 19 | [`references/procedures/19-quality-gates-hard-rules.md`](references/procedures/19-quality-gates-hard-rules.md) |
| 20 | [`references/procedures/20-site-migration.md`](references/procedures/20-site-migration.md) |
| 21 | [`references/procedures/21-script-toolbox.md`](references/procedures/21-script-toolbox.md) |
| 22 | [`references/procedures/22-drift-monitoring.md`](references/procedures/22-drift-monitoring.md) |
| 23 | [`references/procedures/23-semantic-clustering.md`](references/procedures/23-semantic-clustering.md) |
| 24 | [`references/procedures/24-ecommerce-seo.md`](references/procedures/24-ecommerce-seo.md) |
| 25 | [`references/procedures/25-maps-intelligence.md`](references/procedures/25-maps-intelligence.md) |
