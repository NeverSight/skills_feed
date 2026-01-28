---
name: router-template
description: Template for creating router skills. Use as a starting point when building a new router that dispatches to multiple specialized skills. Copy and customize for your domain.
---

# [Domain] Router

Routes to N specialized skills based on task requirements.

## Routing Protocol

1. **Classify** — Identify primary task type from user request
2. **Match** — Find skill(s) with highest signal match
3. **Combine** — Most production tasks need 2-4 skills together
4. **Load** — Read matched SKILL.md files before implementation

## Quick Route

### Tier 1: Core (Always Consider)
| Task Type | Skill | Primary Signal Words |
|-----------|-------|---------------------|
| [task] | `skill-name` | word1, word2, word3 |

### Tier 2: Enhanced (Add When Needed)
| Task Type | Skill | Primary Signal Words |
|-----------|-------|---------------------|
| [task] | `skill-name` | word1, word2, word3 |

### Tier 3: Reference Only
| Task Type | Skill | Primary Signal Words |
|-----------|-------|---------------------|
| [task] | `skill-name` | word1, word2, word3 |

## Signal Matching Rules

### Priority Order
When multiple signals present, resolve by priority:
1. **Explicit framework** — React/Vue/vanilla overrides generic signals
2. **Specific feature** — "multi-step wizard" beats generic "form"
3. **Platform constraint** — mobile/VR/accessibility takes precedence
4. **Default tier** — Fall back to Tier 1 core skills

### Confidence Scoring
- **High (3+ signals)** — Route immediately
- **Medium (1-2 signals)** — Route with Tier 1 defaults
- **Low (0 signals)** — Ask user for clarification

## Common Combinations

### [Scenario Name] (N skills)
```
skill-1 → [what it provides]
skill-2 → [what it provides]
skill-3 → [what it provides]
```
Wiring: [one-line integration summary]

### [Scenario Name] (N skills)
```
skill-1 → [what it provides]
skill-2 → [what it provides]
```
Wiring: [one-line integration summary]

## Decision Table

| Framework | Scale | Features | Route To |
|-----------|-------|----------|----------|
| React | Standard | Auth form | skill-a + skill-b + skill-c |
| Vue | Standard | Data entry | skill-a + skill-d |
| None | Simple | Basic form | skill-e + skill-b |
| Any | Complex | Wizard | skill-f + skill-a + skill-b |

## Fallback Behavior

- **Unknown framework** → Use skill with broadest compatibility
- **No clear signals** → Ask: "What framework?" and "What's the core requirement?"
- **Conflicting signals** → Prefer Tier 1 skills, ask for clarification on Tier 2

## Reference

See `references/integration-guide.md` for:
- Complete wiring patterns
- Code examples for all combinations
- Architecture diagrams
- Edge case handling
