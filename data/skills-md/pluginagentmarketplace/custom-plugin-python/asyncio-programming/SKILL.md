---
name: Asyncio Programming
description: Master asynchronous programming with asyncio, async/await, concurrent operations, and async frameworks
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 05-async-concurrency
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: task_completion_rate
---

# Asyncio Programming

## Overview

Master asynchronous programming in Python with asyncio. Learn to write concurrent code that efficiently handles I/O-bound operations, build async web applications, and understand the async/await paradigm.

## Learning Objectives

- Understand asynchronous programming concepts
- Write async functions with async/await syntax
- Manage concurrent operations with asyncio
- Build async web applications
- Handle async I/O operations efficiently
- Debug and test async code

## Core Topics

### 1. Async/Await Basics
- Understanding coroutines
- async/await syntax
- Event loop fundamentals
- Running async functions
- Async vs sync execution
- Common pitfalls

**Code Example:**
```python
import asyncio
import time

# Synchronous version (slow)
def fetch_data_sync(url):
    print(f"Fetching {url}...")
    time.sleep(2)  # Simulating network delay
    return f"Data from {url}"

def main_sync():
    urls = ['url1', 'url2', 'url3']
    results = []
    for url in urls:
        data = fetch_data_sync(url)
        results.append(data)
    return results

# Takes 6 seconds (2 * 3)
start = time.time()
main_sync()
print(f"Sync took: {time.time() - start:.2f}s")

# Asynchronous version (fast)
async def fetch_data_async(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(2)  # Non-blocking sleep
    return f"Data from {url}"

async def main_async():
    urls = ['url1', 'url2', 'url3']
    # Create tasks and run concurrently
    tasks = [fetch_data_async(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Takes 2 seconds (concurrent execution)
start = time.time()
asyncio.run(main_async())
print(f"Async took: {time.time() - start:.2f}s")
```

### 2. Asyncio Tasks & Coroutines
- Creating and managing tasks
- asyncio.gather() vs asyncio.wait()
- Task cancellation
- Task groups (Python 3.11+)
- Exception handling in tasks
- Timeouts

**Code Example:**
```python
import asyncio

async def process_item(item_id, delay):
    print(f"Processing item {item_id}")
    await asyncio.sleep(delay)
    if item_id == 3:
        raise ValueError(f"Item {item_id} failed!")
    return f"Result {item_id}"

async def main():
    # Method 1: gather (returns results in order)
    tasks = [
        process_item(1, 1),
        process_item(2, 2),
        process_item(3, 1),
    ]
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {i} failed: {result}")
            else:
                print(f"Task {i} result: {result}")
    except Exception as e:
        print(f"Error: {e}")

    # Method 2: wait (returns done/pending sets)
    tasks = [
        asyncio.create_task(process_item(i, i))
        for i in range(1, 4)
    ]
    done, pending = await asyncio.wait(tasks, timeout=2.5)

    print(f"Completed: {len(done)}, Pending: {len(pending)}")

    # Cancel pending tasks
    for task in pending:
        task.cancel()

    # Method 3: Task groups (Python 3.11+)
    async with asyncio.TaskGroup() as tg:
        for i in range(1, 4):
            tg.create_task(process_item(i, 1))
    # All tasks completed or exception raised

asyncio.run(main())
```

### 3. Async I/O Operations
- Async file operations (aiofiles)
- Async HTTP requests (aiohttp)
- Async database operations (asyncpg, motor)
- Async messaging (aio-pika)
- Streams and protocols

**Code Example:**
```python
import asyncio
import aiohttp
import aiofiles
from typing import List

# Async HTTP requests
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_multiple_urls(urls: List[str]):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Async file operations
async def read_file_async(filepath):
    async with aiofiles.open(filepath, 'r') as f:
        content = await f.read()
        return content

async def write_file_async(filepath, content):
    async with aiofiles.open(filepath, 'w') as f:
        await f.write(content)

# Async database operations (example with asyncpg)
import asyncpg

async def fetch_users():
    conn = await asyncpg.connect(
        user='user',
        password='password',
        database='mydb',
        host='localhost'
    )
    try:
        rows = await conn.fetch('SELECT * FROM users')
        return rows
    finally:
        await conn.close()

# Usage
async def main():
    # Fetch URLs concurrently
    urls = [
        'https://api.example.com/data1',
        'https://api.example.com/data2',
        'https://api.example.com/data3',
    ]
    results = await fetch_multiple_urls(urls)

    # Read/write files
    content = await read_file_async('input.txt')
    await write_file_async('output.txt', content.upper())

    # Database operations
    users = await fetch_users()
    print(f"Found {len(users)} users")

asyncio.run(main())
```

### 4. Async Web Frameworks
- FastAPI async routes
- aiohttp web server
- WebSocket handling
- Background tasks
- Middleware and dependencies

**Code Example:**
```python
# FastAPI async example
from fastapi import FastAPI, BackgroundTasks
import asyncio

app = FastAPI()

# Async route
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Async database call
    user = await fetch_user_from_db(user_id)
    return user

# Background task
async def send_notification(email: str, message: str):
    await asyncio.sleep(2)  # Simulate email sending
    print(f"Sent email to {email}: {message}")

@app.post("/orders/")
async def create_order(order_data: dict, background_tasks: BackgroundTasks):
    # Process order synchronously
    order_id = save_order(order_data)

    # Send notification in background
    background_tasks.add_task(
        send_notification,
        order_data['customer_email'],
        f"Order #{order_id} created"
    )

    return {"order_id": order_id}

# aiohttp web server
from aiohttp import web

async def handle_request(request):
    name = request.match_info.get('name', 'Anonymous')
    await asyncio.sleep(1)  # Async operation
    return web.json_response({'message': f'Hello {name}'})

app = web.Application()
app.add_routes([web.get('/{name}', handle_request)])

# WebSocket example
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            await ws.send_str(f"Echo: {msg.data}")
        elif msg.type == web.WSMsgType.ERROR:
            print(f'Error: {ws.exception()}')

    return ws

app.add_routes([web.get('/ws', websocket_handler)])
```

## Hands-On Practice

### Project 1: Async Web Scraper
Build a concurrent web scraper with rate limiting.

**Requirements:**
- Scrape multiple websites concurrently
- Implement rate limiting
- Handle errors gracefully
- Save results to async database
- Progress tracking
- Retry failed requests

**Key Skills:** aiohttp, async I/O, error handling

### Project 2: Real-time Chat Server
Create a WebSocket-based chat application.

**Requirements:**
- WebSocket server with aiohttp
- Multiple chat rooms
- User authentication
- Message broadcasting
- Connection management
- Message history persistence

**Key Skills:** WebSockets, async server, state management

### Project 3: Async Task Queue
Build a distributed task processing system.

**Requirements:**
- Task queue with Redis/RabbitMQ
- Worker pool management
- Task prioritization
- Result caching
- Progress monitoring
- Graceful shutdown

**Key Skills:** Message queues, concurrent workers, cleanup

## Assessment Criteria

- [ ] Understand async/await semantics
- [ ] Write efficient concurrent code
- [ ] Handle async exceptions properly
- [ ] Use asyncio tasks effectively
- [ ] Build async web applications
- [ ] Debug async code
- [ ] Manage async resources (cleanup)

## Resources

### Official Documentation
- [asyncio Docs](https://docs.python.org/3/library/asyncio.html) - Official documentation
- [aiohttp](https://docs.aiohttp.org/) - Async HTTP client/server
- [FastAPI](https://fastapi.tiangolo.com/) - Modern async web framework

### Learning Platforms
- [Using Asyncio in Python](https://realpython.com/async-io-python/) - Real Python guide
- [Python Concurrency](https://learning.oreilly.com/library/view/using-asyncio-in/9781492075325/) - O'Reilly book
- [Asyncio Recipes](https://www.amazon.com/Python-Asyncio-Recipes-Caleb-Hattingh/dp/1484244001) - Practical examples

### Tools
- [aiohttp](https://docs.aiohttp.org/) - Async HTTP
- [aiofiles](https://github.com/Tinche/aiofiles) - Async file I/O
- [asyncpg](https://magicstack.github.io/asyncpg/) - Async PostgreSQL
- [aiodebug](https://github.com/mosquito/aiodebug) - Async debugging

## Next Steps

After mastering asyncio, explore:
- **Multiprocessing** - CPU-bound parallelism
- **Celery** - Distributed task queue
- **gRPC** - Async RPC framework
- **Kafka** - Async event streaming
