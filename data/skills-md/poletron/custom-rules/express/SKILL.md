---
name: express
description: >
  Express.js REST API patterns and best practices.
  Trigger: When building Express.js REST APIs.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with express"

## When to Use

Use this skill when:
- Building REST APIs with Express.js
- Implementing middleware patterns
- Handling authentication
- Structuring Express applications

---

## Critical Patterns

### Route Organization (REQUIRED)

```javascript
// ✅ ALWAYS: Separate routes by resource
// routes/users.js
const router = express.Router();

router.get('/', usersController.list);
router.get('/:id', usersController.getById);
router.post('/', validate(createUserSchema), usersController.create);
router.put('/:id', validate(updateUserSchema), usersController.update);
router.delete('/:id', usersController.delete);

module.exports = router;
```

### Error Handling (REQUIRED)

```javascript
// ✅ ALWAYS: Centralized error handler
app.use((err, req, res, next) => {
  console.error(err.stack);
  
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';
  
  res.status(status).json({
    error: { message, status }
  });
});

// ✅ Async wrapper for async route handlers
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);
```

---

## Decision Tree

```
Need validation?           → Use Joi or Zod middleware
Need auth?                 → Use Passport.js or JWT middleware
Need logging?              → Use Morgan middleware
Need CORS?                 → Use cors middleware
Need rate limiting?        → Use express-rate-limit
```

---

## Commands

```bash
npm init -y
npm install express
npm install -D nodemon
npm run dev
```
