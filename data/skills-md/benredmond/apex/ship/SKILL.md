---
name: ship
description: Review and finalize (REVIEWER + DOCUMENTER phases) - runs adversarial code review, commits changes, completes task, and records reflection to capture pattern outcomes.
argument-hint: [task-identifier]
---

<skill name="apex:ship" phase="ship">

<overview>
Final phase: Review implementation with adversarial agents, commit changes, complete task, and record reflection.

Combines REVIEWER (adversarial code review) and DOCUMENTER (commit, complete, reflect).
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

<phase-gate requires="implement" sets="complete">
  <reads-file>./.apex/tasks/[ID].md</reads-file>
  <requires-section>implementation</requires-section>
  <appends-section>ship</appends-section>
</phase-gate>

<mandatory-actions>
This phase requires THREE mandatory actions in order:
1. **Adversarial Review** - Launch review agents
2. **Git Commit** - Commit all changes
3. **Final Reflection** - Record pattern outcomes and key learnings

YOU CANNOT SKIP ANY OF THESE for APPROVE or CONDITIONAL outcomes.
If REJECT, stop after review, set frontmatter to `phase: rework`, and return to `/apex:implement`.
</mandatory-actions>

<initial-response>
<if-no-arguments>
I'll review and finalize the implementation. Please provide the task identifier.

You can find active tasks in `./.apex/tasks/` or run with:
`/apex:ship [identifier]`
</if-no-arguments>
<if-arguments>Load task file and begin review.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Load task and verify phase">
<instructions>
1. Read `./.apex/tasks/[identifier].md`
2. Verify frontmatter `phase: implement`
3. Parse `<task-contract>` first and note its latest version and any amendments
4. Parse all sections for full context
5. If phase != implement, refuse with: "Task is in [phase] phase. Expected: implement"

Contract rules:
- Final report MUST map changes to AC-* and confirm no out-of-scope work
- If scope/ACs changed during implement, ensure amendments are recorded with rationale and version bump
</instructions>
</step>

<step id="2" title="Gather review context">
<extract>
- `<task-contract>` - Authoritative scope/ACs and amendment history
- `<implementation><files-modified>` - What changed
- `<implementation><files-created>` - What's new
- `<implementation><patterns-used>` - Patterns to validate
- `<implementation><validation-results>` - Test status
- `<implementation><reviewer-handoff>` - Key points for review
- `<plan><architecture-decision>` - Original intentions
- `<plan><warnings>` - Risks to verify mitigated
</extract>

<get-diffs>
```bash
git diff HEAD~N  # or appropriate range for this task's changes
git log --oneline -10
```
</get-diffs>
</step>

<step id="3" title="Phase 1: Launch review agents">
<critical>
Launch ALL 5 Phase 1 agents in a SINGLE message for true parallelism.
</critical>

<agents parallel="true">

<agent type="apex:review:phase1:review-security-analyst">
**Task ID**: [taskId]
**Code Changes**: [Full diff]
**Journey Context**: Architecture warnings, implementation decisions, test results

Review for security vulnerabilities. Return YAML with id, severity, confidence, location, issue, evidence, mitigations_found.
</agent>

<agent type="apex:review:phase1:review-performance-analyst">
**Task ID**: [taskId]
**Code Changes**: [Full diff]
**Journey Context**: Architecture warnings, implementation decisions

Review for performance issues. Return YAML findings.
</agent>

<agent type="apex:review:phase1:review-architecture-analyst">
**Task ID**: [taskId]
**Code Changes**: [Full diff]
**Journey Context**: Original architecture from plan, pattern selections

Review for architecture violations and pattern consistency. Return YAML findings.
</agent>

<agent type="apex:review:phase1:review-test-coverage-analyst">
**Task ID**: [taskId]
**Code Changes**: [Full diff]
**Validation Results**: [From implementation section]

Review for test coverage gaps. Return YAML findings.
</agent>

<agent type="apex:review:phase1:review-code-quality-analyst">
**Task ID**: [taskId]
**Code Changes**: [Full diff]
**Journey Context**: Patterns applied, conventions followed

Review for maintainability and code quality. Return YAML findings.
</agent>

</agents>

<wait-for-all>WAIT for ALL 5 agents to complete before Phase 2.</wait-for-all>
</step>

<step id="4" title="Phase 2: Adversarial challenge">
<agents parallel="true">

<agent type="apex:review:phase2:review-challenger">
**Phase 1 Findings**: [YAML from all 5 Phase 1 agents]
**Original Code**: [Relevant snippets]
**Journey Context**: Plan rationale, implementation justifications

Challenge EVERY finding for:
- Code accuracy (did Phase 1 read correctly?)
- Pattern applicability (does framework prevent this?)
- Evidence quality (Strong/Medium/Weak)
- ROI Analysis:
  - fix_effort: trivial | minor | moderate | significant | major
  - benefit_type: security | reliability | performance | maintainability | correctness
  - roi_score: 0.0-1.0 (benefit / effort ratio)
  - override_decision: pull_forward | keep | push_back
  - override_reason: [Why changing priority]

Return: challenge_result (UPHELD|DOWNGRADED|DISMISSED), evidence_quality, recommended_confidence, roi_analysis
</agent>

<agent type="apex:review:phase2:review-context-defender">
**Phase 1 Findings**: [Findings affecting existing code]
**Repository**: [Path and git info]

Use git history to find justifications for seemingly problematic patterns.
Return: Context justifications for historical code choices.
</agent>

</agents>

<wait-for-all>WAIT for both agents to complete.</wait-for-all>
</step>

<step id="5" title="Synthesize review results">
<confidence-adjustment>
For each finding:
  finalConfidence = phase1Confidence
  finalConfidence *= challengeImpact  # UPHELD=1.0, DOWNGRADED=0.6, DISMISSED=0.2
  finalConfidence *= (0.5 + evidence_score * 0.5)
  if context_justified: finalConfidence *= 0.3
</confidence-adjustment>

<action-decision>
- confidence < 0.3 → DISMISS
- critical AND confidence > 0.5 → FIX_NOW
- high AND confidence > 0.6 → FIX_NOW
- confidence > 0.7 → SHOULD_FIX
- else → NOTE
</action-decision>

<review-decision>
- 0 FIX_NOW → APPROVE (proceed to commit)
- 1-2 FIX_NOW minor → CONDITIONAL (fix or accept with docs)
- 3+ FIX_NOW or critical security → REJECT (return to /apex:implement)
</review-decision>

<reject-flow>
On REJECT:
1. Write `<ship><decision>REJECT</decision>` with a brief rationale
2. Update frontmatter: `phase: rework`, `updated: [ISO timestamp]`
3. STOP. Do NOT commit or finalize reflection. Return to `/apex:implement`.
</reject-flow>
</step>

<step id="5.5" title="Documentation Updates">
<purpose>
Ensure documentation stays in sync with code changes.
</purpose>

<documentation-checklist>
**If task modified workflow or architecture**:
- [ ] CLAUDE.md - Check for stale references to changed behavior
- [ ] README.md - Update any affected workflow descriptions
- [ ] Related design docs - Search in docs/ directory

**If task modified API or CLI**:
- [ ] API documentation files
- [ ] CLI command documentation
- [ ] Usage examples in docs

**If task modified data structures**:
- [ ] Type definition docs
- [ ] Schema documentation
- [ ] Migration notes if breaking change

**Search strategy**:
```bash
# Find docs that might reference changed files
for file in [modified_files]; do
  grep -r "$(basename $file .ts)" docs/ README.md CLAUDE.md
done
```
</documentation-checklist>

<update-procedure>
1. Search for references to modified code
2. Read each found doc FULLY
3. Update outdated references
4. Verify accuracy after update
5. Add to git staging for commit
</update-procedure>

<docs-to-update-output>
Record in `<implementation><docs-updated>`:
```xml
<docs-updated>
  <doc path="[path]" reason="[Why updated]"/>
</docs-updated>
```
</docs-to-update-output>
</step>

<step id="6" title="Git commit">
<critical>
Commit BEFORE final reflection - reflection should reference an immutable commit.
</critical>

<commands>
```bash
git status --short
git add [relevant files]
git commit -m "[Task ID]: [Description]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git log -1 --oneline  # Capture commit SHA
```
</commands>

<checkpoint>Commit SHA captured for evidence.</checkpoint>

<compound-prompt>
After successful commit, display:
```
Committed: [SHA]

Run `/apex:compound [identifier]` to capture learnings for future agents.
```
</compound-prompt>
</step>

<step id="7" title="Reflection and completion">
<critical>
You MUST record a final reflection. This is NOT optional.

Without reflection:
- Learnings aren't captured
- Pattern outcomes aren't recorded
- Future tasks don't benefit
</critical>

<reflection-format>
```markdown
### Reflection
- **Outcome**: success | partial | failure
- **Key Learning**: [Main lesson from this task]
- **Patterns Used**: [PAT:ID from plan] with outcome notes
- **New Patterns / Anti-patterns**: [If discovered]
- **Evidence**: [Commit SHA, files, tests]
```
</reflection-format>

<instructions>
1. Summarize outcome and key learning
2. List patterns used from the plan with outcome notes
3. Capture any new patterns or anti-patterns discovered
4. Reference evidence (commit SHA, file paths, tests)
5. Update the task file's `<ship><reflection>` section
</instructions>
</step>

<step id="9" title="Write ship section to task file">
<output-format>
Append to `<ship>` section:

```xml
<ship>
<metadata>
  <timestamp>[ISO]</timestamp>
  <outcome>success|partial|failure</outcome>
  <commit-sha>[SHA]</commit-sha>
</metadata>

<review-summary>
  <phase1-findings count="X">
    <by-severity critical="N" high="N" medium="N" low="N"/>
    <by-agent security="N" performance="N" architecture="N" testing="N" quality="N"/>
  </phase1-findings>
  <phase2-challenges>
    <upheld>N</upheld>
    <downgraded>N</downgraded>
    <dismissed>N</dismissed>
  </phase2-challenges>
  <false-positive-rate>[X%]</false-positive-rate>
</review-summary>

<contract-verification>
  <contract-version>[N]</contract-version>
  <amendments-audited>[List amendments or "none"]</amendments-audited>
  <acceptance-criteria-verification>
    <criterion id="AC-1" status="met|not-met">[Evidence or exception]</criterion>
  </acceptance-criteria-verification>
  <out-of-scope-check>[Confirm no out-of-scope work slipped in]</out-of-scope-check>
</contract-verification>

<action-items>
  <fix-now>
    <item id="[ID]" severity="[S]" confidence="[C]" location="[file:line]">
      [Issue and fix]
    </item>
  </fix-now>
  <should-fix>[Deferred items]</should-fix>
  <accepted>[Accepted risks with justification]</accepted>
  <dismissed>[False positives with reasons]</dismissed>
</action-items>

<commit>
  <sha>[Full SHA]</sha>
  <message>[Commit message]</message>
  <files>[List of files]</files>
</commit>

<reflection>
  <patterns-reported>
    <pattern id="PAT:X:Y" outcome="[outcome]"/>
  </patterns-reported>
  <key-learning>[Main lesson]</key-learning>
  <reflection-status>recorded|missing</reflection-status>
</reflection>

<final-summary>
  <what-was-built>[Concise description]</what-was-built>
  <patterns-applied count="N">[List]</patterns-applied>
  <test-status passed="X" failed="Y"/>
  <documentation-updated>[What docs changed]</documentation-updated>
</final-summary>
</ship>
```
</output-format>

<update-frontmatter>
For APPROVE or CONDITIONAL only:
Set `phase: complete`, `status: complete`, and `updated: [ISO timestamp]`
</update-frontmatter>
</step>

<step id="10" title="Final report to user">
<template>
✅ **Task Complete**: [Title]

📊 **Metrics**:
- Complexity: [X]/10
- Files modified: [N]
- Files created: [N]
- Tests: [passed]/[total]

💬 **Summary**: [Concise description of what was built]

📚 **Patterns**:
- Applied: [N] patterns
- Reflection: ✅ Recorded

✅ **Acceptance Criteria**:
- AC-* coverage: [met|not met with exceptions]

🔍 **Review**:
- Phase 1 findings: [N]
- Dismissed as false positives: [N] ([X]%)
- Action items: [N] (all resolved)

⏭️ **Next**: Task complete. No further action required.
</template>
</step>

</workflow>

<completion-verification>
BEFORE reporting to user, verify ALL actions completed:

- [ ] Phase 1 review agents launched and returned?
- [ ] Phase 2 challenge agents launched and returned (with ROI analysis)?
- [ ] Documentation checklist completed?
- [ ] Contract verification completed (AC mapping + out-of-scope check)?
- [ ] Git commit created? (verify with git log -1)
- [ ] Reflection recorded in `<ship><reflection>`?

**If ANY unchecked → GO BACK AND COMPLETE IT.**
</completion-verification>

<success-criteria>
- Adversarial review completed (7 agents: 5 Phase 1 + 2 Phase 2)
- ROI analysis included in challenger findings
- Documentation checklist completed (grep → read → update → verify)
- Contract verification completed with AC mapping and scope confirmation
- All FIX_NOW items resolved (or explicitly accepted)
- Git commit created with proper message
- Reflection recorded with patterns and learnings
- Task file updated with complete ship section
- Frontmatter shows phase: complete, status: complete
</success-criteria>

</skill>
