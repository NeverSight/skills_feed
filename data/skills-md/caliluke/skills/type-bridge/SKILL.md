---
name: type-bridge
description: Use the type-bridge Python ORM for TypeDB. Covers the code generator (preferred), entities, relations, attributes, CRUD operations, queries, and schema management. Use when working with TypeDB in Python projects.
---

# type-bridge Python ORM for TypeDB

type-bridge is a Pythonic ORM for TypeDB that provides type-safe abstractions over TypeQL.

## Recommended Workflow: Use the Code Generator

**Always use the code generator** to create Python models from TypeQL schema files. Do not manually write Entity/Relation/Attribute classes—generate them instead.

```text
schema.tql  →  generator  →  attributes.py, entities.py, relations.py
```

### Quick Start with Generator

```bash
# Generate models from your TypeQL schema
python -m type_bridge.generator schema.tql -o ./myapp/models/

# With options
python -m type_bridge.generator schema.tql \
    --output ./myapp/models/ \
    --version 2.0.0 \
    --implicit-keys id
```

### Example Schema (schema.tql)

```typeql
define

# Attributes
attribute name, value string;
attribute email, value string;
attribute age, value integer;

# Entities
entity person,
    owns name @key,
    owns email @unique,
    owns age,
    plays employment:employee;

entity company,
    owns name @key,
    plays employment:employer;

# Relations
relation employment,
    relates employee,
    relates employer,
    owns start-date,
    owns end-date;

attribute start-date, value date;
attribute end-date, value date;
```

### Using Generated Models

```python
from myapp.models import entities, attributes
from type_bridge import Database, SchemaManager

# Connect and sync schema
db = Database(address="localhost:1729", database="mydb")
with db:
    db.create_database()
    schema = SchemaManager(db)
    schema.register(entities.Person, entities.Company)
    schema.sync_schema()

    # CRUD operations using generated classes
    manager = entities.Person.manager(db)
    alice = entities.Person(
        name=attributes.Name("Alice"),
        email=attributes.Email("alice@example.com"),
        age=attributes.Age(30)
    )
    manager.insert(alice)
```

---

## Code Generator Reference

### CLI Options

```text
Usage: python -m type_bridge.generator [OPTIONS] SCHEMA

Arguments:
  SCHEMA  Path to the TypeDB schema file (.tql) [required]

Options:
  -o, --output PATH       Output directory for generated package [required]
  --version TEXT          Schema version string [default: 1.0.0]
  --no-copy-schema        Don't copy the schema file to the output directory
  --implicit-keys TEXT    Attribute names to treat as @key even if not marked
  --help                  Show this message and exit
```

### Programmatic Usage

```python
from type_bridge.generator import generate_models

# From a file path
generate_models("schema.tql", "./myapp/models/")

# From schema text
schema = """
define
entity person, owns name @key;
attribute name, value string;
"""
generate_models(schema, "./myapp/models/")
```

### Generated Package Structure

```text
myapp/models/
├── __init__.py      # Package exports, SCHEMA_VERSION, schema_text()
├── attributes.py    # Attribute class definitions
├── entities.py      # Entity class definitions
├── relations.py     # Relation class definitions
├── structs.py       # Struct definitions (if schema has structs)
├── registry.py      # Pre-computed schema metadata
└── schema.tql       # Copy of original schema
```

### TypeQL to Python Mapping

| TypeQL                          | Generated Python                                   |
| ------------------------------- | -------------------------------------------------- |
| `attribute name, value string;` | `class Name(String): ...`                          |
| `@key`                          | `name: Name = Flag(Key)`                           |
| `@unique`                       | `email: Email = Flag(Unique)`                      |
| `@card(0..1)` or no annotation  | `age: Age \| None = None`                          |
| `@card(1)`                      | `name: Name` (required)                            |
| `@card(0..)`                    | `tags: list[Tag] = Flag(Card(min=0))`              |
| `@card(1..)`                    | `phones: list[Phone] = Flag(Card(min=1))`          |
| `@abstract`                     | `flags = TypeFlags(name="...", abstract=True)`     |
| `sub parent`                    | `class Child(Parent): ...`                         |
| `@regex("...")`                 | `regex: ClassVar[str] = r"..."`                    |
| `@values(...)`                  | `allowed_values: ClassVar[tuple] = (...)`          |
| `@range(0..150)`                | `range_constraint: ClassVar[tuple] = ("0", "150")` |

### Best Practices

1. **Keep generated code separate** from hand-written code
2. **Regenerate after schema changes**—don't edit generated files
3. **Version control the schema**, optionally the generated code
4. **Use `--implicit-keys`** for convention-based keys (e.g., `id`)

```gitignore
# Option A: Regenerate from schema.tql
myapp/models/

# Option B: Version control both, verify in CI
# python -m type_bridge.generator schema.tql -o ./myapp/models/
# git diff --exit-code myapp/models/
```

---

## Understanding Generated Models

The following sections explain the generated code structure for reference. **Do not write these classes manually—use the generator.**

### Supported Value Types

TypeBridge supports all TypeDB value types:

| TypeQL        | Python Base Class | Python Type                    |
| ------------- | ----------------- | ------------------------------ |
| `string`      | `String`          | `str`                          |
| `integer`     | `Integer`         | `int`                          |
| `double`      | `Double`          | `float`                        |
| `decimal`     | `Decimal`         | `decimal.Decimal`              |
| `boolean`     | `Boolean`         | `bool`                         |
| `date`        | `Date`            | `datetime.date`                |
| `datetime`    | `DateTime`        | `datetime.datetime`            |
| `datetime-tz` | `DateTimeTZ`      | `datetime.datetime` (tz-aware) |
| `duration`    | `Duration`        | `isodate.Duration`             |

### Attribute Types

Generated from `attribute` definitions:

```python
# Generated from: attribute name, value string;
class Name(String):
    flags = AttributeFlags(name="name")

# Generated from: attribute age, value integer @range(0..150);
class Age(Integer):
    flags = AttributeFlags(name="age")
    range_constraint: ClassVar[tuple[str | None, str | None]] = ("0", "150")

# Generated from: attribute balance, value decimal;
class Balance(Decimal):
    flags = AttributeFlags(name="balance")

# Generated from: attribute updated-at, value datetime-tz;
class UpdatedAt(DateTimeTZ):
    flags = AttributeFlags(name="updated-at")
```

### Entities

Generated from `entity` definitions:

```python
# Generated from: entity person, owns name @key, owns age;
class Person(Entity):
    flags = TypeFlags(name="person")
    name: Name = Flag(Key)
    age: Age | None = None
```

### Relations

Generated from `relation` definitions:

```python
# Generated from: relation employment, relates employee, relates employer;
class Employment(Relation):
    flags = TypeFlags(name="employment")
    employee: Role[Person] = Role("employee", Person)
    employer: Role[Company] = Role("employer", Company)
```

---

## CRUD Operations

### Entity Manager

```python
# Get manager for an entity type
manager = Person.manager(db)

# Insert single
alice = Person(name=Name("Alice"), email=Email("alice@example.com"))
manager.insert(alice)

# Bulk insert (more efficient)
persons = [Person(name=Name("Bob")), Person(name=Name("Charlie"))]
manager.insert_many(persons)

# Get all
all_persons = manager.all()

# Filter with expressions
seniors = manager.filter(Person.age.gte(Age(65))).execute()

# Get first match
first = manager.filter(name=Name("Alice")).first()

# Count
total = manager.filter().count()

# Update (fetch → modify → update)
alice = manager.filter(name=Name("Alice")).first()
alice.age = Age(31)
manager.update(alice)

# Delete
manager.delete(alice)

# Put (idempotent insert - safe to run multiple times)
manager.put(Person(name=Name("Bob"), email=Email("bob@example.com")))
manager.put_many(persons)  # Bulk idempotent insert
```

### Bulk Operations

```python
# Bulk insert (single transaction, much faster)
manager.insert_many([person1, person2, person3])

# Bulk update
people[0].age = Age(31)
people[1].age = Age(41)
manager.update_many(people)

# Bulk delete (idempotent by default)
deleted = manager.delete_many([alice, bob])  # Returns actually-deleted entities
deleted = manager.delete_many([alice, bob], strict=True)  # Raises if any missing

# Chainable bulk operations
count = manager.filter(Person.age.gt(Age(65))).delete()  # Returns count
updated = manager.filter(Person.age.gt(Age(30))).update_with(
    lambda p: setattr(p, 'status', Status("senior"))
)  # Returns updated entities
```

### Relation Manager

```python
# Get manager for relation type
emp_manager = Employment.manager(db)

# Insert relation (entities must exist)
alice = Person(name=Name("Alice"))
acme = Company(name=Name("Acme"))
employment = Employment(
    employee=alice,
    employer=acme,
    start_date=StartDate(date(2024, 1, 15))
)
emp_manager.insert(employment)

# Query relations
acme_employees = emp_manager.filter(employer=acme).execute()

# Filter by role player attributes
results = emp_manager.filter(Employment.employee.age.gte(Age(30))).execute()
```

### Multi-Player Roles

```python
# Role that accepts multiple entity types
class Trace(Relation):
    flags = TypeFlags(name="trace")
    origin: Role[Document | Email] = Role.multi("origin", Document, Email)

# Access attributes from any player type
Trace.origin.name      # From Document
Trace.origin.subject   # From Email
```

### Transactions

```python
# Explicit transaction for multiple operations
from typedb.driver import TransactionType

with db.transaction(TransactionType.WRITE) as tx:
    person_mgr = Person.manager(tx)
    company_mgr = Company.manager(tx)

    person_mgr.insert(alice)
    company_mgr.insert(acme)
    # Auto-commits on exit, rolls back on exception
```

---

## Query Expressions

### Comparison Expressions

```python
# Available on all attribute field references
Person.age.eq(Age(30))      # ==
Person.age.neq(Age(30))     # !=
Person.age.gt(Age(18))      # >
Person.age.gte(Age(18))     # >=
Person.age.lt(Age(65))      # <
Person.age.lte(Age(65))     # <=

# String-specific
Person.name.contains(Name("Ali"))
Person.name.like(Name("^A.*"))    # Regex match

# Chaining filters (AND)
manager.filter(Person.age.gte(Age(18))).filter(Person.age.lt(Age(65))).execute()
```

### Django-Style Lookups

```python
# Filter with suffix operators (convenient alternative to expressions)
people = manager.filter(name__startswith="Al", age__gt=30).execute()
gmail = manager.filter(email__contains="@gmail.com").execute()
seniors = manager.filter(age__gte=65).execute()

# Available lookups:
# __contains, __startswith, __endswith, __regex  (strings)
# __gt, __gte, __lt, __lte, __eq                 (comparisons)
# __in=[v1, v2, v3]                              (membership)
# __isnull=True|False                            (null check)

# Examples
manager.filter(status__in=["active", "pending"]).execute()
manager.filter(age__isnull=True).execute()  # Missing age
manager.filter(city__regex="^New.*York$").execute()
```

### Sorting Results

```python
# Ascending (default)
results = manager.filter().order_by('age').execute()

# Descending (prefix with '-')
results = manager.filter().order_by('-age').execute()

# Multiple fields
results = manager.filter().order_by('city', '-age').execute()

# Role-player attributes (relations only)
results = emp_manager.filter().order_by('employee__age').execute()
results = emp_manager.filter().order_by('-employer__name').execute()
```

### Boolean Expressions

```python
# OR using method chaining
young_or_old = manager.filter(
    Person.age.lt(Age(25)).or_(Person.age.gt(Age(60)))
).execute()

# AND (explicit)
senior_engineers = manager.filter(
    Person.department.eq(Department("Engineering")).and_(
        Person.job_title.contains(JobTitle("Senior"))
    )
).execute()

# NOT
non_sales = manager.filter(
    Person.department.eq(Department("Sales")).not_()
).execute()
```

### Aggregations

```python
# Single aggregation
result = manager.filter().aggregate(Person.age.avg())
avg_age = result["avg_age"]

# Multiple aggregations
result = manager.filter().aggregate(
    Person.age.avg(),
    Person.salary.sum(),
    Person.score.max()
)

# Available: .avg(), .sum(), .min(), .max(), .count(), .std(), .median()
```

### Group By

```python
# Group by single field
result = manager.group_by(Person.department).aggregate(
    Person.salary.avg(),
    Person.age.avg()
)
# Returns: {"Engineering": {"avg_salary": 95000, "avg_age": 32}, ...}

# Group by multiple fields
result = manager.group_by(Person.department, Person.level).aggregate(
    Person.salary.avg()
)
```

### Pagination

```python
# Limit and offset
page = manager.filter().limit(10).offset(20).execute()

# Combined with sorting (recommended for stable pagination)
page = manager.filter().order_by('age').limit(10).offset(0).execute()

# First N results
top_5 = manager.filter(Person.score.gte(Score(90))).limit(5).execute()
```

---

## Schema Management

```python
from type_bridge import SchemaManager

schema = SchemaManager(db)

# Register models
schema.register(Person, Company, Employment)

# Sync schema (creates types in TypeDB)
schema.sync_schema()

# Force sync (recreates even if exists)
schema.sync_schema(force=True)

# Get current schema
current = schema.get_schema()

# Compare schemas
from type_bridge import SchemaDiff
diff = SchemaDiff.compare(old_schema, new_schema)
```

---

## Built-in Functions (TypeDB 3.8+)

```python
from type_bridge.expressions import iid, label

# These are used internally by type-bridge for IID and type fetching
# The library handles this automatically in manager operations

# Direct usage in custom queries:
expr = iid("$e")       # Generates: iid($e)
expr = label("$t")     # Generates: label($t)

# IMPORTANT: label() only works on TYPE variables, not instance variables
# Pattern: $e isa! $t; $t sub person; ... label($t)
```

---

## Common Patterns

### Get by IID

```python
# Fetch entity by internal ID (fast direct lookup)
person = manager.get_by_iid("0x1e00000000000000000123")
```

### Polymorphic Queries

```python
# Query abstract type to get all subtypes
class Animal(Entity):
    flags = TypeFlags(name="animal", abstract=True)

class Dog(Animal):
    flags = TypeFlags(name="dog")

class Cat(Animal):
    flags = TypeFlags(name="cat")

# Gets both Dogs and Cats
animal_manager = Animal.manager(db)
all_animals = animal_manager.all()
```

### Serialization

```python
# Convert to dict
person_dict = person.to_dict()

# Create from dict
person = Person.from_dict(person_dict)
```

### Raw Queries

```python
# Execute raw TypeQL
results = db.execute_query("""
    match $p isa person, has name $n;
    fetch { "name": $n };
""", "read")
```

---

## Cardinality Flags

```python
from type_bridge import Flag, Key, Unique, Card

class Person(Entity):
    # Key: exactly one, unique identifier
    id: PersonId = Flag(Key)

    # Unique: exactly one, unique but not key
    email: Email = Flag(Unique)

    # Card(0..1): optional (0 or 1)
    nickname: Nickname | None = Flag(Card(max=1))

    # Card(1..): at least one required
    phone: Phone = Flag(Card(min=1))

    # Card(0..): zero or more (default for lists)
    tags: list[Tag] = Flag(Card(min=0))

    # Card(2..5): between 2 and 5
    references: list[Reference] = Flag(Card(min=2, max=5))
```

---

## Instance Methods

Entities and relations have convenience methods for CRUD operations:

```python
# Insert using instance method
alice = Person(name=Name("Alice"), age=Age(30))
alice.insert(db)  # Returns alice for chaining

# Delete using instance method
alice.delete(db)  # Returns alice for chaining

# Chaining
Person(name=Name("Temp")).insert(db).delete(db)

# Serialization
data = alice.to_dict()  # {'name': 'Alice', 'age': 30}
alice = Person.from_dict(data)
```

---

## Exception Handling

```python
from type_bridge import EntityNotFoundError, KeyAttributeError, NotUniqueError

# Entity not found
try:
    manager.delete(nonexistent)
except EntityNotFoundError:
    print("Entity doesn't exist")

# Multiple matches for keyless entity
try:
    manager.delete(keyless_entity)
except NotUniqueError:
    # Use filter().delete() for bulk deletion instead
    count = manager.filter(value=keyless_entity.value).delete()

# Missing @key attribute for update
try:
    manager.update(entity_with_none_key)
except KeyAttributeError as e:
    print(f"Cannot {e.operation}: key '{e.field_name}' is None")
```

---

## Important Notes

1. **Keyword-only arguments**: All Entity/Relation constructors require keyword arguments

   ```python
   # Correct
   Person(name=Name("Alice"), age=Age(30))

   # Wrong - will fail
   Person(Name("Alice"), Age(30))
   ```

2. **Attribute instances**: Always wrap values in attribute types

   ```python
   # Correct
   person.age = Age(31)

   # Wrong
   person.age = 31
   ```

3. **list[Type] is an unordered set**: TypeDB has no list type—order is never preserved

4. **@key required for update()**: Entities must have `@key` attributes for `update()` to work

5. **Connection management**: Use context managers or explicit connect/close

   ```python
   with Database(...) as db:
       # operations
   # Auto-closed
   ```

6. **Schema sync before data**: Always sync schema before inserting data

7. **Use .execute() for queries**: Chain with `.execute()` to get results

   ```python
   results = manager.filter(age__gt=30).execute()  # Returns list
   first = manager.filter(age__gt=30).first()      # Returns single or None
   ```
