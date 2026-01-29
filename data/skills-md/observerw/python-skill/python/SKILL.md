---
name: python
description: Comprehensive guide for the entire Python programming process. This skill MUST be consulted before writing any code in a Python project to ensure adherence to toolchains, standards, and best practices.
---

# Python Programming Guide

## Toolchain

- Type Checking: `ty check <FILE_PATH> --output-format concise`
- Lint: `ruff check --fix --unsafe-fixes <FILE_PATH>`
- Format: `ruff format <FILE_PATH>`
- Run tests: `uv run pytest`
- Sync deps: `uv sync --upgrade`
- NEVER use `python`; use `uv run` instead

## References

When deeply modifying code in these areas, you MUST read the corresponding document first:

- `references/async-programming.md` - before modifying anyio/async code
- `references/type-hints-cheat-sheet.md` - before modifying complex type annotations
- `references/exceptions.md` - before modifying error handling
- `references/logging.md` - before modifying logging

## Code Standards

⚠️ **You MUST fully understand and follow ALL rules demonstrated in the code example below BEFORE writing any code. Every RULE and ANTI-PATTERN shown is mandatory.**

```python
from __future__ import annotations

# RULE: Use relative imports for intra-package imports.
# RULE: Use absolute imports for inter-package and third-party imports.
from . import internal_module
from anyio import fail_after
# ANTI-PATTERN: from mypackage.module import thing  # (when inside mypackage)
# ANTI-PATTERN: from ..other_package import thing

import time
from collections.abc import Awaitable, Callable
from typing import Any, Protocol, TypedDict

import anyio
import attrs
from anyio import fail_after
from loguru import logger


class UserData(TypedDict):
    """
    RULE: Use TypedDict for complex return values instead of plain dict/tuple.

    ANTI-PATTERN: def get_user() -> dict[str, Any]: ...
    ANTI-PATTERN: def get_coords() -> tuple[float, float, str]: ...
    """

    user_id: str
    name: str
    email: str


# RULE: Use Python 3.12+ `type` statement for type aliases
# ANTI-PATTERN: JsonValue: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
type JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


class FetchResult(TypedDict):
    """RULE: Use TypedDict instead of tuple or dict for multi-value returns."""

    data: UserData | None
    error: str | None


class Validator(Protocol):
    """
    RULE: Use Protocol with __call__ for complex callable signatures.

    ANTI-PATTERN: Callable[[dict[str, Any], bool], bool]
    """

    def __call__(self, data: dict[str, Any], *, strict: bool = False) -> bool: ...


@attrs.define
class Config:
    """
    RULE: ALL classes MUST use @attrs.define or @attrs.frozen.

    ANTI-PATTERN: class Foo: def __init__(self, x): self.x = x
    """

    url: str
    timeout: float = 10.0
    headers: dict[str, str] = attrs.field(factory=dict)
    retry: int = attrs.field(default=3)

    @retry.validator
    def _check_retry(self, attribute: attrs.Attribute[int], value: int) -> None:
        """RULE: Use attrs validators for field validation."""
        if value < 0:
            msg = "retry must be >= 0"
            raise ValueError(msg)


@attrs.frozen
class DataSource:
    """
    RULE: Use @attrs.frozen for immutable objects. Prefer composition over inheritance.

    ANTI-PATTERN: class Base: def __getattr__(self, name): ...
    ANTI-PATTERN: class Child(Parent(GrandParent)): ...
    """

    name: str
    endpoint: str
    priority: int = 0


class ServiceError(Exception):
    """RULE: Domain-specific exceptions only."""


class NotFoundError(ServiceError):
    """RULE: Create specific exception types only when different handling is needed."""


def log_time[**P, R](func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
    """
    RULE: Use Python 3.12+ type parameter syntax [T], [**P, R].

    ANTI-PATTERN: T = TypeVar("T")
    ANTI-PATTERN: P = ParamSpec("P")
    ANTI-PATTERN: def func(x: T) -> T: ...
    """

    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.2f}s")
        return result

    return wrapper


@attrs.define
class ApiClient:
    """
    RULE: Use anyio for ALL async code.

    ANTI-PATTERN: asyncio.create_task(coro)
    ANTI-PATTERN: await asyncio.gather(*coros)
    """

    config: Config
    sources: list[DataSource] = attrs.field(factory=list)

    def __attrs_post_init__(self) -> None:
        """RULE: Use __attrs_post_init__ for complex initialization logic."""
        self.sources.sort(key=lambda s: s.priority, reverse=True)

    @log_time
    async def fetch(
        self,
        user_id: str,
        *,
        timeout: float | None = None,
    ) -> UserData:
        """
        RULE: Place parameters with defaults after * to force keyword-only usage.
        RULE: No meaningless return values - raise or return None instead.

        ANTI-PATTERN: return UserData(user_id="", name="", email="")
        """
        timeout = timeout or self.config.timeout
        errors: list[str] = []

        for source in self.sources:
            result = await self._try_fetch_from(source, user_id, timeout)
            if result["data"]:
                return result["data"]
            if result["error"]:
                errors.append(f"{source.name}: {result['error']}")

        msg = f"User {user_id} not found in any source. Errors: {errors}"
        raise NotFoundError(msg)

    async def _try_fetch_from(
        self, source: DataSource, user_id: str, timeout: float
    ) -> FetchResult:
        """
        RULE: No pointless exception wrapping - let unexpected exceptions propagate.

        ANTI-PATTERN: except Exception as e: raise FetchError(str(e)) from e
        """
        try:
            with fail_after(timeout):
                data = await self._fetch_from(source, user_id)
                return FetchResult(data=data, error=None)
        except TimeoutError as e:
            return FetchResult(data=None, error=f"timeout: {e}")
        except ConnectionError as e:
            return FetchResult(data=None, error=f"connection failed: {e}")

    async def _fetch_from(self, source: DataSource, user_id: str) -> UserData:
        """
        RULE: Use concrete types instead of Any when structure is known.

        ANTI-PATTERN: async def _fetch_from(self, source: Any, user_id: Any) -> Any: ...
        """
        await anyio.sleep(0.1)
        return UserData(
            user_id=user_id, name=f"User {user_id}", email="test@example.com"
        )

    async def fetch_multiple(self, user_ids: list[str]) -> list[UserData]:
        """
        RULE: Parallel tasks MUST use anyio.create_task_group().
        RULE: Handle exceptions with except* (Python 3.11+) or ExceptionGroup.
        """
        results: list[UserData] = []
        failed: list[str] = []

        async def fetch_and_collect(uid: str) -> None:
            try:
                data = await self.fetch(uid)
                results.append(data)
            except NotFoundError as e:
                failed.append(f"{uid}: {e}")

        try:
            async with anyio.create_task_group() as tg:
                for user_id in user_ids:
                    tg.start_soon(fetch_and_collect, user_id)
        except* TimeoutError as eg:
            for exc in eg.exceptions:
                print(f"Timeout in parallel fetch: {exc}")

        if failed:
            print(f"Failed to fetch: {failed}")

        return results

    async def process(self, response: dict[str, Any] | list[Any] | str) -> str:
        """
        RULE: Use match instead of chained if isinstance() checks.
        RULE: Use static attribute access instead of getattr/setattr/hasattr.

        ANTI-PATTERN: if isinstance(x, dict): ... elif isinstance(x, list): ...
        ANTI-PATTERN: value = getattr(obj, "field")
        """
        match response:
            case {"status": "ok", "data": data}:
                return f"Success: {data}"
            case {"error": msg}:
                return f"Error: {msg}"
            case list() as items:
                return f"Got {len(items)} items"
            case str() as message:
                return message
            case _:
                return "Unknown"


# ANTI-PATTERN: def create_wrong(**kwargs: Any) -> ApiClient: return ApiClient(config=Config(**kwargs))


async def create_correct(config: Config) -> ApiClient:
    """RULE: Accept constructed objects directly instead of **kwargs."""
    return ApiClient(config=config)


# ANTI-PATTERN: config_path = Path(__file__).parent / "data" / "config.json"


def load_config_correct() -> dict[str, Any]:
    """RULE: Use importlib.resources.files() instead of __file__ path concatenation."""
    import json
    from importlib.resources import files

    config_text = (files("mypackage") / "data" / "config.json").read_text()
    return json.loads(config_text)


@logger.catch(reraise=True)
async def main() -> None:
    """RULE: Use @logger.catch at entrypoints for automatic exception logging."""
    config = Config(url="https://api.example.com", timeout=5.0)
    sources = [
        DataSource(name="primary", endpoint="https://api1.com", priority=10),
        DataSource(name="backup", endpoint="https://api2.com", priority=5),
    ]
    client = ApiClient(config=config, sources=sources)

    user = await client.fetch("user123")
    logger.info("Fetched user: {}", user["name"])

    users = await client.fetch_multiple(["u1", "u2", "u3"])
    logger.info("Fetched {} users", len(users))
```
