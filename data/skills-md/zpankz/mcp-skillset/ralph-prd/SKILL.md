---
name: ralph-prd
description: |
  Generates Product Requirements Documents for complex Ralph Loop tasks.
  Use when asked to "generate a PRD", "create product requirements", or
  "plan a ralph task". Delegates to prometheus agent for strategic planning.
allowed-tools: Read, Write, Grep, Glob, Bash
model: sonnet
context: fork
agent: ralph-domain-agent
user-invocable: true
---

# Ralph PRD Workflow

## Purpose

Generate structured Product Requirements Documents (PRDs) for complex Ralph Loop tasks. This skill helps break down large tasks into manageable phases with clear success criteria and exit conditions.

## Integrations

| Type | References |
|------|------------|
| skills | ralph-graceful-exit |
| agents | prometheus, metis |
| hooks | ralph-activity-log |

## PRD Template Structure

```json
{
  "title": "Task Title",
  "objective": "Clear goal statement",
  "success_criteria": [
    "Criterion 1: Specific, measurable outcome",
    "Criterion 2: Another measurable outcome"
  ],
  "phases": [
    {
      "name": "Phase 1: Discovery",
      "tasks": ["Task 1.1", "Task 1.2"],
      "completion": 0
    },
    {
      "name": "Phase 2: Implementation",
      "tasks": ["Task 2.1", "Task 2.2"],
      "completion": 0
    }
  ],
  "constraints": [
    "Constraint 1",
    "Constraint 2"
  ],
  "exit_conditions": [
    "All tests pass",
    "Documentation complete",
    "No regressions"
  ]
}
```

## Workflow

1. **Analyze task complexity** via metis agent
   - Identify scope and dependencies
   - Estimate effort per phase
   - Flag potential blockers

2. **Generate PRD JSON** via prometheus agent
   - Define clear objective
   - Break into phases
   - Set measurable success criteria

3. **Store PRD** in `.ralph/prd.json`
   - Create .ralph directory if needed
   - Validate JSON structure

4. **Track completion %** per iteration
   - Update phase completion as tasks finish
   - Log progress to ralph-activity-log

5. **Invoke ralph-graceful-exit** when criteria met
   - Check all success_criteria
   - Verify exit_conditions
   - Recommend completion

## Usage

### Generate PRD for New Task

```
/ralph-prd "Implement user authentication with OAuth2"
```

### Check PRD Progress

```
/ralph-prd status
```

### Update Phase Completion

```
/ralph-prd update --phase 1 --completion 100
```

## Progressive Loading

For detailed templates, see:
- [templates/default-prd.json](templates/default-prd.json) - Standard PRD template
- [templates/feature-prd.json](templates/feature-prd.json) - Feature-focused template
