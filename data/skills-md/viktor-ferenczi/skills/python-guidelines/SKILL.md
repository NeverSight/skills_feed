---
name: python-guidelines
description: Guiding principles for writing clear, concise, human readable and maintainable Python code.
license: MIT
---

Add type hints wherever you can. Think more like static typing, avoid changing the type of the same variable.
Define complex (nested) types separately if they are used in more than one place in the code.
Omit type hints when the type is obvious from the context (e.g., `x = 1`).

Write clean, human-readable code. Avoid spaghetti code; keep it structured.
Refactor the code as a separate step before making further changes whenever it would become too nested.
Too much nesting means more than 2 levels inside functions and methods.

Avoid adding too many parameters to functions and methods. In such cases introduce a data model class to store 
that information, especially if they are used together more than once. The same applies to return values.

Prefer using data model classes to dictionaries, Pydantic is good, but can also use a dataclass if you have to. 
For converting between naming schemes, always use explicit `from_something` and `to_something` methods instead of
hardcoding the external names of fields everywhere in the code. It typically happens while loading/saving data
from/to JSON with a different naming convention than the fields of the corresponding Pydantic model class.

Do not use catch-all exception handling (`except Exception`), except to cover retryable processing,
like request handlers or batch data processing. In all other cases use explicit exception handling 
wherever required. Disable catch-all error handling in development, especially if a debugger is connected. 
Never use exception handling for logic, except if there is no other alternative.

Do not combine multiple context managers into a single context manager just to save nesting on `with`
statements at the top level of the application. It is better to write them out explicitly, even if the
nesting level increases.

Do not use excessive nested iteration. While it needs less code, it also makes error handling and debugging
at a per-item level much harder when exceptions happen anywhere inside the generator functions.

Do not introduce abstractions prematurely. Do not add abstract base classes, unless there are multiple
subclasses or there will be multiple soon according to the current plans.

Do not write comments unless they are absolutely necessary to explain *why* the code is written the way it is.
Do not add a description of the method or function arguments if they are obvious from their names or types.
Prefer writing single-line docstrings that explain what the function or method does.

Define any duration in seconds (floating point), unless instructed otherwise.

Prefer test-driven development whenever it is practical.

Use only absolute imports, because relative imports will fail when you run a file directly, as Python loses 
the context of the project's package structure.

Follow these guidelines from the Zen of Python:
- Explicit is better than implicit. Simple is better than complex. Complex is better than complicated. 
- Flat is better than nested. Sparse is better than dense, readability counts.
- Special cases aren't special enough to break the rules, although practicality beats purity.
- Errors should never pass silently, unless explicitly silenced.
- If the implementation is hard to explain, it's a bad idea.
- In the face of ambiguity, refuse the temptation to guess.
