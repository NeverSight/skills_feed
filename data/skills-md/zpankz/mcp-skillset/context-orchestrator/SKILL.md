---
name: context-orchestrator
description: |
  Orchestrates context retrieval from three CLI sources: limitless (personal
  life transcripts), research (online documentation/facts), pieces (local code/LTM).
  Use when external context is needed beyond the current codebase. Triggers on
  /context, /limitless, /research, /pieces, or balanced detection on complex prompts
  involving personal memory, technical documentation, or development history.
triggers: [context, lifelog, research, ltm, recall, lookup, pieces, limitless, pendant, documentation, fact-check]
---

# Context Orchestrator

A unified context extraction system that intelligently routes queries to three specialized CLI tools based on intent classification.

## Quick Start

**Commands** (use directly):
- `/context [query]` - All sources in parallel (personal + research + code)
- `/limitless [query]` - Personal memory (lifelogs, meetings, conversations)
- `/research [query]` - Online documentation (facts, APIs, guides)
- `/pieces [query]` - Local code context (snippets, LTM, history)

**Auto-Detection**: The hook detects context-relevant prompts and suggests CLI commands.

**Maintenance**: See `README.md` for configuration, debugging, and upgrade instructions.

## Context Sources

| Source | CLI | Data Type | Best For |
|--------|-----|-----------|----------|
| **Personal** | `limitless` | Life transcripts, meetings, conversations | "What did I discuss...", "Yesterday's meeting..." |
| **Online** | `research` | Documentation, facts, academic papers | "How to implement...", "Verify that..." |
| **Local** | `pieces` | Code snippets, work history, LTM | "My previous implementation...", "Code I wrote..." |

## Slash Commands

| Command | Description | Mode |
|---------|-------------|------|
| `/context [query]` | Multi-source extraction | Parallel (all relevant) |
| `/limitless [query]` | Personal life context | Single (limitless) |
| `/research [query]` | Online documentation | Single (research) |
| `/pieces [query]` | Local code context | Single (pieces) |

## Intent Classification

### Domain Patterns

```yaml
personal_context:
  patterns:
    - "what did (I|we) (discuss|talk|say|mention)"
    - "meeting|conversation|daily|yesterday|last week"
    - "lifelog|pendant|recording"
    - "(told me|mentioned|said) about"
  primary_cli: limitless
  fallback: pieces (if code-related)

online_research:
  patterns:
    - "documentation|docs for|how to"
    - "fact-check|verify|confirm|is it true"
    - "api|sdk|library|framework"
    - "best practice|implementation guide"
    - "pex|medical|grounding"
  primary_cli: research
  fallback: pieces (for code examples)

local_context:
  patterns:
    - "my code|code I wrote|my implementation"
    - "saved|snippet|previous solution"
    - "ltm|long-term memory|work history"
    - "what was I working on"
  primary_cli: pieces
  fallback: limitless (for discussion context)
```

## Routing Decision Tree

```
User Request
    │
    ├── Explicit Command?
    │   ├── /context → Parallel Mode (all sources)
    │   ├── /limitless → Single Mode (limitless)
    │   ├── /research → Single Mode (research)
    │   └── /pieces → Single Mode (pieces)
    │
    ├── Intent Detection (from hook signal)
    │   ├── Personal patterns → limitless
    │   ├── Research patterns → research
    │   ├── Local patterns → pieces
    │   └── Multiple matches → Parallel Mode
    │
    └── No Clear Signal
        └── Skip (no external context needed)
```

## Orchestration Modes

### Single Source Mode

Use when intent clearly maps to one CLI:

```yaml
mode: single
process:
  1. Identify primary CLI from intent
  2. Construct appropriate command
  3. Execute and capture output
  4. Return structured context
latency: 1-5 seconds
```

### Parallel Mode

Use for `/context` or multi-domain queries:

```yaml
mode: parallel
process:
  1. Spawn subagents for each relevant CLI
  2. Execute extractions in parallel
  3. Collect and merge results
  4. Deduplicate and rank by relevance
latency: Max of individual CLIs (5-15 seconds)
```

### Augmented Mode (with Deep-Research)

Use when integrating with deep-research skill:

```yaml
mode: augmented
process:
  1. Pre-enrichment: Gather personal/local context
  2. Hand off to deep-research Phase 1
  3. Use research CLI as primary in Phase 3
  4. Include pieces patterns in triangulation
integration_point: Phase 0 pre-enrichment
```

## CLI Command Reference

### Limitless (Personal Context)

```bash
# SEMANTIC SEARCH (Recommended) - Vector-based similarity
limitless semantic-search "ICU critical care" --types Lifelog,Chat,Person --limit 5 --json

# Hybrid search (semantic + full-text)
limitless search "medical exam" --mode hybrid --json

# Full-text search (keyword)
limitless lifelogs search "query" --limit 10 --format json

# Get today's snapshot
limitless workflow daily $(date +%Y-%m-%d) --format json

# Get recent activity (last N hours)
limitless workflow recent --hours 24 --format json

# Cross-source search
limitless workflow search "query" --format json

# Graph query (for relationships - FalkorDBLite)
limitless graph query "MATCH (p:Person)-[:SPOKE_IN]->(l:Lifelog) RETURN p.name, count(l) ORDER BY count(l) DESC LIMIT 5"

# Check embedding status
limitless index status
```

### Research (Online Context)

```bash
# Technical documentation
research docs -t "query" -k "framework" --format json

# Fact verification
research fact-check -t "claim to verify" --graph

# Medical/PEX grounding
research pex-grounding -t "medical query"

# SDK/API reference
research sdk-api -t "api question"

# Academic search
research academic -t "research topic"
```

### Pieces (Local Context)

```bash
# Ask with LTM (Long-Term Memory)
pieces ask "query" --ltm

# Semantic code search
pieces search --mode ncs "pattern"

# With file context
pieces ask "query" -f file1.py file2.py

# With saved materials
pieces ask "query" -m 1 2 3

# Full-text search
pieces search --mode fts "exact text"
```

## Subagent Invocation

When spawning subagents for CLI extraction:

```yaml
limitless_agent:
  type: general-purpose
  prompt: "Extract personal context using limitless CLI. Query: {query}"
  spec: agents/limitless-agent.md

research_agent:
  type: researcher
  prompt: "Extract online documentation using research CLI. Query: {query}"
  spec: agents/research-agent.md

pieces_agent:
  type: general-purpose
  prompt: "Extract local code context using pieces CLI. Query: {query}"
  spec: agents/pieces-agent.md
```

## Session Caching

### Cache Strategy

```yaml
cache_location: ~/.claude/.context-cache/session-context.json

ttl_by_source:
  limitless: 30 minutes  # Personal data stable
  research: 60 minutes   # Docs change slowly
  pieces: 15 minutes     # Active development

cache_key_format: "{source}:{command_type}:{query_hash}"

invalidation:
  - New session starts
  - Explicit refresh request
  - TTL expiration
```

### Cache Operations

```python
# Check cache before CLI invocation
cache_key = f"{source}:{hash(query)}"
if cached := get_cache(cache_key):
    if not expired(cached):
        return cached.result

# After successful extraction
set_cache(cache_key, result, ttl=TTL_BY_SOURCE[source])
```

## Integration with Deep-Research

### Phase 0 Pre-Enrichment

When deep-research is invoked, optionally gather context first:

```yaml
phase_0_context:
  trigger: User has relevant personal/local background

  actions:
    personal_background:
      cli: limitless
      query: "Search for relevant conversations about {topic}"

    local_patterns:
      cli: pieces
      query: "Find related code I've written about {topic}"

  output:
    format: Context briefing for Phase 1 scoping
    content:
      - Relevant past discussions
      - Related code implementations
      - Known constraints from experience
```

### Integration Points

| Deep-Research Phase | Context Integration |
|---------------------|---------------------|
| Phase 1 (Scoping) | Include personal context as background |
| Phase 3 (Querying) | Use research CLI as primary retrieval |
| Phase 4 (Triangulation) | Add pieces code patterns as evidence |

## Output Format

### Structured Context Response

```json
{
  "source": "limitless|research|pieces",
  "query": "original query",
  "results": [
    {
      "title": "Result title",
      "content": "Extracted content...",
      "metadata": {
        "timestamp": "ISO8601",
        "confidence": 0.85,
        "source_type": "lifelog|document|snippet"
      }
    }
  ],
  "cached": false,
  "latency_ms": 1234
}
```

### Multi-Source Response

```json
{
  "mode": "parallel",
  "sources": {
    "limitless": { ... },
    "research": { ... },
    "pieces": { ... }
  },
  "merged_context": "Synthesized context from all sources...",
  "total_latency_ms": 3456
}
```

## Error Handling

### CLI Unavailability

```yaml
on_cli_unavailable:
  limitless: "Limitless CLI not configured. Skip personal context."
  research: "Research CLI not available. Skip online lookup."
  pieces: "Pieces not running. Skip local context."

fallback: Continue with available sources
```

### Timeout Handling

```yaml
timeouts:
  limitless: 10s
  research: 15s
  pieces: 8s

on_timeout:
  action: Return partial results
  message: "Context extraction timed out. Proceeding with available data."
```

## Usage Examples

### Example 1: Personal Memory Query

**User**: "What did John say about the API deadline in yesterday's meeting?"

**Process**:
1. Intent detector signals: `{need_limitless: true, confidence: 0.9}`
2. Route to limitless single-source mode
3. Execute: `limitless lifelogs search "John API deadline" --limit 5 --format json`
4. Return structured context with relevant excerpts

### Example 2: Technical Documentation

**User**: "How do I implement WebSocket authentication in Bun?"

**Process**:
1. Intent detector signals: `{need_research: true, confidence: 0.85}`
2. Route to research single-source mode
3. Execute: `research docs -t "WebSocket authentication" -k "bun" --format json`
4. Return documentation with code examples

### Example 3: Multi-Source Context

**User**: `/context What approach should I use for the auth refactor?`

**Process**:
1. Explicit `/context` command triggers parallel mode
2. Spawn three subagents:
   - limitless: "auth refactor discussions"
   - research: "auth best practices"
   - pieces: "previous auth implementations"
3. Collect and merge results
4. Return comprehensive context from all sources

## Best Practices

1. **Cache First**: Always check session cache before CLI invocation
2. **Limit Results**: Use `--limit` flags to avoid context overflow
3. **JSON Output**: Prefer JSON format for structured parsing
4. **Timeout Protection**: Set reasonable timeouts per CLI
5. **Graceful Degradation**: Continue with available sources if one fails
6. **Relevance Ranking**: Prioritize results by confidence/relevance score

---

## Requirements

This skill requires three CLI tools. Graceful degradation occurs if any are missing:

| CLI | Installation | Required For |
|-----|--------------|--------------|
| `limitless` | `bun run ~/Projects/limitless-cli/bin/limitless.ts` | Personal context |
| `research` | `~/.local/bin/research` | Online documentation |
| `pieces` | `/opt/homebrew/bin/pieces` + PiecesOS running | Local code/LTM |

Verify availability: Run `bash ~/.claude/hooks/session-context-primer.sh`

## Hooks Integration

This skill uses two hooks for automatic context detection:

### UserPromptSubmit Hook
- **File**: `~/.claude/hooks/context-intent-detector.ts`
- **Trigger**: Every user prompt
- **Function**: Pattern matching to detect context-relevant queries
- **Output**: JSON signal with detected sources and confidence
- **Timeout**: 1.5s

### SessionStart Hook
- **File**: `~/.claude/hooks/session-context-primer.sh`
- **Trigger**: Session initialization
- **Function**: Validates CLI availability and initializes cache
- **Output**: System prompt with available sources
- **Timeout**: 5s

## Progressive Loading

This skill uses progressive disclosure to optimize context efficiency:

| File | Purpose | When Loaded |
|------|---------|-------------|
| `SKILL.md` | Quick start, command reference | Always (main skill) |
| `README.md` | Configuration, debugging, upgrades | On maintenance request |
| `agents/*.md` | Subagent specifications | When parallel mode triggered |
| `references/*.md` | Detailed CLI documentation | When deep reference needed |
| `scripts/*.py` | Cache/metrics utilities | On explicit invocation |

## Troubleshooting

### Skill Not Triggering
1. Verify hooks registered: `grep context ~/.claude/settings.json`
2. Check pattern matching: `echo '{"prompt":"your query"}' | bun run ~/.claude/hooks/context-intent-detector.ts`
3. Use explicit command: `/context <query>`

### CLI Unavailable
1. Run session primer: `bash ~/.claude/hooks/session-context-primer.sh`
2. Check individual CLIs:
   - `limitless config show` (needs API key)
   - `research --help`
   - `pieces mcp status` (needs PiecesOS)

### Subagents Timing Out
1. Increase timeout in settings.json (default 1.5-5s)
2. Check CLI latency individually
3. View cache: `cat ~/.claude/.context-cache/session-context.json`

### Cache Issues
1. Clear cache: `python3 ~/.claude/skill-db/context-orchestrator/scripts/cache-manager.py clear`
2. View stats: `python3 ~/.claude/skill-db/context-orchestrator/scripts/cache-manager.py stats`

## Additional Resources

- **Configuration & Debugging**: See [README.md](README.md)
- **Deep-Research Integration**: See [DEEP-RESEARCH-INTEGRATION.md](DEEP-RESEARCH-INTEGRATION.md)
- **CLI Command Reference**: See [references/cli-commands.md](references/cli-commands.md)
- **Security Review**: See [docs/SECURITY-REVIEW.md](docs/SECURITY-REVIEW.md)
- **Skill Metadata**: See [skill.yaml](skill.yaml)
