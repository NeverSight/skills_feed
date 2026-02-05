---
name: clean-code
description: Analyze and improve code quality, readability, and maintainability
sasmp_version: "1.3.0"
bonded_agent: 03-clean-code
bond_type: PRIMARY_BOND
version: "2.0.0"
updated: "2025-12-30"
---

# Clean Code Skill

> Atomic skill for code quality analysis and improvement

## Skill Definition

```yaml
skill_id: clean-code
responsibility: Single - Code quality analysis and recommendations
atomic: true
idempotent: true
```

## Parameter Schema

```typescript
interface SkillParams {
  // Required
  code: string;
  language: string;

  // Optional
  focus?: ('naming' | 'functions' | 'comments' | 'formatting')[];
  style_guide?: string;           // airbnb, google, pep8, etc.
  strictness?: 'relaxed' | 'normal' | 'strict';
}

interface SkillResult {
  quality_score: number;          // 0-100
  issues: CleanCodeIssue[];
  metrics: CodeMetrics;
  suggestions: Improvement[];
}

interface CleanCodeIssue {
  category: string;
  severity: 'low' | 'medium' | 'high';
  location: string;
  current: string;
  suggested: string;
  rule: string;
}

interface CodeMetrics {
  lines_of_code: number;
  avg_function_length: number;
  max_function_length: number;
  avg_params_per_function: number;
  cyclomatic_complexity: number;
  naming_score: number;
  comment_ratio: number;
}
```

## Validation Rules

```yaml
input_validation:
  code:
    min_length: 1
    max_length: 100000
    required: true

  language:
    required: true
    allowed: [typescript, javascript, python, java, csharp, go, ruby, kotlin, rust, php]

  focus:
    default: [naming, functions, comments, formatting]

  strictness:
    default: normal
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff:
    type: exponential
    initial_delay_ms: 500
    max_delay_ms: 5000
    multiplier: 2

  retryable_errors:
    - TIMEOUT
    - RATE_LIMIT

  non_retryable_errors:
    - INVALID_SYNTAX
    - UNSUPPORTED_LANGUAGE
```

## Logging & Observability

```yaml
logging:
  level: INFO
  events:
    - analysis_started
    - issue_detected
    - metrics_calculated
    - analysis_completed

metrics:
  - name: quality_score
    type: gauge
  - name: issues_by_category
    type: counter
  - name: analysis_duration_ms
    type: histogram

tracing:
  span_name: clean_code_analysis
  attributes:
    - language
    - code_size
    - strictness
```

## Clean Code Rules

### Naming Rules

```yaml
naming_rules:
  variables:
    - rule: descriptive_names
      bad: [x, temp, data, val, item]
      good: [userCount, totalPrice, customerEmail]

    - rule: pronounceable
      bad: [genymdhms, modymdhms]
      good: [generationTimestamp, modificationDate]

  functions:
    - rule: verb_noun
      bad: [data, process, handle]
      good: [fetchUser, calculateTotal, validateEmail]

  classes:
    - rule: noun_singular
      bad: [Manager, Processor, Data]
      good: [User, Order, PaymentGateway]

  booleans:
    - rule: question_prefix
      bad: [flag, status, open]
      good: [isActive, hasPermission, canEdit]
```

### Function Rules

```yaml
function_rules:
  length:
    ideal: 10
    warning: 20
    error: 50

  parameters:
    ideal: 2
    warning: 3
    error: 5

  nesting:
    ideal: 1
    warning: 2
    error: 4
```

## Usage Examples

### Basic Analysis
```typescript
// Input
{
  code: `
    function p(d) {
      let x = 0;
      for (let i = 0; i < d.length; i++) {
        x += d[i].val;
      }
      return x;
    }
  `,
  language: "typescript"
}

// Output
{
  quality_score: 35,
  issues: [
    {
      category: "naming",
      severity: "high",
      location: "line 1",
      current: "p",
      suggested: "calculateTotalValue",
      rule: "descriptive_names"
    }
  ],
  metrics: {
    lines_of_code: 7,
    avg_function_length: 7,
    naming_score: 20
  }
}
```

## Unit Test Template

```typescript
describe('CleanCodeSkill', () => {
  describe('analyze', () => {
    it('should detect poor variable naming', async () => {
      const code = 'const x = 5; const d = getData();';
      const result = await skill.analyze({ code, language: 'typescript' });

      expect(result.issues).toContainEqual(
        expect.objectContaining({ category: 'naming', current: 'x' })
      );
    });

    it('should calculate accurate quality score', async () => {
      const cleanCode = `
        function calculateOrderTotal(items: Item[]): number {
          return items.reduce((sum, item) => sum + item.price, 0);
        }
      `;
      const result = await skill.analyze({ code: cleanCode, language: 'typescript' });
      expect(result.quality_score).toBeGreaterThan(80);
    });
  });
});
```

## Error Handling

```yaml
errors:
  INVALID_SYNTAX:
    code: 400
    message: "Code contains syntax errors"
    recovery: "Fix syntax errors before analysis"

  UNSUPPORTED_LANGUAGE:
    code: 400
    message: "Language not supported"
    recovery: "Use supported language"
```

## Integration

```yaml
requires:
  - syntax_parser
  - metrics_calculator

emits:
  - code_analyzed
  - issues_detected
  - quality_score_calculated

consumed_by:
  - 03-clean-code (bonded agent)
  - 04-refactoring (for improvement suggestions)
```
