---
name: ln-642-layer-boundary-auditor
description: "L3 Worker. Audits layer boundaries + cross-layer consistency: I/O violations, transaction boundaries (commit ownership), session ownership (DI vs local), async consistency (sync I/O in async), fire-and-forget tasks."
---

# Layer Boundary Auditor

L3 Worker that audits architectural layer boundaries and detects violations.

## Purpose & Scope

- Read architecture.md to discover project's layer structure
- Detect layer violations (I/O code outside infrastructure layer)
- **Detect cross-layer consistency issues:**
  - Transaction boundaries (commit/rollback ownership)
  - Session ownership (DI vs local)
  - Async consistency (sync I/O in async)
  - Fire-and-forget tasks (unhandled exceptions)
- Check pattern coverage (all HTTP calls use client abstraction)
- Detect error handling duplication
- Return violations list to coordinator

## Input (from ln-640)

```
- architecture_path: string    # Path to docs/architecture.md
- codebase_root: string        # Root directory to scan
- skip_violations: string[]    # Files to skip (legacy)
```

## Workflow

### Phase 1: Discover Architecture

```
Read docs/architecture.md

Extract from Section 4.2 (Top-Level Decomposition):
  - architecture_type: "Layered" | "Hexagonal" | "Clean" | "MVC" | etc.
  - layers: [{name, directories[], purpose}]

Extract from Section 5.3 (Infrastructure Layer Components):
  - infrastructure_components: [{name, responsibility}]

IF architecture.md not found:
  Use fallback presets from common_patterns.md

Build ruleset:
  FOR EACH layer:
    allowed_deps = layers that can be imported
    forbidden_deps = layers that cannot be imported
```

### Phase 2: Detect Layer Violations

```
FOR EACH violation_type IN common_patterns.md I/O Pattern Boundary Rules:
  grep_pattern = violation_type.detection_grep
  forbidden_dirs = violation_type.forbidden_in

  matches = Grep(grep_pattern, codebase_root, include="*.py,*.ts,*.js")

  FOR EACH match IN matches:
    IF match.path NOT IN skip_violations:
      IF any(forbidden IN match.path FOR forbidden IN forbidden_dirs):
        violations.append({
          type: "layer_violation",
          severity: "HIGH",
          pattern: violation_type.name,
          file: match.path,
          line: match.line,
          code: match.context,
          allowed_in: violation_type.allowed_in,
          suggestion: f"Move to {violation_type.allowed_in}"
        })
```

### Phase 2.5: Cross-Layer Consistency Checks

#### 2.5.1 Transaction Boundary Violations

**What:** commit()/rollback() called at inconsistent layers (repo + service + API)

**Detection:**
```
repo_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/repositories/**/*.py")
service_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/services/**/*.py")
api_commits = Grep("\.commit\(\)|\.rollback\(\)", "**/api/**/*.py")

layers_with_commits = count([repo_commits, service_commits, api_commits].filter(len > 0))
```

**Safe Patterns (ignore):**
- Comment "# best-effort telemetry" in same context
- File ends with `_callbacks.py` (progress notifiers)
- Explicit `# UoW boundary` comment

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| layers_with_commits >= 3 | CRITICAL | Mixed UoW ownership across all layers |
| repo + api commits | HIGH | Transaction control bypasses service layer |
| repo + service commits | HIGH | Ambiguous UoW owner (repo vs service) |
| service + api commits | MEDIUM | Transaction control spans service + API |

**Recommendation:** Choose single UoW owner (service layer recommended), remove commit() from other layers

**Effort:** L (requires architectural decision + refactoring)

#### 2.5.2 Session Ownership Violations

**What:** Mixed DI-injected and locally-created sessions in same call chain

**Detection:**
```
di_session = Grep("Depends\(get_session\)|Depends\(get_db\)", "**/api/**/*.py")
local_session = Grep("AsyncSessionLocal\(\)|async_sessionmaker", "**/services/**/*.py")
local_in_repo = Grep("AsyncSessionLocal\(\)", "**/repositories/**/*.py")
```

**Violation Rules:**

| Condition | Severity | Issue |
|-----------|----------|-------|
| di_session AND local_in_repo in same module | HIGH | Repo creates own session while API injects different |
| local_session in service calling DI-based repo | MEDIUM | Session mismatch in call chain |

**Recommendation:** Use DI consistently OR use local sessions consistently. Document exceptions (e.g., telemetry)

**Effort:** M

#### 2.5.3 Async Consistency Violations

**What:** Synchronous blocking I/O inside async functions

**Detection:**
```
# For each file with "async def":
sync_file_io = Grep("\.read_bytes\(\)|\.read_text\(\)|\.write_bytes\(\)|\.write_text\(\)", file)
sync_open = Grep("(?<!aiofiles\.)open\(", file)  # open() not preceded by aiofiles.

# Safe patterns (not violations):
# - "asyncio.to_thread(" wrapping the call
# - "await aiofiles.open("
# - "run_in_executor(" wrapping the call
```

**Violation Rules:**

| Pattern | Severity | Issue |
|---------|----------|-------|
| Path.read_bytes() in async def | HIGH | Blocking file read in async context |
| open() without aiofiles in async def | HIGH | Blocking file operation |
| time.sleep() in async def | HIGH | Blocking sleep (use asyncio.sleep) |

**Recommendation:** Use `asyncio.to_thread()` or `aiofiles` for file I/O in async functions

**Effort:** S-M

#### 2.5.4 Fire-and-Forget Violations

**What:** asyncio.create_task() without error handling

**Detection:**
```
all_tasks = Grep("create_task\(", codebase)

# For each match, check context:
# - Has .add_done_callback() → OK
# - Assigned to variable with later await → OK
# - Has "# fire-and-forget" comment → OK (documented intent)
# - None of above → VIOLATION
```

**Violation Rules:**

| Pattern | Severity | Issue |
|---------|----------|-------|
| create_task() without handler or comment | MEDIUM | Unhandled task exception possible |
| create_task() in loop without error collection | HIGH | Multiple silent failures possible |

**Recommendation:** Add `task.add_done_callback(handle_exception)` or document intent with comment

**Effort:** S

---

### Phase 3: Check Pattern Coverage

```
# HTTP Client Coverage
all_http_calls = Grep("httpx\\.|aiohttp\\.|requests\\.", codebase_root)
abstracted_calls = Grep("client\\.(get|post|put|delete)", infrastructure_dirs)

IF len(all_http_calls) > 0:
  coverage = len(abstracted_calls) / len(all_http_calls) * 100
  IF coverage < 90%:
    violations.append({
      type: "low_coverage",
      severity: "MEDIUM",
      pattern: "HTTP Client Abstraction",
      coverage: coverage,
      uncovered_files: files with direct calls outside infrastructure
    })

# Error Handling Duplication
http_error_handlers = Grep("except\\s+(httpx\\.|aiohttp\\.|requests\\.)", codebase_root)
unique_files = set(f.path for f in http_error_handlers)

IF len(unique_files) > 2:
  violations.append({
    type: "duplication",
    severity: "MEDIUM",
    pattern: "HTTP Error Handling",
    files: list(unique_files),
    suggestion: "Centralize in infrastructure layer"
  })
```

### Phase 3.5: Calculate Score

**Unified formula:**
```
penalty = (critical × 2.0) + (high × 1.0) + (medium × 0.5) + (low × 0.2)
score = max(0, 10 - penalty)
```

**Example:**
- 1 CRITICAL + 2 HIGH + 3 MEDIUM = 1×2.0 + 2×1.0 + 3×0.5 = 5.5 penalty
- score = 10 - 5.5 = 4.5

### Phase 4: Return Result

```json
{
  "category": "Layer Boundary",
  "score": 4.5,
  "total_issues": 8,
  "critical": 1,
  "high": 3,
  "medium": 4,
  "low": 0,
  "architecture": {
    "type": "Layered",
    "layers": ["api", "services", "domain", "infrastructure"]
  },
  "findings": [
    {
      "severity": "CRITICAL",
      "location": "app/",
      "issue": "Mixed UoW ownership: commit() found in repositories (3), services (2), api (4)",
      "principle": "Layer Boundary / Transaction Control",
      "recommendation": "Choose single UoW owner (service layer recommended), remove commit() from other layers",
      "effort": "L"
    },
    {
      "severity": "HIGH",
      "location": "app/services/job/service.py:45",
      "issue": "Blocking file I/O in async: Path.read_bytes() inside async def process_job()",
      "principle": "Layer Boundary / Async Consistency",
      "recommendation": "Use asyncio.to_thread(path.read_bytes) or aiofiles",
      "effort": "S"
    },
    {
      "severity": "HIGH",
      "location": "app/domain/pdf/parser.py:45",
      "issue": "Layer violation: HTTP client used in domain layer",
      "principle": "Layer Boundary / I/O Isolation",
      "recommendation": "Move httpx.AsyncClient to infrastructure/http/clients/",
      "effort": "M"
    },
    {
      "severity": "MEDIUM",
      "location": "app/api/v1/jobs.py:78",
      "issue": "Fire-and-forget task without error handler: create_task(notify_user())",
      "principle": "Layer Boundary / Task Error Handling",
      "recommendation": "Add task.add_done_callback(handle_exception) or document with # fire-and-forget comment",
      "effort": "S"
    }
  ],
  "coverage": {
    "http_abstraction": 75,
    "error_centralization": false,
    "transaction_boundary_consistent": false,
    "session_ownership_consistent": true,
    "async_io_consistent": false,
    "fire_and_forget_handled": false
  }
}
```

## Critical Rules

- **Read architecture.md first** - never assume architecture type
- **Skip violations list** - respect legacy files marked for gradual fix
- **File + line + code** - always provide exact location with context
- **Actionable suggestions** - always tell WHERE to move the code
- **No false positives** - verify path contains forbidden dir, not just substring

## Definition of Done

- Architecture discovered from docs/architecture.md (or fallback used)
- All violation types from common_patterns.md checked
- **Cross-layer consistency checked:**
  - Transaction boundaries analyzed (commit/rollback distribution)
  - Session ownership analyzed (DI vs local)
  - Async consistency analyzed (sync I/O in async functions)
  - Fire-and-forget tasks analyzed (error handling)
- Coverage calculated for HTTP abstraction + 4 consistency metrics
- Violations list with severity, location, suggestion
- Summary counts returned to coordinator

## Reference Files

- Layer rules: `../ln-640-pattern-evolution-auditor/references/common_patterns.md`
- Scoring impact: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`

---

**Version:** 2.0.0
**Last Updated:** 2026-02-04
