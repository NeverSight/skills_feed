---
name: faion-backend-developer
description: "Backend orchestrator: coordinates systems (Go, Rust, DB) and enterprise (Java, C#, PHP, Ruby)."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Backend Developer Orchestrator

Coordinates two specialized backend sub-skills for systems-level and enterprise web development.

## Purpose

Routes backend tasks to appropriate sub-skill based on language and context.

## Sub-Skills

| Sub-skill | Focus | Methodologies |
|-----------|-------|---------------|
| **faion-backend-developer:systems** | Go, Rust, databases, caching | 22 |
| **faion-backend-developer:enterprise** | Java, C#, PHP, Ruby frameworks | 25 |

## Routing Logic

**Route to :systems for:**
- Go microservices, concurrency, HTTP handlers
- Rust backend services, async, ownership
- Database design, SQL optimization, NoSQL
- Caching strategies, message queues
- Low-level error handling

**Route to :enterprise for:**
- Java Spring Boot, JPA, Hibernate
- C# ASP.NET Core, Entity Framework
- PHP Laravel, Eloquent, queues
- Ruby Rails, ActiveRecord, Sidekiq
- Enterprise patterns and testing

## Integration

Invoked by parent skill `faion-software-developer` for backend work. Automatically selects appropriate sub-skill based on task context.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-python-developer | Python backends (Django, FastAPI) |
| faion-javascript-developer | Node.js backends |
| faion-api-developer | API design patterns |
| faion-testing-developer | Backend testing strategies |

---

*faion-backend-developer v1.0 | Orchestrator for 47 methodologies*
