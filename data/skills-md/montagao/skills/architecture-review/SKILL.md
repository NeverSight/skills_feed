---
name: architecture-review
description: Review system architecture with an indie hacker lens - bias toward shipping, YAGNI/KISS, fewer moving parts. Invoke as "/architecture-review [path/to/plan]" to roast a plan directory containing overview.md, phases/, and reference/ docs. Use when asked to "review architecture", "roast my design", "check for over-engineering", or "simplify this system".
allowed-tools: Read, Glob, Grep, WebSearch
---

# Architecture Review

Battle-tested indie hacker review of system designs. Roast kindly, score 0-100, and ship faster.

## Perspective

Use industry standards and established patterns as baseline, but bias hard toward:
- **YAGNI/KISS** - Don't build what you don't need yet
- **Fewer moving parts** - Every component is a liability
- **Lower ops burden** - Sleep > uptime dashboards at 3am
- **Faster iteration** - Ship, learn, adapt

## Process

1. **Read the plan** - Glob for `overview.md`, `phases/**/*.md`, `reference/**/*.md` (or similar structure)
2. **Score it 0-100** - Based on meeting requirements without over-engineering
3. **Call out over-engineering** - Name specific components that are too complex
4. **Suggest simpler alternatives** - With explicit tradeoffs
5. **Find library/tool substitutes** - What can you buy instead of build?
6. **List risks and gaps** - What's missing? What will bite you?
7. **Provide action plan** - Do now / next / later

## Review Template

Structure the review as:

```markdown
## Score: XX/100

[One-line verdict]

## Over-Engineering Alerts 🚨

| Component | Problem | Simpler Alternative | Tradeoff |
|-----------|---------|---------------------|----------|
| ... | ... | ... | ... |

## Buy Don't Build 🛒

| Custom Solution | Replace With | Why |
|-----------------|--------------|-----|
| ... | ... | ... |

## Risks & Gaps ⚠️

1. **[Risk]**: [Impact + likelihood]
2. ...

## What's Missing 📋

- [ ] ...

## Action Plan

### Do Now (blocks everything)
- ...

### Do Next (this sprint)
- ...

### Do Later (or never)
- ...

## Detailed Notes

[Section-by-section feedback on phases/components]
```

## Scoring Rubric

- **90-100**: Ship it. Minimal changes needed.
- **70-89**: Solid foundation, some fat to trim.
- **50-69**: Good ideas buried under complexity. Needs simplification pass.
- **30-49**: Rube Goldberg machine. Step back and rethink.
- **0-29**: Start over with requirements, not solutions.

## Red Flags to Watch For

- Microservices for < 5 engineers
- Kafka/queues when a cron job works
- GraphQL for a single client
- Custom auth instead of Clerk/Auth0/Supabase
- Custom CMS instead of headless options
- K8s when a single VPS works
- Event sourcing for CRUD apps
- "Future-proofing" for hypothetical scale
- Multiple databases when one Postgres does it
- Custom job queues when BullMQ/Inngest/Trigger.dev exist

## Good Signs

- Boring technology choices
- Managed services over self-hosted
- Monolith until proven otherwise
- SQLite/Postgres as default
- Feature flags for rollout, not architecture
- Clear boundaries, minimal abstraction layers

## Instructions

<instructions>$ARGUMENTS</instructions>
