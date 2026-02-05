---
name: laravel-transactions-and-consistency
description: Wrap multi-write operations in transactions; use dispatchAfterCommit and idempotency patterns to ensure consistency
---

# Transactions and Consistency

Ensure multi-step changes are atomic; make retries safe.

## Commands

```
DB::transaction(function () use ($order, $payload) {
    $order->update([...]);
    $order->items()->createMany($payload['items']);
    OrderUpdated::dispatch($order);        // or flag for after-commit
});

// Listener queued after commit
class SendInvoice implements ShouldQueue {
    public $afterCommit = true;
}
```

## Patterns

- Use `DB::transaction` to wrap write sequences and related side-effects
- Prefer `$afterCommit` or `dispatchAfterCommit()` for events / jobs
- Make jobs idempotent (check existing state, use unique constraints)
- Use `lockForUpdate()` for row-level coordination when needed
- Validate invariants at the boundary before starting the transaction
