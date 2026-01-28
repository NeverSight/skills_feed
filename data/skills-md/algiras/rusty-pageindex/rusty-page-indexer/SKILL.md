---
name: rusty-page-indexer
description: High-performance semantic indexing and retrieval of local PDF and Markdown files with multi-repo support.
version: 0.5.0
author: Algiras
license: MIT
---

# Rusty Page Indexer Skill

This skill allows agents to index and query local documentation using `rusty-page-indexer`. Unlike standard vector databases, it focuses on **Structural Context**, preserving the document's hierarchical tree for more logical retrieval.

## Why Structure Matters

Standard RAG often slices documents into arbitrary chunks, losing context. `rusty-page-indexer` maintains a **Folder → File → Section** hierarchy. 
- **Logical Retrieval**: Instead of just matching a sentence, you match a logical section (e.g., an entire API endpoint description).
- **Project Awareness**: The LLM understands where a file lives (e.g., `src/auth`) giving it contextual cues about the code's purpose.

## Key Capabilities

- **Multi-repo indexing**: Index multiple projects independently
- **Cross-repo search**: Query across all indexed repositories
- **Parallel processing**: Fast indexing with Rayon
- **Unified tree structure**: Folder -> File -> Section hierarchy
- **Model flexibility**: Works with OpenAI, Ollama, and OpenAI-compatible APIs

## Commands

### 1. Install Tool
Install the `rusty-page-indexer` binary (Linux/macOS).

```bash
curl -fsSL https://raw.githubusercontent.com/Algiras/rusty-pageindex/main/install.sh | bash
```

### 2. Configure Authentication

**OpenAI (remote):**
```bash
rusty-page-indexer auth --api-key "sk-..." --model "gpt-4o-mini"
```

**Ollama (local):**
```bash
rusty-page-indexer auth --api-key "ollama" --api-base "http://localhost:11434/v1" --model "llama3.2"
```

**Other OpenAI-compatible APIs:**
```bash
# Groq
rusty-page-indexer auth --api-key "your-key" --api-base "https://api.groq.com/openai/v1" --model "llama3-70b-8192"

# Together AI
rusty-page-indexer auth --api-key "your-key" --api-base "https://api.together.xyz/v1" --model "meta-llama/Llama-3-70b-chat-hf"
```

### 3. Index Documents
Recursively index a directory of documents (`.md`, `.pdf`).

```bash
# Fast index (no LLM calls, instant)
rusty-page-indexer index <path>

# With LLM-generated summaries (higher quality, slower)
rusty-page-indexer index <path> --enrich

# Two-Phase Strategy (Recommended)
# 1. Index the whole folder quickly for structure
rusty-page-indexer index ./projects
# 2. Enrich only the critical "Holy Grail" docs (specs/manuals)
rusty-page-indexer index ./projects/docs/architecture_spec.md --enrich
```

> [!TIP]
> Use `--enrich` sparingly on large folders. Index generally first, then enrich specific key files for deep reasoning.
```

### 4. List Indexed Repositories
View all indexed repositories with their sizes and paths.

```bash
rusty-page-indexer list
```

### 5. Query Index
Perform semantic search over indexed documents.

```bash
# Search all repositories
rusty-page-indexer query "How does authentication work"

# Path-Scoped Query (Search only specific component/folder)
# Useful for multi-repo work or filtering to 'backend' only.
rusty-page-indexer query "auth" --path backend

# Override model for this query (using argument separator)
rusty-page-indexer query "Explain API" -- --model gpt-4o
```

### 6. Clean Up Indices
Remove indexed repositories.

```bash
# Remove specific index
rusty-page-indexer clean <repo-name>

# Remove all indices
rusty-page-indexer clean --all
```

### 7. Check Status
Verify installation and configuration.

```bash
rusty-page-indexer info
```

## Model Compatibility

### OpenAI Models (Remote)
| Model | Cost | Recommended For |
|-------|------|-----------------|
| `gpt-4o-mini` | $ | General use (fast & cheap) |
| `gpt-4o` | $$$ | Complex queries |
| `gpt-4-turbo` | $$ | Large documents |
| `gpt-3.5-turbo` | cents | Budget option |

### Local Models (Ollama)
| Model | Size | Notes |
|-------|------|-------|
| `llama3.2` | 3B | Recommended for local use |
| `gemma3` | 4B | Highly efficient reasoning model ⭐ |
| `mistral:7b` | 7B | Fast and capable |
| `qwen2.5:7b` | 7B | Reliable |

## Troubleshooting

The tool provides detailed error messages:

| Error | Meaning | Fix |
|-------|---------|-----|
| Model not found | Invalid model name | Use `rusty-page-indexer config --model gpt-4o-mini` |
| Invalid API key | Wrong or expired key | Re-run `auth` with valid key |
| Quota exceeded | Out of credits | Add billing at platform.openai.com or use Ollama |
| Rate limit | Too many requests | Wait 30-60s and retry |
| Connection refused | Ollama not running | Run `ollama serve` |
| Invalid children | Corrupted state | **Nuke & Pave**: `rm -rf ~/.rusty-page-indexer/manifest.json ~/.rusty-page-indexer/indices && rusty-page-indexer info` |

## Typical Workflow

```bash
# 1. Install (if needed)
curl -fsSL https://raw.githubusercontent.com/Algiras/rusty-pageindex/main/install.sh | bash

# 2. Configure for Ollama (free, local)
rusty-page-indexer auth --api-key "ollama" --api-base "http://localhost:11434/v1" --model "llama3.2"

# 3. Index your project
rusty-page-indexer index ./docs --enrich

# 4. Search
rusty-page-indexer query "how does authentication work"

# 5. View indexed repos
rusty-page-indexer list
```

## Storage Location

All data is stored in `~/.rusty-page-indexer/`:
- `config.toml` - API credentials and default model
- `manifest.json` - Index registry
- `indices/` - Tree index files
