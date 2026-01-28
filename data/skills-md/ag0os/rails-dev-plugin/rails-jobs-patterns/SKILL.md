---
name: rails-jobs-patterns
description: ActiveJob and background processing patterns for Rails. Automatically invoked when working with background jobs, Sidekiq, async processing, job queues, scheduling, or the app/jobs directory. Triggers on "job", "background job", "ActiveJob", "Sidekiq", "async", "queue", "perform_later", "worker", "scheduled job", "cron", "retry", "idempotent".
allowed-tools: Read, Grep, Glob
---

# Rails Background Job Patterns

Patterns for building reliable, efficient background jobs in Rails applications.

## When This Skill Applies

- Creating background jobs with ActiveJob
- Configuring Sidekiq queues and workers
- Implementing idempotent job patterns
- Error handling and retry strategies
- Batch processing large datasets
- Scheduling recurring jobs

## Core Principles

### Idempotency
Jobs should be safe to run multiple times:
```ruby
def perform(order_id)
  order = Order.find(order_id)
  return if order.processed?  # Guard against re-processing

  order.with_lock do
    return if order.processed?
    process_order(order)
    order.update!(status: 'processed')
  end
end
```

### Small, Focused Jobs
- Single responsibility per job
- Pass IDs, not objects (serialization)
- Keep payloads minimal

### Error Handling
- Use `retry_on` for transient failures
- Use `discard_on` for permanent failures
- Log errors with context

## Quick Reference

| Pattern | Use When |
|---------|----------|
| `retry_on` | Transient errors (network, timeout) |
| `discard_on` | Permanent failures (record deleted) |
| `with_lock` | Preventing concurrent execution |
| Batch processing | Large datasets |
| Result tracking | Job status reporting |

## Detailed Documentation

- [patterns.md](patterns.md) - Complete job patterns with examples

## Basic Job Structure

```ruby
class ProcessOrderJob < ApplicationJob
  queue_as :default

  retry_on ActiveRecord::RecordNotFound, wait: 5.seconds, attempts: 3
  discard_on ActiveJob::DeserializationError

  def perform(order_id)
    order = Order.find(order_id)
    OrderProcessor.new(order).process!
  end
end
```

## Queue Configuration

```yaml
# config/sidekiq.yml
:queues:
  - [critical, 6]
  - [default, 3]
  - [low, 1]
```

## Testing Jobs

```ruby
RSpec.describe ProcessOrderJob, type: :job do
  include ActiveJob::TestHelper

  it 'processes the order' do
    order = create(:order)

    expect {
      ProcessOrderJob.perform_now(order.id)
    }.to change { order.reload.status }.from('pending').to('processed')
  end

  it 'enqueues in the correct queue' do
    expect {
      ProcessOrderJob.perform_later(1)
    }.to have_enqueued_job.on_queue('default')
  end
end
```
