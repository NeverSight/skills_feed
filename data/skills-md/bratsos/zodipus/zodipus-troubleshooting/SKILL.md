---
name: zodipus-troubleshooting
description: Debug and fix Zodipus errors. Use when validation fails, generation errors occur, types don't match, Query Engine behaves unexpectedly, or user encounters any zodipus-related error.
license: MIT
metadata:
  author: zodipus
  version: "1.0.0"
---

# Troubleshooting

Diagnose and fix common Zodipus issues.

## When to Apply

- User gets validation errors
- Generation fails or produces wrong output
- Types don't match expected
- Query Engine returns unexpected results
- User mentions "error", "not working", "failed"
- Import/module resolution issues

## Quick Diagnosis

### "Cannot find module './generated'"

**Cause:** Generator hasn't run yet.

**Fix:**
```bash
npx prisma generate
```

### ZodError: Validation Failed

**Cause:** Data doesn't match schema.

**Debug:**
```typescript
const result = schema.safeParse(data);
if (!result.success) {
  console.log(JSON.stringify(result.error.format(), null, 2));
}
```

**Output shows exactly which field failed:**
```json
{
  "email": {
    "_errors": ["Invalid email"]
  },
  "createdAt": {
    "_errors": ["Expected date, received string"]
  }
}
```

### "Unknown model: X"

**Cause:** Model not registered in Query Engine.

**Fix:** Ensure you import from `generated-index`:
```typescript
// Wrong
import { UserSchema } from './generated/models';

// Correct
import { models, modelRelations } from './generated/generated-index';
```

### Type Mismatch: Date vs String

**Cause:** `dateFormat` configuration mismatch.

**Check your config:**
```prisma
generator zodipus {
  dateFormat = "coerce"  # Accepts Date | string | number
  # or
  dateFormat = "string"  # Requires ISO string only
}
```

**Regenerate after changing:**
```bash
npx prisma generate
```

### Missing Relations in Query

**Cause:** `relationDepth` too shallow.

**Fix:**
```prisma
generator zodipus {
  relationDepth = "10"  # Increase depth
}
```

---

## Generation Issues

### Generator Not Found

**Error:**
```
Error: Generator "zodipus" not found
```

**Fix:** Install the package:
```bash
npm install zodipus
```

### Prisma Version Mismatch

**Error:**
```
Error: Prisma version mismatch
```

**Fix:** Zodipus requires Prisma 6.0+:
```bash
npm update prisma @prisma/client
```

### Output Directory Issues

**Error:**
```
Error: Cannot write to output directory
```

**Fix:** Ensure directory exists or is creatable:
```bash
mkdir -p ./generated
```

### Custom Schema Not Found

**Error:**
```
Error: Cannot find custom schema: MyCustomSchema
```

**Fix:** Define in `custom-schemas.ts`:
```typescript
// generated/custom-schemas.ts
export const MyCustomSchema = z.object({...});
```

---

## Validation Issues

### Validation Failing on Valid Data

**Symptom:** Data looks correct but fails validation.

**Debug steps:**

1. **Check for hidden characters:**
```typescript
console.log(JSON.stringify(data, null, 2));
```

2. **Check types exactly:**
```typescript
console.log(typeof data.createdAt); // string? Date? number?
```

3. **Test fields individually:**
```typescript
const fields = ['id', 'email', 'name', 'createdAt'];
for (const field of fields) {
  const partial = { [field]: data[field] };
  const result = schema.pick({ [field]: true }).safeParse(partial);
  if (!result.success) {
    console.log(`${field} failed:`, result.error.format());
  }
}
```

### Date Validation Failing

**Symptom:** `Invalid date` or `Expected string` errors.

**Common causes:**

1. **Prisma returns Date, schema expects string:**
```prisma
# Change to coerce
dateFormat = "coerce"
```

2. **Invalid date string format:**
```typescript
// Invalid
{ createdAt: "01/15/2024" }

// Valid (ISO 8601)
{ createdAt: "2024-01-15T00:00:00.000Z" }
```

3. **Null/undefined dates:**
```typescript
// Schema requires date, got null
{ createdAt: null } // Error if field not optional
```

### Enum Validation Failing

**Symptom:** `Invalid enum value` error.

**Check case sensitivity:**
```typescript
// Prisma enum
enum Role {
  USER
  ADMIN
}

// Must match exactly
{ role: 'USER' }  // OK
{ role: 'user' }  // Error
{ role: 'User' }  // Error
```

### JSON Field Validation Failing

**Symptom:** `@zodSchema` field failing validation.

**Check custom schema exists:**
```typescript
// generated/custom-schemas.ts
export const MySchema = z.object({
  // Not z.unknown() - actual schema
});
```

**Check data matches schema:**
```typescript
import { MySchema } from './generated/custom-schemas';

const result = MySchema.safeParse(data.jsonField);
console.log(result);
```

---

## Query Engine Issues

### "Cannot read property 'parse' of undefined"

**Cause:** Query builder not created properly.

**Fix:**
```typescript
const registry = createRegistry({ models, relations: modelRelations });
const userQuery = registry.createQuery('user'); // Returns function
const query = userQuery({ select: { id: true } }); // Call it
query.parse(data); // Now has parse method
```

### Array vs Single Item Mismatch

**Error:** `Expected object, received array`

**Fix:** Use `.array()` for findMany:
```typescript
// Wrong
const users = await prisma.user.findMany(query.query);
query.parse(users); // Error: expected object

// Correct
query.array().parse(users);
```

### Missing Fields in Validated Result

**Cause:** Field not in `select`.

**Fix:** Add to selection:
```typescript
const query = userQuery({
  select: {
    id: true,
    email: true,
    // Add missing field
    name: true,
  }
});
```

### Relation Not Included

**Cause:** Relation not in query configuration.

**Fix:**
```typescript
const query = userQuery({
  select: { id: true },
  // Add relation
  posts: {
    select: { id: true, title: true }
  }
});
```

---

## TypeScript Issues

### Types Not Updating

**Cause:** TypeScript cache.

**Fix:**
```bash
# Restart TS server in VSCode
Cmd+Shift+P → "TypeScript: Restart TS Server"

# Or regenerate
npx prisma generate
```

### "Type 'X' is not assignable to type 'Y'"

**Debug:** Check inferred type:
```typescript
import { z } from 'zod';

const query = userQuery({ select: { id: true } });
type QueryResult = z.infer<ReturnType<typeof query.parse>>;
// Hover over QueryResult to see actual type
```

### Import Path Issues

**ESM/CJS conflicts:**
```typescript
// Try different import styles
import { UserSchema } from './generated';
import { UserSchema } from './generated/index';
import { UserSchema } from './generated/models';
```

**tsconfig paths:**
```json
{
  "compilerOptions": {
    "paths": {
      "@generated/*": ["./generated/*"]
    }
  }
}
```

---

## CLI Debugging

### Inspect Schema Structure

```bash
# View all models
npx zodipus inspect prisma/schema.prisma --models

# View enums
npx zodipus inspect prisma/schema.prisma --enums

# View relations
npx zodipus inspect prisma/schema.prisma --relations

# Full JSON output
npx zodipus inspect prisma/schema.prisma --json
```

### Dry Run Generation

Preview without writing:

```bash
npx zodipus generate prisma/schema.prisma --dry-run
```

### Enable Debug Logging

```prisma
generator zodipus {
  debug = "true"
}
```

---

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `Cannot find module` | Not generated | `npx prisma generate` |
| `Invalid enum value` | Case mismatch | Use exact enum value |
| `Expected string, received object` | Date format | Set `dateFormat = "coerce"` |
| `Unknown model` | Wrong import | Import from `generated-index` |
| `Expected object, received array` | Missing `.array()` | Use `query.array().parse()` |
| `Property does not exist` | Not selected | Add to `select` |
| `Relation not found` | Depth too shallow | Increase `relationDepth` |

---

## Getting Help

### 1. Collect Information

```bash
# Prisma version
npx prisma --version

# Node version
node --version

# Package versions
npm list zodipus zod
```

### 2. Minimal Reproduction

Create a minimal `schema.prisma` that reproduces the issue.

### 3. Check GitHub Issues

Search existing issues: [github.com/zodipus/zodipus/issues](https://github.com/zodipus/zodipus/issues)

### 4. File a Bug Report

Include:
- Prisma schema (simplified)
- Code causing error
- Full error message
- Package versions
