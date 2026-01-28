---
name: rest-api-design-patterns
description: Comprehensive guide for designing RESTful APIs including resource modeling, versioning strategies, HATEOAS, pagination, filtering, and HTTP best practices
tags: [rest-api, api-design, http, resource-modeling, versioning, best-practices]
tier: tier-1
---

# REST API Design Patterns

A comprehensive skill for designing, implementing, and maintaining RESTful APIs. Master resource modeling, HTTP methods, versioning strategies, pagination, filtering, error handling, and best practices for building scalable, maintainable APIs using FastAPI, Express.js, and modern frameworks.

## When to Use This Skill

Use this skill when:

- Designing a new RESTful API from scratch
- Building microservices with HTTP/REST interfaces
- Refactoring existing APIs for better design and consistency
- Implementing CRUD operations with proper HTTP semantics
- Adding versioning to an existing API
- Designing resource relationships and nested endpoints
- Implementing pagination, filtering, and sorting
- Handling errors and validation consistently
- Building hypermedia-driven APIs (HATEOAS)
- Optimizing API performance with caching and compression
- Documenting APIs with OpenAPI/Swagger specifications
- Ensuring API security with authentication and authorization patterns

## Core REST Principles

### What is REST?

REST (Representational State Transfer) is an architectural style for distributed systems that emphasizes:

1. **Resource-Based**: Everything is a resource with a unique identifier (URI)
2. **Standard Methods**: Use standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
3. **Stateless**: Each request contains all information needed to process it
4. **Client-Server**: Clear separation between client and server
5. **Cacheable**: Responses can be cached for performance
6. **Uniform Interface**: Consistent patterns across the API

### REST Maturity Model (Richardson Maturity Model)

**Level 0 - The Swamp of POX**: Single URI, single HTTP method (usually POST)
- Example: `/api` with all operations in POST body

**Level 1 - Resources**: Multiple URIs, each representing a resource
- Example: `/users`, `/posts`, `/products`

**Level 2 - HTTP Verbs**: Proper use of HTTP methods
- Example: GET `/users/123`, POST `/users`, PUT `/users/123`

**Level 3 - Hypermedia Controls (HATEOAS)**: API responses include links to related resources
- Example: Response includes `"_links": {"self": "/users/123", "posts": "/users/123/posts"}`

## Resource Modeling

### Resource Naming Conventions

**1. Use Nouns, Not Verbs**

```
Good:
  GET /users
  GET /products
  POST /orders

Bad:
  GET /getUsers
  GET /getAllProducts
  POST /createOrder
```

**2. Use Plural Nouns for Collections**

```
Good:
  GET /users          # Collection
  GET /users/123      # Individual resource

Bad:
  GET /user
  GET /user/123
```

**3. Use Lowercase and Hyphens**

```
Good:
  /user-profiles
  /order-items
  /payment-methods

Bad:
  /userProfiles
  /OrderItems
  /payment_methods
```

**4. Hierarchy for Related Resources**

```
Good:
  /users/123/posts
  /users/123/posts/456
  /users/123/posts/456/comments

Avoid Deep Nesting (max 2-3 levels):
  /organizations/1/departments/2/teams/3/members/4/tasks/5  # Too deep!
```

### Resource Design Patterns

#### Pattern 1: Collection and Item Resources

```
Collection Resource:
  GET    /products          # List all products
  POST   /products          # Create new product

Item Resource:
  GET    /products/123      # Get specific product
  PUT    /products/123      # Replace product (full update)
  PATCH  /products/123      # Partial update
  DELETE /products/123      # Delete product
```

#### Pattern 2: Nested Resources (Parent-Child Relationships)

```
# Comments belong to posts
GET    /posts/42/comments       # List comments for post 42
POST   /posts/42/comments       # Create comment on post 42
GET    /posts/42/comments/7     # Get specific comment
DELETE /posts/42/comments/7     # Delete specific comment

# Alternative for accessing comments directly
GET    /comments/7              # Get comment by ID (if you have it)
```

#### Pattern 3: Filtering Collections (Query Parameters)

```
GET /products?category=electronics
GET /products?price_min=100&price_max=500
GET /products?sort=price&order=desc
GET /users?status=active&role=admin
GET /posts?author=123&published=true
```

#### Pattern 4: Actions on Resources (Controllers)

For operations that don't fit standard CRUD:

```
POST /users/123/activate          # Activate user account
POST /orders/456/cancel           # Cancel order
POST /payments/789/refund         # Refund payment
POST /documents/321/publish       # Publish document
POST /subscriptions/654/renew     # Renew subscription
```

#### Pattern 5: Bulk Operations

```
POST /users/bulk-create           # Create multiple users
PATCH /products/bulk-update       # Update multiple products
DELETE /orders/bulk-delete        # Delete multiple orders

# Or using query parameters
DELETE /orders?ids=1,2,3,4,5
```

## HTTP Methods Deep Dive

### GET - Retrieve Resources

**Characteristics:**
- Safe: No side effects
- Idempotent: Multiple identical requests have the same effect
- Cacheable: Responses can be cached

**FastAPI Example:**

```python
from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()

# Collection endpoint
@app.get("/items/")
async def list_items(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None
) -> List[dict]:
    """List items with pagination and filtering."""
    # Filter and paginate
    items = get_items_from_db(skip=skip, limit=limit, category=category)
    return items

# Individual resource endpoint
@app.get("/items/{item_id}")
async def get_item(item_id: int) -> dict:
    """Get a specific item by ID."""
    item = get_item_from_db(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

**Express.js Example:**

```javascript
const express = require('express');
const app = express();

// Collection endpoint
app.get('/items', async (req, res) => {
  try {
    const { skip = 0, limit = 10, category } = req.query;
    const items = await getItemsFromDB({ skip, limit, category });
    res.json(items);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Individual resource endpoint
app.get('/items/:id', async (req, res) => {
  try {
    const item = await getItemFromDB(req.params.id);
    if (!item) {
      return res.status(404).json({ error: 'Item not found' });
    }
    res.json(item);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### POST - Create Resources

**Characteristics:**
- Not safe: Has side effects (creates resource)
- Not idempotent: Multiple requests create multiple resources
- Response should include `Location` header with new resource URI

**FastAPI Example:**

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    category: str
    description: Optional[str] = None

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, response: Response) -> dict:
    """Create a new item."""
    # Validate and create
    new_item = create_item_in_db(item)

    # Set Location header
    response.headers["Location"] = f"/items/{new_item.id}"

    return new_item
```

**Express.js Example:**

```javascript
app.use(express.json());

app.post('/items', async (req, res) => {
  try {
    const { name, price, category, description } = req.body;

    // Validate
    if (!name || !price || !category) {
      return res.status(400).json({
        error: 'Missing required fields: name, price, category'
      });
    }

    // Create resource
    const newItem = await createItemInDB({ name, price, category, description });

    // Set Location header and return 201
    res.location(`/items/${newItem.id}`)
       .status(201)
       .json(newItem);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### PUT - Replace Resource

**Characteristics:**
- Not safe: Has side effects
- Idempotent: Multiple identical requests have the same effect
- Replaces entire resource (all fields required)

**FastAPI Example:**

```python
class ItemUpdate(BaseModel):
    name: str
    price: float
    category: str
    description: str

@app.put("/items/{item_id}")
async def replace_item(item_id: int, item: ItemUpdate) -> dict:
    """Replace an entire item (all fields required)."""
    existing_item = get_item_from_db(item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Replace entire resource
    updated_item = replace_item_in_db(item_id, item)
    return updated_item
```

**Express.js Example:**

```javascript
app.put('/items/:id', async (req, res) => {
  try {
    const { name, price, category, description } = req.body;

    // All fields required for PUT
    if (!name || !price || !category || description === undefined) {
      return res.status(400).json({
        error: 'PUT requires all fields: name, price, category, description'
      });
    }

    const existingItem = await getItemFromDB(req.params.id);
    if (!existingItem) {
      return res.status(404).json({ error: 'Item not found' });
    }

    // Replace entire resource
    const updatedItem = await replaceItemInDB(req.params.id, req.body);
    res.json(updatedItem);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### PATCH - Partial Update

**Characteristics:**
- Not safe: Has side effects
- Idempotent: Multiple identical requests have the same effect
- Updates only specified fields (partial update)

**FastAPI Example:**

```python
class ItemPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None

@app.patch("/items/{item_id}")
async def update_item(item_id: int, item: ItemPatch) -> dict:
    """Partially update an item (only provided fields)."""
    existing_item = get_item_from_db(item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update only provided fields
    update_data = item.model_dump(exclude_unset=True)
    updated_item = update_item_in_db(item_id, update_data)
    return updated_item
```

**Express.js Example:**

```javascript
app.patch('/items/:id', async (req, res) => {
  try {
    const existingItem = await getItemFromDB(req.params.id);
    if (!existingItem) {
      return res.status(404).json({ error: 'Item not found' });
    }

    // Update only provided fields
    const updatedItem = await updateItemInDB(req.params.id, req.body);
    res.json(updatedItem);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### DELETE - Remove Resource

**Characteristics:**
- Not safe: Has side effects
- Idempotent: Multiple identical requests have the same effect
- Returns 204 No Content or 200 OK with response body

**FastAPI Example:**

```python
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Delete an item."""
    existing_item = get_item_from_db(item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    delete_item_from_db(item_id)
    return None  # 204 No Content

# Alternative: Return deleted resource
@app.delete("/items/{item_id}")
async def delete_item_with_response(item_id: int) -> dict:
    """Delete an item and return it."""
    existing_item = get_item_from_db(item_id)
    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    delete_item_from_db(item_id)
    return existing_item  # 200 OK with body
```

**Express.js Example:**

```javascript
// 204 No Content approach
app.delete('/items/:id', async (req, res) => {
  try {
    const existingItem = await getItemFromDB(req.params.id);
    if (!existingItem) {
      return res.status(404).json({ error: 'Item not found' });
    }

    await deleteItemFromDB(req.params.id);
    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 200 OK with response body approach
app.delete('/items/:id', async (req, res) => {
  try {
    const existingItem = await getItemFromDB(req.params.id);
    if (!existingItem) {
      return res.status(404).json({ error: 'Item not found' });
    }

    await deleteItemFromDB(req.params.id);
    res.json({ message: 'Item deleted successfully', item: existingItem });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## API Versioning Strategies

### Strategy 1: URI Versioning (Most Common)

Version in the URI path - clear, explicit, easy to understand.

**Pros:**
- Explicit and visible
- Easy to route to different code versions
- Browser-friendly
- Simple for documentation

**Cons:**
- Creates multiple endpoints
- Can lead to code duplication
- URLs change between versions

**FastAPI Implementation:**

```python
from fastapi import FastAPI, APIRouter

app = FastAPI()

# Version 1 router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users")
async def get_users_v1():
    return {"users": ["user1", "user2"], "version": "1.0"}

@v1_router.get("/users/{user_id}")
async def get_user_v1(user_id: int):
    return {"id": user_id, "name": "John", "version": "1.0"}

# Version 2 router
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users")
async def get_users_v2(limit: int = 10, offset: int = 0):
    """V2 adds pagination"""
    return {
        "users": ["user1", "user2"],
        "pagination": {"limit": limit, "offset": offset},
        "version": "2.0"
    }

@v2_router.get("/users/{user_id}")
async def get_user_v2(user_id: int):
    """V2 returns more fields"""
    return {
        "id": user_id,
        "name": "John",
        "email": "john@example.com",
        "created_at": "2024-01-01",
        "version": "2.0"
    }

app.include_router(v1_router)
app.include_router(v2_router)
```

**Express.js Implementation:**

```javascript
const express = require('express');
const app = express();

// Version 1 routes
const v1Router = express.Router();

v1Router.get('/users', (req, res) => {
  res.json({ users: ['user1', 'user2'], version: '1.0' });
});

v1Router.get('/users/:id', (req, res) => {
  res.json({ id: req.params.id, name: 'John', version: '1.0' });
});

// Version 2 routes
const v2Router = express.Router();

v2Router.get('/users', (req, res) => {
  const { limit = 10, offset = 0 } = req.query;
  res.json({
    users: ['user1', 'user2'],
    pagination: { limit, offset },
    version: '2.0'
  });
});

v2Router.get('/users/:id', (req, res) => {
  res.json({
    id: req.params.id,
    name: 'John',
    email: 'john@example.com',
    created_at: '2024-01-01',
    version: '2.0'
  });
});

app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);
```

### Strategy 2: Header Versioning

Version specified in custom header or Accept header.

**Pros:**
- Clean URIs
- No URL pollution
- More "RESTful" (resources have single URI)

**Cons:**
- Less visible
- Harder to test in browser
- More complex routing logic

**FastAPI Implementation:**

```python
from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/users")
async def get_users(api_version: str = Header(default="1.0", alias="X-API-Version")):
    """Handle multiple versions based on header"""
    if api_version == "1.0":
        return {"users": ["user1", "user2"], "version": "1.0"}
    elif api_version == "2.0":
        return {
            "users": ["user1", "user2"],
            "pagination": {"limit": 10, "offset": 0},
            "version": "2.0"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {api_version}"
        )

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    api_version: str = Header(default="1.0", alias="X-API-Version")
):
    """User endpoint with version handling"""
    if api_version == "1.0":
        return {"id": user_id, "name": "John", "version": "1.0"}
    elif api_version == "2.0":
        return {
            "id": user_id,
            "name": "John",
            "email": "john@example.com",
            "created_at": "2024-01-01",
            "version": "2.0"
        }
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported API version: {api_version}"
        )
```

**Express.js Implementation:**

```javascript
app.get('/users', (req, res) => {
  const version = req.get('X-API-Version') || '1.0';

  if (version === '1.0') {
    res.json({ users: ['user1', 'user2'], version: '1.0' });
  } else if (version === '2.0') {
    res.json({
      users: ['user1', 'user2'],
      pagination: { limit: 10, offset: 0 },
      version: '2.0'
    });
  } else {
    res.status(400).json({ error: `Unsupported API version: ${version}` });
  }
});

app.get('/users/:id', (req, res) => {
  const version = req.get('X-API-Version') || '1.0';

  if (version === '1.0') {
    res.json({ id: req.params.id, name: 'John', version: '1.0' });
  } else if (version === '2.0') {
    res.json({
      id: req.params.id,
      name: 'John',
      email: 'john@example.com',
      created_at: '2024-01-01',
      version: '2.0'
    });
  } else {
    res.status(400).json({ error: `Unsupported API version: ${version}` });
  }
});
```

### Strategy 3: Content Negotiation (Accept Header)

Version specified in Accept header with custom media types.

**FastAPI Implementation:**

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.get("/users")
async def get_users(request: Request):
    """Handle versioning via Accept header"""
    accept = request.headers.get("accept", "application/vnd.api.v1+json")

    if "vnd.api.v1+json" in accept:
        return {"users": ["user1", "user2"], "version": "1.0"}
    elif "vnd.api.v2+json" in accept:
        return {
            "users": ["user1", "user2"],
            "pagination": {"limit": 10, "offset": 0},
            "version": "2.0"
        }
    else:
        raise HTTPException(
            status_code=406,
            detail="Not Acceptable: Unsupported media type"
        )
```

**Express.js Implementation:**

```javascript
app.get('/users', (req, res) => {
  const accept = req.get('Accept') || 'application/vnd.api.v1+json';

  if (accept.includes('vnd.api.v1+json')) {
    res.type('application/vnd.api.v1+json')
       .json({ users: ['user1', 'user2'], version: '1.0' });
  } else if (accept.includes('vnd.api.v2+json')) {
    res.type('application/vnd.api.v2+json')
       .json({
         users: ['user1', 'user2'],
         pagination: { limit: 10, offset: 0 },
         version: '2.0'
       });
  } else {
    res.status(406).json({ error: 'Not Acceptable: Unsupported media type' });
  }
});
```

### Strategy 4: Query Parameter Versioning

Version as query parameter (least recommended).

```
GET /users?version=2.0
GET /users/123?v=2
```

**Cons:**
- Mixes versioning with filtering
- Harder to cache
- Less clear separation of concerns

## Pagination Patterns

### Pattern 1: Offset-Based Pagination (Traditional)

Simple but can have performance issues with large datasets.

**FastAPI Implementation:**

```python
from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    limit: int
    offset: int
    has_more: bool

@app.get("/items", response_model=PaginatedResponse)
async def list_items(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Offset-based pagination"""
    # Get total count
    total = count_items_in_db()

    # Get paginated items
    items = get_items_from_db(limit=limit, offset=offset)

    # Check if there are more items
    has_more = (offset + limit) < total

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": has_more
    }
```

**Express.js Implementation:**

```javascript
app.get('/items', async (req, res) => {
  try {
    const limit = Math.min(parseInt(req.query.limit) || 10, 100);
    const offset = parseInt(req.query.offset) || 0;

    const total = await countItemsInDB();
    const items = await getItemsFromDB({ limit, offset });
    const hasMore = (offset + limit) < total;

    res.json({
      items,
      total,
      limit,
      offset,
      has_more: hasMore
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### Pattern 2: Cursor-Based Pagination (Recommended for Large Datasets)

More efficient for large datasets, prevents issues with data changes during pagination.

**FastAPI Implementation:**

```python
from typing import Optional

class CursorPaginatedResponse(BaseModel):
    items: List[dict]
    next_cursor: Optional[str] = None
    has_more: bool

@app.get("/items", response_model=CursorPaginatedResponse)
async def list_items_cursor(
    limit: int = Query(default=10, ge=1, le=100),
    cursor: Optional[str] = None
):
    """Cursor-based pagination"""
    # Get items after cursor
    items = get_items_after_cursor(cursor=cursor, limit=limit + 1)

    # Check if there are more items
    has_more = len(items) > limit

    # Get next cursor from last item
    next_cursor = None
    if has_more:
        items = items[:limit]  # Remove extra item
        next_cursor = items[-1]["id"]  # Use last item ID as cursor

    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more
    }
```

**Express.js Implementation:**

```javascript
app.get('/items', async (req, res) => {
  try {
    const limit = Math.min(parseInt(req.query.limit) || 10, 100);
    const cursor = req.query.cursor || null;

    // Get one extra item to check if there are more
    const items = await getItemsAfterCursor({ cursor, limit: limit + 1 });

    const hasMore = items.length > limit;
    let nextCursor = null;

    if (hasMore) {
      items.pop(); // Remove extra item
      nextCursor = items[items.length - 1].id; // Last item ID as cursor
    }

    res.json({
      items,
      next_cursor: nextCursor,
      has_more: hasMore
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### Pattern 3: Page-Based Pagination

User-friendly for UIs with page numbers.

**FastAPI Implementation:**

```python
class PagePaginatedResponse(BaseModel):
    items: List[dict]
    page: int
    page_size: int
    total_pages: int
    total_items: int

@app.get("/items", response_model=PagePaginatedResponse)
async def list_items_pages(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100)
):
    """Page-based pagination"""
    # Calculate offset
    offset = (page - 1) * page_size

    # Get total count and items
    total_items = count_items_in_db()
    items = get_items_from_db(limit=page_size, offset=offset)

    # Calculate total pages
    total_pages = (total_items + page_size - 1) // page_size

    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_items": total_items
    }
```

**Express.js Implementation:**

```javascript
app.get('/items', async (req, res) => {
  try {
    const page = Math.max(parseInt(req.query.page) || 1, 1);
    const pageSize = Math.min(parseInt(req.query.page_size) || 10, 100);

    const offset = (page - 1) * pageSize;

    const totalItems = await countItemsInDB();
    const items = await getItemsFromDB({ limit: pageSize, offset });
    const totalPages = Math.ceil(totalItems / pageSize);

    res.json({
      items,
      page,
      page_size: pageSize,
      total_pages: totalPages,
      total_items: totalItems
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## Filtering and Sorting

### Advanced Filtering

**FastAPI Implementation:**

```python
from enum import Enum
from typing import Optional, List

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/products")
async def list_products(
    # Filtering
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    tags: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    # Sorting
    sort_by: Optional[str] = Query(default="created_at"),
    order: SortOrder = SortOrder.desc,
    # Pagination
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Advanced filtering and sorting"""
    filters = {
        "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "in_stock": in_stock,
        "tags": tags,
        "search": search
    }

    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}

    # Query database
    products = query_products(
        filters=filters,
        sort_by=sort_by,
        order=order.value,
        limit=limit,
        offset=offset
    )

    return {
        "products": products,
        "filters": filters,
        "sort": {"by": sort_by, "order": order.value},
        "pagination": {"limit": limit, "offset": offset}
    }
```

**Express.js Implementation:**

```javascript
app.get('/products', async (req, res) => {
  try {
    const {
      category,
      min_price,
      max_price,
      in_stock,
      tags,
      search,
      sort_by = 'created_at',
      order = 'desc',
      limit = 10,
      offset = 0
    } = req.query;

    // Build filters
    const filters = {};
    if (category) filters.category = category;
    if (min_price) filters.min_price = parseFloat(min_price);
    if (max_price) filters.max_price = parseFloat(max_price);
    if (in_stock !== undefined) filters.in_stock = in_stock === 'true';
    if (tags) filters.tags = Array.isArray(tags) ? tags : [tags];
    if (search) filters.search = search;

    // Query database
    const products = await queryProducts({
      filters,
      sortBy: sort_by,
      order,
      limit: Math.min(parseInt(limit), 100),
      offset: parseInt(offset)
    });

    res.json({
      products,
      filters,
      sort: { by: sort_by, order },
      pagination: { limit, offset }
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## Error Handling Best Practices

### Consistent Error Response Format

**Standard Error Response Structure:**

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested user was not found",
    "details": {
      "user_id": "123",
      "resource": "user"
    },
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### HTTP Status Codes

**Success Codes:**
- `200 OK`: Successful GET, PUT, PATCH, DELETE with response
- `201 Created`: Successful POST creating a resource
- `202 Accepted`: Request accepted for async processing
- `204 No Content`: Successful DELETE with no response body

**Client Error Codes:**
- `400 Bad Request`: Invalid request syntax or validation error
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource doesn't exist
- `405 Method Not Allowed`: HTTP method not supported
- `409 Conflict`: Request conflicts with current state
- `422 Unprocessable Entity`: Validation failed
- `429 Too Many Requests`: Rate limit exceeded

**Server Error Codes:**
- `500 Internal Server Error`: Generic server error
- `502 Bad Gateway`: Invalid response from upstream server
- `503 Service Unavailable`: Server temporarily unavailable
- `504 Gateway Timeout`: Upstream server timeout

### FastAPI Error Handling

```python
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

app = FastAPI()

# Custom exception
class ResourceNotFoundError(Exception):
    def __init__(self, resource: str, resource_id: str):
        self.resource = resource
        self.resource_id = resource_id

# Global exception handler
@app.exception_handler(ResourceNotFoundError)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": f"The requested {exc.resource} was not found",
                "details": {
                    "resource": exc.resource,
                    "resource_id": exc.resource_id
                },
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
    )

# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
    )

# Using exceptions
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    if not user:
        raise ResourceNotFoundError("user", str(user_id))
    return user

# Manual error responses
@app.post("/users")
async def create_user(email: str):
    if user_exists(email):
        raise HTTPException(
            status_code=409,
            detail={
                "code": "DUPLICATE_EMAIL",
                "message": "A user with this email already exists",
                "details": {"email": email}
            }
        )
    return create_user_in_db(email)
```

### Express.js Error Handling

```javascript
const express = require('express');
const app = express();

app.use(express.json());

// Custom error class
class ResourceNotFoundError extends Error {
  constructor(resource, resourceId) {
    super(`${resource} not found`);
    this.name = 'ResourceNotFoundError';
    this.resource = resource;
    this.resourceId = resourceId;
    this.statusCode = 404;
  }
}

class ValidationError extends Error {
  constructor(message, details) {
    super(message);
    this.name = 'ValidationError';
    this.details = details;
    this.statusCode = 422;
  }
}

// Routes
app.get('/users/:id', async (req, res, next) => {
  try {
    const user = await getUserFromDB(req.params.id);
    if (!user) {
      throw new ResourceNotFoundError('user', req.params.id);
    }
    res.json(user);
  } catch (error) {
    next(error);
  }
});

app.post('/users', async (req, res, next) => {
  try {
    const { email } = req.body;

    if (!email) {
      throw new ValidationError('Validation failed', {
        field: 'email',
        message: 'Email is required'
      });
    }

    const userExists = await checkUserExists(email);
    if (userExists) {
      const error = new Error('Duplicate email');
      error.statusCode = 409;
      error.code = 'DUPLICATE_EMAIL';
      error.details = { email };
      throw error;
    }

    const newUser = await createUserInDB(email);
    res.status(201).json(newUser);
  } catch (error) {
    next(error);
  }
});

// Global error handler (must be last)
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const code = err.code || err.name || 'INTERNAL_SERVER_ERROR';

  const errorResponse = {
    error: {
      code,
      message: err.message,
      timestamp: new Date().toISOString()
    }
  };

  // Add details if available
  if (err.details) {
    errorResponse.error.details = err.details;
  } else if (err.resource && err.resourceId) {
    errorResponse.error.details = {
      resource: err.resource,
      resource_id: err.resourceId
    };
  }

  // Log error for debugging (don't expose in production)
  if (process.env.NODE_ENV !== 'production') {
    errorResponse.error.stack = err.stack;
  }

  res.status(statusCode).json(errorResponse);
});
```

## HATEOAS and Hypermedia

### What is HATEOAS?

HATEOAS (Hypermedia as the Engine of Application State) means including links to related resources in API responses.

**Benefits:**
- Self-documenting API
- Client doesn't need to construct URLs
- Easier API evolution
- Better discoverability

### FastAPI HATEOAS Implementation

```python
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Link(BaseModel):
    rel: str
    href: str
    method: str = "GET"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    links: List[Link]

class UserListResponse(BaseModel):
    users: List[UserResponse]
    links: List[Link]

app = FastAPI()

def build_user_links(user_id: int, base_url: str = "http://api.example.com") -> List[Link]:
    """Build HATEOAS links for a user"""
    return [
        Link(rel="self", href=f"{base_url}/users/{user_id}", method="GET"),
        Link(rel="update", href=f"{base_url}/users/{user_id}", method="PUT"),
        Link(rel="delete", href=f"{base_url}/users/{user_id}", method="DELETE"),
        Link(rel="posts", href=f"{base_url}/users/{user_id}/posts", method="GET"),
        Link(rel="create_post", href=f"{base_url}/users/{user_id}/posts", method="POST")
    ]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user with HATEOAS links"""
    user = get_user_from_db(user_id)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "links": build_user_links(user.id)
    }

@app.get("/users", response_model=UserListResponse)
async def list_users():
    """List users with HATEOAS links"""
    users = get_users_from_db()

    users_with_links = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "links": build_user_links(user.id)
        }
        for user in users
    ]

    collection_links = [
        Link(rel="self", href="http://api.example.com/users", method="GET"),
        Link(rel="create", href="http://api.example.com/users", method="POST")
    ]

    return {
        "users": users_with_links,
        "links": collection_links
    }
```

### Express.js HATEOAS Implementation

```javascript
app.get('/users/:id', async (req, res) => {
  try {
    const user = await getUserFromDB(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const baseUrl = `${req.protocol}://${req.get('host')}`;

    res.json({
      id: user.id,
      name: user.name,
      email: user.email,
      _links: {
        self: { href: `${baseUrl}/users/${user.id}`, method: 'GET' },
        update: { href: `${baseUrl}/users/${user.id}`, method: 'PUT' },
        delete: { href: `${baseUrl}/users/${user.id}`, method: 'DELETE' },
        posts: { href: `${baseUrl}/users/${user.id}/posts`, method: 'GET' },
        create_post: { href: `${baseUrl}/users/${user.id}/posts`, method: 'POST' }
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/users', async (req, res) => {
  try {
    const users = await getUsersFromDB();
    const baseUrl = `${req.protocol}://${req.get('host')}`;

    const usersWithLinks = users.map(user => ({
      id: user.id,
      name: user.name,
      email: user.email,
      _links: {
        self: { href: `${baseUrl}/users/${user.id}`, method: 'GET' },
        update: { href: `${baseUrl}/users/${user.id}`, method: 'PUT' },
        delete: { href: `${baseUrl}/users/${user.id}`, method: 'DELETE' }
      }
    }));

    res.json({
      users: usersWithLinks,
      _links: {
        self: { href: `${baseUrl}/users`, method: 'GET' },
        create: { href: `${baseUrl}/users`, method: 'POST' }
      }
    });
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

## Performance Optimization

### Caching with ETags

**FastAPI Implementation:**

```python
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import hashlib

app = FastAPI()

def generate_etag(data: dict) -> str:
    """Generate ETag from response data"""
    content = str(data).encode('utf-8')
    return hashlib.md5(content).hexdigest()

@app.get("/users/{user_id}")
async def get_user_cached(user_id: int, request: Request):
    """Get user with ETag caching"""
    user = get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate ETag
    etag = generate_etag(user)

    # Check If-None-Match header
    if_none_match = request.headers.get("if-none-match")
    if if_none_match == etag:
        return Response(status_code=304)  # Not Modified

    # Return with ETag header
    return JSONResponse(
        content=user,
        headers={"ETag": etag, "Cache-Control": "max-age=300"}
    )
```

**Express.js Implementation:**

```javascript
const crypto = require('crypto');

function generateETag(data) {
  const content = JSON.stringify(data);
  return crypto.createHash('md5').update(content).digest('hex');
}

app.get('/users/:id', async (req, res) => {
  try {
    const user = await getUserFromDB(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    const etag = generateETag(user);

    // Check If-None-Match header
    if (req.get('If-None-Match') === etag) {
      return res.status(304).send(); // Not Modified
    }

    res.set('ETag', etag)
       .set('Cache-Control', 'max-age=300')
       .json(user);
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

### Rate Limiting

**Express.js Implementation:**

```javascript
const rateLimit = require('express-rate-limit');

// Create rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: {
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later'
    }
  },
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false
});

// Apply to all routes
app.use('/api/', apiLimiter);

// Or create specific limiters
const createAccountLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 requests per hour
  message: 'Too many accounts created, please try again later'
});

app.post('/api/users', createAccountLimiter, async (req, res) => {
  // Create user
});
```

### Compression

**FastAPI Implementation:**

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Add compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/large-data")
async def get_large_data():
    """This response will be compressed if > 1000 bytes"""
    return {"data": [{"id": i, "value": f"item_{i}"} for i in range(1000)]}
```

**Express.js Implementation:**

```javascript
const compression = require('compression');

// Add compression middleware
app.use(compression({
  threshold: 1024, // Only compress responses > 1KB
  level: 6 // Compression level (0-9)
}));

app.get('/large-data', (req, res) => {
  const data = Array.from({ length: 1000 }, (_, i) => ({
    id: i,
    value: `item_${i}`
  }));
  res.json({ data });
});
```

## Security Best Practices

### Authentication Patterns

**JWT Authentication in FastAPI:**

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

@app.post("/login")
async def login(email: str, password: str):
    """Login and get access token"""
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
async def get_current_user(payload: dict = Depends(verify_token)):
    """Protected endpoint - requires authentication"""
    user_id = payload.get("user_id")
    user = get_user_from_db(user_id)
    return user
```

**JWT Authentication in Express.js:**

```javascript
const jwt = require('jsonwebtoken');
const express = require('express');
const app = express();

const SECRET_KEY = 'your-secret-key';

function createAccessToken(data, expiresIn = '15m') {
  return jwt.sign(data, SECRET_KEY, { expiresIn });
}

function verifyToken(req, res, next) {
  const authHeader = req.get('Authorization');

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }

  const token = authHeader.substring(7);

  try {
    const payload = jwt.verify(token, SECRET_KEY);
    req.user = payload;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token has expired' });
    }
    return res.status(401).json({ error: 'Invalid token' });
  }
}

app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await authenticateUser(email, password);
  if (!user) {
    return res.status(401).json({ error: 'Incorrect email or password' });
  }

  const accessToken = createAccessToken({
    sub: user.email,
    user_id: user.id
  });

  res.json({ access_token: accessToken, token_type: 'bearer' });
});

app.get('/users/me', verifyToken, async (req, res) => {
  const user = await getUserFromDB(req.user.user_id);
  res.json(user);
});
```

### Input Validation and Sanitization

**FastAPI Validation:**

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8)
    age: Optional[int] = Field(None, ge=0, le=150)

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

@app.post("/users")
async def create_user(user: UserCreate):
    """Automatically validates input"""
    # Input is already validated by Pydantic
    hashed_password = hash_password(user.password)
    new_user = create_user_in_db(user.email, user.username, hashed_password)
    return new_user
```

## API Documentation

### OpenAPI/Swagger with FastAPI

FastAPI automatically generates OpenAPI documentation:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="My API",
    description="Comprehensive API for managing resources",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

class Item(BaseModel):
    """Item model with rich documentation"""
    name: str = Field(..., description="The name of the item", example="Widget")
    price: float = Field(..., description="Price in USD", example=19.99, gt=0)
    description: str = Field(None, description="Optional item description")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Super Widget",
                    "price": 29.99,
                    "description": "An amazing widget"
                }
            ]
        }
    }

@app.post(
    "/items",
    response_model=Item,
    status_code=201,
    summary="Create a new item",
    description="Create a new item with name, price, and optional description",
    response_description="The created item",
    tags=["items"]
)
async def create_item(item: Item):
    """
    Create a new item with all the information:

    - **name**: The item name (required)
    - **price**: The item price in USD (required, must be positive)
    - **description**: Optional description of the item
    """
    return item
```

## Best Practices Summary

### API Design Principles

1. **Use nouns for resources, not verbs**
2. **Use plural nouns for collections**
3. **Use HTTP methods correctly** (GET, POST, PUT, PATCH, DELETE)
4. **Use proper HTTP status codes**
5. **Version your API** (URI versioning recommended)
6. **Support pagination** for collections
7. **Allow filtering and sorting** with query parameters
8. **Return consistent error responses**
9. **Use HATEOAS** for better discoverability
10. **Document your API** with OpenAPI/Swagger

### Security Principles

1. **Always use HTTPS** in production
2. **Implement authentication** (JWT, OAuth, API keys)
3. **Validate all inputs** thoroughly
4. **Use rate limiting** to prevent abuse
5. **Sanitize outputs** to prevent XSS
6. **Implement CORS** correctly
7. **Use security headers** (CSP, X-Frame-Options, etc.)
8. **Log security events** for monitoring
9. **Keep dependencies updated**
10. **Never expose sensitive data** in responses

### Performance Principles

1. **Use caching** (ETags, Cache-Control headers)
2. **Implement compression** for large responses
3. **Use pagination** for large datasets
4. **Optimize database queries** (indexes, N+1 prevention)
5. **Use async/await** for I/O operations
6. **Implement connection pooling**
7. **Monitor API performance** (response times, error rates)
8. **Use CDNs** for static content
9. **Implement proper logging** without blocking
10. **Load test** your API regularly

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: API Design, Backend Development, REST Architecture
**Compatible With**: FastAPI, Express.js, Node.js, Python, HTTP Frameworks
