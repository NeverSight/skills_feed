---
name: python-backend
description: >
  Python backend development expertise for FastAPI, security patterns, database operations,
  Upstash integrations, and code quality. Use when: (1) Building REST APIs with FastAPI,
  (2) Implementing JWT/OAuth2 authentication, (3) Setting up SQLAlchemy/async databases,
  (4) Integrating Redis/Upstash caching, (5) Refactoring AI-generated Python code (deslopification),
  (6) Designing API patterns, or (7) Optimizing backend performance.
---

# python-backend

Production-ready Python backend patterns for FastAPI, SQLAlchemy, and Upstash.

## When to Use This Skill

- Building REST APIs with FastAPI
- Implementing JWT/OAuth2 authentication
- Setting up SQLAlchemy async databases
- Integrating Redis/Upstash caching and rate limiting
- Refactoring AI-generated Python code
- Designing API patterns and project structure

## Core Principles

1. **Async-first** - Use async/await for I/O operations
2. **Type everything** - Pydantic models for validation
3. **Dependency injection** - Use FastAPI's Depends()
4. **Fail fast** - Validate early, use HTTPException
5. **Security by default** - Never trust user input

## Quick Patterns

### Project Structure

```
src/
├── auth/
│   ├── router.py      # endpoints
│   ├── schemas.py     # pydantic models
│   ├── models.py      # db models
│   ├── service.py     # business logic
│   └── dependencies.py
├── posts/
│   └── ...
├── config.py
├── database.py
└── main.py
```

### Async Routes

```python
# BAD - blocks event loop
@router.get("/")
async def bad():
    time.sleep(10)  # Blocking!

# GOOD - runs in threadpool
@router.get("/")
def good():
    time.sleep(10)  # OK in sync function

# BEST - non-blocking
@router.get("/")
async def best():
    await asyncio.sleep(10)  # Non-blocking
```

### Pydantic Validation

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    age: int = Field(ge=18)
```

### Dependency Injection

```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    user = await get_user(payload["sub"])
    if not user:
        raise HTTPException(401, "User not found")
    return user

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

### SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
```

### Redis Caching

```python
from upstash_redis import Redis

redis = Redis.from_env()

@app.get("/data/{id}")
def get_data(id: str):
    cached = redis.get(f"data:{id}")
    if cached:
        return cached
    data = fetch_from_db(id)
    redis.setex(f"data:{id}", 600, data)
    return data
```

### Rate Limiting

```python
from upstash_ratelimit import Ratelimit, SlidingWindow

ratelimit = Ratelimit(
    redis=Redis.from_env(),
    limiter=SlidingWindow(max_requests=10, window=60),
)

@app.get("/api/resource")
def protected(request: Request):
    result = ratelimit.limit(request.client.host)
    if not result.allowed:
        raise HTTPException(429, "Rate limit exceeded")
    return {"data": "..."}
```

## Reference Documents

For detailed patterns, see:

| Document | Content |
|----------|---------|
| `references/fastapi_patterns.md` | Project structure, async, Pydantic, dependencies, testing |
| `references/security_patterns.md` | JWT, OAuth2, password hashing, CORS, API keys |
| `references/database_patterns.md` | SQLAlchemy async, transactions, eager loading, migrations |
| `references/upstash_patterns.md` | Redis, rate limiting, QStash background jobs |

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/)
- [Upstash Documentation](https://upstash.com/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
