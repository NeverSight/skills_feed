---
name: domain-driven-design
description: Model business domains using DDD tactical and strategic patterns
sasmp_version: "1.3.0"
bonded_agent: 05-domain-driven
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# Domain-Driven Design Skill

> Atomic skill for domain modeling and DDD pattern application

## Skill Definition

```yaml
skill_id: domain-driven-design
responsibility: Single - Domain modeling and DDD pattern guidance
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  action: 'model' | 'aggregate' | 'context_map' | 'event_storm';
  domain_description: string;

  // Optional
  existing_models?: string;
  stakeholder_terms?: string[];
  complexity?: 'core' | 'supporting' | 'generic';
  output_format?: 'text' | 'code' | 'diagram';
}

interface SkillResult {
  domain_model?: DomainModel;
  aggregates?: AggregateDefinition[];
  context_map?: ContextMap;
  event_storm?: EventStormResult;
  ubiquitous_language?: GlossaryEntry[];
}
```

## Validation Rules

```yaml
input_validation:
  action:
    required: true
    enum: [model, aggregate, context_map, event_storm]

  domain_description:
    required: true
    min_length: 50
    max_length: 10000
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 1500
    max_delay_ms: 15000
    multiplier: 2

  retryable_errors:
    - TIMEOUT
    - RATE_LIMIT

  non_retryable_errors:
    - INSUFFICIENT_DOMAIN_INFO
```

## DDD Building Blocks

### Tactical Patterns

```yaml
entity:
  characteristics:
    - Has identity
    - Has lifecycle
    - Can change state
  example:
    name: Order
    identity: orderId

value_object:
  characteristics:
    - No identity
    - Immutable
    - Equality by attributes
  example:
    name: Money
    attributes: [amount, currency]

aggregate:
  characteristics:
    - Consistency boundary
    - Single root entity
    - Transactional unit
  rules:
    - Reference by ID only
    - Single aggregate per transaction
```

### Strategic Patterns

```yaml
bounded_context:
  identification:
    - Linguistic boundary
    - Team ownership
    - Model consistency scope

context_map_patterns:
  - partnership
  - customer_supplier
  - conformist
  - anticorruption_layer
  - open_host_service
```

## Usage Examples

### Domain Modeling
```typescript
// Input
{
  action: "model",
  domain_description: `
    E-commerce order management system. Customers place orders
    containing multiple products.
  `
}

// Output
{
  domain_model: {
    entities: [
      { name: "Order", identity: "orderId" },
      { name: "Customer", identity: "customerId" }
    ],
    value_objects: [
      { name: "Address", attributes: ["street", "city", "zip"] },
      { name: "Money", attributes: ["amount", "currency"] }
    ],
    aggregates: [
      {
        name: "Order",
        root_entity: "Order",
        entities: ["OrderLine"],
        invariants: ["Order total must equal sum of line totals"]
      }
    ]
  },
  ubiquitous_language: [
    { term: "Order", definition: "A customer's request to purchase products" }
  ]
}
```

## Unit Test Template

```typescript
describe('DomainDrivenDesignSkill', () => {
  describe('model', () => {
    it('should identify entities from domain description', async () => {
      const result = await skill.execute({
        action: 'model',
        domain_description: 'Customers place orders for products'
      });

      expect(result.domain_model.entities.map(e => e.name))
        .toContain('Customer');
    });
  });

  describe('aggregate', () => {
    it('should define aggregate boundaries based on invariants', async () => {
      const result = await skill.execute({
        action: 'aggregate',
        domain_description: 'Order with lines, total must match'
      });

      expect(result.aggregates[0].invariants).toBeDefined();
    });
  });
});
```

## Error Handling

```yaml
errors:
  INSUFFICIENT_DOMAIN_INFO:
    code: 400
    message: "Domain description lacks sufficient detail"
    recovery: "Provide more business context and rules"

  AMBIGUOUS_BOUNDARIES:
    code: 422
    message: "Cannot determine clear aggregate boundaries"
    recovery: "Clarify invariants and transactional requirements"
```

## Integration

```yaml
requires:
  - nlp_analyzer
  - domain_extractor

emits:
  - domain_modeled
  - aggregate_defined
  - context_mapped

consumed_by:
  - 05-domain-driven (bonded agent)
  - 07-architecture-patterns (for architecture mapping)
```
