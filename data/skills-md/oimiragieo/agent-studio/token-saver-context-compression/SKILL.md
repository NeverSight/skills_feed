---
name: token-saver-context-compression
description: Search-aware context compression workflow for agent-studio. Use pnpm hybrid search + token-saver compression, then persist distilled learnings via MemoryRecord.
argument-hint: [file-or-text-and-query]
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Token Saver Context Compression

Use this skill to reduce token usage while preserving grounded evidence. This integrates:

- `pnpm search:code` (hybrid retrieval)
- token-saver Python compression scripts
- MemoryRecord persistence into framework memory
- spawn prompt evidence injection (`[mem:*]` / `[rag:*]`)

## When to Use

- `pnpm search:tokens` shows a file/directory exceeds 32K tokens
- Context is large or expensive and you need a compressed summary
- You need query-targeted compression before synthesis
- You need hard evidence sufficiency gating before persisting memory
- You're building a prompt and `search:code` results alone aren't enough context

## Iron Law

Do not persist compressed content directly to memory files from a subprocess.
Emit MemoryRecord payloads and let framework hooks process sync/indexing.

## Workflow

1. Retrieve candidate context (`pnpm search:code "<query>"`).
2. Compress using token-saver in JSON mode (`run_skill_workflow.py --output-format json`).
3. If evidence is insufficient and fail gate is on, stop.
4. Map distilled insights into MemoryRecord-ready payloads.
5. Persist through MemoryRecord so `.claude/hooks/memory/sync-memory-index.cjs` runs.

## Mapping Rule (Deterministic)

- `gotchas.json`:
  - text contains `gotcha|pitfall|anti-pattern|risk|warning|failure`
- `issues.md`:
  - text contains `issue|bug|error|incident|defect|gap`
- `decisions.md`:
  - text contains `decision|tradeoff|choose|selected|rationale`
- `patterns.json`:
  - default fallback for all remaining distilled evidence

## Tooling Commands

Preferred wrapper entrypoint:

```bash
node .claude/skills/token-saver-context-compression/scripts/main.cjs --query "<question>" --mode evidence_aware --limit 20 --fail-on-insufficient-evidence
```

Direct Python engine (advanced):

```bash
python .claude/skills/token-saver-context-compression/scripts/run_skill_workflow.py --file <path> --mode evidence_aware --query "<question>" --output-format json --fail-on-insufficient-evidence
```

## Output Contract

- Wrapper emits JSON with:
  - `search` summary
  - `compression` summary
  - `memoryRecords` grouped by target (`patterns`, `gotchas`, `issues`, `decisions`)
  - `evidence` sufficiency status

## Workflow References

- Skill workflow: `.claude/workflows/token-saver-context-compression-skill-workflow.md`
- Companion tool: `.claude/tools/token-saver-context-compression/token-saver-context-compression.cjs`
- Command surface: `.claude/skills/token-saver-context-compression/commands/token-saver-context-compression.md`
- Citation format is unchanged:
  - memory entries become `[mem:xxxxxxxx]`
  - RAG entries remain `[rag:xxxxxxxx]`

## Integration with search:tokens

Use `pnpm search:tokens` to decide when to invoke this skill:

```bash
# Check if you need compression
pnpm search:tokens .claude/lib/memory
# Output: 60 files, 500KB, ~128K tokens ⚠ OVER CONTEXT

# Then compress with a targeted query
node .claude/skills/token-saver-context-compression/scripts/main.cjs \
  --query "how does memory persistence work" --mode evidence_aware --limit 10
```

The tool reads actual file content from search results (not just file paths), compresses via the Python engine, and extracts memory records classified by type (patterns, gotchas, issues, decisions).

## Adaptive Compression

Adaptive compression (adjusting compression ratio based on corpus size) is automatic and requires no env var configuration. When the input corpus is small, compression is lighter; when it is large, compression is more aggressive. This is controlled internally by the Python engine based on token counts.

## Requirements

- Node.js 18+
- Python 3.10+

## Memory Protocol (MANDATORY)

Before work:

```bash
cat .claude/context/memory/learnings.md
```

After work:

- Add integration learnings to `.claude/context/memory/learnings.md`
- Add integration risks to `.claude/context/memory/issues.md`
