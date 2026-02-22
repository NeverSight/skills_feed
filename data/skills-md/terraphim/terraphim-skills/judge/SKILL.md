---
name: judge
description: >
  Evaluate agent task outputs using a three-dimension rubric (Semantic, Pragmatic,
  Syntactic) derived from the KLS quality framework. Use when: (1) a task has been
  completed and needs quality assessment before acceptance, (2) automated post-task
  quality checks are required, (3) multi-model consensus verdicts are needed for
  agent outputs, (4) documentation, code, or specification quality must be scored
  with structured JSON verdicts, or (5) a human fallback decision is needed after
  model disagreement. Produces JSONL verdict records compatible with the verdict
  schema in automation/judge/.
license: Apache-2.0
---

# Judge

## Overview

Evaluate agent task outputs against a three-dimension rubric and produce structured
verdict records. The judge operates as a quality gate at the task completion boundary,
scoring outputs on Semantic accuracy, Pragmatic usefulness, and Syntactic consistency.

## Rubric: Three KLS Dimensions

The rubric reuses three dimensions from the KLS (Krogstie-Lindland-Sindre) quality
framework defined in `disciplined-quality-evaluation`:

| Dimension | Question | Criteria |
|-----------|----------|----------|
| **Semantic** | Does it accurately represent the domain? | Factual correctness, domain terminology, no contradictions |
| **Pragmatic** | Does it enable the intended decisions/actions? | Actionable, useful, addresses the task goal |
| **Syntactic** | Is it internally consistent and well-structured? | Format compliance, structural completeness, no broken references |

### Scoring

| Score | Meaning |
|-------|---------|
| 1 | Poor -- major issues, blocks use |
| 2 | Below Standard -- significant gaps |
| 3 | Adequate -- meets minimum bar |
| 4 | Good -- clear, useful, few issues |
| 5 | Excellent -- exemplary, no issues |

### Verdict Thresholds

| Condition | Verdict |
|-----------|---------|
| All dimensions >= 3 AND average >= 3.5 | **accept** |
| Any dimension < 3 OR average < 3.5, but all >= 2 | **improve** |
| Any dimension < 2 | **reject** |
| Models disagree on accept/reject | **escalate** |

## Verdict Format

Every judge evaluation produces a JSON verdict record. See `automation/judge/verdict-schema.json`
for the full schema. Minimal structure:

```json
{
  "task_id": "issue-18",
  "model": "opencode/gpt-5-nano",
  "mode": "quick",
  "verdict": "accept",
  "scores": {
    "semantic": 4,
    "pragmatic": 4,
    "syntactic": 5
  },
  "average": 4.33,
  "reasoning": "Brief justification for scores",
  "improvements": [],
  "timestamp": "2026-02-17T14:30:00Z"
}
```

Output MUST be valid JSON only -- no markdown fencing, no preamble, no trailing text.

## Judge Modes

### Quick Judge

- **Model**: opencode/gpt-5-nano (fast, low latency)
- **Purpose**: Rapid pass/fail screening at task completion
- **Timeout**: 30 seconds
- **Prompt template**: [references/prompt-quick.md](references/prompt-quick.md)
- **Output**: Verdict JSON with scores and one-line reasoning

### Deep Judge

- **Model**: opencode/kimi-k2.5-free (thorough, reasoning-capable)
- **Purpose**: Detailed evaluation with improvement suggestions
- **Timeout**: 60 seconds
- **Prompt template**: [references/prompt-deep.md](references/prompt-deep.md)
- **Output**: Verdict JSON with scores, reasoning chain, and improvement list

### Tiebreaker

- **Model**: opencode/gpt-5.1-codex-mini (independent perspective, different provider)
- **Purpose**: Resolve accept/reject disagreement between quick and deep judges
- **Timeout**: 45 seconds
- **Prompt template**: Uses deep prompt with prior verdicts appended
- **Trigger**: Quick and deep verdicts disagree on accept vs reject/improve

## Multi-Iteration Protocol

```
1. Run quick judge
   |
   +-- accept --> DONE (accept)
   +-- reject --> DONE (reject, log improvements)
   +-- improve --> Run deep judge
                   |
                   +-- accept --> DONE (accept)
                   +-- reject --> DONE (reject, log improvements)
                   +-- improve --> Human fallback
```

When quick and deep disagree on accept vs reject:

```
Quick: accept + Deep: reject --> Run tiebreaker
Quick: reject + Deep: accept --> Run tiebreaker
Tiebreaker verdict is final (no further iteration)
```

Maximum 3 model calls before human fallback.

## Human Fallback Criteria

Escalate to human review when:

1. Three model calls completed without consensus
2. Any model returns invalid JSON after retry
3. Any model times out after retry
4. Verdict is "improve" from both quick and deep judges (ambiguous quality)
5. Task involves security-sensitive or compliance-critical content

## Integration Points

### Runner Script

The judge is invoked by `automation/judge/run-judge.sh` (v2), which:
- Writes prompts to temp files (eliminates shell escaping issues with file content)
- Calls opencode with `--file <tempfile>` for reliable prompt delivery
- Parses verdict JSON from opencode's JSON event stream
- Implements the multi-iteration protocol (quick -> deep -> tiebreaker)
- Optionally enriches verdict logging with terraphim-cli term matching

### Verdict Logging

All verdicts are appended to `automation/judge/verdicts.jsonl` as one JSON object per line.
This enables:
- Audit trail of all quality evaluations
- Trend analysis across tasks
- Model performance comparison

### Pre-Push Hook

The judge can be invoked as a pre-push hook via `automation/judge/pre-push-judge.sh`,
blocking pushes that receive a "reject" verdict.

## Terraphim Integration (Optional)

When terraphim-cli is available, the judge runner uses knowledge graph-based
term normalization to identify rubric dimensions in model reasoning.

### Knowledge Graph Setup

```bash
# Install judge KG files and configure role
bash automation/judge/setup-judge-kg.sh

# Verify installation
terraphim-cli thesaurus --limit 50
terraphim-cli find "factual correctness and actionability"
```

### KG Files

Located in `automation/judge/kg/`:

| File | Normalized Term | Purpose |
|------|----------------|---------|
| `judge-semantic.md` | judge-semantic | Synonyms for semantic quality dimension |
| `judge-pragmatic.md` | judge-pragmatic | Synonyms for pragmatic quality dimension |
| `judge-syntactic.md` | judge-syntactic | Synonyms for syntactic quality dimension |
| `judge-verdicts.md` | judge-verdicts | Verdict vocabulary normalization |
| `judge-checklist.md` | judge-checklist | Required verdict elements |

### Fail-Open Design

If terraphim-cli is not installed, the judge falls back to direct JSON
extraction without term normalization. All core functionality works
without terraphim -- the KG integration is an enrichment layer.

## Resources

### references/

- [prompt-quick.md](references/prompt-quick.md) -- Quick judge prompt template for fast screening
- [prompt-deep.md](references/prompt-deep.md) -- Deep judge prompt template for thorough evaluation
