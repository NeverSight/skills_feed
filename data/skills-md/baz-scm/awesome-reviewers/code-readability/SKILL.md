---
name: code-readability
description: Writing clean, understandable, and self-documenting code that is easy to review and maintain over time.
version: '1.0'
---
# Code Readability & Maintainability

Writing **clean code** is a superpower for long-term productivity. Developers should prioritize clarity and explicitness over clever brevity. Code that clearly communicates its intent is easier for teammates (and future you) to understand and modify. High readability also reduces the chance of bugs – clear, well-structured code is more maintainable and less prone to surprise behaviors.

## Examples
- Using meaningful variable and function names (`isServerConnected` instead of `enabled`) to convey intent.
- Replacing a cryptic one-liner with a few well-named intermediate variables that make the logic obvious.

## Guidelines
- **Descriptive Naming:** Choose specific, descriptive names for variables, functions, and classes. Names should communicate intent and avoid ambiguity. For example, prefer `getUserProfile()` over `getData()` to make the code self-explanatory.
- **Clarity Over Cleverness:** Opt for explicit and straightforward code constructs rather than implicit or overly clever ones. For instance, use clear type conversions and named constants instead of magic numbers or implicit casts. This improves readability and avoids confusion.
- **Maintainability:** Keep code structure simple and organized. Write code in a way that reduces cognitive load on the reader – e.g. clear logic flow and consistent style. Clean, readable code is easier to debug and prevents subtle bugs that can arise from unclear operations.
