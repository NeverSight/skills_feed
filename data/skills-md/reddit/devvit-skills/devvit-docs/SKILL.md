---
name: devvit-docs
description: Look up Devvit documentation and reference material exclusively from the reddit/devvit-docs repository. Use when the user asks a question about Devvit APIs, patterns, configuration, or examples and you need authoritative guidance.
---

# Devvit Docs (Exclusive)

Look up Devvit documentation by exploring the **single canonical repository**: `https://github.com/reddit/devvit-docs`.

This skill is **exclusive** to `reddit/devvit-docs`:

- Do not use other repositories (including templates, forks, or examples from elsewhere) as sources of truth.
- Do not use third-party docs, blog posts, or web search results as sources of truth.
- If `reddit/devvit-docs` does not contain the answer, say so explicitly and cite the closest relevant file/section you did find.

## Workflow

### 1. Check for Local Availability

First, check if the Devvit docs repository already exists locally (from the current project root):

```bash
ls node_modules/.cache/devvit-docs 2>/dev/null
```

Windows (PowerShell):

```powershell
Test-Path "node_modules\.cache\devvit-docs"
```

If it exists locally, verify it is the correct repo:

```bash
git -C node_modules/.cache/devvit-docs remote -v
```

Windows (PowerShell):

```powershell
git -C "node_modules\.cache\devvit-docs" remote -v
```

If you suspect docs have changed, update it:

```bash
git -C node_modules/.cache/devvit-docs pull --ff-only
```

Windows (PowerShell):

```powershell
git -C "node_modules\.cache\devvit-docs" pull --ff-only
```

### 2. Clone (Only) the Devvit Docs Repository

If not available locally, clone **only** `reddit/devvit-docs` into the project cache:

```bash
mkdir -p node_modules/.cache
git clone https://github.com/reddit/devvit-docs.git node_modules/.cache/devvit-docs
```

Windows (PowerShell):

```powershell
git clone https://github.com/reddit/devvit-docs.git "node_modules\.cache\devvit-docs"
```

### 3. Determine the Correct Versioned Docs Directory

Prefer searching `versioned_docs/` based on the user's **Devvit package version** (from their `package.json`).

Rules:

- Read the user's `package.json`.
- Determine `X.Y` from one of these fields (first match wins):
  - `dependencies.devvit`
  - `dependencies["@devvit/web"]`
  - `dependencies["@devvit/start"]`
- Parse version strings like `0.12.9-next-...` → `0.12`.
- Choose docs root in this order:
- If `node_modules/.cache/devvit-docs/versioned_docs/version-X.Y` exists, use it as primary.
- Else, fall back to `node_modules/.cache/devvit-docs/docs` (main/current docs).
- Windows paths use `node_modules\.cache\devvit-docs\...` for the same directories.

Optional helper to compute `X.Y` (run in the user's repo root):

```bash
node -e 'const fs=require("fs");const p=JSON.parse(fs.readFileSync("package.json","utf8"));const d=p.dependencies||{};const v=d.devvit||d["@devvit/web"]||d["@devvit/start"]||"";const m=String(v).match(/(\d+)\.(\d+)/);process.stdout.write((m?`${m[1]}.${m[2]}`:"") + "\n")'
```

### 4. Research the Repository (Version-Aware)

Research the repository contents to answer the question:

- Search the selected versioned docs directory first (if applicable).
- If needed, also consult `/tmp/devvit-docs/docs` for broader context (but prefer versioned truth when available).
- Prefer reading the most relevant markdown docs, guides, and examples, and always connect claims back to what you found inside this repo.

Example prompt for the agent:

```
Explore the repository at node_modules/.cache/devvit-docs to answer: {user's question}

First, determine the user's Devvit version (X.Y) from their package.json and prefer:
- node_modules/.cache/devvit-docs/versioned_docs/version-X.Y (if it exists)
- otherwise node_modules/.cache/devvit-docs/docs

If on Windows, use:
- node_modules\.cache\devvit-docs\versioned_docs\version-X.Y
- otherwise node_modules\.cache\devvit-docs\docs

Focus on:
- The most relevant markdown docs and guides (and their surrounding context)
- Any official examples, templates, or snippets referenced by the docs
- Configuration references (e.g., `devvit.json`, routing/menu/forms/triggers docs) if applicable
- Versioning/“next” notes and migration guidance if present

Constraints:
- Use ONLY information from this repository.
- If the repo does not contain the answer, report that explicitly and suggest the closest relevant docs found.
```

### 5. Synthesize and Answer

Use the research findings to provide a clear, accurate answer grounded in `reddit/devvit-docs`.

When answering:

- Prefer quoting or pointing to the specific doc section/file that supports the claim.
- Provide a minimal, correct example if the docs include one.
