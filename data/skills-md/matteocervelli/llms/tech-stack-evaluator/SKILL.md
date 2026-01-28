---
name: tech-stack-evaluator
description: Auto-activates during requirements analysis to evaluate technical stack
  compatibility, recommend appropriate technologies, and assess performance implications.
allowed-tools: Read, Bash, Grep
---

## Purpose

The **tech-stack-evaluator** skill provides systematic evaluation of technical stack requirements and compatibility for feature implementations. It analyzes existing project technology, recommends appropriate libraries/frameworks, assesses compatibility, and identifies performance implications.

## When to Use

This skill auto-activates when you:
- Evaluate technical stack requirements
- Assess technology compatibility
- Recommend frameworks or libraries
- Analyze performance implications
- Check language/framework suitability
- Review dependency compatibility
- Evaluate migration needs
- Assess scalability of technology choices

## Provided Capabilities

### 1. Technology Stack Analysis
- Identify current project stack (language, framework, libraries)
- Evaluate stack maturity and support
- Check version compatibility
- Assess ecosystem health

### 2. Library/Framework Recommendation
- Recommend appropriate libraries for requirements
- Compare alternatives
- Evaluate pros/cons
- Check community support and maintenance

### 3. Compatibility Assessment
- Check compatibility with existing stack
- Identify version conflicts
- Assess breaking changes
- Evaluate upgrade paths

### 4. Performance Analysis
- Evaluate performance characteristics
- Identify bottlenecks
- Assess scalability
- Consider resource requirements

### 5. Technology Constraints
- Identify platform limitations
- Check deployment constraints
- Assess infrastructure requirements
- Evaluate licensing constraints

## Usage Guide

### Step 1: Identify Current Project Stack

Check project configuration files:

**Python Projects**:
```bash
# Check Python version and dependencies
python --version
cat requirements.txt
cat pyproject.toml
cat setup.py
cat Pipfile

# Check installed packages
pip list
```

**TypeScript/JavaScript Projects**:
```bash
# Check Node version and dependencies
node --version
cat package.json
cat package-lock.json
cat yarn.lock
```

**Rust Projects**:
```bash
# Check Rust version and dependencies
rustc --version
cat Cargo.toml
cat Cargo.lock
```

**Document Current Stack**:
```markdown
## Current Project Stack

### Language & Runtime
- **Language**: Python 3.11
- **Package Manager**: uv
- **Virtual Environment**: venv

### Framework
- **Web Framework**: FastAPI 0.104.0
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.0

### Key Dependencies
- `httpx`: 0.25.2 (HTTP client)
- `redis`: 5.0.1 (Caching)
- `pytest`: 7.4.3 (Testing)

### Infrastructure
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Server**: Uvicorn
```

### Step 2: Analyze Feature Requirements

Based on extracted requirements, identify technology needs:

**Example Requirements**:
- "Real-time data synchronization" → WebSockets, async I/O
- "File processing" → File handling libraries
- "API integration" → HTTP client
- "Data validation" → Validation library
- "Background tasks" → Task queue

**Technology Mapping**:
```markdown
## Technology Requirements

| Requirement | Technology Need | Current Support | Gap |
|-------------|----------------|-----------------|-----|
| Real-time updates | WebSockets | ✅ FastAPI supports | None |
| Data validation | Schema validation | ✅ Pydantic | None |
| Background tasks | Task queue | ❌ No task queue | Need Celery/RQ |
| File uploads | File handling | ✅ Built-in | None |
| PDF generation | PDF library | ❌ No PDF lib | Need reportlab |
```

### Step 3: Recommend Technologies

Use `tech-stack-matrix.md` to match requirements with technologies:

**Python Recommendations**:

**Web Frameworks**:
- **FastAPI**: Modern, async, auto-docs (recommended for APIs)
- **Django**: Full-featured, ORM included (for full web apps)
- **Flask**: Lightweight, flexible (for simple apps)

**Database Libraries**:
- **SQLAlchemy**: Powerful ORM, wide DB support
- **Django ORM**: Tightly integrated with Django
- **asyncpg**: Async PostgreSQL driver (high performance)

**Validation**:
- **Pydantic**: Type-based validation, FastAPI integration
- **marshmallow**: Schema validation, serialization
- **cerberus**: Lightweight validation

**HTTP Clients**:
- **httpx**: Modern, async support (recommended)
- **requests**: Synchronous, widely used
- **aiohttp**: Async HTTP client/server

**Task Queues**:
- **Celery**: Mature, feature-rich
- **RQ** (Redis Queue): Simple, Redis-based
- **Dramatiq**: Simple, reliable

**Testing**:
- **pytest**: Most popular, plugin ecosystem
- **unittest**: Built-in, standard library
- **hypothesis**: Property-based testing

### Step 4: Evaluate Compatibility

Check for compatibility issues:

**Version Compatibility**:
```python
# Example: Check Python version requirements
import sys
if sys.version_info < (3, 10):
    raise RuntimeError("Requires Python 3.10+")
```

**Dependency Conflicts**:
```bash
# Check for dependency conflicts
pip check

# Analyze dependency tree
pip-tree
pipdeptree
```

**Compatibility Matrix**:
```markdown
## Compatibility Assessment

### Python Version Compatibility
- **Current**: Python 3.11
- **Required**: Python 3.10+ (for new libraries)
- **Status**: ✅ Compatible

### Framework Compatibility
| Library | Required Version | Current Version | Compatible | Notes |
|---------|-----------------|-----------------|------------|-------|
| FastAPI | ≥0.100.0 | 0.104.0 | ✅ | Compatible |
| Pydantic | ≥2.0.0 | 2.5.0 | ✅ | Compatible |
| SQLAlchemy | ≥2.0.0 | 2.0.23 | ✅ | Compatible |
| New: Celery | ≥5.3.0 | - | ✅ | No conflicts |
| New: reportlab | ≥4.0.0 | - | ✅ | No conflicts |

### Breaking Changes
- None identified for proposed libraries
```

### Step 5: Assess Performance Implications

Evaluate performance characteristics using `language-feature-map.md`:

**Performance Considerations**:

**Async I/O** (Python asyncio, FastAPI):
- **Pros**: High concurrency, efficient I/O handling
- **Cons**: Complexity, requires async-aware libraries
- **Use When**: Many concurrent connections, I/O-bound operations

**Database Performance**:
- **ORM Overhead**: SQLAlchemy adds ~10-20% overhead vs raw SQL
- **Mitigation**: Use bulk operations, eager loading, query optimization

**Caching Strategy**:
- **Redis**: In-memory, microsecond latency
- **Application Cache**: In-process, nanosecond latency
- **Recommendation**: Use Redis for shared cache, application cache for read-heavy data

**Serialization**:
- **JSON**: Standard, slow for large payloads
- **MessagePack**: Binary, 2-3x faster than JSON
- **Protobuf**: Schema-based, fastest, smallest

```markdown
## Performance Assessment

### Expected Performance Characteristics
- **API Response Time**: <200ms (target), FastAPI typically achieves 50-100ms
- **Database Query Time**: <50ms (with proper indexing)
- **Caching Hit Rate**: >80% (target)
- **Concurrent Users**: 1000+ (FastAPI handles well with async)

### Performance Optimizations
1. **Use Connection Pooling**: SQLAlchemy connection pool (size=20)
2. **Implement Caching**: Redis for frequently accessed data
3. **Async I/O**: Use httpx async client for external APIs
4. **Database Indexing**: Add indexes on frequently queried columns
5. **Background Processing**: Use Celery for heavy computations

### Performance Risks
- **Risk**: Large file uploads could block event loop
  - **Mitigation**: Use streaming uploads, background processing
- **Risk**: N+1 query problem with ORM
  - **Mitigation**: Use eager loading (joinedload, selectinload)
```

### Step 6: Identify Constraints

Document technical constraints:

**Platform Constraints**:
```markdown
## Technical Constraints

### Platform Requirements
- **OS**: Linux (Ubuntu 22.04+) or macOS
- **Python**: 3.10+ (for match statements, improved typing)
- **Database**: PostgreSQL 14+ (for JSON improvements)
- **Memory**: 2GB minimum, 4GB recommended
- **Storage**: 10GB for application + dependencies

### Deployment Constraints
- **Container**: Docker-compatible
- **Environment**: Supports environment variables
- **Network**: Outbound HTTPS required for external APIs
- **Ports**: 8000 (application), 5432 (database), 6379 (Redis)

### Licensing Constraints
- All proposed libraries use permissive licenses (MIT, Apache 2.0, BSD)
- No GPL dependencies (avoid copyleft)
- Commercial use permitted

### Development Constraints
- **IDE**: VS Code, PyCharm (type checking support)
- **Type Checking**: mypy required in CI/CD
- **Code Formatting**: Black, isort
- **Testing**: pytest with 80%+ coverage
```

### Step 7: Compare Alternatives

When multiple options exist, create comparison:

```markdown
## Technology Alternatives

### Task Queue Comparison

| Feature | Celery | RQ | Dramatiq |
|---------|--------|----|---------|
| **Maturity** | High (2009) | Medium (2011) | Medium (2016) |
| **Complexity** | High | Low | Low |
| **Broker** | RabbitMQ/Redis | Redis only | RabbitMQ/Redis |
| **Performance** | High | Medium | High |
| **Monitoring** | Flower | RQ Dashboard | Basic |
| **Learning Curve** | Steep | Gentle | Gentle |
| **Recommendation** | ⭐ Enterprise | ⭐ Simple | ⭐ Middle ground |

**Recommendation**: Use RQ for this project
- **Reasoning**: Already using Redis, simple requirements, faster learning curve
- **Trade-off**: Less features than Celery, but sufficient for current needs
```

### Step 8: Create Technology Recommendation

Synthesize findings into recommendation:

```markdown
## Technology Stack Recommendation

### New Libraries to Add

1. **RQ (Redis Queue)** - Background Task Processing
   - **Version**: 1.15.1+
   - **Purpose**: Process file uploads, send emails asynchronously
   - **Justification**: Simple, integrates with existing Redis, sufficient for needs
   - **Alternative Considered**: Celery (too complex for current requirements)

2. **reportlab** - PDF Generation
   - **Version**: 4.0.7+
   - **Purpose**: Generate PDF reports
   - **Justification**: Mature, feature-rich, good documentation
   - **Alternative Considered**: WeasyPrint (CSS-based, but slower)

3. **httpx** - Async HTTP Client
   - **Version**: 0.25.2+ (already using, version OK)
   - **Purpose**: Make async external API calls
   - **Justification**: Modern, async support, timeout handling
   - **Alternative Considered**: aiohttp (more complex API)

### No Changes Required

- **FastAPI**: Current framework suitable for requirements
- **Pydantic**: Current validation library sufficient
- **SQLAlchemy**: Current ORM handles database needs
- **pytest**: Current testing framework adequate

### Version Updates

None required - all current versions compatible with new libraries

### Compatibility Verification

✅ All proposed libraries compatible with:
- Python 3.11
- FastAPI 0.104.0
- Existing dependency versions

### Performance Impact

**Expected Improvements**:
- Background tasks don't block API responses (+50% perceived responsiveness)
- Async external API calls improve throughput (+30% under load)

**Minimal Overhead**:
- RQ: <5% overhead for task queuing
- reportlab: Only used on-demand for PDF generation
```

## Best Practices

### 1. Prefer Existing Stack
- Leverage technologies already in use
- Avoid introducing new languages/frameworks without strong justification
- Consider team familiarity

### 2. Evaluate Maturity
- Prefer mature, well-maintained libraries
- Check last update date (< 6 months ideal)
- Review GitHub stars, issues, contributors
- Check PyPI downloads for Python packages

### 3. Consider Ecosystem
- Strong community support
- Good documentation
- Active development
- Compatible with existing tools

### 4. Performance Testing
- Benchmark critical paths
- Load test under realistic conditions
- Profile to find bottlenecks
- Measure, don't assume

### 5. Future-Proofing
- Choose actively maintained libraries
- Prefer libraries with stable APIs
- Consider migration paths
- Avoid deprecated technologies

### 6. Security Considerations
- Check for known vulnerabilities (CVEs)
- Evaluate security track record
- Consider security features
- Review security advisories

## Resources

### tech-stack-matrix.md
Comprehensive matrix of:
- Popular libraries by category
- Framework comparisons
- Performance characteristics
- Compatibility notes
- Use case recommendations

### language-feature-map.md
Language-specific features:
- Python async/await capabilities
- TypeScript type system features
- Rust ownership model
- Performance characteristics
- Best practices

## Example Usage

### Input (Feature Requirements)
```
Feature: User notification system
- Send email notifications
- In-app real-time notifications
- Background processing for bulk sends
- Track delivery status
```

### Output (Tech Stack Evaluation)
```markdown
## Technical Stack Evaluation

### Current Stack Analysis
- **Language**: Python 3.11 ✅
- **Framework**: FastAPI 0.104.0 ✅ (WebSocket support for real-time)
- **Database**: PostgreSQL 15 ✅
- **Cache**: Redis 7 ✅

### Required Technologies

1. **Task Queue**: RQ 1.15.1
   - **Purpose**: Background email sending
   - **Justification**: Integrates with existing Redis, simple API
   - **Performance**: Handles 1000+ tasks/minute

2. **Email Library**: python-email-validator + SMTP
   - **Purpose**: Email validation and sending
   - **Justification**: Standard library sufficient, no extra dependencies
   - **Alternative**: SendGrid (if high volume needed)

3. **WebSocket**: FastAPI built-in
   - **Purpose**: Real-time in-app notifications
   - **Justification**: Already supported by FastAPI
   - **Performance**: Handles 10,000+ concurrent connections

4. **Notification Storage**: PostgreSQL (existing)
   - **Purpose**: Store notification history
   - **Justification**: Existing database, JSON column support
   - **Performance**: Adequate with proper indexing

### Compatibility Assessment
✅ All technologies compatible with existing stack
✅ No version conflicts
✅ No breaking changes required

### Performance Expectations
- **Email Send**: 100-200ms (backgrounded via RQ)
- **Real-time Push**: <50ms via WebSocket
- **Database Write**: <10ms
- **Overall**: <200ms API response (tasks queued)

### Recommendation
**Proceed with proposed stack** - all requirements met with minimal additions
```

## Integration

This skill is used by:
- **analysis-specialist** agent during Phase 1: Requirements Analysis
- Activates automatically when agent evaluates tech stack
- Provides technology assessment for analysis document generation

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when evaluating tech stack)
**Phase**: 1 (Requirements Analysis)
**Created**: 2025-10-29