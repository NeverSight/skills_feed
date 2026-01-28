---
name: plan
description: Architecture phase (ARCHITECT) - transforms research into rigorous technical architecture through 5 mandatory design artifacts. Interactive and iterative.
argument-hint: [task-identifier]
---

<skill name="apex:plan" phase="plan">

<overview>
Transform research findings into battle-tested implementation plans through interactive design.

Produces 5 mandatory artifacts: Design Rationale and Evidence, Tree of Thought, Chain of Draft, YAGNI Declaration, Pattern Selection.
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

<phase-gate requires="research" sets="plan">
  <reads-file>./.apex/tasks/[ID].md</reads-file>
  <requires-section>research</requires-section>
  <appends-section>plan</appends-section>
</phase-gate>

<principles>
- **Be Skeptical**: Question vague requirements, identify issues early, verify with code
- **Be Interactive**: Get buy-in at each step, don't create full plan in one shot
- **Be Thorough**: Read ALL files FULLY, research patterns with parallel agents
- **Be Evidence-Based**: Every decision backed by code, patterns, or research
- **No Open Questions**: STOP and clarify before proceeding with unknowns
</principles>

<initial-response>
<if-no-arguments>
I'll create a rigorous technical architecture. Please provide the task identifier.

You can find active tasks in `./.apex/tasks/` or run with:
`/apex:plan [identifier]`
</if-no-arguments>
<if-arguments>Load task file and begin architecture process.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Load task and verify phase">
<instructions>
1. Read `./.apex/tasks/[identifier].md`
2. Verify frontmatter `phase: research`
3. Parse `<task-contract>` from the research output FIRST and treat it as authoritative scope/ACs
4. If `<task-contract>` is missing, STOP and ask to rerun research or add the contract with an explicit amendment rationale
5. Parse `<research>` section for context
6. If phase != research, refuse with: "Task is in [phase] phase. Expected: research"
7. Extract context pack references from `<context-pack-refs>`:
   - ctx.patterns = research.pattern-library
   - ctx.impl = research.codebase-patterns
   - ctx.web = research.web-research
   - ctx.history = research.git-history
   - ctx.docs = research.documentation
   - ctx.risks = research.risks
   - ctx.exec = research.recommendations.winner

Contract rules:
- Architecture artifacts MUST NOT contradict task-contract scope or ACs
- If scope/ACs must change, append a <amendments><amendment ...> entry inside task-contract and bump its version
</instructions>

</step>

<step id="2" title="Read research and spawn verification agents">
<critical>
Read ALL files mentioned in research section FULLY before any analysis.
</critical>

<agents parallel="true">
<agent type="intelligence-gatherer">Verify and extend pattern intelligence from research</agent>
<agent type="apex:systems-researcher">Map system flows for components mentioned in research</agent>
<agent type="apex:git-historian">Surface timelines and regressions for affected areas</agent>
<agent type="failure-predictor">Identify what could go wrong based on history</agent>
<agent type="apex:risk-analyst">Enumerate edge cases and mitigations</agent>
</agents>
</step>

<step id="3" title="Present initial understanding">
<template>
Based on research and analysis, I understand we need to [accurate summary].

**Key Findings:**
- [Current implementation at file:line]
- [Pattern discovered with confidence rating]
- [Complexity identified]

**Questions Requiring Human Judgment:**
- [Design preference that affects architecture]
- [Business logic clarification]
- [Risk tolerance decision]

Let's address these before I develop architecture options.
</template>
<wait-for-user>Get confirmation before proceeding.</wait-for-user>
</step>

<step id="4" title="Propose architecture structure">
<template>
Here's my proposed architecture approach:

## Core Components:
1. [Component A] - [purpose]
2. [Component B] - [purpose]
3. [Component C] - [purpose]

## Implementation Phases:
1. [Phase name] - [what it delivers]
2. [Phase name] - [what it delivers]

Does this structure align with your vision? Should I adjust?
</template>
<wait-for-user>Get confirmation before developing artifacts.</wait-for-user>
</step>

<step id="5" title="Develop 5 mandatory artifacts">
<critical>
YOU CANNOT PROCEED WITHOUT ALL 5 ARTIFACTS.
</critical>

<artifact id="1" name="Design Rationale and Evidence">
<purpose>Explain rationale and evidence: WHY exists? WHAT problems before? WHO depends? WHERE are landmines?</purpose>
<schema>
design_rationale:
  current_state:
    what_exists: [Component at file:line, purpose]
    how_it_got_here: [Git archaeology with commit SHA]
    dependencies: [Verified from code]
  problem_decomposition:
    core_problem: [Single sentence]
    sub_problems: [Specific technical challenges]
  hidden_complexity: [Non-obvious issues from patterns/history]
  success_criteria:
    automated: [Test commands, metrics]
    manual: [User verification steps]
</schema>
</artifact>

<artifact id="2" name="Tree of Thought Solutions">
<purpose>Generate EXACTLY 3 substantially different architectures.</purpose>
<schema>
tree_of_thought:
  solution_A:
    approach: [Name]
    description: [2-3 sentences]
    implementation: [Steps with file:line refs]
    patterns_used: [PAT:IDs with confidence ratings]
    pros: [Evidence-backed advantages]
    cons: [Specific limitations]
    complexity: [1-10 justified]
    risk: [LOW|MEDIUM|HIGH with reason]
  solution_B: [FUNDAMENTALLY different paradigm]
  solution_C: [ALTERNATIVE architecture]
  comparative_analysis:
    winner: [A|B|C]
    reasoning: [Why, with evidence]
    runner_up: [A|B|C]
    why_not_runner_up: [Specific limitation]
</schema>
</artifact>

<artifact id="3" name="Chain of Draft Evolution">
<purpose>Show thinking evolution through 3 drafts.</purpose>
<schema>
chain_of_draft:
  draft_1_raw:
    core_design: [Initial instinct]
    identified_issues: [Problems recognized]
  draft_2_refined:
    core_design: [Improved, pattern-guided]
    improvements: [What got better]
    remaining_issues: [Still problematic]
  draft_3_final:
    core_design: [Production-ready]
    why_this_evolved: [Journey from draft 1]
    patterns_integrated: [How patterns shaped design]
</schema>
</artifact>

<artifact id="4" name="YAGNI Declaration">
<purpose>Focus on production edge cases, exclude everything else.</purpose>
<schema>
yagni_declaration:
  explicitly_excluding:
    - feature: [Name]
      why_not: [Specific reason]
      cost_if_included: [Time/complexity]
      defer_until: [Trigger condition]
  preventing_scope_creep:
    - [Temptation]: [Why resisting]
  future_considerations:
    - [Enhancement]: [When makes sense]
  complexity_budget:
    allocated: [1-10]
    used: [By chosen solution]
    reserved: [Buffer]
</schema>
</artifact>

<artifact id="5" name="Pattern Selection Rationale">
<purpose>Justify every pattern choice with evidence.</purpose>

<critical>
YOU CANNOT FABRICATE PATTERNS.

Only use patterns that exist in:
- ctx.patterns (from research.pattern-library)
- ctx.impl (from research.codebase-patterns)

Before listing a pattern:
1. Verify it exists in the research section
2. Confirm confidence rating is from research, not invented
3. Document where in research you found it

VIOLATION: Claiming "PAT:NEW:THING" that wasn't in research
CONSEQUENCE: Final reflection becomes unreliable and confidence ratings become meaningless
</critical>

<intelligence-sources>
Check these sections for valid patterns:
- ctx.impl (reusable_snippets, project_conventions)
- ctx.patterns (pattern_cache.architecture)
- ctx.web (best_practices, official_docs)
- ctx.history (similar_tasks)
</intelligence-sources>

<schema>
pattern_selection:
  applying:
    - pattern_id: [PAT:CATEGORY:NAME]
      confidence_rating: [★★★★☆]
      usage_stats: [X uses, Y% success]
      why_this_pattern: [Specific fit]
      where_applying: [file:line]
      source: [ctx.patterns | ctx.impl | ctx.web]
  considering_but_not_using:
    - pattern_id: [PAT:ID]
      why_not: [Specific reason]
  missing_patterns:
    - need: [Gap identified]
      workaround: [Approach without pattern]
</schema>
</artifact>

</step>

<step id="6" title="Architecture checkpoint">
<template>
## Architecture Review Checkpoint

I've completed the 5 mandatory artifacts. Here's the selected architecture:

**Chosen Solution**: [Winner from Tree of Thought]
**Key Patterns**: [Top 3 patterns]
**Excluded Scope**: [Top 3 YAGNI items]
**Complexity**: [X/10]
**Risk Level**: [LOW|MEDIUM|HIGH]

**Implementation will**:
1. [Key outcome 1]
2. [Key outcome 2]

**Implementation will NOT**:
- [YAGNI item 1]
- [YAGNI item 2]

Should I proceed with the detailed architecture, or adjust any decisions?
</template>
<wait-for-user>Get confirmation before finalizing.</wait-for-user>
</step>

<step id="7" title="Generate architecture decision record">
<schema>
architecture_decision:
  decision: [Clear statement of chosen approach]
  files_to_modify:
    - path: [specific/file.ext]
      purpose: [Why changing]
      pattern: [PAT:ID applying]
      validation: [How to verify]
  files_to_create:
    - path: [new/file.ext]
      purpose: [Why needed]
      pattern: [PAT:ID template]
      test_plan: [Test approach]
  implementation_sequence:
    1. [Step with checkpoint]
    2. [Step with validation]
  validation_plan:
    automated: [Commands to run]
    manual: [User verification]
  potential_failures:
    - risk: [What could go wrong]
      mitigation: [Prevention strategy]
      detection: [Early warning]
</schema>
</step>

<step id="8" title="Write plan section to task file">
<output-format>
Append to `<plan>` section:

```xml
<plan>
<metadata>
  <timestamp>[ISO]</timestamp>
  <chosen-solution>[A|B|C]</chosen-solution>
  <complexity>[1-10]</complexity>
  <risk>[LOW|MEDIUM|HIGH]</risk>
</metadata>

<contract-validation>
  <contract-version>[N]</contract-version>
  <status>aligned|amended</status>
  <acceptance-criteria-coverage>
    <criterion id="AC-1">[How the plan will satisfy this AC]</criterion>
  </acceptance-criteria-coverage>
  <out-of-scope-confirmation>[Confirm no out-of-scope work is planned]</out-of-scope-confirmation>
  <amendments-made>
    <amendment version="[N]" reason="[Rationale or 'none']"/>
  </amendments-made>
</contract-validation>

<design-rationale>
  [Full artifact]
</design-rationale>

<tree-of-thought>
  <solution id="A">[Full details]</solution>
  <solution id="B">[Full details]</solution>
  <solution id="C">[Full details]</solution>
  <winner id="[X]" reasoning="[Why]"/>
</tree-of-thought>

<chain-of-draft>
  <draft id="1">[Raw design]</draft>
  <draft id="2">[Refined]</draft>
  <draft id="3">[Final]</draft>
</chain-of-draft>

<yagni>
  <excluding>[Features cut with reasons]</excluding>
  <scope-creep-prevention>[Temptations resisted]</scope-creep-prevention>
  <complexity-budget allocated="X" used="Y" reserved="Z"/>
</yagni>

<patterns>
  <applying>[Patterns with locations and justifications]</applying>
  <rejected>[Patterns considered but not used]</rejected>
</patterns>

<architecture-decision>
  <files-to-modify>[List with purposes and patterns]</files-to-modify>
  <files-to-create>[List with test plans]</files-to-create>
  <sequence>[Implementation order with checkpoints]</sequence>
  <validation>[Automated and manual checks]</validation>
  <risks>[Potential failures with mitigations]</risks>
</architecture-decision>

<builder-handoff>
  <mission>[Clear directive]</mission>
  <core-architecture>[Winner approach summary]</core-architecture>
  <pattern-guidance>[PAT:IDs with locations]</pattern-guidance>
  <implementation-order>[Numbered steps]</implementation-order>
  <validation-gates>[Checks after each step]</validation-gates>
  <warnings>[Critical risks and edge cases]</warnings>
</builder-handoff>

<next-steps>
Run `/apex:implement [identifier]` to begin implementation.
</next-steps>
</plan>
```
</output-format>

<update-frontmatter>
Set `phase: plan` and `updated: [ISO timestamp]`
</update-frontmatter>

</step>

</workflow>

<self-review-checklist>
- [ ] Design Rationale and Evidence: ALL hidden complexity identified?
- [ ] Tree of Thought: 3 FUNDAMENTALLY different solutions?
- [ ] Chain of Draft: REAL evolution shown?
- [ ] YAGNI: 3+ explicit exclusions?
- [ ] Patterns: Trust scores and usage stats included?
- [ ] Architecture decision: CONCRETE file paths?
- [ ] New files: Test plan included for each?
- [ ] Task contract validated with AC coverage and amendments recorded if any?

**If ANY unchecked → STOP and revise**
</self-review-checklist>

<success-criteria>
- All 5 artifacts completed with evidence
- User confirmed architecture decisions
- Research insights incorporated (ctx.* references used)
- Pattern selections justified with confidence ratings (NO fabricated patterns)
- 3 DISTINCT architectures in Tree of Thought
- YAGNI boundaries explicit
- Task contract validated; AC coverage documented; amendments (if any) recorded with version bump
- Implementation sequence concrete with validation
- Task file updated at ./.apex/tasks/[ID].md
- Checkpoints recorded at start and end
- Task metadata updated for architecture completion
- Architecture artifacts recorded in the task log
</success-criteria>

<next-phase>
`/apex:implement [identifier]` - Build and validate loop
</next-phase>

</skill>
