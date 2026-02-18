---
name: seo-ai-optimizer
version: 1.0.0
description: Audits and optimizes website codebases for SEO and AI bot scanning. Covers technical SEO (meta tags, sitemaps, robots.txt, canonical URLs, page speed hints, structured data), content SEO (heading structure, alt text, readability), and AI bot accessibility (llms.txt, GPTBot/ClaudeBot directives, ai-plugin.json, Schema.org/JSON-LD). Use when user asks to "optimize for SEO", "audit SEO", "improve search rankings", "make site AI-friendly", "add structured data", "fix meta tags", or "optimize for AI bots". Works with any web framework.
---

# SEO & AI Bot Optimizer

Audit and optimize website codebases for search engines and AI systems.

## Important

- ALWAYS audit first, present findings, then propose a plan -- never modify files without user approval
- Fetch latest best practices via web search during each audit to supplement embedded knowledge
- For large codebases (100+ pages), audit a representative sample and offer to expand

## Workflow

1. **Detect** -- Identify project framework and scan for relevant files
2. **Audit** -- Run automated scan + manual review across 4 categories
3. **Research** -- Web search for latest SEO/AI bot best practices
4. **Report** -- Present findings grouped by severity
5. **Plan** -- Propose prioritized improvements for user approval
6. **Implement** -- Apply approved changes
7. **Validate** -- Re-check modified files

---

## Step 1: Detect Project Type

Run the audit script to detect framework and scan files:

```bash
python scripts/audit_seo.py <project-root>
```

The script automatically:
- Detects the framework (Next.js, Nuxt, Astro, Hugo, SvelteKit, static HTML, etc.)
- Finds all HTML/template files (excluding node_modules, build dirs)
- Samples representative files for large codebases

If the script reports "No HTML/template files found," inform the user: this skill is designed for web frontends with HTML output.

For framework-specific configuration guidance, consult `references/framework-configs.md`.

## Step 2: Audit

The audit script checks **per-file issues** and **project-level issues**.

### Per-File Checks (automated)
- **Technical SEO:** title tag, meta description, viewport, charset, canonical, lang attribute
- **Content SEO:** H1 presence/count, heading hierarchy, image alt text, image dimensions
- **Structured Data:** JSON-LD presence/validity, OpenGraph tags, Twitter Cards
- **Performance:** render-blocking scripts, lazy-loading on LCP candidates

### Project-Level Checks (automated)
- robots.txt existence and AI bot directives
- sitemap.xml existence (or sitemap generation package)
- llms.txt existence
- ai-plugin.json existence

### Manual Review (after script)

After running the script, manually review these items that require human judgment:

1. **Title/description quality** -- Are they compelling and keyword-relevant? (not just present)
2. **Structured data accuracy** -- Does JSON-LD match visible page content?
3. **Internal linking** -- Are pages reachable within 3 clicks? Descriptive anchors?
4. **Content depth** -- Sufficient E-E-A-T signals? Author bios? Source citations?
5. **Framework-specific config** -- Are SEO packages properly configured?

Consult `references/technical-seo.md` for the full checklist.

## Step 3: Research Latest Best Practices

Use web search to check for updates:

```
Search: "SEO best practices [current year]"
Search: "AI bot robots.txt directives [current year]"
Search: "llms.txt specification latest"
Search: "Google algorithm update [current month/year]"
```

Compare findings with embedded knowledge in `references/` and note any new recommendations.

## Step 4: Report

Present the audit report to the user in this format:

```markdown
## SEO & AI Bot Audit Report

**Project:** [project name]
**Framework:** [detected framework]
**Files audited:** [N] / [total]
**Date:** [date]

### Critical Issues (must fix)
1. [File:line] Issue description
2. ...

### Warnings (should fix)
1. [File:line] Issue description
2. ...

### Info (nice to have)
1. Issue description
2. ...

### Project-Level Findings
- robots.txt: [status]
- sitemap.xml: [status]
- llms.txt: [status]
- Structured data: [status]
- AI bot directives: [status]

### Latest Best Practices (from web search)
- [Any new recommendations not covered by existing fixes]
```

## Step 5: Plan

Present a prioritized improvement plan:

```markdown
## Improvement Plan

### Priority 1: Critical Fixes
- [ ] [Fix description] -- [file(s) affected]
- [ ] ...

### Priority 2: Warnings
- [ ] [Fix description] -- [file(s) affected]
- [ ] ...

### Priority 3: Enhancements
- [ ] [Fix description] -- [file(s) affected]
- [ ] ...

### New Files to Create
- [ ] robots.txt with AI bot directives
- [ ] sitemap.xml (or install generation package)
- [ ] llms.txt
- [ ] JSON-LD structured data
```

Ask the user: "Which improvements should I implement? You can approve all, select specific items, or modify the plan."

Do NOT proceed without explicit approval.

## Step 6: Implement

Apply approved changes. For each category:

### Technical SEO Fixes
- Add/fix meta tags, title, description, viewport, charset, canonical, lang
- For framework-specific implementation, consult `references/framework-configs.md`

### robots.txt with AI Bot Directives
- Consult `references/ai-bot-guide.md` for the full list of AI crawlers
- Ask user preference: allow all AI bots, allow search only, or block all
- Include sitemap reference: `Sitemap: https://example.com/sitemap.xml`

### llms.txt Generation
- Create based on site structure and content
- Follow format in `references/ai-bot-guide.md`
- Include H1 with site name, blockquote summary, H2 sections with key page links

### Structured Data (JSON-LD)
- Add Organization schema on homepage
- Add Article/BlogPosting on content pages
- Add Product on e-commerce pages
- Add BreadcrumbList for navigation
- Consult `references/ai-bot-guide.md` for templates

### OpenGraph & Twitter Cards
- Add og:title, og:type, og:image, og:url, og:description
- Add twitter:card, twitter:title, twitter:description, twitter:image

### sitemap.xml
- Generate or install appropriate package for the framework
- See `references/framework-configs.md` for framework-specific packages

## Step 7: Validate

After implementing changes:

1. Re-run the audit script on modified files:
   ```bash
   python scripts/audit_seo.py <project-root>
   ```

2. Verify critical issues are resolved
3. Report remaining warnings to user

## Error Handling

### No HTML Files Found
**Cause:** API-only backend or non-web project.
**Solution:** Inform user this skill is for web frontends. Exit gracefully.

### Framework Config Not Found
**Cause:** Framework detected but config file missing or non-standard location.
**Solution:** Warn and skip framework-specific optimizations. Proceed with generic HTML analysis.

### Web Search Fails
**Cause:** Network issues or rate limiting.
**Solution:** Fall back to embedded best practices in `references/`. Note that latest guidelines could not be fetched.

### Large Codebase
**Cause:** 100+ HTML/template files.
**Solution:** The audit script samples 50 representative files by default. Offer to increase with `--max-files N`.

---

## Triggering Tests

Should trigger:
- "Optimize this website for SEO"
- "Audit my site's meta tags"
- "Make this site friendly for AI bots"
- "Add structured data to my pages"
- "Check if my robots.txt handles AI crawlers"
- "Improve my site's search rankings"
- "Add llms.txt to my project"
- "Fix SEO issues in this codebase"

Should NOT trigger:
- "Write a blog post about SEO"
- "Build me a landing page"
- "Set up Google Ads"
- "Help me write marketing copy"
- "Create a REST API endpoint"

## Functional Tests

### Test: Full audit on Next.js project
Given: A Next.js project with missing meta tags and no robots.txt
When: User asks "audit SEO for this project"
Then:
  - Framework detected as Next.js
  - Missing meta tags flagged as critical
  - Missing robots.txt flagged as warning
  - Missing llms.txt flagged as info
  - Report presented with severity grouping

### Test: Implement approved fixes
Given: Audit report with 3 critical issues approved by user
When: User approves all fixes
Then:
  - Meta tags added to layout/head component
  - robots.txt created with AI bot directives
  - Re-validation shows 0 critical issues

### Test: Graceful handling of API-only project
Given: A project with no HTML files (pure API backend)
When: User asks "optimize for SEO"
Then:
  - Script detects no HTML files
  - Skill informs user and exits without changes
