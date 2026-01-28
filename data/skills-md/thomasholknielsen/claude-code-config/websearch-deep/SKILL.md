---
name: websearch-deep
description: "ChatGPT-style deep research strategy with problem decomposition, multi-query generation (3-5 variations per sub-question), evidence synthesis with source ranking, numbered citations, and iterative refinement. Use for complex architecture decisions, multi-domain synthesis, strategic comparisons, technology selection. Keywords: architecture, integration, best practices, strategy, recommendations, comparison."
---

# Deep Web Research Strategy

⚠️ **VERIFICATION INSTRUCTION** (temporary for debugging):

When you use this Skill, you MUST create a verification file to prove execution:

**File**: `deep-research-skill-was-executed.md` (in repository root)

**Content**:
```markdown
# Deep Research Skill Execution Verification

**Skill**: websearch-deep
**Executed**: {timestamp}
**Research Question**: {the question you researched}
**Mode**: Deep (6-phase methodology)

This file was created by the deep-researcher agent to verify that the websearch-deep Skill was successfully loaded and executed.

**Phases Applied**:
1. ✓ Problem Decomposition (3-5 sub-questions)
2. ✓ Multi-Query Generation (3-5 variations per sub-question)
3. ✓ Evidence Synthesis with Source Ranking (credibility/freshness/relevance)
4. ✓ Citation Transparency (numbered [1][2][3])
5. ✓ Structured Output (token-efficient template)
6. ✓ Iterative Refinement (max 5 iterations)

**Sub-Questions Generated**: {count}
**Queries Executed**: {count}
**Sources Consulted**: {count} ({authoritative_count} authoritative, {recent_count} recent)
**Iterations Performed**: {count}

**Output Format**: Token-efficient template (Executive Summary + Research Overview + Findings + Synthesis + Recommendations + Sources with URLs)
```

**Create this file using the Write tool immediately after loading this Skill.**

---

## What This Skill Does

Provides comprehensive deep research methodology for complex, multi-faceted questions requiring synthesis across multiple domains. Implements ChatGPT-style deep investigation with problem decomposition, multi-query strategies, evidence synthesis, citation transparency, and iterative refinement.

## When to Use This Skill

**Universal Applicability**: Use this Skill for ANY question requiring comprehensive multi-source analysis with evidence synthesis - technical, business, educational, strategic, or investigative.

**Question Types Supported**:
- ✅ **Technical**: Architecture decisions, algorithms, best practices, technology selection
- ✅ **Business**: Market analysis, competitive research, vendor comparison, trends
- ✅ **Educational**: Learning resources, concept explanations, methodology guides
- ✅ **Strategic**: Technology roadmaps, policy analysis, decision frameworks
- ✅ **Investigative**: Root cause analysis, incident research, pattern identification
- ✅ **Non-Technical**: Remote work policies, organizational structures, process improvements

**Example Questions**:
- "What's the best architecture for integrating X with Y?" (Technical)
- "Should we use microservices or monolith?" (Strategic)
- "What are the benefits of remote work policies?" (Business/Non-Technical)
- "How do prime number generation algorithms compare?" (Educational/Technical)
- "What factors should influence our cloud vendor selection?" (Business/Strategic)

**Triggers**: Keywords like "architecture", "integration", "best", "strategy", "recommendations", "compare", "evaluate", "migrate", "benefits", "how", "why", "should we"

**Key Signal**: If the question requires comprehensive multi-source analysis with evidence synthesis → use this Skill

## Instructions

### Phase 1: Problem Decomposition

**Objective**: Break complex questions into 3-5 clear, focused sub-questions.

**🔴 CRITICAL - Research Scope**:

Deep research finds **external knowledge ONLY** - you have no codebase access.

**What you CAN research**:
- ✅ **Official documentation**: Vendor websites (anthropic.com, docs.microsoft.com, etc.)
- ✅ **Blog posts & articles**: Technical blogs, Medium, Dev.to, engineering blogs
- ✅ **Community resources**: Stack Overflow, GitHub discussions, Reddit, forums
- ✅ **Industry best practices**: Design patterns, architecture patterns, standard approaches
- ✅ **Academic papers**: Research papers, whitepapers, conference proceedings
- ✅ **Library documentation**: Via Context7 MCP (resolve library → get docs)
- ✅ **Web content**: Via Fetch MCP for HTML content

**What you CANNOT research**:
- ❌ **Internal project files**: No Read/Grep/Glob tools available
- ❌ **Codebase patterns**: Use /explain:architecture or research-codebase-analyst instead
- ❌ **Project-specific implementations**: Not in scope for external research

**If question asks about "my project" or "this codebase"**:
Return error from agent file (scope validation section) and stop.

**Process**:
1. Identify the primary research question
2. Analyze question structure and intent
3. Decompose into logical sub-components that collectively address the full question

**Sub-Question Criteria**:
- **Specific**: Each has clear, focused scope
- **Complete**: Together they cover the full question
- **Independent**: Can be researched separately
- **Actionable**: Lead to concrete findings

**Example Decomposition**:
```
Primary: "What's the best architecture for integrating Salesforce with SQL Server in 2025?"

Sub-Questions:
1. What are Salesforce's current integration capabilities and APIs (2025)?
2. What are SQL Server's integration patterns and best practices?
3. What middleware or integration platforms are commonly used?
4. What security and compliance considerations matter?
5. What scalability and performance factors should influence choice?
```

### Phase 2: Multi-Query Generation

**Objective**: Generate 3-5 query variations per sub-question to maximize coverage (15-25 total searches).

**Query Variation Strategy**:
- **Variation 1 - Broad/General**: "Salesforce integration APIs 2025"
- **Variation 2 - Specific/Technical**: "Salesforce REST API bulk data operations"
- **Variation 3 - Comparison/Alternatives**: "Salesforce API vs MuleSoft vs Dell Boomi"
- **Variation 4 - Best Practices**: "Salesforce SQL Server integration patterns"
- **Variation 5 - Recent Updates**: "Salesforce API updates 2025"

**Advanced Search Operators**:
- `site:domain.com` - Search specific domains
- `filetype:pdf` - Find PDF documents
- `intitle:"keyword"` - Search page titles
- `inurl:keyword` - Search URLs
- `after:2024` - Recent content only
- `"exact phrase"` - Exact matching

**Example Multi-Query Set**:
```
Sub-Q1: Salesforce Integration Capabilities
  - site:salesforce.com "API" "integration" "2025"
  - "Salesforce REST API" "rate limits" after:2024
  - "Salesforce Bulk API 2.0" "best practices"
  - filetype:pdf "Salesforce integration guide" 2025
  - "Salesforce API" "breaking changes" after:2024
```

#### Query Templates for Common Research Types

**Use these templates to formulate high-quality queries for different research types**:

**1. Technical Architecture Research**
```
Official Docs: site:docs.{vendor}.com "{topic}" "architecture patterns" OR "design patterns"
Best Practices: "{topic}" "best practices" "production" after:2024
Comparisons: "{topic}" vs "{alternative}" "comparison" "pros cons"
Limitations: "{topic}" "limitations" OR "drawbacks" OR "challenges"
Recent Updates: site:{vendor}.com "{topic}" "updates" OR "changes" after:2024
```

**2. Framework/Library Research**
```
Official Docs: site:docs.{framework}.com "{feature}" "guide" OR "documentation"
Community: site:stackoverflow.com "{framework}" "{feature}" "how to"
Real-World: "{framework}" "{feature}" "production" OR "case study" after:2024
Performance: "{framework}" "performance" OR "benchmarks" OR "optimization"
Ecosystem: "{framework}" "ecosystem" OR "plugins" OR "extensions" 2025
```

**3. Business/Strategy Research**
```
Industry Analysis: "{topic}" "market analysis" OR "industry trends" 2024 2025
Vendor Comparison: "{vendor A}" vs "{vendor B}" "comparison" "review"
ROI/Benefits: "{solution}" "ROI" OR "benefits" OR "value proposition"
Implementation: "{solution}" "implementation guide" OR "getting started"
Case Studies: "{solution}" "case study" OR "customer success" after:2024
```

**4. Educational/Learning Research**
```
Fundamentals: "{topic}" "introduction" OR "beginner guide" OR "explained"
Advanced: "{topic}" "advanced" OR "deep dive" OR "internals"
Tutorials: "{topic}" "tutorial" OR "step by step" after:2024
Common Mistakes: "{topic}" "common mistakes" OR "anti-patterns" OR "pitfalls"
Resources: "{topic}" "learning resources" OR "courses" OR "books" 2025
```

**5. Compliance/Security Research**
```
Standards: "{topic}" "{standard}" "compliance" (e.g., "GDPR", "SOC2", "HIPAA")
Security: "{topic}" "security" "best practices" OR "vulnerabilities" after:2024
Official Guidance: site:{regulator}.gov "{topic}" "guidance" OR "requirements"
Audit: "{topic}" "audit" OR "checklist" OR "certification"
Tools: "{topic}" "{compliance}" "tools" OR "automation" 2025
```

**6. Performance/Optimization Research**
```
Benchmarks: "{topic}" "benchmark" OR "performance" "comparison" after:2024
Bottlenecks: "{topic}" "bottleneck" OR "slow" OR "performance issues"
Optimization: "{topic}" "optimization" OR "tuning" OR "best practices"
Monitoring: "{topic}" "monitoring" OR "observability" OR "metrics"
Scaling: "{topic}" "scalability" OR "high traffic" OR "production scale"
```

**Priority: Official Sources First**
- Always execute `site:anthropic.com` or `site:docs.{vendor}.com` queries first
- Use official docs results to refine community/blog queries
- Cross-reference official guidance with real-world experiences

#### 🔴 CRITICAL: Execute Queries in Parallel Batches

**Execution Pattern** (MANDATORY for performance):

DO NOT execute queries sequentially (one at a time). Instead, batch into groups of 5-10 and execute in parallel within single messages.

**Batching Strategy**:
1. Generate all 15-25 queries upfront (across all sub-questions)
2. Group into batches of 5-10 queries
3. Execute each batch in a single message with multiple WebSearch tool calls
4. Wait for batch to complete, then proceed to next batch

**Implementation Pattern**:
```python
# Step 1: Generate all queries first
all_queries = []
for sub_question in sub_questions:
    queries = generate_query_variations(sub_question)  # 3-5 queries per sub-Q
    all_queries.extend(queries)
# Total: 15-25 queries across all sub-questions

# Step 2: Execute in parallel batches
batch_size = 5  # Adjust 5-10 based on query complexity
for i in range(0, len(all_queries), batch_size):
    batch = all_queries[i:i+batch_size]

    # Step 3: Execute ALL queries in batch SIMULTANEOUSLY in single message
    # Example: If batch = [q1, q2, q3, q4, q5], call:
    #   WebSearch(q1)
    #   WebSearch(q2)
    #   WebSearch(q3)
    #   WebSearch(q4)
    #   WebSearch(q5)
    # ALL FIVE in the SAME message as parallel tool uses

    results = execute_parallel_batch(batch)
    process_batch_results(results)  # Collect sources immediately
```

**Why This Matters**:
- **Sequential Execution**: 25 queries × 1s each = 25s total
- **Batched Execution** (5 per batch): 5 batches × 1s = 5s total
- **Speedup: 3-5x faster** for Phase 2

**Batch Size Guidance**:
- **Simple queries** (keywords only): Use batch_size=10
- **Complex queries** (advanced operators, multiple site: filters): Use batch_size=5
- **Re-queries** in iteration 2+: Use batch_size=3-5

**Example Batched Execution**:
```
Generated 25 queries across 5 sub-questions

Batch 1 (5 queries - executed in parallel):
  WebSearch("site:salesforce.com 'API' 'integration' '2025'")
  WebSearch("'Salesforce REST API' 'rate limits' after:2024")
  WebSearch("'Salesforce Bulk API 2.0' 'best practices'")
  WebSearch("filetype:pdf 'Salesforce integration guide' 2025")
  WebSearch("'Salesforce API' 'breaking changes' after:2024")
→ Batch completes in ~1s, 5 results returned

Batch 2 (5 queries - executed in parallel):
  WebSearch("'SQL Server ETL' 'best practices' 'real-time'")
  WebSearch("site:docs.microsoft.com 'SQL Server' 'integration'")
  ...
→ Batch completes in ~1s, 5 results returned

Total: 5 batches × 1s each = ~5s (vs 25s sequential)
```

### Phase 3: Evidence Synthesis

**Objective**: Collect, rank, deduplicate, and synthesize evidence from multiple sources.

**Processing Batched Results**:

Since Phase 2 executed queries in parallel batches, you'll receive results grouped by batch. Process all results from all batches together:

1. **Flatten results**: Combine batch 1 + batch 2 + batch 3 + ... → single unified results list
2. **Deduplicate**: Remove duplicate URLs across all batches (same source may appear in multiple queries)
3. **Rank all sources**: Apply 0-10 scoring to the complete flattened list (not per-batch)
4. **Proceed with synthesis**: Use the unified, deduplicated, ranked source list for evidence synthesis

**Example**:
```python
# Collect results from all batches
all_results = []
all_results.extend(batch1_results)  # 5 results from batch 1
all_results.extend(batch2_results)  # 5 results from batch 2
all_results.extend(batch3_results)  # 5 results from batch 3
all_results.extend(batch4_results)  # 5 results from batch 4
all_results.extend(batch5_results)  # 5 results from batch 5
# Total: ~25 results (before deduplication)

# Deduplicate by URL
unique_sources = deduplicate_by_url(all_results)
# After dedup: ~15-20 unique sources (duplicates removed)

# Rank all unique sources
ranked_sources = rank_sources(unique_sources)  # Apply scoring below
```

#### 3a. Source Ranking (0-10 Scale)

Rank every source on three dimensions:

**Credibility Score** (0-10):
- **10**: Official documentation, peer-reviewed papers
- **7-9**: Established tech publications (TechCrunch, Ars Technica), reputable vendors
- **4-6**: Technical blogs, Stack Overflow, community forums
- **1-3**: Unverified sources, marketing content, personal blogs

**Freshness Score** (0-10):
- **10**: Published within last 3 months
- **7-9**: Published within last 6-12 months
- **4-6**: Published within last 1-2 years
- **1-3**: Older than 2 years

**Relevance Score** (0-10):
- **10**: Directly addresses sub-question with concrete examples
- **7-9**: Addresses sub-question with partial detail
- **4-6**: Tangentially related, requires interpretation
- **1-3**: Mentions topic briefly, minimal value

**Overall Source Quality** = (Credibility × 0.5) + (Freshness × 0.2) + (Relevance × 0.3)

#### 3b. Deduplication

- Identify duplicate findings across sources
- Prefer higher-quality sources (overall score) when duplicates exist
- Note consensus: 3+ sources agreeing = strong signal
- Flag outliers: Single source claiming something unique

#### 3c. Contradiction Resolution

When sources contradict:
1. **Check dates**: Newer source may reflect recent changes
2. **Assess authority**: Official docs override blog posts
3. **Present both views**: "Source A [1] recommends X, while Source B [2] suggests Y due to..."
4. **Explain context**: "Approach depends on scale: <100k records use X [1], >1M records use Y [2]"

### Phase 4: Citation Transparency (Clickable Format)

**Objective**: Provide numbered, **clickable** citations for every factual claim.

**🔴 CRITICAL - Use Descriptive Inline Links**:

**Inline Citation Format** (Descriptive Names - Natural Language):
```markdown
Text with claim from [OpenAI: GPT-4](https://url "GPT-4 Technical Report (OpenAI, 2023-03-14)") and [Anthropic: Claude](https://url2 "Introducing Claude (Anthropic, 2023-03-14)"). Multiple sources: [Google DeepMind: Gemini](https://url3 "Gemini Model (Google DeepMind, 2023-12-06)"), [Meta: LLaMA](https://url4 "LLaMA Paper (Meta AI, 2023-02-24)").
```

**Why descriptive names?**
- ✅ More readable inline (natural language flow)
- ✅ Self-documenting (reader knows source without checking References)
- ✅ Still clickable with tooltips
- ✅ Works in ALL markdown viewers (GitHub, VS Code, Obsidian, GitLab, terminals)

**Format**:
```markdown
[Organization: Topic](full-URL "Full Title (Publisher, YYYY-MM-DD)")
```

**Creating Descriptive Names** (from URL analysis):
1. **Extract organization**: From domain (openai.com → OpenAI, anthropic.com → Anthropic)
2. **Extract topic**: From URL path or title (gpt-4 → GPT-4, claude → Claude)
3. **Use format**: `[Org: Topic]`
4. **For duplicates**: Add descriptive suffixes - `[OpenAI: GPT-4]`, `[OpenAI: DALL-E]`, `[OpenAI: Whisper]`
5. **For generic pages**: Use page type - `[Stack Overflow: OAuth Implementation]`, `[Medium: React Patterns]`

**References Section Format** (at end of research - grouped by category):
```markdown
## References

### Official Documentation
- **OpenAI: GPT-4** (2023-03-14). "GPT-4 Technical Report". https://openai.com/research/gpt-4
- **Anthropic: Claude** (2023-03-14). "Introducing Claude". https://www.anthropic.com/claude

### Blog Posts & Articles
- **Google DeepMind: Gemini** (2023-12-06). "Gemini: A Family of Highly Capable Models". https://deepmind.google/technologies/gemini
- **Meta: LLaMA** (2023-02-24). "Introducing LLaMA". https://ai.meta.com/blog/llama

### Academic Papers
- **Attention Is All You Need** (2017-06-12). Vaswani et al. https://arxiv.org/abs/1706.03762

### Community Resources
- **Stack Overflow: OAuth Implementation** (2024-08-15). https://stackoverflow.com/questions/12345
```

**Why grouped References section?**
- Provides organized list view by source type
- Easy to scan authoritative vs. community sources
- Shows evidence diversity at a glance
- Copy-paste for further research

**Category Guidance**:
- **Official Documentation**: Vendor docs, API references, official guides
- **Blog Posts & Articles**: Company engineering blogs, Medium, Dev.to, technical articles
- **Academic Papers**: arXiv, research papers, conference proceedings, whitepapers
- **Community Resources**: Stack Overflow, GitHub discussions, Reddit, forums

**Title Format in Quotes**:
- `"Full Title (Publisher, YYYY-MM-DD)"`
- Keep title concise but descriptive (< 80 chars if possible)
- Always include publisher and date for credibility

**Hover Behavior**:
Most markdown viewers (GitHub, VS Code, Obsidian, GitLab) show the title as a tooltip when hovering over the citation.

**Click Behavior**:
Clicking the descriptive name opens the URL directly in browser.

**Example Inline Usage**:
```markdown
Salesforce provides three primary API types according to [Salesforce: API Docs](https://developer.salesforce.com/docs/apis "Salesforce API Documentation (Salesforce, 2025-01-15)"): REST API for standard operations, [Salesforce: Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/ "Bulk API 2.0 Guide (Salesforce, 2024-11-20)") for large data volumes (>10k records), and [Salesforce: Streaming API](https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/ "Streaming API Guide (Salesforce, 2024-10-05)") for real-time updates. Recent 2025 updates introduced enhanced rate limiting (100k requests/24hrs for Enterprise) and improved error handling as noted in [Salesforce Blog: API Updates](https://developer.salesforce.com/blogs/2025/01/api-updates "API Error Handling Improvements (Salesforce Blog, 2025-01-10)").

## References

### Official Documentation
- **Salesforce: API Docs** (2025-01-15). "Salesforce API Documentation". https://developer.salesforce.com/docs/apis
- **Salesforce: Bulk API 2.0** (2024-11-20). "Bulk API 2.0 Developer Guide". https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/
- **Salesforce: Streaming API** (2024-10-05). "Streaming API Developer Guide". https://developer.salesforce.com/docs/atlas.en-us.api_streaming.meta/api_streaming/

### Blog Posts & Articles
- **Salesforce Blog: API Updates** (2025-01-10). "API Error Handling Improvements". https://developer.salesforce.com/blogs/2025/01/api-updates
```

**Compatibility**: Works in GitHub, VS Code (preview), Obsidian, GitLab, all markdown viewers

### Phase 5: Structured Output (Balanced - Target 250-350 Lines)

**Objective**: Deliver comprehensive, implementation-ready findings with narrative depth.

**Design Principles**:
- ✅ Balanced depth (250-350 lines) - not too verbose, not over-condensed
- ✅ Repository-agnostic (no repo-specific details)
- ✅ Implementation-ready (Executive Summary + Recommendations guide next steps)
- ✅ Sources with full URLs (non-negotiable)
- ✅ Universal (works for any question: technical, business, educational, strategic)

**Output Template**:
```markdown
# Deep Research: {Question}

## Executive Summary

{2-3 paragraph synthesis covering:
- What was researched and why it matters
- Key findings with citations [Org: Topic]
- Strategic recommendation with rationale}

Example length: ~150-200 words total across 2-3 paragraphs.

## Research Overview

- **Sub-Questions Analyzed**: {count}
- **Queries Executed**: {count} queries
- **Sources**: {count} total ({authoritative_count} authoritative / {auth_pct}%, {recent_count} recent / {recent_pct}%)
- **Iterations**: {count}

## Findings

### 1. {Sub-Question 1}

{Opening paragraph: What this sub-question addresses and why it's important}

{2-4 paragraphs of synthesized narrative with inline citations [1][2][3]. Each paragraph covers a specific aspect or theme. Include:
- Core concepts and definitions with citations
- How different sources approach the topic
- Practical implications and examples
- Performance characteristics or trade-offs where relevant}

**Key Insights**:
- {Insight 1: Specific, actionable statement} - {Why it matters and implications} [Org: Topic], [Org: Topic]
- {Insight 2: Specific, actionable statement} - {Why it matters and implications} [Org: Topic]
- {Insight 3: Specific, actionable statement} - {Why it matters and implications} [Org: Topic]

{Optional: **Common Patterns** or **Best Practices** subsection if relevant with 2-3 bullet points}

### 2. {Sub-Question 2}

{Repeat the same structure: Opening paragraph + 2-4 narrative paragraphs + 3-5 Key Insights}

{...continue for all sub-questions...}

## Synthesis

{2-3 paragraphs integrating findings across sub-questions. Show how the pieces fit together and what the big picture reveals.}

**Consensus** (3+ sources agree):
- {Consensus point 1 with source count} [Org: Topic], [Org: Topic], [Org: Topic]
- {Consensus point 2 with source count} [Org: Topic], [Org: Topic], [Org: Topic], [Org: Topic]

**Contradictions** *(if present)*:
- **{Topic}**: {Source A perspective [Org: Topic]} vs {Source B perspective [Org: Topic]}. {Resolution or context explaining difference}

**Research Gaps** *(if any)*:
- {Gap 1}: {What wasn't found and why it matters}

## Recommendations

### Critical (Do First)
1. **{Action}** - {Detailed rationale explaining why this is critical, what happens if not done, and expected impact} [Org: Topic], [Org: Topic]

2. **{Action}** - {Detailed rationale} [Org: Topic]

3. **{Action}** - {Detailed rationale} [Org: Topic]

### Important (Do Next)
4. **{Action}** - {Rationale with evidence and expected benefit} [Org: Topic]

5. **{Action}** - {Rationale with evidence} [Org: Topic]

6. **{Action}** - {Rationale with evidence} [Org: Topic]

### Optional (Consider)
7. **{Action}** - {Rationale and when/why you might skip this} [Org: Topic]

8. **{Action}** - {Rationale} [Org: Topic]

## References

### Official Documentation
- **{Org: Topic}** ({YYYY-MM-DD}). "{Full Title}". {Full URL}
- **{Org: Topic}** ({YYYY-MM-DD}). "{Full Title}". {Full URL}

### Blog Posts & Articles
- **{Org: Topic}** ({YYYY-MM-DD}). "{Full Title}". {Full URL}

### Academic Papers
- **{Paper Title}** ({YYYY-MM-DD}). {Authors}. {Full URL}

### Community Resources
- **{Platform: Topic}** ({YYYY-MM-DD}). {Full URL}
```

**Length Guidance**:
- Executive Summary: 150-200 words
- Each Finding section: 300-400 words (opening + narrative + insights)
- Synthesis: 200-250 words
- Recommendations: 3 Critical + 3-4 Important + 2-3 Optional with detailed rationale
- **Total Target**: 250-350 lines

**Requirements**:
- Executive Summary: Scannable in <30 seconds, tells complete story
- Findings: Each section has 2-4 narrative paragraphs PLUS 3-5 Key Insights bullets
- Narrative paragraphs explain concepts, show evidence, connect ideas
- Key Insights are distilled actionable takeaways
- Synthesis: Shows big picture, notes consensus (with source counts), explores contradictions
- Recommendations: Detailed rationale for each (not just bullet point + citation)
- Sources: MUST include full URLs with title, author/org, date

**What NOT to Include** (token waste):
- ❌ Evidence tables with numeric scores (0-10 ratings)
- ❌ Repository-specific details ("Main Thread Log", "CARE quality score")
- ❌ Separate Pros/Cons sections (integrate into Recommendations)
- ❌ Verbose iteration logs or detailed methodology steps

### Phase 6: Iterative Refinement

**Objective**: Validate completeness and re-query gaps (max 5 iterations).

**Completeness Validation Checklist**:
- [ ] All sub-questions have findings with 3+ source citations?
- [ ] Contradictions identified and explained? (If none, explicitly state "No contradictions found")
- [ ] Recent sources included (within 6-12 months)?
- [ ] Authoritative sources prioritized (official docs)?
- [ ] Practical recommendations provided (3 Critical + 3-4 Important + 2-3 Optional)?
- [ ] Research gaps explicitly noted?

**Automated Gap Detection Logic**:

```python
gaps = []
completeness_score = 100

# Check citation coverage
for sub_q in sub_questions:
    citation_count = count_citations(sub_q)
    if citation_count < 3:
        gaps.append(f"Sub-Q{i}: Only {citation_count} citations (need 3+)")
        completeness_score -= 10

# Check for contradictions exploration
if contradictions_section_empty():
    gaps.append("No contradictions explored - search for '{topic} criticisms' OR '{topic} limitations'")
    completeness_score -= 10

# Check authoritative source coverage
auth_sources = count_authoritative_sources()  # credibility >= 8
if auth_sources < total_sources * 0.5:
    gaps.append(f"Only {auth_sources} authoritative sources ({round(auth_sources/total_sources*100)}%) - need 50%+")
    completeness_score -= 10

# Check recency
recent_sources = count_recent_sources()  # within 6 months
if recent_sources < total_sources * 0.3:
    gaps.append(f"Only {recent_sources} recent sources ({round(recent_sources/total_sources*100)}%) - need 30%+")
    completeness_score -= 5

# Check recommendation depth
if critical_recommendations < 3:
    gaps.append(f"Only {critical_recommendations} Critical recommendations (need 3)")
    completeness_score -= 10

# Check for research gaps section
if research_gaps_section_missing():
    gaps.append("Research Gaps section missing - document what wasn't found")
    completeness_score -= 5

return completeness_score, gaps
```

**Re-Query Decision Logic**:
```python
iteration_count = 1
completeness_score, gaps = validate_completeness()

# 🔴 MANDATORY: Always perform minimum 2 iterations
# Even if iteration 1 achieves 85%+, iteration 2 improves depth
if iteration_count < 2 or (completeness_score < 85% and iteration_count <= 5):
    # Generate targeted re-queries for each gap
    requery_list = []

    for gap in gaps:
        if "citations" in gap:
            # Need more sources for specific sub-question
            requery_list.append(f"'{sub_question_topic}' 'detailed guide' OR 'comprehensive overview'")

        elif "contradictions" in gap:
            # Need to explore downsides/criticisms
            requery_list.append(f"'{topic}' 'criticism' OR 'limitations' OR 'downsides'")
            requery_list.append(f"'{topic}' 'vs' 'alternative' 'when not to use'")

        elif "authoritative" in gap:
            # Need more official sources
            requery_list.append(f"site:docs.{vendor}.com '{topic}' 'official'")
            requery_list.append(f"site:{vendor}.com '{topic}' 'documentation'")

        elif "recent" in gap:
            # Need more recent sources
            requery_list.append(f"'{topic}' 'updates' OR 'changes' after:2024")
            requery_list.append(f"'{topic}' '2025' OR '2024' 'latest'")

    # Execute re-queries in parallel batch (1-5 queries)
    # Use smaller batch size for re-queries since they're targeted
    requery_batch = requery_list[:5]  # Up to 5 re-queries

    # Execute ALL re-queries in batch SIMULTANEOUSLY in single message
    # Example: If requery_batch = [rq1, rq2, rq3], call:
    #   WebSearch(rq1)
    #   WebSearch(rq2)
    #   WebSearch(rq3)
    # ALL THREE in the SAME message as parallel tool uses
    execute_parallel_batch(requery_batch)
    iteration_count += 1

    # Update findings incrementally
    append_iteration_findings()
    completeness_score, gaps = validate_completeness()

else:
    # Either complete (≥85%) or max iterations reached
    if completeness_score < 85%:
        note_limitations_in_research_gaps_section(gaps)
    finalize_output()
```

**Iteration Update Pattern**:
When adding findings from later iterations, append to existing sections:

```markdown
### 1. {Sub-Question}

{Original findings from iteration 1}

**Iteration 2 Additions**:
{New findings from re-queries, with citations [Org: Topic], [Org: Topic], [Org: Topic]}

**Key Insights**:
- {Original insight 1} [Org: Topic]
- {Original insight 2} [Org: Topic]
- {NEW insight from iteration 2} [Org: Topic], [Org: Topic]
```

**When to Stop Iterating**:
- 🔴 **MANDATORY**: Minimum 2 iterations (iteration_count >= 2)
- ✅ Completeness score ≥ 85%
- ✅ All sub-questions have 3+ citations
- ✅ Contradictions section populated (or explicitly noted as "None identified")
- ✅ 50%+ authoritative sources, 30%+ recent sources
- ✅ 3+ Critical recommendations
- ⏱️ OR iteration_count > 5 (max iterations reached)

**Stop only if**: (iteration_count >= 2 AND completeness >= 85%) OR iteration_count > 5

**If Max Iterations Reached Without 85%**:
Add explicit Research Gaps section:
```markdown
## Research Gaps

Due to iteration limit, the following gaps remain:
- {Gap 1}: {What's missing and why it matters}
- {Gap 2}: {What's missing and suggested follow-up approach}
```

## Examples

### Example 1: Architecture Decision Research

**Scenario**: User asks "What's the best architecture for integrating Salesforce with SQL Server in 2025?"

**Process**:

**Phase 1 - Decomposition**:
```
Sub-Q1: Salesforce integration capabilities (2025)?
Sub-Q2: SQL Server integration patterns?
Sub-Q3: Middleware options?
Sub-Q4: Security considerations?
Sub-Q5: Scalability factors?
```

**Phase 2 - Multi-Query Generation and Batched Execution**:
```
Generated 25 queries across 5 sub-questions

Batch 1 (5 queries - executed in parallel):
  WebSearch("site:salesforce.com 'API' 'integration' '2025'")
  WebSearch("'Salesforce REST API' 'rate limits' after:2024")
  WebSearch("'Salesforce Bulk API 2.0' 'best practices'")
  WebSearch("filetype:pdf 'Salesforce integration guide' 2025")
  WebSearch("'Salesforce API' 'breaking changes' after:2024")
→ Batch completes in ~1s, 5 results returned

Batch 2 (5 queries - executed in parallel):
  WebSearch("'SQL Server ETL' 'best practices' 'real-time'")
  WebSearch("site:docs.microsoft.com 'SQL Server' 'integration'")
  WebSearch("'SQL Server Always On' 'high availability'")
  WebSearch("'SQL Server CDC' 'change data capture'")
  WebSearch("'SQL Server linked servers' 'performance'")
→ Batch completes in ~1s, 5 results returned

Batch 3-5 (15 more queries across 3 batches):
  ... (middleware, security, scalability queries)
→ Each batch completes in ~1s

Execution Time:
- 5 batches × ~1s each = ~5s total
- Sequential would be: 25 queries × 1s = 25s
- Speedup: 5x faster
```

**Phase 3 - Evidence**:
```
18 sources identified
12 ranked as authoritative (credibility ≥ 8)
3 contradictions (real-time vs batch approaches)
```

**Phase 4 - Citations**:
```
[1] Salesforce API Guide (Cred: 10, Fresh: 10, Rel: 10, Overall: 10.0)
[2] MuleSoft Patterns (Cred: 9, Fresh: 8, Rel: 9, Overall: 8.9)
```

**Phase 5 - Output**:
```
Executive Summary: 2 paragraphs
Findings: 5 sub-sections with 28 citations
Recommendations: 3 critical, 4 important, 2 enhancements
```

**Phase 6 - Refinement**:
```
Iteration 1: Identified gap in disaster recovery
Iteration 2: Re-queried "Salesforce SQL backup strategies"
Iteration 3: Completeness 92% → finalized
```

**Output**: Deep Mode Context File with executive summary, 5 sub-question analyses, evidence table, synthesis, pros/cons, 28 citations

### Example 2: Technology Selection Research

**Scenario**: "Should we use microservices or monolith architecture for our e-commerce platform?"

**Process**:

**Decomposition**:
```
1. Scalability characteristics for e-commerce?
2. Team size and DevOps implications?
3. Transaction patterns differences?
4. Deployment complexity trade-offs?
5. Real-world e-commerce case studies?
```

**Multi-Query** (sample):
```
"microservices e-commerce" "scalability" after:2024
"monolith vs microservices" "team size" "best practices"
site:aws.amazon.com "e-commerce architecture" "patterns"
```

**Evidence Synthesis**:
```
15 sources (10 authoritative)
Consensus: Team size <20 → monolith, >50 → microservices
Contradiction: Database approach (shared vs distributed)
```

**Output**: Structured analysis with pros/cons for both approaches, team size recommendations, migration considerations, case studies with citations

## Best Practices

- **Start Broad, Then Narrow**: Begin with general queries, then drill into specifics based on initial findings
- **Verify Across Sources**: Never rely on single source - cross-reference critical claims with 3+ sources
- **Prioritize Recency**: For technology topics, prefer sources <1 year old
- **Official Docs First**: Start with official documentation, then supplement with community insights
- **Track Contradictions**: Don't hide conflicting information - present it with context
- **Iterate When Needed**: Don't force completeness - if gaps remain after 5 iterations, note limitations
- **Citation Discipline**: Every factual claim needs a numbered citation

## Common Patterns

### Pattern 1: Architecture Decision Research
- Decompose into: Current state, Requirements, Options, Trade-offs, Case studies
- Multi-query: Official docs, vendor comparisons, real-world implementations
- Synthesize: Pros/cons matrix with cited evidence

### Pattern 2: Technology Migration Research
- Decompose into: Current tech assessment, Target tech capabilities, Migration path, Risk analysis, Timeline estimation
- Multi-query: Migration guides, success/failure stories, tool comparisons
- Synthesize: Step-by-step migration plan with risk mitigation

### Pattern 3: Best Practices Research
- Decompose into: Industry standards, Common patterns, Anti-patterns, Tooling, Case studies
- Multi-query: Official guidelines, expert blogs, conference talks, GitHub repos
- Synthesize: Consolidated best practices list with rationale

## Troubleshooting

**Issue 1: Too Many Sources, Can't Synthesize**
- Focus on top-ranked sources (overall score ≥ 7.0)
- Group findings by theme, not by source
- Identify consensus first, then note outliers

**Issue 2: Contradictory Information**
- Check publication dates (newer may reflect recent changes)
- Assess source authority (official > blog)
- Look for context (contradictions may be scenario-dependent)
- Present both views with citations

**Issue 3: Insufficient Recent Sources**
- Broaden date range to last 2 years
- Check for technology name changes (old vs new terminology)
- Combine recent + authoritative older sources
- Note in output: "Based on 2023 sources; 2025 updates pending verification"

**Issue 4: Completeness Score Below 85%**
- Identify specific gaps (which sub-questions lack depth?)
- Generate 1-3 targeted re-queries
- If still below 85% after 3 iterations, note limitations explicitly

## Integration Points

- **WebSearch Tool**: Execute all search queries through WebSearch
- **Context7 MCP**: Supplement with official framework/library docs when applicable
- **Evidence Table**: Track all sources in structured format for quality assessment
- **Context Files**: Persist findings to `.agent/Session-{name}/context/research-web-analyst.md`

## Key Terminology

- **Sub-Question**: Focused component of primary research question
- **Query Variation**: Different phrasing/angle of same information need
- **Source Quality Score**: Composite metric (credibility + freshness + relevance)
- **Consensus View**: Finding supported by 3+ independent authoritative sources
- **Contradiction**: Conflicting claims from multiple sources requiring context
- **Completeness Score**: Percentage of research objectives met with adequate evidence
- **Iteration**: Research cycle (query → collect → synthesize → validate)

## Additional Resources

- Advanced Google Search Operators: https://ahrefs.com/blog/google-advanced-search-operators/
- Source Evaluation Criteria: https://guides.library.cornell.edu/evaluate
- Citation Best Practices: https://apastyle.apa.org/
- Research Synthesis Methods: https://methods.sagepub.com/book/systematic-approaches-to-a-successful-literature-review
