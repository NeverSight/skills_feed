---
name: perplexity-cli
description: |
  CLI interface for Perplexity AI. Perform AI-powered searches, queries, and research directly from terminal.
  Use when user mentions Perplexity, AI search, web research, or needs to query AI models like GPT, Claude, Grok, Gemini.
  Commands: query.
compatibility: |
  Requires perplexity CLI installed. Verify with `perplexity --help`.
  Config location: ~/.perplexity-cli/
allowed-tools: Bash(perplexity:*), Read
---

# Perplexity CLI Skill

## Overview

Perplexity CLI is a command-line interface for Perplexity AI that allows AI-powered searches directly from the terminal with support for multiple models, streaming output, and file attachments.

## Prerequisites

```bash
# Verify installation
perplexity --help

## Quick Reference

| Command | Description |
|---------|-------------|
| `perplexity "query"` | Search with default settings |

| Mode | Flag | Description |
|------|------|-------------|
| pro | `--mode pro` | Deep search with reasoning (default) |
| deep-research | `--mode deep-research` | Comprehensive research |

## Common Operations

### Basic Query
```bash
perplexity "What is quantum computing?"
```

### Query with Specific Mode
```bash
perplexity "Explain neural networks" --mode pro
```

### Read Query from File, Save Response
```bash
perplexity -f question.md -o answer.md 
```

### Query with Sources 
```bash
perplexity "Climate research" --sources web,scholar 
```

## All Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--mode` | | Search mode |
| `--sources` | `-s` | Sources: web,scholar,social |
| `--language` | `-l` | Response language (e.g., en-US, pt-BR) |
| `--file` | `-f` | Read query from file |
| `--output` | `-o` | Save response to file |

## Best Practices

1. Use `--mode deep-research` for comprehensive research tasks
2. Use `-f` and `-o` flags for batch processing

## Piping and Scripting

```bash
# Pipe query from stdin
echo "What is Go?" | perplexity

# Use in scripts
RESPONSE=$(perplexity "Quick answer" --mode pro 2>/dev/null)

# Batch processing
cat questions.txt | while read q; do
  perplexity "$q" -o "answers/$(echo $q | md5sum | cut -c1-8).md"
done
```
