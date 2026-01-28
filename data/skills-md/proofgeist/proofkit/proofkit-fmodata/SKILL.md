---
name: proofkit-fmodata
description: Type-safe FileMaker OData client with Drizzle-inspired ORM and TypeScript code generation. Use when working with FileMaker databases in TypeScript projects, querying FM data, defining typed schemas, generating types from FM layouts, or troubleshooting fmodata/typegen issues. Triggers on FileMaker + TypeScript integration tasks.
---

# ProofKit FMOData

Type-safe ORM for FileMaker's OData API with TypeScript code generation.

## Up-to-Date Documentation

For the latest docs, fetch from proofkit.dev:
- **FMOData**: `https://proofkit.dev/llms/fmodata`
- **Typegen**: `https://proofkit.dev/llms/typegen`
- **All packages**: `https://proofkit.dev/llms-full.txt`

## Quick Setup

```bash
# 1. Install packages
pnpm add @proofkit/fmodata@beta @proofkit/typegen

# 2. Create config (proofkit-typegen.config.jsonc)
npx @proofkit/typegen init

# 3. Set env vars
FM_SERVER=https://your-server.com
FM_DATABASE=YourDatabase.fmp12
OTTO_API_KEY=your-api-key  # or FM_USERNAME/FM_PASSWORD

# 4. Generate types
npx @proofkit/typegen generate

# 5. Or use interactive UI
npx @proofkit/typegen ui
```

## Define Tables

```typescript
import { fmTableOccurrence, textField, numberField, timestampField } from "@proofkit/fmodata";
import { z } from "zod";

export const Users = fmTableOccurrence("Users", {
  id: textField().primaryKey().entityId("FMFID:100001"),
  name: textField().notNull(),
  email: textField().notNull(),
  active: numberField()
    .readValidator(z.coerce.boolean())
    .writeValidator(z.boolean().transform(v => v ? 1 : 0)),
  createdAt: timestampField().readOnly(),
}, {
  entityId: "FMTID:1000001",
  navigationPaths: ["Contacts", "Orders"],
});
```

## Query Patterns

```typescript
import { FMServerConnection, eq, and, gt, asc, contains } from "@proofkit/fmodata";

const connection = new FMServerConnection({
  serverUrl: process.env.FM_SERVER,
  auth: { apiKey: process.env.OTTO_API_KEY }
});
const db = connection.database("MyDatabase.fmp12");

// List with filters
const result = await db.from(Users).list()
  .where(and(eq(Users.active, true), gt(Users.age, 18)))
  .orderBy(asc(Users.name))
  .top(10)
  .execute();

// Get single record
const user = await db.from(Users).get("user-123").execute();

// Select specific fields
const result = await db.from(Users).list()
  .select({ userId: Users.id, userName: Users.name })
  .execute();

// String filters
.where(contains(Users.email, "@example.com"))
.where(startsWith(Users.name, "John"))
```

## CRUD Operations

```typescript
// Insert
const result = await db.from(Users)
  .insert({ name: "John", email: "john@example.com" })
  .execute();

// Update
const result = await db.from(Users)
  .update({ name: "Jane" })
  .byId("user-123")
  .execute();

// Delete
const result = await db.from(Users)
  .delete()
  .byId("user-123")
  .execute();

// Batch operations (atomic)
const result = await db.batch([
  db.from(Users).list().top(10),
  db.from(Users).insert({ name: "Alice", email: "alice@example.com" }),
]).execute();
```

## Relationships

```typescript
// Expand related records
const result = await db.from(Users).list()
  .expand(Contacts, (b) =>
    b.select({ name: Contacts.name })
     .where(eq(Contacts.active, true))
  )
  .execute();

// Navigate from a record
const result = await db.from(Contacts).get("contact-123")
  .navigate(Users)
  .select({ username: Users.username })
  .execute();
```

## Error Handling

```typescript
import { isHTTPError, ValidationError, TimeoutError } from "@proofkit/fmodata";

const result = await db.from(Users).list().execute();

if (result.error) {
  if (isHTTPError(result.error)) {
    if (result.error.isNotFound()) console.log("Not found");
    if (result.error.is5xx()) console.log("Server error");
  } else if (result.error instanceof ValidationError) {
    console.log("Validation failed:", result.error.issues);
  } else if (result.error instanceof TimeoutError) {
    console.log("Request timed out");
  }
}
```

## Troubleshooting

### Connection Issues

**"Unauthorized" or 401 errors**
- Verify `OTTO_API_KEY` or `FM_USERNAME`/`FM_PASSWORD` env vars
- Ensure FM account has `fmodata` privilege enabled
- Check OData service is enabled on FM Server

**"Not Found" or 404 errors**
- Verify database name includes `.fmp12` extension
- Check table/layout name matches exactly (case-sensitive)
- Ensure OData is enabled for the table occurrence

### Type Generation Issues

**typegen can't connect**
- Run `npx @proofkit/typegen ui` to debug interactively
- Check connection health indicator in UI
- Verify env vars are loaded (check `--env-path` flag)

**Generated types don't match FM schema**
- Re-run `npx @proofkit/typegen generate` after FM schema changes
- Use `--reset-overrides` to recreate override files
- Check field type mappings in config

### Query Issues

**"Field not found" errors**
- Ensure field is defined in `fmTableOccurrence`
- Check `entityId` matches FM field ID (use typegen to auto-generate)
- Verify field is on the OData-exposed table occurrence

**Validation errors on read/write**
- Check `readValidator`/`writeValidator` schemas match FM data types
- FM stores booleans as 0/1 numbers - use coercion validators
- Empty strings may need `.catch("")` or `.nullable()`

### Performance Issues

**Slow queries**
- Add `.top(n)` to limit results
- Use `.select()` to fetch only needed fields
- Avoid expanding large related record sets

## References

- **[fmodata-api.md](references/fmodata-api.md)** - Complete API reference: field builders, operators, query methods
- **[typegen-config.md](references/typegen-config.md)** - Configuration options and examples
