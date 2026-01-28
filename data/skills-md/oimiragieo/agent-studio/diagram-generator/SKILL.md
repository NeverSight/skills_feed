---
name: diagram-generator
description: Generates architecture, database, and system diagrams using Mermaid syntax. Creates visual representations of system architecture, database schemas, component relationships, and data flows.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Glob, Grep]
best_practices:
  - Use Mermaid syntax for diagrams
  - Extract structure from code and documentation
  - Create clear, readable diagrams
  - Include relationships and dependencies
  - Generate both high-level and detailed views
error_handling: graceful
streaming: supported
templates: [architecture-diagram, database-diagram, component-diagram, sequence-diagram]
---

<identity>
Diagram Generator Skill - Generates architecture, database, and system diagrams using Mermaid syntax to visualize system structure, relationships, and flows.
</identity>

<capabilities>
- Creating architecture diagrams
- Documenting database schemas
- Visualizing component relationships
- Documenting data flows
- Creating sequence diagrams
- Generating system overviews
</capabilities>

<instructions>
<execution_process>

### Step 1: Identify Diagram Type

Determine what type of diagram is needed:

- **Architecture Diagram**: System structure and components
- **Database Diagram**: Schema and relationships
- **Component Diagram**: Component interactions
- **Sequence Diagram**: Process flows
- **Flowchart**: Decision flows

### Step 2: Extract Structure

Analyze code and documentation (Use Parallel Read/Grep/Glob):

- Read architecture documents
- Analyze component structure
- Extract database schema
- Identify relationships
- Understand data flows

### Step 3: Generate Mermaid Diagram

Create diagram using Mermaid syntax:

- Use appropriate diagram type
- Define nodes and relationships
- Add labels and descriptions
- Include styling if needed

### Step 4: Embed in Documentation

Embed diagram in markdown:

- Use mermaid code blocks
- Add diagram description
- Reference in documentation
  </execution_process>

<integration>
**Integration with Architect Agent**:
- Generates architecture diagrams
- Documents system structure
- Visualizes component relationships

**Integration with Database Architect Agent**:

- Generates database schema diagrams
- Documents table relationships
- Visualizes data models

**Integration with Technical Writer Agent**:

- Embeds diagrams in documentation
- Creates visual documentation
- Enhances documentation clarity
  </integration>

<best_practices>

1. **Use Mermaid**: Standard syntax for compatibility
2. **Keep Clear**: Simple, readable diagrams
3. **Show Relationships**: Include all important connections
4. **Add Labels**: Clear node and edge labels
5. **Update Regularly**: Keep diagrams current with code
   </best_practices>
   </instructions>

<examples>
<code_example>
**Architecture Diagram**

```mermaid
graph TB
    Client[Client Application]
    API[API Gateway]
    Auth[Auth Service]
    User[User Service]
    DB[(Database)]

    Client --> API
    API --> Auth
    API --> User
    User --> DB
    Auth --> DB
```

</code_example>

<code_example>
**Database Schema Diagram**

```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    USERS {
        uuid id PK
        string email
        string name
    }
    ORDERS ||--|{ ORDER_ITEMS : contains
    ORDERS {
        uuid id PK
        uuid user_id FK
        date created_at
    }
    ORDER_ITEMS {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
    }
```

</code_example>

<code_example>
**Component Diagram**

```mermaid
graph LR
    A[Component A] --> B[Component B]
    A --> C[Component C]
    B --> D[Component D]
    C --> D
```

</code_example>

<code_example>
**Sequence Diagram**

```mermaid
sequenceDiagram
    participant User
    participant API
    participant Auth
    participant DB

    User->>API: Login Request
    API->>Auth: Validate Credentials
    Auth->>DB: Query User
    DB-->>Auth: User Data
    Auth-->>API: JWT Token
    API-->>User: Auth Response
```

</code_example>
</examples>

<examples>
<usage_example>
**Example Commands**:

```bash
# Generate architecture diagram
node .claude/tools/diagram-generator/scripts/generate.mjs --type architecture "authentication system"

# Generate database schema diagram
node .claude/tools/diagram-generator/scripts/generate.mjs --type database "user management module"

# Generate component diagram
node .claude/tools/diagram-generator/scripts/generate.mjs --type component "API service relationships"

# Generate sequence diagram
node .claude/tools/diagram-generator/scripts/generate.mjs --type sequence "user login flow"
```

</usage_example>
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
