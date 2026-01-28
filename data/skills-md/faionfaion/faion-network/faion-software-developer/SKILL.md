---
name: faion-software-developer
description: "Full-stack development: Python, JavaScript, Go, APIs, testing, frontend."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Software Developer Orchestrator

Coordinates 7 specialized sub-skills for comprehensive software development.

## Purpose

Routes development tasks to appropriate specialized sub-skills based on technology, domain, and task type.

## Sub-Skills

| Sub-skill | Methodologies | Focus |
|-----------|---------------|-------|
| faion-python-developer | 24 | Django, FastAPI, async, pytest, type hints |
| faion-javascript-developer | 18 | React, Node.js, Next.js, TypeScript, Bun |
| faion-backend-developer | 47 | Go, Rust, Java, C#, PHP, Ruby, databases |
| faion-frontend-developer | 18 | Tailwind, CSS-in-JS, design tokens, PWA, a11y |
| faion-api-developer | 19 | REST, GraphQL, OpenAPI, auth, versioning |
| faion-testing-developer | 12 | Unit, integration, E2E, TDD, mocking |
| faion-devtools-developer | 46 | Automation, architecture, code quality, CI/CD |

**Total:** 184 methodologies across 7 sub-skills

## Routing Logic

| Task Type | Route To |
|-----------|----------|
| Python/Django/FastAPI code | faion-python-developer |
| JavaScript/TypeScript/React/Node.js code | faion-javascript-developer |
| Go/Rust/Java/C#/PHP/Ruby code | faion-backend-developer |
| Database design, caching | faion-backend-developer |
| Tailwind/CSS/UI libraries | faion-frontend-developer |
| Design tokens, PWA, accessibility | faion-frontend-developer |
| REST/GraphQL API design | faion-api-developer |
| API auth, versioning, rate limiting | faion-api-developer |
| Testing (any type) | faion-testing-developer |
| Browser automation, web scraping | faion-devtools-developer |
| Code review, refactoring | faion-devtools-developer |
| Architecture patterns (DDD, CQRS) | faion-devtools-developer |
| CI/CD, monorepo, tooling | faion-devtools-developer |

## Multi-Skill Tasks

For tasks spanning multiple domains, coordinate relevant sub-skills:

**Full-stack Python app:**
1. faion-python-developer (backend)
2. faion-api-developer (API design)
3. faion-frontend-developer (UI)
4. faion-testing-developer (tests)

**React + Node.js app:**
1. faion-javascript-developer (React + Node.js)
2. faion-frontend-developer (styling)
3. faion-api-developer (API)
4. faion-testing-developer (tests)

**Microservices architecture:**
1. faion-backend-developer (services in Go/Rust/Java)
2. faion-api-developer (API gateway)
3. faion-devtools-developer (architecture patterns)
4. faion-testing-developer (integration tests)

## Agents

| Agent | Purpose |
|-------|---------|
| faion-code-agent | Code generation and review |
| faion-test-agent | Test generation and execution |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-net | Parent orchestrator for all projects |
| faion-software-architect | Architecture design decisions |
| faion-devops-engineer | Deployment, infrastructure |
| faion-ml-engineer | AI/ML integrations |
| faion-sdd | Specification-driven development |

## Usage

Invoked via `/faion-net` or directly as `/faion-software-developer`. Automatically routes to appropriate sub-skill.

---

*faion-software-developer v2.0 | Orchestrator | 7 sub-skills | 184 methodologies*
