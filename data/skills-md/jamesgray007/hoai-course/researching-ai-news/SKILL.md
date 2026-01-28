---
name: researching-ai-news
description: Research and compile the latest AI news from across the industry. Use this skill when asked to find AI news, get AI updates, research what's happening in AI, check for AI announcements, or gather intelligence on AI companies. Triggers include requests for "AI news", "latest AI developments", "what's new in AI", "AI industry updates", or news about specific AI companies (OpenAI, Anthropic, Google, Microsoft, Meta, Amazon, Nvidia, xAI, Mistral, Cohere, Apple, Salesforce).
---

# Researching AI News

Research and compile AI news from across the industry, covering major companies and emerging trends.

## Companies to Track

**Frontier Labs:**
- OpenAI
- Anthropic
- Google DeepMind / Google AI
- Meta AI / FAIR
- xAI

**Tech Giants:**
- Microsoft AI
- Amazon AWS AI / Bedrock
- Nvidia
- Apple (Apple Intelligence)
- Salesforce (Einstein AI)
- IBM (watsonx)

**AI Startups & Specialists:**
- Mistral AI
- Cohere
- Stability AI
- Runway
- Hugging Face
- Perplexity AI
- Other emerging labs

## Topics to Cover

1. **Product launches & updates** - New models, features, API changes
2. **Research breakthroughs** - Papers, benchmarks, capabilities
3. **Regulations & policy** - Government actions, safety initiatives, legal developments
4. **Industry trends** - Funding, partnerships, acquisitions, market moves
5. **Enterprise AI adoption** - Real-world implementations, case studies, ROI reports

## Research Workflow

### Step 1: Run Perplexity Searches

Use the Perplexity MCP tools for comprehensive, citation-rich results:

**Primary tool: `mcp__perplexity__perplexity_search`**
- Best for quick, targeted queries with ranked results
- Returns titles, URLs, snippets, and metadata
- Use `max_results: 10` for comprehensive coverage

**Deep research: `mcp__perplexity__perplexity_research`**
- Use for complex topics requiring synthesis across sources
- Returns comprehensive analysis with citations
- Best for industry trends and regulatory developments

### Search Queries

Run these searches in parallel using `mcp__perplexity__perplexity_search`:

```
Company news (run in parallel):
- "OpenAI announcement news December 2024"
- "Anthropic Claude news December 2024"
- "Google Gemini AI news December 2024"
- "Microsoft AI Copilot news December 2024"
- "Meta Llama AI news December 2024"
- "Nvidia AI news December 2024"
- "xAI Grok news December 2024"
- "Amazon AWS Bedrock AI news December 2024"
- "Mistral AI news December 2024"
- "Apple Intelligence news December 2024"

Industry topics (run in parallel):
- "AI regulation policy news December 2024"
- "AI research breakthrough news December 2024"
- "AI startup funding investment news December 2024"
- "enterprise AI deployment case study 2024"
```

For deeper analysis, use `mcp__perplexity__perplexity_research` with:
```json
{
  "messages": [
    {"role": "user", "content": "What are the most significant AI industry developments in the last 48 hours? Include product launches, research breakthroughs, regulatory changes, and major funding announcements. Focus on verified announcements from official sources."}
  ]
}
```

### Step 2: Filter for Recency

Include stories from the last 24-48 hours. Use 24 hours for daily briefings; extend to 48 hours on Mondays or slow news days to capture weekend developments.

### Step 3: Deduplicate Results

Before compiling output:
- Identify stories appearing across multiple searches
- Consolidate duplicate stories into a single entry
- Use the most authoritative source (official blog > news outlet > aggregator)
- Note if multiple sources are covering the same story (indicates higher significance)

### Step 4: Verify Major Claims

For significant announcements:
- Cross-reference against official company blogs, press releases, or verified social accounts
- Check if the story has been confirmed by multiple reputable sources
- Flag unverified or single-source stories as "Developing" or "Unconfirmed"

### Step 5: Compile Results

Format output as bullet points with source links:

```markdown
## AI News - [Date]

### Company Updates
- **[Company]**: [Brief summary of news] ([Source](url))
- **[Company]**: [Brief summary of news] ([Source](url))

### Product Launches
- [Product/feature description] ([Source](url))

### Research & Breakthroughs
- [Research summary] ([Source](url))

### Regulation & Policy
- [Policy development] ([Source](url))

### Enterprise Adoption
- [Company/industry implementation story] ([Source](url))

### Industry Trends
- [Trend/funding/partnership] ([Source](url))
```

### Step 6: Prioritize

Order stories by significance:
1. Major model releases or capabilities
2. Significant policy/regulatory changes
3. Large funding rounds or acquisitions
4. Research breakthroughs
5. Enterprise adoption stories with measurable outcomes
6. Product updates and features

## Output Guidelines

- Keep summaries to 1-2 sentences per story
- Always include source links
- Group related stories together
- Note if a category has no news ("No significant updates")
- Flag breaking/developing stories with "[DEVELOPING]" prefix
- Flag unverified stories with "[UNCONFIRMED]" prefix
- Prefer official sources over secondary coverage

## Perplexity MCP Tools Reference

| Tool | Use Case |
|------|----------|
| `mcp__perplexity__perplexity_search` | Quick searches, specific company news, targeted queries |
| `mcp__perplexity__perplexity_research` | Deep analysis, trend synthesis, comprehensive reports |
| `mcp__perplexity__perplexity_ask` | Follow-up questions, clarifications, verification |

### Search Tips

- Use company + product names for precision ("Claude 3.5", "GPT-4o", "Gemini 2.0")
- Include current month/year in queries for better recency filtering
- Run company searches in parallel for efficiency
- Use `perplexity_research` for synthesizing trends across multiple sources
- Perplexity automatically includes citations - preserve these in output
- For verification, use `perplexity_ask` to confirm details from official sources
