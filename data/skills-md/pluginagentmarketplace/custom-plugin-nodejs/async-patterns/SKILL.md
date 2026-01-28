---
name: async-patterns
description: Master asynchronous programming in Node.js with Promises, async/await, streams, and event-driven patterns for efficient non-blocking operations
sasmp_version: "1.3.0"
bonded_agent: 01-nodejs-fundamentals
bond_type: PRIMARY_BOND
---

# Async Programming Patterns Skill

Master asynchronous programming - the foundation of Node.js performance and scalability.

## Quick Start

Three pillars of async JavaScript:
1. **Callbacks** - Traditional pattern (error-first)
2. **Promises** - Modern chainable pattern
3. **Async/Await** - Synchronous-looking async code

## Core Patterns

### Callbacks → Promises → Async/Await Evolution
```javascript
// 1. Callbacks (old way)
fs.readFile('file.txt', (err, data) => {
  if (err) throw err;
  console.log(data);
});

// 2. Promises (better)
fs.promises.readFile('file.txt')
  .then(data => console.log(data))
  .catch(err => console.error(err));

// 3. Async/Await (modern)
async function readFile() {
  try {
    const data = await fs.promises.readFile('file.txt');
    console.log(data);
  } catch (err) {
    console.error(err);
  }
}
```

### Sequential vs Parallel
```javascript
// ❌ Slow: Sequential (300ms total)
async function slow() {
  const a = await fetch('/api/a'); // 100ms
  const b = await fetch('/api/b'); // 100ms
  const c = await fetch('/api/c'); // 100ms
  return [a, b, c];
}

// ✅ Fast: Parallel (100ms total)
async function fast() {
  const [a, b, c] = await Promise.all([
    fetch('/api/a'),
    fetch('/api/b'),
    fetch('/api/c')
  ]);
  return [a, b, c];
}
```

### Promise Methods
```javascript
// Promise.all - Wait for all (fails if one fails)
const [users, posts] = await Promise.all([getUsers(), getPosts()]);

// Promise.allSettled - Wait for all (never fails)
const results = await Promise.allSettled([fetch1(), fetch2(), fetch3()]);

// Promise.race - First to complete
const fastest = await Promise.race([server1(), server2()]);

// Promise.any - First to succeed
const result = await Promise.any([tryAPI1(), tryAPI2()]);
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Understand event loop
- ✅ Master callbacks
- ✅ Learn Promises basics
- ✅ Practice async/await

### Intermediate (3-4 weeks)
- ✅ Error handling patterns
- ✅ Sequential vs parallel execution
- ✅ Promise composition
- ✅ Event emitters

### Advanced (5-6 weeks)
- ✅ Streams and backpressure
- ✅ Concurrency control
- ✅ Circuit breakers
- ✅ Performance optimization

## Common Patterns

### Error Handling
```javascript
// Try/catch for async/await
async function safeOperation() {
  try {
    const result = await riskyOperation();
    return { success: true, data: result };
  } catch (error) {
    console.error('Operation failed:', error);
    return { success: false, error: error.message };
  }
}

// Process-level handlers
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason);
});
```

### Retry with Exponential Backoff
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

### Concurrency Limit
```javascript
async function batchProcess(items, concurrency = 5) {
  const results = [];
  for (let i = 0; i < items.length; i += concurrency) {
    const batch = items.slice(i, i + concurrency);
    const batchResults = await Promise.all(
      batch.map(item => processItem(item))
    );
    results.push(...batchResults);
  }
  return results;
}
```

## Streams
```javascript
const { pipeline } = require('stream');
const fs = require('fs');

// Efficient file processing
pipeline(
  fs.createReadStream('input.txt'),
  transformStream,
  fs.createWriteStream('output.txt'),
  (err) => {
    if (err) console.error('Pipeline failed:', err);
    else console.log('Pipeline succeeded');
  }
);
```

## Event Emitters
```javascript
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}
const emitter = new MyEmitter();

emitter.on('event', (data) => {
  console.log('Event fired:', data);
});

emitter.emit('event', { id: 123 });
```

## When to Use

Use async patterns when:
- Handling I/O operations (file, network, database)
- Building scalable Node.js applications
- Managing multiple concurrent operations
- Processing streams of data
- Creating event-driven architectures

## Related Skills
- Express REST API (async route handlers)
- Database Integration (async queries)
- Testing & Debugging (test async code)
- Performance Optimization (async performance)

## Resources
- [MDN Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [Node.js Async Guide](https://nodejs.dev/en/learn/asynchronous-flow-control/)
- [JavaScript.info Async](https://javascript.info/async)
