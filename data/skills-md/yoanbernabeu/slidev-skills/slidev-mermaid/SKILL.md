---
name: slidev-mermaid
description: Create diagrams with Mermaid in Slidev. Use this skill for flowcharts, sequence diagrams, class diagrams, and more.
---

# Mermaid Diagrams in Slidev

This skill covers creating visual diagrams using Mermaid syntax in Slidev presentations. Mermaid allows you to create flowcharts, sequence diagrams, class diagrams, and many other diagram types using simple text.

## When to Use This Skill

- Creating flowcharts and process diagrams
- Showing system architecture
- Visualizing sequences and workflows
- Creating class and entity diagrams
- Building organizational charts
- Displaying timelines and Gantt charts

## Basic Syntax

Use a code block with `mermaid` language:

````markdown
```mermaid
graph TD
    A[Start] --> B[Process]
    B --> C[End]
```
````

## Flowcharts

### Top-Down Flow

````markdown
```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```
````

### Left-Right Flow

````markdown
```mermaid
graph LR
    A[Input] --> B[Process] --> C[Output]
```
````

### Node Shapes

````markdown
```mermaid
graph TD
    A[Rectangle]
    B(Rounded)
    C([Stadium])
    D[[Subroutine]]
    E[(Database)]
    F((Circle))
    G>Asymmetric]
    H{Diamond}
    I{{Hexagon}}
    J[/Parallelogram/]
    K[\Parallelogram Alt\]
```
````

### Arrow Types

````markdown
```mermaid
graph LR
    A --> B
    C --- D
    E -.-> F
    G ==> H
    I --text--> J
    K ---|text| L
```
````

## Sequence Diagrams

### Basic Sequence

````markdown
```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant D as Database

    U->>S: Request
    S->>D: Query
    D-->>S: Result
    S-->>U: Response
```
````

### With Activation

````markdown
```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>+S: Login Request
    S->>S: Validate
    S-->>-C: Token

    C->>+S: API Call
    S-->>-C: Data
```
````

### Notes and Loops

````markdown
```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob

    Note over A: Alice thinks
    A->>B: Hello Bob!
    Note over A,B: Shared note

    loop Every minute
        A->>B: Are you there?
    end

    alt Success
        B-->>A: Yes!
    else Failure
        B-->>A: No response
    end
```
````

## Class Diagrams

### Basic Class

````markdown
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }

    class Dog {
        +String breed
        +bark()
    }

    class Cat {
        +meow()
    }

    Animal <|-- Dog
    Animal <|-- Cat
```
````

### Relationships

````markdown
```mermaid
classDiagram
    classA --|> classB : Inheritance
    classC --* classD : Composition
    classE --o classF : Aggregation
    classG --> classH : Association
    classI -- classJ : Link
    classK ..> classL : Dependency
    classM ..|> classN : Realization
```
````

## State Diagrams

````markdown
```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing: Start
    Processing --> Success: Complete
    Processing --> Error: Fail
    Success --> [*]
    Error --> Idle: Retry
```
````

### Nested States

````markdown
```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Idle
        Idle --> Running: Start
        Running --> Paused: Pause
        Paused --> Running: Resume
        Running --> Idle: Stop
    }

    Active --> [*]: Shutdown
```
````

## Entity Relationship Diagrams

````markdown
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string name
        string email
    }
    ORDER ||--|{ LINE_ITEM : contains
    ORDER {
        int id PK
        date created
        string status
    }
    PRODUCT ||--o{ LINE_ITEM : includes
    PRODUCT {
        int id PK
        string name
        float price
    }
    LINE_ITEM {
        int quantity
    }
```
````

## Gantt Charts

````markdown
```mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD

    section Planning
    Requirements    :a1, 2024-01-01, 7d
    Design         :a2, after a1, 5d

    section Development
    Backend        :b1, after a2, 14d
    Frontend       :b2, after a2, 14d

    section Testing
    QA             :c1, after b1, 7d
    UAT            :c2, after c1, 3d
```
````

## Pie Charts

````markdown
```mermaid
pie title Language Usage
    "JavaScript" : 45
    "Python" : 25
    "TypeScript" : 20
    "Other" : 10
```
````

## Git Graphs

````markdown
```mermaid
gitGraph
    commit
    commit
    branch feature
    checkout feature
    commit
    commit
    checkout main
    merge feature
    commit
```
````

## Mind Maps

````markdown
```mermaid
mindmap
    root((Slidev))
        Features
            Markdown
            Vue Components
            Animations
        Tech Stack
            Vite
            Vue 3
            UnoCSS
        Export
            PDF
            PPTX
            SPA
```
````

## Timeline

````markdown
```mermaid
timeline
    title History of Slidev
    2020 : Project Started
    2021 : v0.1 Released
         : Theme System Added
    2022 : Monaco Editor
         : Magic Move
    2023 : v0.40
         : Improved Animations
    2024 : v0.50
         : Browser Export
```
````

## Styling Diagrams

### Theme Option

````markdown
```mermaid {theme: 'neutral'}
graph TD
    A --> B --> C
```
````

Available themes: `default`, `neutral`, `dark`, `forest`, `base`

### Scale Option

````markdown
```mermaid {scale: 0.8}
graph TD
    A --> B --> C
```
````

### Combined Options

````markdown
```mermaid {theme: 'neutral', scale: 0.7}
graph LR
    A --> B --> C --> D
```
````

## Custom Styling

### Node Classes

````markdown
```mermaid
graph TD
    A[Important]:::important --> B[Normal]
    B --> C[Warning]:::warning

    classDef important fill:#f96,stroke:#333,stroke-width:2px
    classDef warning fill:#ff0,stroke:#333
```
````

### Link Styling

````markdown
```mermaid
graph LR
    A --> B
    B --> C
    linkStyle 0 stroke:#f00,stroke-width:2px
    linkStyle 1 stroke:#0f0,stroke-width:2px
```
````

## Configuration

### Global Mermaid Config

Create `setup/mermaid.ts`:

```typescript
import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    theme: 'neutral',
    themeVariables: {
      primaryColor: '#3b82f6',
      primaryTextColor: '#fff',
      primaryBorderColor: '#2563eb',
      lineColor: '#64748b',
      secondaryColor: '#f1f5f9',
    },
  }
})
```

## Best Practices

### 1. Keep Diagrams Simple

❌ **Too complex**
```
20+ nodes, crossing lines everywhere
```

✓ **Clear and focused**
```
5-10 nodes, logical flow
```

### 2. Use Meaningful Labels

❌ **Vague labels**
```mermaid
graph TD
    A --> B --> C
```

✓ **Descriptive labels**
```mermaid
graph TD
    Request[HTTP Request] --> Auth[Authentication]
    Auth --> Response[JSON Response]
```

### 3. Choose Right Diagram Type

| Content | Diagram Type |
|---------|--------------|
| Process flow | Flowchart |
| API calls | Sequence |
| Data models | Class/ER |
| Project timeline | Gantt |
| Distribution | Pie |
| Hierarchy | Mind map |

### 4. Consider Animation

Use v-click to reveal diagram parts:

````markdown
<v-click>

```mermaid
graph TD
    A --> B
```

</v-click>

<v-click>

```mermaid
graph TD
    A --> B --> C
```

</v-click>
````

## Common Patterns

### System Architecture

````markdown
```mermaid
graph TB
    subgraph Client
        UI[Web App]
        Mobile[Mobile App]
    end

    subgraph Backend
        API[API Gateway]
        Auth[Auth Service]
        Core[Core Service]
    end

    subgraph Data
        DB[(PostgreSQL)]
        Cache[(Redis)]
    end

    UI --> API
    Mobile --> API
    API --> Auth
    API --> Core
    Core --> DB
    Core --> Cache
```
````

### Request Flow

````markdown
```mermaid
sequenceDiagram
    actor User
    participant FE as Frontend
    participant BE as Backend
    participant DB as Database

    User->>FE: Click Button
    FE->>BE: POST /api/action
    BE->>DB: INSERT
    DB-->>BE: OK
    BE-->>FE: 201 Created
    FE-->>User: Success Toast
```
````

## Output Format

When creating diagrams:

```
DIAGRAM PURPOSE: [What it illustrates]
DIAGRAM TYPE: [flowchart/sequence/class/etc.]

```mermaid {[options]}
[diagram code]
```

KEY ELEMENTS:
- Node A: [represents...]
- Node B: [represents...]
- Arrow X->Y: [means...]

STYLING NOTES:
- Theme: [chosen theme]
- Scale: [if adjusted]
- Custom classes: [if any]
```
