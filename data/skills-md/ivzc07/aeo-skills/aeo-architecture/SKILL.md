---
name: aeo-architecture
description: Analyze and protect code architecture. Detects circular dependencies and layer violations.
---

# AEO Architecture

**Purpose:** Analyze and protect code architecture. Detects circular dependencies, layer violations, and manages ADRs (Architecture Decision Records).

## Configuration

Define architecture layers at `$PAI_DIR/USER/aeo-layers.yaml`:

```yaml
layers:
  - name: "presentation"
    path: "src/components/"
    may_import: ["domain", "application"]
    may_not_import: ["infrastructure", "presentation"]

  - name: "domain"
    path: "src/domain/"
    may_import: []
    may_not_import: ["presentation", "application", "infrastructure"]

  - name: "application"
    path: "src/services/"
    may_import: ["domain"]
    may_not_import: ["presentation", "infrastructure"]

  - name: "infrastructure"
    path: "src/infrastructure/"
    may_import: ["domain"]
    may_not_import: ["presentation", "application"]
```

**Default:** No layers defined - only detect circular dependencies

## When to Analyze

Run architecture analysis:
- After feature implementation
- Before git commit (via aeo-qa-agent)
- When circular dependency suspected
- During code review

## Detection Types

### 1. Circular Dependencies

**Detection:**

```bash
# Build dependency graph
find src -name "*.js" -o -name "*.ts" | while read file; do
  grep -h "^import" "$file" | \
    sed "s/.*from ['\"]\(.*\)['\"].*/\1/" | \
    while read import; do
      echo "$file -> $import"
    done
done > /tmp/deps.txt

# Detect cycles
# (Use graph algorithm or madge)
npx madge --circular --extensions ts,tsx,js,jsx src/
```

**Example Circular Dependency:**

```
❌ CIRCULAR DEPENDENCY DETECTED

Cycle:
  src/services/UserService.js
    → src/repositories/UserRepository.js
      → src/models/User.js
        → src/services/UserService.js
          (back to start - cycle!)

Why this matters:
• Creates tight coupling
• Makes code impossible to test in isolation
• Can cause runtime errors during module loading
• Violates clean architecture principles

Resolution Options:
1. Extract shared code - Create new module for shared functionality
2. Invert dependency - Use dependency injection
3. Introduce interface - Abstract the dependency

Recommended: Option 1 - Extract shared functionality

Your choice (1-3):
```

---

### 2. Layer Violations

**Detection:**

```bash
# Check if presentation layer imports infrastructure
grep -r "import.*from.*infrastructure" src/components/

# Check if domain imports presentation
grep -r "import.*from.*components" src/domain/
```

**Example Layer Violation:**

```
⚠️ LAYER VIOLATION DETECTED

Violation: Presentation layer importing Infrastructure

File: src/components/UserList.tsx:5
Import: import db from '../infrastructure/database.js'

Why this violates architecture:
• Presentation should only import from Application/Domain
• Direct database access in component creates tight coupling
• Makes testing difficult (need real database)
• Violates separation of concerns

Correct Pattern:
❌ src/components/UserList.tsx
   import db from '../infrastructure/database.js'

✅ src/components/UserList.tsx
   import { getUsers } from '../services/UserService.js'

✅ src/services/UserService.js
   import db from '../infrastructure/database.js'
   export function getUsers() {
     return db.query('SELECT * FROM users')
   }

Action: Fix violation before commit
```

---

### 3. Breaking Encapsulation

**Detection:**

```bash
# Check for private field access from outside class
grep -r "#[a-zA-Z]*\s*=" src/ | grep -v "this\.#"
```

**Example Encapsulation Breaking:**

```
❌ ENCAPSULATION VIOLATION

File: src/utils/userHelper.js:42
Issue: Accessing private field #passwordHash from outside

Code:
```javascript
class User {
  #passwordHash  // Private field
}

// In another file:
user.#passwordHash = 'new'  // ❌ VIOLATION
```

Why this violates encapsulation:
• Private fields are implementation details
• Bypasses validation and invariants
• Makes code fragile to internal changes
• Breaks abstraction boundary

Correct Approach:
```javascript
class User {
  #passwordHash

  setPassword(newPassword) {
    // Validate and hash
    this.#passwordHash = hash(newPassword)
  }

  getPassword() {
    return this.#passwordHash
  }
}

// Use public API:
user.setPassword('new')
```

Action: Fix encapsulation violation
```

---

## Architecture Decision Records (ADRs)

### ADR Format

Create ADRs at `$PAI_DIR/USER/ADRs/`:

```markdown
# ADR-001: Use JWT for Authentication

## Status
Accepted

## Context
We need authentication for our API. Options considered:
- Session-based auth
- JWT tokens
- API keys

## Decision
Use JWT tokens because:
1. Stateless - scales horizontally
2. Standard - well-supported libraries
3. Flexible - supports multiple auth providers

## Consequences
- Positive: No session storage needed
- Positive: Works well with microservices
- Negative: Token revocation requires blacklist
- Negative: Larger payload than session IDs

## Implementation
- Use jose library for JWT handling
- Store refresh tokens in Redis
- Set access token expiry to 15 minutes

## Date
2026-01-22
```

### Recording ADRs

When making significant architectural decisions:

1. **Create ADR file:**
   ```bash
   # Find next ADR number
   next_num=$(ls ~/.claude/USER/ADRs/ | grep ADR- | wc -l)
   adr_file=~/.claude/USER/ADRs/ADR-$(printf "%03d" $((next_num + 1)))-${title}.md
   ```

2. **Use template:**
   ```bash
   cat > "$adr_file" << 'EOF'
   # ADR-XXX: [Title]

   ## Status
   Proposed

   ## Context
   [Problem statement and context]

   ## Decision
   [The decision]

   ## Consequences
   - Positive: [Benefits]
   - Negative: [Drawbacks]

   ## Date
   $(date -u +%Y-%m-%d)
   EOF
   ```

3. **Reference ADRs in code:**
   ```javascript
   // See ADR-001: Use JWT for Authentication
   import { generateToken } from './auth/jwt.js'
   ```

---

## Architecture Analysis Commands

### Check Circular Dependencies

```bash
# Using madge
npx madge --circular --extensions ts,tsx src/

# Output:
# ✅ No circular dependencies found
# or
# ❌ Circular dependencies found:
#   src/a.js → src/b.js → src/a.js
```

### Check Layer Violations

```bash
# Check layer compliance
check_layers() {
  local layer=$1
  local path=$2
  local forbidden=$3

  echo "Checking $layer layer..."

  for forbidden_import in $forbidden; do
    violations=$(grep -r "import.*from.*$forbidden_import" "$path" 2>/dev/null)
    if [ -n "$violations" ]; then
      echo "❌ $layer importing from $forbidden_import:"
      echo "$violations"
    fi
  done
}

# Run checks
check_layers "presentation" "src/components" "infrastructure"
check_layers "domain" "src/domain" "presentation,application"
```

### Generate Dependency Graph

```bash
# Visualize dependencies
npx madge --image deps.svg --extensions ts,tsx src/

# Output:
# Generated deps.svg
```

---

## Integration

**With aeo-qa-agent:**

```javascript
// In QA review, Step 4: Check Architecture
if (architecture_violations_found) {
  invoke_skill('aeo-architecture', {
    type: 'violation',
    violations: violations
  });
}
```

**With aeo-escalation:**

```javascript
// When architecture violation detected
invoke_skill('aeo-escalation', {
  type: 'architecture_violation',
  issue: 'circular_dependency',
  options: [
    'Extract shared code',
    'Refactor dependencies',
    'Defer to architect'
  ],
  recommended: 1
});
```

---

## Best Practices

**DO:**
- Define clear layer boundaries upfront
- Use dependency injection to break cycles
- Record significant architectural decisions
- Review architecture before committing
- Generate dependency graphs periodically

**DON'T:**
- Allow circular dependencies to persist
- Let layers bleed into each other
 Skip architecture review for "quick fixes"
- Break encapsapsulation for convenience
- Forget to document architectural decisions

---

## Example Session

```
AEO-QA: [Step 4: Check Architecture]

AEO-Architecture: Analyzing codebase...

                Detected Issues:
                ❌ Circular dependency: UserService → UserRepository → User → UserService
                ❌ Layer violation: UserList.tsx importing database.js
                ✅ Encapsulation: All private fields properly protected

                [Invokes aeo-escalation for circular dependency]

Escalation: ⚠️ ARCHITECTURE VIOLATION DETECTED

           Issue: Circular dependency between modules

           Circular Path:
            UserService.js imports UserRepository.js
            UserRepository.js imports User.js
            User.js imports UserService.js

           Options:
           1. Extract shared code - Create UserValueObject module
           2. Refactor dependencies - Introduce UserInterface
           3. Defer to architect - Let architect decide

           Recommended: Option 1 - Extract shared code

Developer: 1

AEO-Architecture: Creating UserValueObject module...

                [Refactoring...]
                [Updating imports...]
                [Running tests...]
                ✅ Circular dependency resolved

                [Recording ADR-003: Extract User Value Object]

AEO-QA: Architecture check passed

AEO-Core: Ready to commit
```

---

## ADR Management

### List ADRs

```bash
ls -1 ~/.claude/USER/ADRs/ | sort
# ADR-001-use-jwt-for-authentication.md
# ADR-002-adopt-event-sourcing.md
# ADR-003-extract-user-value-object.md
```

### Find ADR by Topic

```bash
grep -r "JWT" ~/.claude/USER/ADRs/
# ADR-001-use-jwt-for-authentication.md:## Context
# ADR-001-use-jwt-for-authentication.md:# - Use JWT tokens
```

### Propose New ADR

```bash
# Create proposed ADR
cat > ~/.claude/USER/ADRs/ADR-004-adopt-graphql.md << 'EOF'
# ADR-004: Adopt GraphQL

## Status
Proposed

## Context
Current REST API has issues:
- Over-fetching data
- Multiple round trips for related data
- Versioning complexity

## Decision
Adopt GraphQL for...

## Consequences
- Positive: Single query for related data
- Positive: Strongly typed schema
- Negative: Learning curve
- Negative: Complexity in caching

## Date
$(date -u +%Y-%m-%d)
EOF

# Then discuss with team before marking as "Accepted"
```

---

## Architecture Health Score

Calculate architecture health:

```bash
# 100 points total
score=100

# Subtract for issues
circular_deps=$(npx madge --circular src/ 2>/dev/null | grep "Found" | wc -l)
score=$((score - circular_deps * 20))

layer_violations=$(grep -r "import.*infrastructure" src/components/ 2>/dev/null | wc -l)
score=$((score - layer_violations * 10))

echo "Architecture Health: $score/100"
```

**Interpretation:**
- 90-100: Excellent architecture
- 70-89: Good, minor issues
- 50-69: Needs improvement
- < 50: Critical architectural problems

---

## Disable Architecture Checks

To disable for a project, delete `$PAI_DIR/USER/aeo-layers.yaml`:

```bash
rm ~/.claude/USER/aeo-layers.yaml
# AEO will skip layer checks, still detect circular deps
```
