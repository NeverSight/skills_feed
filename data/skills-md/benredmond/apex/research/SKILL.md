---
name: research
description: Intelligence gathering phase - spawns parallel agents to analyze codebase, patterns, git history, and web research. Creates or updates task file with findings.
argument-hint: [task-description|ticket-id|file-path|task-id]
---

<skill name="apex:research" phase="research">

<overview>
Conduct comprehensive research by orchestrating parallel sub-agents. Outputs to `./.apex/tasks/[ID].md`.

This is the **first phase** of the APEX workflow. It gathers all intelligence needed for planning and implementation.
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

<phase-gate requires="none" sets="research">
  <creates-file>./.apex/tasks/[ID].md</creates-file>
  <appends-section>research</appends-section>
</phase-gate>

<initial-response>
<if-no-arguments>
I'll conduct comprehensive research to gather intelligence and explore the codebase.

Please provide:
- Task description (e.g., "implement dark mode toggle")
- Linear/JIRA ticket ID (e.g., "APE-59")
- Path to task file (e.g., "./tickets/feature.md")
- Existing APEX task ID

I'll analyze patterns, explore the codebase, find similar tasks, and create a detailed research document.
</if-no-arguments>
<if-arguments>Immediately begin research - skip this message.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Parse input and identify task">
<instructions>
Determine input type and create/find task:

**Text description**: Create a task entry with intent, inferred type, generated identifier, and tags
**Ticket ID (APE-59)**: Fetch ticket details (if available), then create a task entry with identifier set to ticket ID
**File path**: Read file fully, parse content, then create a task entry
**Database ID**: Look up existing task by ID to retrieve it

Store `taskId` and `identifier` for all subsequent operations.
</instructions>
</step>

<step id="2" title="Optimize and improve prompt">
<purpose>
Vague task briefs lead to wasted research effort. Enhance before proceeding.
</purpose>

<optimization-steps>
1. **Clarify Intent**: What is the user REALLY trying to accomplish?
   - Look for implicit goals behind explicit requests
   - Identify the "why" behind the "what"

2. **Add Specificity**: Transform vague terms into concrete requirements
   - "improve performance" → "reduce API response time below 200ms"
   - "fix the bug" → "prevent null pointer when user has no profile"

3. **Structure Requirements**: Break into testable acceptance criteria
   - Given [context], When [action], Then [expected result]

4. **Include Testing**: How will we verify success?
   - Unit test expectations
   - Integration test scenarios
   - Manual verification steps

5. **Pattern Enhancement**: Check existing patterns or similar past tasks
   - What worked before?
   - What failed and why?
</optimization-steps>

<enhanced-prompt-format>
```yaml
original_prompt: "[User's original request]"
enhanced_prompt:
  intent: "[Clarified goal]"
  scope:
    in: ["[Specific inclusions]"]
    out: ["[Explicit exclusions]"]
  acceptance_criteria:
    - "[Testable criterion 1]"
    - "[Testable criterion 2]"
  success_metrics:
    - "[Measurable outcome]"
  related_patterns: ["[PAT:IDs from quick lookup]"]
```
</enhanced-prompt-format>
</step>

<step id="3" title="Read mentioned files FULLY">
<critical>
Before ANY analysis or spawning agents:
- If user mentions specific files, READ THEM FULLY first
- Use Read tool WITHOUT limit/offset parameters
- Read in main context BEFORE spawning sub-tasks
- This ensures full context before decomposing research
</critical>
</step>

<step id="4" title="Triage scan + Ambiguity Gate (Pre-Agents)">
<purpose>
Run a low-cost scan to reduce ambiguity before spawning deep research agents.
</purpose>

<triage-scan>
- Run cheap `rg` scans to locate entrypoints, tests, and likely target areas:
  - `rg -n "main|entry|cli|index\\.(ts|js)|server\\.(ts|js)" src`
  - `rg -n "describe\\(|it\\(" tests`
  - `rg -n "[task keywords]" src tests docs` (derive keywords from enhanced_prompt)
- Capture candidate files/areas to refine scope.
- Do NOT open large files unless the user explicitly mentioned them.
- Use this scan ONLY to detect ambiguity and shape clarifying questions.
</triage-scan>

<critical>
Ambiguity is a BLOCKING condition that ONLY users can resolve.
DO NOT spawn deep research agents with unclear requirements.
</critical>

<ambiguity-checklist>
Check for these ambiguity indicators:

**Vague Goals**:
- "improve", "enhance", "optimize" without metrics
- "fix the bug" without reproduction steps
- "make it better" without criteria

**Unclear Scope**:
- No defined boundaries (what's in/out)
- Multiple interpretations possible
- Triage scan surfaces multiple plausible entrypoints/tests

**Technical Choices**:
- Triage scan shows multiple candidate libraries/approaches
- Architecture decisions user should make
- Technology/library selection needed

**Missing Constraints**:
- No performance requirements
- No security requirements specified
- No compatibility requirements
</ambiguity-checklist>

<assessment-logic>
```python
def assess_ambiguity(enhanced_prompt, triage_scan):
    ambiguities = []

    # Check each category
    if has_vague_goals(enhanced_prompt):
        ambiguities.append({"type": "vague_goal", "question": "..."})

    if has_unclear_scope(enhanced_prompt, triage_scan):
        ambiguities.append({"type": "unclear_scope", "question": "..."})

    if needs_technical_choice(triage_scan):
        ambiguities.append({"type": "technical_choice", "question": "..."})

    if missing_constraints(enhanced_prompt):
        ambiguities.append({"type": "missing_constraint", "question": "..."})

    return ambiguities
```
</assessment-logic>

<decision>
- **0 ambiguities**: PROCEED to spawn parallel research agents
- **1+ ambiguities**: ASK USER before spawning deep research agents

**Question Format**:
```
Before I spawn deep research agents, I need to clarify:

[For each ambiguity, ONE focused question]

1. **[Category]**: [Specific question]?
   - Option A: [Choice with implication]
   - Option B: [Choice with implication]
   - Option C: [Let me know your preference]
```
</decision>

<max-rounds>
Maximum 1 clarification round. After user responds:
- Incorporate answers into enhanced_prompt
- Proceed to spawn parallel research agents (do NOT ask more questions)
</max-rounds>
</step>

<step id="5" title="Create task file">
<instructions>
Create `./.apex/tasks/[identifier].md` with frontmatter:

```markdown
---
id: [database_id]
identifier: [identifier]
title: [Task title]
created: [ISO timestamp]
updated: [ISO timestamp]
phase: research
status: active
---

# [Title]

<research>
<!-- Will be populated by this skill -->
</research>

<plan>
<!-- Populated by /apex:plan -->
</plan>

<implementation>
<!-- Populated by /apex:implement -->
</implementation>

<ship>
<!-- Populated by /apex:ship -->
</ship>
```
</instructions>
</step>

<step id="6" title="Spawn parallel research agents">
<critical>
Use the clarified enhanced_prompt (post-ambiguity resolution) as the source of truth for all agent prompts.
</critical>
<agents parallel="true">

<agent type="intelligence-gatherer" required="true">
**Task ID**: [taskId]
**Research Focus**: [User's question/area]

Discover relevant patterns, find similar tasks, identify predicted failures, generate execution strategy.
Return: Context pack with pattern intelligence.
</agent>

<agent type="implementation-pattern-extractor" required="true">
**Task Context**: [Brief description]
**Task Type**: [bug|feature|refactor|test]

Extract concrete implementation patterns from THIS codebase with file:line references.
Return: YAML with primary patterns, conventions, reusable snippets, testing patterns.
</agent>

<agent type="web-researcher" required="true">
**Research Topic**: [Component/Technology/Pattern]
**Context**: [What we're trying to accomplish]

Find official documentation, best practices, security concerns, recent changes.
Return: YAML with official_docs, best_practices, security_concerns, recent_changes.
</agent>

<agent type="apex:git-historian" required="true">
**Scope**: [files/directories]
**Window**: 9 months

Analyze git history for similar changes, regressions, ownership.
Return: Structured git intelligence.
</agent>

<agent type="apex:documentation-researcher" required="true">
**Scope**: Project markdown documentation
**Focus**: [Task-relevant topics]

Search project docs for:
- Architecture context and design decisions
- Past decisions and rationale (ADRs)
- Historical learnings and gotchas
- Related documentation that may need updating

Return: YAML with architecture_context, past_decisions, historical_learnings, docs_to_update.
</agent>

<agent type="learnings-researcher" required="true">
**Task Intent**: [Enhanced prompt intent]
**Keywords**: [Extracted keywords from task]

Search past task files (.apex/tasks/*.md) for:
- Problems solved and how they were fixed
- Decisions made with rationale
- Gotchas and surprising discoveries
- Related tasks via related_tasks links

Return: YAML with top 5 relevant learnings ranked by relevance score.
</agent>

<agent type="apex:systems-researcher" signal-based="true">
**Trigger**: Cross-component changes, architectural impacts
**Focus Area**: [Component or subsystem]

Trace execution flow, dependencies, state transitions, integration points.
</agent>

<agent type="apex:risk-analyst" signal-based="true">
**Trigger**: Complexity >= 7, production-critical, security-sensitive

Surface forward-looking risks, edge cases, monitoring gaps, mitigations.
</agent>

</agents>

<wait-for-all>CRITICAL: Wait for ALL agents to complete before proceeding.</wait-for-all>
</step>

<step id="7" title="Synthesize findings">
<priority-order>
1. Live codebase = primary truth (what actually exists)
2. Implementation patterns = concrete project conventions
3. Official documentation = authoritative reference
4. Pattern library = proven cross-project solutions
5. Best practices = industry consensus
6. Git history = evolution understanding
</priority-order>

<synthesis-tasks>
- Validate pattern library findings against actual codebase
- Cross-reference with official docs
- Identify gaps between current code and recommendations
- Flag inconsistencies and deprecated patterns
- Note security concerns
- Resolve contradictions (codebase > docs > patterns > opinions)
</synthesis-tasks>
</step>

<step id="8" title="Display Intelligence Report">
<purpose>Give user visibility into gathered intelligence before the technical adequacy gate.</purpose>

<display-format>
```
## Intelligence Report

**Task**: [Title]
**Agents Deployed**: [N]
**Files Analyzed**: [X]

### Baseline Metrics
- Complexity estimate: [1-10]
- Risk level: [Low/Medium/High]
- Pattern coverage: [X patterns found, Y% high-trust]

### Pattern Intelligence
- High-trust patterns (★★★★☆+): [N] patterns applicable
- Similar past tasks: [N] found, [X]% success rate
- Predicted failure points: [N] identified

### Historical Intelligence
- Related commits: [N] in last 9 months
- Previous attempts: [List any failed/reverted changes]
- Key maintainers: [Names/areas]

### Execution Strategy
- Recommended approach: [Brief]
- Parallelization opportunities: [Yes/No]
- Estimated scope: [Small/Medium/Large]

### Key Insights
1. [Most important finding]
2. [Second most important]
3. [Third most important]
```
</display-format>
</step>

<step id="9" title="Technical Adequacy Gate (Phase 2)">
<purpose>
Verify we have sufficient intelligence to architect a solution.
</purpose>

<scoring-dimensions>
**Technical Context (30% weight)**:
- [ ] Primary files identified with line numbers
- [ ] Dependencies mapped
- [ ] Integration points documented
- [ ] Current behavior understood

**Risk Assessment (20% weight)**:
- [ ] Security concerns identified
- [ ] Performance implications assessed
- [ ] Breaking change potential evaluated
- [ ] Rollback strategy considered

**Dependency Mapping (15% weight)**:
- [ ] Upstream dependencies known
- [ ] Downstream consumers identified
- [ ] External API constraints documented
- [ ] Version compatibility checked

**Pattern Availability (35% weight)**:
- [ ] Relevant patterns found (confidence ≥ 0.5)
- [ ] Similar past tasks reviewed
- [ ] Implementation patterns from codebase extracted
- [ ] Anti-patterns identified to avoid
</scoring-dimensions>

<confidence-calculation>
```python
def calculate_adequacy(checklist_results):
    weights = {
        "technical_context": 0.30,
        "risk_assessment": 0.20,
        "dependency_mapping": 0.15,
        "pattern_availability": 0.35
    }

    score = sum(
        weights[dim] * (checked / total)
        for dim, (checked, total) in checklist_results.items()
    )

    return score  # 0.0 to 1.0
```
</confidence-calculation>

<decision-thresholds>
- **≥ 0.8**: PROCEED to Tree of Thought
- **0.6-0.8**: PROCEED with caution, note gaps
- **< 0.6**: INSUFFICIENT - spawn recovery agents or escalate

**If INSUFFICIENT**:
```
## Insufficient Context

Adequacy Score: [X]% (threshold: 60%)

**Gaps Identified**:
- [Dimension]: [What's missing]

**Recovery Options**:
1. Spawn additional agents for [specific gap]
2. Ask user for [specific information]
3. Proceed with documented limitations

Which approach should I take?
```
</decision-thresholds>
</step>

<step id="10" title="Generate Tree of Thought recommendations">
<instructions>
Produce exactly 3 distinct solution approaches:

**Solution A**: [Approach name]
- Philosophy, implementation path, pros, cons, risk level

**Solution B**: [Different paradigm]
- Philosophy, implementation path, pros, cons, risk level

**Solution C**: [Alternative architecture]
- Philosophy, implementation path, pros, cons, risk level

**Comparative Analysis**: Winner with reasoning, runner-up with why not
</instructions>
</step>

<step id="11" title="Write research section to task file">
<output-format>
Append to `<research>` section:

```xml
<research>
<metadata>
  <timestamp>[ISO]</timestamp>
  <agents-deployed>[N]</agents-deployed>
  <files-analyzed>[X]</files-analyzed>
  <confidence>[0-10]</confidence>
  <adequacy-score>[0.0-1.0]</adequacy-score>
  <ambiguities-resolved>[N]</ambiguities-resolved>
</metadata>

<context-pack-refs>
  <!-- Shorthand for downstream phases -->
  ctx.patterns = pattern-library section
  ctx.impl = codebase-patterns section
  ctx.web = web-research section
  ctx.history = git-history section
  ctx.docs = documentation section (from documentation-researcher)
  ctx.learnings = past-learnings section (from learnings-researcher)
  ctx.risks = risks section
  ctx.exec = recommendations.winner section
</context-pack-refs>

<executive-summary>
[2-3 paragraphs synthesizing ALL findings]
</executive-summary>

<web-research>
  <official-docs>[Key findings with URLs]</official-docs>
  <best-practices>[Practices with sources]</best-practices>
  <security-concerns>[Issues with severity and mitigation]</security-concerns>
  <gap-analysis>[Codebase vs recommendations]</gap-analysis>
</web-research>

<codebase-patterns>
  <primary-pattern location="file:line">[Description with code snippet]</primary-pattern>
  <conventions>[Naming, structure, types, error handling]</conventions>
  <reusable-snippets>[Copy-pasteable code with sources]</reusable-snippets>
  <testing-patterns>[How similar features are tested]</testing-patterns>
  <inconsistencies>[Multiple approaches found]</inconsistencies>
</codebase-patterns>

<pattern-library>
  <pattern id="PAT:X:Y" confidence="★★★★☆" uses="N" success="X%">[Relevance]</pattern>
  <anti-patterns>[Patterns to avoid with reasons]</anti-patterns>
</pattern-library>

<documentation>
  <architecture-context>[Relevant architecture docs found]</architecture-context>
  <past-decisions>[ADRs and design decisions]</past-decisions>
  <historical-learnings>[Gotchas and lessons from docs]</historical-learnings>
  <docs-to-update>[Files that may need updating after this task]</docs-to-update>
</documentation>

<past-learnings>
  <count>[Number of relevant learnings found]</count>
  <coverage>[EXCELLENT|GOOD|SPARSE|NONE]</coverage>
  <learnings>
    <learning task-id="[ID]" relevance="[0.0-1.0]">
      <title>[Task title]</title>
      <summary>[Why this is relevant and what's useful]</summary>
      <problems>[Problems solved, if any]</problems>
      <decisions>[Decisions made, if any]</decisions>
      <gotchas>[Gotchas discovered, if any]</gotchas>
    </learning>
  </learnings>
  <patterns-across>[Common themes from multiple past tasks]</patterns-across>
</past-learnings>

<git-history>
  <similar-changes>[Commits with lessons]</similar-changes>
  <evolution>[How code got here]</evolution>
</git-history>

<risks>
  <risk probability="H|M|L" impact="H|M|L">[Description with mitigation]</risk>
</risks>

<recommendations>
  <solution id="A" name="[Name]">
    <philosophy>[Core principle]</philosophy>
    <path>[Implementation steps]</path>
    <pros>[Advantages]</pros>
    <cons>[Disadvantages]</cons>
    <risk-level>[Low|Medium|High]</risk-level>
  </solution>
  <solution id="B" name="[Name]">...</solution>
  <solution id="C" name="[Name]">...</solution>
  <winner id="[A|B|C]" reasoning="[Why]"/>
</recommendations>

<task-contract version="1">
  <intent>[Single-sentence intent]</intent>
  <in-scope>[Explicit inclusions]</in-scope>
  <out-of-scope>[Explicit exclusions]</out-of-scope>
  <acceptance-criteria>
    <criterion id="AC-1">Given..., When..., Then...</criterion>
  </acceptance-criteria>
  <non-functional>
    <performance>[Performance constraints]</performance>
    <security>[Security constraints]</security>
    <compatibility>[Compatibility constraints]</compatibility>
  </non-functional>
  <amendments>
    <!-- Append amendments in plan/implement/ship with explicit rationale and version bump -->
  </amendments>
</task-contract>

<next-steps>
Run `/apex:plan [identifier]` to create architecture from these findings.
</next-steps>
</research>
```
</output-format>

<update-frontmatter>
Set `updated: [ISO timestamp]` and verify `phase: research`
</update-frontmatter>
</step>

</workflow>

<success-criteria>
- Prompt optimized and enhanced with specificity
- All mentioned files read fully
- Triage scan completed and ambiguity resolved before spawning agents
- All parallel agents completed (including documentation-researcher, learnings-researcher)
- Implementation patterns extracted with file:line refs
- Web research validated against official docs
- Patterns analyzed with confidence ratings
- Documentation context gathered
- Past learnings searched and top 5 relevant included
- Git history examined
- Intelligence report displayed to user
- Ambiguity detection completed (0 ambiguities OR user clarified)
- Technical adequacy score ≥ 0.6
- 3 solution approaches generated (Tree of Thought)
- Risks identified with mitigations
- Task contract created with intent, scope, ACs, and NFRs
- Task file created/updated at ./.apex/tasks/[ID].md
- Context pack refs documented for downstream phases
</success-criteria>

<next-phase>
`/apex:plan [identifier]` - Architecture and design decisions
</next-phase>

</skill>
