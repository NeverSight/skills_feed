---
name: backend-developer
description: Use when designing APIs, Architecture, Security, or Scalability for Node, Python, Go, or Java backend systems.
license: MIT
metadata:
  version: "2.0"
  capabilities:
    ["API Design", "System Architecture", "Security", "Polyglot Development"]
  languages: ["Node.js", "Python", "Go", "Java", "Kotlin"]
  databases: ["PostgreSQL", "MongoDB", "Redis"]
---

# Backend Development Standards

This skill provides expert guidelines for building robust, scalable, and secure distributed systems.

## Core Philosophy

1.  **Documentation is Truth**: Never guess syntax or patterns. If unsure, use `search_web` to find official docs.
2.  **Security First**: Every input is malicious until validated. Every endpoint needs explicit AuthN/AuthZ.
3.  **Simplicity**: Prefer boring technology that works. Complexity must be justified.

## 1. Dynamic Context Loading

**CRITICAL STEP**: Before helping the user, you MUST identify the specific technology stack.

**Logic:**

1.  Check the user's request and open files.
2.  **Load the relevant references** using `view_file`.

| Detected Stack                | Files to Load                    |
| :---------------------------- | :------------------------------- |
| **Architectural / DB Design** | `references/general-patterns.md` |
| **Node.js (Express)**         | `references/node-express.md`     |
| **Node.js (NestJS)**          | `references/node-nestjs.md`      |
| **Python (Django)**           | `references/python-django.md`    |
| **Python (FastAPI)**          | `references/python-fastapi.md`   |
| **Go (Gin)**                  | `references/go-gin.md`           |
| **Go (Echo)**                 | `references/go-echo.md`          |
| **Java (Spring Boot)**        | `references/java-springboot.md`  |

> [!NOTE]
> If the user asks a general question (e.g., "How do I secure my API?"), load `references/general-patterns.md`.

## 2. Core Responsibilities

### A. API Design (Contract First)

- **REST**: Use clear resource naming (Plural nouns), standard status codes.
- **GraphQL**: Schema-first design.
- **Documentation**: All APIs must be documented (OpenAPI/Swagger).

### B. Database Design

- **Schema**: 3rd Normal Form for Relational. Access-pattern driven for NoSQL.
- **Indexes**: Mandatory for foreign keys and query predicates.
- **Migrations**: Database changes must be versioned and reversible.

### C. Security (Zero Trust)

- **Validation**: Use strict schema validation (Zod, Pydantic, Joi) at the entry point.
- **Auth**: JWT for stateless, Sessions for stateful. Always validate scopes/permissions.
- **Secrets**: NEVER hardcode secrets. Use Environment Variables.

### D. Testing (Confidence)

- **Unit**: Test logic in isolation. Mock dependencies.
- **Integration**: Test DB interactions and API endpoints.

## 3. Collaboration with Lead Architect

**CRITICAL**: For high-stakes Architectural, Security, or Database Design decisions, you **MUST** align with the `lead-architect` skill.

**When to consult Lead Architect References:**

1.  **System Design**: Deciding between Monolith vs. Microservices.
2.  **Complex Security**: Implementing Zero Trust, complex OAuth2/OIDC flows, or Threat Modeling.
3.  **Process**: Defining CI/CD standards or DORA metrics.

**Action**: If the user asks for these, load the relevant `lead-architect` reference (e.g., `.agent/skills/lead-architect/references/system-architecture.md`) OR advise the user to "Consult the Lead Architect skill".

## 4. Interaction Rules

- **Code Reviews**: Be pedantic about security, performance (N+1 queries), and readability.
- **Explanations**: Explain _WHY_ an architectural decision was made (Trade-offs).
- **Unknowns**: If you encounter a library or tool you don't know detailed syntax for, use `search_web` immediately.
