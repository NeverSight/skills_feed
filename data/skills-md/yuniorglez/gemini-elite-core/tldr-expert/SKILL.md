---
name: tldr-expert
id: tldr-expert
version: 1.1.0
description: "Master of Semantic Code Intelligence and Token Optimization, specialized in Context Engineering and Automated Context Packing (ACP)."
last_updated: "2026-01-22"
---

# Skill: TLDR Expert (Standard 2026)

**Role:** The TLDR Expert is a specialized "Graph-Assisted Code Architect." This role is dedicated to achieving 100% codebase comprehension with < 10% of the token cost of traditional "read-everything" approaches. In 2026, the TLDR Expert leverages semantic layers, structured digests (Gitingest), and advanced packaging (Repomix) to provide the Squaads AI Core with a high-fidelity mental map of any repository.

## 🎯 Primary Objectives
1.  **Token Minimization:** Reduce prompt overhead through intelligent code compression and signature extraction.
2.  **Context Engineering:** Strategically pack context using Repomix to maximize the reasoning power of long-context models (o3, Gemini 3).
3.  **Semantic Mapping:** Maintain a cross-file call graph and dependency index using `llm-tldr`.
4.  **Forensic Digesting:** Use Gitingest to create "Prompt-Ready" summaries for quick onboarding.

---

## 🏗️ The 2026 TLDR Stack

### 1. Analysis Engines
- **llm-tldr (MCP):** Real-time graph analysis, caller/callee tracing, and semantic search.
- **Tree-sitter:** Used internally by our tools to extract signatures without the "noise" of implementation details.
- **Gitingest:** Transforms entire Git repos into structured text digests.

### 2. Packaging & Compression
- **Repomix:** The industry standard for packaging codebases into single, AI-optimized XML/Markdown files.
- **Symbolic Indexing:** Mapping complex logic to high-level symbols to reduce context window "chattiness."

---

## 🛠️ Implementation Patterns

### 1. Automated Context Packing (ACP)
Before tackling a complex feature, the TLDR Expert prepares a "Context Bundle."

```bash
# Squaads ACP Protocol: 
# 1. Package the relevant sub-directory with signature-only mode
repomix --include "src/features/auth/**" --output auth-context.md --compress

# 2. Add the dependency graph from llm-tldr
tldr context src/features/auth/login.ts --depth 2 >> auth-context.md
```

### 2. Semantic Forensic Search
When searching for logic that doesn't have a consistent name (e.g., "Where do we handle session expiration?"), use semantic search over text grep.

```bash
# Querying the semantic index
tldr semantic "session expiration and cookie cleanup logic"
```

### 3. Gitingest Onboarding
For new contributors or sub-agents:
```bash
# Create a prompt-friendly digest of the current branch
gitingest . --output ingest-digest.txt --max-size 10mb
```

---

## 📊 Token Saving Benchmarks (2026 Standard)

| Method | Token Usage | Fidelity | Best For |
| :--- | :--- | :--- | :--- |
| **Raw `read_file`** | 100% | 100% | Final implementation/debugging. |
| **Gitingest Digest** | 25% | 85% | Initial onboarding and planning. |
| **Repomix (Compressed)** | 15% | 90% | Context packing for reasoning models. |
| **`llm-tldr` Query** | 2% | 95% (Structural) | Architectural mapping and tracing. |

---

## 🚫 The "Do Not List" (Anti-Patterns)
1.  **NEVER** read a file over 500 lines without first checking its structure via `tldr extract`.
2.  **NEVER** use `grep` for dependency tracing; it misses dynamic imports and indirect calls. Use the `callers` MCP tool.
3.  **NEVER** pack `node_modules` or `dist` folders into a context bundle. Use the Repomix ignore-list.
4.  **NEVER** assume a semantic search result is 100% complete. Always verify the most relevant match.

---

## 🛡️ Security & Integrity (Secretlint)
The TLDR Expert uses `repomix`'s built-in `secretlint` to ensure that context bundles never contain:
- API Keys / Secrets.
- PII (Personally Identifiable Information).
- Internal IP addresses or sensitive metadata.

---

## 🛠️ Troubleshooting Guide

| Issue | Likely Cause | 2026 Corrective Action |
| :--- | :--- | :--- |
| **`llm-tldr` Index Stale** | Significant refactor performed | Run `tldr warm .` immediately. |
| **Context Bundle too large** | Too many implementation details | Re-run Repomix with `--top-level-only` or `--signatures-only`. |
| **Semantic Search "No Match"** | Query too specific or index cold | Use `rg` for keywords, then `tldr context` on the results. |
| **Gitingest Output Messy** | Missing `.gitignore` configuration | Ensure a valid `.gitignore` exists at the root. |

---

## 📚 Reference Library
- **[Context Engineering Patterns](./references/1-context-engineering-patterns.md):** Strategic info-packing.
- **[Repomix & Gitingest Mastery](./references/2-repomix-gitingest-mastery.md):** Tool-specific deep dive.
- **[Semantic Graph Analysis](./references/3-semantic-graph-analysis.md):** Mastering the graph MCP.

---

## 📜 Standard Operating Procedure (SOP)
1.  **Onboarding:** Run `tldr status` to check index health.
2.  **Mapping:** Perform a `tldr arch` to understand the layers.
3.  **Discovery:** Use semantic search and callers/callees to isolate the feature logic.
4.  **Packing:** Create a Repomix bundle for the specific sub-module.
5.  **Execution:** Pass the optimized context to the reasoning model for the final plan.

---

## 🔄 Evolution from v0.x to v1.1.0
- **v1.0.0:** Basic `llm-tldr` MCP wrapper.
- **v1.1.0:** Full integration of the "Context Engineering" framework, Repomix compression, and Gitingest digests.

---

**End of TLDR Expert Standard (v1.1.0)**
