---
name: laravel-jobs
description: Background jobs and event listeners for async processing. Use when working with queued jobs, background processing, events, or when user mentions jobs, queues, listeners, events, async processing.
---

# Laravel Jobs

Background jobs and event listeners: thin delegation layers to actions.

## Core Concept

**[jobs-listeners.md](references/jobs-listeners.md)** - Job patterns:
- Jobs as thin delegation layers
- Queue configuration
- Retry logic and timeouts
- Unique jobs
- Job middleware
- Event listeners
- When to use jobs vs sync actions

## Pattern

```php
final class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, Queueable;

    public function __construct(
        public readonly int $orderId,
    ) {}

    public function handle(ProcessOrderAction $action): void
    {
        $order = Order::findOrFail($this->orderId);

        $action($order);
    }

    public function middleware(): array
    {
        return [new WithoutOverlapping($this->orderId)];
    }
}

// Listener
final class SendOrderConfirmationListener
{
    public function handle(OrderPlaced $event): void
    {
        SendOrderConfirmationJob::dispatch($event->order->id);
    }
}
```

Jobs delegate to actions. Keep domain logic in actions, not jobs.
