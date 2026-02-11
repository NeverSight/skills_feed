---
name: deep-research
description: Conduct comprehensive, multi-round research that produces rich visual reports. Use when asked for "deep research", "comprehensive analysis", "compare frameworks", "evaluate options", "research the state of X", or any task requiring investigation across 10+ sources. NOT for quick lookups — this is a 5-15 minute deep dive that produces a briefing-quality artifact with screenshots, diagrams, tables, and cited findings.
---

# Deep Research

Produce Gemini Deep Research-quality output: rich artifacts with embedded screenshots, mermaid diagrams, comparison tables, and narrative synthesis. Tuned for developer decisions — framework selection, architecture patterns, dependency evaluation, competitive analysis.

## When to Use This Skill

- "Research the current state of X"
- "Compare Framework A vs Framework B"
- "What are the best approaches for..."
- "Deep dive into..."
- Any request where the answer requires **synthesizing information from many sources**

**Do NOT use for**: quick factual lookups, single-source answers, or "find me a CSS button" (use `design-lookup` instead).

## Input Protocol — Before Any Search

1. **Decompose** the topic into 3-5 research axes.
   - Example: "Compare Next.js vs Remix" → Performance, DX, Ecosystem, Deployment, Community
2. **Identify the decision context** — what is the user actually deciding?
   - Framework choice? Architecture pattern? Build vs buy? Migration risk?
3. **Draft a research plan** — present 3-5 axes with planned queries to the user.
   - Save it as an artifact (e.g., `research_plan.md`).
   - Proceed on approval, or refine if the user redirects scope.

## Phase 1: Breadth Scan

**Goal**: Map the landscape. Find *what exists* before reading anything.

1. Run **5-8 parallel searches** across different axes. Use at least two tools:
   - `tavily_search` — broad topic queries
   - `search_web` — alternate search perspective
   - `tavily_research` — delegate an entire sub-question (powerful for "state of X" queries)
2. **Dev-specific breadth**:
   - `search_code` or `search_repositories` — find relevant GitHub repos
   - Search npm trends, bundle sizes, download counts when evaluating packages
   - Search for migration stories: "migrating from X to Y" experience reports
3. Collect **15-25 candidate URLs**, not 5. Score each by authority tier (see [references/research-heuristics.md](references/research-heuristics.md)).
4. **Do not stop at snippets.** Snippets are for candidate selection only.

**Output**: Candidate source list with tier ratings. Present to user if interactive, or proceed if autonomous.

## Phase 2: Deep Read

**Goal**: Extract actual content — implementation details, code examples, benchmarks, data.

1. **Select the top 8-12 sources** from Phase 1 (prioritize S and A tier).
2. **Full extraction** — get the complete page content:
   - `tavily_extract` or `read_url_content` for text-heavy pages
   - `tavily_crawl` to follow documentation multi-page structures
   - `browser_subagent` to **screenshot** key pages (UIs, dashboards, architecture diagrams)
   - `get_file_contents` (GitHub MCP) to read actual source code from repos
3. **Analyze each source**:
   - Extract specific claims, numbers, patterns, code examples
   - Note the authority tier and any bias (is this the framework's own marketing?)
   - Tag findings by research axis
4. **Self-correction**: If a source is fluff (marketing-only, thin tutorial, SEO filler):
   - Discard it
   - Run a refined follow-up search with more specific terms
   - Try adding: "benchmark", "technical deep dive", "lessons learned", "postmortem"

**Output**: Annotated source notes organized by axis.

## Phase 3: Synthesis

**Goal**: Build the research briefing artifact. This is the main deliverable.

1. **Choose the report template** from [references/report-templates.md](references/report-templates.md):
   - **Comprehensive Brief** — for landscape/state-of-the-art research
   - **Comparison Brief** — for head-to-head evaluations
2. **Write the report as a rich markdown artifact**:
   - **Narrative prose** in the executive summary — not bullets, not lists. Write as if briefing a tech lead.
   - **Comparison tables** with real data extracted from sources
   - **Mermaid diagrams** for architecture, decision trees, ecosystem maps
   - **Embedded screenshots** captured via `browser_subagent` during Phase 2
   - **Code examples** pulled from actual repos or docs
   - Use `generate_image` for custom visualizations when no screenshot captures the concept
3. **Cite every claim** — link to the source URL inline. Use the format: `[Source Name](URL)`.
4. **Gap analysis** — explicitly call out:
   - What couldn't be determined and why
   - Conflicting information between sources
   - Areas where only low-tier sources were found

**Output**: The research artifact (e.g., `research_report.md`).

## Phase 4: Iteration

**Goal**: Fill gaps identified in Phase 3.

1. Review the gap analysis section of your report.
2. For each fillable gap:
   - Run 1-2 targeted searches with refined queries
   - Extract and read the results
   - Update the report artifact in-place
3. **Max 3 total iterations** (Phase 1-3 = round 1, then up to 2 more targeted rounds).
4. After final iteration, mark remaining gaps as "Unresolved" with explanation.

## Tool Strategy

| Purpose | Primary | Fallback |
|---------|---------|----------|
| Topic discovery | `tavily_search` | `search_web` |
| Delegated deep research | `tavily_research` | Manual multi-search |
| Full page extraction | `tavily_extract` | `read_url_content` |
| Multi-page docs | `tavily_crawl` | `tavily_map` + manual |
| Visual evidence | `browser_subagent` (screenshot) | `generate_image` |
| GitHub analysis | `search_code`, `get_file_contents` | `read_url_content` on raw GitHub |
| Architecture diagrams | Mermaid in markdown | `generate_image` |
| Data visualization | Markdown tables | `generate_image` for charts |

## Quality Gates

Before delivering the report, verify:

- [ ] **Source diversity** — at least 1 S-tier and 2 A-tier sources cited (or explicitly flagged as unavailable)
- [ ] **Visual richness** — at least 1 screenshot/image AND 1 diagram/table embedded
- [ ] **Narrative quality** — executive summary reads as prose, not bullet points
- [ ] **Citation completeness** — every factual claim links to a source
- [ ] **Gap transparency** — gaps and conflicts are explicitly documented
- [ ] **Actionable output** — recommendations section exists with ranked, specific advice

## Anti-Patterns

- **Snippet-only research** — stopping at search result descriptions without full extraction
- **Text-wall reports** — no visuals, no tables, no diagrams. The whole point is richness.
- **Source-by-source organization** — findings must be grouped thematically by research axis, not by URL
- **Single-tool reliance** — use at least 2 different search/extraction tools for source diversity
- **Uncited claims** — every substantive finding must link to its source
- **Marketing echo** — repeating a framework's own marketing claims without independent verification
- **Premature stopping** — delivering after 3-5 sources when the topic warrants 15+

## References

- **Source authority scoring and query patterns**: [references/research-heuristics.md](references/research-heuristics.md)
- **Report structure templates**: [references/report-templates.md](references/report-templates.md)
