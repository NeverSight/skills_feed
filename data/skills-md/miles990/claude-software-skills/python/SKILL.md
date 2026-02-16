---
name: python
description: Python programming patterns and best practices
domain: programming-languages
version: 1.1.0
tags: [python, typing, async, dataclasses, decorators]
triggers:
  keywords:
    primary: [python, py, pandas, numpy, pip, venv]
    secondary: [asyncio, typing, dataclass, decorator, pytest]
  context_boost: [data, analysis, scripting, automation, backend]
  context_penalty: [java, csharp, golang]
  priority: high
---

# Python

## Overview

Modern Python development patterns including type hints, async programming, and Pythonic idioms.

---

## Type Hints

### Basic Types

```python
from typing import (
    Optional, Union, List, Dict, Set, Tuple,
    TypeVar, Generic, Callable, Any,
    Literal, TypedDict, Protocol
)
from dataclasses import dataclass
from datetime import datetime

# Basic type hints
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Optional (can be None)
def find_user(user_id: str) -> Optional['User']:
    return users.get(user_id)

# Union types
def process(value: Union[str, int]) -> str:
    return str(value)

# Python 3.10+ union syntax
def process_new(value: str | int | None) -> str:
    return str(value) if value else ""

# Collections
def process_items(
    items: List[str],
    mapping: Dict[str, int],
    unique: Set[str],
    pair: Tuple[str, int]
) -> None:
    pass

# Python 3.9+ built-in generics
def process_items_new(
    items: list[str],
    mapping: dict[str, int],
    unique: set[str]
) -> None:
    pass
```

### Advanced Types

```python
# TypeVar for generics
T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# Generic classes
class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def get(self, id: str) -> T | None:
        return self._items.get(id)

    def save(self, id: str, item: T) -> None:
        self._items[id] = item

# TypedDict for structured dicts
class UserDict(TypedDict):
    id: str
    name: str
    email: str
    age: int  # Required
    nickname: str  # Required

class PartialUserDict(TypedDict, total=False):
    nickname: str  # Optional

# Literal types
Mode = Literal["read", "write", "append"]

def open_file(path: str, mode: Mode) -> None:
    pass

# Protocol (structural typing)
class Readable(Protocol):
    def read(self) -> str: ...

def process_readable(source: Readable) -> str:
    return source.read()

# Callable types
Handler = Callable[[str, int], bool]
AsyncHandler = Callable[[str], 'Awaitable[bool]']

def register_handler(handler: Handler) -> None:
    pass
```

---

## Dataclasses

```python
from dataclasses import dataclass, field, asdict, astuple
from typing import ClassVar
from datetime import datetime

@dataclass
class User:
    id: str
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)
    _cache: dict = field(default_factory=dict, repr=False, compare=False)

    # Class variable (not instance field)
    MAX_TAGS: ClassVar[int] = 10

    def __post_init__(self):
        # Validation after init
        if len(self.tags) > self.MAX_TAGS:
            raise ValueError(f"Too many tags (max {self.MAX_TAGS})")

# Frozen (immutable)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Slots for memory efficiency
@dataclass(slots=True)
class LightweightUser:
    id: str
    name: str

# Convert to dict/tuple
user = User(id="1", email="test@example.com", name="Test")
user_dict = asdict(user)
user_tuple = astuple(user)
```

---

## Decorators

```python
from functools import wraps
from typing import TypeVar, Callable, ParamSpec
import time

P = ParamSpec('P')
R = TypeVar('R')

# Basic decorator
def timer(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

# Decorator with arguments
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception: Exception | None = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

# Class decorator
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

# Usage
@timer
@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    # ... fetch logic
    pass

@singleton
class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
```

---

## Async Programming

```python
import asyncio
from typing import AsyncIterator
import aiohttp

# Async function
async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Parallel execution
async def fetch_all(urls: list[str]) -> list[str]:
    tasks = [fetch_url(url) for url in urls]
    return await asyncio.gather(*tasks)

# With error handling
async def fetch_all_safe(urls: list[str]) -> list[str | None]:
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r if isinstance(r, str) else None for r in results]

# Async context manager
class AsyncDatabase:
    async def __aenter__(self) -> 'AsyncDatabase':
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.disconnect()

    async def connect(self) -> None:
        print("Connecting...")

    async def disconnect(self) -> None:
        print("Disconnecting...")

# Async generator
async def paginate(
    fetch_page: Callable[[int], 'Awaitable[list[T]]']
) -> AsyncIterator[T]:
    page = 1
    while True:
        items = await fetch_page(page)
        if not items:
            break
        for item in items:
            yield item
        page += 1

# Using async for
async def process_all_items():
    async for item in paginate(fetch_page):
        await process_item(item)

# Semaphore for rate limiting
async def fetch_with_limit(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_limited(url: str) -> str:
        async with semaphore:
            return await fetch_url(url)

    return await asyncio.gather(*[fetch_limited(url) for url in urls])
```

---

## Context Managers

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, AsyncGenerator

# Class-based context manager
class Timer:
    def __init__(self, name: str):
        self.name = name
        self.start: float = 0
        self.elapsed: float = 0

    def __enter__(self) -> 'Timer':
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.elapsed = time.perf_counter() - self.start
        print(f"{self.name}: {self.elapsed:.4f}s")

# Generator-based context manager
@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.4f}s")

# Async context manager
@asynccontextmanager
async def async_timer(name: str) -> AsyncGenerator[None, None]:
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.4f}s")

# Usage
with timer("operation"):
    do_something()

async with async_timer("async_operation"):
    await do_something_async()
```

---

## Itertools and Generators

```python
from itertools import (
    chain, islice, groupby, takewhile, dropwhile,
    combinations, permutations, product, accumulate
)
from typing import Iterator, Iterable

# Generator function
def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Take first n
first_10_fib = list(islice(fibonacci(), 10))

# Generator expression
squares = (x ** 2 for x in range(10))

# Chain multiple iterables
all_items = chain(list1, list2, list3)

# Group by
data = [
    {"type": "a", "value": 1},
    {"type": "a", "value": 2},
    {"type": "b", "value": 3},
]
for key, group in groupby(sorted(data, key=lambda x: x["type"]), key=lambda x: x["type"]):
    print(f"{key}: {list(group)}")

# Batching
def batch(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    iterator = iter(iterable)
    while batch := list(islice(iterator, size)):
        yield batch

# Sliding window
def sliding_window(iterable: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    from collections import deque
    iterator = iter(iterable)
    window = deque(islice(iterator, size), maxlen=size)
    if len(window) == size:
        yield tuple(window)
    for item in iterator:
        window.append(item)
        yield tuple(window)
```

---

## Error Handling

```python
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')
E = TypeVar('E', bound=Exception)

# Custom exceptions
class AppError(Exception):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code

class ValidationError(AppError):
    def __init__(self, message: str, fields: dict[str, list[str]]):
        super().__init__(message, "VALIDATION_ERROR")
        self.fields = fields

# Result type pattern
@dataclass
class Ok(Generic[T]):
    value: T

    def is_ok(self) -> bool:
        return True

    def is_err(self) -> bool:
        return False

@dataclass
class Err(Generic[E]):
    error: E

    def is_ok(self) -> bool:
        return False

    def is_err(self) -> bool:
        return True

Result = Ok[T] | Err[E]

def parse_int(s: str) -> Result[int, ValueError]:
    try:
        return Ok(int(s))
    except ValueError as e:
        return Err(e)

# Exception chaining
try:
    process_data()
except ValueError as e:
    raise AppError("Failed to process data", "PROCESS_ERROR") from e
```

---

## Related Skills

- [[ai-ml-integration]] - ML/AI with Python
- [[backend]] - FastAPI/Django
- [[automation-scripts]] - Scripting and automation
