---
name: skill-design
description: Design and refactor Agent Skills with concise, high-signal instructions and explicit trigger metadata. Use when creating a new skill, revising SKILL.md/README.md structure, or improving skill discoverability and portability.
license: MIT
metadata:
  author: shihyuho
  version: "1.4.0"
---

# Skill Design

Design skills as reusable behavior systems that are easy to discover and execute.

## Trigger Contract

Use this skill when users ask to:

- create a new skill
- refactor an existing skill
- improve trigger quality or discoverability
- align `SKILL.md`, `README.md`, and `references/`
- remove ambiguity or conflicting guidance

Typical trigger phrases:

- "create a skill for X"
- "design a new skill"
- "refactor this skill"
- "make this skill reusable"
- "align README and SKILL behavior"

## Core Principles

- Optimize for reliable agent behavior, not document aesthetics.
- Make trigger conditions explicit and searchable.
- Keep instructions executable and verifiable.
- Avoid implicit project context unless explicitly required.

## Writing Style Rules

- Use imperative voice.
- Keep sections short and high-signal.
- Prefer concrete constraints over abstract advice.
- Use `MUST`/`NEVER` for true invariants (safety, correctness, irreversible failure).
- For normal guidance, use direct action verbs and clear defaults.
- Avoid weak modal wording for hard rules (`should`, `could`, `may`, `consider`, `usually`).
- Remove narrative text that does not change execution.

## Metadata and Discovery

- Write frontmatter `description` in third person.
- Include both what the skill does and when to use it.
- Keep trigger terms concrete (`file type`, `task type`, `user phrasing`).
- Do not put workflow details in `description`; keep those in the body.

## Workflow

### Phase 1 - Define Contract

1. Define who uses the skill and when it triggers.
2. Define non-negotiable behavior and failure boundaries.
3. Define deterministic vs heuristic decisions.

### Phase 2 - Structure Content

1. Write trigger and constraints first.
2. Keep `SKILL.md` as execution logic and decision constraints.
3. Move bulky detail to `references/` and keep one source of truth per schema.
4. Add `scripts/` only for repeatable deterministic operations.
5. When composing with other skills, invoke them by name and never copy their instruction bodies.

### Phase 3 - Author/Refactor SKILL

1. Tighten description and trigger wording.
2. Convert soft guidance into explicit, executable instructions.
3. Provide one default path first; add alternatives only when necessary.
4. Remove duplicate or contradictory instructions.

### Phase 4 - Align README (Human-Facing)

1. Keep README value-first: problem -> value -> example -> activation.
2. Treat `README.md` as style charter for future AI output quality.
3. Keep implementation internals out of README.
4. Keep claims behavior-accurate.

### Phase 5 - Validate

1. Run available validator for your environment.
2. If no validator exists, run manual consistency checks.
3. Confirm no repository-specific assumptions remain unless explicitly intended.

## Progressive Disclosure Rules

- Keep `SKILL.md` body compact (target under 500 lines).
- Put advanced or domain-specific detail in `references/`.
- Link reference files directly from `SKILL.md` (avoid deep nested references).
- For long reference files (100+ lines), add a short table of contents.

## README Rules

- In this skill, `README.md` means the skill-level README (for example `skills/<skill-name>/README.md`), not the repository root README.
- `README.md` is not required by Agent Skills Specification.
- `README.md` is recommended for faster human understanding and adoption.
- Keep README focused on outcomes, style expectations, and activation cues.

## Anti-Patterns

- Hardcoded local paths as universal defaults.
- Tool lock-in with no fallback path.
- Copying external skill instruction bodies instead of invoking the source skill.
- Workflow summary inside frontmatter `description`.
- Duplicated schema definitions across files.
- Long narrative prose with no executable instruction.
- Repeating `MUST`/`NEVER` for non-critical guidance.
- Offering too many equivalent options without a default recommendation.

## Done Checklist

- `SKILL.md` has explicit trigger contract and executable workflow.
- Frontmatter `description` clearly states what + when.
- `README.md` defines style expectations for future contributions.
- `references/` contains heavy details only when needed.
- No stale terms, duplicated schema ownership, or contradictory rules.
- Validation evidence is recorded (tool-based or manual).
- Example validation command: `npx --yes skills-ref validate ./skills/<skill-name>`.

## See Also

- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
