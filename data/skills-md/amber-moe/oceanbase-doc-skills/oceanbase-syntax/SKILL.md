---
name: oceanbase-syntax
description: Write SQL syntax definitions for OceanBase documentation. Syntax sections define structure without semicolons, while examples show executable statements. Use when writing syntax sections or reviewing SQL statement documentation.
license: MIT
metadata:
  audience: technical-writers
  domain: sql-syntax
---

# OceanBase SQL Syntax Documentation

This skill provides guidelines for writing SQL syntax sections in OceanBase documentation.

## Key principle

**Syntax sections define structure, not executable statements.**

## Syntax section rules

### No semicolons

Syntax definitions end WITHOUT semicolons:

**Correct:**

```sql
ALTER SYSTEM KILL SESSION 'session_id, serial#'

ALTER SYSTEM KILL SESSION 'session_id' [IMMEDIATE]
```

**Incorrect:**

```sql
ALTER SYSTEM KILL SESSION 'session_id, serial#';

ALTER SYSTEM KILL SESSION 'session_id' [IMMEDIATE];
```

### Why no semicolons?

- Syntax sections explain format and structure
- They are not directly executable statements
- Semicolons are statement terminators, not part of syntax definition
- Examples section shows executable statements with semicolons

## Syntax notation

### Optional parameters

Use square brackets `[]` for optional parameters:

```sql
ALTER SYSTEM KILL SESSION 'session_id' [IMMEDIATE]
```

### Multiple options

Use pipe `|` for alternatives:

```sql
CREATE TABLE table_name (
    column_name data_type [NOT NULL | NULL]
)
```

### Repetition

Use `...` for repeating elements:

```sql
CREATE TABLE table_name (
    column_name data_type,
    ...
)
```

### Required vs optional

- No brackets = required
- `[brackets]` = optional
- `{braces}` = required group (if used)
- `|` = alternative choice

## Syntax section structure

### Basic format

```markdown
## Syntax

```sql
STATEMENT_NAME parameter1 [optional_parameter]
```
```

### Complex syntax

For multi-line syntax:

```sql
CREATE TABLE table_name (
    column_name data_type [column_constraint],
    ...
) [table_option]
```

### Multiple syntax variants

When multiple forms exist:

```sql
ALTER SYSTEM KILL SESSION 'session_id, serial#';

ALTER SYSTEM KILL SESSION 'session_id' [IMMEDIATE];
```

Note: Even in syntax section, show variants with semicolons separated, but the syntax definition itself doesn't need semicolons if showing the pattern.

## Examples section

**Examples ARE executable and include semicolons:**

```sql
obclient [KILL_USER]> ALTER SYSTEM KILL SESSION '3221487726';
```

## Parameter descriptions

After syntax, provide parameter table:

| Parameter | Description |
|-----------------|------------------------------------------------------------|
| session_id | The Client Session ID of the current session. |
| serial# | This parameter is not implemented in the current version and is reserved only for syntax compatibility. |
| IMMEDIATE | Immediately switches back to the specified session to execute `KILL`. This parameter is optional. |

## Common patterns

### Simple statement

```sql
SHOW PROCESSLIST
```

### With options

```sql
SHOW [FULL] PROCESSLIST
```

### With multiple clauses

```sql
CREATE TABLE table_name (
    column_definition,
    ...
) [table_options]
```

### With subclauses

```sql
ALTER TABLE table_name
    ADD column_name data_type [AFTER existing_column]
```

## Testing syntax

**Important:** When sql_parser files and test cases differ:

- **Follow test cases** - they reflect actual functionality
- Test cases show what users can actually use
- Document real, working syntax

## Quality checklist

- [ ] Syntax section has NO semicolons
- [ ] Examples section HAS semicolons
- [ ] Optional parameters in brackets
- [ ] Clear notation for alternatives
- [ ] Parameter table provided
- [ ] Syntax matches test cases (not just parser)
- [ ] Formatting is consistent

## Common mistakes

### ❌ Adding semicolons to syntax

```sql
ALTER SYSTEM KILL SESSION 'session_id';  # Wrong
```

### ❌ Mixing syntax and examples

Don't show executable examples in syntax section.

### ❌ Inconsistent notation

Use consistent notation throughout:

- `[]` for optional
- `|` for alternatives
- `...` for repetition

## Best practices

1. **Keep syntax concise** - show structure, not implementation details
2. **Use clear notation** - standard SQL syntax notation
3. **Provide parameter table** - explain each parameter
4. **Match test cases** - document what actually works
5. **Separate syntax from examples** - different sections, different rules
