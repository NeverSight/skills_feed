---
name: ac-spec-generator
description: Generate feature lists from specifications. Use when creating feature_list.json, converting requirements to features, generating 50-100+ testable features, or initializing autonomous projects.
---

# AC Spec Generator

Generate comprehensive feature lists from project specifications.

## Purpose

Transforms parsed specifications into actionable feature lists with testable acceptance criteria, enabling autonomous implementation.

## Quick Start

```python
from scripts.spec_generator import SpecGenerator

generator = SpecGenerator(project_dir)
feature_list = await generator.generate(spec)
await generator.save_feature_list(feature_list)
```

## Feature List Schema

```json
{
  "features": [
    {
      "id": "auth-001",
      "description": "User can register with email and password",
      "category": "authentication",
      "status": "pending",
      "passes": false,
      "test_cases": [
        "Valid registration creates user",
        "Duplicate email shows error",
        "Weak password rejected"
      ],
      "dependencies": [],
      "estimated_effort": "2h",
      "priority": 1
    }
  ],
  "total": 50,
  "completed": 0,
  "metadata": {
    "generated_at": "2024-01-15T10:00:00Z",
    "spec_version": "1.0.0"
  }
}
```

## Generation Strategy

### Feature Decomposition
- Break requirements into atomic, testable units
- Generate 50-100+ features for comprehensive coverage
- Order by dependency (foundations first)
- Group by category for organization

### Categories
- `core`: Essential functionality
- `authentication`: Login/register/permissions
- `data`: Models, storage, retrieval
- `api`: Endpoints, integrations
- `ui`: User interface components
- `testing`: Test infrastructure
- `deployment`: CI/CD, hosting

### Priority Assignment
1. **Critical**: Blocks other features
2. **High**: Core functionality
3. **Medium**: Important but not blocking
4. **Low**: Nice-to-have, polish

## Workflow

1. **Parse**: Load and validate spec
2. **Analyze**: Identify requirement patterns
3. **Decompose**: Break into atomic features
4. **Prioritize**: Assign priority and order
5. **Enrich**: Add test cases and estimates
6. **Export**: Save feature_list.json

## Integration

- Input: Parsed spec from `ac-spec-parser`
- Output: Feature list for `ac-state-tracker`
- Uses: `ac-complexity-assessor` for estimates

## API Reference

See `scripts/spec_generator.py` for full implementation.
