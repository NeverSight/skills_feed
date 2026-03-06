---
name: legacy
description: Modernize legacy codebases, migrate frameworks, and reduce technical debt. Use for legacy system updates or framework migrations.
---

# Legacy Modernization

Safely upgrade and modernize legacy systems.

## When to Use

- Framework migrations
- Language version upgrades
- Monolith decomposition
- Technical debt reduction
- Dependency updates

## Migration Strategies

### Strangler Fig Pattern

```
┌─────────────────────────────────────┐
│           Load Balancer             │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
┌──────▼──────┐ ┌──────▼──────┐
│   Legacy    │ │    New      │
│   System    │ │   Service   │
└─────────────┘ └─────────────┘

1. Route new features to new service
2. Gradually migrate existing features
3. Eventually retire legacy system
```

### Branch by Abstraction

```python
# 1. Create abstraction layer
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

# 2. Wrap legacy implementation
class LegacyPaymentProcessor(PaymentProcessor):
    def __init__(self, legacy_system):
        self.legacy = legacy_system

    def process(self, amount: float) -> bool:
        return self.legacy.old_process_method(amount)

# 3. Create new implementation
class ModernPaymentProcessor(PaymentProcessor):
    def process(self, amount: float) -> bool:
        # New implementation
        pass

# 4. Use feature flag to switch
processor = (ModernPaymentProcessor() if feature_flag("new_payment")
             else LegacyPaymentProcessor(legacy))
```

## Migration Checklist

### Before Starting

- [ ] Document current behavior
- [ ] Add tests for existing functionality
- [ ] Set up monitoring and alerts
- [ ] Create rollback plan
- [ ] Communicate with stakeholders

### During Migration

- [ ] Make incremental changes
- [ ] Test after each change
- [ ] Monitor error rates
- [ ] Keep legacy running in parallel
- [ ] Document breaking changes

### After Migration

- [ ] Remove feature flags
- [ ] Clean up legacy code
- [ ] Update documentation
- [ ] Archive old codebase
- [ ] Post-mortem lessons learned

## Common Migrations

### jQuery to React

```javascript
// Phase 1: Embed React in jQuery app
const root = document.getElementById("new-component");
ReactDOM.render(<NewComponent />, root);

// Phase 2: Shared state
window.appState = { user: null };
// Both jQuery and React read from appState

// Phase 3: Gradual replacement
// Replace one component at a time
```

### Python 2 to 3

```python
# Use __future__ imports for compatibility
from __future__ import print_function, division, absolute_import

# Use six for cross-version compatibility
import six
if six.PY2:
    text_type = unicode
else:
    text_type = str

# Run 2to3 tool
# python -m lib2to3 --write --nobackups src/
```

## Compatibility Layers

```python
# Adapter for API changes
class CompatibilityAdapter:
    def __init__(self, new_service):
        self.new = new_service

    # Old API signature
    def get_user(self, user_id):
        # Translate to new API
        return self.new.fetch_user(id=user_id)

    # Deprecation warning
    def old_method(self):
        warnings.warn(
            "old_method is deprecated, use new_method instead",
            DeprecationWarning
        )
        return self.new.new_method()
```

## Examples

**Input:** "Migrate from Express to Fastify"
**Action:** Create adapter layer, migrate routes incrementally, test each step

**Input:** "Reduce technical debt in this module"
**Action:** Add tests first, refactor incrementally, maintain compatibility
