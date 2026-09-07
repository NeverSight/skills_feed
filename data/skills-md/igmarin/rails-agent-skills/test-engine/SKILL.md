---
name: test-engine
type: atomic
license: MIT
description: >
  Use when setting up or reviewing dummy-app and engine specs.
  Trigger words: test engine, dummy app, engine specs.
metadata:
  version: 1.0.0
  user-invocable: "true"
---

# Test Engine

## HARD-GATE

```text
EVERY engine MUST have a dummy app for testing.
If it doesn't exist, generate it:
cd my_engine && bundle exec rails plugin new . --dummy-path=spec/dummy --skip-git

Validate the dummy app boots before proceeding:
cd spec/dummy && bundle exec rails runner "puts 'Boot OK'"

If this fails, check the engine's `engine.rb` initializer order and ensure the engine is correctly mounted in `spec/dummy/config/routes.rb` before writing any specs.
```

## Core Process

1. Identify the engine type and public behaviors.
2. Add the smallest integration test that proves mounting and boot work. **Verify it passes before continuing** — if it fails, check `engine.rb` initializer order and mount configuration.
3. Add request, routing, configuration, and generator coverage as needed.
4. Add regression tests for coupling bugs before refactoring.
5. Run the full test suite (`bundle exec rspec`) to verify all specs pass.

**Minimal request spec to prove the engine mounts:**

```ruby
# spec/requests/my_engine/root_spec.rb
require 'rails_helper'

RSpec.describe 'MyEngine mount', type: :request do
  it 'returns ok for the engine root' do
    get my_engine.root_path
    expect(response).to have_http_status(:ok)
  end
end
```

**Configuration spec (engine respects host config):**

```ruby
# spec/my_engine/configuration_spec.rb
RSpec.describe MyEngine::Configuration do
  around do |example|
    original = MyEngine.config.widget_count
    MyEngine.config.widget_count = 3
    example.run
    MyEngine.config.widget_count = original
  end

  it 'uses configured value' do
    expect(MyEngine.config.widget_count).to eq(3)
  end
end
```

## Advanced Coverage Patterns

**Namespace-scoped routing spec:**

```ruby
# spec/routing/my_engine/widgets_routing_spec.rb
require 'rails_helper'

RSpec.describe MyEngine::WidgetsController, type: :routing do
  routes { MyEngine::Engine.routes }

  it 'routes GET /widgets to widgets#index' do
    expect(get: '/widgets').to route_to('my_engine/widgets#index')
  end
end
```

**Generator idempotency spec:**

```ruby
# spec/generators/my_engine/install_generator_spec.rb
require 'rails_helper'
require 'generators/my_engine/install/install_generator'

RSpec.describe MyEngine::Generators::InstallGenerator, type: :generator do
  destination File.expand_path('../tmp', __dir__)

  before { prepare_destination }

  it 'generates the initializer' do
    run_generator
    expect(file('config/initializers/my_engine.rb')).to exist
  end

  it 'is idempotent on re-run' do
    run_generator
    expect { run_generator }.not_to raise_error
    expect(file('config/initializers/my_engine.rb')).to exist
  end
end
```

## Output Style

When completing engine test setup, summarise results as:

```
Engine Test Report — [Engine Name]
- Dummy app: [location], boot ✓, migrations ✓
- Specs: mounting ✓, generators ✓, core (<n> examples, 0 failures)
- Suite: bundle exec rspec — <n> examples, 0 failures
```

## Integration

| Skill | When to chain |
|-------|---------------|
| create-engine | When structuring the engine for testability or adding configuration seams |
| review-engine | When validating test coverage adequacy or identifying gaps |
| write-tests | When improving spec structure, matchers, or shared examples |
