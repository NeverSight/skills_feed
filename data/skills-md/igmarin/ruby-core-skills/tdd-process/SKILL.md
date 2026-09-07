---
name: tdd-process
license: MIT
description: >
  Enforces Red-Green-Refactor with hard gates: Red phase writes failing test that MUST
  fail on assertion (not syntax/config) and presents test+failure before proceeding,
  runs tests on the specific file (not full suite) after each phase, Green phase writes
  minimal code to pass and stops there, Refactor phase runs test after each micro-change
  and MUST stay Green throughout. Generates failing test cases, validates test failure
  before proceeding, gates implementation behind passing red-phase checks.
  Use when the user requests TDD workflow, asks to write tests first, mentions
  Red-Green-Refactor methodology, or uses trigger words: TDD, test-first, test gate.
metadata:
  version: 1.0.0
  user-invocable: "true"
  type: "process-discipline"
---
# TDD Process

## Process Steps

### Step 1: Red Phase
- Write a failing test for the target behavior
- Run the test suite on that specific file
- **Gate:** Failure must be on the assertion — not a syntax or configuration error
- **Checkpoint:** Present the test code and failure output before proceeding to implementation

### Step 2: Green Phase
- Write the minimal code required to pass the test — nothing more
- Run the test file
- **Checkpoint:** Present the minimal implementation once tests pass

### Step 3: Refactor Phase
- Clean up duplication, naming, class structures, and documentation
- Run the test suite after each micro-change
- **Gate:** Tests must remain green throughout

---

## Framework Example

### RSpec
**Failing Test (RED):**
```ruby
# spec/user_spec.rb
RSpec.describe User do
  describe "#full_name" do
    it "combines first name and last name" do
      user = User.new(first_name: "Ada", last_name: "Lovelace")
      expect(user.full_name).to eq("Ada Lovelace")
    end
  end
end
```
*Failure command & output:*
```bash
$ bundle exec rspec spec/user_spec.rb
...
1 example, 1 failure
Failed examples:
rspec ./spec/user_spec.rb:4 # User#full_name combines first name and last name (NoMethodError: undefined method `full_name')
```

**Minimal Implementation (GREEN):**
```ruby
# lib/user.rb
class User
  def initialize(first_name:, last_name:)
    @first_name, @last_name = first_name, last_name
  end

  def full_name
    "#{@first_name} #{@last_name}"
  end
end
```

> Additional framework examples are available in companion files:
> - `EXAMPLES_PYTEST.md` — pytest (Python)
> - `EXAMPLES_JEST.md` — Jest (JavaScript/TypeScript)
> - `EXAMPLES_GO_TEST.md` — Go testing package

---

## Integration

| Context | Next Skill |
|---------|-----------|
| Testing first slices | **test-planning-process** |
| Refactoring green code | **refactor-process** |
| Documenting public APIs | **write-yard-docs** |
