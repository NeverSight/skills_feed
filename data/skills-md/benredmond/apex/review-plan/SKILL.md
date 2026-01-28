---
name: review-plan
description: Advisory plan review - validates plan correctness and identifies gaps before implementation. Works on any task with research and plan sections.
argument-hint: [task-identifier]
---

<skill name="apex:review-plan" phase="advisory">

<overview>
Lightweight plan review that catches gaps and errors before implementation commitment.

Three focused lenses:
1. **Completeness** - Are all required plan artifacts present and substantive?
2. **Gap Analysis** - What did research find that plan doesn't address?
3. **Correctness** - Is the plan internally consistent and feasible?

Output goes to chat. User fixes issues inline, then proceeds to implement.
</overview>

<phase-gate requires="none" sets="none">
  <reads-file>./.apex/tasks/[ID].md</reads-file>
  <expects-sections>research, plan</expects-sections>
  <outputs-to>chat</outputs-to>
</phase-gate>

<principles>
- **Advisory Only**: No phase changes, no file modifications
- **Fast**: Direct analysis, no subagents
- **Actionable**: Every gap or error includes what to fix
- **Honest**: Call out real problems, don't rubber-stamp
- **Flexible**: Works regardless of current phase
</principles>

<initial-response>
<if-no-arguments>
I'll review the plan for gaps and correctness. Please provide the task identifier.

You can find tasks in `./.apex/tasks/` or run with:
`/apex:review-plan [identifier]`
</if-no-arguments>
<if-arguments>Load task file and begin review.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Load task and extract sections">
<instructions>
1. Read `./.apex/tasks/[identifier].md`
2. Note current phase from frontmatter (informational only - don't block)
3. Extract and parse (note any missing sections):
   - `<task-contract>` - From within `<research>` section
   - `<research>` - All findings from research phase
   - `<plan>` - All artifacts from plan phase
4. If `<research>` or `<plan>` sections are missing/empty, report as finding (don't refuse)
5. Verify file paths mentioned in `<plan><architecture-decision><files-to-modify>` exist using glob/ls
</instructions>
</step>

<step id="2" title="Completeness Check">
<purpose>
Verify all mandatory plan artifacts are present and substantive.
</purpose>

<mandatory-artifacts>
Look for these concepts (tag names may vary):

1. **Design Rationale** - Current state, problem breakdown, hidden complexity, success criteria
2. **Tree of Thought** - 3 different solution approaches with a winner selected
3. **Chain of Draft** - Evolution through multiple drafts
4. **YAGNI** - What's explicitly excluded, complexity budget
5. **Patterns** - Which patterns are being applied (can be empty)
6. **Architecture Decision** - Files to change, implementation steps, how to validate
7. **Builder Handoff** - Clear mission, ordered steps, validation checkpoints
8. **Contract Validation** - AC coverage confirmation
</mandatory-artifacts>

<contract-validation>
- [ ] Plan acknowledges the current contract version
- [ ] If amendments exist in task-contract, they are acknowledged in plan
- [ ] Every AC in task-contract is addressed somewhere in plan
</contract-validation>

<output-format>
## Completeness Check

### Missing Artifacts
- **[Artifact name]**: Not found or empty
  - **Fix**: Add required section to plan

### Incomplete Artifacts
- **[Artifact name]**: Missing [specific subsection]
  - **Fix**: Add [subsection] with [expected content]

### Contract Issues
- **Version mismatch**: Contract v[X] but plan references v[Y]
  - **Fix**: Update plan to reference current contract version
- **Unacknowledged amendment**: Amendment not recorded in plan
  - **Fix**: Acknowledge the amendment in plan

**Completeness Score**: [N] artifacts present, [N] issues
</output-format>
</step>

<step id="3" title="Gap Analysis">
<purpose>
Find what research discovered that plan doesn't address.
</purpose>

<checklist>
**Research Risks vs Plan Mitigations:**
- [ ] Every risk identified in research has a mitigation in plan
- [ ] High-probability AND high-impact risks have explicit handling
- List any unaddressed risks with their probability/impact

**Research Security Concerns vs Plan:**
- [ ] Security concerns from research are addressed in plan OR explicitly excluded
- List any unaddressed security concerns

**Pattern Provenance:**
- [ ] Patterns claimed in plan can be traced to research (pattern library or codebase conventions)
- [ ] Trust scores roughly match what research found
- List any patterns that appear fabricated or unsupported

**Documentation Drift:**
- [ ] Docs flagged for update in research are included in plan's files to modify (or noted as intentionally skipped)
- List any documentation that will drift

**Research Recommendations vs Chosen Solution:**
- [ ] Plan's chosen solution aligns with research recommendation (or has justification for divergence)
- List any unexplained divergences

**Task Contract Coverage:**
- [ ] Every AC in task-contract maps to implementation steps
- [ ] Non-functional requirements are addressed in validation approach
- List any uncovered ACs or NFRs

**Complexity Budget:**
- [ ] Plan's complexity estimate is reasonable given what research found
- Flag if plan seems significantly over/under-scoped
</checklist>

<output-format>
## Gap Analysis

### Unaddressed Risks
- **[Risk name]** (probability: [H/M/L], impact: [H/M/L]): Research identified [description]. Plan has no mitigation.
  - **Fix**: Add mitigation to plan's risk section.

### Security Gaps
- **[Concern]**: From research, not addressed in plan.
  - **Fix**: Add to risks or explicitly exclude with rationale.

### Pattern Issues
- **[Pattern]**: Claimed in plan but can't find source in research.
  - **Fix**: Remove pattern or trace back to research source.
- **[Pattern]**: Confidence rating mismatch ([X] in plan vs [Y] in research).
  - **Fix**: Align confidence rating with research.

### Documentation That Will Drift
- **[doc path]**: Research flagged for update, not in plan's files to modify.
  - **Fix**: Add to files or note why update not needed.

### Uncovered Requirements
- **AC-[N]**: [Description] - No implementation step addresses this.
  - **Fix**: Add step to cover this AC.
- **NFR [type]**: [Constraint] - Not validated.
  - **Fix**: Add validation for this constraint.

**Gap Score**: [N] gaps ([N] critical, [N] moderate, [N] minor)
</output-format>
</step>

<step id="4" title="Correctness Check">
<purpose>
Verify plan is internally consistent and feasible.
</purpose>

<checklist>
**Internal Consistency:**
- [ ] Chosen solution in summary/metadata matches the winner in Tree of Thought
- [ ] Complexity estimate aligns with risks (high risk → expect higher complexity)
- [ ] Implementation sequence in architecture decision matches builder handoff
- [ ] Risk level matches actual risks identified
- List any contradictions

**Tree of Thought Validity:**
- [ ] 3 solutions are genuinely different approaches (not variations of same idea)
- [ ] Winner selection has concrete reasoning citing evidence (not "this feels right")
- [ ] Pros/cons reference specific findings from research, not hypotheticals

**Chain of Draft Evolution:**
- [ ] Final draft is meaningfully different from first draft (not cosmetic rewording)
- [ ] Issues identified in earlier drafts are resolved in later drafts
- [ ] Evolution shows actual refinement based on research insights

**YAGNI Coherence:**
- [ ] Excluded features don't contradict task contract in-scope items
- [ ] Excluded features aren't required by any AC

**Implementation Sequence:**
- [ ] Steps are in dependency order (foundations before dependents)
- [ ] Each step has a concrete validation (command to run, not "verify it works")
- [ ] File paths to modify exist (verify via glob)
- [ ] New files are clearly marked as new

**Validation Quality:**
- [ ] Automated validation includes actual runnable commands (npm test, pytest, etc.)
- [ ] Manual verification has specific steps, not vague checks

**Feasibility:**
- [ ] No circular dependencies in implementation sequence
- [ ] Patterns applied at sensible locations (not generic "apply everywhere")
- [ ] No magical thinking ("this edge case won't happen")
</checklist>

<output-format>
## Correctness Check

### Internal Contradictions
- **[Field A] vs [Field B]**: [A] says [X] but [B] says [Y]
  - **Fix**: Reconcile to [recommendation]

### Tree of Thought Issues
- **Solutions not distinct**: [A] and [B] are variations of same approach
  - **Fix**: Replace [B] with genuinely different architecture
- **Weak winner reasoning**: Selection based on preference, not evidence
  - **Fix**: Add specific research findings supporting choice

### Implementation Issues
- **Step [N]**: [Problem - missing validation, wrong order, etc.]
  - **Fix**: [Specific correction]
- **Vague validation gate**: "[gate text]" is not testable
  - **Fix**: Replace with concrete command: `[suggested command]`

### File Path Issues
- **[path]**: Listed in files-to-modify but does not exist
  - **Fix**: Correct path or move to files-to-create

### Feasibility Concerns
- **[Concern]**: [Why this might not work]
  - **Fix**: [How to address]

**Correctness Score**: [SOUND / MINOR_ISSUES / MAJOR_ISSUES]
</output-format>
</step>

<step id="5" title="Deliver Review">
<output-format>
# Plan Review: [Task Title]

## Summary

| Dimension | Status | Issues |
|-----------|--------|--------|
| Completeness | [✅ Complete / ⚠️ Gaps / ❌ Missing Artifacts] | [N] |
| Gap Analysis | [✅ Clean / ⚠️ Gaps / ❌ Major Gaps] | [N] |
| Correctness | [✅ Sound / ⚠️ Minor Issues / ❌ Major Issues] | [N] |

**Recommendation**: [PROCEED / REVISE / RETHINK]

---

## Completeness Check
[From step 2]

---

## Gap Analysis
[From step 3]

---

## Correctness Check
[From step 4]

---

## Action Items

### Must Fix Before Implement
> Issues that will cause implementation to fail or produce wrong results

1. [Issue with specific fix]

### Should Address
> Issues that won't block but will cause problems later

1. [Issue with specific fix]

### Consider
> Improvements that would make the plan better

1. [Suggestion]

---

## Next Steps

[If PROCEED]: Ready for `/apex:implement [identifier]`
[If REVISE]: Fix the issues above in this session, then re-run `/apex:review-plan [identifier]`
[If RETHINK]: Fundamental issues found - consider returning to `/apex:plan [identifier]` to rework architecture
</output-format>
</step>

</workflow>

<classification-rubric>
**Must Fix** (blocks implementation):
- Missing mandatory artifacts (completeness)
- Unaddressed high-impact risks
- Fabricated patterns (no source in research)
- Uncovered acceptance criteria
- File paths that don't exist (listed as modify, not create)
- Internal contradictions (metadata vs content)
- Vague validation gates with no concrete commands

**Should Address** (causes problems later):
- Unaddressed medium-impact risks
- Documentation drift (docs-to-update not in plan)
- Unacknowledged contract amendments
- Weak Tree of Thought (solutions too similar)
- Chain of Draft shows no real evolution
- Trust score mismatches
- NFRs not validated

**Consider** (improvements):
- Minor inconsistencies in wording
- Complexity budget slightly high
- Could use additional patterns
- Validation could be more thorough
</classification-rubric>

<recommendation-criteria>
- **PROCEED**: 0 Must Fix items
- **REVISE**: 1-3 Must Fix items (fixable in current session)
- **RETHINK**: 4+ Must Fix items OR most key artifacts missing OR fundamental architecture problems (wrong solution chosen, contradicts research)
</recommendation-criteria>

<success-criteria>
- Task file read (regardless of phase)
- Missing sections reported as findings, not errors
- File existence verified via glob/ls
- Completeness check: key artifacts assessed
- Gap analysis: risks, security, patterns, docs, ACs, NFRs checked
- Correctness check: consistency, validity, feasibility assessed
- Classification rubric applied consistently
- Clear recommendation with actionable next steps
</success-criteria>

</skill>
