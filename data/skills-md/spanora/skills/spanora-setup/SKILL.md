---
name: spanora-setup
description: >-
  Setup Spanora AI observability in any project (JavaScript/TypeScript or Python).
  Use when user asks to "add spanora", "setup spanora", "integrate spanora",
  "add AI observability", "monitor LLM calls with spanora", "track AI costs",
  or mentions spanora in the context of adding observability to their project.
  Detects the language and installed AI SDKs (Vercel AI, Anthropic, OpenAI,
  LangChain) and configures the optimal integration pattern.
metadata:
  author: spanora
  version: "2.0.0"
license: MIT
---

# Spanora Setup Agent Skill

You are integrating Spanora AI observability into the user's project. Follow this guide step by step.

## 1. When to Invoke

Activate this skill when the user says any of:

- "add spanora", "setup spanora", "integrate spanora"
- "add AI observability", "add LLM monitoring"
- "monitor LLM calls with spanora", "track AI costs"
- "instrument my agent", "add tracing to my agent"
- mentions "spanora" in the context of adding observability

## 2. Public Documentation — Source of Truth

The official Spanora documentation at **https://spanora.ai/docs** is always up to date and is the canonical source of truth. The bundled `references/` files in this skill are the primary step-by-step guide, but **if you encounter ambiguity, an unfamiliar API, edge cases, or something that doesn't match what you see in the user's code — fetch the relevant doc page** using WebFetch. If the public docs contradict a bundled reference, the public docs win.

**Key pages by integration pattern:**

| Pattern | Doc page |
| --- | --- |
| Vercel AI SDK | https://spanora.ai/docs/integrations/vercel-ai |
| OpenAI SDK | https://spanora.ai/docs/integrations/openai |
| Anthropic SDK | https://spanora.ai/docs/integrations/anthropic |
| LangChain Python | https://spanora.ai/docs/integrations/langchain |
| Raw OTEL / other | https://spanora.ai/docs/integrations/raw-otel |
| TypeScript SDK reference | https://spanora.ai/docs/sdk |
| OTEL attribute conventions | https://spanora.ai/docs/sdk/attributes |

You do **not** need to fetch docs on every run — only when something is unclear or you suspect the bundled references may be stale.

## 3. Prerequisites

The user must have a **Spanora API key** (starts with `ak_`). **Never ask the user to paste their API key into the conversation.**

1. Check if `SPANORA_API_KEY` is already set in `.env` (or `.env.local`) or as a shell environment variable. Only check for **presence** — do **not** output or log the value.
2. If already set, proceed to the next step.
3. If not set, instruct the user to add it themselves:
   - Tell them: **"Please add your Spanora API key to your `.env` file as `SPANORA_API_KEY=ak_...`. You can find your key at https://spanora.ai/settings."**
   - Do **not** accept the key in conversation or write the key value to any file.
   - Wait for the user to confirm they have set it before proceeding.
4. If `.env` is not in `.gitignore`, remind the user to add it.

## 4. Language Detection

Determine the project language by checking for config files in the project root:

| File found         | Language                    |
| ------------------ | --------------------------- |
| `package.json`     | **JavaScript / TypeScript** |
| `pyproject.toml`   | **Python**                  |
| `setup.py`         | **Python**                  |
| `requirements.txt` | **Python**                  |

If both JS and Python files are present, ask the user which part of the project to instrument.

## 5. Detection — Determine the Integration Pattern

### JavaScript / TypeScript

Read `package.json` and check `dependencies` and `devDependencies`:

| Dependency found    | Pattern to use                |
| ------------------- | ----------------------------- |
| `ai`                | **Pattern A** — Vercel AI SDK |
| `@anthropic-ai/sdk` | **Pattern B** — Anthropic SDK |
| `openai`            | **Pattern C** — OpenAI SDK    |
| None of the above   | **Pattern D** — Raw Core SDK  |

If multiple are present, prefer in order: A > B > C. Use the pattern matching the SDK the user's code actually calls. If unsure, ask.

### Python

Read `pyproject.toml` (or `requirements.txt` / `setup.py`) and check dependencies:

| Dependency found | Pattern to use                        |
| ---------------- | ------------------------------------- |
| `langchain`      | **Pattern E** — LangChain / LangGraph |

More Python patterns may be added in the future. If the user's Python project does not use LangChain, inform them that Spanora supports any Python framework via raw OpenTelemetry — refer them to the LangChain reference as a template for OTEL setup.

## 6. Package Manager Detection

### JavaScript / TypeScript

| File found          | Package manager |
| ------------------- | --------------- |
| `pnpm-lock.yaml`    | `pnpm`          |
| `yarn.lock`         | `yarn`          |
| `bun.lockb`         | `bun`           |
| `package-lock.json` | `npm`           |

### Python

| File found     | Package manager |
| -------------- | --------------- |
| `uv.lock`      | `uv`            |
| `poetry.lock`  | `poetry`        |
| `Pipfile.lock` | `pipenv`        |
| Otherwise      | `pip`           |

## 7. Install

### JavaScript / TypeScript

```bash
pnpm add @spanora-ai/sdk
# or: npm install @spanora-ai/sdk / yarn add @spanora-ai/sdk / bun add @spanora-ai/sdk
```

### Python (LangChain)

```bash
pip install opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-langchain langgraph
# or: uv add ... / poetry add ... / pipenv install ...
```

No Spanora SDK is needed for Python — tracing uses standard OpenTelemetry.

## 8. Integration — Read the Matching Reference

Based on the detected pattern, read the corresponding reference file for code examples and API usage:

**JavaScript / TypeScript:**

- **Pattern A** (Vercel AI SDK): Read `references/vercel-ai.md`
- **Pattern B** (Anthropic SDK): Read `references/anthropic.md`
- **Pattern C** (OpenAI SDK): Read `references/openai.md`
- **Pattern D** (Raw Core SDK): Read `references/core-sdk.md`

**Python:**

- **Pattern E** (LangChain / LangGraph): Read `references/langchain-python.md`

**For JS/TS patterns, always also read `references/common.md`** for shared patterns: `init()`, `shutdown()`, tool tracking (`trackToolHandler`, `runTool`), multi-agent shared context, agent naming guidance, API key setup, and the migration checklist. Python patterns are self-contained in their reference file.

Apply the patterns from the reference files to the user's code. The reference files contain production-ready examples verified against the SDK source and integration tests.

## 9. Ensure Full Instrumentation Coverage

**Every AI execution must produce at least one trace.** For each LLM call site in the user's code, use the highest-fidelity approach available:

1. **Auto-telemetry** — `experimental_telemetry` for Vercel AI SDK, auto-instrumentation for LangChain. Preferred when available — zero manual work.
2. **Provider wrappers** — `trackOpenAI`, `trackAnthropic`, `trackVercelAI` / `trackVercelAIStream`. Use when auto-telemetry is unavailable for a call site (e.g. tool-loop agents, custom agent patterns).
3. **Core SDK functions** — `trackLlm`, `trackLlmStream`, `recordLlm`. Fallback for any LLM call not covered by the above.

After applying the base integration, scan the user's code for any LLM call that would not produce a span. If found, wrap it with the appropriate tracking function from the list above. Do not leave blind spots.

## 10. Offer Optional Enrichments

After applying the base integration, **mention** these optional features to the user. Do not add them by default — only include them if the user's code has the relevant context available or the user asks for them:

- **User & org context** — `userId`, `orgId`, `agentSessionId` on `track()` calls. Links traces to end users, tenants, and sessions in the dashboard. Only add if the code has access to these values (e.g. from a request context, auth session, or API input).
- **Operation type** — `operation` on LLM meta (`trackLlm`, `trackOpenAI`, `trackAnthropic`, `recordLlm`). Defaults to `"chat"`. Set to `"embeddings"` for embedding calls or `"text_completion"` for completion calls. Only relevant when the user's code makes non-chat LLM calls.

**Field name reference:**

- `track()` uses `agent` (not `agentName`) for the agent name
- LLM tracking functions use `prompt` (not `promptInput`) for the input prompt
- LLM result/extractors use `output` (not `promptOutput`) for the output text

Each reference file has an "Optional Enrichments" section with code examples for these features.
