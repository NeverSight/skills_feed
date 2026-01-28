---
name: solution-design
description: Invoke IMMEDIATELY via python script when user has a defined problem or root cause and needs solution options. Generates diverse solutions from multiple reasoning perspectives. Do NOT explore first - the script orchestrates the solution generation workflow.
---

# Solution Design

When this skill activates, IMMEDIATELY invoke the script. The script IS the
workflow.

This skill generates solutions for a defined problem or root cause. It does NOT
identify problems or perform root cause analysis--use problem-analysis for that.

## Invocation

<invoke working-dir=".claude/skills/scripts" cmd="python3 -m skills.solution_design.design --step 1 --total-steps 9" />

Do NOT explore or analyze first. Run the script and follow its output.
