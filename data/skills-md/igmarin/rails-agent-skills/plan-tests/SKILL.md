---
name: plan-tests
type: atomic
license: MIT
description: >
  Use when choosing the first failing spec for a Rails change.
  One minimal example opens the gate. Trigger words: first failing test,
  what test first, TDD, spec selection.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Plan Tests

## Quick Reference

| Change type | First spec | Path | Why |
|-------------|-----------|------|-----|
| API contract, params, status code, JSON shape | Request spec | `spec/requests/` | Proves the real HTTP contract |
| Domain rule on a cohesive record or value object | Model spec | `spec/models/` | Fast feedback on domain behavior |
| Multi-step orchestration across collaborators | Service spec | `spec/services/` | Focuses on the workflow boundary |
| Enqueue/run/retry/discard behavior | Job spec | `spec/jobs/` | Captures async semantics directly |
| Critical Turbo/Stimulus or browser-visible flow | System spec | `spec/system/` | Use only when browser interaction is the real risk |
| Engine routing, generators, host integration | Engine spec | `spec/requests/` or engine path | Normal app specs miss engine wiring — see `test-engine` |
| Bug fix | Reproduction spec | Where the bug is observed | Proves the fix and prevents regression |

## HARD-GATE

```text
CHECKPOINT: Test Design Review

1. Present: Show the failing spec(s) written
2. Ask:
   - Does this test cover the right behavior?
   - Is the boundary correct (request vs service vs model)?
   - Are the most important edge cases represented?
   - Is the failure reason correct (feature missing, not setup error)?
3. Confirm: Only proceed to implementation once test design is approved.
```

## Core Process

Start at the highest-value boundary that proves the behavior with the least unnecessary setup.

### Steps

1. **Name the behavior:** State the user-visible outcome or invariant to prove.
2. **Locate the boundary:** Decide where the behavior is observed first — HTTP request, service entry point, model rule, job execution, engine integration, or external adapter. Use the Quick Reference table to map the change type to the right spec type.
3. **Write one failing example:** Keep it minimal; one example is enough to open the gate. List additional cases as follow-up coverage.
4. **Suggest the path:** Name the likely spec path using normal Rails conventions (e.g. `spec/requests/...`, `spec/services/...`, `spec/jobs/...`, `spec/models/...`).
5. **Run and validate:** Confirm the failure is because the behavior is missing, not because the setup is broken.
6. **Hand off:** Continue with the skill that fits the slice — [`write-tests`](skills/write-tests/SKILL.md) for general spec writing, [`test-service`](skills/test-service/SKILL.md) for service-layer coverage, or [`test-engine`](skills/test-engine/SKILL.md) for engine integration.

### Examples

#### Good: New JSON Endpoint

```ruby
# Behavior: POST /orders validates params and returns 201 with JSON payload
# First slice: request spec
# Suggested path: spec/requests/orders/create_spec.rb

RSpec.describe "POST /orders", type: :request do
  let(:user) { create(:user) }
  let(:valid_params) { { order: { product_id: create(:product).id, quantity: 1 } } }

  before { sign_in user }

  it "creates an order and returns 201" do
    post orders_path, params: valid_params, as: :json
    expect(response).to have_http_status(:created)
    expect(response.parsed_body["id"]).to be_present
  end
end
```

#### Good: New Orchestration Service

```ruby
# Behavior: Orders::CreateOrder validates inventory, persists, and enqueues follow-up work
# First slice: service spec
# Suggested path: spec/services/orders/create_order_spec.rb

RSpec.describe Orders::CreateOrder do
  subject(:result) { described_class.call(user: user, product: product, quantity: 1) }

  let(:user)    { create(:user) }
  let(:product) { create(:product, stock: 5) }

  it "returns a successful result with the new order" do
    expect(result).to be_success
    expect(result.order).to be_persisted
  end
end
```

### Pitfalls

| Pitfall | What to do |
|---------|------------|
| Starting with a PORO spec because it is easy | Easy ≠ high-signal — choose the boundary that proves the real behavior |
| Writing three spec types before running any | Pick one slice, run it, prove the failure, then proceed |
| Defaulting to one spec type for everything | Match the spec type to the layer where the real risk lives (HTTP, domain, async, browser) |
| Jumping to system specs too early | Reserve for critical browser flows that lower layers cannot prove |

## Extended Resources (Progressive Disclosure)

Load these files only when their specific content is needed:

- **[assets/first_slice_template.md](assets/first_slice_template.md)** — Use when documenting the test plan; provides a structured template for behavior, boundary decision, opening gate spec, and follow-up coverage

## Output Style

When completing test planning, produce a brief structured summary and populate the full plan using **[assets/first_slice_template.md](assets/first_slice_template.md)**. The summary must cover:

- **Behavior** — user-visible outcome being proved
- **First Slice** — spec type, file path, and boundary rationale
- **Opening Gate** — expected RED failure message and confirmation that failure reason is "feature missing, not setup error"
- **Follow-up Coverage** — bulleted list of additional cases deferred from the initial gate
- **Design Checkpoint** — confirmation that behavior, boundary, edge cases, and failure reason are all validated
