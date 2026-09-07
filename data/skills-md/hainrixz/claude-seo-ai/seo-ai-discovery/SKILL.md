---
name: seo-ai-discovery
description: Audit AI discovery files and agent endpoints at the site root — /llms.txt and /llms-full.txt structure and link health, /agents.md, the UCP merchant profile at /.well-known/ucp (only when no ecommerce module owns it), the ARD /.well-known/ai-catalog.json, and /sitemap_agentic_discovery.xml — plus a robots cross-check that these files are not blocked for the bots meant to read them. Module M21 "AI discovery & agent endpoints" (weight 0 — reported, never scored). Appears in the AI Visibility report only.
allowed-tools: Read, Grep, Glob, Bash
---

# seo-ai-discovery (M21 — AI discovery & agent endpoints)

Discovery files tell agents and coding assistants where to look; none of them is a documented answer-engine ranking or citation signal, so every M21 finding is `speculative` or `directional` and the module's weight is **0**. Robots/UA posture lives in `seo-ai-crawlers` (M14); agentic-commerce readiness (UCP + catalog feeds on stores) lives in `seo-ecommerce` (M18).

## Inputs
Work from the PageSnapshot named in your dispatch envelope: `<run_dir>/site/discovery.json` holds the probe results (status, content-type, bytes, raw bodies ≤256 KB) for `/llms.txt`, `/llms-full.txt`, `/agents.md`, `/.well-known/ucp`, `/.well-known/ai-catalog.json`, `/sitemap_agentic_discovery.xml`, `/api/ucp/mcp`; `<run_dir>/site/robots.json` holds the per-bot verdicts for the robots cross-check; `vertical` in the envelope decides UCP ownership. Deterministic findings already emitted by `audit.mjs` are listed in `<run_dir>/findings.deterministic.json` — do not re-emit those ids; add model-judged findings only. If invoked directly with a URL/path and no snapshot exists, first run `node "${CLAUDE_PLUGIN_ROOT}/scripts/snapshot.mjs" <target> --out "${CLAUDE_PLUGIN_DATA}/runs"` and use the printed snapshot path.

## Audits
1. **llms.txt** — present (200, text); llmstxt.org structure: one H1 title, optional summary blockquote, H2 sections of `- [title](url): note` links; linked URLs resolve (`--deep`, ≤25 checked); the file is not disallowed in robots to the AI bots that would read it. `/llms-full.txt` is reported present/absent only.
2. **agents.md** — present/absent; note when it is a platform default (Shopify ships one) — informational.
3. **UCP profile** (`/.well-known/ucp`) — **only when `ecommerce` is not active** (M18 owns it otherwise): public (200, no auth), JSON, `ucp.version` as `YYYY-MM-DD`, `services`/`capabilities` objects keyed by reverse-DNS names → arrays of `{version, spec, transport?, endpoint?, schema}`. Note a declared `dev.shopify.catalog` entry — it says the platform exposes a catalog service, which is a platform default, not a merchant decision.
4. **ARD catalog** (`/.well-known/ai-catalog.json`) — present and parseable JSON. Report-only: v0.9 draft (2026-05-28), near-zero adoption.
5. **Agentic sitemap** (`/sitemap_agentic_discovery.xml`) — present, well-formed XML, sampled `<loc>` entries resolve.

## Fixes
- **AUTO** (`fixable: auto`), **disclosure-gated** and **scored 0**: generate or repair `llms.txt` / `llms-full.txt` from the site's own structure (sitemap URLs + parsed titles) only on explicit request (`fix --category ai-discovery`, alias `llms`), shown as a diff before writing, always with the disclosure that impact is low/uncertain.
- **ADVISORY** (`fixable: advisory`): UCP/ARD/agentic-sitemap adoption, and unblocking a disallowed discovery file (the robots write belongs to M14). The tool never authors a merchant profile — platforms generate those.
- **Never fabricate** link targets, descriptions, endpoints, or versions — ask the user or leave a clearly-marked `TODO` placeholder.

## Verification
- `node "${CLAUDE_PLUGIN_ROOT}/scripts/ai-discovery.mjs" --snapshot <pages/<slug>.json> [--deep]` — re-reads `site/discovery.json`, validates llms.txt structure (`dom_assert`), UCP/ARD JSON shape (`schema_validator`), agentic-sitemap XML (`xml_parse`), and the robots cross-check (`robots_parse`).
- When the discovery probes did not run (no network, local path), status is `needs_api` — never a false `pass`.

## Findings
Conform to `schema/finding.schema.json`; axis `ai`; severity ≤2; confidence `speculative` unless noted. **Severity policy**: 5 is reserved for catastrophic, eligibility-killing facts at site/template scope; 4 major · 3 moderate · 2 minor · 1 cosmetic · 0 informational — and only an `established` severity-5 `fail` in an active category can cap a score (`references/scoring-model.md`). M21's category weight is **0**, so nothing here can move or cap either score whatever its severity. `evidence.observed` quotes the file/probe line verbatim; `verification.reproduce` is the command above; `expected_impact` is banded (no naked %). Ids:
- `M21.llmstxt.missing` (warn 1, `fixable: auto`) · `M21.llmstxt.malformed` (warn 1, `fixable: auto`) · `M21.llmstxt.broken_links` (warn 2, `fixable: proposed`, `directional`) · `M21.llmstxt.blocked_for_ai_bots` (warn 2, `fixable: advisory`, `directional` — file exists but robots disallows it to the bots meant to read it).
- `M21.agents_md.present` (pass 1) · `M21.agents_md.missing` (warn 1, `fixable: advisory`).
- `M21.ucp.present_valid` (pass 2) · `M21.ucp.invalid` (warn 2, `fixable: advisory`) · `M21.ucp.not_public` (warn 2, `fixable: advisory`) — only when ecommerce is inactive; otherwise `not_applicable` naming M18 as owner.
- `M21.ai_catalog.present` (pass 1) · `M21.ai_catalog.invalid_json` (warn 1, `fixable: advisory`).
- `M21.agentic_sitemap.present` (pass 1) · `M21.agentic_sitemap.broken_locs` (warn 2, `fixable: proposed`, `directional`).

## Honesty
- **Google Search ignores llms.txt** — Google's statement (2026-06-15 — TO-VERIFY the exact date; it appears in *Optimizing your website for generative AI features*, updated 2026-07-10, and *AI features and your website* says "no … AI text files"). Never present llms.txt as an AI Overviews / AI Mode lever.
- Vendor support is partial (Anthropic and Perplexity read it in retrieval; OpenAI uncommitted); adoption is ~10% and, per Ahrefs (May 2026), 97% of llms.txt files received zero bot requests. Quote that figure only in `rationale` with the citation — never in `expected_impact`.
- UCP, ARD, and the agentic sitemap concern **agent commerce and resource discovery**, not answer-engine citation. Report them; nothing here moves the AI Visibility score.
- Shopify stores ship all of these by default (May 2026) — their presence on a Shopify store is a platform default, not a merchant merit signal.
