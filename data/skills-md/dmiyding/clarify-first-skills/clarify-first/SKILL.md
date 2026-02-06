---
name: clarify-first
description: Use this skill when a request is ambiguous/underspecified, contains conflicts, or has high-impact consequences. The agent must do a quick risk triage (low/medium/high). For low-risk work, proceed with explicit assumptions and reversible steps. For medium/high-risk or conflicting requirements, pause execution, summarize context, list uncertainties, ask targeted clarification questions (with choices), and get confirmation before irreversible actions (writing files, running commands, deleting data, deploying, messaging, spending money). If a better solution exists, propose it and ask the user to choose.
---

# Clarify First (Agent Skill)

This skill prevents “guess-and-run”. It is a *meta* workflow skill: when requirements are unclear or conflicting, the agent must align with the user before acting.

Language rule:
- Match the user’s language. If the user writes Chinese, you may ask questions in Chinese.
- For Chinese phrasing templates, see `references/zh-CN.md`.

## When to Activate

Activate when **any** of these are true:

1. **Ambiguity**: unclear terms (“optimize it”, “make it similar”, “ASAP”, “just fix it”), missing definition of “done”, vague scope, unclear deliverables.
2. **Missing constraints**: no target platform/version, no file paths, no acceptance criteria, no performance/security/UX constraints, no deadline/priority tradeoffs.
3. **Conflicts**: requirements contradict (“no breaking changes” + “refactor everything”), budget/time vs quality, “keep minimal diff” + “major redesign”.
4. **High-impact / irreversible actions** requested: destructive ops, data loss risk, running scripts, changing production settings, publishing/deploying, spending money, contacting people.
5. **User intent mismatch risk**: the request could mean multiple things depending on context.

Do **not** activate (or keep it minimal) when the request is already precise, low-risk, and has clear acceptance criteria.

## Core Workflow (Do this in order)

### Step 0 — Risk triage (B: risk-based)

Classify the next action as **low / medium / high** risk.

Use this rubric:

- **Low**: read-only inspection; formatting; adding comments/docs; adding tests (no prod impact); local-only changes that are easily reversible and clearly scoped.
- **Medium**: non-trivial refactors; changing APIs; dependency upgrades; performance/security changes without benchmarks; any change likely to ripple.
- **High**: destructive operations; running scripts with side effects; deleting data; migrations; deploy/publish; changing secrets/config; spending money; contacting people; anything hard to undo.

Tool-using agents:
- Treat **writing files** and **running commands** as at least **medium risk** if requirements or blast-radius are unclear.
- Treat commands that can modify state outside the repo (network calls, installs, migrations, deletes) as **high risk** unless explicitly approved.

Policy (risk-based):

- **Low risk**: you MAY proceed *without* asking questions, but MUST (a) state assumptions explicitly, (b) keep changes minimal and reversible, (c) stop and ask if new ambiguity appears.
- **Medium risk**: do read-only inspection first; ask targeted questions for missing constraints; propose 2–3 options; wait for confirmation before large edits.
- **High risk**: do not execute; ask for confirmation first (and consider requiring an explicit “Yes, proceed”).

### Step 1 — Context recap (alignment snapshot)

Provide a short recap (2–6 bullets) of:
- What the user asked for (as understood)
- Relevant constraints already known (repo, language, target environment, timeline)
- What you are *not* assuming yet

### Step 2 — Uncertainties & conflicts

List uncertainties as **action-blocking** vs **nice-to-have**:
- **Blocking**: must be answered to avoid wrong work
- **Optional**: can proceed with an explicit assumption if user agrees

If conflicts exist, quote them plainly and ask which requirement wins.

### Step 3 — Propose 2–3 concrete options

For each option, include:
- What will be done
- Tradeoffs (time/risk/quality)
- What you need from the user

### Step 4 — Ask targeted clarification questions

Ask the **minimum** number of questions needed (prefer **1–5** total).

Rules:
- Questions must be specific, answerable, and ordered by impact.
- Whenever possible, provide **2–3 choices** and mark a default as “(Recommended)”.
- Avoid open-ended “tell me more” unless unavoidable.

### Step 5 — Confirm and restate before acting

After the user answers, restate the finalized requirements in a short “Working Agreement”:
- Scope (in/out)
- Deliverables
- Constraints
- Acceptance criteria
- What you will do next

Then ask for a clear go-ahead: “Confirm / OK to proceed?”

Only after confirmation should the agent execute **medium/high-risk** irreversible steps.

## “Better solution” guardrail

If you see a clearly better approach than what the user requested:
- Present it as an option (don’t override the request silently).
- Explain the tradeoff briefly.
- Ask the user to choose.

## Output Template

Use this structure when clarification is needed:

1) **Alignment snapshot**
- …

2) **Open questions (Blocking)**
- Q1 (choices…)
- Q2 (choices…)

3) **Open questions (Optional)**
- …

4) **Options**
- Option A (Recommended): …
- Option B: …
- Option C: …

5) **Proposed next step**
- “If you confirm Option A + answers to Q1–Q2, I will …”

## Quick Question Bank (keep it short)

Use only what’s relevant; prefer choices.

- **Scope**: what is in/out? single file vs whole repo?
- **Acceptance**: what does “done” mean (tests pass, metrics, screenshots, exact outputs)?
- **Constraints**: framework/runtime versions, target OS, backwards compatibility, performance/security/UX requirements.
- **Risk**: is it OK to change APIs, upgrade deps, run commands, delete/overwrite, deploy/publish?
- **Context**: expected current behavior vs desired behavior; minimal repro; logs/errors; sample inputs/outputs.

## Examples

### Example 1 — Vague coding request

Input: “帮我把这个项目优化一下，尽快上线。”

Expected behavior:
- Snapshot: what “optimize” might mean (performance/UX/bundle size/test flakiness)
- Blocking questions: target “上线” environment, definition of “done”, constraints (no breaking changes?)
- Options: “quick wins only” vs “full refactor” vs “perf profiling first”
- Wait for confirmation before changes

### Example 2 — Conflicting constraints

Input: “不要改接口，但把后端彻底重构成微服务。”

Expected behavior:
- Call out conflict: “彻底重构” implies interface changes risk
- Ask which is higher priority + acceptable migration plan
- Propose phased approach options
