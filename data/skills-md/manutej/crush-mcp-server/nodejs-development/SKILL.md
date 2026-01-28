---
name: nodejs-development
description: Comprehensive Node.js development skill covering event loop, async patterns, streams, file system, HTTP servers, process management, and modern Node.js best practices
category: backend
tags: [nodejs, javascript, backend, async, streams, http, api, server]
version: 1.0.0
---

# Node.js Development Skill

This skill provides comprehensive guidance for building modern Node.js applications covering the event loop, async patterns, streams, file system operations, HTTP servers, process management, and best practices for production-ready Node.js development.

## When to Use This Skill

Use this skill when:
- Building RESTful APIs and backend services
- Creating command-line interface (CLI) tools and utilities
- Developing microservices and distributed systems
- Building real-time applications with WebSockets or Server-Sent Events
- Creating build tools, task runners, and development tools
- Working with file processing and data transformation
- Implementing server-side data validation and business logic
- Building proxy servers and middleware layers
- Creating automation scripts and system utilities
- Developing serverless functions and cloud-native applications
- Implementing background job processors and workers
- Building GraphQL servers and API gateways

## Core Concepts

### Event Loop

The event loop is the heart of Node.js, enabling non-blocking I/O operations despite JavaScript being single-threaded.

**Event Loop Phases:**

```javascript
// The event loop processes operations in this order:
// 1. Timers (setTimeout, setInterval)
// 2. Pending callbacks (I/O callbacks deferred from previous iteration)
// 3. Idle, prepare (internal use)
// 4. Poll (retrieve new I/O events)
// 5. Check (setImmediate callbacks)
// 6. Close callbacks (socket.on('close'))

// Understanding execution order
console.log('1 - Start');

setTimeout(() => {
  console.log('2 - Timeout');
}, 0);

setImmediate(() => {
  console.log('3 - Immediate');
});

Promise.resolve().then(() => {
  console.log('4 - Promise');
});

process.nextTick(() => {
  console.log('5 - Next Tick');
});

console.log('6 - End');

// Output order: 1, 6, 5, 4, 2, 3
// (process.nextTick and Promises run before other phases)
```

**Event Loop Best Practices:**

```javascript
// Don't block the event loop
// Bad - blocking operation
const data = fs.readFileSync('large-file.txt'); // Blocks

// Good - non-blocking
fs.readFile('large-file.txt', (err, data) => {
  // Non-blocking
});

// Better - using promises
const data = await fs.promises.readFile('large-file.txt');

// Avoid heavy CPU operations
// Bad - blocks event loop
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// Good - offload to worker threads
const { Worker } = require('worker_threads');

function computeInWorker(n) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./fibonacci-worker.js', {
      workerData: n
    });
    worker.on('message', resolve);
    worker.on('error', reject);
  });
}
```

### Modules

Node.js supports both CommonJS and ES Modules for organizing code.

**CommonJS (Traditional):**

```javascript
// math.js - Exporting
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

module.exports = { add, subtract };

// Alternative export syntax
exports.multiply = (a, b) => a * b;

// app.js - Importing
const { add, subtract } = require('./math');
const fs = require('fs'); // Built-in module
const express = require('express'); // npm package

console.log(add(5, 3)); // 8
```

**ES Modules (Modern):**

```javascript
// math.mjs or math.js (with "type": "module" in package.json)
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export default class Calculator {
  add(a, b) { return a + b; }
}

// app.mjs - Importing
import { add, subtract } from './math.mjs';
import Calculator from './math.mjs';
import fs from 'fs';
import express from 'express';

console.log(add(5, 3)); // 8
```

**Built-in Modules:**

```javascript
// Core Node.js modules (no npm install required)
const fs = require('fs');           // File system
const path = require('path');       // Path utilities
const http = require('http');       // HTTP server
const https = require('https');     // HTTPS server
const crypto = require('crypto');   // Cryptography
const os = require('os');           // Operating system
const events = require('events');   // Event emitter
const stream = require('stream');   // Streams
const util = require('util');       // Utilities
const child_process = require('child_process'); // Child processes
const cluster = require('cluster'); // Clustering
const url = require('url');         // URL parsing
const querystring = require('querystring'); // Query strings
```

### Async Programming

Node.js provides multiple patterns for handling asynchronous operations.

**Callbacks (Traditional):**

```javascript
const fs = require('fs');

// Error-first callback pattern
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }
  console.log('File contents:', data);
});

// Callback hell (avoid this)
fs.readFile('file1.txt', (err, data1) => {
  if (err) return console.error(err);
  fs.readFile('file2.txt', (err, data2) => {
    if (err) return console.error(err);
    fs.readFile('file3.txt', (err, data3) => {
      if (err) return console.error(err);
      console.log(data1, data2, data3);
    });
  });
});
```

**Promises:**

```javascript
const fs = require('fs').promises;

// Basic promise
fs.readFile('file.txt', 'utf8')
  .then(data => {
    console.log('File contents:', data);
    return data;
  })
  .catch(err => {
    console.error('Error:', err);
  })
  .finally(() => {
    console.log('Operation complete');
  });

// Promise chaining
fs.readFile('file1.txt', 'utf8')
  .then(data1 => {
    console.log('File 1:', data1);
    return fs.readFile('file2.txt', 'utf8');
  })
  .then(data2 => {
    console.log('File 2:', data2);
    return fs.readFile('file3.txt', 'utf8');
  })
  .then(data3 => {
    console.log('File 3:', data3);
  })
  .catch(err => {
    console.error('Error:', err);
  });

// Promise.all for parallel operations
Promise.all([
  fs.readFile('file1.txt', 'utf8'),
  fs.readFile('file2.txt', 'utf8'),
  fs.readFile('file3.txt', 'utf8')
])
  .then(([data1, data2, data3]) => {
    console.log(data1, data2, data3);
  })
  .catch(err => {
    console.error('Error:', err);
  });

// Promise utilities
Promise.race([
  fetch('https://api1.com'),
  fetch('https://api2.com')
]); // Returns first to complete

Promise.allSettled([
  promise1,
  promise2,
  promise3
]); // Waits for all, returns all results (success or failure)

Promise.any([
  promise1,
  promise2
]); // Returns first successful promise
```

**Async/Await (Modern):**

```javascript
const fs = require('fs').promises;

// Basic async/await
async function readFile() {
  try {
    const data = await fs.readFile('file.txt', 'utf8');
    console.log('File contents:', data);
    return data;
  } catch (err) {
    console.error('Error:', err);
    throw err;
  }
}

// Sequential execution
async function readFilesSequentially() {
  try {
    const data1 = await fs.readFile('file1.txt', 'utf8');
    const data2 = await fs.readFile('file2.txt', 'utf8');
    const data3 = await fs.readFile('file3.txt', 'utf8');
    return [data1, data2, data3];
  } catch (err) {
    console.error('Error:', err);
    throw err;
  }
}

// Parallel execution
async function readFilesParallel() {
  try {
    const [data1, data2, data3] = await Promise.all([
      fs.readFile('file1.txt', 'utf8'),
      fs.readFile('file2.txt', 'utf8'),
      fs.readFile('file3.txt', 'utf8')
    ]);
    return [data1, data2, data3];
  } catch (err) {
    console.error('Error:', err);
    throw err;
  }
}

// Top-level await (ES modules only)
const data = await fs.readFile('config.json', 'utf8');
const config = JSON.parse(data);

// Error handling patterns
async function robustOperation() {
  try {
    const result = await riskyOperation();
    return { success: true, data: result };
  } catch (err) {
    console.error('Operation failed:', err);
    return { success: false, error: err.message };
  }
}

// Multiple error handling
async function multipleOperations() {
  const results = await Promise.allSettled([
    operation1(),
    operation2(),
    operation3()
  ]);

  results.forEach((result, index) => {
    if (result.status === 'fulfilled') {
      console.log(`Operation ${index} succeeded:`, result.value);
    } else {
      console.error(`Operation ${index} failed:`, result.reason);
    }
  });
}
```

**Promisify Utility:**

```javascript
const util = require('util');
const fs = require('fs');

// Convert callback-based function to promise-based
const readFile = util.promisify(fs.readFile);
const writeFile = util.promisify(fs.writeFile);

async function processFile() {
  const data = await readFile('input.txt', 'utf8');
  const processed = data.toUpperCase();
  await writeFile('output.txt', processed);
}

// Custom promisify
function promisify(fn) {
  return (...args) => {
    return new Promise((resolve, reject) => {
      fn(...args, (err, result) => {
        if (err) reject(err);
        else resolve(result);
      });
    });
  };
}
```

### Streams

Streams are one of Node.js's most powerful features for handling data efficiently.

**Stream Types:**

```javascript
const fs = require('fs');
const { Readable, Writable, Duplex, Transform } = require('stream');

// 1. Readable Stream
const readStream = fs.createReadStream('large-file.txt', {
  encoding: 'utf8',
  highWaterMark: 64 * 1024 // 64KB chunks
});

readStream.on('data', (chunk) => {
  console.log('Received chunk:', chunk.length);
});

readStream.on('end', () => {
  console.log('Finished reading');
});

readStream.on('error', (err) => {
  console.error('Error:', err);
});

// 2. Writable Stream
const writeStream = fs.createWriteStream('output.txt');

writeStream.write('Hello ');
writeStream.write('World\n');
writeStream.end();

writeStream.on('finish', () => {
  console.log('Finished writing');
});

// 3. Pipe - connecting streams
fs.createReadStream('input.txt')
  .pipe(fs.createWriteStream('output.txt'));

// 4. Transform Stream
class UpperCaseTransform extends Transform {
  _transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
}

fs.createReadStream('input.txt')
  .pipe(new UpperCaseTransform())
  .pipe(fs.createWriteStream('output.txt'));

// 5. Custom Readable Stream
class NumberStream extends Readable {
  constructor(max) {
    super();
    this.current = 0;
    this.max = max;
  }

  _read() {
    if (this.current <= this.max) {
      this.push(String(this.current++));
    } else {
      this.push(null); // End stream
    }
  }
}

const numberStream = new NumberStream(10);
numberStream.on('data', (num) => {
  console.log(num);
});

// 6. Custom Writable Stream
class LogStream extends Writable {
  _write(chunk, encoding, callback) {
    console.log(`[LOG] ${chunk.toString()}`);
    callback();
  }
}

const logStream = new LogStream();
logStream.write('Message 1\n');
logStream.write('Message 2\n');
```

**Stream Patterns:**

```javascript
const { pipeline } = require('stream');
const { createReadStream, createWriteStream } = require('fs');
const { createGzip } = require('zlib');

// Pipeline - handles errors and cleanup automatically
pipeline(
  createReadStream('input.txt'),
  createGzip(),
  createWriteStream('input.txt.gz'),
  (err) => {
    if (err) {
      console.error('Pipeline failed:', err);
    } else {
      console.log('Pipeline succeeded');
    }
  }
);

// Stream utilities
const { finished, pipeline: promisePipeline } = require('stream/promises');

async function processFile() {
  await promisePipeline(
    createReadStream('input.txt'),
    createGzip(),
    createWriteStream('output.txt.gz')
  );
  console.log('Processing complete');
}

// Backpressure handling
const reader = createReadStream('large-file.txt');
const writer = createWriteStream('output.txt');

reader.on('data', (chunk) => {
  const canContinue = writer.write(chunk);
  if (!canContinue) {
    // Pause reading if write buffer is full
    reader.pause();
  }
});

writer.on('drain', () => {
  // Resume reading when write buffer is drained
  reader.resume();
});
```

### File System

The `fs` module provides file system operations.

**Reading Files:**

```javascript
const fs = require('fs');
const fsPromises = require('fs').promises;

// Synchronous (blocking - avoid in production)
try {
  const data = fs.readFileSync('file.txt', 'utf8');
  console.log(data);
} catch (err) {
  console.error(err);
}

// Callback-based
fs.readFile('file.txt', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }
  console.log(data);
});

// Promise-based
fsPromises.readFile('file.txt', 'utf8')
  .then(data => console.log(data))
  .catch(err => console.error(err));

// Async/await
async function readFile() {
  try {
    const data = await fsPromises.readFile('file.txt', 'utf8');
    console.log(data);
  } catch (err) {
    console.error('Error:', err);
  }
}

// Read JSON file
async function readJSON(filename) {
  const data = await fsPromises.readFile(filename, 'utf8');
  return JSON.parse(data);
}
```

**Writing Files:**

```javascript
// Write file (overwrites if exists)
await fsPromises.writeFile('output.txt', 'Hello World');

// Append to file
await fsPromises.appendFile('log.txt', 'New log entry\n');

// Write JSON
async function writeJSON(filename, data) {
  await fsPromises.writeFile(
    filename,
    JSON.stringify(data, null, 2)
  );
}

// Atomic write (write to temp, then rename)
async function atomicWrite(filename, data) {
  const tempFile = `${filename}.tmp`;
  await fsPromises.writeFile(tempFile, data);
  await fsPromises.rename(tempFile, filename);
}
```

**File Operations:**

```javascript
const path = require('path');

// Check if file exists
async function fileExists(filename) {
  try {
    await fsPromises.access(filename);
    return true;
  } catch {
    return false;
  }
}

// Get file stats
const stats = await fsPromises.stat('file.txt');
console.log({
  size: stats.size,
  isFile: stats.isFile(),
  isDirectory: stats.isDirectory(),
  modified: stats.mtime,
  created: stats.birthtime
});

// Copy file
await fsPromises.copyFile('source.txt', 'dest.txt');

// Move/rename file
await fsPromises.rename('old-name.txt', 'new-name.txt');

// Delete file
await fsPromises.unlink('file-to-delete.txt');

// Create directory
await fsPromises.mkdir('new-directory', { recursive: true });

// Read directory
const files = await fsPromises.readdir('directory');
console.log(files);

// Read directory with file types
const entries = await fsPromises.readdir('directory', {
  withFileTypes: true
});

for (const entry of entries) {
  if (entry.isFile()) {
    console.log('File:', entry.name);
  } else if (entry.isDirectory()) {
    console.log('Directory:', entry.name);
  }
}

// Remove directory
await fsPromises.rmdir('directory');

// Remove directory recursively
await fsPromises.rm('directory', { recursive: true, force: true });

// Watch for file changes
const watcher = fs.watch('file.txt', (eventType, filename) => {
  console.log(`File ${filename} changed: ${eventType}`);
});

// Stop watching
watcher.close();
```

**Path Utilities:**

```javascript
const path = require('path');

// Join paths (handles separators correctly)
const fullPath = path.join('/users', 'john', 'documents', 'file.txt');
// /users/john/documents/file.txt

// Resolve absolute path
const absolute = path.resolve('documents', 'file.txt');
// /current/working/directory/documents/file.txt

// Get directory name
path.dirname('/users/john/file.txt'); // /users/john

// Get file name
path.basename('/users/john/file.txt'); // file.txt
path.basename('/users/john/file.txt', '.txt'); // file

// Get extension
path.extname('file.txt'); // .txt

// Parse path
const parsed = path.parse('/users/john/file.txt');
// {
//   root: '/',
//   dir: '/users/john',
//   base: 'file.txt',
//   ext: '.txt',
//   name: 'file'
// }

// Format path
const formatted = path.format({
  dir: '/users/john',
  base: 'file.txt'
}); // /users/john/file.txt

// Normalize path
path.normalize('/users/john/../jane/./file.txt');
// /users/jane/file.txt

// Check if absolute
path.isAbsolute('/users/john'); // true
path.isAbsolute('documents/file.txt'); // false

// Get relative path
path.relative('/users/john', '/users/jane/file.txt');
// ../jane/file.txt
```

### HTTP/HTTPS

Creating HTTP servers and making HTTP requests.

**HTTP Server:**

```javascript
const http = require('http');

// Basic HTTP server
const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World\n');
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});

// Server with routing
const server = http.createServer((req, res) => {
  const { method, url } = req;

  if (url === '/' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<h1>Home Page</h1>');
  } else if (url === '/api/users' && method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ users: ['Alice', 'Bob'] }));
  } else if (url === '/api/users' && method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      const data = JSON.parse(body);
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, data }));
    });
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

server.listen(3000);

// JSON API server
const server = http.createServer(async (req, res) => {
  try {
    if (req.url === '/api/data' && req.method === 'GET') {
      const data = { message: 'Hello', timestamp: Date.now() };
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(data));
    } else if (req.url === '/api/data' && req.method === 'POST') {
      const body = await getRequestBody(req);
      const data = JSON.parse(body);

      // Process data
      const result = { received: data, processed: true };

      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(result));
    } else {
      res.writeHead(404);
      res.end(JSON.stringify({ error: 'Not found' }));
    }
  } catch (err) {
    res.writeHead(500);
    res.end(JSON.stringify({ error: err.message }));
  }
});

function getRequestBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}
```

**HTTPS Server:**

```javascript
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem')
};

const server = https.createServer(options, (req, res) => {
  res.writeHead(200);
  res.end('Secure Hello World\n');
});

server.listen(443);
```

**Making HTTP Requests:**

```javascript
const https = require('https');

// Basic GET request
https.get('https://api.example.com/data', (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log(JSON.parse(data));
  });
}).on('error', (err) => {
  console.error('Error:', err.message);
});

// POST request
const postData = JSON.stringify({ name: 'John', age: 30 });

const options = {
  hostname: 'api.example.com',
  port: 443,
  path: '/users',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData)
  }
};

const req = https.request(options, (res) => {
  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('Response:', JSON.parse(data));
  });
});

req.on('error', (err) => {
  console.error('Error:', err.message);
});

req.write(postData);
req.end();

// Promise wrapper for HTTP requests
function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const req = https.request(url, options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          headers: res.headers,
          body: data
        });
      });
    });

    req.on('error', reject);

    if (options.body) {
      req.write(options.body);
    }

    req.end();
  });
}

// Using fetch (Node.js 18+)
async function fetchData() {
  const response = await fetch('https://api.example.com/data');
  const data = await response.json();
  console.log(data);
}

async function postData() {
  const response = await fetch('https://api.example.com/users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name: 'John', age: 30 })
  });
  const result = await response.json();
  console.log(result);
}
```

### Process and Environment

Managing process lifecycle and environment variables.

**Process Object:**

```javascript
// Process information
console.log('Node version:', process.version);
console.log('Platform:', process.platform);
console.log('Architecture:', process.arch);
console.log('Process ID:', process.pid);
console.log('Current directory:', process.cwd());
console.log('Memory usage:', process.memoryUsage());
console.log('CPU usage:', process.cpuUsage());
console.log('Uptime:', process.uptime());

// Command-line arguments
// node app.js --port 3000 --host localhost
console.log('Arguments:', process.argv);
// ['node', '/path/to/app.js', '--port', '3000', '--host', 'localhost']

// Parse arguments
function parseArgs() {
  const args = {};
  for (let i = 2; i < process.argv.length; i += 2) {
    const key = process.argv[i].replace('--', '');
    const value = process.argv[i + 1];
    args[key] = value;
  }
  return args;
}

const config = parseArgs();
console.log(config); // { port: '3000', host: 'localhost' }

// Environment variables
const port = process.env.PORT || 3000;
const nodeEnv = process.env.NODE_ENV || 'development';
const dbUrl = process.env.DATABASE_URL;

console.log('Port:', port);
console.log('Environment:', nodeEnv);

// Set environment variable
process.env.MY_VAR = 'value';

// Exit process
process.exit(0); // Success
process.exit(1); // Error

// Exit codes
const EXIT_CODES = {
  SUCCESS: 0,
  GENERAL_ERROR: 1,
  INVALID_ARGUMENT: 2,
  CONFIG_ERROR: 3
};

if (!config.isValid) {
  console.error('Invalid configuration');
  process.exit(EXIT_CODES.CONFIG_ERROR);
}

// Process events
process.on('exit', (code) => {
  console.log(`Process exiting with code ${code}`);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught exception:', err);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled rejection:', reason);
  process.exit(1);
});

process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
});

// Send signals to process
process.kill(process.pid, 'SIGTERM');
```

**Child Processes:**

```javascript
const { exec, execFile, spawn, fork } = require('child_process');

// exec - run shell command
exec('ls -la', (err, stdout, stderr) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log('Output:', stdout);
  console.error('Errors:', stderr);
});

// execFile - run executable directly (safer)
execFile('node', ['--version'], (err, stdout, stderr) => {
  if (err) {
    console.error('Error:', err);
    return;
  }
  console.log('Node version:', stdout);
});

// spawn - for long-running processes or large output
const ls = spawn('ls', ['-la', '/usr']);

ls.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

ls.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

ls.on('close', (code) => {
  console.log(`Process exited with code ${code}`);
});

// fork - spawn Node.js processes
// parent.js
const child = fork('./child.js');

child.on('message', (msg) => {
  console.log('Message from child:', msg);
});

child.send({ hello: 'child' });

// child.js
process.on('message', (msg) => {
  console.log('Message from parent:', msg);
});

process.send({ hello: 'parent' });

// Promise-based exec
const util = require('util');
const execPromise = util.promisify(exec);

async function runCommand() {
  try {
    const { stdout, stderr } = await execPromise('ls -la');
    console.log('Output:', stdout);
  } catch (err) {
    console.error('Error:', err);
  }
}
```

**Cluster Module:**

```javascript
const cluster = require('cluster');
const http = require('http');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  console.log(`Master process ${process.pid} is running`);

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    // Restart worker
    cluster.fork();
  });
} else {
  // Workers share the same port
  http.createServer((req, res) => {
    res.writeHead(200);
    res.end(`Process ${process.pid} handled request\n`);
  }).listen(8000);

  console.log(`Worker ${process.pid} started`);
}
```

## API Reference

### Buffer

Buffers handle binary data in Node.js.

```javascript
// Create buffers
const buf1 = Buffer.from('Hello World');
const buf2 = Buffer.from([72, 101, 108, 108, 111]);
const buf3 = Buffer.alloc(10); // 10 bytes, filled with 0
const buf4 = Buffer.allocUnsafe(10); // Faster, but may contain old data

// Read/write buffers
buf3.write('Hello');
console.log(buf3.toString()); // Hello
console.log(buf3.toString('hex')); // Hex representation

// Buffer operations
const buf5 = Buffer.concat([buf1, buf2]);
const buf6 = buf1.slice(0, 5); // Hello

// Buffer comparison
Buffer.compare(buf1, buf2); // -1, 0, or 1

// JSON conversion
const json = JSON.stringify(buf1);
const parsed = Buffer.from(JSON.parse(json));
```

### Events

EventEmitter is the foundation of Node.js's event-driven architecture.

```javascript
const EventEmitter = require('events');

// Create event emitter
class MyEmitter extends EventEmitter {}
const myEmitter = new MyEmitter();

// Listen for events
myEmitter.on('event', (arg1, arg2) => {
  console.log('Event occurred:', arg1, arg2);
});

// Emit events
myEmitter.emit('event', 'arg1', 'arg2');

// Listen once
myEmitter.once('oneTime', () => {
  console.log('This will only fire once');
});

// Remove listener
function handler() {
  console.log('Handler called');
}

myEmitter.on('event', handler);
myEmitter.off('event', handler);

// Error handling
myEmitter.on('error', (err) => {
  console.error('Error occurred:', err);
});

// Real-world example: Custom logger
class Logger extends EventEmitter {
  log(message) {
    this.emit('log', { message, timestamp: Date.now() });
  }

  error(message) {
    this.emit('error', { message, timestamp: Date.now() });
  }
}

const logger = new Logger();

logger.on('log', (data) => {
  console.log(`[${new Date(data.timestamp).toISOString()}] ${data.message}`);
});

logger.on('error', (data) => {
  console.error(`[${new Date(data.timestamp).toISOString()}] ERROR: ${data.message}`);
});

logger.log('Application started');
logger.error('Something went wrong');
```

### Crypto

Cryptographic operations for security.

```javascript
const crypto = require('crypto');

// Generate random data
const randomBytes = crypto.randomBytes(16).toString('hex');
console.log('Random:', randomBytes);

// Hash data (one-way)
const hash = crypto.createHash('sha256');
hash.update('password123');
console.log('Hash:', hash.digest('hex'));

// HMAC (keyed hash)
const hmac = crypto.createHmac('sha256', 'secret-key');
hmac.update('message');
console.log('HMAC:', hmac.digest('hex'));

// Password hashing with salt
function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex');
  const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex');
  return { salt, hash };
}

function verifyPassword(password, salt, hash) {
  const hashToVerify = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex');
  return hash === hashToVerify;
}

const { salt, hash } = hashPassword('mypassword');
console.log(verifyPassword('mypassword', salt, hash)); // true

// Encryption/Decryption
function encrypt(text, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', Buffer.from(key), iv);
  let encrypted = cipher.update(text);
  encrypted = Buffer.concat([encrypted, cipher.final()]);
  return iv.toString('hex') + ':' + encrypted.toString('hex');
}

function decrypt(text, key) {
  const parts = text.split(':');
  const iv = Buffer.from(parts[0], 'hex');
  const encrypted = Buffer.from(parts[1], 'hex');
  const decipher = crypto.createDecipheriv('aes-256-cbc', Buffer.from(key), iv);
  let decrypted = decipher.update(encrypted);
  decrypted = Buffer.concat([decrypted, decipher.final()]);
  return decrypted.toString();
}

const key = crypto.randomBytes(32); // 256 bits
const encrypted = encrypt('Hello World', key);
const decrypted = decrypt(encrypted, key);
console.log(decrypted); // Hello World
```

## Workflow Patterns

### REST API Server with Express

```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Logging middleware
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();
});

// Routes
app.get('/api/users', async (req, res) => {
  try {
    const users = await db.getUsers();
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await db.getUserById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/users', async (req, res) => {
  try {
    const user = await db.createUser(req.body);
    res.status(201).json(user);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.put('/api/users/:id', async (req, res) => {
  try {
    const user = await db.updateUser(req.params.id, req.body);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.delete('/api/users/:id', async (req, res) => {
  try {
    await db.deleteUser(req.params.id);
    res.status(204).end();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Database Integration

```javascript
// MongoDB with Mongoose
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/myapp', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const userSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  age: Number,
  createdAt: { type: Date, default: Date.now }
});

const User = mongoose.model('User', userSchema);

// CRUD operations
async function createUser(data) {
  const user = new User(data);
  await user.save();
  return user;
}

async function getUsers() {
  return await User.find();
}

async function getUserById(id) {
  return await User.findById(id);
}

async function updateUser(id, data) {
  return await User.findByIdAndUpdate(id, data, { new: true });
}

async function deleteUser(id) {
  return await User.findByIdAndDelete(id);
}

// PostgreSQL with pg
const { Pool } = require('pg');

const pool = new Pool({
  user: 'dbuser',
  host: 'localhost',
  database: 'mydb',
  password: 'password',
  port: 5432
});

async function queryUsers() {
  const result = await pool.query('SELECT * FROM users');
  return result.rows;
}

async function createUser(name, email) {
  const result = await pool.query(
    'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
    [name, email]
  );
  return result.rows[0];
}
```

### Authentication & Authorization

```javascript
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

// Hash password
async function hashPassword(password) {
  const salt = await bcrypt.genSalt(10);
  return await bcrypt.hash(password, salt);
}

// Verify password
async function verifyPassword(password, hash) {
  return await bcrypt.compare(password, hash);
}

// Generate JWT
function generateToken(user) {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: '7d' }
  );
}

// Verify JWT
function verifyToken(token) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (err) {
    return null;
  }
}

// Auth middleware
function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  const decoded = verifyToken(token);
  if (!decoded) {
    return res.status(401).json({ error: 'Invalid token' });
  }

  req.user = decoded;
  next();
}

// Login route
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;

  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const isValid = await verifyPassword(password, user.password);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken(user);
  res.json({ token, user: { id: user.id, email: user.email } });
});

// Protected route
app.get('/api/profile', authMiddleware, (req, res) => {
  res.json({ user: req.user });
});
```

## Best Practices

### Error Handling

```javascript
// Async error handling wrapper
function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Usage
app.get('/api/users', asyncHandler(async (req, res) => {
  const users = await db.getUsers();
  res.json(users);
}));

// Custom error classes
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404);
  }
}

class ValidationError extends AppError {
  constructor(message = 'Validation failed') {
    super(message, 400);
  }
}

// Global error handler
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.isOperational ? err.message : 'Internal server error';

  // Log error
  console.error(err);

  // Send response
  res.status(statusCode).json({
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// Unhandled errors
process.on('uncaughtException', (err) => {
  console.error('UNCAUGHT EXCEPTION!', err);
  process.exit(1);
});

process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION!', err);
  process.exit(1);
});
```

### Security

```javascript
// Use helmet for security headers
const helmet = require('helmet');
app.use(helmet());

// Rate limiting
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);

// CORS
const cors = require('cors');

app.use(cors({
  origin: 'https://example.com',
  credentials: true
}));

// Input validation
const { body, validationResult } = require('express-validator');

app.post('/api/users',
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 8 }),
  body('name').trim().notEmpty(),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // Process request
  }
);

// Sanitize user input
function sanitize(input) {
  if (typeof input === 'string') {
    return input.replace(/[<>]/g, '');
  }
  return input;
}

// Environment variables
// Never commit .env files
// Use dotenv for local development
require('dotenv').config();

// Secrets management
const secrets = {
  jwtSecret: process.env.JWT_SECRET,
  dbPassword: process.env.DB_PASSWORD,
  apiKey: process.env.API_KEY
};

// Validate required env vars
const requiredEnvVars = ['JWT_SECRET', 'DB_PASSWORD'];
for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}
```

### Performance

```javascript
// Use compression
const compression = require('compression');
app.use(compression());

// Caching
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 }); // 10 minutes

app.get('/api/data', async (req, res) => {
  const cachedData = cache.get('data');
  if (cachedData) {
    return res.json(cachedData);
  }

  const data = await fetchData();
  cache.set('data', data);
  res.json(data);
});

// Database connection pooling
const pool = new Pool({
  max: 20, // Maximum number of connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});

// Use indexes in databases
// MongoDB
userSchema.index({ email: 1 });

// PostgreSQL
// CREATE INDEX idx_users_email ON users(email);

// Pagination
app.get('/api/users', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const skip = (page - 1) * limit;

  const users = await User.find()
    .skip(skip)
    .limit(limit);

  const total = await User.countDocuments();

  res.json({
    data: users,
    page,
    limit,
    total,
    pages: Math.ceil(total / limit)
  });
});

// Optimize queries
// Bad - N+1 query problem
const users = await User.find();
for (const user of users) {
  user.posts = await Post.find({ userId: user.id });
}

// Good - use joins/population
const users = await User.find().populate('posts');

// Stream large responses
app.get('/api/export', (req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.write('[');

  let first = true;
  User.find().cursor().on('data', (user) => {
    if (!first) res.write(',');
    res.write(JSON.stringify(user));
    first = false;
  }).on('end', () => {
    res.write(']');
    res.end();
  });
});
```

### Testing

```javascript
// Using Jest
const request = require('supertest');
const app = require('./app');

describe('GET /api/users', () => {
  it('should return all users', async () => {
    const res = await request(app)
      .get('/api/users')
      .expect(200);

    expect(Array.isArray(res.body)).toBe(true);
  });
});

describe('POST /api/users', () => {
  it('should create a new user', async () => {
    const userData = {
      name: 'John Doe',
      email: 'john@example.com'
    };

    const res = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);

    expect(res.body.name).toBe(userData.name);
    expect(res.body.email).toBe(userData.email);
  });

  it('should return 400 for invalid data', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({})
      .expect(400);
  });
});

// Mocking
jest.mock('./database');
const db = require('./database');

test('getUser returns user data', async () => {
  db.getUserById.mockResolvedValue({
    id: 1,
    name: 'John Doe'
  });

  const user = await getUser(1);
  expect(user.name).toBe('John Doe');
});

// Integration tests with test database
beforeAll(async () => {
  await mongoose.connect(process.env.TEST_DB_URL);
});

afterAll(async () => {
  await mongoose.connection.close();
});

beforeEach(async () => {
  await User.deleteMany({});
});
```

### Logging

```javascript
// Using winston
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}

logger.info('Server started');
logger.error('Error occurred', { error: err.message });

// Request logging
const morgan = require('morgan');
app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));
```

### Deployment

```javascript
// Graceful shutdown
const server = app.listen(PORT);

process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server gracefully');

  server.close(() => {
    console.log('Server closed');

    // Close database connections
    mongoose.connection.close(false, () => {
      console.log('MongoDB connection closed');
      process.exit(0);
    });
  });

  // Force shutdown after 30 seconds
  setTimeout(() => {
    console.error('Forced shutdown');
    process.exit(1);
  }, 30000);
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() });
});

// Process monitoring
const v8 = require('v8');
const os = require('os');

app.get('/metrics', (req, res) => {
  const heapStats = v8.getHeapStatistics();

  res.json({
    memory: {
      used: process.memoryUsage().heapUsed,
      total: heapStats.total_heap_size,
      limit: heapStats.heap_size_limit
    },
    cpu: process.cpuUsage(),
    uptime: process.uptime(),
    system: {
      freemem: os.freemem(),
      totalmem: os.totalmem(),
      loadavg: os.loadavg()
    }
  });
});
```

## Summary

This Node.js development skill covers:

1. **Core Concepts**: Event loop, modules (CommonJS/ES), async patterns, streams, file system, HTTP/HTTPS
2. **API Reference**: Buffer, Events, Crypto, and core modules
3. **Workflow Patterns**: REST APIs, database integration, authentication
4. **Best Practices**: Error handling, security, performance, testing, logging, deployment
5. **Real-world Examples**: Complete patterns for building production-ready applications

The patterns and examples represent modern Node.js development practices for building scalable, secure, and maintainable backend applications.
