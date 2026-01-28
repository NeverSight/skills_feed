---
name: code
description: Executable documentation governance with compound engineering and abductive learning. Enforces the Seven Laws through type compilation, schema validation, and hookify-based enforcement. Implements programmatic compound engineering where K' = K ∪ crystallize(assess(τ)) for monotonic knowledge growth. Integrates abstracted abductive learning (OHPT protocol) for systematic debugging and pattern extraction. Trigger when writing code, debugging, establishing governance, or when mentioned vibecode, compound, abductive, or executable documentation. Self-validating and homoiconic.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
context: fork
agent: code-governance-agent
user-invocable: true
---

# Code: Executable Documentation Governance

```
λο.τ :: Vibecode → ExecutableDocumentation
     where τ ∈ {compiles, validates, runs, passes}

compound :: Knowledge → Response → Knowledge
compound K τ = K ∪ crystallize(assess(τ))
```

## Metaschema

This skill is **homoiconic**: it enforces the same patterns it describes. The structure mirrors the content; the DAG below governs both skill loading and project governance.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PROGRESSIVE LOADING DAG                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  L0: SKILL.md (this file)                                          │
│      │  • Core laws, routing, quick patterns                       │
│      │  • Compound engineering integration                         │
│      │  • Always loaded (~500 lines)                               │
│      │                                                             │
│      ├──► L1: references/laws.md                                   │
│      │        • Seven Laws complete specification                  │
│      │        • Load when: implementing governance                 │
│      │                                                             │
│      ├──► L1: references/executable-doc.md                         │
│      │        • Tier hierarchy, conversion methodology             │
│      │        • Load when: converting docs to code                 │
│      │                                                             │
│      ├──► L1: references/patterns.md                               │
│      │        • TODO management, type documentation                │
│      │        • Load when: establishing patterns                   │
│      │                                                             │
│      ├──► L1: references/compound-engineering.md                   │
│      │        • K' = K ∪ crystallize(assess(τ))                   │
│      │        • Load when: crystallizing learnings                 │
│      │                                                             │
│      ├──► L1: references/abductive-learning.md                     │
│      │        • OHPT protocol for debugging                        │
│      │        • Load when: systematic debugging needed             │
│      │                                                             │
│      ├──► L2: scripts/preflight.py                                 │
│      │        • Execute directly for validation                    │
│      │        • Load when: customizing checks                      │
│      │                                                             │
│      ├──► L2: scripts/validate-skill.py                            │
│      │        • Self-validation (homoiconic)                       │
│      │        • Load when: validating this or other skills         │
│      │                                                             │
│      ├──► L2: hooks/*                                              │
│      │        • Hookify rules for governance + compound learning   │
│      │        • Install via: scripts/install-hooks.sh              │
│      │                                                             │
│      └──► L3: templates/*                                          │
│               • CI/CD configs                                      │
│               • Copy when: initializing projects                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## The Seven Laws

```haskell
-- Core invariants (see references/laws.md for complete spec)
LAW_1: ∀f ∈ Features. deployed(f) ⟹ e2e_verified(f)
LAW_2: ∀e ∈ Executions. observable(e) ∧ traceable(e)
LAW_3: ∀r ∈ CriticalRules. script_enforced(r)
LAW_4: ∀pr ∈ PRs. merged(pr) ⟹ human_reviewed(pr)
LAW_5: ∀d ∈ AuthoritativeDoc. d ⊂ Codebase
LAW_6: compiles(d) ∨ validates(d) ⟹ current(d)
LAW_7: ∀plan ∈ Plans. expressed_as_todos(plan) ∧ in_code(plan)
```

## Routing

```python
def route(task: Task) -> Pipeline:
    """Route task to appropriate governance level."""
    
    if task.type == "simple_change":
        return R1_SINGLE  # Preflight only
    
    if task.type == "feature":
        return R2_COMPOSE  # Preflight → E2E → Log review
    
    if task.type in ["architecture", "governance", "release"]:
        return R3_FULL  # Full Seven Laws verification
    
    return R0_DIRECT  # No governance (rare)
```

| Level | Pipeline | Verification |
|-------|----------|--------------|
| R0 | Direct | None |
| R1 | `preflight` | Types, schemas, linting |
| R2 | `preflight → e2e → logs` | + Runtime behavior |
| R3 | `full_governance` | All Seven Laws |

## Quick Start

### 1. Initialize Project Governance

```bash
# Copy governance templates to project
cp templates/ci.yml ./.github/workflows/

# Run preflight to verify setup
python scripts/preflight.py --init

# Install governance hooks (optional)
bash scripts/install-hooks.sh
```

### 2. Establish Executable Documentation

```python
# BAD: External documentation (will drift)
# docs/api.md: "User endpoint returns JSON with name and email"

# GOOD: Type as documentation (compiles = current)
@dataclass
class UserResponse:
    """User endpoint response. If this compiles, docs are current."""
    name: str
    email: EmailStr
    created_at: datetime
```

### 3. Plan with TODOs

```python
# Instead of external implementation plan, use in-code TODOs:

# TODO(auth-1,required): Implement password hashing
# Context: Security requirement SR-101
# Acceptance: bcrypt cost factor 12, no plaintext storage

# TODO(auth-2): Add rate limiting
# Context: Prevent brute force per SR-102
# Approach: Redis sliding window, 5 attempts/minute

async def login(credentials: LoginCredentials) -> AuthResult:
    # Implementation replaces TODOs as work completes
    pass
```

### 4. Validate Before Merge

```bash
# Run preflight (automatically runs in CI)
python scripts/preflight.py

# Check remaining TODOs
grep -rn "TODO(.*required" --include="*.py" --include="*.ts" src/

# Generate architecture diagram (from code, not hand-drawn)
npx madge --image docs/deps.svg src/
```

## Executable Documentation Hierarchy

| Tier | Form | Trust | Verification |
|------|------|-------|--------------|
| **T1** | Type signatures | 0.95 | Compiler |
| **T2** | Schema definitions | 0.95 | Validator |
| **T3** | API specs (generated) | 0.95 | Generator |
| **T4** | Database migrations | 0.95 | Migration runner |
| **T5** | Linter rules | 0.90 | Linter |
| **T6** | Test assertions | 0.70 | Test runner |
| **T7** | TODOs in code | 0.60 | Grep/lint |
| **T8** | Inline comments | 0.50 | Localized drift |
| **T9** | External docs | 0.10 | **Will drift** |

**Governing Principle:**
```
IF    types check       (T1)
AND   schemas validate  (T2)
AND   specs generate    (T3)
AND   migrations run    (T4)
AND   linters pass      (T5)
AND   todos resolved    (T7)
THEN  documentation IS current
```

## Conversion Methodology

When documentation is needed, convert to code-based form:

```python
def document_in_code(need: str) -> CodeDoc:
    """Convert documentation need to executable form."""
    
    # Priority order: higher tier = more trustworthy
    if can_express_as_type(need):
        return TypeDefinition(need)  # T1
    
    if can_express_as_schema(need):
        return SchemaDefinition(need)  # T2
    
    if can_express_as_linter_rule(need):
        return LinterRule(need)  # T5
    
    if can_express_as_test(need):
        return TestCase(need)  # T6, with tautology caveat
    
    if can_express_as_todo(need):
        return TODO(need)  # T7
    
    # Last resort: inline comment (T8)
    # NEVER external doc (T9)
    return InlineComment(need)
```

**For complete conversion patterns, load:** `references/executable-doc.md`

## Preflight Script

Core validation that runs before every commit:

```bash
#!/bin/bash
# Minimal preflight example — run python scripts/preflight.py for full version

set -e

echo "=== PREFLIGHT: Executable Documentation Verification ==="

# T1: Types compile
npm run typecheck || { echo "❌ Types invalid"; exit 1; }

# T2: Schemas validate  
npm run validate:schemas || { echo "❌ Schemas invalid"; exit 1; }

# T5: Linting passes
npm run lint || { echo "❌ Linting failed"; exit 1; }

# T7: Required TODOs resolved
grep -rn "TODO(.*required" src/ && { echo "❌ Required TODOs remain"; exit 1; }

echo "✅ Preflight passed"
```

**For complete preflight implementation, run:** `python scripts/preflight.py`

## TODO Categories

```python
# Standard categories for TODO-based planning:

# TODO(feature-id): Standard task
# TODO(feature-id,required): Must complete before merge (blocks CI)
# TODO(feature-id,blocked:other): Waiting on dependency
# TODO(tech-debt): Known improvement needed
# TODO(security): Security-related (high priority)
# FIXME: Known bug requiring fix
# HACK: Temporary solution needing proper implementation
```

**Lifecycle:**
```
PLAN → Write TODOs at implementation points
DEVELOP → Implement, remove TODO when done
VERIFY → grep for remaining TODOs
COMPLETE → Zero required TODOs = feature complete
```

**For TODO management, use:** `grep -rn "TODO(.*required" --include="*.py" --include="*.ts" src/`

## Unit Test Skepticism (LAW_3 Caveat)

```python
# WARNING: AI writes tautological tests
# Test documents what code DOES, not what code SHOULD DO

# REQUIREMENT: "Users can log in with valid credentials"

# AI IMPLEMENTATION (buggy):
def authenticate(user, password):
    return True  # BUG: Always succeeds

# AI TEST (tautological):
def test_authenticate():
    assert authenticate("user", "pass") == True  # ✓ PASSES!
    # Test verifies implementation, not requirement
```

**Mitigation:**
- E2E tests verify actual behavior (LAW_1)
- Human review verifies intent (LAW_4)
- Unit tests provide regression protection only
- Trust hierarchy: `E2E (0.9) > Review (0.75) > Unit (0.3)`

## Diagram Generation

Generate diagrams from code, never hand-draw:

```bash
# Dependency graph from imports
npx madge --image docs/deps.svg src/

# Type relationships
npx ts-diagram src/ > docs/types.mmd

# Database schema from migrations
pg_dump --schema-only | sqlt-graph > docs/schema.svg

# OpenAPI from annotations (generated = current)
npm run generate:openapi
```

**Use standard tools:** `npx madge`, `npx ts-diagram`, `pg_dump | sqlt-graph`

## Self-Validation (Homoiconicity)

This skill validates itself using the same rules it prescribes:

```python
# scripts/validate-skill.py validates:
# 1. SKILL.md under 500 lines ✓
# 2. References progressively loaded ✓
# 3. Scripts executable ✓
# 4. No external docs (only code-based) ✓
# 5. DAG structure maintained ✓
```

Run: `python scripts/validate-skill.py code/`

## Compound Engineering

The self-improvement loop that makes knowledge recursive:

```haskell
compound :: Knowledge → Response → Knowledge
compound K τ = K ∪ crystallize(assess(τ))

-- K grows monotonically; never loses valid knowledge
-- Crystallization compresses: raw experience → reusable pattern
```

### The Compound Loop

```
Plan(K) → Execute → Assess → Compound(K→K')
   ↑                              |
   └────────── K' ────────────────┘
```

Each iteration makes the next **easier**, not harder.

### Trigger Detection

Compound when resolution patterns detected:

| Pattern | Example | Action |
|---------|---------|--------|
| Confirmation | "that worked", "correct" | Extract solution |
| Insight | "I see now", "the key is" | Extract principle |
| Prevention | "next time", "to avoid" | Extract guard |
| Connection | "this relates to", "like" | Extract vertex |

### Learning Crystallization

```yaml
# Required schema for compounded learnings
date: YYYY-MM-DD
trigger: "what initiated learning"
domain: "coding|debugging|architecture|..."
observation: "what was observed"
hypothesis: "best explanation"
root_cause: "fundamental cause (not surface)"
solution: "what worked"
why_works: "mechanistic explanation"
prevention: "how to avoid in future"
vertices:
  - "[[shared concept 1]]"
  - "[[shared concept 2]]"
confidence: 0.85
```

**Validation before adding to K:**
- [ ] Has >=2 shared vertices with existing K
- [ ] Root cause is fundamental (not surface symptom)
- [ ] Solution is generalizable (not one-off)
- [ ] Prevention is actionable

**For complete compound engineering spec, load:** `references/compound-engineering.md`

## Abductive Learning (OHPT Protocol)

Inference to the best explanation for systematic debugging:

```
O (Observation) → H (Hypothesis) → P (Prediction) → T (Test)
```

| Phase | Question | Output |
|-------|----------|--------|
| **O** | What was observed? | Symptom description |
| **H** | What explains O? | Candidate causes (ranked by parsimony) |
| **P** | If H true, what else? | Testable predictions |
| **T** | Does P hold? | Evidence confirming/refuting H |

### Quick Template

```python
"""
O: [What was observed - be specific]
H: [Best explanation - testable, parsimonious]
P: [If H true, then... - observable consequences]
T: [Test result - confirms/refutes H]
"""
```

**For complete OHPT protocol, load:** `references/abductive-learning.md`

## Hookify Integration

Governance enforcement through hookify rules:

| Hook | Event | Purpose |
|------|-------|---------|
| `law1-e2e-deploy` | bash | Verify E2E before deploy |
| `law2-observability` | file | Warn on debug logging |
| `law5-external-docs` | file | Block external documentation |
| `law6-compile-current` | bash | Check types before merge |
| `law7-required-todos` | bash | Verify TODOs resolved |
| `stop-checklist` | stop | Seven Laws completion check |
| `tautological-tests` | file | Detect test anti-patterns |
| `compound-learning` | stop | Prompt crystallization |
| `abductive-hypothesis` | file | Require OHPT in tests |
| `knowledge-monotonicity` | file | Prevent knowledge deletion |
| `vertex-sharing` | file | Require vertex connections |
| `inference-chain` | file | Complete reasoning chains |
| `pattern-crystallization` | bash | Extract on commits |

**Install hooks:** `bash scripts/install-hooks.sh`

## Integration Points

| Skill | Integration |
|-------|-------------|
| `graph` | Topology validation (η ≥ 4) |
| `critique` | Multi-lens code review |
| `hierarchical-reasoning` | S→T→O decomposition |
| `component` | Generate CI/CD configs |
| `skill-optimiser` | Validate this skill |
| `learn` | Compound engineering loop |
| `ultrawork` | Parallel governance checks |

## File Structure

```
code/
├── SKILL.md                    # This file (L0)
├── references/
│   ├── laws.md                 # Seven Laws complete spec (L1)
│   ├── executable-doc.md       # Tier system, conversion (L1)
│   ├── patterns.md             # TODO, types, diagrams (L1)
│   ├── compound-engineering.md # K' = K ∪ crystallize(assess(τ)) (L1)
│   └── abductive-learning.md   # OHPT debugging protocol (L1)
├── scripts/
│   ├── preflight.py            # Validation orchestration (L2)
│   ├── validate-skill.py       # Self-validation (L2)
│   └── install-hooks.sh        # Install governance hooks (L2)
├── templates/
│   └── ci.yml                  # GitHub Actions template (L3)
└── hooks/                      # Hookify governance + compound rules
    ├── hookify.law1-e2e-deploy.local.md
    ├── hookify.law2-observability.local.md
    ├── hookify.law5-external-docs.local.md
    ├── hookify.law6-compile-current.local.md
    ├── hookify.law7-required-todos.local.md
    ├── hookify.stop-checklist.local.md
    ├── hookify.tautological-tests.local.md
    ├── hookify.compound-learning.local.md      # Crystallize before stop
    ├── hookify.abductive-hypothesis.local.md   # OHPT in tests
    ├── hookify.knowledge-monotonicity.local.md # K never shrinks
    ├── hookify.vertex-sharing.local.md         # Require connections
    ├── hookify.inference-chain.local.md        # Complete reasoning
    └── hookify.pattern-crystallization.local.md # Extract on commit
```

## Holarchic Structure

Every component is a complete holon:

```
SKILL (this file)
  ├── Contains: Complete governance framework
  ├── Validates: Itself via scripts/validate-skill.py
  └── Holons:
        ├── preflight.py
        │   ├── Contains: Complete validation pipeline
        │   ├── Validates: Project code
        │   └── Holons: Individual check functions
        │
        ├── hooks/*
        │   ├── Contains: Seven Laws enforcement rules
        │   ├── Validates: Via hookify plugin
        │   └── Holons: Individual law-specific rules
        │
        └── templates/*
            ├── Contains: Complete project setup
            ├── Validates: Via instantiation
            └── Holons: Individual config files
```

**Scale invariance:** `λο.τ` applies at every level—skill, script, function, line.

---

```
┌─────────────────────────────────────────────────────────────────┐
│  SEVEN LAWS          │  TRUST HIERARCHY    │  VERIFICATION     │
├──────────────────────┼─────────────────────┼───────────────────┤
│  1. E2E verified     │  Types (0.95)       │  Compiles         │
│  2. Observable       │  Schemas (0.95)     │  Validates        │
│  3. Script enforced  │  E2E (0.90)         │  Passes           │
│  4. Human reviewed   │  Review (0.75)      │  Approved         │
│  5. Code is doc      │  Unit (0.30)        │  (Low trust)      │
│  6. Compile=current  │  External (0.10)    │  (Will drift)     │
│  7. TODOs are plans  │                     │                   │
└──────────────────────┴─────────────────────┴───────────────────┘
```
