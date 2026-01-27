---
name: ac-complexity-assessor
description: Assess feature and project complexity. Use when estimating effort, determining spec pipeline type, calculating cost estimates, or planning resource allocation.
---

# AC Complexity Assessor

Assess complexity for effort estimation and planning.

## Purpose

Analyzes features and projects to determine complexity levels, estimate effort, and select appropriate processing pipelines.

## Quick Start

```python
from scripts.complexity_assessor import ComplexityAssessor

assessor = ComplexityAssessor(project_dir)
assessment = await assessor.assess_project()
print(assessment.pipeline_type)  # SIMPLE/STANDARD/COMPLEX
print(assessment.estimated_hours)
```

## Assessment Output

```json
{
  "project_complexity": "STANDARD",
  "pipeline_type": "STANDARD",
  "metrics": {
    "total_features": 75,
    "dependency_depth": 4,
    "category_count": 8,
    "integration_points": 5,
    "technology_complexity": 3
  },
  "estimates": {
    "total_hours": 120,
    "estimated_cost_usd": 45.00,
    "estimated_sessions": 15,
    "features_per_session": 5
  },
  "feature_estimates": [
    {
      "id": "auth-001",
      "complexity": "low",
      "estimated_hours": 1.5,
      "factors": ["standard_pattern", "no_dependencies"]
    }
  ],
  "recommendations": [
    "Consider parallelizing UI features",
    "auth-003 may need more time due to OAuth"
  ]
}
```

## Complexity Levels

### SIMPLE (1-3 phases)
- < 20 features
- Shallow dependencies (depth < 2)
- Single technology
- No external integrations

### STANDARD (7 phases)
- 20-100 features
- Moderate dependencies (depth 2-5)
- 2-3 technologies
- Limited integrations

### COMPLEX (8+ phases)
- > 100 features
- Deep dependencies (depth > 5)
- Multiple technologies
- Many integrations

## Complexity Factors

### Feature Complexity
- Implementation difficulty
- Test complexity
- Documentation needs
- Integration requirements

### Project Complexity
- Total feature count
- Dependency graph depth
- Technology stack breadth
- External integrations

### Risk Factors
- Unfamiliar technologies
- Complex algorithms
- Security requirements
- Performance constraints

## Pipeline Selection

```
SIMPLE Pipeline:
  1. Plan → 2. Implement → 3. Verify

STANDARD Pipeline:
  1. Analyze → 2. Plan → 3. Test Design
  4. Implement → 5. Test → 6. Review → 7. Verify

COMPLEX Pipeline:
  1. Deep Analyze → 2. Architecture → 3. Plan
  4. Test Design → 5. Implement → 6. Test
  7. Integration → 8. Review → 9. Verify
```

## Cost Estimation

```python
cost = (features * avg_tokens_per_feature * cost_per_token)
     + (sessions * session_overhead)
     + (complexity_multiplier * base_cost)
```

## API Reference

See `scripts/complexity_assessor.py` for full implementation.
