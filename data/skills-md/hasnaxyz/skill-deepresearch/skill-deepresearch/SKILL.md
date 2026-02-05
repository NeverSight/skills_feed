---
name: skill-deepresearch
description: Perform deep research on any topic using Exa.ai for parallel semantic search and Claude/OpenAI for synthesis. Use when you need comprehensive research reports with citations, analysis of topics from multiple angles, or thorough investigation of technical subjects.
---

# Deep Research

Agentic deep research skill using Exa.ai for search and Claude/OpenAI for synthesis.

## Invocation

```
/deepresearch <topic>
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--depth <level>` | Research depth: quick (6 queries), normal (15), deep (30) | normal |
| `--model <provider>` | LLM: claude or openai | claude |
| `--output <path>` | Custom output path | ~/.skills/skill-deepresearch/exports/ |
| `--json` | Also save sources as JSON | false |
| `--no-firecrawl` | Skip deep scraping | false |

## Examples

```bash
# Quick overview of a topic
/deepresearch "What is RAG?" --depth quick

# Standard research with Claude
/deepresearch "Best practices for building production ML systems"

# Deep research with OpenAI, custom output
/deepresearch "Compare Next.js vs Remix" --depth deep --model openai --output ./research.md
```

## Requirements

- `EXA_API_KEY` - Required for search
- `ANTHROPIC_API_KEY` - Required for Claude synthesis
- `OPENAI_API_KEY` - Required for OpenAI synthesis
- `FIRECRAWL_API_KEY` - Optional for deep scraping

## Output

Reports are saved to `~/.skills/skill-deepresearch/exports/` with format:
- `report-{topic-slug}-{timestamp}.md` - Full research report
- `sources-{topic-slug}-{timestamp}.json` - Raw sources (if --json)
