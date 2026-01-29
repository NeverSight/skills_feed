---
name: architecture
description: >
  Use when asked to document architecture, understand system structure, create diagrams, or
  analyze component relationships. Focuses on interfaces and high-level design. Triggers on:
  "use architecture mode", "architecture", "system design", "how is this structured",
  "document the system", "create a diagram", "high-level overview", "component diagram".
  Read-only mode for analysis, can create documentation files.
---

# Architecture Mode

High-level design and system understanding.

## Core Constraint

> "Interfaces in; interfaces out. Data in; data out. Major flows, contracts, behaviors, and failure modes only."

If you find yourself describing implementation details, STOP. Zoom out.

## What to Focus On

✅ **Include**:

- System boundaries and contracts
- Data flow between components
- Integration points and APIs
- Error surfaces and failure modes
- Key design decisions and tradeoffs

❌ **Never Include**:

- Implementation details (how functions work internally)
- Line-by-line code analysis
- Minor utility functions
- Specific algorithms (unless architecturally significant)
- Variable names, loop structures, or conditionals
- Database schema details (only mention "stores X in Y")

## Anti-Patterns

| ❌ Don't Do This                        | ✅ Do This Instead                       |
| --------------------------------------- | ---------------------------------------- |
| "The function iterates over items..."   | "Component X transforms input to output" |
| "Line 42 calls the validate method..."  | "Validation happens at the API boundary" |
| "The for loop processes each record..." | "Records flow from A → B → C"            |
| "This uses a HashMap with..."           | "State is cached in memory"              |

## Analysis Framework

### 1. Component Identification

- What are the major components/modules?
- What is each component's single responsibility?
- How are they organized (layers, services, etc.)?

### 2. Interface Analysis

- What are the public APIs?
- What data structures cross boundaries?
- What are the contracts between components?

### 3. Data Flow

- How does data enter the system?
- How does it transform as it moves?
- Where is state stored?

### 4. Integration Points

- What external systems are connected?
- What protocols/formats are used?
- What are the failure modes?

### 5. Quality Attributes

- How is reliability achieved?
- How does it scale?
- What security measures exist?

## Architecture Overview Format

```markdown
## Architecture Overview

### Purpose

[What this system does in 1-2 sentences]

### Components

| Component | Responsibility   | Dependencies |
| --------- | ---------------- | ------------ |
| `api`     | HTTP interface   | auth, db     |
| `auth`    | Authentication   | db           |
| `db`      | Data persistence | -            |

### Data Flow

[Mermaid diagram - see below]

### Key Decisions

| Decision | Rationale | Tradeoffs   |
| -------- | --------- | ----------- |
| [choice] | [why]     | [pros/cons] |
```

## Mermaid Diagrams

### Component Diagram

```mermaid
graph LR
    Client --> API
    API --> Auth
    API --> Service
    Service --> DB
    Service --> Cache
```

### Sequence Diagram

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant S as Service
    participant D as Database

    C->>A: POST /orders
    A->>S: create_order()
    S->>D: INSERT order
    D-->>S: order_id
    S-->>A: Order
    A-->>C: 201 Created
```

## API Contract Format

````markdown
## API: /orders

### POST /orders

Create a new order.

**Request**:

```json
{
  "items": [{ "sku": "ABC", "qty": 2 }],
  "customer_id": "cust_123"
}
```
````

**Response** (201):

```json
{
  "order_id": "ord_456",
  "status": "pending",
  "total": 49.99
}
```

**Errors**:

- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing auth
- `422 Unprocessable Entity` - Business rule violation

```

## Guidelines

- Focus on **what** and **why**, not **how**
- Use diagrams liberally - they communicate structure better than prose
- Document decision rationale, not just the decision
- Identify failure modes and how they're handled
- Keep documentation close to the code it describes
```
