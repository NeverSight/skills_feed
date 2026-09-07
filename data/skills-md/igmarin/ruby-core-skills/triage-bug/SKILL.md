---
name: triage-bug
license: MIT
description: >
  Use when investigating a bug, error, or regression in a Ruby or Rails codebase.
  Creates a failing reproduction test, isolates the broken code path, and
  produces a minimal fix plan. Trigger words: debug, broken, error, regression,
  stack trace, failing test, bug report, Ruby bug, Rails error, .rb file broken.
metadata:
  version: 1.0.0
  user-invocable: "true"
  origin: "Extracted from igmarin/rails-agent-skills v5.1.17"
---
# Triage Bug

## Quick Reference

| Bug shape | Likely first spec/test |
|-----------|-------------------|
| HTTP/API symptoms (status, JSON, redirect) | Integration/Request spec or controller test |
| Data/logic symptoms (wrong value, validation) | Unit or service test |
| Timing/Async symptoms (missing job, email) | Background worker or unit test |
| Integration/dependency regression | Component/integration test |

## HARD-GATE

```text
DO NOT guess at fixes without a reproduction path.
1. Reproduce the bug.
2. Choose the right failing test boundary.
3. Plan the smallest safe repair.
```

## Core Process

Work through each step in order. The final triage output must include all seven named outputs below.

1. **Capture the report** → **Observed behavior** and **Expected behavior**: restate actual behavior, expected behavior, and reproduction steps.
2. **Bound the scope** → **Likely boundary**: identify whether the issue is in request handling, domain logic, background workers, integration boundaries, or an external dependency.
3. **Gather current evidence**: logs, error messages, edge-case inputs, recent changes, or missing guards.
4. **Choose the first failing test** → **First failing test to add** and **Exact command to run before the fix**: pick the boundary where the bug is visible to users or operators.
5. **Define the smallest fix path** → **Smallest safe fix path**: name the likely files and the narrowest behavior change needed to make the test pass.
6. **Produce a skeleton test** → **Skeleton test**: provide a failing test/spec to run before implementing the fix (see canonical example below).
7. **Hand off** → **Follow-up skills**: continue through `test-planning-process` → `tdd-process` → implementation skill.

*Language: Must be in English unless explicitly requested otherwise.*

### Canonical Request-Boundary Example

When the report is an order creation failure visible through `POST /orders`, default to the request boundary first:

- **First failing test:** `spec/requests/orders_spec.rb` (or `test/integration/orders_test.rb`)
- **Command:** `bundle exec rspec spec/requests/orders_spec.rb` (or `bundle exec ruby test/integration/orders_test.rb`)
- **Expected RED:** response is not `422` with `"Out of stock"` yet, or the service raises instead of returning a handled error.
- **Smallest fix path:** `Orders::CreateOrder` handles the stock guard and returns `{ success: false, error: "Out of stock" }` without creating the order.
- **Skeleton test:**
  ```ruby
  # spec/requests/orders_spec.rb
  RSpec.describe "POST /orders" do
    context "when product is out of stock" do
      let(:product) { Product.new(stock: 0) }

      it "returns 422 with an error message" do
        post "/orders", params: { product_id: product.id, quantity: 1 }
        expect(response.status).to eq(422)
        expect(response.body).to include("Out of stock")
      end
    end
  end
  ```
  *For a Minitest equivalent, see [assets/examples.md](assets/examples.md). Do not replace this example with a pricing, model-only, or class-only scenario unless the bug report points there.*

### Boundary Guide

See [BOUNDARY_GUIDE.md](./BOUNDARY_GUIDE.md) for the full bug-shape → test-type mapping and layer diagnosis tips.

### Pitfalls

| Pitfall | What to do |
|---------|------------|
| Unit test when the bug is visible at request level | Start where the failure is actually observed |
| Bundling reproduction, refactor, and new features | Fix the bug in the smallest safe slice only |
| Flaky evidence treated as green light to patch | Stabilize reproduction before touching code |
| The explanation relies on "probably" or "maybe" | Ambiguity means the reproduction step isn't done yet |

## Extended Resources

- [BOUNDARY_GUIDE.md](./BOUNDARY_GUIDE.md)
- [assets/examples.md](assets/examples.md)

## Integration

| Skill | When to chain |
|-------|---------------|
| **test-planning-process** | To choose the strongest first failing test for the bug |
| **tdd-process** | To run the TDD loop correctly after the test is chosen |
| **refactor-process** | When the bug sits inside a risky refactor area and behavior must be preserved first |
| **review-process** | To review the final bug fix for regressions and missing coverage |
