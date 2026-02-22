---
name: dart-best-practices
description: |-
  General best practices for Dart development.
  Covers code style, effective Dart, and language features.
license: Apache-2.0
---

# Dart Best Practices

## 1. When to use this skill
Use this skill when:
-   Writing or reviewing Dart code.
-   Looking for guidance on idiomatic Dart usage.

## 2. Best Practices

### Multi-line Strings
Prefer using multi-line strings (`'''`) over concatenating strings with `+` and
`\n`, especially for large blocks of text like SQL queries, HTML, or
PEM-encoded keys. This improves readability and avoids
`lines_longer_than_80_chars` lint errors by allowing natural line breaks.

**Avoid:**
```dart
final pem = '-----BEGIN RSA PRIVATE KEY-----\n' +
    base64Encode(fullBytes) +
    '\n-----END RSA PRIVATE KEY-----';
```

**Prefer:**
```dart
final pem = '''
-----BEGIN RSA PRIVATE KEY-----
${base64Encode(fullBytes)}
-----END RSA PRIVATE KEY-----''';
```

### Robust extractions of values from a Map with Switch Expressions
When parsing `Map` structures or JSON (e.g., from `jsonDecode`), use switch
expressions with object patterns for deep validation and extraction. This is
clearer and safer than manual `is` checks or `as` casts.

**Avoid (Unsafe Access):**
```dart
final json = jsonDecode(stdout);
if (json is Map &&
    json['configuration'] is Map &&
    json['configuration']['properties'] is Map &&
    json['configuration']['properties']['core'] is Map) {
  return json['configuration']['properties']['core']['project'] as String?;
}
return null;
```

**Prefer (Deep Pattern Matching):**
```dart
return switch (jsonDecode(stdout)) {
  {
    'configuration': {
      'properties': {'core': {'project': final String project}},
    },
  } =>
    project,
  _ => null,
};
```

This pattern cleanly handles deeply nested structures and nullable fields
without the complexity of verbose `if-else` blocks or the risk of runtime cast
errors.

### Line Length
Avoid lines longer than 80 characters, even in Markdown files and comments.
This ensures code is readable in split-screen views and on smaller screens
without horizontal scrolling.

**Prefer:**
Target 80 characters for wrapping text. Exceptions are allowed for long URLs
or identifiers that cannot be broken.
