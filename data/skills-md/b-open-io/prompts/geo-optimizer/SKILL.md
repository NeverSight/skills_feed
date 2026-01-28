---
name: geo-optimizer
version: 1.0.0
description: This skill should be used when the user asks to "audit for AI visibility", "optimize for ChatGPT", "check GEO readiness", "analyze hedge density", "generate agentfacts", "check if my site works with AI search", "test LLM crawlability", "check discovery gap", or mentions Generative Engine Optimization, AI crawlers, Perplexity discoverability, or NANDA protocol.
---

# GEO Optimizer

Generative Engine Optimization (GEO) for AI search visibility.

## What is GEO?

GEO is NOT traditional SEO. AI search engines (ChatGPT, Perplexity, Claude, Gemini) work fundamentally differently:

1. **They fetch raw HTML** - Many don't render JavaScript
2. **They have size limits** - Crawlers abandon pages >1MB HTML
3. **They evaluate confidence** - Hedged language ("maybe", "possibly") ranks 3x lower than confident assertions
4. **They need machine-readable metadata** - AgentFacts/NANDA protocol for AI agent discovery

## Quick Audit Workflow

### 1. Technical Visibility Check
```bash
# Run full GEO audit
python3 ${CLAUDE_SKILL_DIR}/scripts/audit-geo.py https://example.com

# Check HTML size and JS dependency
curl -sI https://example.com | grep -i content-length
```

### 2. Content Authority Analysis
```bash
# Check hedge density of your content
python3 ${CLAUDE_SKILL_DIR}/scripts/check-hedge-density.py --url https://example.com/blog/post

# Or analyze text directly
python3 ${CLAUDE_SKILL_DIR}/scripts/check-hedge-density.py --text "Your content here"
```

### 3. Agent Infrastructure Setup
```bash
# Generate AgentFacts schema for your domain
python3 ${CLAUDE_SKILL_DIR}/scripts/generate-agentfacts.py \
  --domain example.com \
  --agent-name "Example Service" \
  --capabilities text,image \
  --output /.well-known/agent-facts
```

## Core Metrics

### Hedge Density Score
Measures uncertainty language in content. Target: <0.2%

**Hedge words to avoid:**
- maybe, possibly, perhaps, might, could be
- however, although, it seems, arguably
- some believe, it appears, potentially

**Why it matters:** Research shows confident citations rank 3x higher in AI responses. Every hedge word signals uncertainty to LLMs.

See: `references/hedge-density.md`

### HTML Size Budget
Maximum: 1MB raw HTML. Above this threshold:
- 18% of pages abandoned by crawlers
- Content truncation risks
- Slower indexing

Check with: `curl -sI URL | grep content-length`

See: `references/technical-visibility.md`

### JS Dependency Risk
AI crawlers vary in JavaScript rendering:
- **Rendering crawlers:** GPTBot, PerplexityBot (sometimes)
- **Non-rendering:** ClaudeBot, many others

If your content requires JS to display, you're invisible to ~40% of AI crawlers.

### Discovery Gap
Startups face a "recency wall" - 30:1 visibility disadvantage vs established domains:

| Site Age | Visibility | Strategy |
|----------|------------|----------|
| <2 years | ~3.3% | Web-augmented: Reddit, referring domains |
| 2+ years | ~99% | GEO content: entity density, hedge reduction |

See: `references/discovery-strategies.md`

## AgentFacts Setup

The NANDA protocol provides machine-readable metadata for AI agent discovery. Place at `/.well-known/agent-facts`:

```json
{
  "@context": "https://nanda.dev/ns/agent-facts/v1",
  "id": "nanda:example.com",
  "agent_name": "urn:agent:example:com",
  "endpoints": {
    "static": ["https://api.example.com/v1/agent"]
  },
  "capabilities": {
    "modalities": ["text"],
    "authentication": {
      "methods": ["oauth2", "jwt"]
    }
  },
  "trust": {
    "certification": "self-attested",
    "human_oversight": "true"
  }
}
```

See: `references/agentfacts-schema.md`

## Audit Report Sections

A complete GEO audit covers:

1. **Technical Visibility**
   - HTML payload size (target: <1MB)
   - JS dependency assessment
   - Crawler accessibility

2. **Content Authority**
   - Hedge density score (target: <0.2%)
   - Confidence assessment
   - Entity density

3. **Discovery Strategy**
   - Site age analysis
   - Recency wall detection
   - Recommended approach

4. **Agent Infrastructure**
   - AgentFacts presence
   - Schema validation
   - NANDA compliance

## Scripts

| Script | Purpose |
|--------|---------|
| `audit-geo.py` | Full GEO audit for a URL |
| `check-hedge-density.py` | Analyze content confidence |
| `generate-agentfacts.py` | Create NANDA-compliant schema |

## Reference Documentation

| File | Contents |
|------|----------|
| `hedge-density.md` | Confidence scoring methodology |
| `agentfacts-schema.md` | NANDA protocol specification |
| `technical-visibility.md` | Crawler behavior & limits |
| `discovery-strategies.md` | Startup vs incumbent approaches |

## Example Commands

```bash
# Full audit with report
python3 ${CLAUDE_SKILL_DIR}/scripts/audit-geo.py https://mysite.com --output report.md

# Quick hedge check
python3 ${CLAUDE_SKILL_DIR}/scripts/check-hedge-density.py --url https://mysite.com/about

# Generate AgentFacts for SaaS
python3 ${CLAUDE_SKILL_DIR}/scripts/generate-agentfacts.py \
  --domain myapp.com \
  --agent-name "MyApp AI" \
  --capabilities text \
  --auth oauth2,apikey
```

## Key Takeaways

1. **GEO != SEO** - Different crawlers, different rules
2. **Confidence wins** - Hedge density <0.2% is the target
3. **Size matters** - Stay under 1MB HTML
4. **JS is risky** - Content must work without rendering
5. **Age affects strategy** - Startups need web-augmented signals
6. **AgentFacts is future-proofing** - Implement NANDA now
