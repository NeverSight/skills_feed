---
name: performance-optimization
description: Optimize Node.js application performance with caching, clustering, profiling, and monitoring techniques
sasmp_version: "1.3.0"
bonded_agent: 01-nodejs-fundamentals
bond_type: PRIMARY_BOND
---

# Performance Optimization Skill

Master Node.js performance optimization for fast, scalable, and efficient backend applications.

## Quick Start

Optimize in 4 areas:
1. **Caching** - Redis/in-memory caching
2. **Clustering** - Use all CPU cores
3. **Profiling** - Find bottlenecks
4. **Monitoring** - Track performance

## Core Concepts

### Caching with Redis
```javascript
const redis = require('redis');
const client = redis.createClient({ url: process.env.REDIS_URL });

// Cache middleware
async function cacheMiddleware(req, res, next) {
  const key = `cache:${req.originalUrl}`;

  const cached = await client.get(key);
  if (cached) {
    return res.json(JSON.parse(cached));
  }

  // Override res.json to cache response
  const originalJson = res.json.bind(res);
  res.json = (data) => {
    client.setEx(key, 3600, JSON.stringify(data)); // 1 hour
    originalJson(data);
  };

  next();
}

// Usage
app.get('/api/users', cacheMiddleware, getUsers);
```

### Clustering (Use All CPU Cores)
```javascript
const cluster = require('cluster');
const os = require('os');

if (cluster.isMaster) {
  const numCPUs = os.cpus().length;

  console.log(`Master ${process.pid} starting ${numCPUs} workers`);

  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }

  cluster.on('exit', (worker) => {
    console.log(`Worker ${worker.process.pid} died, restarting...`);
    cluster.fork();
  });
} else {
  // Worker process - start Express server
  const app = require('./app');
  app.listen(3000, () => {
    console.log(`Worker ${process.pid} started`);
  });
}
```

## Learning Path

### Beginner (2-3 weeks)
- ✅ Implement basic caching
- ✅ Use compression middleware
- ✅ Optimize database queries
- ✅ Enable production mode

### Intermediate (4-5 weeks)
- ✅ Setup Redis caching
- ✅ Implement clustering
- ✅ Database indexing
- ✅ Response pagination

### Advanced (6-8 weeks)
- ✅ CPU/memory profiling
- ✅ Load balancing
- ✅ CDN integration
- ✅ Performance monitoring

## Database Optimization

### Connection Pooling
```javascript
// PostgreSQL pool
const { Pool } = require('pg');

const pool = new Pool({
  max: 20,  // Max connections
  min: 5,   // Min connections
  idleTimeoutMillis: 30000
});

// MongoDB with Mongoose
mongoose.connect(uri, {
  maxPoolSize: 10,
  minPoolSize: 5
});
```

### Query Optimization
```javascript
// ❌ Bad: N+1 query problem
const users = await User.find();
for (const user of users) {
  user.posts = await Post.find({ userId: user.id }); // N queries
}

// ✅ Good: Single query with join
const users = await User.find().populate('posts'); // 1 query

// Add indexes
userSchema.index({ email: 1 }, { unique: true });
userSchema.index({ createdAt: -1 });

// Use lean() for read-only queries (faster)
const users = await User.find().lean(); // Returns plain objects
```

### Pagination
```javascript
async function getUsers(req, res) {
  const page = parseInt(req.query.page) || 1;
  const limit = parseInt(req.query.limit) || 10;
  const skip = (page - 1) * limit;

  const [users, total] = await Promise.all([
    User.find().limit(limit).skip(skip),
    User.countDocuments()
  ]);

  res.json({
    data: users,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit)
    }
  });
}
```

## Response Optimization

### Compression
```javascript
const compression = require('compression');

app.use(compression({
  level: 6,
  threshold: 1024  // Only compress > 1KB
}));
```

### Response Caching Headers
```javascript
app.get('/api/static-data', (req, res) => {
  res.set('Cache-Control', 'public, max-age=3600'); // Cache 1 hour
  res.json(data);
});

// For frequently changing data
res.set('Cache-Control', 'public, max-age=60'); // Cache 1 minute
```

## Async Optimization

### Parallel Execution
```javascript
// ❌ Sequential (300ms)
const users = await getUsers();    // 100ms
const posts = await getPosts();    // 100ms
const comments = await getComments(); // 100ms

// ✅ Parallel (100ms)
const [users, posts, comments] = await Promise.all([
  getUsers(),
  getPosts(),
  getComments()
]);
```

### Stream Large Files
```javascript
const fs = require('fs');

// ❌ Bad: Load entire file into memory
app.get('/large-file', async (req, res) => {
  const data = await fs.promises.readFile('large.txt');
  res.send(data);
});

// ✅ Good: Stream file
app.get('/large-file', (req, res) => {
  const stream = fs.createReadStream('large.txt');
  stream.pipe(res);
});
```

## CPU Profiling

### Built-in Profiler
```bash
# Start with profiler
node --prof app.js

# Generate readable output
node --prof-process isolate-0x*.log > profile.txt
```

### Performance Measurement
```javascript
const { performance } = require('perf_hooks');

const start = performance.now();
await heavyOperation();
const end = performance.now();
console.log(`Operation took ${end - start}ms`);
```

## Memory Optimization

### Avoid Memory Leaks
```javascript
// ❌ Bad: Memory leak
const cache = {};
app.get('/data/:id', (req, res) => {
  cache[req.params.id] = data; // Never cleaned up
  res.json(data);
});

// ✅ Good: Use LRU cache with limits
const LRU = require('lru-cache');
const cache = new LRU({
  max: 500,  // Max 500 items
  maxAge: 1000 * 60 * 60  // TTL: 1 hour
});
```

### Monitor Memory
```javascript
const used = process.memoryUsage();
console.log({
  rss: `${Math.round(used.rss / 1024 / 1024)}MB`,
  heapTotal: `${Math.round(used.heapTotal / 1024 / 1024)}MB`,
  heapUsed: `${Math.round(used.heapUsed / 1024 / 1024)}MB`
});
```

## Monitoring & APM

### Winston Logging
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

// Request logging
app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    logger.info('HTTP Request', {
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: Date.now() - start
    });
  });

  next();
});
```

### APM Tools
- **New Relic** - Full-stack monitoring
- **Datadog** - Infrastructure + APM
- **Dynatrace** - AI-powered monitoring
- **PM2 Plus** - Node.js specific monitoring

## Load Testing

### Artillery
```yaml
# load-test.yml
config:
  target: 'http://localhost:3000'
  phases:
    - duration: 60
      arrivalRate: 10

scenarios:
  - name: "Get users"
    flow:
      - get:
          url: "/api/users"
```

```bash
artillery run load-test.yml
```

## Performance Checklist
- ✅ Enable Node.js production mode (`NODE_ENV=production`)
- ✅ Use clustering (PM2 or cluster module)
- ✅ Implement caching (Redis)
- ✅ Database connection pooling
- ✅ Add database indexes
- ✅ Compress responses (gzip)
- ✅ Use CDN for static assets
- ✅ Optimize images
- ✅ Paginate large datasets
- ✅ Stream large files
- ✅ Monitor with APM tools

## Production Optimizations
```javascript
// production.js
if (process.env.NODE_ENV === 'production') {
  // Trust proxy (for load balancer)
  app.set('trust proxy', 1);

  // Disable x-powered-by header
  app.disable('x-powered-by');

  // Enable compression
  app.use(compression());

  // Use production logger
  app.use(productionLogger());
}
```

## When to Use

Optimize performance when:
- Application is slow or unresponsive
- Need to handle high traffic
- Database queries are bottleneck
- Memory usage is high
- Scaling horizontally
- Preparing for production

## Related Skills
- Express REST API (optimize API performance)
- Async Programming (async optimization)
- Database Integration (query optimization)
- Docker Deployment (production deployment)

## Resources
- [Node.js Performance Guide](https://nodejs.org/en/docs/guides/simple-profiling/)
- [Redis Documentation](https://redis.io/docs)
- [PM2 Clustering](https://pm2.keymetrics.io/docs/usage/cluster-mode/)
- [Web Performance](https://web.dev/performance/)
