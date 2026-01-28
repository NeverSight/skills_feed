---
name: python-type-hints-guide
description: Comprehensive reference guide for Python type hints, static type checking with mypy, modern type annotation patterns (PEP 484, 585, 604, 612, 613), and type hint best practices for Python 3.9+. Use during code reviews to ensure proper type annotation usage, evaluate mypy configuration, and identify type hint anti-patterns.
allowed-tools: Read, Grep, Glob
---

# Python Type Hints Guide

## Purpose

This skill provides comprehensive guidance on Python type hints and static type checking for Python 3.9+ codebases. It serves as a reference during code reviews to ensure proper type annotation usage, evaluate type hint quality, and promote best practices for gradual typing adoption.

This skill should be referenced by the uncle-duke-python agent when:
- Reviewing Python code for type hint usage
- Evaluating type annotation quality and consistency
- Identifying type hint anti-patterns
- Recommending mypy configuration improvements
- Guiding gradual typing adoption strategies

## Context

Type hints (introduced in PEP 484) enable static type checking in Python while maintaining the language's dynamic nature. Modern Python (3.9+) has significantly improved type hint syntax with built-in generic types and the union operator. Proper type hints improve:

- **Code documentation**: Self-documenting function signatures
- **IDE support**: Better autocomplete and refactoring
- **Bug detection**: Catch type errors before runtime
- **Maintainability**: Easier to understand code contracts
- **Refactoring safety**: Catch breaking changes early

This guide focuses on modern Python (3.9+) patterns and assumes familiarity with basic Python syntax.

## Prerequisites

- Python 3.9 or later (for built-in generic types)
- Python 3.10+ recommended (for union operator |)
- mypy installed for static type checking: `pip install mypy`
- Understanding of Python's dynamic typing system

## Type Hints Basics (PEP 484)

### Basic Types

Use built-in type names directly for simple types:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(x: int, y: int) -> int:
    return x + y

def calculate_average(scores: list[float]) -> float:
    return sum(scores) / len(scores)

def is_valid(flag: bool) -> bool:
    return not flag
```

### None Type

Use `None` for functions that don't return a value:

```python
def log_message(message: str) -> None:
    print(f"[LOG] {message}")
    # No return statement or explicit return None
```

### Optional Types

Use `Optional[T]` or `T | None` (Python 3.10+) for values that can be None:

```python
from typing import Optional

# Python 3.9 style
def find_user(user_id: int) -> Optional[dict]:
    # May return dict or None
    return None

# Python 3.10+ style (preferred)
def find_user_modern(user_id: int) -> dict | None:
    # May return dict or None
    return None

# With default None parameter
def greet(name: str, title: str | None = None) -> str:
    if title:
        return f"Hello, {title} {name}!"
    return f"Hello, {name}!"
```

### Collection Types (Python 3.9+)

Python 3.9+ allows using built-in collection types directly (lowercase):

```python
# Modern Python 3.9+ (preferred)
def process_names(names: list[str]) -> dict[str, int]:
    return {name: len(name) for name in names}

def unique_items(items: set[int]) -> list[int]:
    return sorted(items)

def get_coordinates() -> tuple[float, float]:
    return (42.0, -71.0)

# Variable-length tuple (homogeneous)
def process_values(values: tuple[int, ...]) -> int:
    return sum(values)

# Nested collections
def process_matrix(matrix: list[list[float]]) -> float:
    return sum(sum(row) for row in matrix)
```

**Legacy Python 3.8 and below** (avoid in modern code):

```python
from typing import List, Dict, Set, Tuple

def process_names(names: List[str]) -> Dict[str, int]:
    return {name: len(name) for name in names}
```

### Union Types

Use `Union[T, U]` or `T | U` (Python 3.10+) for multiple possible types:

```python
from typing import Union

# Python 3.9 style
def process_id(user_id: Union[int, str]) -> str:
    return str(user_id)

# Python 3.10+ style (preferred)
def process_id_modern(user_id: int | str) -> str:
    return str(user_id)

# Multiple types
def parse_value(value: int | float | str | None) -> float:
    if value is None:
        return 0.0
    return float(value)
```

### Any Type

Use `Any` when type cannot be determined or for gradual typing:

```python
from typing import Any

# Accept any type (escape hatch)
def legacy_function(data: Any) -> Any:
    # Used when migrating untyped code
    return data

# Dict with any values
def process_config(config: dict[str, Any]) -> None:
    # Config can have values of any type
    pass
```

**Warning**: Overusing `Any` defeats the purpose of type hints. Use sparingly and document why.

## Advanced Types

### Generic Types (TypeVar, Generic)

Create reusable generic functions and classes:

```python
from typing import TypeVar, Generic

# Type variable for generic functions
T = TypeVar('T')

def first_item(items: list[T]) -> T | None:
    return items[0] if items else None

# Usage preserves type information
names: list[str] = ["Alice", "Bob"]
first_name: str | None = first_item(names)  # Type checker knows this is str | None

numbers: list[int] = [1, 2, 3]
first_number: int | None = first_item(numbers)  # Type checker knows this is int | None

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T | None:
        return self._items.pop() if self._items else None

# Usage
string_stack: Stack[str] = Stack()
string_stack.push("hello")  # OK
string_stack.push(42)  # Type error!

# Bounded type variable (constrains to subclasses)
from numbers import Number
NumT = TypeVar('NumT', bound=Number)

def add_numbers(x: NumT, y: NumT) -> NumT:
    return x + y  # type: ignore[return-value]
```

### Protocol Classes (Structural Subtyping - PEP 544)

Define interfaces based on structure (duck typing with type checking):

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

# Both Circle and Square satisfy Drawable protocol
# without explicit inheritance
def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # OK
render(Square())  # OK

# Protocol with properties
class Sized(Protocol):
    @property
    def size(self) -> int:
        ...

# Real-world example: file-like objects
class SupportsRead(Protocol):
    def read(self, size: int = -1) -> str:
        ...

def process_file(file: SupportsRead) -> str:
    return file.read()
```

### Literal Types (PEP 586)

Specify exact literal values allowed:

```python
from typing import Literal

def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> None:
    print(f"Log level set to {level}")

set_log_level("DEBUG")  # OK
set_log_level("TRACE")  # Type error!

# Multiple literals
def open_file(path: str, mode: Literal["r", "w", "a", "rb", "wb"]) -> None:
    pass

# Literal booleans (rarely needed)
def process(flag: Literal[True]) -> None:
    # Only accepts True, not False
    pass

# Combining with Union
Mode = Literal["read", "write", "append"]
def process_mode(mode: Mode | None = None) -> None:
    pass
```

### TypedDict (PEP 589)

Define dictionaries with specific key-value type requirements:

```python
from typing import TypedDict, NotRequired

# Basic TypedDict
class User(TypedDict):
    name: str
    age: int
    email: str

def create_user(user: User) -> None:
    print(f"Creating user: {user['name']}")

# Usage
user: User = {"name": "Alice", "age": 30, "email": "alice@example.com"}
create_user(user)  # OK

# Missing required key
bad_user: User = {"name": "Bob", "age": 25}  # Type error! Missing 'email'

# Optional keys (Python 3.11+)
class UserOptional(TypedDict):
    name: str
    age: int
    email: NotRequired[str]  # Optional key

# For Python 3.9-3.10, use total=False
class PartialUser(TypedDict, total=False):
    email: str
    phone: str

class RequiredUser(PartialUser):
    name: str  # Required
    age: int   # Required

# Inheritance
class Employee(User):
    employee_id: int
    department: str
```

### Final Types (PEP 591)

Indicate values that should not be reassigned or overridden:

```python
from typing import Final, final

# Final variable (constant)
MAX_CONNECTIONS: Final[int] = 100

# Type error if reassigned
MAX_CONNECTIONS = 200  # Type error!

# Final class attribute
class Config:
    API_URL: Final[str] = "https://api.example.com"

# Final method (cannot be overridden)
class Base:
    @final
    def process(self) -> None:
        print("Processing")

class Derived(Base):
    def process(self) -> None:  # Type error! Cannot override @final method
        print("Custom processing")

# Final class (cannot be subclassed)
@final
class ImmutablePoint:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Point3D(ImmutablePoint):  # Type error! Cannot subclass @final class
    pass
```

### NewType

Create distinct types for type safety:

```python
from typing import NewType

# Create new types for domain concepts
UserId = NewType('UserId', int)
OrderId = NewType('OrderId', int)

def get_user(user_id: UserId) -> dict:
    return {"id": user_id, "name": "User"}

def get_order(order_id: OrderId) -> dict:
    return {"id": order_id, "status": "pending"}

# Usage
user_id = UserId(42)
order_id = OrderId(100)

get_user(user_id)  # OK
get_user(order_id)  # Type error! OrderId is not UserId
get_user(42)  # Type error! int is not UserId

# NewType is zero-cost at runtime (just returns the value)
# But provides type safety during static checking
```

### Callable Types

Type hint for callable objects (functions, lambdas, callables):

```python
from typing import Callable

# Basic callable: (param_types...) -> return_type
def apply_operation(x: int, operation: Callable[[int], int]) -> int:
    return operation(x)

# Usage
def double(n: int) -> int:
    return n * 2

result = apply_operation(5, double)  # OK
result = apply_operation(5, lambda x: x * 3)  # OK

# Multiple parameters
def apply_binary(
    x: int,
    y: int,
    operation: Callable[[int, int], int]
) -> int:
    return operation(x, y)

apply_binary(5, 3, lambda a, b: a + b)  # OK

# No parameters
def run_callback(callback: Callable[[], None]) -> None:
    callback()

# Variable arguments (use ... for flexibility)
def log_with_formatter(
    message: str,
    formatter: Callable[..., str]
) -> None:
    formatted = formatter(message)
    print(formatted)

# Callback type alias
Validator = Callable[[str], bool]

def validate_input(value: str, validator: Validator) -> bool:
    return validator(value)
```

### Type Aliases

Create readable aliases for complex types:

```python
from typing import TypeAlias

# Simple alias
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]

def scale_vector(vector: Vector, factor: float) -> Vector:
    return [x * factor for x in vector]

# Complex nested types
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None

def parse_json(data: str) -> JSON:
    import json
    return json.loads(data)

# Union aliases
Numeric: TypeAlias = int | float
OptionalString: TypeAlias = str | None

# Callable alias
HandlerFunction: TypeAlias = Callable[[str, dict], None]

# Generic alias
from typing import TypeVar
T = TypeVar('T')
Result: TypeAlias = tuple[T, str | None]  # (value, error)

def safe_parse(value: str) -> Result[int]:
    try:
        return (int(value), None)
    except ValueError as e:
        return (0, str(e))
```

## Function Annotations

### Parameter Type Hints

```python
# Basic parameters
def greet(name: str, age: int) -> str:
    return f"{name} is {age} years old"

# Default values with type hints
def greet_with_title(
    name: str,
    title: str = "Mr.",
    excited: bool = False
) -> str:
    greeting = f"{title} {name}"
    return greeting + "!" if excited else greeting

# Multiple types (union)
def process_id(user_id: int | str) -> str:
    return str(user_id)
```

### *args and **kwargs Type Hints

```python
# *args: variable positional arguments
def sum_numbers(*args: int) -> int:
    return sum(args)

sum_numbers(1, 2, 3, 4)  # OK
sum_numbers(1, 2, "3")  # Type error!

# **kwargs: variable keyword arguments
def configure(**kwargs: str) -> dict[str, str]:
    return kwargs

configure(host="localhost", port="8000")  # OK
configure(host="localhost", port=8000)  # Type error! port must be str

# Mixed args, kwargs
def complex_function(
    required: str,
    *args: int,
    **kwargs: bool
) -> None:
    pass

complex_function("test", 1, 2, 3, flag=True, debug=False)  # OK

# Different types for args/kwargs
from typing import Any

def flexible_function(
    *args: int | str,
    **kwargs: Any
) -> None:
    pass
```

### Overload Decorator

Use `@overload` to provide multiple type signatures:

```python
from typing import overload

# Overload signatures (not implemented)
@overload
def process(data: str) -> str: ...

@overload
def process(data: int) -> int: ...

@overload
def process(data: list[str]) -> list[str]: ...

# Actual implementation (must be compatible with all overloads)
def process(data: str | int | list[str]) -> str | int | list[str]:
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, int):
        return data * 2
    else:
        return [s.upper() for s in data]

# Type checker knows return type based on input
result1: str = process("hello")  # OK, knows it returns str
result2: int = process(42)  # OK, knows it returns int
result3: list[str] = process(["a", "b"])  # OK, knows it returns list[str]

# More complex overload example
@overload
def get_value(container: dict[str, int], key: str) -> int: ...

@overload
def get_value(container: list[int], key: int) -> int: ...

def get_value(
    container: dict[str, int] | list[int],
    key: str | int
) -> int:
    return container[key]  # type: ignore[index]
```

## Class Type Hints

### Instance Variables

```python
class User:
    # Instance variable annotations (PEP 526)
    name: str
    age: int
    email: str | None

    def __init__(self, name: str, age: int, email: str | None = None) -> None:
        self.name = name
        self.age = age
        self.email = email

# Alternative: annotate in __init__
class Product:
    def __init__(self, name: str, price: float) -> None:
        self.name: str = name
        self.price: float = price
        self.stock: int = 0  # Type inferred from default value
```

### Class Variables (ClassVar)

```python
from typing import ClassVar

class Config:
    # Class variable (shared across all instances)
    api_url: ClassVar[str] = "https://api.example.com"
    max_retries: ClassVar[int] = 3

    # Instance variable
    session_id: str

    def __init__(self, session_id: str) -> None:
        self.session_id = session_id

# Class variables are accessed on the class
print(Config.api_url)  # OK

# Type checker distinguishes class vs instance variables
config = Config("abc123")
config.session_id  # OK (instance variable)
config.api_url  # OK but mypy may warn (accessing class var from instance)
```

### Property Type Hints

```python
class Circle:
    def __init__(self, radius: float) -> None:
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self) -> float:
        """Read-only property"""
        import math
        return math.pi * self._radius ** 2

# Cached property
from functools import cached_property

class DataProcessor:
    def __init__(self, data: list[int]) -> None:
        self._data = data

    @cached_property
    def processed_data(self) -> list[int]:
        """Expensive computation, cached after first access"""
        return [x * 2 for x in self._data]
```

### __init__ Annotations

```python
class DatabaseConnection:
    def __init__(
        self,
        host: str,
        port: int = 5432,
        username: str | None = None,
        password: str | None = None,
        *,  # Force keyword-only arguments after this
        timeout: float = 30.0,
        ssl: bool = True
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.ssl = ssl

# Usage
db = DatabaseConnection(
    "localhost",
    5432,
    timeout=60.0,  # Keyword-only
    ssl=False
)
```

## mypy Configuration

### Basic mypy Setup

Create `mypy.ini` or `pyproject.toml` for mypy configuration:

**mypy.ini:**
```ini
[mypy]
# Type checking strictness
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_unimported = False
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
check_untyped_defs = True
strict_equality = True

# Import discovery
namespace_packages = True
ignore_missing_imports = False

# Per-module options
[mypy-tests.*]
disallow_untyped_defs = False

[mypy-third_party_lib.*]
ignore_missing_imports = True
```

**pyproject.toml:**
```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
check_untyped_defs = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "third_party_lib.*"
ignore_missing_imports = true
```

### Common mypy Flags

**Strict mode (all checks enabled):**
```bash
mypy --strict myfile.py
```

**Common individual flags:**
```bash
# Require type hints on all functions
mypy --disallow-untyped-defs myfile.py

# Warn about functions that return Any
mypy --warn-return-any myfile.py

# Disallow Any types
mypy --disallow-any-expr myfile.py  # Very strict!

# Show error codes
mypy --show-error-codes myfile.py

# Incremental mode (faster)
mypy --incremental myfile.py

# Specific Python version
mypy --python-version 3.9 myfile.py
```

**Useful combinations:**
```bash
# Recommended starting point
mypy --check-untyped-defs --warn-redundant-casts myfile.py

# Strict for new code
mypy --strict --allow-untyped-calls myfile.py

# CI/CD friendly (no incremental cache)
mypy --no-incremental --show-error-codes mypackage/
```

### Ignoring Errors Appropriately

Use type ignore comments sparingly and document why:

```python
# Ignore specific error on one line
result = legacy_function()  # type: ignore[no-untyped-call]

# Ignore all errors on one line (avoid!)
bad_code = something()  # type: ignore

# Ignore multiple specific errors
value = complex_operation()  # type: ignore[arg-type, return-value]

# Ignore for entire function (last resort)
def legacy_code() -> Any:  # type: ignore[no-untyped-def]
    pass

# Better: Fix the issue or use proper typing
def proper_code() -> dict[str, Any]:
    """Returns config dict with various value types."""
    return {"key": "value"}
```

**When to use type: ignore:**
- Interfacing with untyped third-party libraries
- Complex type narrowing that mypy can't infer
- Known false positives (file a mypy issue!)
- Temporary during gradual typing migration

**When NOT to use type: ignore:**
- To avoid adding type hints
- Because "mypy is wrong" (usually mypy is right!)
- Without documenting the reason
- Instead of fixing the actual type error

### Type: ignore Comments Best Practices

```python
# BAD: No error code
result = func()  # type: ignore

# GOOD: Specific error code with explanation
# mypy can't infer the narrowed type after this check
result = func()  # type: ignore[arg-type]  # Known false positive, see issue #123

# GOOD: Document workaround
# TODO: Remove once library adds type stubs
data = legacy_lib.get_data()  # type: ignore[no-untyped-call]

# BEST: Fix the issue instead
def properly_typed_function(x: int) -> str:
    return str(x)
```

## Best Practices

### 1. Gradual Typing Strategy

Start with critical code paths, expand gradually:

```python
# Phase 1: Public API functions
def public_api(user_id: int) -> dict[str, Any]:
    return _internal_function(user_id)

def _internal_function(user_id):  # Not typed yet
    return {"id": user_id}

# Phase 2: Expand to internal functions
def _internal_function_typed(user_id: int) -> dict[str, int]:
    return {"id": user_id}

# Phase 3: Strict typing everywhere
def fully_typed(user_id: int) -> User:
    return User(id=user_id, name="Unknown")
```

**Recommended adoption order:**
1. Public API functions and methods
2. Core business logic
3. Internal utilities
4. Tests (can be less strict)
5. Scripts and one-off code (optional)

### 2. When to Use Type Hints

**Always type hint:**
- Public APIs and library functions
- Function signatures (parameters and return types)
- Class attributes and properties
- Complex data structures

**Consider type hints:**
- Internal/private functions in large codebases
- Helper functions with non-obvious signatures
- Callback functions

**Optional type hints:**
- Very simple, obvious functions
- Scripts and notebooks
- Prototype code
- One-liners and lambdas

```python
# Always type hint: Public API
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    return price * (1 - discount_percent / 100)

# Optional: Very obvious helper
def _double(x):
    return x * 2

# Consider: Less obvious helper (recommended)
def _format_currency(amount: float, currency: str = "USD") -> str:
    return f"{amount:.2f} {currency}"
```

### 3. Type Hint Readability

Prioritize readability over exhaustive typing:

```python
# BAD: Overly complex, hard to read
def process(
    data: dict[str, list[tuple[int, str, dict[str, list[int | str | None]]]]]
) -> list[tuple[str, int]]:
    pass

# GOOD: Use type aliases for readability
PersonData = dict[str, list[int | str | None]]
Record = tuple[int, str, PersonData]
DataDict = dict[str, list[Record]]
Result = list[tuple[str, int]]

def process_readable(data: DataDict) -> Result:
    pass

# BETTER: Use TypedDict for structured dicts
class PersonData(TypedDict):
    age: int
    name: str
    tags: list[str]

class Record(TypedDict):
    id: int
    type: str
    data: PersonData

def process_structured(data: dict[str, list[Record]]) -> Result:
    pass
```

### 4. Avoiding Over-Specification

Don't type hint more than necessary:

```python
# BAD: Over-specified (too rigid)
def process_items(items: list[str]) -> list[str]:
    return [item.upper() for item in items]

# GOOD: Accept any iterable, return list (more flexible)
from collections.abc import Iterable

def process_items_flexible(items: Iterable[str]) -> list[str]:
    return [item.upper() for item in items]

# Now works with lists, tuples, sets, generators, etc.
process_items_flexible(["a", "b"])  # OK
process_items_flexible(("a", "b"))  # OK
process_items_flexible(x for x in ["a", "b"])  # OK

# BAD: Forces specific dict implementation
def merge(d1: dict[str, int], d2: dict[str, int]) -> dict[str, int]:
    return {**d1, **d2}

# GOOD: Accept any mapping
from collections.abc import Mapping

def merge_flexible(
    d1: Mapping[str, int],
    d2: Mapping[str, int]
) -> dict[str, int]:
    return {**d1, **d2}
```

**Use abstract types from `collections.abc`:**
- `Iterable[T]` instead of `list[T]` for inputs
- `Sequence[T]` when you need indexing/length
- `Mapping[K, V]` instead of `dict[K, V]` for inputs
- `MutableMapping[K, V]` when you need to modify
- Return concrete types like `list`, `dict`

### 5. Using Protocol for Duck Typing

Prefer Protocol over rigid inheritance:

```python
from typing import Protocol

# BAD: Forces inheritance
class Animal:
    def make_sound(self) -> str:
        raise NotImplementedError

class Dog(Animal):  # Must inherit
    def make_sound(self) -> str:
        return "Woof"

# GOOD: Duck typing with type safety
class CanMakeSound(Protocol):
    def make_sound(self) -> str: ...

class Dog:  # No inheritance needed
    def make_sound(self) -> str:
        return "Woof"

class Car:
    def make_sound(self) -> str:
        return "Vroom"

def hear_sound(thing: CanMakeSound) -> None:
    print(thing.make_sound())

hear_sound(Dog())  # OK
hear_sound(Car())  # OK (anything with make_sound method)

# Real-world example: file-like objects
class SupportsRead(Protocol):
    def read(self, n: int = -1) -> str: ...

def process_text_file(file: SupportsRead) -> int:
    content = file.read()
    return len(content)

# Works with any object that has a read() method
import io
process_text_file(io.StringIO("test"))  # OK
with open("file.txt") as f:
    process_text_file(f)  # OK
```

### 6. Type Narrowing

Help mypy understand type narrowing through conditionals:

```python
def process_value(value: int | str | None) -> str:
    # mypy tracks type narrowing through conditionals

    if value is None:
        return "No value"
        # After this check, value is int | str in else branch

    if isinstance(value, int):
        return f"Number: {value}"
        # After this check, value is str in else branch

    # mypy knows value must be str here
    return f"Text: {value.upper()}"

# Use isinstance for type narrowing
def double_if_number(value: int | str) -> int | str:
    if isinstance(value, int):
        # mypy knows value is int here
        return value * 2
    # mypy knows value is str here
    return value

# Use type guards for custom narrowing
from typing import TypeGuard

def is_list_of_strings(val: list[Any]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process_list(items: list[Any]) -> None:
    if is_list_of_strings(items):
        # mypy knows items is list[str] here
        for item in items:
            print(item.upper())  # OK, item is str
```

## Common Patterns

### Forward References (String Annotations)

Use string annotations for forward references:

```python
# Forward reference (class not yet defined)
class Node:
    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next

# Python 3.10+: Can use | with quotes
class TreeNode:
    def __init__(
        self,
        value: int,
        left: "TreeNode | None" = None,
        right: "TreeNode | None" = None
    ) -> None:
        self.value = value
        self.left = left
        self.right = right

# Python 3.7+: Use from __future__ import annotations
from __future__ import annotations

class ModernNode:
    def __init__(self, value: int, next: ModernNode | None = None) -> None:
        self.value = value
        self.next = next
    # No quotes needed with __future__ import!
```

### Circular Type Dependencies

Handle circular dependencies with TYPE_CHECKING:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Imports only used for type checking (not at runtime)
    from mypackage.models import User

class Post:
    def __init__(self, author: "User") -> None:
        self.author = author

# In models.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypackage.posts import Post

class User:
    def __init__(self, posts: list["Post"]) -> None:
        self.posts = posts
```

### Generic Container Types

Type hint containers properly:

```python
# Homogeneous lists
def process_names(names: list[str]) -> None:
    for name in names:
        print(name.upper())  # mypy knows name is str

# Mixed types (use Union)
def process_mixed(items: list[int | str]) -> None:
    for item in items:
        if isinstance(item, int):
            print(item * 2)
        else:
            print(item.upper())

# Nested containers
def process_matrix(matrix: list[list[float]]) -> float:
    return sum(sum(row) for row in matrix)

# Dict with specific key/value types
def process_scores(scores: dict[str, float]) -> float:
    return sum(scores.values())

# Complex nested structure
ComplexData = dict[str, list[dict[str, int | str]]]

def process_complex(data: ComplexData) -> None:
    pass
```

### Callback Type Hints

Type hint callbacks and handlers:

```python
from typing import Callable

# Simple callback
def run_with_callback(callback: Callable[[int], None]) -> None:
    callback(42)

run_with_callback(lambda x: print(x))  # OK

# Event handler
EventHandler = Callable[[str, dict[str, Any]], None]

def register_handler(event: str, handler: EventHandler) -> None:
    pass

def on_user_created(event_name: str, data: dict[str, Any]) -> None:
    print(f"Event: {event_name}, Data: {data}")

register_handler("user.created", on_user_created)

# Factory function
Factory = Callable[[], T]

def create_default(factory: Factory[T]) -> T:
    return factory()

create_default(lambda: [])  # Returns list
create_default(lambda: {})  # Returns dict

# Validator function
Validator = Callable[[str], bool]

def validate_email(email: str) -> bool:
    return "@" in email

def process_with_validation(value: str, validator: Validator) -> bool:
    return validator(value)

process_with_validation("test@example.com", validate_email)
```

### Context Manager Type Hints

Type hint context managers properly:

```python
from typing import Iterator, Generator
from contextlib import contextmanager

# Simple context manager class
class DatabaseConnection:
    def __enter__(self) -> "DatabaseConnection":
        print("Opening connection")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        print("Closing connection")

# Generator-based context manager
@contextmanager
def open_file(path: str) -> Iterator[list[str]]:
    file = open(path)
    try:
        yield file.readlines()
    finally:
        file.close()

# Generic context manager
from typing import Generic
T = TypeVar('T')

@contextmanager
def managed_resource(resource: T) -> Iterator[T]:
    try:
        yield resource
    finally:
        print(f"Cleaning up {resource}")

# Async context manager
class AsyncDatabaseConnection:
    async def __aenter__(self) -> "AsyncDatabaseConnection":
        print("Opening async connection")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        print("Closing async connection")
```

## Anti-Patterns

### Using Any Everywhere

```python
# BAD: Defeats purpose of type hints
def process(data: Any) -> Any:
    return data

def calculate(x: Any, y: Any) -> Any:
    return x + y

# GOOD: Use specific types
def process_user(data: dict[str, str]) -> User:
    return User(**data)

def calculate_sum(x: int, y: int) -> int:
    return x + y

# ACCEPTABLE: Gradual typing transition
def legacy_function(data: Any) -> dict[str, Any]:
    # TODO: Add proper types once interface is stable
    return {"result": data}
```

### Over-Complicated Type Hints

```python
# BAD: Unreadable, overly complex
def transform(
    data: dict[str, list[tuple[int, str, dict[str, list[int | str | None]]]]]
) -> list[tuple[str, dict[str, list[int]]]]:
    pass

# GOOD: Use type aliases
InputRecord = tuple[int, str, dict[str, list[int | str | None]]]
InputData = dict[str, list[InputRecord]]
OutputRecord = tuple[str, dict[str, list[int]]]
OutputData = list[OutputRecord]

def transform_readable(data: InputData) -> OutputData:
    pass

# BETTER: Use TypedDict or dataclasses
from dataclasses import dataclass

@dataclass
class Record:
    id: int
    name: str
    metadata: dict[str, list[int | str | None]]

@dataclass
class TransformedRecord:
    name: str
    values: dict[str, list[int]]

def transform_structured(
    data: dict[str, list[Record]]
) -> list[TransformedRecord]:
    pass
```

### Ignoring Type Errors Without Justification

```python
# BAD: Silencing errors without understanding
result = risky_operation()  # type: ignore

# BAD: Generic ignore
value = complex_call()  # type: ignore

# GOOD: Specific error with explanation
# mypy doesn't understand this runtime type check
result = risky_operation()  # type: ignore[arg-type]  # See issue #456

# GOOD: Document temporary workaround
# TODO: Remove after upgrading to library v2.0 with type stubs
value = legacy_lib.call()  # type: ignore[no-untyped-call]

# BEST: Fix the underlying issue
def properly_typed_operation() -> int:
    return 42

result = properly_typed_operation()  # No ignore needed!
```

### Not Running mypy in CI/CD

```python
# BAD: Only running mypy locally
# Developers forget, type errors slip through

# GOOD: CI/CD pipeline (GitHub Actions example)
# .github/workflows/type-check.yml
"""
name: Type Check
on: [push, pull_request]
jobs:
  mypy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install mypy
      - run: mypy src/
"""

# GOOD: pre-commit hook
# .pre-commit-config.yaml
"""
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v0.991
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
"""
```

### Inconsistent Type Hint Usage

```python
# BAD: Inconsistent typing within same module
def get_user(user_id: int) -> dict:  # Untyped dict
    return {"id": user_id}

def create_user(name, email):  # No types at all
    return {"name": name, "email": email}

def delete_user(user_id: int) -> bool:  # Typed
    return True

# GOOD: Consistent typing throughout
class User(TypedDict):
    id: int
    name: str
    email: str

def get_user(user_id: int) -> User:
    return {"id": user_id, "name": "Unknown", "email": "unknown@example.com"}

def create_user(name: str, email: str) -> User:
    return {"id": 0, "name": name, "email": email}

def delete_user(user_id: int) -> bool:
    return True
```

## Tools

### mypy - Standard Type Checker

```bash
# Install
pip install mypy

# Basic usage
mypy file.py
mypy src/

# With config file
mypy --config-file mypy.ini src/

# Show error codes
mypy --show-error-codes src/

# Strict mode
mypy --strict src/

# Generate HTML report
mypy --html-report mypy-report src/

# Ignore missing imports
mypy --ignore-missing-imports src/

# Check specific Python version
mypy --python-version 3.9 src/
```

**Pros:**
- Official type checker
- Excellent documentation
- Large community
- Extensive configuration options

**Cons:**
- Can be slow on large codebases
- Sometimes conservative type inference

### pyright - Microsoft Type Checker

```bash
# Install (requires Node.js)
npm install -g pyright

# Or use via pip
pip install pyright

# Basic usage
pyright src/

# Watch mode
pyright --watch src/

# VS Code integration
# Install "Pylance" extension (includes pyright)
```

**Pros:**
- Very fast
- Excellent IDE integration (VS Code)
- Advanced type inference
- Good error messages

**Cons:**
- Different configuration than mypy
- Less community adoption than mypy

### pyre - Facebook Type Checker

```bash
# Install
pip install pyre-check

# Initialize
pyre init

# Run
pyre check

# Incremental mode
pyre start
pyre incremental
```

**Pros:**
- Fast incremental checking
- Good for large codebases
- Advanced features (infer, query)

**Cons:**
- Less widespread adoption
- Primarily tested on Facebook's codebase

### Type Stubs (.pyi files)

Create stub files for untyped code or third-party libraries:

**mylib.pyi:**
```python
# Stub file (parallel to mylib.py)
def process(data: str) -> int: ...

class Handler:
    def handle(self, event: str) -> None: ...
```

**Usage:**
```bash
# Install type stubs for popular libraries
pip install types-requests
pip install types-redis
pip install types-PyYAML

# Search for available stubs
pip search types-

# Generate stubs from Python code
stubgen -p mypackage -o stubs/
```

**Stub file best practices:**
- Use `...` for function bodies
- Include all public API
- More permissive types than implementation
- Keep in sync with actual code

## Checklists

### Type Hint Quality Checklist

When reviewing code for type hints, verify:

- [ ] All public functions have parameter and return type hints
- [ ] Type hints are accurate (match actual behavior)
- [ ] Complex types use aliases for readability
- [ ] No overuse of `Any` (each `Any` is justified)
- [ ] Collection types are properly specified (e.g., `list[str]` not `list`)
- [ ] Optional parameters use `| None` or `Optional[]`
- [ ] `*args` and `**kwargs` are typed when used
- [ ] Class attributes have type annotations
- [ ] Properties have return type hints
- [ ] No `type: ignore` without error code and explanation
- [ ] Forward references use quotes or `__future__.annotations`
- [ ] Union types use `|` operator (Python 3.10+) or `Union[]`
- [ ] TypedDict used for structured dicts
- [ ] Protocol used instead of forced inheritance where appropriate

### mypy Configuration Checklist

For proper mypy setup, ensure:

- [ ] `mypy.ini` or `pyproject.toml` configuration exists
- [ ] Python version specified in config
- [ ] `warn_return_any` enabled
- [ ] `warn_unused_configs` enabled
- [ ] `no_implicit_optional` enabled
- [ ] `warn_redundant_casts` enabled
- [ ] `warn_unused_ignores` enabled
- [ ] `strict_equality` enabled
- [ ] Per-module overrides for tests and third-party code
- [ ] CI/CD pipeline runs mypy
- [ ] Pre-commit hook for mypy (optional but recommended)
- [ ] Team agrees on strictness level

### Gradual Typing Migration Checklist

When adding types to existing codebase:

- [ ] Start with most critical/public API functions
- [ ] Add types to new code immediately
- [ ] Focus on one module at a time
- [ ] Use `Any` temporarily for complex migrations
- [ ] Run mypy incrementally (not `--strict` initially)
- [ ] Document known type issues in TODO comments
- [ ] Create type stubs for untyped dependencies
- [ ] Enable stricter mypy options gradually
- [ ] Update documentation with type examples
- [ ] Train team on type hint best practices

## Examples

See the `examples/` directory for comprehensive examples:

- `examples/basic_types.py` - Basic type hint usage
- `examples/advanced_types.py` - Generic types, protocols, TypedDict
- `examples/good_vs_bad.py` - Common patterns vs anti-patterns
- `examples/mypy_config_examples/` - Sample mypy configurations

## Templates

### Template: mypy.ini Configuration

Located at: `templates/mypy.ini`

Use this as a starting point for mypy configuration in new projects.

### Template: Type Stub File

Located at: `templates/stub_file.pyi`

Use this template when creating type stubs for untyped code.

### Template: Typed Class

Located at: `templates/typed_class.py`

Example of a well-typed Python class with all common patterns.

## Related Skills

- **python-testing-patterns**: Type hints improve testability and test clarity
- **python-code-style**: Type hints are part of PEP 8 style guidelines
- **python-async-patterns**: Async functions require special type hint considerations

## References

### PEPs (Python Enhancement Proposals)

- **PEP 484**: Type Hints (foundation)
- **PEP 526**: Syntax for Variable Annotations
- **PEP 544**: Protocols (structural subtyping)
- **PEP 585**: Type Hinting Generics In Standard Collections (Python 3.9+)
- **PEP 586**: Literal Types
- **PEP 589**: TypedDict
- **PEP 591**: Final qualifier
- **PEP 604**: Union operator `|` (Python 3.10+)
- **PEP 612**: Parameter Specification Variables
- **PEP 613**: TypeAlias annotation
- **PEP 647**: Type Guards

### Official Documentation

- Python typing module: https://docs.python.org/3/library/typing.html
- mypy documentation: https://mypy.readthedocs.io/
- Type hints cheat sheet: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

### External Resources

- Real Python typing guide: https://realpython.com/python-type-checking/
- typing_extensions package: https://pypi.org/project/typing-extensions/

---

**Version:** 1.0
**Last Updated:** 2025-12-24
**Target Python Version:** 3.9+
**Maintainer:** Uncle Duke (Python Development Agent)
