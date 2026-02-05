---
name: solid-principles
description: Apply and validate SOLID principles in object-oriented design
sasmp_version: "1.3.0"
bonded_agent: 01-design-principles
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# SOLID Principles Skill

> Atomic skill for applying and validating SOLID principles

## Skill Definition

```yaml
skill_id: solid-principles
responsibility: Single - SOLID principle analysis and application
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  code: string;                    // Code to analyze
  language: string;                // Programming language

  // Optional
  principles?: ('SRP' | 'OCP' | 'LSP' | 'ISP' | 'DIP')[];  // Focus areas
  strictness?: 'relaxed' | 'normal' | 'strict';            // Validation level
  include_examples?: boolean;                               // Show fixes
}

interface SkillResult {
  violations: Violation[];
  compliance_score: number;        // 0-100
  suggestions: Suggestion[];
  metrics: PrincipleMetrics;
}
```

## Validation Rules

```yaml
input_validation:
  code:
    min_length: 10
    max_length: 50000
    required: true
  language:
    allowed: [typescript, javascript, python, java, csharp, go, ruby]
    required: true
  principles:
    default: ['SRP', 'OCP', 'LSP', 'ISP', 'DIP']

output_validation:
  compliance_score:
    min: 0
    max: 100
  violations:
    max_count: 50
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
    - CONTEXT_OVERFLOW

  non_retryable_errors:
    - INVALID_INPUT
    - UNSUPPORTED_LANGUAGE
```

## Logging & Observability

```yaml
logging:
  level: INFO
  events:
    - skill_invoked
    - analysis_started
    - violation_found
    - analysis_completed
    - error_occurred

metrics:
  - name: analysis_duration_ms
    type: histogram
  - name: violations_per_principle
    type: counter
  - name: compliance_score
    type: gauge

tracing:
  span_name: solid_principles_analysis
  attributes:
    - language
    - code_size
    - principle_count
```

## Principle Definitions

### SRP - Single Responsibility Principle

```yaml
definition: "A class should have only one reason to change"
detection:
  indicators:
    - Multiple unrelated methods
    - Mixed abstraction levels
    - Too many dependencies
  thresholds:
    methods_per_class: 10
    dependencies: 5
    lines_of_code: 200
```

### OCP - Open/Closed Principle

```yaml
definition: "Open for extension, closed for modification"
detection:
  indicators:
    - Switch statements on type
    - Instanceof/typeof checks
    - Frequent modifications for new features
  patterns:
    - Strategy pattern opportunity
    - Template method opportunity
```

### LSP - Liskov Substitution Principle

```yaml
definition: "Subtypes must be substitutable for base types"
detection:
  indicators:
    - Overridden methods with different behavior
    - Empty method implementations
    - Type checking in polymorphic code
  violations:
    - Precondition strengthening
    - Postcondition weakening
    - Invariant breaking
```

### ISP - Interface Segregation Principle

```yaml
definition: "Clients should not depend on interfaces they don't use"
detection:
  indicators:
    - Large interfaces (>5 methods)
    - Unused method implementations
    - Throw NotImplemented patterns
  thresholds:
    max_interface_methods: 5
```

### DIP - Dependency Inversion Principle

```yaml
definition: "Depend on abstractions, not concretions"
detection:
  indicators:
    - Direct instantiation with 'new'
    - Concrete class parameters
    - No interface/abstract usage
  patterns:
    - Constructor injection missing
    - Service locator anti-pattern
```

## Usage Examples

### Basic Analysis
```typescript
// Input
{
  code: "class UserService { ... }",
  language: "typescript"
}

// Output
{
  violations: [
    {
      principle: "SRP",
      location: "UserService:1",
      severity: "high",
      message: "Class has 5 different responsibilities",
      suggestion: "Extract to: AuthService, ProfileService, NotificationService"
    }
  ],
  compliance_score: 65,
  suggestions: [...],
  metrics: { srp: 60, ocp: 80, lsp: 100, isp: 70, dip: 45 }
}
```

### Focused Analysis
```typescript
// Input
{
  code: "interface Repository { ... }",
  language: "typescript",
  principles: ["ISP"],
  strictness: "strict"
}
```

## Unit Test Template

```typescript
describe('SolidPrinciplesSkill', () => {
  describe('analyze', () => {
    it('should detect SRP violation in god class', async () => {
      const code = `
        class UserManager {
          saveUser() {}
          sendEmail() {}
          generateReport() {}
          validateInput() {}
          logActivity() {}
        }
      `;

      const result = await skill.analyze({ code, language: 'typescript' });

      expect(result.violations).toContainEqual(
        expect.objectContaining({ principle: 'SRP' })
      );
      expect(result.compliance_score).toBeLessThan(70);
    });

    it('should pass for well-designed code', async () => {
      const code = `
        class UserRepository {
          save(user: User): void {}
          find(id: string): User {}
          delete(id: string): void {}
        }
      `;

      const result = await skill.analyze({ code, language: 'typescript' });

      expect(result.violations).toHaveLength(0);
      expect(result.compliance_score).toBeGreaterThan(90);
    });

    it('should handle invalid input gracefully', async () => {
      await expect(
        skill.analyze({ code: '', language: 'typescript' })
      ).rejects.toThrow('INVALID_INPUT');
    });
  });
});
```

## Error Handling

```yaml
errors:
  INVALID_INPUT:
    code: 400
    message: "Invalid input parameters"
    recovery: "Check parameter schema"

  UNSUPPORTED_LANGUAGE:
    code: 400
    message: "Language not supported"
    recovery: "Use supported language"

  ANALYSIS_TIMEOUT:
    code: 408
    message: "Analysis exceeded time limit"
    recovery: "Reduce code size or complexity"

  CONTEXT_OVERFLOW:
    code: 413
    message: "Code too large for analysis"
    recovery: "Split into smaller modules"
```

## Integration

```yaml
requires:
  - code_parser
  - ast_analyzer

emits:
  - solid_analysis_completed
  - violation_detected

consumed_by:
  - 01-design-principles (bonded agent)
  - 04-refactoring (for smell detection)
```
