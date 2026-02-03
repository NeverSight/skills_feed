---
name: nitro-datastore
description: Use when working with JSON data in Python - nested dictionary access, querying collections, bulk transformations, or file-based config management
---

# Nitro DataStore

Schema-agnostic JSON data store for Python with multiple access patterns.

## Installation

```bash
pip install nitro-datastore
```

## Quick Reference

| Access Pattern | Syntax | Best For |
|----------------|--------|----------|
| Dot notation | `data.site.name` | Static keys |
| Dictionary | `data['site']['name']` | Kebab-case keys, dynamic access |
| Path-based | `data.get('site.name', default)` | Dynamic paths, defaults |

## Core Patterns

### Creating and Loading

```python
from nitro_datastore import NitroDataStore

# From dict
data = NitroDataStore({'site': {'name': 'Nitro'}})

# From file
data = NitroDataStore.from_file('config.json')

# From directory (auto-merges alphabetically)
data = NitroDataStore.from_directory('data/')
```

### Reading Values

```python
# Dot notation (returns NitroDataStore for nested dicts)
data.site.name

# Path with default
data.get('site.theme.colors.primary', '#000')

# Multiple values
data.get_many(['site.name', 'site.url'])
```

### Writing Values

```python
# Dot notation
data.site.name = 'New Name'

# Path-based (creates intermediate dicts)
data.set('config.cache.ttl', 3600)

# Merge another datastore
data.merge(other_data)
```

### Query Builder

```python
results = (data.query('posts')
    .where(lambda p: p.get('published'))
    .sort(key=lambda p: p.get('views'), reverse=True)
    .limit(10)
    .execute())

# Utilities
count = data.query('posts').where(...).count()
first = data.query('posts').first()
titles = data.query('posts').pluck('title')
by_category = data.query('posts').group_by('category')
```

### Bulk Operations

```python
# Update matching values
count = data.update_where(
    condition=lambda path, value: 'http://' in str(value),
    transform=lambda value: value.replace('http://', 'https://')
)

# Clean up
data.remove_nulls()
data.remove_empty()
```

### Path Discovery

```python
# List all paths
paths = data.list_paths()
paths = data.list_paths(prefix='site')

# Glob patterns
titles = data.find_paths('posts.*.title')
urls = data.find_paths('**.url')

# Find by key name
all_urls = data.find_all_keys('url')

# Find by value predicate
emails = data.find_values(lambda v: isinstance(v, str) and '@' in v)
```

### Transformations

```python
# Transform all values (returns new instance)
upper = data.transform_all(
    lambda path, value: value.upper() if isinstance(value, str) else value
)

# Transform keys
snake_case = data.transform_keys(lambda k: k.replace('-', '_'))
```

### File Output

```python
data.save('output.json', indent=2)
plain_dict = data.to_dict()
```

## Common Gotchas

| Issue | Problem | Solution |
|-------|---------|----------|
| Kebab-case keys | `data.user-name` invalid Python | Use `data['user-name']` |
| Dots in keys | `data.get('key.with.dots')` looks for nested | Use `data['key.with.dots']` |
| Transform mutability | `data.transform_keys(...)` doesn't mutate | Assign result: `data = data.transform_keys(...)` |
| Nested access returns | `data.site` returns `NitroDataStore` | Use `.to_dict()` for plain dict |

## Security Features

```python
# Path traversal protection
data = NitroDataStore.from_file(path, base_dir='/safe/dir')

# File size limits
data = NitroDataStore.from_file(path, max_size=10*1024*1024)
```
