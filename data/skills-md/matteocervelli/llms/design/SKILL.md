---
name: design
description: Design system architecture, API contracts, and data flows. Use when translating
  analyzed requirements into technical design for feature implementation.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Feature Design Skill

## Purpose

This skill provides systematic guidance for designing software architecture, API contracts, data models, and workflows based on analyzed requirements.

## When to Use

- After requirements analysis is complete
- Need to design technical architecture for a feature
- Defining API contracts and data structures
- Planning module interactions and data flows
- Before starting implementation

## Design Workflow

### 1. Architecture Design

**Choose Architectural Pattern:**
Review `architecture-patterns.md` for appropriate patterns:
- **Layered Architecture**: UI → Business Logic → Data Access
- **Modular Architecture**: Cohesive modules with clear interfaces
- **Event-Driven**: Message-based communication
- **Microservices**: Independent, deployable services (if applicable)

**For This Project (Python):**
- Follow existing structure: `src/tools/`, `src/core/`, `src/utils/`
- Use dependency injection for testability
- Keep files under 500 lines (split if needed)
- Maintain single responsibility principle

**Define Components:**
```
Component Name: <name>
Responsibility: <what it does>
Dependencies: <what it needs>
Interfaces: <public API>
```

**Deliverable:** Component diagram with responsibilities

### 2. Data Model Design

**Define Entities:**
- Identify domain entities from requirements
- Define attributes and types
- Specify relationships (one-to-one, one-to-many, many-to-many)
- Define validation rules
- Consider data lifecycle (CRUD operations)

**For Python Projects:**
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EntityModel(BaseModel):
    """Entity description."""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic configuration."""
        validate_assignment = True
```

**Deliverable:** Data models with Pydantic schemas

### 3. API Design

**Design API Contracts:**
Refer to `api-design-guide.md` for best practices

**REST API Pattern:**
```
Resource: /api/v1/resources
Methods:
  GET    /resources        - List resources
  GET    /resources/{id}   - Get single resource
  POST   /resources        - Create resource
  PUT    /resources/{id}   - Update resource (full)
  PATCH  /resources/{id}   - Update resource (partial)
  DELETE /resources/{id}   - Delete resource

Request Body:
  {
    "field1": "value",
    "field2": 123
  }

Response Body:
  {
    "data": {...},
    "meta": {
      "timestamp": "2025-01-15T10:30:00Z",
      "version": "1.0"
    }
  }

Error Response:
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Field validation failed",
      "details": [...]
    }
  }
```

**For Internal APIs (Python Functions/Methods):**
```python
def process_feature(
    input_data: InputModel,
    options: Optional[ProcessOptions] = None
) -> ProcessResult:
    """
    Process feature with given input.

    Args:
        input_data: Input data model
        options: Optional processing options

    Returns:
        ProcessResult with outcome

    Raises:
        ValidationError: If input is invalid
        ProcessError: If processing fails
    """
    pass
```

**Deliverable:** API specification with request/response formats

### 4. Data Flow Design

**Map Data Flows:**
- Input sources (user input, API, database, file)
- Processing steps (validation, transformation, business logic)
- Output destinations (response, database, file, external service)
- Error paths and handling

**Sequence Diagram Format:**
```
User → API Endpoint → Validator → Business Logic → Repository → Database
                          ↓             ↓              ↓
                      ValidationError  BusinessError  DatabaseError
                          ↓             ↓              ↓
                      Error Handler → Error Response → User
```

**Deliverable:** Sequence diagrams for key workflows

### 5. Module Interaction Design

**Define Module Boundaries:**
- **Interfaces**: Public API contracts (abstract classes, protocols)
- **Core Logic**: Business logic implementation
- **Utilities**: Helper functions (pure, stateless)
- **Data Access**: Repository pattern for persistence

**Python Module Structure:**
```
src/tools/feature_name/
├── __init__.py           # Public exports
├── models.py             # Pydantic models
├── interfaces.py         # Abstract interfaces
├── core.py               # Core business logic
├── repository.py         # Data access layer
├── validators.py         # Input validation
├── utils.py              # Helper functions
└── tests/
    ├── test_core.py
    ├── test_validators.py
    └── fixtures.py
```

**Dependency Injection Pattern:**
```python
class FeatureService:
    """Service with injected dependencies."""

    def __init__(
        self,
        repository: FeatureRepository,
        validator: FeatureValidator
    ):
        self.repository = repository
        self.validator = validator
```

**Deliverable:** Module dependency graph

### 6. Error Handling Design

**Define Error Hierarchy:**
```python
class FeatureError(Exception):
    """Base exception for feature."""
    pass

class ValidationError(FeatureError):
    """Input validation failed."""
    pass

class ProcessingError(FeatureError):
    """Processing failed."""
    pass

class NotFoundError(FeatureError):
    """Resource not found."""
    pass
```

**Error Handling Strategy:**
- Validate early (fail fast)
- Catch specific exceptions
- Log errors with context
- Return meaningful error messages
- Don't expose internal details

**Deliverable:** Error handling specification

### 7. Configuration Design

**Externalize Configuration:**
```python
from pydantic_settings import BaseSettings

class FeatureConfig(BaseSettings):
    """Feature configuration from environment."""

    api_key: str
    timeout: int = 30
    max_retries: int = 3
    debug: bool = False

    class Config:
        env_prefix = "FEATURE_"
        case_sensitive = False
```

**Configuration Sources:**
1. Environment variables (highest priority)
2. .env files
3. Configuration files (JSON/YAML)
4. Default values (lowest priority)

**Deliverable:** Configuration specification

## Output Format

Use the `templates/architecture-doc.md` template to generate:

```markdown
# Architecture Design: [Feature Name]

## Overview
Brief description of the feature and design approach.

## Architecture Pattern
[Chosen pattern] with rationale.

## Component Design
### Component 1: [Name]
- **Responsibility**: [What it does]
- **Dependencies**: [What it needs]
- **Interface**: [Public API]

## Data Model
### Entity: [Name]
```python
class EntityModel(BaseModel):
    field: str
```

## API Specification
### Endpoint: [Method] [Path]
- **Request**: [Schema]
- **Response**: [Schema]
- **Errors**: [Error codes]

## Data Flows
[Sequence diagrams or descriptions]

## Module Structure
```
src/tools/feature/
├── ...
```

## Error Handling
[Exception hierarchy and strategy]

## Configuration
[Required configuration with defaults]

## Testing Strategy
- Unit tests: [What to test]
- Integration tests: [What to test]
- Mocking strategy: [What to mock]

## Security Considerations
[From security-checklist.md in analysis phase]

## Performance Considerations
- Expected throughput: [N req/s]
- Response time: [< N ms]
- Resource usage: [Memory, CPU]

## Implementation Notes
[Any specific guidance for implementation]

## Open Questions
- [ ] Question 1
- [ ] Question 2
```

## Best Practices

**Architecture:**
- Prefer composition over inheritance
- Design for testability (dependency injection)
- Keep modules loosely coupled
- Follow SOLID principles
- Keep files under 500 lines

**Data Models:**
- Use Pydantic for validation
- Type hint everything
- Provide sensible defaults
- Document field constraints
- Consider backward compatibility

**APIs:**
- RESTful for external APIs
- Clear function signatures for internal APIs
- Consistent naming conventions
- Version APIs from the start
- Document all parameters and return values

**Error Handling:**
- Create specific exception types
- Log errors with sufficient context
- Don't catch exceptions you can't handle
- Provide actionable error messages
- Consider retry strategies

## Supporting Resources

- **architecture-patterns.md**: Common architectural patterns
- **api-design-guide.md**: API design best practices
- **templates/architecture-doc.md**: Output template

## Example Usage

```bash
# 1. Review analysis report from previous phase
Read docs/implementation/feature-name-analysis.md

# 2. Choose architecture pattern
Review architecture-patterns.md

# 3. Design data models
Create models.py with Pydantic schemas

# 4. Design API contracts
Use api-design-guide.md for REST/function APIs

# 5. Design module structure
Follow project conventions (src/tools/...)

# 6. Generate architecture document
Use templates/architecture-doc.md template

# 7. Review and validate
Check design meets requirements from analysis phase
```

## Integration with Feature Implementation Flow

**Input:** Requirements analysis report
**Process:** Systematic design using patterns and guidelines
**Output:** Architecture document with specs
**Next Step:** Implementation skill for coding

## Design Review Checklist

Before proceeding to implementation:
- [ ] Architecture pattern chosen and justified
- [ ] All components identified with clear responsibilities
- [ ] Data models defined with Pydantic schemas
- [ ] API contracts specified (endpoints or function signatures)
- [ ] Data flows documented (sequence diagrams)
- [ ] Module structure follows project conventions
- [ ] Error handling strategy defined
- [ ] Configuration externalized
- [ ] Testing strategy outlined
- [ ] Security considerations addressed
- [ ] Performance requirements documented
- [ ] Design reviewed by peer (if applicable)
- [ ] Stakeholder sign-off (if required)