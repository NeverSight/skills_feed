---
name: laravel:template-method-and-plugins
description: Stabilize workflows with Template Method or Strategy; extend by adding new classes instead of editing core logic
---

# Template Method and Pluggable Strategies

Keep core flows stable; enable extension via small classes.

## Template Method

Use a base class that defines the algorithm skeleton; subclasses override hooks.

```php
abstract class Importer {
    final public function handle(string $path): void {
        $rows = $this->load($path);
        $data = $this->normalize($rows);
        $this->validate($data);
        $this->save($data);
    }
    abstract protected function load(string $path): array;
    protected function normalize(array $rows): array { return $rows; }
    protected function validate(array $data): void {}
    abstract protected function save(array $data): void;
}
```

## Strategy/Plugin

Define an interface; register implementations; select by key/config.

```php
interface PaymentGateway { public function charge(int $cents, string $currency): string; }

final class StripeGateway implements PaymentGateway { /* ... */ }
final class BraintreeGateway implements PaymentGateway { /* ... */ }

final class PaymentsRegistry {
    /** @param array<string,PaymentGateway> $drivers */
    public function __construct(private array $drivers) {}
    public function for(string $key): PaymentGateway { return $this->drivers[$key]; }
}
```

Prefer adding a class over editing switch statements. Test implementations in isolation.

