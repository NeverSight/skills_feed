---
name: review-plan-implementation
description: Review an implemented .plan.md by executing the instructions in its ## Reviewer Handoff section.
metadata:
  short-description: Review plan implementation
---

# Review Plan Implementation

## Goal

Given a `.plan.md` file, validate the implementation by following the plan's `## Reviewer Handoff` instructions and reporting whether code changes align with the plan.

## When to use

Use this skill when a user asks to review, verify, or audit work completed from a plan file in `.cursor/plans/*.plan.md`.

## Minimal workflow

1. **Load and validate the plan file**
   - Read the provided `.plan.md` path.
   - Confirm YAML frontmatter exists and `todos` are present.
   - Confirm a `## Reviewer Handoff` section exists.
   - If `## Reviewer Handoff` is missing, stop and report that the plan cannot be reviewed with this skill until that section is added.

2. **Extract handoff instructions**
   - Parse the `## Reviewer Handoff` section and identify:
     - Implementation summary claims
     - File-level changelog entries
     - UI manual verification checklist

3. **Review plan alignment (code review mindset)**
   - Compare completed todos in frontmatter to the claimed implementation in `## Reviewer Handoff`.
   - Inspect changed files and verify claims are accurate.
   - Prioritize findings:
     - Bugs
     - Behavioral regressions
     - Missing or incorrect implementation versus the plan
     - Missing tests or verification gaps
   - If no issues are found, explicitly state that.

4. **Execute or delegate UI verification**
   - Use the UI checklist from `## Reviewer Handoff` as the source of truth.
   - Assume the tester has no codebase context.
   - Ensure each UI step references a route/page and specific on-page area (section/panel/table).
   - If a step is ambiguous (for example component names only), rewrite it into actionable user-facing steps and call out that rewrite.

5. **Report format**
   - Present findings first, ordered by severity, with file references where applicable.
   - Then provide:
     - Open questions/assumptions
     - Plan alignment verdict (`aligned`, `partially aligned`, `not aligned`)
     - UI verification status and any blockers

## Output template

Use this structure:

```markdown
Review target: `<plan filepath>`

Findings:
1. [Severity] <title> — `<file path:line>`
1. [Severity] <title> — `<file path:line>`

Open questions / assumptions:
1. <question or assumption>

Plan alignment verdict: <aligned | partially aligned | not aligned>

UI verification:
1. <what was verified>
1. <what remains or is blocked>
```

## Notes

- Do not modify the plan status while reviewing unless the user explicitly asks for updates.
- Treat `## Reviewer Handoff` as the authoritative review scope unless the user expands scope.
- If the user asks for a strict sign-off decision, provide a clear yes/no with rationale.
