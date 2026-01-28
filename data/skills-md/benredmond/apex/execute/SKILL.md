---
name: execute
description: Orchestrator that runs the full APEX workflow (research → plan → implement → ship) in a single session. Use for tasks you want to complete without context switches.
argument-hint: [task-description|ticket-id|file-path]
---

<skill name="apex:execute" phase="orchestrator">

<overview>
Meta-skill that chains all 4 APEX phases in sequence:

1. `/apex:research` - Intelligence gathering
2. `/apex:plan` - Architecture design
3. `/apex:implement` - Build and validate
4. `/apex:ship` - Review and reflect

Use this for single-session task completion. For multi-session work, invoke individual skills.
</overview>

<when-to-use>
- Small to medium tasks that fit in one session
- When you don't need to pause between phases
- When you want full workflow without manual skill invocation
</when-to-use>

<when-not-to-use>
- Large complex tasks that need human review between phases
- When you want to pause after research to think
- When context overflow is likely
- When you want to run phases in separate sessions
</when-not-to-use>

<initial-response>
<if-no-arguments>
I'll run the full APEX workflow. Please provide:
- Task description (e.g., "implement dark mode toggle")
- Ticket ID (e.g., "APE-59")
- Path to task file

Example: `/apex:execute "add user authentication"`
</if-no-arguments>
<if-arguments>Begin full workflow.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Research phase">
<invoke skill="apex:research">
Pass the original input argument.
</invoke>

<verify>
- Task file created at ./.apex/tasks/[ID].md
- Frontmatter shows phase: research
- `<research>` section populated
</verify>

<extract>
Store `identifier` for subsequent skill invocations.
</extract>

<on-failure>
Stop and report: "Research phase failed. See task file for details."
</on-failure>
</step>

<step id="2" title="Plan phase">
<invoke skill="apex:plan">
Pass the identifier from step 1.
</invoke>

<verify>
- Frontmatter shows phase: plan
- `<plan>` section populated
- 5 mandatory artifacts present
</verify>

<on-needs-input>
Plan phase is interactive. If user input needed:
1. Present the question to user
2. Get response
3. Continue plan phase with response
</on-needs-input>

<on-failure>
Stop and report: "Plan phase failed. Run `/apex:plan [identifier]` to retry."
</on-failure>
</step>

<step id="3" title="Implement phase">
<invoke skill="apex:implement">
Pass the identifier.
</invoke>

<verify>
- Frontmatter shows phase: implement
- `<implementation>` section populated
- All tests passing
</verify>

<on-failure>
If tests failing after max retries:
1. Report current state
2. Ask user: "Implementation has issues. Continue to ship (will document issues) or stop here?"
3. If stop, leave task in implement phase for manual intervention
</on-failure>
</step>

<step id="4" title="Ship phase">
<invoke skill="apex:ship">
Pass the identifier.
</invoke>

<verify>
- Frontmatter shows phase: complete, status: complete
- `<ship>` section populated
- Git commit created
- Reflection recorded
</verify>

<on-failure>
Stop and report: "Ship phase failed. Run `/apex:ship [identifier]` to retry."
</on-failure>
</step>

<step id="5" title="Final report">
<template>
## APEX Workflow Complete ✅

**Task**: [Title]
**File**: ./.apex/tasks/[identifier].md

### Phases Completed:
1. ✅ Research - [summary]
2. ✅ Plan - [chosen architecture]
3. ✅ Implement - [files changed, tests status]
4. ✅ Ship - [commit SHA, reflection status]

### Metrics:
- Total patterns applied: [N]
- Tests: [passed]/[total]
- Review findings: [N] ([dismissed]% false positives)
- Commit: [SHA]

### Key Learning:
[From reflection]

Task complete. Full history in `./.apex/tasks/[identifier].md`
</template>
</step>

</workflow>

<error-handling>

<phase-failure>
If any phase fails:
1. Report which phase failed
2. Report current state of task file
3. Suggest manual intervention: "Run `/apex:[phase] [identifier]` to retry"
4. Do NOT continue to next phase
</phase-failure>

<user-input-needed>
If any phase needs user input:
1. Present the question
2. Wait for response
3. Continue that phase with response
4. Do NOT skip the interaction
</user-input-needed>

<context-overflow>
If context is getting large:
1. Warn user: "Context is large. Consider continuing in new session."
2. Report current phase and identifier
3. User can restart with individual skill from current phase
</context-overflow>

</error-handling>

<success-criteria>
- All 4 phases completed successfully
- Task file shows phase: complete, status: complete
- Git commit exists
- Reflection recorded
- Final report displayed to user
</success-criteria>

</skill>
