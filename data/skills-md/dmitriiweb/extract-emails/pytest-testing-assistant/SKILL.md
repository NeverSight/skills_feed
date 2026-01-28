---
name: pytest-testing-assistant
description: Write focused pytest tests as standalone functions (one test per function), avoiding test classes.
---

# Pytest Testing Assistant

## Quick start
- Write tests as plain functions; do not use test classes. Aim for one focused test per function/behavior.
- Use clear names: `test_<function>_<behavior>`; keep AAA (arrange/act/assert) obvious.
- Prefer one primary assertion per test; add minimal supporting checks when necessary.
- Use fixtures sparingly to keep tests readable; favor in-test setup when simple.
- Run with `pytest` or `pytest path/to/test_file.py` to scope runs.
- See `references/pytest_rules.md` for detailed guidelines and examples.

## Workflow
1) **Identify behavior**  
   - Target a single function/behavior per test. Name the test after the behavior being validated.  

2) **Write the test**  
   - Use a standalone function `def test_<thing>():` (no classes).  
   - Keep a clear arrange/act/assert structure; avoid hidden work in fixtures unless it improves clarity.  
   - Use parametrization for small input/output matrices instead of loops.  

3) **Assertions**  
   - Prefer one main assertion; add secondary checks only when they clarify the outcome.  
   - Include helpful assertion messages or use expressive matchers for readability.  

4) **Run and iterate**  
   - Run `pytest` (optionally narrow with paths or `-k` expressions).  
   - Refine names and setup for readability and isolation.  

## Reference
- `references/pytest_rules.md`: structure rules, naming patterns, and usage tips.
