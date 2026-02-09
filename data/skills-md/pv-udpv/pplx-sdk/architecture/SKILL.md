---
name: architecture
description: Visualize and document pplx-sdk system architecture with Mermaid diagrams — layer maps, data flow, dependency graphs, sequence diagrams, and component relationships. Use when designing new features, onboarding, or documenting how the system works.
context: fork
agent: architect
---

# Architecture Diagramming & Visualization

Create, maintain, and reason about pplx-sdk system architecture using Mermaid diagrams.

## When to use

Use this skill when:
- Visualizing system architecture or component relationships
- Designing a new feature and need to map dependencies
- Documenting data flow through the SDK layers
- Creating sequence diagrams for API call flows
- Analyzing import graphs to detect circular dependencies
- Onboarding — generating a visual overview of the codebase
- Planning refactors that touch multiple layers

## Instructions

### Step 1: Identify Diagram Type

| Need | Diagram Type | Mermaid Syntax |
|------|-------------|----------------|
| Layer overview | Layered block diagram | `block-beta` or `graph TD` |
| Data flow | Flowchart | `graph LR` |
| API call sequence | Sequence diagram | `sequenceDiagram` |
| Class relationships | Class diagram | `classDiagram` |
| State transitions | State diagram | `stateDiagram-v2` |
| Component dependencies | Dependency graph | `graph TD` |
| Deployment / infra | C4 or flowchart | `graph TD` with subgraphs |

### Step 2: Map the Architecture

The pplx-sdk layered architecture:

```mermaid
graph TD
    Client["client.py<br/>PerplexityClient, Conversation"]
    Domain["domain/<br/>models.py, services"]
    Transport["transport/<br/>http.py, sse.py"]
    Shared["shared/<br/>auth.py, logging.py, retry.py"]
    Core["core/<br/>protocols.py, types.py, exceptions.py"]

    Client --> Domain
    Client --> Transport
    Client --> Shared
    Domain --> Transport
    Domain --> Shared
    Domain --> Core
    Transport --> Shared
    Transport --> Core
    Shared --> Core

    style Core fill:#e1f5fe
    style Shared fill:#f3e5f5
    style Transport fill:#fff3e0
    style Domain fill:#e8f5e9
    style Client fill:#fce4ec
```

### Step 3: Generate Specific Diagrams

#### SSE Streaming Sequence

```mermaid
sequenceDiagram
    participant App as Application
    participant Client as PerplexityClient
    participant Transport as SSETransport
    participant API as perplexity.ai

    App->>Client: ask_stream(query)
    Client->>Transport: stream(payload)
    Transport->>API: POST /rest/sse/perplexity.ask
    loop SSE Events
        API-->>Transport: event: query_progress
        Transport-->>Client: StreamChunk(progress)
        API-->>Transport: event: answer_chunk
        Transport-->>Client: StreamChunk(text)
    end
    API-->>Transport: event: final_response
    Transport-->>Client: StreamChunk(final)
    API-->>Transport: : [end]
    Client-->>App: Entry (complete)
```

#### Exception Hierarchy

```mermaid
classDiagram
    class PerplexitySDKError {
        +str message
        +dict details
    }
    class TransportError {
        +int status_code
        +str response_body
    }
    class AuthenticationError {
        401
    }
    class RateLimitError {
        +float retry_after
        429
    }
    class StreamingError
    class ValidationError

    PerplexitySDKError <|-- TransportError
    PerplexitySDKError <|-- StreamingError
    PerplexitySDKError <|-- ValidationError
    TransportError <|-- AuthenticationError
    TransportError <|-- RateLimitError
```

#### Retry State Machine

```mermaid
stateDiagram-v2
    [*] --> Requesting
    Requesting --> Success: 2xx response
    Requesting --> RetryWait: 429 / 5xx
    Requesting --> Failed: 4xx (non-429)
    RetryWait --> Requesting: backoff elapsed
    RetryWait --> Failed: max_retries exceeded
    Success --> [*]
    Failed --> [*]
```

### Step 4: Embed in Documentation

Place diagrams in:
- `README.md` — high-level architecture overview
- `docs/architecture.md` — detailed component diagrams
- Inline in module docstrings — for complex flow explanations
- PR descriptions — for explaining changes visually

### Diagram Conventions

- Use consistent colors per layer (Core=blue, Shared=purple, Transport=orange, Domain=green, Client=pink)
- Label edges with function/method names when showing call flow
- Use subgraphs to group related components
- Include error paths in sequence diagrams (alt/opt blocks)
- Prefer top-down (`TD`) for hierarchy, left-right (`LR`) for flow

### Step 5: Validate Architecture

After diagramming, verify:
1. No upward dependencies (lower layers must not import higher layers)
2. No circular imports between modules
3. All public APIs are accessible through `client.py`
4. Exception hierarchy is consistent with `core/exceptions.py`
5. Transport protocol conformance (`core/protocols.py`)
