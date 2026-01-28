---
name: project-planning
description: Guides comprehensive software project planning including task breakdown, estimation, sprint planning, backlog management, resource allocation, milestone tracking, and risk management. Creates user stories, acceptance criteria, project roadmaps, and work breakdown structures. Use when planning software projects, organizing sprints, breaking down features into tasks, estimating effort, managing backlogs, or when users mention "project planning", "sprint planning", "task breakdown", "roadmap", "backlog management", "user stories", or "project estimation".
---

# Project Planning

## Overview

This skill provides comprehensive guidance for planning and managing software projects using industry best practices. It covers breaking down requirements into manageable tasks, estimating effort, organizing sprints, managing backlogs, and tracking progress effectively.

**Key Principles:**

- Adapt practices to team size and project complexity
- Start simple, add complexity as needed
- Focus on delivering value, not following process
- Regular inspection and adaptation are key
- Maintain sustainable pace, avoid burnout

## Planning Workflow

Follow this workflow when planning software projects:

## 1. Define Project Scope

- **Vision Statement**: Clear project purpose and objectives
- **Success Criteria**: Measurable outcomes that define success
- **Stakeholders**: Identify all stakeholders and their roles
- **Constraints**: Budget, timeline, resources, technical limitations
- **Deliverables**: Core features, documentation, training materials

### 2. Break Down Requirements

- Transform requirements into epics (large bodies of work)
- Break epics into user stories: "As a [role], I want [feature] so that [benefit]"
- Create technical tasks from user stories
- Define acceptance criteria for each story

### 3. Estimate Effort

- Use story points (Fibonacci: 1, 2, 3, 5, 8, 13) for relative sizing
- Conduct planning poker for team consensus
- Apply three-point estimation for critical/uncertain tasks

### 4. Organize and Prioritize

- Group work into sprints (1-4 weeks)
- Prioritize using MoSCoW (Must/Should/Could/Won't) or Value vs. Effort
- Manage backlog with clear prioritization tiers: Now, Next, Later, Backlog

### 5. Track and Adjust

- Monitor sprint progress and velocity
- Identify and manage risks (technical, schedule, resource, external)
- Conduct regular retrospectives and adapt practices

## User Story Format

```markdown
**Title**: [Action] as [Role]

**As a** [user type]
**I want** [goal/feature]
**So that** [business value/benefit]

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

**Priority**: [High/Medium/Low]
**Estimated Effort**: [X story points]
**Dependencies**: [List any dependencies]
```

## Story Point Sizing Guide

- **1 point**: Trivial change, < 2 hours, no complexity
- **2 points**: Simple task, 2-4 hours, well understood
- **3 points**: Small feature, 4-8 hours, some complexity
- **5 points**: Medium feature, 1-2 days, moderate complexity
- **8 points**: Large feature, 2-3 days, significant complexity
- **13+ points**: Too large - must be broken down

## Bundled Resources

### References (references/)

Load these on-demand for detailed guidance:

- **core-planning-workflow.md**: Complete project setup process, requirements breakdown techniques, estimation methods, sprint planning procedures, and velocity tracking (load when planning new projects or setting up processes)

- **backlog-not-prioritized.md**: Backlog organization (Now/Next/Later/Backlog), Definition of Ready/Done, prioritization frameworks (MoSCoW, RICE, Value vs. Effort), and refinement practices (load when organizing or refining backlogs)

- **now-sprint-ready.md**, **next-2-3-sprints.md**, **later-future.md**: Criteria for different backlog tiers and work item organization strategies (load when categorizing backlog items by timeline)

- **task-management-best-practices.md**: Task attributes, dependency management, critical path analysis, status updates, and decision logging (load when managing task execution and tracking)

- **schedule-risks.md**: Schedule risk identification, assessment, and mitigation strategies (load when dealing with timeline concerns or delays)

- **technical-risks.md**: Technical risk identification, assessment, and handling strategies (load when dealing with technical uncertainties or architecture decisions)

- **external-dependencies.md**: Managing third-party dependencies, tracking, communication, and mitigation strategies for external blockers (load when dealing with vendor or partner dependencies)

- **templates-and-checklists.md**: Project kickoff checklist, user story templates, sprint planning templates, task breakdown templates, and status report formats (load when creating deliverables or standardizing artifacts)

- **anti-patterns-to-avoid.md**: Common planning mistakes, warning signs of project issues, and best practices (load when troubleshooting project problems or conducting retrospectives)

- **integration-with-development-workflow.md**: Integrating planning with development processes and CI/CD considerations (load when connecting planning to technical workflows)
