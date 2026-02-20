---
name: ticket-creator
description: >-
  This skill should be used when the user asks to "create a ticket",
  "create a Linear ticket", "make a ticket", "write a ticket",
  "create an issue", "file a bug", "create a feature ticket",
  "write a bug report", "I need a ticket for...", "there's a bug in...",
  "turn this into a ticket", "write this up as a ticket",
  or wants to create any Linear issue for implementation.
version: 1.0.0
allowed_tools:
  - AskUserQuestion
  - Task
  - TaskCreate
  - TaskList
  - TaskGet
  - TaskUpdate
  - mcp__claude_ai_Linear__create_issue
  - mcp__claude_ai_Linear__list_issues
  - mcp__claude_ai_Linear__get_issue
  - mcp__claude_ai_Linear__list_teams
---

# Ticket Creator

Create well-structured Linear tickets optimized for AI agent (Claude Code) implementation. Follow a pattern-first, template-driven workflow that ensures the implementing agent can plan and execute without making open-ended architectural decisions. Consult `references/guidelines.md` for detailed quality criteria and writing guidelines.

## Core Principle: Pattern-First

The strongest predictor of ticket success is whether the implementing agent can copy-and-adapt from an existing pattern. Every ticket MUST reference an existing code pattern or explicitly flag it as a first-time pattern requiring extra specification.

## AskUserQuestion Usage

Only invoke `AskUserQuestion` when the answer cannot be deduced from the current conversation context, the codebase, or prior responses. If the information is available or can be inferred, proceed without asking. This applies to all stages — classification, deduplication, information gathering, anti-pattern resolution, splitting, and confirmation.

## Workflow

Use `TaskCreate` at the start to plan the workflow steps, and `TaskUpdate` to mark each step as you complete it. This keeps progress visible and survives `/compact`.

### 1. Gather Context & Classify

Extract as much information as possible from the current conversation before asking any questions. If work has been discussed, use that context to pre-fill ticket details.

Classify the ticket:
- **Normal** (feature, improvement, refactor) → `references/template-normal.md`
- **Bug** (error, broken behavior) → `references/template-bug.md`

Identify the domain from context or keywords:

| Domain | Keywords |
|--------|----------|
| UI | page, component, layout, frontend, table, form, modal, sidebar |
| Backend | server action, API, endpoint, database, schema, query, migration, job |
| Data-Engine | harvester, actor, pipeline, scraper, PDF, Python, data-engine |

If classification is ambiguous, use `AskUserQuestion` to clarify.

### 2. Check for Duplicates

Use `Task` with subagent_type `general-purpose` to search Linear for existing similar tickets. Instruct the sub-agent to call `list_issues` with relevant search terms and return only: issue ID, title, URL, and a one-sentence summary per match. This prevents the raw `list_issues` payload from polluting the main context.

If a matching ticket exists, surface it and ask whether to proceed or update the existing ticket.

### 3. Load Template & Gather Information

Load the appropriate template from `references/`. Gather missing required information conversationally, 1-2 questions at a time, in this priority order:

1. What are we building/fixing and why? What's the scope?
2. Is there an existing pattern to follow? (**most critical**)
3. Technical details — types, contracts, file paths
4. Side effects, integration points, permissions
5. Acceptance criteria and verification hints

For **bug tickets**: if a Sentry issue ID or URL is available, use `Task` with subagent_type `general-purpose` to fetch the Sentry error details. Instruct the sub-agent to return only the fields needed for the ticket: error message, affected file/line, root cause (if determinable), frequency/user impact, and any relevant breadcrumbs. See `references/template-bug.md` for the full field list. This prevents verbose Sentry payloads (stack traces, raw breadcrumbs) from flooding the main context.

### 4. Pattern Discovery

Use `Task` with subagent_type `Explore` to search the codebase for:
- Existing implementations to reference as patterns
- Relevant Claude Code skills (scan `.claude/` directories for `SKILL.md` files)

Include discovered patterns in the ticket's "Existing pattern to follow" field. Include discovered skills in the Implementation Toolkit section using the format: `skills: [skill-name-1, skill-name-2]`

### 5. Quality Gate

Run all anti-pattern checks from `references/anti-patterns.md`. Surface any warnings and resolve them with the user before proceeding.

Evaluate whether the ticket should be **split** (see Ticket Splitting below).

### 6. Draft & Confirm

Compile the ticket using the loaded template. Present a **concise preview** — title, summary, key fields, acceptance criteria — not the full ticket body.

Ask the user to confirm or request changes before creating.

### 7. Create in Linear

Create the ticket using `create_issue` with: team ("Sylla Tech"), title, description, priority. Only set assignee if the user specifies one.

If dependencies exist, use `blockedBy` or `blocks` fields. Link related tickets found during deduplication using `relatedTo`.

Share the ticket link with the user after creation.

## Ticket Splitting

When splitting, use `TaskCreate` with `blockedBy` to model the dependency order between split tickets (e.g., backend before UI). Use `TaskList` to review progress and `TaskUpdate` to track each ticket through stages 3-7.

### Multi-Category Split

If work spans multiple domains (e.g., UI + Backend + Data-Engine), create separate linked tickets — one per domain. Run stages 3-7 for each, carrying forward shared context (priority, description, related tickets). Cross-link tickets using `relatedTo`.

### File-Based Split

If a ticket would modify more than **8 files**, suggest splitting into smaller, focused tickets. Each split ticket should be independently implementable.

## Title Conventions

| Type | Format |
|------|--------|
| Feature | `Implement [thing] for [purpose]` |
| UI Page | `Create [page name] page at [route]` |
| UI Component | `Add [component] to [location]` |
| API/Endpoint | `Add [method] [endpoint] endpoint` |
| Refactor | `Refactor [what] to [improvement]` |
| Bug | `Fix [symptom] in [location]` |

## Reference Files

| File | Purpose |
|------|---------|
| `references/template-normal.md` | Template for features, improvements, refactors (with conditional UI/Backend/Data-Engine sections) |
| `references/template-bug.md` | Template for bug fixes (with Sentry MCP integration) |
| `references/anti-patterns.md` | Anti-pattern detection rules to run before ticket creation |
| `references/guidelines.md` | Quality criteria, writing guidelines, and verification rules |
| `references/layout-patterns.md` | UI layout pattern decision table and component reference |

## Example Tickets

Consult these real ticket examples to calibrate structure and detail level:

| Example | Domain | Based On |
|---------|--------|----------|
| `examples/backend-ticket.md` | Backend (server action + API) | S-1176 |
| `examples/bug-ticket.md` | Bug fix (root cause known) | S-1222 |
| `examples/data-engine-ticket.md` | Data-engine harvester | S-1149 |
| `examples/ui-ticket.md` | UI page creation | S-1163 |

## Quality Test

Before creating, verify: *"Could the implementing agent create a complete plan from this ticket without making any open-ended architectural decisions?"*

If the answer is no, identify what's ambiguous and ask for it. See `references/guidelines.md` for the full quality checklist.
