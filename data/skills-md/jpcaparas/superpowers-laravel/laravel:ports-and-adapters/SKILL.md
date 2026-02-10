---
name: laravel:ports-and-adapters
description: Use hexagonal architecture for external systems; define ports (interfaces) and per-provider adapters; select adapter at composition edge
---

# Ports and Adapters (Hexagonal)

Abstract integrations behind stable interfaces. Keep vendor SDKs out of your domain code.

## Shape

- Port: PHP interface that expresses only what the app needs
- Adapters: one per provider, wrapping SDK quirks
- Selection: choose adapter via config/env/service provider

## Example (email)

```php
// Port
interface MailPort {
    public function send(string $to, string $subject, string $html): void;
}

// Adapter
final class SesMailAdapter implements MailPort {
    public function __construct(private \Aws\Ses\SesClient $ses) {}
    public function send(string $to, string $subject, string $html): void {
        // wrap SES specifics here
    }
}

// Composition (AppServiceProvider)
$this->app->singleton(MailPort::class, function () {
    return match (config('mail.driver')) {
        'ses' => new SesMailAdapter(app('aws.ses')),
        default => new SmtpMailAdapter(/* ... */),
    };
});
```

## Tips

- Normalize SDK data into your own types/DTOs
- Expose only portable capabilities via the port
- Keep adapters thin and well-tested

