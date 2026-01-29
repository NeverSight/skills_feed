---
name: recurse-ml
description: >
  Python ML coding patterns for identifying and avoiding common pitfalls.
  Trigger: When writing ML code with Python best practices.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with recurse ml"

## When to Use

Use this skill when:
- Writing Python ML/data science code
- Identifying common Python anti-patterns
- Improving code reliability and readability
- Avoiding subtle bugs in ML pipelines

---

## Decision Tree

```
Need exception handling?   → Use specific exceptions (bare-exceptions.md)
Need conditionals?         → Check conditionals.md for patterns
Need boolean checks?       → See bool.md for comparisons
Need type safety?          → Apply typing.md guidelines
Need debugging?            → Use rml-verify.md
```

---

## Critical Patterns

### Don't Catch Bare Exceptions (REQUIRED)

```python
# ❌ BAD - Hides unintended exceptions
try:
    risky_operation()
except:
    handle_error()

# ❌ EQUALLY BAD
try:
    risky_operation()
except Exception:
    handle_error()

# ✅ GOOD - Catch specific exceptions
try:
    risky_operation()
except SpecificException:
    handle_error()

# ✅ OK if reraising
try:
    risky_operation()
except SpecificException as e:
    handle_error(e)
    raise  # Reraise the exception
```

**Why:** Bare exceptions hide bugs and give false stability.

---

## Resources

Specialized ML coding patterns in this skill:
- **Bare Exceptions**: [bare-exceptions.md](bare-exceptions.md)
- **Boolean Comparisons**: [bool.md](bool.md)
- **Comments**: [comments.md](comments.md)
- **Conditionals**: [conditionals.md](conditionals.md)
- **Control Flow**: [flow.md](flow.md)
- **Infinite Loops**: [infinite-loops.md](infinite-loops.md)
- **Mutable Defaults**: [mutable-defaults.md](mutable-defaults.md)
- **RML Verification**: [rml-verify.md](rml-verify.md)
- **Side Effects**: [side-effects.md](side-effects.md)
- **Type Hints**: [typing.md](typing.md)
- **Unreachable Code**: [unreachable-code.md](unreachable-code.md)
