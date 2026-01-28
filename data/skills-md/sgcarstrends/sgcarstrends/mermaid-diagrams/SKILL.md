---
name: mermaid-diagrams
description: Create and maintain architecture diagrams using Mermaid syntax for system architecture, workflows, database schemas, and sequence diagrams. Use when visualizing system components, data flows, or documenting architecture.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Mermaid Diagrams Skill

This skill helps you create and maintain architecture diagrams using Mermaid syntax.

## When to Use This Skill

- Visualizing system architecture
- Documenting data flows and workflows
- Creating database entity-relationship diagrams
- Sequence diagrams for API interactions
- State diagrams for workflows
- Flowcharts for decision logic
- Updating architecture documentation

## Mermaid Overview

Mermaid is a diagramming and charting tool that uses text-based syntax:
- **Text-Based**: Diagrams defined in plain text
- **Version Control**: Track changes in git
- **Easy Updates**: Modify diagrams like code
- **Multiple Types**: Flowcharts, sequence, ER, class, state, etc.
- **Integration**: Works in Markdown, GitHub, and many other platforms

## Diagram Types

### 1. System Architecture (Flowchart)

```mermaid
flowchart TB
    subgraph Internet
        User[User/Browser]
    end

    subgraph Cloudflare
        DNS[DNS]
        CDN[CDN/Caching]
    end

    subgraph AWS["AWS (ap-southeast-1)"]
        subgraph API Service
            ALB[Application Load Balancer]
            Lambda[Lambda Function<br/>Hono API]
        end

        subgraph Data Layer
            RDS[(PostgreSQL<br/>RDS)]
            Redis[(Redis<br/>Upstash)]
        end

        subgraph Web App
            NextJS[Next.js App<br/>Lambda@Edge]
        end

        subgraph Storage
            S3[S3 Bucket<br/>Static Assets]
        end
    end

    subgraph External Services
        LTA[LTA DataMall API]
        QStash[QStash<br/>Workflow Engine]
        Gemini[Google Gemini<br/>AI Service]
        Social[Social Media APIs]
    end

    User --> DNS
    DNS --> CDN
    CDN --> NextJS
    CDN --> ALB
    ALB --> Lambda
    Lambda --> RDS
    Lambda --> Redis
    Lambda --> QStash
    Lambda --> LTA
    QStash --> Lambda
    Lambda --> Gemini
    Lambda --> Social
    NextJS --> Lambda
    NextJS --> S3
```

**Source file:**
```
// apps/docs/diagrams/system-architecture.mmd
flowchart TB
    User[User/Browser] --> DNS[Cloudflare DNS]
    DNS --> NextJS[Next.js App]
    // ... rest of diagram
```

### 2. Workflow Sequence Diagram

```mermaid
sequenceDiagram
    participant QStash as QStash Cron
    participant Workflow as Update Workflow
    participant LTA as LTA DataMall
    participant DB as PostgreSQL
    participant Redis as Redis Cache
    participant Gemini as Gemini AI
    participant Social as Social Media

    QStash->>Workflow: Trigger (Daily 10 AM)

    alt Data Update
        Workflow->>LTA: Fetch car data
        LTA-->>Workflow: Car records
        Workflow->>DB: Save car data
        Workflow->>Redis: Invalidate cache
    end

    alt Blog Generation
        Workflow->>DB: Get latest data
        DB-->>Workflow: Data for analysis
        Workflow->>Gemini: Generate blog post
        Gemini-->>Workflow: Blog content
        Workflow->>DB: Save blog post
    end

    alt Social Media
        Workflow->>DB: Get latest post
        DB-->>Workflow: Post content
        Workflow->>Social: Post to platforms
        Social-->>Workflow: Success
    end

    Workflow-->>QStash: Complete
```

**Source file:**
```
// apps/docs/diagrams/workflow-sequence.mmd
sequenceDiagram
    participant QStash
    participant Workflow
    // ... rest of diagram
```

### 3. Database Entity-Relationship Diagram

```mermaid
erDiagram
    CARS {
        uuid id PK
        string make
        string model
        string month
        int number
        string vehicleType
        string fuelType
        timestamp createdAt
    }

    COE {
        uuid id PK
        string month
        int biddingNo
        string vehicleClass
        int quota
        int bidsReceived
        int premiumAmount
        timestamp createdAt
    }

    POSTS {
        uuid id PK
        string title
        string slug UK
        text content
        text excerpt
        string status
        timestamp publishedAt
        timestamp createdAt
    }

    ANALYTICS {
        uuid id PK
        string path
        string referrer
        string userAgent
        string country
        timestamp timestamp
    }

    POSTS ||--o{ ANALYTICS : "tracks visits"
```

**Source file:**
```
// apps/docs/diagrams/database-erd.mmd
erDiagram
    CARS {
        uuid id PK
        // ... rest of schema
    }
```

### 4. API Architecture

```mermaid
graph LR
    Client[Client] --> API[API Gateway]

    API --> V1[v1 Routes]

    V1 --> Cars[Cars Endpoints]
    V1 --> COE[COE Endpoints]
    V1 --> Blog[Blog Endpoints]
    V1 --> Health[Health Check]

    Cars --> CarService[Car Service]
    COE --> COEService[COE Service]
    Blog --> BlogService[Blog Service]

    CarService --> DB[(Database)]
    COEService --> DB
    BlogService --> DB

    CarService --> Cache[(Redis)]
    COEService --> Cache
    BlogService --> Cache
```

### 5. State Diagram (Workflow States)

```mermaid
stateDiagram-v2
    [*] --> Scheduled
    Scheduled --> Running: Trigger
    Running --> FetchingData: Start
    FetchingData --> ProcessingData: Data Received
    FetchingData --> Failed: API Error
    ProcessingData --> SavingData: Processed
    SavingData --> GeneratingBlog: Saved
    GeneratingBlog --> PostingToSocial: Generated
    PostingToSocial --> Completed: Posted
    PostingToSocial --> PartiallyCompleted: Some Failed
    Failed --> [*]
    Completed --> [*]
    PartiallyCompleted --> [*]
```

### 6. Class Diagram (TypeScript Interfaces)

```mermaid
classDiagram
    class Car {
        +String id
        +String make
        +String model
        +String month
        +Number number
        +String vehicleType
        +String fuelType
    }

    class COE {
        +String id
        +String month
        +Number biddingNo
        +String vehicleClass
        +Number quota
        +Number bidsReceived
        +Number premiumAmount
    }

    class BlogPost {
        +String id
        +String title
        +String slug
        +String content
        +String excerpt
        +String status
        +Date publishedAt
    }

    class Analytics {
        +String id
        +String path
        +String referrer
        +Date timestamp
    }

    BlogPost "1" --> "*" Analytics : tracks
```

## Creating Diagrams

### File Organization

```
docs/
├── diagrams/                    # Source .mmd files
│   ├── system.mmd
│   ├── workflows.mmd
│   ├── database.mmd
│   ├── api.mmd
│   ├── infrastructure.mmd
│   └── social.mmd
└── architecture/                # Markdown docs with embedded diagrams
    ├── system.md
    ├── workflows.md
    ├── database.md
    ├── api.md
    ├── infrastructure.md
    └── social.md
```

### Embed in Markdown Docs

```markdown
# System Architecture

The system consists of the following components:

```mermaid
flowchart TB
    User[User/Browser] --> DNS[Cloudflare DNS]
    DNS --> NextJS[Next.js App]
    DNS --> API[Hono API]
    // ... rest of diagram
\```

## Components

### Frontend
- Next.js 16 with App Router
- Deployed on AWS Lambda@Edge
- Static assets on S3 + CloudFront

### Backend
- Hono API on AWS Lambda
- PostgreSQL on RDS
- Redis caching with Upstash
```

## Common Patterns

### System Overview

```mermaid
flowchart TB
    subgraph Frontend
        Web[Next.js Web App]
        Admin[Admin Panel]
    end

    subgraph Backend
        API[Hono API]
        Workflows[QStash Workflows]
    end

    subgraph Data
        DB[(PostgreSQL)]
        Cache[(Redis)]
    end

    subgraph External
        LTA[LTA DataMall]
        AI[Gemini AI]
    end

    Web --> API
    Admin --> API
    API --> DB
    API --> Cache
    Workflows --> LTA
    Workflows --> AI
    Workflows --> DB
```

### Data Flow

```mermaid
flowchart LR
    A[LTA DataMall] -->|Fetch| B[Workflow]
    B -->|Transform| C[Processing]
    C -->|Save| D[(Database)]
    D -->|Cache| E[(Redis)]
    E -->|Serve| F[API]
    F -->|Response| G[Client]
```

### Request Flow

```mermaid
sequenceDiagram
    Client->>+API: GET /api/v1/cars/makes
    API->>+Cache: Check cache
    Cache-->>-API: Cache miss
    API->>+DB: Query database
    DB-->>-API: Results
    API->>Cache: Store in cache
    API-->>-Client: JSON response
```

### Deployment Pipeline

```mermaid
flowchart LR
    A[Git Push] --> B[GitHub Actions]
    B --> C{Branch?}
    C -->|main| D[Production]
    C -->|staging| E[Staging]
    C -->|dev| F[Development]
    D --> G[Deploy API]
    D --> H[Deploy Web]
    G --> I[Run Migrations]
    H --> J[Invalidate CDN]
```

## Styling Diagrams

### Colors and Themes

```mermaid
flowchart TB
    A[Start]:::green --> B{Decision}:::yellow
    B -->|Yes| C[Success]:::green
    B -->|No| D[Error]:::red

    classDef green fill:#0D9373,stroke:#07C983,color:#fff
    classDef yellow fill:#FDB022,stroke:#F59E0B,color:#000
    classDef red fill:#DC2626,stroke:#B91C1C,color:#fff
```

### Subgraphs for Organization

```mermaid
flowchart TB
    subgraph AWS
        subgraph Compute
            Lambda[Lambda]
            ECS[ECS]
        end

        subgraph Storage
            S3[S3]
            RDS[(RDS)]
        end
    end

    Lambda --> S3
    Lambda --> RDS
```

## Best Practices

### 1. Use Meaningful Labels

```mermaid
# ❌ Unclear labels
A --> B
B --> C

# ✅ Clear labels
User[User] --> API[API Gateway]
API --> DB[(Database)]
```

### 2. Group Related Components

```mermaid
# ✅ Organized with subgraphs
flowchart TB
    subgraph Frontend
        Web[Web App]
        Mobile[Mobile App]
    end

    subgraph Backend
        API[API]
        Workers[Workers]
    end

    Web --> API
    Mobile --> API
```

### 3. Add Arrows for Data Flow

```mermaid
# ❌ No direction
A -- B

# ✅ Shows direction
A -->|Request| B
B -->|Response| A
```

### 4. Use Appropriate Diagram Types

- **Flowchart**: System architecture, data flow
- **Sequence**: API interactions, workflows
- **ER Diagram**: Database schemas
- **State**: Workflow states, FSM
- **Class**: TypeScript interfaces, OOP

## Exporting Diagrams

### PNG/SVG Export

```bash
# Install mermaid-cli
pnpm add -g @mermaid-js/mermaid-cli

# Generate PNG
mmdc -i diagram.mmd -o diagram.png

# Generate SVG
mmdc -i diagram.mmd -o diagram.svg

# Generate PDF
mmdc -i diagram.mmd -o diagram.pdf
```

### Batch Export

```bash
# Export all diagrams
for file in diagrams/*.mmd; do
  mmdc -i "$file" -o "${file%.mmd}.png"
done
```

## Updating Diagrams

### Workflow

1. Edit source `.mmd` file in `docs/diagrams/`
2. Update corresponding Markdown file in `docs/architecture/`
3. Preview in GitHub or VS Code
4. Commit changes

```bash
# Edit diagram
vim docs/diagrams/system.mmd

# Update documentation
vim docs/architecture/system.md

# Commit
git add docs/diagrams/system.mmd
git add docs/architecture/system.md
git commit -m "docs: update system architecture diagram"
```

## Troubleshooting

### Syntax Errors

```mermaid
# ❌ Invalid syntax
flowchart TB
    A -> B  # Wrong arrow syntax

# ✅ Correct syntax
flowchart TB
    A --> B
```

### Layout Issues

```mermaid
# ❌ Unclear layout
flowchart LR
    A --> B --> C --> D --> E

# ✅ Better layout with subgraphs
flowchart TB
    A --> B
    B --> C

    subgraph Processing
        C --> D
        D --> E
    end
```

### Diagram Not Rendering

```markdown
# Issue: Mermaid not rendering
# Solution: Ensure proper code fence

# ❌ Wrong
\```mermaid
graph TD
\```

# ✅ Correct
\```mermaid
flowchart TD
    A --> B
\```
```

## Live Editors

### Online Editors

- **Mermaid Live Editor**: https://mermaid.live
- **GitHub**: Renders mermaid in markdown

### VS Code Extensions

```bash
# Install Mermaid extension
# Search: "Mermaid Markdown Syntax Highlighting"
```

## References

- Mermaid Documentation: https://mermaid.js.org
- Flowchart Syntax: https://mermaid.js.org/syntax/flowchart.html
- Sequence Diagrams: https://mermaid.js.org/syntax/sequenceDiagram.html
- ER Diagrams: https://mermaid.js.org/syntax/entityRelationshipDiagram.html
- State Diagrams: https://mermaid.js.org/syntax/stateDiagram.html
- Related files:
  - `docs/diagrams/` - Source diagram files
  - `docs/architecture/` - Documentation with diagrams
  - Root CLAUDE.md - Documentation guidelines

## Best Practices Summary

1. **Source Control**: Keep `.mmd` files in `diagrams/` directory
2. **Meaningful Labels**: Use clear, descriptive node labels
3. **Subgraphs**: Group related components for clarity
4. **Appropriate Types**: Choose the right diagram type for the purpose
5. **Consistent Style**: Use consistent colors and formatting
6. **Data Flow**: Show direction with arrows
7. **Documentation**: Embed diagrams in relevant docs
8. **Keep Updated**: Update diagrams when architecture changes
