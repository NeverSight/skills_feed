---
name: laravel-state-machines
description: State machines using Spatie Model States for complex state transitions. Use when working with complex state management, state transitions, or when user mentions state machines, Spatie Model States, state transitions, transition validation.
---

# Laravel State Machines

State machines with Spatie Model States for complex state transitions and validation.

## Core Concept

**[state-management.md](references/state-management.md)** - State machine patterns:
- Spatie Model States setup
- State classes with behavior
- Transition classes with validation
- State-specific methods
- When to use state machines vs simple enums
- Testing state transitions

## Pattern

```php
// State classes
final class DraftOrderState extends OrderState
{
    public function canBeSubmitted(): bool
    {
        return true;
    }
}

final class PendingOrderState extends OrderState
{
    public function canBeSubmitted(): bool
    {
        return false;
    }
}

// Transition class
final class SubmitOrderTransition extends Transition
{
    public function handle(): OrderState
    {
        // Validation and side effects

        return new PendingOrderState($this->order);
    }
}

// Usage
$order->status->transitionTo(PendingOrderState::class);
```

Use state machines for complex state with validation, side effects, or state-specific behavior. Use simple enums for basic status fields.
