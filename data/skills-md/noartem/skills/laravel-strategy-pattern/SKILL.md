---
name: laravel-strategy-pattern
description: Use the Strategy pattern to select behavior at runtime; bind multiple implementations to a shared interface
---

# Strategy Pattern

Create a common interface and multiple implementations. Choose a strategy by key or context.

```php
interface TaxCalculator { public function for(int $cents): int; }
final class NzTax implements TaxCalculator { /* ... */ }
final class AuTax implements TaxCalculator { /* ... */ }

final class TaxFactory {
  public function __construct(private array $drivers) {}
  public function forCountry(string $code): TaxCalculator { return $this->drivers[$code]; }
}
```

Register in a service provider and inject the factory where needed.
