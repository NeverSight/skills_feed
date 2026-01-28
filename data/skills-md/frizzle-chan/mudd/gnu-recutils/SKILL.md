---
name: gnu-recutils
description: Work with GNU recutils for plain-text record databases. Use when creating, querying, or validating .rec files, defining record schemas with %rec descriptors, converting between rec/CSV formats, or when the user mentions recutils, recsel, recins, recfmt, or record-oriented data files.
---

# GNU Recutils

GNU recutils is a set of tools for managing human-readable, plain-text databases. Records are stored in `.rec` files with a simple `field: value` syntax.

## Quick Reference

### Core Commands

| Command | Purpose |
|---------|---------|
| `recsel` | Select and query records |
| `recins` | Insert new records |
| `recdel` | Delete records |
| `recset` | Modify field values |
| `recfix` | Validate, check integrity, sort |
| `recfmt` | Format output with templates |
| `recinf` | Print information about rec files |
| `rec2csv` | Convert to CSV |
| `csv2rec` | Convert from CSV |

### Basic File Format

```rec
# Comment line
Field_name: field value
Another_field: another value

Field_name: second record
Another_field: its value
```

Records are separated by blank lines. Field names are case-sensitive and conventionally capitalized.

### Multi-line Values

Use `+` continuation for multi-line content:

```rec
Description: This is the first line
+ and this continues on the second line
+ and a third line too.
```

Or use backslash at end of line:

```rec
Description: This is a long value that \
continues on the next line.
```

## Schema Definitions (%rec Descriptors)

Place schema declarations before records:

```rec
%rec: Entity
%key: Id
%mandatory: Id Name
%allowed: Id Name Prototype Description OnLook OnTouch
%type: Prototype rec Entity
%type: Count int
%type: Active bool
%unique: Name

Id: sword
Name: Iron Sword
Count: 1
Active: yes
```

### Common Descriptors

| Descriptor | Purpose | Example |
|------------|---------|---------|
| `%rec: Type` | Names the record type | `%rec: Entity` |
| `%key: field` | Primary key (unique, mandatory) | `%key: Id` |
| `%mandatory: f1 f2` | Required fields | `%mandatory: Id Name` |
| `%allowed: f1 f2` | Whitelist of valid fields | `%allowed: Id Name Desc` |
| `%prohibit: f1` | Forbidden fields | `%prohibit: Password` |
| `%unique: field` | Field must be unique | `%unique: Email` |
| `%type: field type` | Field type constraint | `%type: Count int` |
| `%auto: field` | Auto-generated field | `%auto: Created_at` |
| `%sort: field` | Default sort order | `%sort: Name` |

### Field Types

| Type | Description | Example Values |
|------|-------------|----------------|
| `int` | Integer | `42`, `-7` |
| `real` | Floating point | `3.14`, `-2.5` |
| `bool` | Boolean | `yes`, `no`, `true`, `false`, `1`, `0` |
| `line` | Single line (no newlines) | `Hello world` |
| `date` | ISO 8601 date | `2024-01-15` |
| `email` | Email address | `user@example.com` |
| `uuid` | UUID | `550e8400-e29b-41d4-a716-446655440000` |
| `rec Type` | Foreign key reference | References another record type |
| `enum A B C` | Enumeration | One of the listed values |
| `regexp /pattern/` | Regex pattern | Must match pattern |
| `size N` | Max size in bytes | String length limit |
| `range MIN MAX` | Numeric range | `range 1 100` |

### Foreign Key References

```rec
%rec: Room
%key: Id

Id: tavern
Name: The Rusty Tavern

%rec: Entity
%key: Id
%type: Room rec Room

Id: mug
Name: Beer Mug
Room: tavern
```

### Entity Containment (MUDD)

Entities can be nested using a `Container` field:

```rec
%rec: Entity
%key: Id
%type: Prototype rec Entity
%type: Container rec Entity

Id: table
Name: Wooden Table
Prototype: furniture

Id: lamp
Name: Brass Lamp
Prototype: object
Container: table
```

The lamp is "on" the table. Recfix validates that Container references exist.

## Common Operations

### Query Records

```bash
# All records
recsel data.rec

# Filter by field value
recsel -e 'Name = "sword"' data.rec

# Pattern matching
recsel -e 'Name ~ "Iron"' data.rec

# Numeric comparison
recsel -e 'Count > 5' data.rec

# Multiple conditions
recsel -e 'Type = "weapon" && Count > 0' data.rec

# Select specific fields
recsel -p Id,Name data.rec

# Count matching records
recsel -c -e 'Active = yes' data.rec

# Select by record type
recsel -t Entity data.rec
```

### Insert Records

```bash
# Insert from stdin
echo -e "Id: axe\nName: Battle Axe" | recins data.rec

# Insert with field values
recins -f Id -v sword -f Name -v "Iron Sword" data.rec
```

### Modify Records

```bash
# Update field value
recset -e 'Id = "sword"' -f Count -s 5 data.rec

# Delete field from record
recset -e 'Id = "sword"' -f Obsolete -d data.rec
```

### Delete Records

```bash
# Delete matching records
recdel -e 'Count = 0' data.rec

# Delete by record number
recdel -n 3 data.rec
```

### Validate

```bash
# Check file integrity
recfix data.rec

# Check and report all errors
recfix --check data.rec
```

### Convert Formats

```bash
# To CSV
rec2csv data.rec > data.csv

# From CSV
csv2rec data.csv > data.rec
```

### Format Output

```bash
# Custom output format
recsel data.rec | recfmt '{{Id}}: {{Name}}\n'

# Template-based formatting (recfmt reads from stdin)
recsel data.rec | recfmt -f template.fmt
```

## Expression Syntax

Used with `-e` flag in recsel, recdel, recset:

| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equals | `Name = "sword"` |
| `!=` | Not equals | `Type != "armor"` |
| `<`, `>`, `<=`, `>=` | Numeric comparison | `Count > 5` |
| `~` | Regex match | `Name ~ "^Iron"` |
| `&&` | Logical AND | `Type = "weapon" && Rare = yes` |
| `||` | Logical OR | `Type = "weapon" || Type = "armor"` |
| `!` | Logical NOT | `! (Count = 0)` |
| `#field` | Field count (0 if absent) | `#Description` |

## Tips

- Use `recfix --check` before loading data to catch schema violations
- Foreign keys (`%type: Field rec OtherType`) validate references exist
- Field names start with a letter and contain only `[a-zA-Z0-9_]`; special fields start with `%`
- Empty lines separate records; use `+ ` continuation for multi-line values
- Comments start with `#` at the beginning of a line
- For JSON output, pipe through `recsel -p` and parse with a script

## MUDD Naming Convention

In this project, entity fields use **PascalCase** (e.g., `DescriptionShort`, `OnAttack`). This avoids visual noise from underscores. See `data/entities.rec` for examples.
