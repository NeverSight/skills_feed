---
name: debug:express
description: Debug Express.js and Node.js applications with systematic diagnostic techniques. This skill provides comprehensive guidance for troubleshooting middleware execution issues, routing problems, CORS errors, async error handling, memory leaks, and unhandled promise rejections. Covers DEBUG environment variable usage, Node Inspector with Chrome DevTools, VS Code debugging, Morgan request logging, and diagnostic middleware patterns. Includes four-phase debugging methodology and common error message reference.
---

# Express.js Debugging Guide

A systematic approach to debugging Express.js applications using proven techniques and tools.

## Common Error Patterns

### 1. Cannot GET /route (404 Errors)
**Symptoms:** Route returns 404, middleware not matching
**Common Causes:**
- Route not registered before catch-all handlers
- Missing leading slash in path
- Case sensitivity issues
- Router not mounted correctly

```javascript
// Wrong: catch-all before specific routes
app.use('*', notFoundHandler);
app.get('/api/users', getUsers); // Never reached

// Correct: specific routes before catch-all
app.get('/api/users', getUsers);
app.use('*', notFoundHandler);
```

### 2. Middleware Not Executing
**Symptoms:** Request hangs, next() not called, order issues
**Common Causes:**
- Forgetting to call `next()`
- Async middleware without proper error handling
- Wrong middleware order

```javascript
// Wrong: missing next()
app.use((req, res, next) => {
  console.log('Request received');
  // Hangs - next() never called
});

// Correct: always call next() or send response
app.use((req, res, next) => {
  console.log('Request received');
  next();
});

// Correct async middleware
app.use(async (req, res, next) => {
  try {
    await someAsyncOperation();
    next();
  } catch (err) {
    next(err); // Pass error to error handler
  }
});
```

### 3. CORS Errors
**Symptoms:** Browser blocks requests, preflight fails
**Common Causes:**
- CORS middleware placed after routes
- Missing OPTIONS handler
- Credentials not configured

```javascript
const cors = require('cors');

// Wrong: CORS after routes
app.get('/api/data', handler);
app.use(cors()); // Too late

// Correct: CORS before routes
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || '*',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.get('/api/data', handler);
```

### 4. Async Error Handling
**Symptoms:** Unhandled promise rejections, app crashes
**Common Causes:**
- Missing try/catch in async handlers
- Promises not caught
- No global error handler

```javascript
// Wrong: unhandled async error
app.get('/users', async (req, res) => {
  const users = await User.findAll(); // Throws, crashes app
  res.json(users);
});

// Correct: wrap async handlers
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get('/users', asyncHandler(async (req, res) => {
  const users = await User.findAll();
  res.json(users);
}));

// Global error handler (must be last)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message
  });
});
```

### 5. Memory Leaks
**Symptoms:** Heap growing, OOM errors, slow responses over time
**Common Causes:**
- Unclosed database connections
- Event listeners not removed
- Large objects in closures
- Global caches without limits

```javascript
// Wrong: unbounded cache
const cache = {};
app.get('/data/:id', (req, res) => {
  cache[req.params.id] = largeObject; // Memory leak
});

// Correct: use LRU cache with limits
const LRU = require('lru-cache');
const cache = new LRU({ max: 500, ttl: 1000 * 60 * 5 });

// Check for leaks
node --inspect --expose-gc app.js
// Use Chrome DevTools Memory tab
```

### 6. Unhandled Promise Rejections
**Symptoms:** Warnings in console, silent failures
**Setup global handlers:**

```javascript
// Add to app entry point
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  // Log to error tracking service
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
  // Graceful shutdown
  process.exit(1);
});
```

## Debugging Tools

### 1. DEBUG Environment Variable
The most powerful built-in debugging tool for Express.

```bash
# See all Express internal logs
DEBUG=express:* node app.js

# Specific areas only
DEBUG=express:router node app.js
DEBUG=express:application,express:router node app.js

# Multiple packages
DEBUG=express:*,body-parser:* node app.js

# Your own debug statements
DEBUG=myapp:* node app.js
```

```javascript
// In your code
const debug = require('debug')('myapp:server');
debug('Server starting on port %d', port);
```

### 2. Node Inspector (--inspect)
Start with Chrome DevTools support:

```bash
# Start with inspector
node --inspect app.js

# Break on first line
node --inspect-brk app.js

# Specific port
node --inspect=0.0.0.0:9229 app.js
```

Open `chrome://inspect` in Chrome, click "Open dedicated DevTools for Node".

### 3. VS Code Debugger
Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Express",
      "program": "${workspaceFolder}/app.js",
      "env": {
        "DEBUG": "express:*",
        "NODE_ENV": "development"
      },
      "console": "integratedTerminal"
    },
    {
      "type": "node",
      "request": "attach",
      "name": "Attach to Process",
      "port": 9229
    }
  ]
}
```

### 4. Morgan Logger
HTTP request logging middleware:

```javascript
const morgan = require('morgan');

// Development: colored, concise
app.use(morgan('dev'));

// Production: Apache combined format
app.use(morgan('combined'));

// Custom format with response time
app.use(morgan(':method :url :status :response-time ms - :res[content-length]'));

// Log to file
const fs = require('fs');
const accessLogStream = fs.createWriteStream('./access.log', { flags: 'a' });
app.use(morgan('combined', { stream: accessLogStream }));
```

### 5. ndb Debugger
Enhanced debugging experience:

```bash
npm install -g ndb
ndb node app.js
```

Features: Better UI, async stack traces, blackbox scripts, profile recording.

### 6. ESLint for Prevention
Catch errors before runtime:

```bash
npm install eslint eslint-plugin-node --save-dev
npx eslint --init
```

```json
{
  "extends": ["eslint:recommended", "plugin:node/recommended"],
  "rules": {
    "no-unused-vars": "error",
    "no-undef": "error",
    "node/no-missing-require": "error"
  }
}
```

## The Four Phases (Express-specific)

### Phase 1: Reproduce and Isolate
1. **Get exact error message** - Check terminal, browser console, network tab
2. **Identify the route** - Which endpoint is failing?
3. **Check request details** - Method, headers, body, query params
4. **Minimal reproduction** - Can you trigger with curl/Postman?

```bash
# Test endpoint directly
curl -v http://localhost:3000/api/users
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"test"}' http://localhost:3000/api/users
```

### Phase 2: Gather Information
1. **Enable DEBUG logging**
   ```bash
   DEBUG=express:* node app.js
   ```

2. **Add strategic logging**
   ```javascript
   app.use((req, res, next) => {
     console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
     console.log('Headers:', req.headers);
     console.log('Body:', req.body);
     next();
   });
   ```

3. **Check middleware order**
   ```javascript
   app._router.stack.forEach((r, i) => {
     if (r.route) {
       console.log(`${i}: Route ${r.route.path}`);
     } else if (r.name) {
       console.log(`${i}: Middleware ${r.name}`);
     }
   });
   ```

4. **Inspect with breakpoints**
   - Set breakpoint at route handler entry
   - Step through middleware chain
   - Inspect req/res objects

### Phase 3: Analyze and Hypothesize
1. **Check the stack trace** - Follow the call stack from error
2. **Verify assumptions**
   - Is the route registered?
   - Is middleware in correct order?
   - Are environment variables set?
   - Is database connected?

3. **Common culprits checklist:**
   - [ ] Body parser before routes?
   - [ ] CORS before routes?
   - [ ] Auth middleware applied?
   - [ ] Error handler at the end?
   - [ ] Async errors caught?

### Phase 4: Fix and Verify
1. **Make one change at a time**
2. **Test the specific failing case**
3. **Run full test suite**
4. **Check for regressions**

```bash
# Run tests
npm test

# Watch mode during fixes
npm test -- --watch
```

## Quick Reference Commands

### Start Debugging Session
```bash
# Full debug output
DEBUG=express:*,myapp:* node --inspect app.js

# Attach debugger and break immediately
node --inspect-brk app.js

# With nodemon for auto-reload
DEBUG=express:* nodemon --inspect app.js
```

### Inspect Running Process
```bash
# List Node processes
ps aux | grep node

# Attach Chrome DevTools
# Open chrome://inspect in browser

# Memory usage
node --expose-gc -e "console.log(process.memoryUsage())"
```

### Test Endpoints
```bash
# GET request with verbose output
curl -v http://localhost:3000/api/endpoint

# POST with JSON
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'

# With authorization
curl -H "Authorization: Bearer TOKEN" http://localhost:3000/api/protected

# Follow redirects
curl -L http://localhost:3000/redirect

# Show response headers
curl -I http://localhost:3000/api/endpoint
```

### Check Middleware Stack
```javascript
// Add to app.js temporarily
console.log('Middleware stack:');
app._router.stack.forEach((layer, index) => {
  if (layer.route) {
    console.log(`${index}: Route - ${Object.keys(layer.route.methods)} ${layer.route.path}`);
  } else if (layer.name === 'router') {
    console.log(`${index}: Router - ${layer.regexp}`);
  } else {
    console.log(`${index}: Middleware - ${layer.name}`);
  }
});
```

### Memory Debugging
```bash
# Start with increased memory
node --max-old-space-size=4096 app.js

# Generate heap snapshot
node --inspect app.js
# In Chrome DevTools: Memory tab > Take heap snapshot

# Track memory over time
node -e "setInterval(() => console.log(process.memoryUsage()), 1000)"
```

### Log Analysis
```bash
# Tail logs with filtering
tail -f app.log | grep ERROR

# Count error types
grep -o 'Error: [^,]*' app.log | sort | uniq -c | sort -rn

# Find slow requests (Morgan format)
grep -E '[0-9]{4,}ms' access.log
```

## Diagnostic Middleware Template

Add this to quickly diagnose issues:

```javascript
// debug-middleware.js
const debug = require('debug')('myapp:debug');

module.exports = function diagnosticMiddleware(req, res, next) {
  const start = Date.now();

  debug('Incoming request:');
  debug('  Method: %s', req.method);
  debug('  URL: %s', req.originalUrl);
  debug('  Headers: %O', req.headers);
  debug('  Body: %O', req.body);
  debug('  Query: %O', req.query);
  debug('  Params: %O', req.params);

  // Capture response
  const originalSend = res.send;
  res.send = function(body) {
    const duration = Date.now() - start;
    debug('Response:');
    debug('  Status: %d', res.statusCode);
    debug('  Duration: %dms', duration);
    debug('  Body length: %d', body?.length || 0);
    return originalSend.call(this, body);
  };

  next();
};

// Usage: app.use(require('./debug-middleware'));
```

## Common Error Messages Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `Cannot GET /path` | Route not found | Check route registration, order |
| `TypeError: Cannot read property 'x' of undefined` | Missing data in req | Validate req.body, req.params |
| `Error: Request timeout` | Slow operation, no response | Check DB, add timeout handling |
| `PayloadTooLargeError` | Body exceeds limit | Increase body-parser limit |
| `ECONNREFUSED` | Can't connect to service | Check DB/Redis is running |
| `EADDRINUSE` | Port already in use | Kill process or change port |
| `ERR_HTTP_HEADERS_SENT` | Response sent twice | Remove duplicate res.send() |

## Sources

- [Express.js Official Debugging Guide](https://expressjs.com/en/guide/debugging.html)
- [VS Code Node.js Debugging](https://code.visualstudio.com/docs/nodejs/nodejs-debugging)
- [Better Stack: Node.js Debugging](https://betterstack.com/community/guides/scaling-nodejs/nodejs-debugging/)
- [Better Stack: Common Node.js Errors](https://betterstack.com/community/guides/scaling-nodejs/nodejs-errors/)
- [Kinsta: How to Debug Node.js](https://kinsta.com/blog/node-debug/)
- [DigitalOcean: Debug Node.js with Chrome DevTools](https://www.digitalocean.com/community/tutorials/how-to-debug-node-js-with-the-built-in-debugger-and-chrome-devtools)
- [Better Stack: Express Error Handling](https://betterstack.com/community/guides/scaling-nodejs/error-handling-express/)
