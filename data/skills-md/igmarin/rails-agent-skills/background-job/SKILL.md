---
name: background-job
type: persona
tags: [personas]
license: MIT
description: >
  Use when running the full background-job loop: design, TDD, retry, monitor.
  Trigger words: background job, async processing, Sidekiq, Solid Queue,
  Active Job, worker.
metadata:
  version: 1.0.0
  user-invocable: "true"
  entry_point: "Invoke when implementing background jobs with proper retry/discard strategies and monitoring"
  phases: "Phase 1: Job Design, Phase 2: TDD Implementation, Phase 3: Retry/Discard Configuration, Phase 4: Testing & Monitoring"
  hard_gates: "Job Design Complete, Tests Pass, Retry Strategy Configured, Failure Scenarios Tested"
  dependencies:
    - source: self
      skills: [implement-background-job, write-tests]
    - source: ruby-core-skills
      skills: [tdd-process]
  keywords: rails, background-job, async, sidekiq, solid-queue, active-job, retry, monitoring
---
# Background Job Persona

Orchestrates robust background job implementation with TDD discipline, proper retry/discard strategies, comprehensive failure scenario testing, and production monitoring to ensure reliable async processing.

---

## Phase 1: Job Design

**Objective:** Define job responsibilities, idempotency strategy, and error classification before writing code.

**Steps:**
1. **Job Purpose** — Define trigger conditions, input parameters, expected output/side effects, and criticality.
2. **Idempotency** — Design job to be safely re-runnable: use unique job keys, status checks, or sentinel timestamps.
3. **Error Classification** — Classify all anticipated errors:
   - Transient (network timeouts, rate limits) → retry
   - Permanent (invalid data, record not found) → discard
   - Configuration (missing credentials) → alert
4. **Queue & Timeout** — Assign queue priority and set execution timeout.

**HARD GATE — Job Design Complete:**
- [ ] Purpose, trigger, input/output defined
- [ ] Idempotency strategy specified
- [ ] All errors classified as transient/permanent
- [ ] Queue and timeout values chosen

**If gate fails:** Clarify requirements before implementation.

---

## Phase 2: TDD Implementation

**Objective:** Implement job logic under TDD discipline.

**Steps:**
1. Choose unit vs. integration test approach.
2. Write failing tests covering: successful execution, idempotency (run twice = same result), transient error raises, permanent error discards.
3. Confirm tests **FAIL** for the right reason (job not yet implemented).
4. Propose implementation approach and wait for explicit user approval.
5. Implement job using the structure shown in Phase 3 (retry/discard declarations included from the start); confirm tests **PASS**.
6. Run full test suite — confirm no regressions.

**HARD GATE — Tests Pass:**
- [ ] Tests exist and run
- [ ] Tests failed before implementation
- [ ] All tests pass after implementation
- [ ] Full suite green

**Example job test skeleton** (for `OrderConfirmationEmailJob` — see Phase 3 for the matching implementation):
```ruby
# spec/jobs/order_confirmation_email_job_spec.rb
RSpec.describe OrderConfirmationEmailJob do
  let(:order) { create(:order, :completed) }

  it 'sends confirmation email' do
    expect(EmailService).to receive(:send_confirmation).with(order.id, order.customer_email, order.total)
    described_class.perform_now(order.id, order.customer_email, order.total)
  end

  it 'is idempotent' do
    expect(EmailService).to receive(:send_confirmation).once
    2.times { described_class.perform_now(order.id, order.customer_email, order.total) }
  end

  it 'raises on transient errors so retry triggers' do
    allow(EmailService).to receive(:send_confirmation).and_raise(EmailService::TimeoutError)
    expect { described_class.perform_now(order.id, order.customer_email, order.total) }.to raise_error(EmailService::TimeoutError)
  end

  it 'logs and re-raises on transient error' do
    allow(EmailService).to receive(:send_confirmation).and_raise(EmailService::TimeoutError)
    expect(Rails.logger).to receive(:error).with(/transient error/)
    expect { described_class.perform_now(order.id, order.customer_email, order.total) }
      .to raise_error(EmailService::TimeoutError)
  end

  it 'discards silently on permanent error' do
    allow(EmailService).to receive(:send_confirmation).and_raise(EmailService::InvalidEmailError)
    expect { described_class.perform_now(order.id, "bad", order.total) }.not_to raise_error
  end
end
```

---

## Phase 3: Retry/Discard Configuration

**Objective:** Harden job for production with correct retry backoff, discard rules, timeouts, and monitoring hooks.

**Steps:**
1. Choose backend (Solid Queue for Rails 8+, Sidekiq for high scale) and configure worker concurrency.
2. Apply `retry_on` with exponential backoff and a capped attempt count (3–5) for every transient error class.
3. Apply `discard_on` for every permanent error class; log discards.
4. Set job execution timeout and queue timeout at the worker/config level.
5. Wire error tracking (e.g., Sentry) and metrics (e.g., StatsD/Datadog) in `ApplicationJob` callbacks.

**Complete job implementation** (matches the test skeleton in Phase 2):
```ruby
# app/jobs/order_confirmation_email_job.rb
class OrderConfirmationEmailJob < ApplicationJob
  queue_as :default

  retry_on  EmailService::TimeoutError,    wait: :exponentially_longer, attempts: 5
  retry_on  EmailService::RateLimitError,  wait: :exponentially_longer, attempts: 3
  discard_on ActiveRecord::RecordNotFound
  discard_on EmailService::InvalidEmailError

  def perform(order_id, customer_email, order_total)
    order = Order.find(order_id)
    return if order.email_sent_at.present?   # idempotency guard

    EmailService.send_confirmation(order_id, customer_email, order_total)
    order.update!(email_sent_at: Time.current)
  rescue EmailService::TimeoutError, EmailService::RateLimitError => e
    Rails.logger.error("[#{self.class}] transient error: #{e.message}")
    raise
  end
end
```

**Solid Queue (Rails 8+) snippet:**
```ruby
# config/initializers/solid_queue.rb
SolidQueue.configure { |c| c.worker = { processes: 2, threads: 5, polling_interval: 1 } }
```

**Sidekiq snippet:**
```ruby
# config/initializers/sidekiq.rb
Sidekiq.configure_server { |c| c.redis = { url: ENV['REDIS_URL'] } }
```

**Monitoring hook in ApplicationJob:**
```ruby
class ApplicationJob < ActiveJob::Base
  around_perform do |job, block|
    start = Time.current
    block.call
    StatsD.timing("jobs.#{job.class.name.underscore}.duration", Time.current - start)
    StatsD.increment("jobs.#{job.class.name.underscore}.success")
  rescue StandardError
    StatsD.increment("jobs.#{job.class.name.underscore}.failure")
    raise
  end
end
```

**HARD GATE — Retry Strategy Configured:**
- [ ] `retry_on` declared for every transient error with backoff and attempt cap
- [ ] `discard_on` declared for every permanent error with logging
- [ ] Timeouts configured at job and worker level
- [ ] Metrics/alerting wired

**If gate fails:** Job is not production-ready.

---

## Phase 4: Failure Scenario Testing & Monitoring

**Objective:** Verify retry/discard behaviour under injected failures at the integration/production level and confirm observability.

**Steps:**
1. Inject transient errors at the integration level → assert job raises and the queue backend schedules a retry (not just that the error propagates in a unit test).
2. Inject permanent errors → assert job does **not** raise, error is logged, and the job is not re-enqueued.
3. Confirm timeout handling by stubbing slow operations and verifying the worker-level timeout fires correctly.
4. Verify metrics increment on success and failure paths (assert StatsD/Datadog counters, not just that no exception is raised).
5. Confirm queue-depth alerts fire when queue backs up.

**HARD GATE — Failure Scenarios Tested:**
- [ ] Retry path tested end-to-end (job raises on transient error and backend re-enqueues)
- [ ] Discard path tested (no raise on permanent error, job not re-enqueued)
- [ ] Error logging assertions pass
- [ ] Metrics verified on success and failure
- [ ] Performance acceptable under expected load

**If gate fails:** Address failure scenarios before deploying.

---

## HARD GATE: Production Readiness

**Never deploy a background job without:**
- Idempotency guard implemented and tested
- All transient errors covered by `retry_on` with backoff
- All permanent errors covered by `discard_on` with logging
- Failure scenario tests passing
- Metrics and error-tracking wired
- Timeouts configured

## Error Recovery

**Job fails repeatedly in production:**
1. Check retry patterns and error rates in monitoring.
2. Review logs for error class and stack trace.
3. Classify error (transient vs. permanent) and adjust `retry_on`/`discard_on` if mis-classified.
4. Fix root cause; redeploy.

**Queue backs up:**
1. Scale worker processes/threads.
2. Promote critical jobs to a higher-priority queue.
3. Optimise job execution time or batch size.

## Output Style

When completing a background job implementation, output MUST include:

```markdown
# Background Job Report — [Job Name]

## Design
- Job class: <path>
- Purpose: <one-line description>
- Idempotency strategy: <database unique constraint / Redis lock / conditional check>
- Error classification: transient (<list>) / permanent (<list>)

## TDD
- Spec: <spec file path>
- RED: <failure message confirming job behavior missing>
- GREEN: <spec passes after implementation>

## Retry Configuration
- retry_on: <error classes, backoff strategy, attempt cap>
- discard_on: <error classes, logging>
- Timeouts: <job-level and worker-level>

## Failure Scenarios Tested
- Transient error → retries: ✓
- Permanent error → discards: ✓
- Idempotency → no duplicate side effects: ✓
- Timeout handling: ✓

## Monitoring
- Metrics: <StatsD/Datadog counters for success/failure/duration>
- Error tracking: <Sentry/Honeybadger integration>
- Queue depth alerts: <configured threshold>
```

---

## Integration

| Predecessor | This Persona | Successor |
|-------------|--------------|----------|
| load-context | background-job | code-review |
| tdd | background-job | quality |
| None (standalone) | background-job | PR submission |

**Use `implement-background-job` alone** if the job design is already decided and you only need to implement the job class and specs.
