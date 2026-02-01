---
name: ai-news
description: >
  Aggregate and analyze AI news from 7 authoritative sources including expert newsletters (Andrew Ng's The Batch),
  research papers (HuggingFace), industry news (TechCrunch, AI News), and community discussions (Reddit, Hacker News).
  Provides deep trend analysis with expert sentiment and community opinions. This skill should be used when the user
  wants a comprehensive AI news digest, research recent developments, understand community sentiment, or stay updated
  on AI trends. Invoke with `/ai-news <days>` (e.g., `/ai-news 3` for past 3 days).
---

# AI News Aggregator

This skill aggregates AI news from 7 authoritative sources and produces a comprehensive, deeply-analyzed report.
It uses a multi-agent workflow for parallel fetching, verification, sentiment analysis, and expert-informed reporting.

## Usage

```
/ai-news <days>
```

**Arguments:**
- `days` (optional, default: 7) - Number of days to look back from today

**Examples:**
- `/ai-news 3` - Get AI news from the past 3 days
- `/ai-news 7` - Get AI news from the past week
- `/ai-news` - Same as `/ai-news 7`

## News Sources (7 Total)

### Expert & Newsletter Sources
| Source | Type | URL | Value |
|--------|------|-----|-------|
| The Batch | Expert Newsletter | https://www.deeplearning.ai/the-batch/ | Andrew Ng's expert analysis |
| smol.ai | Curated Digest | https://news.smol.ai/ | Daily AI news roundup |

### Research Sources
| Source | Type | URL | Value |
|--------|------|-----|-------|
| HuggingFace Papers | Trending Research | https://huggingface.co/papers | Community-voted papers |

### Industry News
| Source | Type | URL | Value |
|--------|------|-----|-------|
| TechCrunch AI | Startup/Funding | https://techcrunch.com/category/artificial-intelligence/ | VC, launches, M&A |
| AI News | Enterprise | https://www.artificialintelligence-news.com/ | Business adoption |

### Community Sources
| Source | Type | URL | Value |
|--------|------|-----|-------|
| Reddit ML | Community Discussion | r/MachineLearning, r/LocalLLaMA | Sentiment, hot takes |
| Hacker News | Dev Discussion | https://news.ycombinator.com/ | Technical discourse |

## Multi-Agent Workflow

Execute this workflow in order:

### Phase 1: Planning (Main Orchestrator)

1. Parse the `<days>` argument (default to 7 if not provided)
2. Calculate the date range: `[today - days, today]`
3. Prepare to spawn 7 parallel executor agents

### Phase 2: Parallel Execution

Spawn agents in parallel using Bash tool, each running one fetcher script:

```bash
# Run all 7 fetchers in parallel (from project root)
uv run python .claude/skills/ai-news/scripts/fetch_smol_news.py <days>
uv run python .claude/skills/ai-news/scripts/fetch_hf_papers.py <days>
uv run python .claude/skills/ai-news/scripts/fetch_hn_ai.py <days>
uv run python .claude/skills/ai-news/scripts/fetch_ai_news.py <days>
uv run python .claude/skills/ai-news/scripts/fetch_techcrunch.py <days>
uv run python .claude/skills/ai-news/scripts/fetch_the_batch.py <days>
uv run python .claude/skills/ai-news/scripts/fetch_reddit_ml.py <days> --min-score 20
```

**Key Outputs:**
- Each script returns JSON with items, metadata, and source info
- Reddit script includes `community_sentiment` with hot topics and engagement stats
- The Batch includes expert attribution

### Phase 3: Verification & Deduplication

After collecting results from all sources:

1. **Date Range Validation**: Confirm all items fall within `[start_date, end_date]`
2. **Deduplication**: Remove duplicate stories across sources
   - Match by URL or title similarity (>80% match)
   - Keep the version with most metadata
3. **Quality Filter**: Remove low-quality or off-topic items

### Phase 4: Deep Analysis & Sentiment Extraction

This is the **critical phase** for producing a valuable report. Perform these analyses:

#### 4.1 Theme Clustering
Group all items into major themes:
- **Research & Models**: New architectures, benchmarks, capabilities
- **Industry & Business**: Funding, acquisitions, enterprise adoption
- **Tools & Infrastructure**: Developer tools, APIs, frameworks
- **Policy & Safety**: Regulation, alignment, ethics
- **Applications**: Real-world deployments, use cases

#### 4.2 Trend Identification
For each major theme, analyze:
- What's the narrative arc? (emerging, maturing, declining)
- How many sources cover this topic?
- What's the engagement level (scores, comments)?

#### 4.3 Expert Sentiment Extraction
From **The Batch** (Andrew Ng) articles:
- Extract key opinions and predictions
- Note any warnings or concerns raised
- Identify recommended actions or takeaways

#### 4.4 Community Sentiment Analysis
From **Reddit** and **Hacker News**:
- What are the hot topics people are excited about?
- What criticisms or concerns are being raised?
- What's the overall mood (optimistic, skeptical, concerned)?
- Use the `community_sentiment` data from Reddit fetch

#### 4.5 Cross-Source Correlation
Identify stories that appear across multiple sources:
- Research paper on HuggingFace + discussed on Reddit
- Industry news on TechCrunch + expert analysis in The Batch
- These cross-source items are often the most significant

### Phase 5: Report Generation

Generate a **comprehensive, detailed report** with these sections:

```markdown
# AI News Report: [Start Date] to [End Date]

## Executive Summary
[3-4 paragraphs providing a narrative overview of the most important developments.
Start with the single biggest story, then cover 2-3 other major themes.
End with a forward-looking statement about what to watch.]

---

## Top Stories This Period

### 1. [Most Important Story Title]
**Sources:** [list sources covering this]
**Why It Matters:** [2-3 sentences on significance]
**Expert Take:** [Quote or paraphrase from The Batch if available]
**Community Reaction:** [Sentiment from Reddit/HN if available]
[Link to primary source]

### 2. [Second Most Important Story]
[Same structure...]

### 3. [Third Most Important Story]
[Same structure...]

---

## Trend Deep Dives

### Trend 1: [Trend Name]
**What's Happening:** [Detailed explanation of the trend]
**Key Evidence:**
- [Paper/Article 1 with link]
- [Paper/Article 2 with link]
- [Paper/Article 3 with link]

**Expert Analysis:** [What experts are saying - from The Batch, etc.]

**Community Sentiment:** [What Reddit/HN thinks]
- Hot takes: [Notable comments or discussions]
- Concerns raised: [Any skepticism or criticism]

**What This Means:** [Implications for practitioners, businesses, researchers]

**What to Watch:** [Future developments to monitor]

### Trend 2: [Trend Name]
[Same detailed structure...]

### Trend 3: [Trend Name]
[Same detailed structure...]

---

## Research Highlights

### Papers of the Week
[For each top paper from HuggingFace:]

#### [Paper Title]
- **Link:** [arxiv/HF link]
- **TL;DR:** [1-2 sentence summary]
- **Why Notable:** [What makes this significant]
- **Upvotes:** [engagement metric]

[Repeat for top 5-10 papers]

### Research Themes
[Group papers by theme with brief analysis]

---

## Industry & Business News

### Funding & Acquisitions
[List with brief analysis of what it signals]

### Product Launches
[Notable AI product launches with impact assessment]

### Enterprise Adoption
[Companies adopting AI, partnerships, deployments]

### Policy & Regulation
[Any regulatory news or policy developments]

---

## Community Pulse

### Hot Topics on Reddit
**Top Discussions:**
1. [Title] - [score] points, [comments] comments
   - Key debate: [what people are arguing about]
2. [Title] - [score] points, [comments] comments
   - Key insight: [notable comment or consensus]

**Community Sentiment:**
- Overall mood: [optimistic/skeptical/mixed]
- Hot topics: [list from sentiment analysis]
- Emerging interests: [what's gaining traction]

### Hacker News Highlights
[Notable AI discussions with key points]

---

## Expert Corner: The Batch by Andrew Ng

### This Week's Key Insights
[Summarize main points from The Batch articles]

### Andrew Ng's Take
[Direct quotes or paraphrased expert opinion]

### Recommended Actions
[Any actionable advice from expert sources]

---

## What This All Means

### For Researchers
[Implications and opportunities]

### For Practitioners/Engineers
[What to learn, tools to try, skills to develop]

### For Business Leaders
[Strategic implications, investment signals]

### For the Broader AI Field
[Where things are heading, big picture trends]

---

## Full Item List

### By Date (Most Recent First)
[Complete chronological list with:
- Date
- Title (linked)
- Source
- Brief description if available]

---

## Report Metadata
- **Date Range:** [Start] to [End]
- **Total Items Analyzed:** [count]
- **Sources Consulted:** [list of 7 sources]
- **Generated:** [timestamp]
```

### Phase 5.1: Persist Report

After generating the report markdown, save it to disk:

```bash
cat <<'EOF' | uv run python .claude/skills/ai-news/scripts/write_report.py \
  --start-date YYYY-MM-DD \
  --end-date YYYY-MM-DD \
  --days N \
  --sources-ok source1,source2 \
  --sources-failed source3 \
  --total-items COUNT
<REPORT MARKDOWN HERE>
EOF
```

The script will:
- Write the report to `reports/ai-news_START_to_END_TIMESTAMP.md`
- Update `reports/manifest.jsonl`
- Copy to `reports/latest.md`
- Return JSON with filepath and metadata

Verify the JSON response includes `filepath` (and other expected fields) after the command runs.

**Important:** Always run this after displaying the report to the user.

### Phase 5.2: Render HTML

After saving the markdown, generate a self-contained HTML version alongside it:

```bash
uv run python .claude/skills/ai-news/scripts/render_html.py /path/to/report.md
```

The script writes `/path/to/report.html` (same basename) and prints the HTML filepath to stdout. Use the
`filepath` returned from Phase 5.1 as the input path.

### Phase 5.3: Upload to Cloudflare Archive (Optional)

If the `ADMIN_API_SECRET` environment variable is set, upload the HTML report to the Cloudflare archive:

```bash
ADMIN_API_SECRET=$ADMIN_API_SECRET uv run python .claude/skills/ai-news/scripts/upload_to_cloudflare.py \
  /path/to/report.html \
  --start-date YYYY-MM-DD \
  --end-date YYYY-MM-DD \
  --days N \
  --total-items COUNT
```

The script uploads the HTML to Cloudflare R2 and updates the KV index. The report will be immediately available at:
- Archive listing: https://julienh15.github.io/AI-News-Reports/archive/
- Direct link: https://ai-news-signup.julienh15.workers.dev/archive/{report_id}

**Note:** This step is optional and only runs if `ADMIN_API_SECRET` is available in the environment.

## Scripts Reference

All scripts are in `.claude/skills/ai-news/scripts/` directory:

| Script | Source | API/Method | Special Features |
|--------|--------|------------|------------------|
| `fetch_smol_news.py` | smol.ai | RSS feed | Curated summaries |
| `fetch_hf_papers.py` | HuggingFace | Date-based URL | Upvote counts |
| `fetch_hn_ai.py` | Hacker News | Algolia API | AI keyword filtering |
| `fetch_ai_news.py` | AI News | HTML scraping | Enterprise focus |
| `fetch_techcrunch.py` | TechCrunch | RSS feed | Startup/funding focus |
| `fetch_the_batch.py` | The Batch | HTML parsing | Expert analysis |
| `fetch_reddit_ml.py` | Reddit | JSON API | Sentiment analysis |
| `render_html.py` | Markdown | python-markdown | Self-contained HTML output |
| `upload_to_cloudflare.py` | Cloudflare | Worker API | Upload to R2 + KV archive |

## Error Handling

- If a source fails, continue with available sources
- Report which sources succeeded/failed in the output
- Minimum viable report requires at least 2 sources

## Quality Guidelines

### Report Length
- Executive Summary: 300-500 words
- Each Trend Deep Dive: 400-600 words
- Total report: 2000-4000 words depending on activity level

### Analysis Depth
- Don't just list items - explain significance
- Connect dots across sources
- Provide actionable insights
- Include both optimistic and critical perspectives

### Linking
- Every claim should link to a source
- Use markdown hyperlinks consistently
- Include both discussion links and original sources

## Architecture Reference

See `references/ARCHITECTURE.md` for detailed workflow diagrams and technical specifications.
