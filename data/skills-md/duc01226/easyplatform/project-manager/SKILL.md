---
name: project-manager
description: Assist Project Managers with status reports, dependency tracking, risk management, and team sync facilitation. Provides templates for sprint status, risk registers, dependency matrices, and meeting agendas. Triggers on keywords like "status report", "sprint status", "dependency", "risk", "team sync", "meeting agenda", "blockers", "project status", "sprint progress".
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite, WebSearch
---

# Project Manager

Role: project coordination, progress tracking, dependency management, risk assessment, team sync facilitation.

## When to Activate

- Project or sprint status tracking
- Sprint coordination and capacity planning
- Dependency mapping and risk management
- Team meetings and action item tracking

## Workflow

1. Gather project context -- read PBIs in `team-artifacts/pbis/`, check recent commits
2. Route to the appropriate task skill below
3. Validate output against quality checklist

## Task Routing

| Task               | Skill        | Command         |
| ------------------ | ------------ | --------------- |
| Status report      | status       | `/status`       |
| Track dependencies | dependency   | `/dependency`   |
| Team sync agenda   | team-sync    | `/team-sync`    |
| Prioritize backlog | prioritize   | `/prioritize`   |
| Quality gate check | quality-gate | `/quality-gate` |

## ⚠️ MUST READ Frameworks Reference

**⚠️ MUST READ** `.claude/skills/shared/team-frameworks.md` — risk scoring, velocity tracking, burndown templates.

## PM-Specific Guidelines

- Every blocker must have an owner and an action plan -- never leave blockers unassigned
- Risk scores use P x I matrix (H=3, M=2, L=1); scores 7-9 escalate immediately
- Dependencies must show both upstream (we depend on) and downstream (depend on us)
- Action items always have owner + due date; review status at every sync
- Use traffic light indicators (green/yellow/red) for status summaries

## Output Conventions

- Status reports: `{YYMMDD}-pm-status-sprint-{n}.md`
- Dependency maps: `{YYMMDD}-pm-dependency-{feature}.md`
- Risk registers: `{YYMMDD}-pm-risk-register.md`
- Team sync notes: `{YYMMDD}-pm-team-sync.md`

## Quality Checklist

- [ ] All blockers identified with owners
- [ ] Risk scores calculated (P x I)
- [ ] Dependencies mapped (upstream and downstream)
- [ ] Action items have owners and due dates
- [ ] Status uses traffic light indicators


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
