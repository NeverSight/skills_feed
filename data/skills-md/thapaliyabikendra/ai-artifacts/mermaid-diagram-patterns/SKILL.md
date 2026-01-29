---
name: mermaid-diagram-patterns
description: "Create Mermaid diagrams for technical documentation including ERDs, sequence diagrams, flowcharts, and architecture diagrams. Use when: (1) designing database schemas (ERD), (2) documenting API interactions (sequence), (3) illustrating process flows (flowchart), (4) visualizing system architecture."
layer: 1
tech_stack: [mermaid, markdown]
topics: [erd, sequence-diagram, flowchart, class-diagram, architecture-diagram]
depends_on: []
complements: [technical-design-patterns]
keywords: [Mermaid, ERD, Sequence, Flowchart, Graph, ClassDiagram, erDiagram]
---

# Mermaid Diagram Patterns

Create clear, professional Mermaid diagrams for technical documentation.

## When to Use

- Database schema visualization (ERD)
- API interaction sequences
- Process and workflow flowcharts
- System architecture diagrams
- State machines and user journeys
- Decision trees

## Diagram Type Selection

| Scenario | Diagram Type | Mermaid Syntax |
|----------|--------------|----------------|
| Database schema | ERD | `erDiagram` |
| API calls | Sequence | `sequenceDiagram` |
| Process flow | Flowchart | `graph TD` or `flowchart TD` |
| Component architecture | Flowchart | `graph LR` |
| State transitions | State | `stateDiagram-v2` |
| User workflow | Journey | `journey` |
| Project timeline | Gantt | `gantt` |
| Class relationships | Class | `classDiagram` |

## ERD Pattern (Database Schema)

Use for entity definitions in technical design documents.

```mermaid
erDiagram
    %% Entity definitions with attributes
    PATIENT {
        uuid Id PK
        string FirstName
        string LastName
        string Email UK
        string Phone
        date DateOfBirth
        timestamp CreationTime
        uuid CreatorId FK
        boolean IsDeleted
    }

    DOCTOR {
        uuid Id PK
        string FullName
        string Specialization
        string Email UK
        string Phone
    }

    APPOINTMENT {
        uuid Id PK
        uuid PatientId FK
        uuid DoctorId FK
        timestamp AppointmentDate
        string Description
        smallint Status "0=Scheduled,1=Completed,2=Cancelled"
    }

    %% Relationships
    PATIENT ||--o{ APPOINTMENT : "has"
    DOCTOR ||--o{ APPOINTMENT : "conducts"
```

### ERD Conventions

| Symbol | Meaning |
|--------|---------|
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |
| `||--o{` | One-to-Many |
| `||--||` | One-to-One |
| `}o--o{` | Many-to-Many |

## Sequence Diagram Pattern (API Interactions)

Use for documenting API flows in technical design.

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant API as API Gateway
    participant S as AppService
    participant DB as Database

    C->>+API: POST /api/app/patients
    API->>API: Validate JWT
    API->>+S: CreateAsync(dto)
    S->>S: Validate input
    S->>+DB: Insert Patient
    DB-->>-S: Patient entity
    S-->>-API: PatientDto
    API-->>-C: 201 Created

    Note over C,DB: Error handling
    C->>+API: POST /api/app/patients (invalid)
    API->>+S: CreateAsync(dto)
    S-->>-API: ValidationException
    API-->>-C: 400 Bad Request
```

### Sequence Conventions

| Arrow | Meaning |
|-------|---------|
| `->>` | Sync request |
| `-->>` | Sync response |
| `--)` | Async message |
| `+` / `-` | Activation/deactivation |

## Flowchart Pattern (Process Flow)

Use for business processes and decision flows.

```mermaid
flowchart TD
    A[Start: New Appointment Request] --> B{Patient Exists?}
    B -->|Yes| C[Load Patient]
    B -->|No| D[Create Patient]
    D --> C
    C --> E{Doctor Available?}
    E -->|Yes| F[Create Appointment]
    E -->|No| G[Show Available Slots]
    G --> H[User Selects Slot]
    H --> F
    F --> I[Send Confirmation]
    I --> J[End]

    style A fill:#e1f5fe
    style J fill:#c8e6c9
    style B fill:#fff3e0
    style E fill:#fff3e0
```

### Flowchart Conventions

| Shape | Syntax | Use For |
|-------|--------|---------|
| Rectangle | `[text]` | Process/Action |
| Diamond | `{text}` | Decision |
| Stadium | `([text])` | Start/End |
| Parallelogram | `[/text/]` | Input/Output |
| Circle | `((text))` | Connector |

## Architecture Diagram Pattern

Use for system component visualization.

```mermaid
graph LR
    subgraph Client
        UI[React App]
    end

    subgraph API["API Layer"]
        GW[API Gateway]
        AUTH[AuthServer]
    end

    subgraph Services["Application Services"]
        PS[PatientService]
        DS[DoctorService]
        AS[AppointmentService]
    end

    subgraph Data["Data Layer"]
        PG[(PostgreSQL)]
        RD[(Redis Cache)]
    end

    UI --> GW
    UI --> AUTH
    GW --> PS & DS & AS
    PS & DS & AS --> PG
    PS & DS & AS --> RD

    style PG fill:#336791,color:#fff
    style RD fill:#dc382d,color:#fff
```

## State Diagram Pattern

Use for entity lifecycle documentation.

```mermaid
stateDiagram-v2
    [*] --> Scheduled: Create

    Scheduled --> Confirmed: Patient Confirms
    Scheduled --> Cancelled: Cancel

    Confirmed --> InProgress: Check-in
    Confirmed --> Cancelled: Cancel
    Confirmed --> NoShow: No Check-in

    InProgress --> Completed: Finish

    Completed --> [*]
    Cancelled --> [*]
    NoShow --> [*]

    note right of Scheduled: Initial state
    note right of Completed: Triggers billing
```

## Styling Guidelines

### Color Palette (ABP/Healthcare Theme)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#1976d2',
    'primaryTextColor': '#fff',
    'primaryBorderColor': '#1565c0',
    'lineColor': '#424242',
    'secondaryColor': '#f5f5f5',
    'tertiaryColor': '#e3f2fd'
}}}%%
```

### Styling Classes

```
style NodeId fill:#color,stroke:#color,color:#textcolor
classDef className fill:#color,stroke:#color
class NodeId className
```

## Quality Checklist

- [ ] Correct diagram type for the scenario
- [ ] Clear, descriptive labels
- [ ] Consistent arrow directions (TD=top-down, LR=left-right)
- [ ] Proper relationship cardinality (ERD)
- [ ] Activation bars for long operations (sequence)
- [ ] Decision points clearly marked (flowchart)
- [ ] Subgraphs for logical grouping
- [ ] Comments for complex sections (`%%`)

## Integration Points

This skill is used by:
- **backend-architect**: ERD in technical-design.md, API sequences
- **business-analyst**: Process flows in requirements.md, user journeys

## References

- [Mermaid Official Docs](https://mermaid.js.org/intro/)
- [references/diagram-examples.md](references/diagram-examples.md) - Additional examples
