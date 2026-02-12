---
name: skill-system-insight
description: "Observe user interaction patterns, extract per-session facets, update a dual-matrix soul state, and periodically synthesize a personalized Soul profile for better collaboration."
license: MIT
compatibility: opencode
metadata:
  os: windows, linux, macos
  storage: postgres.agent_memories
  version: 1
---

# Skill System Insight

This skill turns sessions into structured, explainable behavioral insights ("facets"), and uses those facets to evolve a user's Soul state over time.

The intent is pragmatic: collaborate better by learning the user's working style, not by inventing a persona.

## Architecture: Hybrid 3-Layer System

```
Layer 1: Base Profile (balanced.md)
  - Static skeleton: section format + safety/quality defaults.

Layer 2: Dual Matrix (soul-state)
  - Personality Matrix (slow/stable): openness, directness, autonomy, rigor, warmth
  - Emotion Matrix (faster baseline): patience, enthusiasm, caution, empathy

Layer 3: Synthesized Profile (user.md)
  - Periodically regenerated from Layer 1 + Layer 2 + accumulated facets.
```

Layer 2 is the ground truth. Layer 3 is a readable projection.

## Data Model

- Facets (per-session extraction): `schema/facet.yaml`
- Soul state (dual matrix + counters/buffers): `schema/soul-state.yaml`

Storage uses the Postgres `agent_memories` table:

- Facets: `memory_type='episodic'`, `category='insight-facet'`
- Soul state: `memory_type='semantic'`, `category='soul-state'`

## Pipeline

```
Trigger (manual or suggested) -> Extract Facet -> Update Matrix -> (optional) Synthesize Profile
```

References:

- Facet extraction prompt: `prompts/facet-extraction.md`
- Soul synthesis prompt: `prompts/soul-synthesis.md`
- Extraction procedure: `scripts/extract-facets.md`
- Matrix update algorithm: `scripts/update-matrix.md`
- Profile regeneration procedure: `scripts/synthesize-profile.md`

## How To Trigger

This is a manual workflow.

- User can ask explicitly: "insight", "extract facets", "learn my preferences", "update my profile".
- Router suggestion pattern (lightweight, non-pushy):
  - "Want me to run an insight pass to learn from this session? (stores a facet + may update your matrix)"

When the user asks (or agrees), run:

1) `scripts/extract-facets.md`
2) `scripts/update-matrix.md`
3) If the synthesis trigger fires: `scripts/synthesize-profile.md`

## Constraints (Non-Negotiable)

### Transparency

Always explain what was learned and why.

- Facets must contain evidence strings tied to concrete moments.
- Matrix updates must add short context lines explaining each applied adjustment.

### Rate limiting

Max 3 facets per user per rolling 24 hours.

If over limit: do not store a new facet. Instead, write a short note to the user summarizing what you would have captured, and ask them to pick 1 session to record.

### Confidence threshold

Do not change matrix values on a single observation.

- Threshold: 3+ similar observations in the same direction.
- Personality step size: +/- 0.05 per qualifying adjustment.
- Emotion baseline step size: +/- 0.1 per qualifying adjustment.

Accumulation should be tracked (buffers) so the threshold is testable and explainable.

## Where Layer 1 and Layer 3 Live

- Base profile (Layer 1): `skill/skills/skill-system-soul/profiles/balanced.md`
- Synthesized user profile (Layer 3): `skill/skills/skill-system-soul/profiles/<user>.md`

The synthesis step should preserve the 6-section format used by `balanced.md`:

1. Identity
2. Decision Heuristics
3. Communication Style
4. Quality Bar
5. Tool Preferences
6. Anti-Patterns

## Storage Pattern (agent_memories)

Example SQL templates (copy/paste and substitute values):

```sql
-- Store a facet
SELECT store_memory(
  'episodic',
  'insight-facet',
  ARRAY['session:ses_xxx', 'user:arthu'],
  'Session Facet: <brief_summary>',
  '<full facet YAML as text>',
  '{"session_type": "...", "outcome": "..."}',
  'insight-agent',
  'ses_xxx',
  5.0
);

-- Store/update matrix state
SELECT store_memory(
  'semantic',
  'soul-state',
  ARRAY['user:arthu', 'matrix'],
  'Soul State: arthu',
  '<full soul-state YAML as text>',
  '{"total_insights": 0, "last_updated": "..."}',
  'insight-agent',
  NULL,
  9.0
);

-- Query recent facets
SELECT * FROM search_memories('insight-facet user:arthu', NULL, NULL, NULL, NULL, 0.0, 50);
```

## Operational Notes

- Facet extraction should be completable in one pass. If you cannot justify an adjustment with concrete evidence, propose no adjustment.
- Users may communicate in Chinese; treat that as a signal about comfort, not as a personality dimension.
- Keep values clamped to [0.0, 1.0].

```skill-manifest
{
  "schema_version": "2.0",
  "id": "skill-system-insight",
  "version": "1.0.0",
  "capabilities": ["insight-extract", "insight-matrix-update", "insight-synthesize"],
  "effects": ["db.read", "db.write", "fs.write"],
  "operations": {
    "extract-facets": {
      "description": "Extract a per-session facet from transcript. Rate limited to 3/24h per user.",
      "input": {
        "session_id": { "type": "string", "required": true, "description": "Session to analyze" },
        "user": { "type": "string", "required": true, "description": "User handle" }
      },
      "output": {
        "description": "Facet YAML stored to agent_memories",
        "fields": { "status": "ok | error", "memory_id": "integer" }
      },
      "entrypoints": {
        "agent": "Follow scripts/extract-facets.md procedure (no executable script)"
      }
    },
    "update-matrix": {
      "description": "Update dual matrix from stored facet with confidence gating.",
      "input": {
        "user": { "type": "string", "required": true, "description": "User handle" }
      },
      "output": {
        "description": "Updated soul-state YAML stored to agent_memories",
        "fields": { "status": "ok | error", "values_changed": "boolean" }
      },
      "entrypoints": {
        "agent": "Follow scripts/update-matrix.md procedure"
      }
    },
    "synthesize-profile": {
      "description": "Regenerate Layer 3 Soul profile from matrix + recent facets.",
      "input": {
        "user": { "type": "string", "required": true, "description": "User handle" }
      },
      "output": {
        "description": "User profile written to skill-system-soul/profiles/<user>.md",
        "fields": { "status": "ok | error", "profile_path": "string" }
      },
      "entrypoints": {
        "agent": "Follow scripts/synthesize-profile.md procedure"
      }
    }
  },
  "stdout_contract": {
    "last_line_json": false,
    "note": "Agent-executed procedures; output is structured YAML stored to DB, not stdout."
  }
}
```
