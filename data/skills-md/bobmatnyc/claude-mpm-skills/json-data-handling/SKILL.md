---
name: json-data-handling
description: Working effectively with JSON data structures.
updated_at: 2025-10-30T17:00:00Z
tags: [json, data, parsing, serialization]
progressive_disclosure:
  entry_point:
    summary: "Working effectively with JSON data structures."
    when_to_use: "When working with data, databases, or data transformations."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
---
# JSON Data Handling

Working effectively with JSON data structures.

## Python

### Basic Operations

```python
import json

# Parse JSON string
data = json.loads('{"name": "John", "age": 30}')

# Convert to JSON string
json_str = json.dumps(data)

# Pretty print
json_str = json.dumps(data, indent=2)

# Read from file
with open('data.json', 'r') as f:
    data = json.load(f)

# Write to file
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Advanced

```python
# Custom encoder for datetime
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json_str = json.dumps({'date': datetime.now()}, cls=DateTimeEncoder)

# Handle None values
json.dumps(data, skipkeys=True)

# Sort keys
json.dumps(data, sort_keys=True)
```

## JavaScript

### Basic Operations

```javascript
// Parse JSON string
const data = JSON.parse('{"name": "John", "age": 30}');

// Convert to JSON string
const jsonStr = JSON.stringify(data);

// Pretty print
const jsonStr = JSON.stringify(data, null, 2);

// Read from file (Node.js)
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));

// Write to file
fs.writeFileSync('output.json', JSON.stringify(data, null, 2));
```

### Advanced

```javascript
// Custom replacer
const jsonStr = JSON.stringify(data, (key, value) => {
  if (typeof value === 'bigint') {
    return value.toString();
  }
  return value;
});

// Filter properties
const filtered = JSON.stringify(data, ['name', 'age']);

// Handle circular references
const getCircularReplacer = () => {
  const seen = new WeakSet();
  return (key, value) => {
    if (typeof value === 'object' && value !== null) {
      if (seen.has(value)) return;
      seen.add(value);
    }
    return value;
  };
};
JSON.stringify(circularObj, getCircularReplacer());
```

## Common Patterns

### Validation

```python
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number", "minimum": 0}
    },
    "required": ["name", "age"]
}

# Validate
validate(instance=data, schema=schema)
```

### Deep Merge

```python
def deep_merge(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result
```

### Nested Access

```python
# Safe nested access
def get_nested(data, *keys, default=None):
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

# Usage
value = get_nested(data, 'user', 'address', 'city', default='Unknown')
```

### Transform Keys

```python
# Convert snake_case to camelCase
def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def transform_keys(obj):
    if isinstance(obj, dict):
        return {to_camel_case(k): transform_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [transform_keys(item) for item in obj]
    return obj
```

## Best Practices

### ✅ DO

```python
# Use context managers for files
with open('data.json', 'r') as f:
    data = json.load(f)

# Handle exceptions
try:
    data = json.loads(json_str)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")

# Validate structure
assert 'required_field' in data
```

### ❌ DON'T

```python
# Don't parse untrusted JSON without validation
data = json.loads(user_input)  # Validate first!

# Don't load huge files at once
# Use streaming for large files

# Don't use eval() as alternative to json.loads()
data = eval(json_str)  # NEVER DO THIS!
```

## Streaming Large JSON

```python
import ijson

# Stream large JSON file
with open('large_data.json', 'rb') as f:
    objects = ijson.items(f, 'item')
    for obj in objects:
        process(obj)
```

## Remember
- Always validate JSON structure
- Handle parse errors gracefully
- Use schemas for complex structures
- Stream large JSON files
- Pretty print for debugging
