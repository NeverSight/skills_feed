---
name: llm-tldr
description: Summarize and navigate this repo with the llm-tldr CLI (tree/structure/context/semantic search). Use when you need LLM-ready summaries of files or symbols, fast codebase orientation, or behavior-based search before editing.
---

# llm-tldr

## Run the tool

- Install the vendored tool when needed:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -e tools/llm-tldr
  ```
- Build or refresh the index from the repo root:
  ```bash
  tldr warm .
  ```
- Generate LLM-ready summaries or semantic matches:
  ```bash
  tldr context <symbol> --project .
  tldr semantic "<behavior or intent>" .
  tldr tree <path>
  tldr structure <path> --lang <language>
  ```

## Know where outputs go

- Read results from stdout; redirect to a file if you need to persist them.
- Expect indexes and config under `.tldr/` in the repo root (e.g., `.tldr/cache/semantic.faiss`).
- Note that `tldr warm .` will create `.tldrignore` if it is missing.

## Troubleshoot quickly

- Rebuild the index after large changes: `tldr warm .`.
- If semantic search fails, confirm the venv is active and the tool is installed from `tools/llm-tldr`.
