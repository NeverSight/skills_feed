---
name: refactoring
description: Detect code smells and apply safe refactoring techniques
sasmp_version: "1.3.0"
bonded_agent: 04-refactoring
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# Refactoring Skill

> Atomic skill for code smell detection and safe refactoring

## Skill Definition

```yaml
skill_id: refactoring
responsibility: Single - Code smell detection and refactoring guidance
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  action: 'detect' | 'plan' | 'apply' | 'validate';
  code: string;
  language: string;

  // Optional
  smell_categories?: SmellCategory[];
  risk_tolerance?: 'low' | 'medium' | 'high';
  test_coverage?: 'none' | 'partial' | 'full';
}

type SmellCategory = 'bloaters' | 'oo_abusers' | 'change_preventers' | 'dispensables' | 'couplers';

interface SkillResult {
  smells?: CodeSmell[];
  plan?: RefactoringPlan;
  refactored_code?: string;
  validation?: ValidationResult;
}
```

## Validation Rules

```yaml
input_validation:
  action:
    required: true
    enum: [detect, plan, apply, validate]

  code:
    required: true
    min_length: 10
    max_length: 100000

  language:
    required: true
    allowed: [typescript, javascript, python, java, csharp, go]
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 1000
    max_delay_ms: 10000
    multiplier: 2

  retryable_errors:
    - TIMEOUT
    - RATE_LIMIT

  non_retryable_errors:
    - INVALID_CODE
    - UNSAFE_REFACTORING
```

## Code Smell Catalog

### Bloaters

```yaml
long_method:
  threshold: 20 lines
  severity_scale:
    20-30: low
    30-50: medium
    50+: high
  refactorings:
    - Extract Method
    - Replace Temp with Query

large_class:
  threshold: 200 lines
  refactorings:
    - Extract Class
    - Extract Subclass

long_parameter_list:
  threshold: 3 params
  refactorings:
    - Introduce Parameter Object
    - Preserve Whole Object
```

### Couplers

```yaml
feature_envy:
  description: "Method uses another class's data more than its own"
  refactorings:
    - Move Method
    - Extract Method

message_chains:
  pattern: "a.b().c().d().e()"
  threshold: 3 calls
  refactorings:
    - Hide Delegate
```

## Refactoring Techniques

```yaml
extract_method:
  safety: high
  steps:
    1. Create new method with descriptive name
    2. Copy extracted code
    3. Replace original with call
    4. Run tests

move_method:
  safety: medium
  steps:
    1. Copy method to target
    2. Adjust references
    3. Update callers
    4. Remove original
    5. Run tests
```

## Usage Examples

### Smell Detection
```typescript
// Input
{
  action: "detect",
  code: `
    class OrderProcessor {
      process(order, user, config, logger, db, cache, validator) {
        // 150 lines of code
      }
    }
  `,
  language: "typescript"
}

// Output
{
  smells: [
    {
      name: "Long Parameter List",
      category: "bloaters",
      severity: "high",
      location: "OrderProcessor.process"
    },
    {
      name: "Long Method",
      category: "bloaters",
      severity: "high"
    }
  ]
}
```

## Unit Test Template

```typescript
describe('RefactoringSkill', () => {
  describe('detect', () => {
    it('should detect Long Method smell', async () => {
      const code = generateLongMethod(60);
      const result = await skill.execute({
        action: 'detect',
        code,
        language: 'typescript'
      });

      expect(result.smells).toContainEqual(
        expect.objectContaining({ name: 'Long Method' })
      );
    });
  });
});
```

## Error Handling

```yaml
errors:
  INVALID_CODE:
    code: 400
    message: "Code cannot be parsed"
    recovery: "Fix syntax errors"

  UNSAFE_REFACTORING:
    code: 400
    message: "Refactoring too risky without tests"
    recovery: "Add tests or increase risk_tolerance"
```

## Integration

```yaml
requires:
  - ast_parser
  - smell_detector

emits:
  - smells_detected
  - refactoring_planned
  - refactoring_applied

consumed_by:
  - 04-refactoring (bonded agent)
  - 01-design-principles (for principle violations)
```
