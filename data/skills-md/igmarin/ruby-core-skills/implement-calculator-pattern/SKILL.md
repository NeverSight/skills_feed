---
name: implement-calculator-pattern
license: MIT
description: >
  Use when building variant-based calculators with SERVICE_MAP routing via
  `Factory.for(entity)` (ONLY permitted entry point — direct instantiation FORBIDDEN),
  BaseService defines `calculate`→`compute_result` if `should_calculate?`, NullService has
  `should_calculate?`=false+`compute_result`=nil, Concrete services override both methods
  and MUST call `super` in `should_calculate?` — and each component is tested in order
  (write spec → run → verify Red → implement → run → verify Green before next component,
  without collapsing NullService and concrete into one step). Test coverage includes: named
  variants, inactive plan, nil plan, and unknown variant contexts. Scaffolds tests per variant.
  Trigger words: strategy pattern, factory pattern, null object pattern, variant calculator,
  dispatch table, SERVICE_MAP, no-op fallback.
metadata:
  version: 1.0.0
  user-invocable: "true"
  origin: "Extracted from igmarin/rails-agent-skills v5.1.17"
---

# Implement Calculator Pattern

One API for the client: `Calculator::Factory.for(entity).calculate`. The factory picks the strategy; NullService handles unknown variants safely.

## Quick Reference

| Component | Responsibility |
|-----------|---------------|
| **Factory** | Dispatch to correct service class via SERVICE_MAP; fall back to NullService |
| **BaseService** | Guard with `should_calculate?`; delegate to `compute_result` |
| **NullService** | Always returns nil safely — never raises |
| **Concrete** | Override `should_calculate?` (add variant check on top of `super`) and `compute_result` |

## HARD-GATE

```text
Tests Gate Implementation

For each component (Factory → BaseService → NullService → Concrete):
1. Write the spec/test — contexts per variant, plus the NullService path
2. Run it — verify it fails because the component does not exist yet
3. Implement the component — minimum code to make the test pass
4. Run again — confirm green, then proceed to the next component
Each component gets its own RED command/output and GREEN command/output before
the next component starts. Do not collapse NullService and concrete services
into a single verification step.
```

**Output requirements per component:**
- Test coverage: Factory, NullService, and every concrete service must cover named variants, inactive plan, nil plan, and unknown variant contexts (or explicitly explain why a context does not apply).
- End with the calculator test directory command and the broader test suite command when available.
- Language — English unless explicitly requested otherwise.

## Core Process

1. Create the **Factory**. No qualifying context or unknown variant → `NullService`.
2. Create the **BaseService**. Define `calculate` that delegates to `compute_result` if `should_calculate?` is true.
3. Create the **NullService**. Always return false for `should_calculate?` and nil for `compute_result`.
4. Create **Concrete** services. Override `should_calculate?` and `compute_result`. Always call `super` in `should_calculate?`.
5. Run the full test suite.
6. Verify the **Single entry point rule:** `Factory.for(entity)` is the **only** permitted access path.

## File Structure

```
services/<calculator_name>/
├── factory.rb
├── base_service.rb
├── null_service.rb
├── standard_service.rb
├── premium_service.rb
```

## Minimal Inline Implementation

```ruby
# factory.rb
module PricingCalculator
  class Factory
    SERVICE_MAP = {
      "standard" => StandardService,
      "premium"  => PremiumService
    }.freeze

    def self.for(entity)
      SERVICE_MAP.fetch(entity.plan_variant, NullService).new(entity)
    end
  end
end
```

```ruby
# null_service.rb
module PricingCalculator
  class NullService < BaseService
    def should_calculate? = false
    def compute_result    = nil
  end
end
```

```ruby
# base_service.rb
module PricingCalculator
  class BaseService
    def initialize(entity)
      @entity = entity
    end

    def calculate
      return nil unless should_calculate?
      compute_result
    end

    private

    def should_calculate?
      @entity.present?
    end

    def compute_result
      raise NotImplementedError
    end
  end
end
```

## Minimal Usage Example

```ruby
# Single public entry point — never instantiate service classes directly
price = PricingCalculator::Factory.for(order).calculate
```

Full implementations for all components including multi-variant expansion are in [IMPLEMENTATION.md](IMPLEMENTATION.md). Full test examples are in [TESTING.md](TESTING.md).

**Pitfalls**
| Pitfall | Fix |
|---------|-----|
| SERVICE_MAP key mismatch | Keys must match exactly what is stored in the database — typos cause silent NullService fallbacks |
| Missing NullService spec/test | Always add a context for unknown/nil variants or fallback regressions go undetected |
| Direct service instantiation | Route through `Factory.for(entity)` — direct instantiation bypasses the NullService safety net |
| Forgetting `super` in concrete `should_calculate?` | Always call `super` — skipping it removes the base nil/presence guard |

## Further Reading

- [assets/examples.md](assets/examples.md) — Additional worked examples showing alternative domain contexts (e.g., discount calculators, shipping calculators) using the same pattern.
- [IMPLEMENTATION.md](IMPLEMENTATION.md) — Full Ruby implementations for every component (Factory, BaseService, NullService, Concrete Service), module naming conventions, and multi-variant expansion guidance.
- [TESTING.md](TESTING.md) — Full RSpec/Minitest examples covering all variant contexts (named variants, inactive plan, nil plan, unknown variant) for Factory, NullService, and concrete services.

## Integration

| Skill | When to chain |
|-------|---------------|
| **write-tests** | For writing spec files |
| **create-service-object** | For naming conventions, YARD docs, and `frozen_string_literal` baseline |
