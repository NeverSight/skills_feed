---
name: express-rest-api
description: Build production-ready RESTful APIs with Express.js including routing, middleware, validation, and error handling for scalable backend services
sasmp_version: "1.3.0"
bonded_agent: 01-nodejs-fundamentals
bond_type: PRIMARY_BOND
---

# Express REST API Skill

Master building robust, scalable REST APIs with Express.js, the de-facto standard for Node.js web frameworks.

## Quick Start

Build a basic Express API in 5 steps:
1. **Setup Express** - `npm install express`
2. **Create Routes** - Define GET, POST, PUT, DELETE endpoints
3. **Add Middleware** - JSON parsing, CORS, security headers
4. **Handle Errors** - Centralized error handling
5. **Test & Deploy** - Use Postman/Insomnia, deploy to cloud

## Core Concepts

### 1. Express Application Structure
```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Routes
app.use('/api/users', userRoutes);
app.use('/api/products', productRoutes);

// Error handling
app.use(errorHandler);

app.listen(3000, () => console.log('Server running'));
```

### 2. RESTful Route Design
```javascript
// GET    /api/users       - Get all users
// GET    /api/users/:id   - Get user by ID
// POST   /api/users       - Create user
// PUT    /api/users/:id   - Update user
// DELETE /api/users/:id   - Delete user

const router = express.Router();

router.get('/', getAllUsers);
router.get('/:id', getUserById);
router.post('/', createUser);
router.put('/:id', updateUser);
router.delete('/:id', deleteUser);

module.exports = router;
```

### 3. Middleware Patterns
```javascript
// Authentication middleware
const authenticate = (req, res, next) => {
  const token = req.headers.authorization;
  if (!token) return res.status(401).json({ error: 'Unauthorized' });
  // Verify token...
  next();
};

// Validation middleware
const validate = (schema) => (req, res, next) => {
  const { error } = schema.validate(req.body);
  if (error) return res.status(400).json({ error: error.message });
  next();
};

// Usage
router.post('/users', authenticate, validate(userSchema), createUser);
```

### 4. Error Handling
```javascript
// Custom error class
class APIError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
  }
}

// Global error handler
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    success: false,
    error: err.message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});
```

## Learning Path

### Beginner (2-3 weeks)
- ✅ Setup Express and create basic routes
- ✅ Understand middleware concept
- ✅ Implement CRUD operations
- ✅ Test with Postman

### Intermediate (4-6 weeks)
- ✅ Implement authentication (JWT)
- ✅ Add input validation
- ✅ Organize code (MVC pattern)
- ✅ Connect to database

### Advanced (8-10 weeks)
- ✅ API versioning (`/api/v1/`, `/api/v2/`)
- ✅ Rate limiting and security
- ✅ Pagination and filtering
- ✅ API documentation (Swagger)
- ✅ Performance optimization

## Essential Packages

```javascript
{
  "dependencies": {
    "express": "^4.18.0",
    "helmet": "^7.0.0",          // Security headers
    "cors": "^2.8.5",            // Cross-origin requests
    "morgan": "^1.10.0",         // HTTP logger
    "express-validator": "^7.0.0", // Input validation
    "express-rate-limit": "^6.0.0" // Rate limiting
  }
}
```

## Common Patterns

### Response Format
```javascript
// Success
{ success: true, data: {...} }

// Error
{ success: false, error: "Message" }

// Pagination
{
  success: true,
  data: [...],
  pagination: { page: 1, limit: 10, total: 100 }
}
```

### HTTP Status Codes
- `200 OK` - Successful GET/PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Auth required
- `403 Forbidden` - No permission
- `404 Not Found` - Resource not found
- `500 Internal Error` - Server error

## Project Structure
```
src/
├── controllers/    # Route handlers
├── routes/        # Route definitions
├── middlewares/   # Custom middleware
├── models/        # Data models
├── services/      # Business logic
├── utils/         # Helpers
└── app.js         # Express setup
```

## Production Checklist
- ✅ Environment variables (.env)
- ✅ Security headers (Helmet)
- ✅ CORS configuration
- ✅ Rate limiting
- ✅ Input validation
- ✅ Error handling
- ✅ Logging (Morgan/Winston)
- ✅ Testing (Jest/Supertest)
- ✅ API documentation

## Real-World Example

Complete user API:
```javascript
const express = require('express');
const router = express.Router();
const { body } = require('express-validator');

// GET /api/users
router.get('/', async (req, res, next) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const users = await User.find()
      .limit(limit)
      .skip((page - 1) * limit);

    res.json({ success: true, data: users });
  } catch (error) {
    next(error);
  }
});

// POST /api/users
router.post('/',
  body('email').isEmail(),
  body('password').isLength({ min: 8 }),
  async (req, res, next) => {
    try {
      const user = await User.create(req.body);
      res.status(201).json({ success: true, data: user });
    } catch (error) {
      next(error);
    }
  }
);

module.exports = router;
```

## When to Use

Use Express REST API when:
- Building backend for web/mobile apps
- Creating microservices
- Developing API-first applications
- Need flexible, lightweight framework
- Want large ecosystem and community

## Related Skills
- Async Programming (handle async operations)
- Database Integration (connect to MongoDB/PostgreSQL)
- JWT Authentication (secure your APIs)
- Jest Testing (test your endpoints)
- Docker Deployment (containerize your API)

## Resources
- [Express.js Official Docs](https://expressjs.com)
- [REST API Best Practices](https://restfulapi.net)
- [MDN HTTP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP)
