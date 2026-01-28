---
name: laravel-providers
description: Service providers, bootstrapping, and application configuration. Use when working with service providers, app configuration, bootstrapping, or when user mentions service providers, AppServiceProvider, bootstrap, booters, configuration, helpers.
---

# Laravel Providers

Service providers and application bootstrapping patterns.

## Core Concepts

**[service-providers.md](references/service-providers.md)** - Service providers:
- AppServiceProvider organization with named methods
- Model::unguard() for mass assignment
- Factory resolver for Data classes
- Morph map registration
- Configuration patterns

**[bootstrap-booters.md](references/bootstrap-booters.md)** - Bootstrap & Booters:
- Invokable booter classes
- Middleware registration
- Exception handling setup
- Scheduling configuration
- Clean bootstrap organization

**[environment.md](references/environment.md)** - Environment config:
- Template and instance pattern
- `.env-local` templates
- Git-ignored instances
- Optional git-crypt for secrets

**[helpers.md](references/helpers.md)** - Helper functions:
- Global helper registration
- Autoloading helpers
- When to use (sparingly)
- Alternatives with static methods

## Pattern

```php
// AppServiceProvider
final class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        $this->configureMorphMap();
        $this->configureDataFactories();
        Model::unguard();
    }

    private function configureMorphMap(): void
    {
        Relation::morphMap([
            'order' => Order::class,
            'product' => Product::class,
        ]);
    }
}
```

Organize AppServiceProvider with named private methods for clarity.
