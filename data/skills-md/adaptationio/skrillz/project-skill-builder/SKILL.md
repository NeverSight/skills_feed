---
name: project-skill-builder
description: Create project-specific Claude Code skills tailored to particular codebases, domains, or organizations. Workflow for analyzing project context, identifying skill opportunities, designing project-specific patterns, and building custom skills. Use when creating skills for specific projects, capturing project knowledge, building team-specific workflows, or developing domain-specific skill toolkits.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Project Skill Builder

## Overview

project-skill-builder helps create skills tailored to specific projects, codebases, or organizational contexts by combining universal skill patterns with project-specific knowledge.

**Purpose**: Build skills customized for specific project needs

**Approach**: Universal patterns (from skill-builder-generic) + Project-specific knowledge = Custom skills

**Project Skill Builder Workflow** (5 steps):
1. **Analyze Project Context** - Understand codebase, patterns, domain, team needs
2. **Identify Skill Opportunities** - Where would skills add most value?
3. **Design Project Patterns** - Adapt universal patterns to project specifics
4. **Build Custom Skill** - Use development-workflow with project context
5. **Validate and Deploy** - Test in project, validate effectiveness

## When to Use

- Creating skills for specific codebase patterns
- Capturing team knowledge in skills
- Building domain-specific workflows
- Project onboarding automation
- Team-specific development patterns

## Workflow

### Step 1: Analyze Project Context

**Understand**:
- Codebase architecture and patterns
- Tech stack and conventions
- Team workflows and practices
- Domain-specific requirements
- Common pain points

**Output**: Project context document

---

### Step 2: Identify Skill Opportunities

**Find**:
- Repetitive tasks (automation opportunities)
- Undocumented knowledge (capture in skills)
- Team workflows (standardization opportunities)
- Onboarding needs (knowledge transfer)

**Output**: Skill opportunity list (prioritized)

---

### Step 3: Design Project Patterns

**Adapt**:
- Universal patterns → Project-specific implementations
- Generic examples → Project-specific examples
- Standard workflows → Team workflows

**Output**: Project-specific skill design

---

### Step 4: Build Custom Skill

**Use**: development-workflow with project context
- Research: Project patterns (not generic)
- Planning: Project-specific architecture
- Implementation: Project examples and workflows

**Output**: Project-specific skill

---

### Step 5: Validate and Deploy

**Test**: In actual project context
**Validate**: Effective for team/project
**Deploy**: To project .claude/skills/

**Output**: Deployed, validated project skill

---

## Examples

**Project-Specific Skill Types**:
- API integration workflows (project's specific APIs)
- Deployment procedures (project's infrastructure)
- Code patterns (project's architecture patterns)
- Testing frameworks (project's test setup)
- Review checklists (team's review standards)

---

## Quick Reference

### Workflow

```
Analyze Project → Identify Opportunities → Design Patterns →
Build with development-workflow → Validate in Project
```

### Integration

**Uses**: development-workflow, skill-researcher (for project patterns)
**Produces**: Project-specific skills
**Deploys to**: .claude/skills/ in project repository

---

**project-skill-builder enables creation of skills tailored to specific project needs and team contexts.**
