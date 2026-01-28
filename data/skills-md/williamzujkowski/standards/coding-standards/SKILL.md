---
name: coding-standards
description: Comprehensive coding standards and best practices for maintainable, consistent software development across multiple languages and paradigms
---

# Coding Standards Skill

## Level 1: Quick Start (5 minutes)

### What You'll Learn

Apply essential coding standards for clean, maintainable code that follows industry best practices.

### Core Principles

- **Consistency**: Follow established style guides (PEP 8, Airbnb, Google)
- **Readability**: Write self-documenting code with clear naming
- **Maintainability**: Keep functions small (<50 lines), files focused (<500 lines)
- **Quality**: Enforce standards with linters and formatters

### Quick Reference

```python
# ✅ Good: Clear naming, single responsibility
def calculate_user_discount(user: User, order: Order) -> Decimal:
    """Calculate discount based on user tier and order total."""
    if user.tier == "premium":
        return order.total * Decimal("0.15")
    return order.total * Decimal("0.05")

# ❌ Bad: Unclear naming, mixed concerns
def calc(u, o):
    d = 0.15 if u.t == "p" else 0.05
    save_to_db(u, o, d)  # Side effect!
    return o.t * d
```

### Essential Checklist

- [ ] Follow language-specific style guide
- [ ] Use meaningful, descriptive names
- [ ] Limit function complexity (cyclomatic < 10)
- [ ] Configure linter and formatter
- [ ] Add pre-commit hooks

### Common Pitfalls

- Inconsistent naming conventions within a project
- Functions that do too many things
- Missing or outdated documentation
- Skipping code reviews

---

## Level 2: Implementation (30 minutes)

### Deep Dive Topics

#### 1. Code Style and Formatting

**Naming Conventions by Language:**

```typescript
// TypeScript/JavaScript
class UserService {}           // PascalCase for classes
const getUserById = () => {}   // camelCase for functions
const API_ENDPOINT = "..."     // UPPER_SNAKE_CASE for constants
```

```python
# Python
class UserService:              # PascalCase for classes
def get_user_by_id():          # snake_case for functions
API_ENDPOINT = "..."           # UPPER_SNAKE_CASE for constants
```

**File Organization:**

```
src/
├── models/           # Data models and types
├── services/         # Business logic (max 500 lines/file)
├── controllers/      # Request handlers
├── utils/           # Shared utilities
└── config/          # Configuration
```

#### 2. Documentation Standards

**Function Documentation:**

```typescript
/**
 * Calculates the final price after applying discounts and tax.
 *
 * @param basePrice - The original price before any adjustments
 * @param discountRate - Discount as a decimal (0.1 = 10%)
 * @param taxRate - Tax rate as a decimal (0.08 = 8%)
 * @returns The final price rounded to 2 decimal places
 * @throws {ValidationError} If basePrice is negative
 *
 * @example
 * const finalPrice = calculateFinalPrice(100, 0.1, 0.08);
 * // Returns 97.20 (100 - 10% discount + 8% tax)
 */
function calculateFinalPrice(
  basePrice: number,
  discountRate: number,
  taxRate: number
): number {
  if (basePrice < 0) {
    throw new ValidationError("Base price cannot be negative");
  }
  const discounted = basePrice * (1 - discountRate);
  return Math.round(discounted * (1 + taxRate) * 100) / 100;
}
```

#### 3. Architecture Patterns

**SOLID Principles Application:**

```typescript
// Single Responsibility Principle
class UserRepository {
  async findById(id: string): Promise<User> {}
  async save(user: User): Promise<void> {}
}

class UserValidator {
  validate(user: User): ValidationResult {}
}

// Dependency Injection
class UserService {
  constructor(
    private readonly repository: UserRepository,
    private readonly validator: UserValidator
  ) {}

  async createUser(userData: UserData): Promise<User> {
    const validation = this.validator.validate(userData);
    if (!validation.isValid) {
      throw new ValidationError(validation.errors);
    }
    return this.repository.save(new User(userData));
  }
}
```

#### 4. Error Handling

```typescript
// Custom error hierarchy
class ApplicationError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

class ValidationError extends ApplicationError {
  constructor(message: string, public fields: string[]) {
    super(message, "VALIDATION_ERROR", 400);
  }
}

// Usage with proper error handling
async function processPayment(payment: Payment): Promise<Result> {
  try {
    validatePaymentData(payment);
    const result = await paymentGateway.charge(payment);
    await auditLog.record("payment.success", { paymentId: result.id });
    return result;
  } catch (error) {
    if (error instanceof ValidationError) {
      logger.warn("Invalid payment data", { fields: error.fields });
      throw error;
    }
    logger.error("Payment processing failed", { error, payment });
    throw new ApplicationError(
      "Payment processing failed",
      "PAYMENT_ERROR",
      502
    );
  }
}
```

### Implementation Patterns

#### DRY (Don't Repeat Yourself)

```typescript
// ❌ Bad: Repeated logic
function calculateEmployeeSalary(employee: Employee): number {
  if (employee.type === "full-time") {
    return employee.baseSalary * 1.2 + 5000;
  }
  return employee.baseSalary * 1.2;
}

function calculateContractorPay(contractor: Contractor): number {
  return contractor.baseSalary * 1.2;
}

// ✅ Good: Extracted common logic
function applyStandardBonus(baseSalary: number): number {
  return baseSalary * 1.2;
}

function calculateEmployeeSalary(employee: Employee): number {
  const withBonus = applyStandardBonus(employee.baseSalary);
  return employee.type === "full-time" ? withBonus + 5000 : withBonus;
}
```

### Automation Tools

```json
// package.json - Automation setup
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "format": "prettier --write \"**/*.{ts,tsx,json,md}\"",
    "type-check": "tsc --noEmit",
    "validate": "npm run lint && npm run type-check && npm run test"
  },
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

### Integration Points

- Links to [Security Standards](../security-practices/SKILL.md) for secure coding
- Links to [Testing Standards](../testing/SKILL.md) for testable code design
- Links to [NIST Compliance](../nist-compliance/SKILL.md) for SI-10, SI-11 controls

---

## Level 3: Mastery (Extended Learning)

### Advanced Topics

#### 1. Performance Optimization Patterns

**Memoization:**

```typescript
function memoize<T extends (...args: any[]) => any>(fn: T): T {
  const cache = new Map<string, ReturnType<T>>();
  return ((...args: Parameters<T>) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  }) as T;
}

// Usage
const expensiveCalculation = memoize((n: number) => {
  // Complex computation
  return Array.from({ length: n }, (_, i) => i * i).reduce((a, b) => a + b);
});
```

#### 2. Concurrency Patterns

```typescript
// Parallel execution with error handling
async function processItemsConcurrently<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number = 5
): Promise<Array<R | Error>> {
  const results: Array<R | Error> = [];
  const executing: Promise<void>[] = [];

  for (const item of items) {
    const promise = processor(item)
      .then((result) => {
        results.push(result);
      })
      .catch((error) => {
        results.push(error);
      });

    executing.push(promise);

    if (executing.length >= concurrency) {
      await Promise.race(executing);
      executing.splice(
        executing.findIndex((p) => p === promise),
        1
      );
    }
  }

  await Promise.all(executing);
  return results;
}
```

#### 3. API Design Best Practices

```typescript
// RESTful API design
interface ApiResponse<T> {
  data: T;
  meta: {
    timestamp: string;
    requestId: string;
  };
  errors?: ApiError[];
}

// Versioning strategy
app.use("/api/v1", v1Routes);
app.use("/api/v2", v2Routes);

// Pagination standard
interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

#### 4. Refactoring Strategies

**Extract Method:**

```typescript
// Before
function generateReport(data: Data[]): Report {
  // 100+ lines of complex logic
  const filtered = data.filter(/* complex condition */);
  const transformed = filtered.map(/* complex transformation */);
  const aggregated = transformed.reduce(/* complex aggregation */);
  // More complex logic...
}

// After
function generateReport(data: Data[]): Report {
  const filtered = filterRelevantData(data);
  const transformed = transformDataForReport(filtered);
  const aggregated = aggregateMetrics(transformed);
  return formatReport(aggregated);
}
```

### Resources

#### Essential Reading

- [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Refactoring by Martin Fowler](https://refactoring.com/)
- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns)

#### Tools and Frameworks

- **Linters**: ESLint, Pylint, RuboCop, Checkstyle
- **Formatters**: Prettier, Black, gofmt
- **Static Analysis**: SonarQube, CodeClimate, DeepSource
- **Documentation**: JSDoc, Sphinx, Doxygen

#### Language-Specific Style Guides

- [Python PEP 8](https://peps.python.org/pep-0008/)
- [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Effective Go](https://go.dev/doc/effective_go)

### Templates

#### Code Review Checklist

```markdown
## Code Review Checklist

### Functionality
- [ ] Code meets requirements
- [ ] Edge cases handled
- [ ] Error handling comprehensive

### Code Quality
- [ ] Follows style guide
- [ ] Names are clear and descriptive
- [ ] Functions are focused (<50 lines)
- [ ] No code duplication

### Testing
- [ ] Unit tests included
- [ ] Tests cover edge cases
- [ ] Tests are maintainable

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
```

### Scripts

#### Complexity Checker

```python
#!/usr/bin/env python3
"""Check cyclomatic complexity of Python files."""
import sys
from radon.complexity import cc_visit

def check_complexity(filename: str, max_complexity: int = 10) -> bool:
    """Check if file exceeds complexity threshold."""
    with open(filename) as f:
        code = f.read()

    results = cc_visit(code)
    violations = [r for r in results if r.complexity > max_complexity]

    if violations:
        print(f"❌ {filename}: Complexity violations found")
        for v in violations:
            print(f"  - {v.name}: complexity {v.complexity} (max {max_complexity})")
        return False

    print(f"✅ {filename}: All functions within complexity limit")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_complexity.py <file>")
        sys.exit(1)

    passed = check_complexity(sys.argv[1])
    sys.exit(0 if passed else 1)
```

## Examples

### Basic Usage

```python
// TODO: Add basic example for coding-standards
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for coding-standards
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how coding-standards
// works with other systems and services
```

See `examples/coding-standards/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring coding-standards functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for coding-standards
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Bundled Resources

- [Full CODING_STANDARDS.md](../../docs/standards/CODING_STANDARDS.md)
- [UNIFIED_STANDARDS.md](../../docs/standards/UNIFIED_STANDARDS.md)
- Example linter configs in `./resources/`
- Pre-commit hook templates in `./templates/`
- Complexity checking scripts in `./scripts/`
