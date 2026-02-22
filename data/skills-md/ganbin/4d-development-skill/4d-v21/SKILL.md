---
name: 4d-v21
description: >
  Comprehensive 4D v21 development expert with embedded official documentation.
  Covers ORDA patterns, entity classes, data model classes, queries, classic
  methods, data types, error handling, forms, events, web server, and REST API.
  Use when working with 4D files (.4dm), 4D language questions, 4D project
  structure, entity classes, ORDA queries, database operations, form development,
  web server configuration, REST API usage, or any 4D-specific syntax issue.
  Includes full official 4D v21 documentation for on-demand retrieval.
  Triggers on: .4dm files, 4D code, ORDA, entity selection, dataclass, 4D query,
  4D form, 4D web server, 4D REST, 4D command, 4D collection, 4D object.
---

# 4D Development Expert (v21)

## Skill Version

- **4D Version**: v21
- **Skill Version**: 1.0
- **Docs**: Full official 4D v21 documentation embedded in `docs/` (3,387 files)

This skill targets **4D v21** specifically. Do not assume features from other versions exist unless verified in the embedded documentation.

---

## How to Use This Skill

**CRITICAL**: For any 4D task, ALWAYS prefer reading the embedded documentation files (`docs/`) over relying on training data. The `docs/` folder contains the authoritative 4D v21 reference.

**Workflow:**
1. Check this file for critical rules and routing
2. Read the relevant `references/` file for curated knowledge and patterns
3. If more detail is needed, read the specific `docs/` file pointed to by the reference
4. For edge cases, use grep to search across `docs/`
5. Only fall back to training data if `docs/` doesn't cover the topic

**Priority reading**: Always check `references/manual-insights.md` — it contains real-world corrections from code reviews that override documentation.

---

## Local Conventions

Before providing 4D guidance, check if a `local/` directory exists in this skill folder with project-specific conventions:

```bash
ls local/*.md 2>/dev/null
```

If files exist, read them first. The `local/` directory (gitignored) can contain:
- Company-specific naming conventions and documentation standards
- Project-specific database schemas
- Version overrides (e.g., if project uses 4D v19.2 instead of v21)

---

## Critical Syntax Rules

These are the most common sources of bugs in 4D code. Know them by heart.

### 1. Assignment vs Comparison

```4d
// WRONG: = is comparison, returns True/False
$name = Request("Enter name")        // Compares, doesn't assign!
If ($input = Request("Name"))        // WRONG: compares, doesn't assign

// CORRECT: := is assignment
$name:=Request("Enter name")        // Assigns
$input:=Request("Name")
If ($input # "")                     // Then compare separately
```

**Rule**: `:=` assigns. `=` compares. Never mix them.

### 2. Object Properties Are Case-Sensitive

```4d
// Variables: case-INSENSITIVE
$MyVar:="test"
$myvar:="changed"            // Same variable!

// Object properties: case-SENSITIVE
$obj.Name:="John"
$obj.name:="Jane"            // Different properties!
```

### 3. Collection vs Array Indexing

```4d
// Collections: 0-based
$col:=New collection("A"; "B"; "C")
$first:=$col[0]              // "A"

// Arrays: 1-based with special element zero
ARRAY TEXT($arr; 3)
$arr{1}:="A"                 // First element
$arr{0}:="default"           // Special element zero
```

### 4. Null Queries Require Literal Syntax

```4d
// WRONG: Null as placeholder doesn't work
$result:=ds.Users.query("email = :1"; Null)

// CORRECT: literal null in query string
$result:=ds.Users.query("email = null")
$active:=ds.Users.query("email != null")
```

### 5. Linked Collection Queries

```4d
// WRONG: conditions can match DIFFERENT collection elements
ds.Users.query("projects[].status = 'active' AND projects[].budget > 1000")

// CORRECT: [a] links conditions to the SAME element
ds.Users.query("projects[a].status = 'active' AND projects[a].budget > 1000")
```

### 6. Numeric Object Properties Are Always Real

```4d
$obj:=New object("count"; 5)
Value type($obj.count)  // Returns Is real, NEVER Is longint
```

### 7. Decimal Separator Is Always Period

```4d
$price:=19.99    // CORRECT — always period
$price:=19,99    // WRONG — two separate numbers!
```

### 8. 4D has a strict left-to-right precedence

```4d
if ($length > 1+$i) // Runtime error: $length>1 -> true -> true+$i -> error
if ($length > (1+$i)) // No error

$result:=3+4*5 // 35
$result:=3+(4*5) // 23
```

---

## Quick Decision Router

### By Task

| Task | Read First | Then If Needed |
|------|-----------|----------------|
| Syntax errors, operators | [language-syntax.md](references/language-syntax.md) | `docs/Concepts/operators.md` |
| Data types, conversions | [data-types.md](references/data-types.md) | `docs/Concepts/data-types.md` |
| ORDA, entity classes | [orda-modern.md](references/orda-modern.md) | `docs/ORDA/ordaClasses.md` |
| Database queries | [query-patterns.md](references/query-patterns.md) | `docs/API/DataClassClass.md` |
| Error handling | [error-handling.md](references/error-handling.md) | `docs/Concepts/error-handling.md` |
| Legacy/classic code | [classic-patterns.md](references/classic-patterns.md) | `docs/Concepts/arrays.md` |
| Forms, events, UI | [forms-and-ui.md](references/forms-and-ui.md) | [events-index.md](references/events-index.md) |
| Web server, REST API | [web-and-rest.md](references/web-and-rest.md) | [rest-index.md](references/rest-index.md) |
| Specific class API | [api-index.md](references/api-index.md) | `docs/API/{ClassName}Class.md` |
| Specific command | [commands-index.md](references/commands-index.md) | `docs/commands/{name}.md` |
| Legacy command | [legacy-commands-index.md](references/legacy-commands-index.md) | `docs/commands-legacy/{name}.md` |

### By Error / Symptom

| Error or Symptom | Read |
|-----------------|------|
| "Type mismatch" or wrong type | [data-types.md](references/data-types.md) |
| "Cannot use = to assign" / silent assignment bug | [language-syntax.md](references/language-syntax.md) |
| Query returns wrong results | [query-patterns.md](references/query-patterns.md) |
| "Null query" not working | [manual-insights.md](references/manual-insights.md) |
| Entity/EntitySelection methods | [orda-modern.md](references/orda-modern.md) then [api-index.md](references/api-index.md) |
| Form events not firing | [forms-and-ui.md](references/forms-and-ui.md) then [events-index.md](references/events-index.md) |
| Process variables not working | [classic-patterns.md](references/classic-patterns.md) |
| REST endpoint 404 or auth error | [web-and-rest.md](references/web-and-rest.md) |
| Transaction or save error | [error-handling.md](references/error-handling.md) |
| `local` keyword confusion | [manual-insights.md](references/manual-insights.md) |
| Need to find a specific 4D command | [commands-index.md](references/commands-index.md) |
| Need to find a legacy command | [legacy-commands-index.md](references/legacy-commands-index.md) |

---

## Docs Navigator

The `docs/` folder contains the **full official 4D v21 documentation** (3,387 files, 48MB). Use this section to find the right file.

### Category Quick Lookup

| Need | Directory | File Pattern | Example Path |
|------|-----------|-------------|--------------|
| Class API reference | `docs/API/` | `{Class}Class.md` | `docs/API/CollectionClass.md` |
| ORDA concepts | `docs/ORDA/` | `{topic}.md` | `docs/ORDA/entities.md` |
| Modern commands | `docs/commands/` | `{command-name}.md` | `docs/commands/dialog.md` |
| Commands by theme | `docs/commands/theme/` | `{Theme}.md` | `docs/commands/theme/JSON.md` |
| Language concepts | `docs/Concepts/` | `{topic}.md` | `docs/Concepts/classes.md` |
| REST endpoints | `docs/REST/` | `${endpoint}.md` | `docs/REST/$filter.md` |
| Form events | `docs/Events/` | `on{Event}.md` | `docs/Events/onClicked.md` |
| Form objects | `docs/FormObjects/` | `{type}_overview.md` | `docs/FormObjects/listbox_overview.md` |
| Web server | `docs/WebServer/` | `{topic}.md` | `docs/WebServer/sessions.md` |
| Legacy commands | `docs/commands-legacy/` | `{command-name}.md` | `docs/commands-legacy/alert.md` |
| Settings | `docs/settings/` | `{topic}.md` | `docs/settings/web.md` |
| Project structure | `docs/Project/` | `{topic}.md` | `docs/Project/architecture.md` |
| AI Kit | `docs/aikit/` | various | `docs/aikit/` |
| ViewPro | `docs/ViewPro/` | various | `docs/ViewPro/` |
| WritePro | `docs/WritePro/` | various | `docs/WritePro/` |

### Search Patterns

When you need to find something specific across `docs/`:

```bash
# Find a command by name
grep -rl "title: CommandName" docs/commands/ docs/commands-legacy/

# Find a class method
grep -rl "\.methodName" docs/API/

# Find usage of a specific function
grep -rl "functionName" docs/ --include="*.md"

# Find a form event
ls docs/Events/on*.md

# Find a form object type
ls docs/FormObjects/*_overview.md

# Find a REST endpoint
ls docs/REST/\$*.md

# Find settings for a topic
grep -rl "keyword" docs/settings/

# Find a legacy command by theme
grep -rl "CommandName" docs/commands/theme/
```

### Index Files

For structured navigation of large categories, read these generated indexes:

| Index | Content | Files Indexed |
|-------|---------|---------------|
| [api-index.md](references/api-index.md) | All API classes with key methods | 42 |
| [commands-index.md](references/commands-index.md) | Modern commands + theme categories | 65 + 76 |
| [concepts-index.md](references/concepts-index.md) | Language concept files | 29 |
| [orda-index.md](references/orda-index.md) | ORDA documentation structure | 10 |
| [rest-index.md](references/rest-index.md) | REST API endpoints | 36 |
| [events-index.md](references/events-index.md) | Form and system events | 61 |
| [form-objects-index.md](references/form-objects-index.md) | Form object types | 54 |
| [webserver-index.md](references/webserver-index.md) | Web server documentation | 14 |
| [legacy-commands-index.md](references/legacy-commands-index.md) | Legacy commands by theme | 1,211 |
| [all-categories-index.md](references/all-categories-index.md) | Master navigation | 32 categories |

---

## Reference Files Guide

### Curated Knowledge (hand-written, with code examples)

| File | Covers | Priority |
|------|--------|----------|
| [language-syntax.md](references/language-syntax.md) | Assignment, operators, control flow, methods, classes, strings, formulas | High — read for any syntax question |
| [data-types.md](references/data-types.md) | All types, conversions, null/undefined, collections, objects, pointers | High — read for type errors |
| [orda-modern.md](references/orda-modern.md) | ORDA architecture, entity classes, computed attributes, shared objects, signals | High — read for new feature development |
| [query-patterns.md](references/query-patterns.md) | Query syntax, placeholders, null queries, linked collections, formulas, performance | High — read for any query work |
| [error-handling.md](references/error-handling.md) | Try/Catch, ON ERR CALL, transactions, Throw, logging | Medium — read when handling errors |
| [classic-patterns.md](references/classic-patterns.md) | Arrays, process variables, pointers, sets, migration strategies | Medium — read for legacy code |
| [forms-and-ui.md](references/forms-and-ui.md) | Forms, events, form objects, list boxes, subforms, form classes | Medium — read for UI work |
| [web-and-rest.md](references/web-and-rest.md) | Web server, REST API, HTTP handlers, sessions, authentication | Medium — read for web/REST work |
| [manual-insights.md](references/manual-insights.md) | Real-world corrections from code reviews — overrides other sources | **Always check** for edge cases |

### Common Workflows

**New Feature Development:**
1. [orda-modern.md](references/orda-modern.md) for architecture patterns
2. [query-patterns.md](references/query-patterns.md) for database operations
3. [error-handling.md](references/error-handling.md) for robust error management
4. Specific `docs/API/` files for class method details

**Legacy Code Maintenance:**
1. [classic-patterns.md](references/classic-patterns.md) for understanding legacy code
2. [orda-modern.md](references/orda-modern.md) for modernization options
3. [language-syntax.md](references/language-syntax.md) for syntax questions

**Debugging:**
1. Check [Critical Syntax Rules](#critical-syntax-rules) above first
2. [language-syntax.md](references/language-syntax.md) for syntax errors
3. [data-types.md](references/data-types.md) for type errors
4. [query-patterns.md](references/query-patterns.md) for query issues
5. [manual-insights.md](references/manual-insights.md) for known gotchas

**Web/REST Development:**
1. [web-and-rest.md](references/web-and-rest.md) for server and REST patterns
2. [orda-modern.md](references/orda-modern.md) for exposed functions
3. [rest-index.md](references/rest-index.md) for specific endpoint docs

---

## External Resources

When the embedded docs don't cover your case:

- **Official docs**: https://developer.4d.com/docs/
- **Community forum**: https://discuss.4d.com/
- **Blog** (feature deep-dives): https://blog.4d.com/
- **GitHub depot** (code examples): https://github.com/4d-depot
