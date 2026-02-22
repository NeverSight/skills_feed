---
name: council
description: >
  Consult an advisory council of three AI personas — Cato (skeptic), Ada (optimist), Marcus (pragmatist) —
  backed by different frontier LLM agents (Gemini, Claude, Codex). Each persona runs as a separate agent
  process with full repo context and returns independent feedback. Use when the user says "/council",
  asks for a second opinion, wants feedback on code changes, needs a premortem, wants to pressure-test
  a decision, or asks "what do you think about this approach?" Claude may also proactively suggest
  consulting the council before major architectural decisions, risky deploys, or ambiguous trade-offs
  (but should ask for user approval first).
---

# Council

Consult your advisory council: three AI personas backed by different frontier models, each with full repo context.

## Personas

| Name | Archetype | Core question | Default provider |
|------|-----------|---------------|-----------------|
| **Cato** | Skeptical Strategist | "What could go wrong?" | `gemini` |
| **Ada** | Expansive Optimist | "What could this become?" | `claude` |
| **Marcus** | Pragmatic Builder | "What do we do next?" | `codex` |

For full persona details, see [references/personas.md](references/personas.md).

## How to invoke

Run `scripts/counsel.py` via Bash from the current working directory:

```bash
# Consult one persona
python3 <skill-dir>/scripts/counsel.py cato "Should we use Redis or Postgres for session storage?"

# Consult all three (runs in parallel)
python3 <skill-dir>/scripts/counsel.py all "Review the changes in the last commit — are we missing anything?"

# Override a persona's provider
python3 <skill-dir>/scripts/counsel.py ada "Is this API design too minimal?" --ada-provider codex
```

Replace `<skill-dir>` with the absolute path to this skill directory.

## When to consult whom

- **Cato alone**: Security review, risk assessment, premortem, "is this safe to deploy?"
- **Ada alone**: Product direction, UX decisions, "is this feature compelling enough?"
- **Marcus alone**: Implementation tiebreakers, scope cuts, "what's the simplest path?"
- **All three**: Major architecture decisions, launch readiness, "should we do X or Y?"

## Choosing the right moment

Proactively suggest consulting the council when:
- The user is about to make an irreversible architectural decision
- There are multiple valid approaches with non-obvious trade-offs
- A deployment feels risky or under-tested
- The user explicitly asks "what do you think?" about a high-stakes choice

Always ask the user before invoking — say something like: "This feels like a good moment to consult the council. Want me to ask Cato/Ada/Marcus/all for their take?"

## Handling responses

1. Run the script and capture output
2. Show the full, unedited response from each persona to the user — do not summarize or paraphrase their words
3. After showing all responses, briefly note key agreements or tensions across personas
4. Ask the user how they want to proceed — the council advises, the user decides

## Provider configuration

Each persona defaults to a different LLM provider for genuine model diversity. Override with flags if a provider is unavailable:

- `--cato-provider claude|codex|gemini`
- `--ada-provider claude|codex|gemini`
- `--marcus-provider claude|codex|gemini`

The script has a 5-minute timeout per persona. All agents run in read-only mode in the current directory.
