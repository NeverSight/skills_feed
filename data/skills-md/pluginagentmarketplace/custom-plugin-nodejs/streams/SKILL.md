---
name: streams
description: Master Node.js streams for memory-efficient processing of large datasets, real-time data handling, and building data pipelines
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 03-async-programming
bond_type: PRIMARY_BOND
---

# Node.js Streams Skill

Master streams for memory-efficient processing of large files, real-time data, and building composable data pipelines.

## Quick Start

Streams in 4 types:
1. **Readable** - Source of data (file, HTTP request)
2. **Writable** - Destination (file, HTTP response)
3. **Transform** - Modify data in transit
4. **Duplex** - Both readable and writable

## Core Concepts

### Readable Stream
```javascript
const fs = require('fs');

// Create readable stream
const readStream = fs.createReadStream('large-file.txt', {
  encoding: 'utf8',
  highWaterMark: 64 * 1024 // 64KB chunks
});

// Event-based consumption
readStream.on('data', (chunk) => {
  console.log(`Received ${chunk.length} bytes`);
});

readStream.on('end', () => {
  console.log('Finished reading');
});

readStream.on('error', (err) => {
  console.error('Read error:', err);
});
```

### Writable Stream
```javascript
const writeStream = fs.createWriteStream('output.txt');

// Write data
writeStream.write('Hello, ');
writeStream.write('World!\n');
writeStream.end(); // Signal end

// Handle backpressure
const ok = writeStream.write(data);
if (!ok) {
  // Wait for drain event before writing more
  writeStream.once('drain', () => {
    continueWriting();
  });
}
```

### Transform Stream
```javascript
const { Transform } = require('stream');

// Custom transform: uppercase text
const upperCase = new Transform({
  transform(chunk, encoding, callback) {
    this.push(chunk.toString().toUpperCase());
    callback();
  }
});

// Usage
fs.createReadStream('input.txt')
  .pipe(upperCase)
  .pipe(fs.createWriteStream('output.txt'));
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Understand stream types
- ✅ Read/write file streams
- ✅ Basic pipe operations
- ✅ Handle stream events

### Intermediate (3-4 weeks)
- ✅ Transform streams
- ✅ Backpressure handling
- ✅ Object mode streams
- ✅ Pipeline utility

### Advanced (5-6 weeks)
- ✅ Custom stream implementation
- ✅ Async iterators
- ✅ Web Streams API
- ✅ Performance optimization

## Pipeline (Recommended)
```javascript
const { pipeline } = require('stream/promises');
const zlib = require('zlib');

// Compose streams with error handling
async function compressFile(input, output) {
  await pipeline(
    fs.createReadStream(input),
    zlib.createGzip(),
    fs.createWriteStream(output)
  );
  console.log('Compression complete');
}

// With transform
await pipeline(
  fs.createReadStream('data.csv'),
  csvParser(),
  transformRow(),
  jsonStringify(),
  fs.createWriteStream('data.json')
);
```

### Pipeline with Error Handling
```javascript
const { pipeline } = require('stream');

pipeline(
  source,
  transform1,
  transform2,
  destination,
  (err) => {
    if (err) {
      console.error('Pipeline failed:', err);
    } else {
      console.log('Pipeline succeeded');
    }
  }
);
```

## HTTP Streaming
```javascript
const http = require('http');
const fs = require('fs');

// Stream file as HTTP response
http.createServer((req, res) => {
  const filePath = './video.mp4';
  const stat = fs.statSync(filePath);

  res.writeHead(200, {
    'Content-Type': 'video/mp4',
    'Content-Length': stat.size
  });

  // Stream instead of loading entire file
  fs.createReadStream(filePath).pipe(res);
}).listen(3000);

// Stream HTTP request body
http.createServer((req, res) => {
  const writeStream = fs.createWriteStream('./upload.bin');
  req.pipe(writeStream);

  req.on('end', () => {
    res.end('Upload complete');
  });
}).listen(3001);
```

## Object Mode Streams
```javascript
const { Transform } = require('stream');

const jsonParser = new Transform({
  objectMode: true,
  transform(chunk, encoding, callback) {
    try {
      const obj = JSON.parse(chunk);
      this.push(obj);
      callback();
    } catch (err) {
      callback(err);
    }
  }
});

// Process objects instead of buffers
const processRecords = new Transform({
  objectMode: true,
  transform(record, encoding, callback) {
    record.processed = true;
    record.timestamp = Date.now();
    this.push(record);
    callback();
  }
});
```

## Async Iterators
```javascript
const { Readable } = require('stream');

// Create from async iterator
async function* generateData() {
  for (let i = 0; i < 100; i++) {
    yield { id: i, data: `item-${i}` };
  }
}

const stream = Readable.from(generateData(), { objectMode: true });

// Consume with for-await
async function processStream(readable) {
  for await (const chunk of readable) {
    console.log('Processing:', chunk);
  }
}
```

## Backpressure Handling
```javascript
const readable = fs.createReadStream('huge-file.txt');
const writable = fs.createWriteStream('output.txt');

readable.on('data', (chunk) => {
  // Check if writable can accept more data
  const canContinue = writable.write(chunk);

  if (!canContinue) {
    // Pause reading until writable is ready
    readable.pause();
    writable.once('drain', () => {
      readable.resume();
    });
  }
});

// Or use pipeline (handles automatically)
pipeline(readable, writable, (err) => {
  if (err) console.error('Error:', err);
});
```

## Custom Readable Stream
```javascript
const { Readable } = require('stream');

class DatabaseStream extends Readable {
  constructor(query, options) {
    super({ ...options, objectMode: true });
    this.query = query;
    this.cursor = null;
  }

  async _read() {
    if (!this.cursor) {
      this.cursor = await db.collection('items').find(this.query).cursor();
    }

    const doc = await this.cursor.next();
    if (doc) {
      this.push(doc);
    } else {
      this.push(null); // Signal end
    }
  }
}

// Usage
const dbStream = new DatabaseStream({ status: 'active' });
for await (const item of dbStream) {
  console.log(item);
}
```

## Unit Test Template
```javascript
const { Readable, Transform } = require('stream');
const { pipeline } = require('stream/promises');

describe('Stream Processing', () => {
  it('should transform data correctly', async () => {
    const input = Readable.from(['hello', 'world']);
    const chunks = [];

    const upperCase = new Transform({
      transform(chunk, enc, cb) {
        this.push(chunk.toString().toUpperCase());
        cb();
      }
    });

    await pipeline(
      input,
      upperCase,
      async function* (source) {
        for await (const chunk of source) {
          chunks.push(chunk.toString());
        }
      }
    );

    expect(chunks).toEqual(['HELLO', 'WORLD']);
  });
});
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Memory grows infinitely | No backpressure | Use pipeline or handle drain |
| Data loss | Errors not caught | Use pipeline with error callback |
| Slow processing | Small chunk size | Increase highWaterMark |
| Stream hangs | Missing end() call | Call writable.end() |

## When to Use

Use streams when:
- Processing large files (GB+)
- Real-time data processing
- Memory-constrained environments
- Building data pipelines
- HTTP request/response handling

## Related Skills

- Async Programming (async patterns)
- Performance Optimization (memory efficiency)
- Express REST API (streaming responses)

## Resources

- [Node.js Streams Docs](https://nodejs.org/api/stream.html)
- [Stream Handbook](https://github.com/substack/stream-handbook)
- [Node.js Streams Guide](https://nodejs.dev/learn/nodejs-streams)
