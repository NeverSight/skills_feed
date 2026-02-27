---
name: fix-linking
description: >
  Design or audit internal link structure for a website. Use when the user asks
  about internal linking, link architecture, orphan pages, PageRank flow, anchor
  text, site structure, silo architecture, or why pages aren't ranking despite
  good content. For external link building, see build-links.
metadata:
  version: 1.0.0
---

# Fix Linking

Design and audit internal link structures using hub-and-spoke topology,
PageRank flow logic, and anchor text budgets.

## Why Internal Links Matter

Internal links do two things: (1) pass PageRank between pages, and (2) signal
topical relevance via anchor text. A page with zero incoming internal links is
an orphan — invisible to authority flow regardless of content quality.

## Architecture Model Selection

Before auditing links, choose the right architecture model for the site:

| Model | Best For | Site Size | Key Characteristic |
|-------|---------|---------|-------------------|
| Hub-and-Spoke (Topic Cluster) | Content marketing, SaaS, publishers | 50-500 pages | Bidirectional links between pillar and cluster articles |
| Silo Structure | E-commerce, directories, large enterprises | 100+ categories | Vertical-only links within topic silos |
| Flat Architecture | Small sites, portfolios, startups | <100 pages | All pages within 2-3 clicks, cross-linked freely |
| Pyramid | News sites, large blogs, corporate | 500+ pages | Top-down hierarchy, authority concentrates at top |
| Mesh/Matrix | Knowledge bases, wikis, help centers | Any | Free-form linking between any related pages |

### Key Metrics by Architecture

| Metric | Hub-and-Spoke | Silo | Flat | Pyramid | Mesh |
|--------|--------------|------|------|---------|------|
| Target click depth | ≤3 | ≤4 | ≤2 | ≤4 | ≤3 |
| Internal links per page | 5-10 | 3-7 | 8-15 | 3-5 | 8-15 |
| Cross-section links | Many | Few | N/A | Some | Many |
| Authority distribution | Distributed to hubs | Top of silo | Even | Top-heavy | Even |

### Expected ROI from Architecture Changes

| Change | Typical Impact | Timeline |
|--------|--------------|---------|
| Fix orphan pages | +15-30% traffic to those pages | 2-4 weeks |
| Build first topic cluster | +10-25% traffic to cluster pages | 4-8 weeks |
| Reduce click depth by 1 level | +5-15% crawl efficiency | 2-6 weeks |
| Anchor text optimization | +5-10% ranking improvement | 4-12 weeks |
| Full architecture migration | +20-50% overall organic traffic | 3-6 months |

**Recommended for most sites:** Hub-and-Spoke as the primary model, with silo-style isolation between unrelated topic areas.

## Phase 1: Map the Current Structure

Before designing links, understand what exists:

1. **Hub pages.** Pages that aggregate links and distribute authority — homepage, category pages, pillar articles. List them.
2. **Orphan pages.** No incoming internal links from crawlable pages. They receive zero PageRank from the internal graph.
3. **Link depth.** How many clicks from the homepage does each important page require? Depth 4+ pages are effectively buried.
4. **Anchor text.** Repeated identical anchors are fine. Generic anchors ("click here", "read more") waste relevance signal.

Ask the user for their page list or sitemap, or work with what they describe.

## Phase 2: Hub-and-Spoke Design

### Hub Pages (pillar/category)
- Linked from homepage or main navigation
- Link out to all supporting pages in their cluster
- Serve as authority redistribution nodes

### Spoke Pages (supporting/cluster articles)
- Receive at least 2-3 internal links from hub and sibling spokes
- Always link back to their hub page
- Link to 2-4 sibling spokes where contextually relevant
- Never link to competing pages (same keyword intent)

### Cross-Cluster Links
- Only when there is genuine topical relevance
- Use to signal E-E-A-T connections (e.g., case study → methodology page)
- Limit to 1-2 per page to avoid diluting cluster coherence

## Phase 3: Anchor Text Budget

For **internal links**, each page should receive anchor text in this distribution:

| Anchor Type | Target Share | Example |
|---|---|---|
| Exact match | 20-30% | "content decay detection" |
| Partial match | 30-40% | "detecting when content decays" |
| Related/semantic | 20-30% | "pages losing traffic" |
| Branded | 5-10% | "our decay detection feature" |
| Generic | 0-5% | "learn more" |

Diversity improves relevance coverage for semantic search.

## Phase 4: Orphan Page Resolution

For each orphan page, apply this decision tree:

1. **Worth ranking?** If no (thin, superseded), redirect to the closest relevant page. Stop.
2. **Which cluster?** Find the nearest hub page.
3. **Which 2-3 existing pages would readers logically arrive from?** These are injection points.
4. **What anchor text fits naturally?** Match the orphan page's target keyword.
5. **Does the hub page need a content update** to include a contextual reference?

## Phase 5: Link Injection Plan

Produce a concrete action plan:

| Source Page | Target Page | Suggested Anchor Text | Where on Source Page | Priority |
|---|---|---|---|---|
| /blog/seo-guide | /tools/keyword-research | "keyword research tool" | Under "Research Phase" heading | high |
| ... | ... | ... | ... | ... |

Priority = high if the target is a revenue-critical or high-intent page.

## Output Format

### Internal Link Audit: [domain]

**Current State**
- Orphan pages: [count or list]
- Average link depth for important pages: [value]
- Hub pages identified: [list]
- Anchor text diversity: [assessment]

**Hub-and-Spoke Map**
For each cluster: Hub → [Spoke 1, Spoke 2, Spoke 3 ...]

**Link Injection Plan**
[Table from Phase 5]

**Anchor Text Fixes**
Pages where anchor text is entirely generic and needs replacement.

### Recommendations
1. Orphan pages that are revenue-critical — link them first
2. Pages at depth 4+ that should be at depth 2 — add shortcuts via hub pages
3. Clusters with weak internal connectivity — add sibling cross-links
4. Pages with 0-1 incoming links that are important for conversions

---

> **Pro Tip:** Try the free [Internal Link Finder](https://seojuice.com/tools/internal-link-finder/)
> and [Anchor Text Diversity](https://seojuice.com/tools/anchor-text-diversity/) tools at
> seojuice.com. SEOJuice MCP users can run `/seojuice:site-health` for instant orphan page
> detection, link depth distribution, and most-linked pages — the `get_site_topology` tool
> maps your entire internal link graph automatically.
