---
name: ensemble-team
description: >
  Set up a full AI ensemble/mob programming team for any software project. Creates
  team member profiles (.team/), coordinator instructions (harness-specific config
  file), project owner constraints (PROJECT.md), team agreements (TEAM_AGREEMENTS.md),
  domain glossary, and supporting docs. Use when: (1) starting a new project and
  wanting a full expert agent team, (2) the user asks to "set up a team", "create a
  mob team", "set up ensemble programming", or "create agent profiles", (3) converting
  an existing project to the driver-reviewer mob model, (4) the user wants AI agents
  to work as a coordinated product team with retrospectives and consensus-based
  decisions.
license: CC0-1.0
metadata:
  author: jwilger
  version: "1.0"
  requires: []
  context: []
  phase: build
  standalone: true
---

# Ensemble Team Setup

Set up an AI ensemble programming team for any software project. Creates the full
structure for a team of expert agents working in a single-driver mob programming style
with consensus-based decisions, TDD, and continuous retrospectives.

## Workflow

### Phase 1: Project Discovery

Gather essential project information. Ask the user:

1. **Project name and description**: What is being built? What problem does it solve?
2. **Tech stack**: Language, framework, database, frontend approach, testing tools.
   If unsure, help them decide based on their goals.
3. **Product vision**: Target user? MVP scope? Vague ideas are fine — the Product
   Manager agent will refine them.
4. **Dev environment**: Nix? Docker? Standard package managers? CI provider?
5. **Repository**: Existing repo or new? Branching strategy?

### Phase 2: Team Composition

Determine the right team.

**PREREQUISITE**: Read `references/role-catalog.md` before proceeding.

#### Tiered Team Presets

Start with a preset, then adjust based on project needs. The team formation session
(Phase 5) helps determine the right fit. The user may modify any preset.

| Preset | Size | Composition |
|--------|------|-------------|
| **Full** | ~9 | 1 Product Manager, 1 UI/UX Designer, 1 Accessibility Specialist, 1 Domain SME, 1 QA Analyst, 4 Software Engineers |
| **Lean** | ~5-6 | 1 Product Manager, 1 Domain SME, 1 Dev Practice Lead, 2-3 Software Engineers, 1 flex role (UX, QA, or DevOps based on need) |
| **Solo-plus** | ~3 | 1 Domain SME, 1 Dev Practice Lead, 1 Software Engineer |

**Approximate token costs per discussion round**:
- **Solo-plus** (~3 agents): Lightweight. ~5-10K tokens per round.
- **Lean** (~5-6 agents): Moderate. ~15-25K tokens per round.
- **Full** (~9 agents): Heavy. ~30-50K tokens per round. Reserve for projects
  where the governance overhead pays for itself.

Actual costs depend on model, context length, and discussion complexity. These
are rough estimates for setting expectations, not precise accounting.

**Selecting a preset**: Ask the user about project scope, timeline, and complexity.
Solo-plus suits focused tasks or spikes. Lean suits most projects. Full suits
large-scope products with UI, accessibility, and quality requirements.

**Extend, do not replace**: These presets build on the role catalog. See the catalog
for conditional roles (Security, Data/ML, API Specialist, etc.) that can augment any
preset. Odd numbers preferred for tie-breaking.

**Research each expert — do NOT pick from a memorized list.** For each role:
1. Identify the specific technology/domain this project needs
2. Use WebSearch to find the recognized authority — the person who wrote the book,
   created the tool, or gave the defining talks for that specific area
3. Verify their credentials, recent work, and relevance to this project
4. Evaluate: published authority, distinctive voice, practical experience,
   complementary perspective to other team members

Present each proposed expert with: name, credentials, key published work, why they
fit THIS project, and what they'd focus on. Let user approve, swap, or remove.

### Phase 3: Generate Team Profiles

Create `.team/<name>.md` for each member.

**PREREQUISITE**: Read `references/profile-template.md` before proceeding.

Required sections: Opening bio, Role, Core Philosophy (5-8 principles from their
published work), Technical Expertise (6-12 items), On This Project (concrete
guidance), Communication Style (personality + 4-6 characteristic phrases), Mob
Approach, Code Review Checklist (6-12 checks), Lessons (empty, to be updated).

**Quality gates**: Profile must not be interchangeable with another expert. Must
include project-specific guidance. Must capture their distinctive voice.

#### AI-Approximation Disclaimer

Every profile MUST include the following disclaimer block immediately after the
opening biography paragraph:

```
> **AI-Approximation Notice**: This profile is an AI-generated approximation inspired
> by [Name]'s published work, talks, and writings. The real [Name] has not endorsed
> or reviewed this profile. All outputs should be verified against their actual
> published work. This profile creates a "diversity of heuristics" drawing on their
> known perspectives — it does not simulate the actual person.
```

#### AI Self-Awareness Clause

Each profile must include in the "Your Role on This Team" section a statement that
the team member is aware it is an AI agent embodying a perspective, not the actual
person. Human time constraints are irrelevant to AI agents. Standing aside on a
decision when the topic falls outside the role's expertise is appropriate deference,
not disapproval.

#### Compressed Active-Context Form

Each profile MUST include a `## Compressed Context` section at the end: a dense
summary of the profile in **under 500 tokens** covering role, top 3-5 principles,
key expertise areas, and characteristic review focus. This compressed form is loaded
during discussion and review phases. The full profile is loaded only when the member
is actively driving or navigating code.

### Phase 4: Generate Project Scaffolding

#### Coordinator Instructions (harness config file)

**PREREQUISITE**: Read `references/coordinator-template.md` before proceeding.

Fill in roster, build tools, team size. Place in the harness-specific config
file (e.g., `CLAUDE.md` for Claude Code, `.cursorrules` for Cursor, project
instructions for other harnesses). This file is for the coordinator only.

#### PROJECT.md

**PREREQUISITE**: Read `references/project-template.md` before proceeding.

Fill in tech stack, scope (Must/Should/Could/Out), dev mandates, environment.

#### TEAM_AGREEMENTS.md — Skeleton Only
Create a **skeleton** `TEAM_AGREEMENTS.md` with section headers but NO pre-filled
agreements. The team writes their own agreements during the formation session (Phase 5).

#### Supporting docs

- **docs/glossary.md**: Domain glossary skeleton (Core Types table, Actions table,
  Errors table, Type Design Principles)
- **docs/deferred-items.md**: Tracker table (Item | Category | Source | Severity | Status)
- **docs/future-ideas.md**: Parking lot for out-of-scope ideas

### Phase 5: Team Formation Session

This is the critical phase. The team debates and reaches consensus on their own
working agreements.

**PREREQUISITE**: Read `references/team-agreements-template.md` before proceeding.

**How it works**: The coordinator activates the full team, then presents each discussion
topic (from the reference file) one at a time. The team debates, proposes approaches,
and reaches consensus. The Driver records the agreed-upon norms in
`TEAM_AGREEMENTS.md`.

**The 10 topics** (non-exhaustive — team may add more):
1. How do we decide what to build?
2. How does the Driver-Reviewer mob model work?
3. When is a piece of work "done"?
4. What is our commit and integration pipeline?
5. How do we resolve disagreements?
6. What are our code conventions?
7. When and how do we hold retrospectives?
8. What are our architectural principles?
9. How do we communicate as a team?
10. What tooling and repository conventions do we follow?

Each topic includes the **problem** it addresses and **sub-questions** to guide
discussion. The team's answers become their agreements — not pre-canned templates.

### Phase 6: Configure Permissions

Grant team agents the permissions they need to do their work (file editing, shell
access, etc.). How this is configured depends on the harness:

- **Claude Code**: Create/update `.claude/settings.json` with `"allow": ["Edit", "Write", "Bash(*)"]`
- **Cursor/Windsurf**: Configure tool permissions in the IDE settings
- **Other harnesses**: Follow the harness documentation for agent permission grants

### Phase 7: Configure CI

Add `paths-ignore` rules to CI config for any harness-generated session or transcript
directories (e.g., `.claude-sessions/` for Claude Code) to prevent them from triggering
CI runs.

### Phase 8: Summary

Present: files created, how to start the team (the coordinator reads CLAUDE.md and
activates the team), suggest telling the coordinator what to build.

## Retrospective Protocol

Retrospectives are event-driven, not time-based. AI agents work continuously —
arbitrary intervals are meaningless.

- **Trigger**: After each shipped PR (merged to the integration branch).
- **Participants**: The team that did the work, while they still have context.
- **Format**: The team reflects on what worked, what did not, and suggests process
  improvements. Any structured format (Start/Stop/Continue or equivalent) is fine
  as long as it produces concrete suggestions.
- **Output**: Retrospective suggestions are SUGGESTIONS only. They require explicit
  human approval before adoption.
- **Boundary**: The team does NOT self-modify its own agreements, profiles, or
  process documents. The human reviews suggestions and decides what to adopt.
  Approved changes are then applied by the team at the human's direction.
- **Mini-retros** after each CI build remain a lightweight checkpoint (did we follow
  the pipeline? was the commit atomic?) and do not require human approval.

## Key Principles

Non-negotiable aspects baked in from production experience.

**PREREQUISITE**: Read `references/lessons-learned.md` before proceeding.

- Consensus before push (review locally, then push)
- Refactor step is mandatory every commit
- CI wait rule (never queue multiple CI runs)
- Mini-retro after every CI build (team runs it, not coordinator)
- PR-triggered retrospective with human-approved outputs
- Driver handoff protocol (summary + git log + green baseline)
- Glossary compliance (domain types match glossary)
- Deferred items tracked immediately
- Reviewer coordination (check others' reviews first)
- Explicit Driver onboarding in activation prompts
- Session transcripts excluded from CI triggers
- AI-approximation disclaimer on every profile
- Compressed active-context form on every profile
- Stand-aside means deference, not disapproval
