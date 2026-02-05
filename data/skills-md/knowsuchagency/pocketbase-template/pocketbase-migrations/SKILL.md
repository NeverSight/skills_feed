---
name: pocketbase-migrations
description: Comprehensive guide for PocketBase migrations (0.20+) using Go-based migration system. Use when creating or modifying PocketBase collections, managing fields, setting up relations, or writing migration files.
---

# PocketBase Migrations

Guide for creating PocketBase migrations using the Go-based system (0.20+).

## Core Workflow

### Critical Migration Pattern

**ALWAYS follow this workflow:**

1. Write ONE migration at a time
2. Execute immediately with `mise run migrate`
3. Verify it worked with `mise run show-collections`
4. Only then write the next migration
5. Run `mise run backup` before destructive changes

**Never write multiple migrations without running them between each one.**

## Migration Structure

```go
package migrations

import (
    "github.com/pocketbase/pocketbase/core"
    "github.com/pocketbase/pocketbase/tools/types"
    m "github.com/pocketbase/pocketbase/migrations"
)

func init() {
    m.Register(func(app core.App) error {
        // Up migration
        return nil
    }, func(app core.App) error {
        // Down migration
        return nil
    })
}
```

## Collection Operations

### Create Base Collection

```go
collection := core.NewBaseCollection("posts")

// Add fields
collection.Fields.Add(&core.TextField{
    Name: "title",
    Required: true,
    Max: 100,
})

// Set rules (use types.Pointer())
collection.ListRule = types.Pointer("@request.auth.id != ''")
collection.CreateRule = types.Pointer("@request.auth.id != ''")
collection.UpdateRule = types.Pointer("@request.auth.id = author")
collection.DeleteRule = types.Pointer("@request.auth.id = author")

return app.Save(collection)
```

### Update Existing Collection

```go
collection, err := app.FindCollectionByNameOrId("posts")
if err != nil {
    return err
}

// Add field
collection.Fields.Add(&core.DateField{
    Name: "publishedAt",
})

// Remove field
collection.Fields.RemoveByName("oldField")

// Update rules
collection.UpdateRule = types.Pointer("@request.auth.id = author")

return app.Save(collection)
```

## Common Field Types

See [references/field-types.md](references/field-types.md) for complete field type reference.

### Quick Reference

```go
// Text
&core.TextField{Name: "title", Required: true, Max: 100}

// Number
&core.NumberField{Name: "price", Min: types.Pointer(0.0)}

// Boolean
&core.BoolField{Name: "isActive"}

// Email
&core.EmailField{Name: "email", Required: true}

// Date
&core.DateField{Name: "publishedAt"}

// Auto-managed date
&core.AutodateField{Name: "created", OnCreate: true}

// Select
&core.SelectField{
    Name: "status",
    Values: []string{"draft", "published"},
    MaxSelect: 1,
}

// File
&core.FileField{
    Name: "avatar",
    MaxSelect: 1,
    MaxSize: 5242880, // bytes
}

// Editor (rich text)
&core.EditorField{
    Name: "content",
    MaxSize: 1048576,
}

// JSON
&core.JSONField{Name: "metadata", MaxSize: 65535}
```

## Working with Relations

### Best Practices

1. Create collections in dependency order
2. Fetch collections before creating relations
3. Use actual collection IDs for relations
4. Handle self-referencing relations in separate migrations

### Relation Field

```go
// Fetch the target collection first
authorsCollection, err := app.FindCollectionByNameOrId("authors")
if err != nil {
    return err
}

// Add relation field
collection.Fields.Add(&core.RelationField{
    Name: "author",
    Required: true,
    MaxSelect: 1,  // Note: use MaxSelect, not Max
    CollectionId: authorsCollection.Id,
    CascadeDelete: true,
})

// System users collection
collection.Fields.Add(&core.RelationField{
    Name: "creator",
    CollectionId: "_pb_users_auth_",
    MaxSelect: 1,
})
```

### Migration Order for Relations

Create collections in this order:

1. Independent collections (no relations)
2. Collections depending on system collections
3. Collections with relations to other custom collections
4. Self-referencing relations (separate migration)

Example order:
```
1_create_categories.go       # Independent
2_create_authors.go          # Depends on system users
3_create_posts.go           # Depends on authors & categories
4_create_comments.go        # Depends on posts & users
5_add_parent_to_comments.go # Self-referencing
```

## Collection Rules

### Rule Types

- `ListRule` - List records
- `ViewRule` - View individual records
- `CreateRule` - Create records
- `UpdateRule` - Update records
- `DeleteRule` - Delete records

### Common Patterns

```go
// Public access
types.Pointer("")

// Authenticated only
types.Pointer("@request.auth.id != ''")

// Owner only
types.Pointer("@request.auth.id = author")

// Published or owner
types.Pointer("status = 'published' || author = @request.auth.id")

// Through relations
types.Pointer("author.user = @request.auth.id")
```

## View Collections

```go
viewQuery := `
SELECT 
    posts.id,
    posts.title,
    users.name as author_name
FROM posts
JOIN users ON posts.author = users.id
`
collection := core.NewViewCollection("posts_with_authors", viewQuery)
return app.Save(collection)
```

## Error Handling

Always check errors:

```go
collection, err := app.FindCollectionByNameOrId("posts")
if err != nil {
    return err
}

if err := app.Save(collection); err != nil {
    return err
}
```

## Task Commands

- `mise run makemigration <name>` - Create new migration file
- `mise run migrate` - Run pending migrations
- `mise run migratedown` - Rollback last migration
- `mise run show-collections` - Display collections
- `mise run backup` - Backup database to /tmp

## Best Practices

1. **Import types package** for nullable values: `"github.com/pocketbase/pocketbase/tools/types"`
2. **Use `types.Pointer()`** for rule assignments and pointer values
3. **Check collection existence** before creating relations
4. **Validate field names** don't conflict with system fields (id, created, updated)
5. **Handle errors immediately** after operations
6. **Never skip migration testing** - run each one before writing the next
7. **Backup before destructive changes**

## Common Gotchas

- Use `MaxSelect` (not `Max`) for RelationField
- Use `MaxSize` (not `Max`) for EditorField
- System users collection ID: `"_pb_users_auth_"`
- For number min/max: `types.Pointer(0.0)`
- Empty rules need: `types.Pointer("")`
- Self-referencing relations need separate migrations

## Additional Resources

- Field types reference: [references/field-types.md](references/field-types.md)
- Official docs: https://pocketbase.io/docs/go-collections/
