---
name: bad-example-skill
description: ANTI-PATTERN - Example showing violations of self-containment (DO NOT COPY)
category: framework
toolchain: python
tags: [anti-pattern, bad-example, violations]
version: 1.0.0
author: claude-mpm-skills
updated: 2025-11-30
progressive_disclosure:
  entry_point:
    summary: "ANTI-PATTERN - Example showing violations of self-containment (DO NOT COPY)"
    when_to_use: "When working with bad-example-skill or related functionality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# ⚠️ BAD EXAMPLE - Interdependent Skill (Anti-Pattern)

**WARNING**: This is an **ANTI-PATTERN** example showing what NOT to do.

**DO NOT COPY THIS STRUCTURE**. See [good-self-contained-skill](../good-self-contained-skill/) for correct approach.

---

## ❌ VIOLATION #1: Relative Path Dependencies

```markdown
## Related Documentation

For setup instructions, see [../setup-skill/SKILL.md](../setup-skill/SKILL.md)

For testing patterns, see:
- [../../testing/pytest-patterns/](../../testing/pytest-patterns/)
- [../../testing/test-utils/](../../testing/test-utils/)

Database integration: [../../data/database-skill/](../../data/database-skill/)
```

**Why This is Wrong**:
- ❌ Uses relative paths (`../`, `../../`)
- ❌ Assumes hierarchical directory structure
- ❌ Breaks in flat deployment (`~/.claude/skills/`)
- ❌ Links break when skill deployed standalone

**Correct Approach**:
```markdown
## Complementary Skills

Consider these related skills (if deployed):

- **setup-skill**: Installation and configuration patterns
- **pytest-patterns**: Testing framework and fixtures
- **database-skill**: Database integration patterns

*Note: All skills are independently deployable.*
```

---

## ❌ VIOLATION #2: Missing Essential Content

```markdown
## Testing

This skill uses pytest for testing.

**See pytest-patterns skill for all testing code.**

To write tests for this framework, install pytest-patterns skill
and refer to its documentation.
```

**Why This is Wrong**:
- ❌ No actual testing patterns included
- ❌ Requires user to have another skill
- ❌ Skill is incomplete without other skills
- ❌ "See other skill" instead of inlining

**Correct Approach**:
```markdown
## Testing (Self-Contained)

**Essential pytest pattern** (inlined):

```python
import pytest
from example_framework.testing import TestClient

@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)

def test_home_route(client):
    """Test homepage."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}
```

**Advanced fixtures** (if pytest-patterns skill deployed):
- Parametrized fixtures
- Database session fixtures
- Mock fixtures

*See pytest-patterns skill for comprehensive patterns.*
```

---

## ❌ VIOLATION #3: Hard Skill Dependencies

```markdown
## Prerequisites

**Required Skills**:
1. **setup-skill** - Must be installed first
2. **database-skill** - Required for database operations
3. **pytest-patterns** - Required for testing

Install all required skills before using this skill:
```bash
claude-code skills add setup-skill database-skill pytest-patterns
```

This skill will not work without these dependencies.
```

**Why This is Wrong**:
- ❌ Lists other skills as "Required"
- ❌ Skill doesn't work standalone
- ❌ Creates deployment coupling
- ❌ Violates self-containment principle

**Correct Approach**:
```markdown
## Prerequisites

**External Dependencies**:
```bash
pip install example-framework pytest sqlalchemy
```

## Complementary Skills

When using this skill, consider (if deployed):
- **setup-skill**: Advanced configuration patterns (optional)
- **database-skill**: ORM patterns and optimization (optional)
- **pytest-patterns**: Testing enhancements (optional)

*This skill is fully functional independently.*
```

---

## ❌ VIOLATION #4: Cross-Skill Imports

```python
"""
Bad example - importing from other skills.
"""

# ❌ DON'T DO THIS
from skills.database_skill import get_db_session
from skills.pytest_patterns import fixture_factory
from ..shared.utils import validate_input

# Using imported patterns
@app.route("/users")
def create_user(data):
    # Requires database-skill to be installed
    with get_db_session() as session:
        user = User(**data)
        session.add(user)
        return user.to_dict()
```

**Why This is Wrong**:
- ❌ Imports from other skills
- ❌ Code won't run without other skills
- ❌ Creates runtime dependencies
- ❌ Violates Python module boundaries

**Correct Approach**:
```python
"""
Good example - self-contained implementation.
"""
from contextlib import contextmanager

# ✅ Include pattern directly in this skill
@contextmanager
def get_db_session():
    """Database session context manager (self-contained)."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@app.route("/users")
def create_user(data):
    # Works independently
    with get_db_session() as session:
        user = User(**data)
        session.add(user)
        return user.to_dict()
```

---

## ❌ VIOLATION #5: Hierarchical Directory Assumptions

```markdown
## Project Structure

This skill is located in:
```
toolchains/python/frameworks/bad-example-skill/
```

**Navigate to parent directories for related skills**:
- `../` - Other framework skills
- `../../testing/` - Testing skills
- `../../data/` - Database skills

**All skills in `toolchains/python/frameworks/` are related to this skill.**
```

**Why This is Wrong**:
- ❌ Assumes specific directory structure
- ❌ Navigation instructions using relative paths
- ❌ Won't work in flat deployment
- ❌ Confuses deployment location with skill relationships

**Correct Approach**:
```markdown
## Related Skills

**Complementary Python Framework Skills** (informational):

- **fastapi-patterns**: Web framework patterns
- **django-patterns**: Full-stack framework patterns
- **flask-patterns**: Micro-framework patterns

**Testing Skills**:
- **pytest-patterns**: Testing framework
- **test-driven-development**: TDD workflow

*Note: Skills are independently deployable. Directory structure may vary.*
```

---

## ❌ VIOLATION #6: Incomplete Examples

```python
# Database setup
# (See database-skill for complete implementation)

class User(db.Model):
    # ... see database-skill for model definition ...
    pass

# Testing
# (See pytest-patterns for test examples)

def test_user():
    # ... see pytest-patterns for fixtures ...
    pass

# Deployment
# (See deployment-skill for production setup)
```

**Why This is Wrong**:
- ❌ Examples are fragments, not complete code
- ❌ "See other skill" instead of showing code
- ❌ Users can't copy-paste and run
- ❌ Skill provides no actual implementation guidance

**Correct Approach**:
```python
# Complete database model (self-contained)
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """User model - complete implementation."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# Complete test example (self-contained)
import pytest
from example_framework.testing import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_create_user(client):
    """Test user creation - complete working test."""
    response = client.post("/users", json={
        "username": "testuser",
        "email": "test@example.com"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

# Complete deployment example (self-contained)
import os

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

app = App(config=ProductionConfig())

# Run with: gunicorn -w 4 app:app
```

---

## ❌ VIOLATION #7: References Directory with Cross-Skill Paths

```
bad-example-skill/
├── SKILL.md
├── metadata.json
└── references/
    ├── testing.md          # Contains: ../../pytest-patterns/
    ├── database.md         # Contains: ../../database-skill/
    └── deployment.md       # Contains: ../../../universal/deployment/
```

**references/testing.md contains**:
```markdown
# Testing Patterns

For complete testing patterns, see:
- [Pytest Patterns](../../pytest-patterns/SKILL.md)
- [TDD Workflow](../../../universal/testing/test-driven-development/)

Refer to those skills for all testing code.
```

**Why This is Wrong**:
- ❌ References directory has cross-skill paths
- ❌ Progressive disclosure leads outside skill
- ❌ Breaks in flat deployment
- ❌ References aren't self-contained

**Correct Approach**:
```
good-example-skill/
├── SKILL.md
├── metadata.json
└── references/
    ├── advanced-patterns.md    # All about THIS skill
    ├── api-reference.md        # THIS skill's API
    └── examples.md             # THIS skill's examples
```

**references/advanced-patterns.md should contain**:
```markdown
# Advanced Testing Patterns

**Advanced pytest fixtures** (this skill):

```python
# Parametrized test fixture
@pytest.fixture(params=["value1", "value2"])
def data_variants(request):
    return request.param

def test_with_variants(data_variants):
    # Test with multiple data variants
    assert process(data_variants) is not None
```

**Further enhancements** (if pytest-patterns deployed):
- Fixture factories
- Custom markers
- Plugin integration

*See pytest-patterns skill for comprehensive advanced patterns.*
```

---

## ❌ VIOLATION #8: metadata.json with Skill Dependencies

```json
{
  "name": "bad-example-skill",
  "version": "1.0.0",
  "requires": [
    "setup-skill",
    "database-skill",
    "pytest-patterns"
  ],
  "self_contained": false,
  "dependencies": ["example-framework"],
  "notes": [
    "This skill requires setup-skill to be installed first",
    "Must deploy with database-skill for database operations",
    "Won't work without pytest-patterns for testing"
  ]
}
```

**Why This is Wrong**:
- ❌ Lists other skills in "requires" field
- ❌ `"self_contained": false`
- ❌ Notes say skill won't work without others
- ❌ Creates deployment coupling

**Correct Approach**:
```json
{
  "name": "good-example-skill",
  "version": "1.0.0",
  "requires": [],
  "self_contained": true,
  "dependencies": ["example-framework", "pytest", "sqlalchemy"],
  "complementary_skills": [
    "setup-skill",
    "database-skill",
    "pytest-patterns"
  ],
  "notes": [
    "This skill is fully self-contained and works independently",
    "All essential patterns are inlined",
    "Complementary skills provide optional enhancements"
  ]
}
```

---

## Summary of Violations

| Violation | Example | Impact |
|-----------|---------|--------|
| **Relative Paths** | `../../other-skill/` | Breaks in flat deployment |
| **Missing Content** | "See other skill for X" | Incomplete, not self-sufficient |
| **Hard Dependencies** | "Requires other-skill" | Can't deploy standalone |
| **Cross-Skill Imports** | `from skills.other import` | Runtime dependency |
| **Hierarchical Assumptions** | "Navigate to parent dir" | Location-dependent |
| **Incomplete Examples** | Code fragments only | Not usable |
| **References Cross-Skill** | `references/` has `../` | Progressive disclosure broken |
| **Metadata Dependencies** | `"requires": ["skill"]` | Deployment coupling |

---

## How to Fix These Violations

### Step 1: Remove All Relative Paths
```bash
# Find violations
grep -r "\.\\./" bad-example-skill/

# Remove them - use skill names instead
# ❌ [skill](../../skill/SKILL.md)
# ✅ skill (if deployed)
```

### Step 2: Inline Essential Content
```markdown
# Before (wrong):
## Testing
See pytest-patterns skill for all testing code.

# After (correct):
## Testing (Self-Contained)

**Essential pattern** (inlined):
[20-50 lines of actual testing code]

**Advanced patterns** (if pytest-patterns deployed):
- Feature list

*See pytest-patterns for comprehensive guide.*
```

### Step 3: Remove Hard Dependencies
```markdown
# Before (wrong):
**Required Skills**: pytest-patterns, database-skill

# After (correct):
**Complementary Skills** (optional):
- pytest-patterns: Testing enhancements
- database-skill: ORM optimization
```

### Step 4: Make Imports Self-Contained
```python
# Before (wrong):
from skills.database import get_db_session

# After (correct):
@contextmanager
def get_db_session():
    """Inlined pattern."""
    # Implementation here
```

### Step 5: Update metadata.json
```json
// Before (wrong):
{
  "requires": ["other-skill"],
  "self_contained": false
}

// After (correct):
{
  "requires": [],
  "self_contained": true,
  "complementary_skills": ["other-skill"]
}
```

---

## Verification

After fixing, verify self-containment:

```bash
# Should return empty (no violations)
grep -r "\.\\./" skill-name/
grep -r "from skills\." skill-name/
grep -i "requires.*skill" skill-name/SKILL.md

# Isolation test
cp -r skill-name /tmp/skill-test/
cd /tmp/skill-test/skill-name
cat SKILL.md  # Should be complete and useful

# Metadata check
cat metadata.json | jq '.requires'  # Should be [] or external packages only
```

---

## See Good Example Instead

**DO NOT USE THIS EXAMPLE AS A TEMPLATE**

Instead, see:
- **[good-self-contained-skill](../good-self-contained-skill/)**: Correct template
- **[SKILL_SELF_CONTAINMENT_STANDARD.md](../../docs/SKILL_SELF_CONTAINMENT_STANDARD.md)**: Complete standard

---

**Remember**: This example shows what NOT to do. Always ensure your skills are self-contained!
