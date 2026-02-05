---
name: system-architecture
description: >-
  System architecture guidance for Python/React full-stack projects. Use during
  the design phase when making architectural decisions — component boundaries, service
  layer design, data flow patterns, database schema planning, and technology trade-off
  analysis. Covers FastAPI layer architecture (Routes/Services/Repositories/Models),
  React component hierarchy, state management, and cross-cutting concerns (auth, errors,
  logging). Produces architecture documents and ADRs. Does NOT cover implementation
  (use python-backend-expert or react-frontend-expert) or API contract design
  (use api-design-patterns).
license: MIT
compatibility: 'Python 3.12+, FastAPI 0.115+, React 18+, SQLAlchemy 2.0+, TypeScript 5+'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: architecture
allowed-tools: Read Grep Glob
context: fork
---

# System Architecture

## When to Use

Activate this skill when:
- Designing a new module, service, or major feature that requires structural decisions
- Choosing between architectural approaches (e.g., where to place logic, how to structure data flow)
- Planning database schema changes or refactoring existing schema
- Making frontend state management decisions (server state vs client state, context vs store)
- Evaluating technology trade-offs for a new capability
- Creating or reviewing Architecture Decision Records (ADRs)
- Setting up a new project or major subsystem from scratch

Do NOT use this skill for:
- Writing implementation code (use `python-backend-expert` or `react-frontend-expert`)
- API contract design or endpoint specifications (use `api-design-patterns`)
- Testing patterns or strategies (use `pytest-patterns` or `react-testing-patterns`)
- Deployment or infrastructure decisions (use `docker-best-practices` or `deployment-pipeline`)

## Instructions

### Project Layer Architecture

The standard Python/React full-stack architecture follows a layered pattern with strict dependency direction.

#### Backend Layers (FastAPI)

```
HTTP Request
    ↓
┌─────────────────────┐
│   Routers (routes/)  │  ← HTTP concerns: request parsing, response formatting, status codes
│                      │     Uses: Depends() for injection, Pydantic schemas for validation
├─────────────────────┤
│   Services           │  ← Business logic: orchestration, validation rules, domain operations
│   (services/)        │     No HTTP awareness. Raises domain exceptions, not HTTPException.
├─────────────────────┤
│   Repositories       │  ← Data access: queries, CRUD operations, database interactions
│   (repositories/)    │     No business logic. Returns model instances or None.
├─────────────────────┤
│   Models (models/)   │  ← SQLAlchemy ORM models: table definitions, relationships, indexes
│   Schemas (schemas/) │  ← Pydantic v2 models: request/response contracts, validation
└─────────────────────┘
    ↓
Database
```

**Dependency direction rules:**
- Routers depend on Services (never on Repositories directly)
- Services depend on Repositories (never on Routers)
- Repositories depend on Models (never on Services)
- Schemas are shared across layers but define no dependencies themselves
- Never skip layers: no direct database access from routes

**Dependency injection pattern:**
```python
# Router depends on Service via Depends()
@router.post("/users", response_model=UserResponse)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await service.create_user(data)

# Service depends on Repository via constructor injection
class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

# Repository depends on AsyncSession via Depends()
class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
```

#### Frontend Layers (React/TypeScript)

```
┌─────────────────────┐
│   Pages (pages/)     │  ← Route-level components: data fetching, layout composition
├─────────────────────┤
│   Layouts            │  ← Page structure: navigation, sidebars, content areas
│   (layouts/)         │
├─────────────────────┤
│   Features           │  ← Domain-specific: UserProfile, OrderList, ChatPanel
│   (features/)        │     Composed from shared components + hooks
├─────────────────────┤
│   Shared Components  │  ← Reusable UI: Button, Modal, Table, Form, Input
│   (components/)      │     No business logic. Configurable via props.
├─────────────────────┤
│   Hooks (hooks/)     │  ← Custom hooks: useAuth, usePagination, useDebounce
│   API (api/)         │  ← API client functions, TanStack Query configurations
├─────────────────────┤
│   Types (types/)     │  ← Shared TypeScript interfaces and type definitions
└─────────────────────┘
```

**Component dependency direction:**
- Pages import Features and Layouts
- Features import Shared Components and Hooks
- Shared Components import only other Shared Components and Types
- Hooks import API functions and Types
- API functions import Types only

### Decision Framework

When facing architectural decisions, follow this structured process:

#### Step 1: Define the Problem
- What capability is needed?
- What are the non-functional requirements? (performance, scalability, maintainability)
- What constraints exist? (team size, timeline, existing infrastructure)

#### Step 2: Identify Options
- List 2-3 viable architectural approaches
- For each option, document:
  - How it works (brief technical description)
  - Advantages
  - Disadvantages
  - Risks

#### Step 3: Evaluate Against Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Maintainability | High | Can the team understand, modify, and debug this easily? |
| Testability | High | Can each component be tested in isolation? |
| Performance | Medium | Does it meet latency and throughput requirements? |
| Team familiarity | Medium | Does the team have experience with this approach? |
| Operational cost | Low | What are the infrastructure and maintenance costs? |
| Future flexibility | Low | How easily can this evolve as requirements change? |

#### Step 4: Decide and Document
- Choose the option that best satisfies the weighted criteria
- Document the decision in an ADR (see `references/architecture-decision-record-template.md`)
- Record what was NOT chosen and why — this context is valuable for future decisions

#### Step 5: Communicate
- Share the ADR with the team
- Identify any migration or rollout steps needed
- Flag reversibility: is this a one-way door or a two-way door?

### Database Schema Design

#### Design Principles

1. **Start normalized (3NF)** — Denormalize only for proven performance bottlenecks, not speculation
2. **One migration per logical change** — Each Alembic migration should represent a single, coherent schema modification
3. **Always include downgrade** — Every migration must have a working `downgrade()` function
4. **Index strategically:**
   - Primary keys (automatic)
   - Foreign keys (always)
   - Columns in WHERE clauses of frequent queries
   - Composite indexes for multi-column lookups
   - Partial indexes for filtered queries (e.g., `WHERE is_active = true`)

#### SQLAlchemy 2.0 Async Patterns

```python
# Model definition with Mapped types (SQLAlchemy 2.0 style)
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Relationships: ALWAYS use eager loading with async
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author",
        lazy="selectin",  # or "joined" — NEVER "lazy" with async
    )
```

**Async session rules:**
- One `AsyncSession` per request — never share across concurrent tasks
- Use `async with` context manager for automatic cleanup
- Map session boundaries to transaction boundaries
- Use `selectin` or `joined` loading — lazy loading is incompatible with asyncio
- Use `run_sync()` only as a last resort for legacy code

#### Migration Planning

1. Schema change → Generate migration: `alembic revision --autogenerate -m "description"`
2. Review generated migration — verify column types, indexes, constraints
3. Test upgrade: `alembic upgrade head`
4. Test downgrade: `alembic downgrade -1`
5. Test data preservation: ensure existing data survives the round-trip

### Frontend Architecture

#### State Management Decision Tree

```
Is the data from the server?
├── YES → Use TanStack Query (useQuery, useMutation)
│         Configure staleTime, gcTime, query keys
│
└── NO → Is it needed across multiple components?
         ├── YES → Is it complex with actions/reducers?
         │         ├── YES → Use Zustand store
         │         └── NO  → Use React Context
         │
         └── NO → Use useState / useReducer locally
```

**TanStack Query conventions:**
- Query keys: `[resource, ...identifiers]` (e.g., `["users", userId]`, `["posts", { page, limit }]`)
- Use `queryOptions()` factory to centralize key + fn definitions — prevents copy-paste key errors
- Set `staleTime` based on data freshness needs (default 0 is too aggressive for most cases)
- Invalidate with `invalidateQueries()` after mutations — never manual `refetch()`
- Handle all states: `isPending`, `isError`, `data`

**Component design rules:**
- Props for configuration, hooks for data
- Lift state only as high as needed — no premature context creation
- Keep components under 200 lines — extract sub-components or custom hooks when larger
- Use `children` and composition over deep prop drilling

#### Routing Structure

Organize routes to mirror the URL structure:

```
src/
├── pages/
│   ├── HomePage.tsx           → /
│   ├── LoginPage.tsx          → /login
│   ├── users/
│   │   ├── UserListPage.tsx   → /users
│   │   └── UserDetailPage.tsx → /users/:id
│   └── settings/
│       └── SettingsPage.tsx   → /settings
```

### Cross-Cutting Concerns

#### Authentication Flow

```
Login Request
    ↓
Backend: Validate credentials → Generate JWT (access + refresh tokens)
    ↓
Frontend: Store access token in memory, refresh token in httpOnly cookie
    ↓
API Calls: Attach access token via Authorization header
    ↓
Token Expired: Use refresh token to obtain new access token
    ↓
Refresh Failed: Redirect to login
```

**Architecture decisions for auth:**
- Access tokens: short-lived (15-30 min), stored in memory (not localStorage)
- Refresh tokens: longer-lived (7-30 days), stored in httpOnly cookie
- Backend: FastAPI `Depends()` chain for token validation → user extraction → permission check
- Frontend: Auth context providing `user`, `login()`, `logout()`, `isAuthenticated`

#### Error Handling Strategy

Errors should be handled at the appropriate layer:

| Layer | Error Type | Action |
|-------|-----------|--------|
| Router | `HTTPException` | Return HTTP error response with status code |
| Service | Domain exceptions | Raise custom exceptions (e.g., `UserNotFoundError`) |
| Repository | Database exceptions | Catch and re-raise as domain exceptions or let propagate |
| Frontend | API errors | Display user-friendly messages, retry where appropriate |

**Backend exception hierarchy:**
```python
class AppError(Exception):
    """Base application error."""

class NotFoundError(AppError):
    """Resource not found."""

class ConflictError(AppError):
    """Resource conflict (duplicate, version mismatch)."""

class ValidationError(AppError):
    """Business rule violation."""
```

Router-level exception handler maps domain exceptions to HTTP responses:
```python
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

#### Logging Architecture

**Backend (structlog):**
- Structured JSON logs in production
- Human-readable console in development
- Bind request context (request_id, user_id) at middleware level
- Log at service layer (business events), not repository layer (too noisy)
- Use log levels: DEBUG (development only), INFO (business events), WARNING (recoverable issues), ERROR (failures requiring attention)

**Frontend:**
- `console.*` in development
- Structured error reporting to backend or Sentry in production
- Log user actions for debugging, not for analytics

#### Configuration Management

**Backend (pydantic-settings):**
```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str
    debug: bool = False
```

**Frontend (environment variables):**
- `VITE_API_URL` for API base URL
- Build-time injection via Vite's `import.meta.env`
- No secrets in frontend environment variables

## Examples

### Architecture Decision: Real-Time Notifications

**Problem:** The application needs real-time notifications for users (new messages, status updates).

**Options evaluated:**

| Option | Pros | Cons |
|--------|------|------|
| **WebSocket** | True bidirectional, low latency | Complex connection management, harder to scale |
| **Server-Sent Events (SSE)** | Simple, HTTP-based, auto-reconnect | Unidirectional (server→client only), limited browser connections |
| **Polling** | Simplest implementation, works everywhere | Higher latency, unnecessary server load |

**Decision:** WebSocket for this use case.

**Rationale:** Notifications require low latency and the system will eventually need bidirectional communication (typing indicators, presence). SSE would work for notifications alone but would require a separate solution for future bidirectional needs. Polling introduces unacceptable latency for real-time UX.

**Architecture:**
- Backend: FastAPI WebSocket endpoint with `ConnectionManager` class
- Frontend: Custom `useWebSocket` hook with automatic reconnection
- Scaling: Redis pub/sub for multi-instance message distribution
- Persistence: Store notifications in database for offline users
- Fallback: REST endpoint for notification history and initial load

See `references/architecture-decision-record-template.md` for the full ADR format.

## Edge Cases

### Monolith vs Microservices

**Default to modular monolith** for teams smaller than 10 developers. A modular monolith provides:
- Clear module boundaries without network overhead
- Shared database with module-specific schemas
- Easy refactoring and code navigation
- Simple deployment and debugging

**Consider microservices** only when:
- Independent scaling is required for specific components
- Different modules need different technology stacks
- Team size exceeds 10 and ownership boundaries are clear
- Deployment independence is a business requirement

**Migration path:** Design module boundaries in the monolith as if they were services (no direct cross-module database access, communicate via service interfaces). This makes extraction to microservices straightforward when needed.

### When to Break the Layer Pattern

The strict Router → Service → Repository pattern should be followed for standard CRUD operations. Acceptable exceptions:

- **Background tasks:** May call services directly without going through a router
- **Event handlers:** Domain event listeners may call services from any context
- **CLI commands:** Management scripts may access services or repositories directly
- **Migrations:** Data migrations may access models directly (no service/repo layer needed)
- **Health checks:** May access the database directly for simple connectivity verification

In all cases, business logic should still live in the service layer — these exceptions are about the entry point, not about bypassing business rules.

### Evolving Architecture

When the architecture needs to change:
1. Write an ADR documenting the motivation and the proposed change
2. Identify all affected modules and their dependencies
3. Plan an incremental migration — never big-bang rewrites
4. Maintain backward compatibility during transition (strangler fig pattern)
5. Set a deadline for completing the migration and removing legacy code
