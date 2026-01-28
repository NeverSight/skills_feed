---
name: implement
description: Build and validate loop (BUILDER + validation) - implements the architecture, runs tests, iterates until passing. Writes code following the plan.
argument-hint: [task-identifier]
---

<skill name="apex:implement" phase="implement">

<overview>
Implement the architecture from the plan phase. Build code, run tests, iterate until all validations pass.

Combines BUILDER (write code) and validation (run tests) in a tight loop.
</overview>

<phase-model>
phase_model:
  frontmatter: [research, plan, implement, rework, complete]
  rework: enabled
  db_role: [RESEARCH, ARCHITECT, BUILDER, BUILDER_VALIDATOR, REVIEWER, DOCUMENTER]
  legacy_db_role: [VALIDATOR]
source_of_truth:
  gating: frontmatter.phase
  telemetry: db_role
</phase-model>

<phase-gate requires="plan|rework" sets="implement">
  <reads-file>./.apex/tasks/[ID].md</reads-file>
  <requires-section>plan</requires-section>
  <appends-section>implementation</appends-section>
</phase-gate>

<principles>
- **Follow the Plan**: The architecture was approved - implement it, don't redesign
- **Pattern Discipline**: Only use patterns from the plan's pattern selection
- **Fail Fast**: Run tests frequently, fix issues immediately
- **No Guessing**: If spec is unclear, return to plan or ask user
</principles>

<initial-response>
<if-no-arguments>
I'll implement the planned architecture. Please provide the task identifier.

You can find active tasks in `./.apex/tasks/` or run with:
`/apex:implement [identifier]`
</if-no-arguments>
<if-arguments>Load task file and begin implementation.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Load task and verify phase">
<instructions>
1. Read `./.apex/tasks/[identifier].md`
2. Verify frontmatter `phase: plan` OR `phase: rework`
3. Parse `<task-contract>` first and treat it as authoritative scope/ACs
4. Parse `<plan>` section, especially `<builder-handoff>`
5. If phase == rework, treat this as a Ship REJECT rework loop
6. If phase not in [plan, rework], refuse with: "Task is in [phase] phase. Expected: plan or rework"

Contract rules:
- Implementation MUST satisfy all AC-* or explicitly document unmet criteria
- If scope/ACs must change, append a <amendments><amendment ...> entry inside task-contract and bump its version
</instructions>

</step>

<step id="2" title="Extract implementation directives">
<extract-from-plan>
- `<builder-handoff><mission>` - What we're building
- `<builder-handoff><core-architecture>` - The chosen approach
- `<builder-handoff><pattern-guidance>` - Patterns to apply with locations
- `<builder-handoff><implementation-order>` - Sequence of steps
- `<builder-handoff><validation-gates>` - Checks after each step
- `<builder-handoff><warnings>` - Critical risks to avoid
- `<architecture-decision><files-to-modify>` - Existing files to change
- `<architecture-decision><files-to-create>` - New files to add
</extract-from-plan>

<extract-from-contract>
- `<task-contract><acceptance-criteria>` - AC-* to track and validate
</extract-from-contract>

<create-todo-list>
Create TodoWrite items for each implementation step from the plan.
</create-todo-list>
</step>

<step id="3" title="Pre-implementation verification">
<checks>
- [ ] All files to modify exist and are readable
- [ ] No syntax errors in current codebase (`npm run lint` or equivalent)
- [ ] Tests currently passing (baseline)
- [ ] Dependencies available
</checks>
<on-failure>Document blockers and ask user how to proceed.</on-failure>
</step>

<step id="4" title="Implementation loop">
<loop until="all steps complete AND all tests pass">

<builder-phase>
<for-each-step>
1. **Read target files** fully before modifying
2. **Apply patterns** from plan's pattern-guidance
3. **Write code** following architecture decision
4. **Document pattern usage**: `# [PAT:ID] ★★★★☆ (X uses, Y% success)`
5. **Run syntax check** immediately after writing
</for-each-step>

<pattern-discipline>
ONLY use patterns listed in `<plan><patterns><applying>`.
DO NOT invent new pattern names.
If you need a pattern not in the plan, document it as a gap.
</pattern-discipline>

<failure-prevention>
Review `<plan><architecture-decision><risks>` before each step.
Apply mitigations proactively.
</failure-prevention>
</builder-phase>

<validator-phase>
<after-each-step>
1. Run validation gate from plan
2. If passes, continue to next step
3. If fails, fix and retry (max 3 attempts per step)
4. After 3 failures, document issue and ask user
</after-each-step>

<validation-commands>
- Syntax: `npm run lint` / `ruff check` / language-appropriate
- Types: `tsc --noEmit` / `mypy` / language-appropriate
- Unit tests: `npm test` / `pytest` / language-appropriate
- Integration: As specified in plan
</validation-commands>
</validator-phase>

<checkpoint-after-each-step>
Record a checkpoint in the task log after each step (summary + confidence).
</checkpoint-after-each-step>

</loop>
</step>

<step id="4.5" title="Pattern Evidence Gate">
<critical>
Before running full validation, verify all patterns you intend to claim.
</critical>

<verification-checklist>
For each pattern in `<patterns-used>`:
1. [ ] Pattern exists in `<plan><patterns><applying>`
2. [ ] Trust score matches what's in the plan
3. [ ] Location (file:line) is accurate and verifiable
4. [ ] Outcome is honest (worked|tweaked|failed)
</verification-checklist>

<evidence-collection>
Record pattern usage evidence BEFORE validation:
- pattern_id
- file and line range
- outcome (worked|tweaked|failed)
- notes on usage
</evidence-collection>

<fabrication-check>
IF any pattern in `<patterns-used>` is NOT in `<plan><patterns><applying>`:
→ REMOVE it from patterns-used
→ Document as "unplanned pattern discovered"
→ Do NOT claim it in the final reflection

Unplanned patterns can be documented as "new patterns" in the final reflection,
but NOT as "patterns used" (which updates confidence).
</fabrication-check>
</step>

<step id="5" title="Comprehensive validation">
<critical>
This is NOT optional. Run FULL test suite before completing.
</critical>

<spawn-validator>
<agent type="apex:test-validator">
**Task ID**: [taskId]
**Modified Files**: [list from implementation]
**Predictions**: [from plan's risk section]

Run: Syntax → Formatting → Type check → Unit tests → Integration tests → Coverage

Return: Validation report comparing predictions vs reality
</agent>
</spawn-validator>

<decision-logic>
IF any failures:
  → Return to builder-phase with issue list
  → Fix and re-run validation
  → Max 3 full cycles before escalating to user

IF only warnings:
  → Document for review phase
  → Proceed

IF all pass:
  → Proceed to write implementation section
</decision-logic>
</step>

<step id="6" title="Write implementation section to task file">
<output-format>
Append to `<implementation>` section:

```xml
<implementation>
<metadata>
  <timestamp>[ISO]</timestamp>
  <duration>[Time spent]</duration>
  <iterations>[Build-validate cycles]</iterations>
</metadata>

<files-modified>
  <file path="[path]">
    <changes>[Summary of what changed]</changes>
    <patterns-applied>
      <pattern id="PAT:X:Y">[How it was used]</pattern>
    </patterns-applied>
    <diff-summary>[Key additions/removals]</diff-summary>
  </file>
</files-modified>

<files-created>
  <file path="[path]">
    <purpose>[Why created]</purpose>
    <patterns-applied>[PAT:IDs]</patterns-applied>
    <test-file>[Corresponding test if any]</test-file>
  </file>
</files-created>

<validation-results>
  <syntax status="pass|fail">[Details]</syntax>
  <types status="pass|fail">[Details]</types>
  <tests status="pass|fail" passed="X" failed="Y" skipped="Z">[Details]</tests>
  <coverage>[Percentage if available]</coverage>
</validation-results>

<acceptance-criteria-status>
  <criterion id="AC-1" status="met|not-met">[Evidence or reason]</criterion>
</acceptance-criteria-status>

<patterns-used>
  <pattern id="PAT:X:Y" location="file:line" outcome="worked|tweaked|failed">
    [Notes on usage]
  </pattern>
</patterns-used>

<issues-encountered>
  <issue resolved="true|false">
    <description>[What happened]</description>
    <resolution>[How fixed, or why unresolved]</resolution>
  </issue>
</issues-encountered>

<deviations-from-plan>
  <deviation>
    <planned>[What plan said]</planned>
    <actual>[What we did instead]</actual>
    <reason>[Why deviation was necessary]</reason>
  </deviation>
</deviations-from-plan>

<reviewer-handoff>
  <summary>[What was built]</summary>
  <key-changes>[Most important modifications]</key-changes>
  <test-coverage>[What's tested]</test-coverage>
  <known-limitations>[Edge cases, TODOs]</known-limitations>
  <patterns-for-reflection>[Patterns to report in the final reflection]</patterns-for-reflection>
</reviewer-handoff>

<next-steps>
Run `/apex:ship [identifier]` to review and finalize.
</next-steps>
</implementation>
```
</output-format>

<update-frontmatter>
Set `phase: implement` and `updated: [ISO timestamp]`
</update-frontmatter>

</step>

</workflow>

<critical-requirements>

<pattern-fabrication-prevention>
YOU CANNOT FABRICATE PATTERNS.

Only claim patterns that exist in `<plan><patterns><applying>`.
In `<patterns-used>`, only list patterns from the plan.
Pattern IDs claimed here will be validated during `/apex:ship`.

VIOLATION: Claiming "PAT:NEW:THING" that was never in the plan
CONSEQUENCE: The final reflection becomes unreliable and confidence becomes meaningless
</pattern-fabrication-prevention>

<syntax-gate>
Before completing implementation:
- Run linting
- Check for common errors (double async, missing brackets)
- Fix ALL syntax errors before proceeding
- DO NOT transition to ship with syntax errors
</syntax-gate>

<contract-gate>
Before finishing:
- Confirm all AC-* are met, or explicitly mark any unmet criteria with reasons
- If contract scope/ACs changed, record an amendment with rationale and bump contract version
</contract-gate>

<spec-unclear-protocol>
If implementation reveals spec ambiguity:
1. Document the ambiguity
2. Ask user for clarification
3. If architectural change needed, note it for plan revision
4. Do NOT guess and implement wrong thing
</spec-unclear-protocol>

</critical-requirements>

<success-criteria>
- All implementation steps from plan completed
- All validation gates passed
- Full test suite passing
- No syntax errors
- Acceptance criteria status reported for all AC-*
- Patterns used are from plan only (Pattern Evidence Gate passed)
- Deviations documented with reasons
- Task file updated at ./.apex/tasks/[ID].md
- Checkpoints recorded at start, per-step, and end
- Pattern evidence recorded for usage
- Task metadata updated for build/validate completion
</success-criteria>

<next-phase>
`/apex:ship [identifier]` - Review, document, and reflect
</next-phase>

</skill>
