---
name: codex-plan
description: Create detailed implementation plan using Codex 5.3 with xhigh reasoning
user_invocable: true
argument_hint: "<what you want to plan>"
---

# Codex Plan Skill

You are being asked to create a detailed implementation plan using Codex. Your job is to:
1. Understand the user's planning request (shown below as `ARGUMENTS:`)
2. Ask clarifying questions using AskUserQuestion
3. Craft an excellent, detailed prompt for Codex
4. Execute Codex to generate and save the plan

**Always uses:** `gpt-5.3-codex` with `xhigh` reasoning
**Output:** `codex-plan.md` in current directory

---

## Step 1: Analyze the Request

The user's planning request appears at the end of this instruction as `ARGUMENTS: <request>`.

Identify:
- What is the core goal?
- What technology/domain is involved?
- What aspects are ambiguous or underspecified?
- What decisions would significantly impact the plan?

### Fast-path (Trivial Tasks)

If the task is extremely trivial — single file config change, typo fix, <2 files affected, no architectural decisions — **skip Codex**. Write `codex-plan.md` yourself directly with a simplified structure:

```markdown
# Plan: [Task Name]
**Generated**: [Date]
**Estimated Complexity**: Low
## Overview
[1-2 sentences]
## Task
- **Location**: [file path]
- **Description**: [what to do]
- **Acceptance Criteria**: [testable criteria]
```

Even on fast-path, **still ask at least 1 clarifying question** (Step 2) before writing the plan. After writing, skip to Step 6 (Verify Output).

---

## Step 2: Ask Clarifying Questions (REQUIRED)

**Use AskUserQuestion tool** to ask **1-5** targeted questions before generating the plan.

Evaluate task ambiguity first:
- **Simple/clear tasks** (well-defined scope, obvious approach) → ask **1-2** questions
- **Complex/ambiguous tasks** (multiple approaches, unclear requirements) → ask **3-5** questions
- **Never 0** — always ask at least 1 question to confirm understanding

Good clarifying questions:
- Narrow down scope and requirements
- Clarify technology choices
- Understand constraints (time, budget, team size)
- Identify must-haves vs nice-to-haves
- Uncover integration requirements
- Determine security/compliance needs

### Example Question Patterns

**For "implement auth":**
- What authentication methods? (email/password, OAuth, SSO, magic links)
- RBAC or just authenticated/unauthenticated?
- Backend stack? (Node/Express, Python/Django, etc.)
- Session storage? (Database, Redis, JWT stateless)
- Features needed? (password reset, email verification, 2FA)
- Compliance requirements? (SOC2, GDPR, HIPAA)

**For "build an API":**
- What resources/entities to manage?
- REST or GraphQL?
- Authentication method?
- Expected scale/traffic?
- Rate limiting, caching, versioning?

**For "fix a bug":**
- How to reproduce reliably? (steps, environment, frequency)
- Expected vs actual behavior?
- Related test coverage? (existing tests that should have caught this)
- Affected platforms/browsers/environments?

**For "refactoring":**
- Must external API/interface remain compatible?
- Existing test coverage to rely on?
- Performance constraints? (must not regress)
- Incremental or big-bang? (can we merge partial progress?)

**For "infrastructure/DevOps":**
- Target environment? (local, staging, production)
- Existing CI/CD pipeline?
- Secrets management approach?
- Rollback requirements? (blue-green, canary, instant)

---

## Step 3: Locate Target Files

**You are the Product Manager and Locator.** Your job is to FIND the relevant files, NOT to plan the implementation.

After getting answers, discover:
- **Entry points**: main files, CLI entry, route handlers
- **Files to modify**: specific files the task will touch
- **Key imports/dependencies**: modules these files depend on
- **Existing patterns**: naming conventions, error handling style, architecture

Produce a `## Target Files` list for the Codex prompt:

```
## Target Files to Read
- `src/auth/login.ts` — current login handler, will be modified
- `src/middleware/session.ts` — session middleware, imports from login
- `src/types/user.ts` — User type definition, dependency
```

**Do NOT summarize file contents** — just list paths with one-line purpose. Codex will read them in full via `<context_loading>`.

---

## Step 4: Craft the Codex Prompt

Create a detailed prompt that includes:
1. **Clear objective** — What plan needs to be created
2. **All requirements** — Everything learned from clarifying questions
3. **Constraints** — Technology choices, timeline, team size
4. **Target Files** — The file paths list from Step 3
5. **Plan structure** — Read from `references/plan-template.md` and inject its full content
6. **Output instructions** — Write to `codex-plan.md` in current directory

**CRITICAL:** Tell Codex to NOT ask any clarifying questions — it has all the information it needs and should just write the plan and save the file.

**Adaptive template:** For minor/trivial tasks, tell Codex it MUST omit irrelevant sections (Phases, E2E Tests, Rollback) and may output a flat task list instead, to comply with `<output_verbosity_spec>`.

### Example Codex Prompt

```
Create a detailed implementation plan for [TASK DESCRIPTION].

## Requirements
- [Requirement 1 from clarifying questions]
- [Requirement 2]
- [Requirement 3]
- NOT needed: [Things explicitly excluded]

## Target Files to Read
- `[path/to/file1]` — [one-line purpose]
- `[path/to/file2]` — [one-line purpose]
- `[path/to/file3]` — [one-line purpose]

## Plan Structure

Read and follow the exact template structure from `references/plan-template.md`.

Adapt the template to task complexity:
- For minor tasks, OMIT irrelevant sections (e.g., multiple Phases, E2E Tests, Rollback) and use a flat task list instead.
- For complex tasks, use the full phased structure with all sections.

## Behavioral Constraints

<output_verbosity_spec>
- Default: 3-6 sentences or <=5 bullets for typical answers.
- Simple yes/no questions: <=2 sentences.
- Complex multi-step or multi-file tasks:
  - 1 short overview paragraph
  - then <=5 bullets tagged: What changed, Where, Risks, Next steps, Open questions.
- Avoid long narrative paragraphs; prefer compact bullets and short sections.
- Do not rephrase the user's request unless it changes semantics.
</output_verbosity_spec>

<design_and_scope_constraints>
- Implement EXACTLY and ONLY what the user requests.
- No extra features, no added components, no UX embellishments.
- Style aligned to the design system at hand.
- Do NOT invent colors, shadows, tokens, animations, or new UI elements unless requested or necessary.
- If any instruction is ambiguous, choose the simplest valid interpretation.
</design_and_scope_constraints>

<context_loading>
- Start by reading ALL files listed in "Target Files to Read" — in full, not just the sections mentioned in the task.
- Then expand to key files they import from or that depend on them.
- Absorb surrounding patterns, naming conventions, error handling style, and architecture before writing any code.
- Do not ask clarifying questions about things that are answerable by reading the codebase.
</context_loading>

## Instructions
- Write the complete plan to a file called `codex-plan.md` in the current directory
- Do NOT ask any clarifying questions - you have all the information needed
- Be specific and actionable - include code snippets where helpful
- Follow test-driven development: specify what tests to write BEFORE implementation
- Identify task dependencies so parallel work is possible
- Just write the plan and save the file

Begin immediately.
```

---

## Step 5: Execute Codex (REQUIRED)

Run this exact command with your crafted prompt:

```bash
codex exec --full-auto --skip-git-repo-check \
  -c model=gpt-5.3-codex \
  -c model_reasoning_effort=xhigh \
  -c model_reasoning_summary=concise \
  --output-last-message /tmp/codex-plan-result.txt \
  "YOUR_CRAFTED_PROMPT_HERE"
```

Then show the results:
```bash
cat /tmp/codex-plan-result.txt
```

---

## Step 6: Verify Output (REQUIRED)

After Codex finishes (or after writing the plan yourself on fast-path):

1. **Read** the generated `codex-plan.md`
2. **Check structure**: file exists, is valid Markdown, contains at minimum:
   - `# Plan:` heading
   - `## Overview` section
   - At least one `### Task` entry
3. **If checks fail** OR `codex exec` returned an error/timeout:
   - Adjust the prompt (simplify requirements, fix ambiguities)
   - Retry execution **once**
4. **If retry also fails**: show the error to the user and explain what went wrong
5. **If checks pass**: show the plan results to the user

---

## Important Rules

1. **ALWAYS ask at least 1 clarifying question** — Do not skip Step 2 (1-5 questions based on complexity)
2. **ALWAYS use gpt-5.3-codex with xhigh reasoning** — No exceptions (unless fast-path)
3. **ALWAYS tell Codex not to ask questions** — It should just execute
4. **ALWAYS use --full-auto flag**
5. **ALWAYS verify output in Step 6** — Check structure, retry once on failure
6. **Output file**: `codex-plan.md` in current working directory

---

## Now Execute

The user's planning request is shown as `ARGUMENTS:` below. Analyze it and begin with Step 1.
