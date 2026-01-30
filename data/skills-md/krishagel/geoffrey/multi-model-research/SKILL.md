---
name: multi-model-research
description: Orchestrate multiple frontier LLMs (Claude, GPT-5.1, Gemini 3.0 Pro, Perplexity Sonar, Grok 4.1) for comprehensive research using LLM Council pattern with peer review and synthesis
triggers:
  - "deep dive"
  - "research council"
  - "multi-model research"
  - "comprehensive research"
  - "council research"
allowed-tools: Bash, Read, mcp__obsidian-vault__create_vault_file
version: 0.1.0
---

# Multi-Model Research Agent

Implements Karpathy's LLM Council pattern for superior research through parallel queries, peer review, and chairman synthesis.

## Architecture

**Geoffrey/Claude (Native Council Member):**
- Routes simple vs complex queries
- Calls external API orchestrator (`research.py`)
- Provides my own research response
- Conducts peer review phase
- Requests GPT-5.1 synthesis (chairman)
- Saves final report to Obsidian

**Python External API Orchestrator:**
- Fetches responses from GPT-5.1, Gemini 3.0 Pro, Perplexity Sonar, Grok 4.1
- Returns JSON with all external responses
- I handle all orchestration and synthesis

## When to Use This Skill

Use multi-model research when:
- **Complex analysis needed** - Multiple perspectives valuable
- **Factual verification critical** - Cross-model validation
- **Comprehensive coverage required** - No single model sufficient
- **Current information essential** - Perplexity provides web grounding
- **Contested topics** - Benefit from diverse model perspectives

## Simple vs Council Mode

**Simple Mode** (Perplexity only):
- Factual lookups
- Current events
- Quick research with citations
- Completes in <15 seconds

**Council Mode** (Full council):
- Comparative analysis
- Deep research
- Multiple perspectives needed
- Strategic questions
- Completes in <90 seconds

## Workflow

### Simple Query

```
User: "What are the latest developments in quantum computing?"
     ↓
I decide: Simple query (factual, current)
     ↓
I call: uv run scripts/research.py --query "..." --models perplexity
     ↓
I read: JSON response from Perplexity
     ↓
I format: Markdown report with citations
     ↓
I save: To Obsidian Geoffrey/Research folder
     ↓
I return: Summary to user with Obsidian link
```

### Council Query

```
User: "Compare the AI strategies of OpenAI, Anthropic, and Google"
     ↓
I decide: Council query (comparative, complex)
     ↓
I call: uv run scripts/research.py --query "..." --models gpt,gemini,perplexity,grok
     ↓
I read: JSON with all external responses
     ↓
I provide: My own (Claude) research response
     ↓
I conduct: Peer review (each model ranks others)
     ↓
I request: GPT-5.1 chairman synthesis
     ↓
I format: Comprehensive markdown report
     ↓
I save: To Obsidian Geoffrey/Research folder
     ↓
I return: Summary with Obsidian link
```

## Output Format

All research reports saved to Obsidian include:

- **Executive Summary** (2-3 paragraphs)
- **Key Findings** (organized by theme, inline citations)
- **Confidence Assessment** (what's certain vs debated)
- **References Section** (all sources with URLs and dates)

Citations use numeric format: [1], [2], etc.

## Technical Details

**Python Script:**
```bash
cd skills/multi-model-research
uv run scripts/research.py --query "Your question" --models perplexity --output /tmp/responses.json
```

**Config:**
- `config.yaml` - Model settings, routing rules
- `prompts/system_prompts.yaml` - Per-model system prompts
- `prompts/peer_review.md` - Peer review template
- `prompts/chairman_synthesis.md` - GPT-5.1 synthesis template

**Dependencies:**
- httpx (async HTTP client)
- pyyaml (config parsing)
- python-dotenv (env vars)
- python-frontmatter (Obsidian frontmatter)

**API Keys Required:**
- OPENAI_API_KEY (GPT-5.1)
- GEMINI_API_KEY (Gemini 3.0 Pro)
- PERPLEXITY_API_KEY (Sonar Pro)
- XAI_API_KEY (Grok 4.1)

All keys configured in `~/.env` file.

## Examples

**Simple Research:**
```
User: "What is RAG in AI?"

I route to: Simple mode (Perplexity)
Output: Concise explanation with current examples and citations
Time: ~10 seconds
```

**Council Research:**
```
User: "Compare serverless vs containers for production ML workloads"

I route to: Council mode (all 4 external + me)
Process:
  1. GPT-5.1: Provides comprehensive technical comparison
  2. Gemini 3.0: Analyzes cost and performance trade-offs
  3. Perplexity: Current industry trends and case studies
  4. Grok 4.1: Developer sentiment from X/Twitter
  5. Claude (me): Synthesize with nuanced analysis
  6. Peer review: Each model ranks others
  7. GPT-5.1 (chairman): Final synthesis

Output: Multi-perspective analysis with citations
Time: ~60 seconds
```

## Limitations

- **Cost**: Council mode uses 4-5 API calls per query
- **Latency**: Council mode takes 60-90 seconds
- **API Limits**: Rate limits may throttle parallel requests
- **Citation Quality**: Non-Perplexity models require URL extraction

## Future Enhancements

- Streaming responses during deliberation
- Cost tracking and budget limits
- Query history and versioning
- Custom model weights based on topic
- Integration with Geoffrey's knowledge base

---

*This skill implements Karpathy's LLM Council pattern released November 22, 2025.*
