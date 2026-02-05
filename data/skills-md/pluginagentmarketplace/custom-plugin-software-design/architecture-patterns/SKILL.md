---
name: architecture-patterns
description: Design, evaluate, and document software architecture patterns
sasmp_version: "1.3.0"
bonded_agent: 07-architecture-patterns
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# Architecture Patterns Skill

> Atomic skill for architecture design and evaluation

## Skill Definition

```yaml
skill_id: architecture-patterns
responsibility: Single - Architecture pattern recommendation and documentation
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  action: 'recommend' | 'evaluate' | 'document' | 'migrate';

  // Conditional
  requirements?: SystemRequirements;    // For recommend
  current_architecture?: string;        // For evaluate, migrate
  target_architecture?: string;         // For migrate

  // Optional
  constraints?: ArchitectureConstraints;
  team_size?: number;
  output_format?: 'text' | 'diagram' | 'adr';
}

interface SystemRequirements {
  functional: string[];
  non_functional: {
    scalability: 'low' | 'medium' | 'high';
    maintainability: 'low' | 'medium' | 'high';
    testability: 'low' | 'medium' | 'high';
    performance: 'low' | 'medium' | 'high';
  };
  domain_complexity: 'simple' | 'moderate' | 'complex';
}

interface SkillResult {
  recommendation?: ArchitectureRecommendation;
  evaluation?: ArchitectureEvaluation;
  documentation?: ArchitectureDocumentation;
  migration_plan?: MigrationPlan;
}
```

## Validation Rules

```yaml
input_validation:
  action:
    required: true
    enum: [recommend, evaluate, document, migrate]

  requirements:
    required_when: action == 'recommend'

  current_architecture:
    required_when: action in ['evaluate', 'migrate']
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 2000
    max_delay_ms: 20000
    multiplier: 2

  retryable_errors:
    - TIMEOUT
    - RATE_LIMIT

  non_retryable_errors:
    - INVALID_REQUIREMENTS
    - UNKNOWN_PATTERN
```

## Architecture Patterns

### Pattern Catalog

```yaml
layered:
  complexity: low
  scalability: limited
  testability: medium
  best_for:
    - Simple CRUD applications
    - Small teams (1-5)

hexagonal:
  complexity: medium
  scalability: high
  testability: high
  best_for:
    - Complex business logic
    - High testability requirements

clean:
  complexity: high
  scalability: high
  testability: high
  best_for:
    - Enterprise applications
    - Long-lived systems

cqrs:
  complexity: high
  scalability: very_high
  best_for:
    - Read-heavy systems
    - Different scaling requirements

event_sourcing:
  complexity: very_high
  scalability: very_high
  best_for:
    - Audit requirements
    - Temporal queries
```

### Decision Matrix

```yaml
decision_matrix:
  simple_crud:
    recommended: layered
    avoid: [event_sourcing, cqrs]

  complex_domain:
    recommended: hexagonal
    avoid: [layered]

  high_scalability:
    recommended: cqrs
    avoid: [layered]

  audit_requirements:
    recommended: event_sourcing
```

## Usage Examples

### Recommendation
```typescript
// Input
{
  action: "recommend",
  requirements: {
    functional: ["User management", "Order processing"],
    non_functional: {
      scalability: "high",
      maintainability: "high",
      testability: "high"
    },
    domain_complexity: "complex"
  },
  team_size: 8
}

// Output
{
  recommendation: {
    primary_pattern: "Hexagonal Architecture",
    alternatives: [
      { pattern: "Clean Architecture", fit_score: 0.85 }
    ],
    rationale: "Complex domain with high testability needs",
    tradeoffs: [
      { benefit: "High testability", cost: "Initial learning curve" }
    ]
  }
}
```

### ADR Generation
```typescript
// Input
{
  action: "document",
  system_description: "E-commerce platform with complex pricing",
  output_format: "adr"
}

// Output
{
  documentation: {
    adr: `
# ADR-001: Adopt Hexagonal Architecture

## Status
Accepted

## Context
Building e-commerce platform with complex pricing rules.

## Decision
Adopt Hexagonal Architecture with domain-centric design.

## Consequences
### Positive
- Domain logic isolated and highly testable
- Easy to swap external providers

### Negative
- More initial setup required
    `
  }
}
```

## Unit Test Template

```typescript
describe('ArchitecturePatternsSkill', () => {
  describe('recommend', () => {
    it('should recommend Layered for simple CRUD', async () => {
      const result = await skill.execute({
        action: 'recommend',
        requirements: {
          non_functional: { scalability: 'low' },
          domain_complexity: 'simple'
        },
        team_size: 3
      });

      expect(result.recommendation.primary_pattern).toBe('Layered Architecture');
    });

    it('should recommend Hexagonal for complex domain', async () => {
      const result = await skill.execute({
        action: 'recommend',
        requirements: {
          non_functional: { testability: 'high' },
          domain_complexity: 'complex'
        },
        team_size: 8
      });

      expect(result.recommendation.primary_pattern).toBe('Hexagonal Architecture');
    });
  });
});
```

## Error Handling

```yaml
errors:
  INVALID_REQUIREMENTS:
    code: 400
    message: "Requirements incomplete or invalid"
    recovery: "Provide at least functional or non-functional requirements"

  UNKNOWN_PATTERN:
    code: 400
    message: "Architecture pattern not recognized"
    recovery: "Use supported pattern name"
```

## Integration

```yaml
requires:
  - pattern_matcher
  - adr_generator

emits:
  - architecture_recommended
  - architecture_evaluated
  - adr_generated

consumed_by:
  - 07-architecture-patterns (bonded agent)
  - 05-domain-driven (for DDD architecture mapping)
```
