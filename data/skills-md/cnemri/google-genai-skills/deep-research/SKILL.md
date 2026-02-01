---
name: deep-research
description: "Perform autonomous, multi-step research using the Gemini Deep Research Agent (Interactions API). Supports web search, file/directory context, and resilient streaming."
---

# Deep Research

Use this skill to conduct deep, autonomous research tasks that require planning, searching, reading, and synthesizing information.

This skill uses the **Gemini Deep Research Agent** (`deep-research-pro-preview-12-2025`) via the Interactions API.

## Prerequisites

*   `GOOGLE_API_KEY`: Required for accessing the Interactions API (currently in Preview via AI Studio).
*   `google-genai` SDK v0.3.0+

## Usage

### Basic Research
Start a research task and stream the results to the console.

```bash
uv run skills/deep-research/scripts/research.py "Research the history of RISC-V architecture."
```

### Research with Context (Files or Directories)
Provide local files (PDFs, text) or entire directories for the agent to read and incorporate into its research.

**Direct Upload (Best for specific docs):**
```bash
# Single file
uv run skills/deep-research/scripts/research.py "Analyze this report" --file report.pdf

# Entire directory
uv run skills/deep-research/scripts/research.py "Summarize these meeting notes" --file ./notes/
```

**File Search Store (Best for large corpora):**
Use `--use-file-store` to index files into a searchable store (RAG) instead of uploading them into the context window.

```bash
uv run skills/deep-research/scripts/research.py "Find trends in these 1000 PDFs" --file ./large_corpus/ --use-file-store
```

### Saving the Report
Save the final Markdown report to a file.

```bash
uv run skills/deep-research/scripts/research.py "Competitive landscape of EV batteries" --output report.md
```

### Continuing Research (Follow-up)
Ask follow-up questions to an existing research session using the `Interaction ID` (displayed at the start of the previous run).

```bash
uv run skills/deep-research/scripts/research.py "Elaborate on the second point about lithium supply." --follow-up "INTERACTION_ID_HERE"
```

## References
*   [Online Documentation](references/online_docs.md)

## How it Works
1.  **Planning**: The agent breaks down your prompt into steps.
2.  **Execution**: It autonomously searches the web and reads your provided files.
3.  **Resilience**: The script automatically reconnects if the long-running stream drops.
4.  **Synthesis**: It produces a comprehensive, cited report.
