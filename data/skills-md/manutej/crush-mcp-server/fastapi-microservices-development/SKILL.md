---
name: fastapi-microservices-development
description: Comprehensive guide for building production-ready microservices with FastAPI including REST API patterns, async operations, dependency injection, and deployment strategies
tags: [fastapi, microservices, rest-api, async, python, production]
tier: tier-1
---

# FastAPI Microservices Development

A comprehensive skill for building production-ready microservices using FastAPI. This skill covers REST API design patterns, asynchronous operations, dependency injection, testing strategies, and deployment best practices for scalable Python applications.

## When to Use This Skill

Use this skill when:

- Building RESTful microservices with Python
- Developing high-performance async APIs
- Creating production-grade web services with comprehensive validation
- Implementing service-oriented architectures
- Building APIs requiring advanced dependency injection
- Developing services with complex authentication/authorization
- Creating scalable, maintainable backend services
- Building APIs with automatic OpenAPI documentation
- Implementing WebSocket services alongside REST APIs
- Deploying containerized Python services to production

## Core Concepts

### FastAPI Fundamentals

FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.

**Key Features:**
- **Fast**: Very high performance, on par with NodeJS and Go (powered by Starlette and Pydantic)
- **Fast to code**: Increase development speed by 200-300%
- **Fewer bugs**: Reduce human-induced errors by about 40%
- **Intuitive**: Great editor support with autocompletion everywhere
- **Easy**: Designed to be easy to learn and use
- **Short**: Minimize code duplication
- **Robust**: Production-ready code with automatic interactive documentation
- **Standards-based**: Based on OpenAPI and JSON Schema

### Async/Await Programming

FastAPI fully supports asynchronous request handling using Python's `async`/`await` syntax:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/burgers')
async def read_burgers():
    burgers = await get_burgers(2)
    return burgers
```

**When to use `async def`:**
- Database queries with async drivers
- External API calls
- File I/O operations
- Long-running computations that can be awaited
- WebSocket connections
- Background task processing

**When to use regular `def`:**
- Simple CRUD operations
- Synchronous database libraries
- CPU-bound operations
- Quick data transformations

### Dependency Injection System

FastAPI's dependency injection is one of its most powerful features, enabling:

- Code reusability across endpoints
- Shared logic implementation
- Database connection management
- Authentication and authorization
- Request validation
- Background task scheduling

**Basic Dependency Pattern:**

```python
from typing import Annotated, Union
from fastapi import Depends, FastAPI

app = FastAPI()

# Dependency function
async def common_parameters(
    q: Union[str, None] = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

# Using dependency in multiple endpoints
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return {"params": commons, "items": ["item1", "item2"]}

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return {"params": commons, "users": ["user1", "user2"]}
```

## Microservices Architecture Patterns

### Service Design Principles

**1. Single Responsibility**
- Each microservice handles one business capability
- Clear boundaries and minimal coupling
- Independent deployment and scaling

**2. API-First Design**
- Design APIs before implementation
- Use OpenAPI schemas for contracts
- Version APIs appropriately

**3. Database Per Service**
- Each service owns its data
- No direct database sharing
- Use APIs for cross-service data access

**4. Stateless Services**
- Services don't maintain client session state
- Enables horizontal scaling
- Use external storage for session data

### Service Communication Patterns

**Synchronous Communication (REST APIs):**
```python
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    # Call another microservice
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"http://inventory-service/stock/{order_id}")
            inventory_data = response.json()
        except httpx.HTTPError:
            raise HTTPException(status_code=503, detail="Inventory service unavailable")

    return {"order_id": order_id, "inventory": inventory_data}
```

**Event-Driven Communication:**
- Use message brokers (RabbitMQ, Kafka, Redis)
- Publish/Subscribe patterns
- Asynchronous processing
- Loose coupling between services

### Service Discovery

**Options:**
- Environment variables for simple setups
- Consul, Eureka for dynamic discovery
- Kubernetes DNS for K8s deployments
- API Gateway for centralized routing

## REST API Design Patterns

### Resource Modeling

**RESTful Resource Design:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Resource Models
class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# Collection Endpoints
@app.get("/items/", response_model=List[Item])
async def list_items(skip: int = 0, limit: int = 100):
    """List all items with pagination"""
    items = await get_items_from_db(skip=skip, limit=limit)
    return items

@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item"""
    new_item = await save_item_to_db(item)
    return new_item

# Resource Endpoints
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """Get a specific item by ID"""
    item = await get_item_from_db(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """Update an existing item"""
    updated_item = await update_item_in_db(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item"""
    success = await delete_item_from_db(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
```

### API Versioning

**URL Path Versioning (Recommended):**

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# V1 API Router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users/")
async def list_users_v1():
    return {"version": "v1", "users": []}

# V2 API Router
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users/")
async def list_users_v2():
    return {"version": "v2", "users": [], "metadata": {}}

app.include_router(v1_router)
app.include_router(v2_router)
```

### Request/Response Validation

FastAPI uses Pydantic for automatic validation:

```python
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=0, le=150)

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator('password')
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('must contain at least one uppercase letter')
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # Automatic validation of request body
    new_user = await save_user(user)
    return new_user
```

## Advanced Dependency Injection

### Dependencies with Yield

Dependencies can use `yield` for setup/teardown operations:

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# Database dependency with cleanup
async def get_db():
    db = await connect_to_database()
    try:
        yield db
    finally:
        await db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    items = await db.query("SELECT * FROM items")
    return items
```

**Advanced Resource Management:**

```python
from fastapi import Depends, HTTPException

async def get_database():
    with Session() as session:
        try:
            yield session
        except HTTPException:
            session.rollback()
            raise
        finally:
            session.close()

@app.post("/users/")
async def create_user(user: UserCreate, db = Depends(get_database)):
    try:
        new_user = db.add(User(**user.dict()))
        db.commit()
        return new_user
    except Exception as e:
        # Session automatically rolled back by dependency
        raise HTTPException(status_code=500, detail=str(e))
```

### Sub-Dependencies

Dependencies can depend on other dependencies:

```python
from typing import Optional
from fastapi import FastAPI, Depends, Cookie

app = FastAPI()

async def query_extractor(q: Optional[str] = None):
    return q

async def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q

@app.get('/items/')
async def read_items(query: str = Depends(query_or_cookie_extractor)):
    return {'query': query}
```

### Class-Based Dependencies

Use classes for complex dependency logic:

```python
from typing import Optional
from fastapi import FastAPI, Depends

app = FastAPI()

class CommonQueryParams:
    def __init__(
        self,
        q: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return {"q": commons.q, "skip": commons.skip, "limit": commons.limit}

# Shortcut syntax
@app.get("/users/")
async def read_users(commons: CommonQueryParams = Depends()):
    return commons
```

### Global Dependencies

Apply dependencies to all routes:

```python
from fastapi import FastAPI, Depends, Header, HTTPException

async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    return x_token

async def verify_key(x_key: str = Header(...)):
    if x_key != "secret-key":
        raise HTTPException(status_code=400, detail="Invalid X-Key header")
    return x_key

# Apply to entire application
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# Apply to router
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    dependencies=[Depends(verify_token)]
)

@router.get("/")
async def read_items():
    return [{"item_id": "Foo"}]

app.include_router(router)
```

### Reusable Dependency Aliases

Create type aliases for common dependencies:

```python
from typing import Annotated
from fastapi import Depends

# Define reusable dependency types
async def get_current_user():
    return {"username": "johndoe"}

CurrentUser = Annotated[dict, Depends(get_current_user)]

# Use across multiple endpoints
@app.get("/items/")
def read_items(user: CurrentUser):
    return {"user": user, "items": []}

@app.post("/items/")
def create_item(user: CurrentUser, item: Item):
    return {"user": user, "item": item}

@app.delete("/items/{item_id}")
def delete_item(user: CurrentUser, item_id: int):
    return {"user": user, "deleted": item_id}
```

## Authentication & Authorization

### OAuth2 with Password Flow

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    user = await get_user_from_db(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### OAuth2 with Scopes

```python
from fastapi.security import SecurityScopes
from pydantic import ValidationError

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_scopes = payload.get("scopes", [])
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/items/", dependencies=[Security(get_current_user, scopes=["items:read"])])
async def read_items():
    return [{"item_id": "Foo"}]

@app.post("/items/", dependencies=[Security(get_current_user, scopes=["items:write"])])
async def create_item(item: Item):
    return item
```

## Background Tasks

### Simple Background Tasks

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log_file:
        log_file.write(message)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}\n")
    return {"message": "Notification sent in the background"}
```

### Background Tasks with Dependencies

```python
from fastapi import BackgroundTasks, Depends
from typing import Annotated

def write_log(message: str):
    with open("log.txt", mode="a") as log_file:
        log_file.write(message)

async def get_query_and_log(
    query: str | None = None,
    background_tasks: BackgroundTasks = Depends()
):
    if query:
        background_tasks.add_task(write_log, f"query: {query}\n")
    return query

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
    query: Annotated[str | None, Depends(get_query_and_log)],
):
    background_tasks.add_task(write_log, f"email: {email}, query: {query}\n")
    return {"message": "Notification sent"}
```

## WebSocket Support

### Basic WebSocket

```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

### WebSocket with Dependencies

```python
from fastapi import WebSocket, Depends, Query, Cookie, WebSocketException, status

async def get_cookie_or_token(
    websocket: WebSocket,
    session: str | None = Cookie(None),
    token: str | None = Query(None),
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.websocket("/ws/{item_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: str = Depends(get_cookie_or_token),
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(
                f"Session: {cookie_or_token}, Item: {item_id}, Data: {data}"
            )
    except WebSocketDisconnect:
        print(f"Client {item_id} disconnected")
```

### WebSocket Connection Manager

```python
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
```

## Database Integration

### SQLAlchemy with Async

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

@app.get("/users/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### MongoDB with Motor

```python
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

MONGODB_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGODB_URL)
database = client.mydatabase

async def get_database():
    return database

@app.post("/items/")
async def create_item(item: Item, db = Depends(get_database)):
    result = await db.items.insert_one(item.dict())
    return {"id": str(result.inserted_id)}

@app.get("/items/{item_id}")
async def read_item(item_id: str, db = Depends(get_database)):
    from bson import ObjectId
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item["_id"] = str(item["_id"])
    return item
```

## Error Handling

### Custom Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

### Override Default Exception Handlers

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc), status_code=400)
```

## Testing

### Test Setup with TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 45.2}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Foo"

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert "name" in response.json()
```

### Testing with Dependencies

```python
from fastapi import Depends

async def override_get_db():
    return {"test": "database"}

app.dependency_overrides[get_db] = override_get_db

def test_with_dependency():
    response = client.get("/items/")
    assert response.status_code == 200
    # Uses overridden dependency
```

### Async Testing

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_read_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## Production Deployment

### Docker Configuration

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Multi-stage Build:**

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./app /app

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Kubernetes Deployment

**deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: myregistry/fastapi-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  selector:
    app: fastapi
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Environment Configuration

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "FastAPI Microservice"
    database_url: str
    redis_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

@app.get("/info")
async def info(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name}
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness_check(db = Depends(get_db)):
    try:
        # Check database connectivity
        await db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service not ready")
```

## Monitoring & Logging

### Structured Logging

```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        return json.dumps(log_data)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## Best Practices

### 1. Project Structure

```
fastapi-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   └── database.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_items.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

### 2. Separation of Concerns

**models.py** - Database models:
```python
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
```

**schemas.py** - Pydantic schemas:
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
```

**services.py** - Business logic:
```python
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def create_user(self, user_data: UserCreate):
        # Business logic here
        pass
```

**routers.py** - API endpoints:
```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)
```

### 3. Security Best Practices

- Always use HTTPS in production
- Implement rate limiting
- Validate and sanitize all inputs
- Use dependency injection for auth
- Store secrets in environment variables
- Implement CORS properly
- Use security headers
- Hash passwords with bcrypt/argon2
- Implement JWT token expiration
- Use OAuth2 scopes for authorization

### 4. Performance Optimization

- Use async/await for I/O operations
- Implement caching (Redis)
- Use database connection pooling
- Paginate large responses
- Compress responses (gzip)
- Use CDN for static assets
- Implement database indexes
- Use background tasks for heavy operations
- Monitor with APM tools
- Load test before production

### 5. API Documentation

FastAPI automatically generates OpenAPI documentation, but you can enhance it:

```python
app = FastAPI(
    title="My Microservice API",
    description="Production-ready microservice with FastAPI",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

@app.get(
    "/items/",
    response_model=List[Item],
    summary="List all items",
    description="Retrieve a paginated list of items from the database",
    response_description="List of items with pagination metadata",
)
async def list_items(
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(100, description="Maximum number of items to return"),
):
    """
    List items with pagination support.

    - **skip**: Number of items to skip (for pagination)
    - **limit**: Maximum number of items to return
    """
    return await get_items(skip=skip, limit=limit)
```

## Common Patterns & Examples

See EXAMPLES.md for 15+ detailed, production-ready examples covering:
- CRUD operations with async databases
- Authentication flows
- File upload handling
- Caching strategies
- Rate limiting
- Event-driven architectures
- Testing patterns
- Deployment configurations
- And more...

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Backend Development, Microservices, Python, REST APIs
**Compatible With**: FastAPI 0.100+, Python 3.7+, Pydantic 2.0+
