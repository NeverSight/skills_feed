---
name: code-structural-search
description: Use ast-grep for AST-based code pattern matching.
version: 1.0.0
model: sonnet
invoked_by: user
user_invocable: true
tools: [Read, Write, Edit]
---

# Code Structural Search

Use ast-grep for AST-based code pattern matching.

## When to Use

- Find code by structure, not keywords
- "Find all functions with 3 arguments"
- "Find all classes that extend X"
- "Find all database queries"
- "Find all error handling patterns"
- Precise code refactoring (change exact patterns)

## Interface

```javascript
Skill({ skill: 'code-structural-search', args: 'pattern-here --lang ts' });
```

## Language Support

ast-grep supports 20+ languages via tree-sitter:

| Language   | Flag            | File Extensions      |
| ---------- | --------------- | -------------------- |
| JavaScript | `--lang js`     | .js, .jsx            |
| TypeScript | `--lang ts`     | .ts, .tsx            |
| Python     | `--lang py`     | .py, .pyi            |
| Go         | `--lang go`     | .go                  |
| Rust       | `--lang rs`     | .rs                  |
| Java       | `--lang java`   | .java                |
| C          | `--lang c`      | .c, .h               |
| C++        | `--lang cpp`    | .cpp, .cc, .hpp, .hh |
| C#         | `--lang cs`     | .cs                  |
| Kotlin     | `--lang kt`     | .kt, .kts            |
| Swift      | `--lang swift`  | .swift               |
| PHP        | `--lang php`    | .php                 |
| Ruby       | `--lang rb`     | .rb                  |
| Lua        | `--lang lua`    | .lua                 |
| Elixir     | `--lang ex`     | .ex, .exs            |
| HTML       | `--lang html`   | .html, .htm          |
| CSS        | `--lang css`    | .css                 |
| JSON       | `--lang json`   | .json                |
| Bash       | `--lang bash`   | .sh, .bash           |
| Thrift     | `--lang thrift` | .thrift              |

## Pattern Examples

### JavaScript/TypeScript

**Find all functions:**

```
function $NAME($ARGS) { $$ }
```

**Find functions with exactly 2 arguments:**

```
function $NAME($A, $B) { $$ }
```

**Find async functions:**

```
async function $NAME($ARGS) { $$ }
```

**Find class methods:**

```
class $NAME {
  $METHOD($ARGS) { $$ }
}
```

**Find arrow functions:**

```
const $NAME = ($ARGS) => { $$ }
```

**Find console.log statements:**

```
console.log($$$)
```

**Find try-catch blocks:**

```
try { $$ } catch ($ERR) { $$ }
```

### Python

**Find all functions:**

```
def $NAME($ARGS): $$$
```

**Find class definitions:**

```
class $NAME: $$$
```

**Find async functions:**

```
async def $NAME($ARGS): $$$
```

**Find imports:**

```
import $MODULE
```

**Find from imports:**

```
from $MODULE import $$$
```

### Go

**Find all functions:**

```
func $NAME($ARGS) $RETURN { $$ }
```

**Find struct definitions:**

```
type $NAME struct { $$$ }
```

**Find interface definitions:**

```
type $NAME interface { $$$ }
```

### Rust

**Find all functions:**

```
fn $NAME($ARGS) -> $RETURN { $$ }
```

**Find impl blocks:**

```
impl $NAME { $$$ }
```

**Find pub functions:**

```
pub fn $NAME($ARGS) -> $RETURN { $$ }
```

### Java

**Find all methods:**

```
public $RETURN $NAME($ARGS) { $$ }
```

**Find class definitions:**

```
public class $NAME { $$$ }
```

**Find interface definitions:**

```
public interface $NAME { $$$ }
```

## Pattern Syntax

| Symbol  | Meaning                         | Example               |
| ------- | ------------------------------- | --------------------- |
| `$NAME` | Single node/identifier          | `function $NAME() {}` |
| `$$$`   | Zero or more statements/nodes   | `class $NAME { $$$ }` |
| `$$`    | Zero or more statements (block) | `if ($COND) { $$ }`   |
| `$_`    | Anonymous wildcard (discard)    | `console.log($_)`     |

## Performance

- Speed: <50ms per search (typical)
- Best combined with semantic search (Phase 1)
- Use ripgrep first for initial file discovery

## vs Other Tools

**vs Ripgrep (grep):**

- Ripgrep: Fast text search, finds keywords
- ast-grep: Structural search, finds exact code patterns
- Use ripgrep first → then ast-grep to refine

**vs Semantic Search (Phase 1):**

- Semantic: Understands code meaning
- ast-grep: Understands code structure
- Combined: Best results (Phase 2)

## Usage Workflow

1. **Broad search** with ripgrep:

   ```
   Skill({ skill: 'ripgrep', args: 'authenticate --type ts' })
   ```

2. **Structural refinement** with ast-grep:

   ```
   Skill({ skill: 'code-structural-search', args: 'function authenticate($$$) { $$ } --lang ts' })
   ```

3. **Semantic understanding** with Phase 1:
   ```
   Skill({ skill: 'code-semantic-search', args: 'authentication logic' })
   ```

## Common Use Cases

### Security Patterns

**Find unvalidated inputs:**

```
router.post($PATH, ($REQ, $RES) => { $$ })
```

**Find SQL queries (potential injection):**

```
db.query(`SELECT * FROM ${$VAR}`)
```

**Find eval usage:**

```
eval($$$)
```

### Code Quality Patterns

**Find deeply nested functions:**

```
function $NAME($ARGS) {
  if ($COND) {
    if ($COND2) {
      if ($COND3) { $$ }
    }
  }
}
```

**Find long parameter lists (>5 params):**

```
function $NAME($A, $B, $C, $D, $E, $F, $$$) { $$ }
```

**Find unused variables:**

```
const $NAME = $VALUE;
```

### Refactoring Patterns

**Find old API usage:**

```
oldAPI.deprecatedMethod($$$)
```

**Find callback patterns (convert to async/await):**

```
$FUNC($ARGS, ($ERR, $DATA) => { $$ })
```

**Find React class components (convert to hooks):**

```
class $NAME extends React.Component { $$$ }
```

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern → `.claude/context/memory/learnings.md`
- Issue found → `.claude/context/memory/issues.md`
- Decision made → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
