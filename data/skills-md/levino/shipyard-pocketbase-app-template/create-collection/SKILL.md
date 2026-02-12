---
name: create-collection
description: Use this skill when you need to alter the PocketBase database schema - creating, updating, or deleting collections. Never write migration SQL by hand.
allowed-tools: Read, Write, Bash
---

# PocketBase Collection Management

Use this skill whenever you need to modify the database schema (create/update/delete collections).

## Why This Approach

PocketBase automatically generates migration files when collections are created/modified via the SDK. This ensures:
- Correct internal IDs
- Proper migration format
- Automatic rollback functions
- No manual SQL errors

## Instructions

### 1. Get the PocketBase URL

Find the container IP:
```bash
docker network inspect shipyard-pocketbase-template_default --format '{{range .Containers}}{{.IPv4Address}}{{end}}'
```

### 2. Write a Temporary Script

Create a temp JS file (e.g., `temp-collection.js`):

```javascript
import PocketBase from 'pocketbase'

const pb = new PocketBase('http://<CONTAINER_IP>:8090')

await pb.collection('_superusers').authWithPassword('admin@test.local', 'testtest123')

// CREATE a collection
await pb.collections.create({
  name: 'my_collection',
  type: 'base',  // or 'auth' for user collections
  fields: [
    { name: 'title', type: 'text', required: true },
    { name: 'completed', type: 'bool' },
    { name: 'user_id', type: 'text', required: true },
  ],
  listRule: '@request.auth.id != ""',
  viewRule: '@request.auth.id != ""',
  createRule: '@request.auth.id != ""',
  updateRule: 'user_id = @request.auth.id',
  deleteRule: 'user_id = @request.auth.id',
})

// UPDATE a collection
// const collection = await pb.collections.getOne('my_collection')
// await pb.collections.update(collection.id, { name: 'new_name' })

// DELETE a collection
// await pb.collections.delete('my_collection')

console.log('Done!')
```

### 3. Run the Script

```bash
node temp-collection.js
```

### 4. Verify Migration Was Created

```bash
ls -la pocketbase/pb_migrations/
```

You should see a new `.js` file with the timestamp and collection name.

### 5. Delete the Temp Script

```bash
rm temp-collection.js
```

## Field Types

Common field types for `pb.collections.create()`:
- `text` - String field
- `bool` - Boolean
- `number` - Numeric
- `email` - Email validation
- `url` - URL validation
- `date` - Date/datetime
- `select` - Enum (add `values: ['a', 'b']`)
- `relation` - Foreign key (add `collectionId: 'xxx'`)
- `file` - File upload
- `json` - JSON data

## Rules

Access rules use PocketBase filter syntax:
- `null` - Superusers only
- `''` (empty string) - Anyone
- `'@request.auth.id != ""'` - Authenticated users
- `'user_id = @request.auth.id'` - Owner only
