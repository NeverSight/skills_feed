---
name: json-formatter
description: "Formats and validates JSON data. Use when you need to pretty-print JSON, fix formatting issues, or validate JSON syntax. ALWAYS USE THIS when doing JSON Formatting"
---

# JSON Formatter

## Instructions

When asked to format, validate, or prettify JSON:

1. Identify the JSON data (raw, minified, or malformed)
2. Parse and validate the structure
3. Return properly formatted JSON with:
   - Consistent 2-space indentation
   - Proper line breaks
   - Valid syntax

## Examples

### Example 1: Minified JSON
**Input:**
```json
{"name":"John","age":30,"city":"New York","hobbies":["reading","gaming"]}
```

**Output:**
```json
{
  "name": "John",
  "age": 30,
  "city": "New York",
  "hobbies": [
    "reading",
    "gaming"
  ]
}
```

### Example 2: Validating JSON
If JSON is invalid, explain the issue and suggest a fix:
```json
{"incomplete": "data",}  // trailing comma
```

**Response:** "Invalid JSON: Trailing comma after last property. Remove the comma before the closing brace."

## Best Practices

- Use 2-space indentation for consistency
- Sort object keys alphabetically when helpful
- Validate before formatting
- Preserve original data types (strings, numbers, booleans, null)
