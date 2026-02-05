---
name: ln-641-pattern-analyzer
description: L3 Worker. Analyzes single pattern implementation, calculates 4 scores (compliance, completeness, quality, implementation), identifies gaps and issues. Usually invoked by ln-640, can also analyze a specific pattern on user request.
---

# Pattern Analyzer

L3 Worker that analyzes a single architectural pattern against best practices and calculates 4 scores.

## Purpose & Scope
- Analyze ONE pattern per invocation (receives pattern name, locations, best practices from coordinator)
- Find all implementations in codebase (Glob/Grep)
- Validate implementation exists and works
- Calculate 4 scores: compliance, completeness, quality, implementation
- Identify gaps and issues with severity and effort estimates
- Return structured analysis result to coordinator

## Input (from ln-640 coordinator)
```
- pattern: string          # Pattern name (e.g., "Job Processing")
- locations: string[]      # Known file paths/directories
- adr_reference: string    # Path to related ADR (if exists)
- bestPractices: object    # Best practices from MCP Ref/Context7/WebSearch
```

## Workflow

### Phase 1: Find Implementations
```
# Use locations from coordinator + additional search
files = []
files.append(Glob(locations))

# Expand search using common_patterns.md grep patterns
IF pattern == "Job Processing":
  files.append(Grep("Queue|Worker|Job|Bull|BullMQ", "**/*.{ts,js,py}"))
IF pattern == "Event-Driven":
  files.append(Grep("EventEmitter|publish|subscribe|on\\(", "**/*.{ts,js,py}"))
# ... etc

deduplicate(files)
```

### Phase 2: Read and Analyze Code
```
FOR EACH file IN files (limit: 10 key files):
  Read(file)
  Extract:
    - Components implemented
    - Patterns used
    - Error handling approach
    - Logging/observability
    - Tests coverage
```

### Phase 3: Calculate 4 Scores

**Compliance Score (0-100):**
```
score = 0

# Detection: ADR documentation exists
IF Glob("docs/adr/*{pattern}*.md") OR Glob("docs/architecture/*.md" contains pattern):
  +20

# Detection: Standard naming conventions
IF Grep("class.*{Pattern}(Service|Handler|Worker|Processor)", files):
  +15
IF file names follow pattern (e.g., job_processor.py, event_handler.ts):
  +15

# Detection: No anti-patterns
IF NOT Grep("(callback hell|Promise\.all without error|global state)", files):
  +20

# Detection: Industry standard structure
IF pattern == "Job Processing":
  IF Grep("(queue|worker|job|processor)", files) AND Grep("(retry|backoff|dlq)", files):
    +30
IF pattern == "Event-Driven":
  IF Grep("(EventEmitter|publish|subscribe|emit)", files) AND Grep("(schema|validate)", files):
    +30
```

**Completeness Score (0-100):**
```
score = 0

# Detection: Required components present
component_patterns = bestPractices[pattern].required_components  # from coordinator
FOR EACH component IN component_patterns:
  IF Grep(component.grep_pattern, files):
    +component.weight  # Total: 40 points

# Detection: Error handling
IF Grep("(try|catch|except|error|Error|Exception)", files):
  +10
IF Grep("(retry|backoff|circuit.?breaker)", files):
  +10

# Detection: Logging/observability
IF Grep("(logger|logging|log\\.|console\\.log|structlog)", files):
  +10
IF Grep("(metrics|prometheus|statsd|trace)", files):
  +5

# Detection: Tests exist
IF Glob("**/test*{pattern}*") OR Glob("**/*{pattern}*.test.*"):
  +15

# Detection: Documentation
IF Grep("docstring|@param|@returns|\"\"\"", files):
  +10
```

**Quality Score (0-100):**
```
score = 0

# Detection: Short methods (<50 lines)
method_lengths = analyze_method_lengths(files)
IF average(method_lengths) < 30: +25
ELIF average(method_lengths) < 50: +15

# Detection: Low cyclomatic complexity
IF NOT Grep("(if.*if.*if|for.*for.*for|switch.*case.*case.*case)", files):
  +25

# Detection: No code smells
IF NOT Grep("(TODO|FIXME|HACK|XXX|REFACTOR)", files):
  +10
IF NOT Grep("(magic number|hardcoded)", files):
  +10

# Detection: SOLID principles
IF Grep("(interface|abstract|Protocol|ABC)", files):  # Dependency Inversion
  +15

# Detection: Performance patterns
IF Grep("(async|await|asyncio|Promise)", files):  # Non-blocking
  +10
IF Grep("(cache|memoize|lru_cache)", files):
  +5
```

**Implementation Score (0-100):**
```
score = 0

# Detection: Code compiles/runs
IF no syntax errors in files:
  +30

# Detection: Used in production (imported elsewhere)
imports = Grep("from.*{pattern}|import.*{pattern}", codebase_root, exclude=files)
IF len(imports) > 0:
  +25

# Detection: No dead code
unused_exports = find_unused_exports(files)
IF len(unused_exports) == 0:
  +15

# Detection: Integrated with other patterns
IF Grep("(dependency.?injection|@inject|container)", files):
  +10
IF Grep("(config|settings|env)", files):
  +5

# Detection: Monitored
IF Grep("(health.?check|readiness|liveness|/health)", files):
  +10
IF Grep("(alert|alarm|notification)", files):
  +5
```

### Phase 4: Identify Issues and Gaps
```
issues = []
FOR EACH bestPractice IN bestPractices:
  IF NOT implemented:
    issues.append({
      severity: "HIGH" | "MEDIUM" | "LOW",
      category: "compliance" | "completeness" | "quality" | "implementation",
      issue: description,
      suggestion: how to fix,
      effort: estimate ("2h", "4h", "1d", "3d")
    })

gaps = {
  undocumented: aspects not in ADR,
  unimplemented: ADR decisions not in code
}

recommendations = [
  "Create ADR for X",
  "Update existing ADR with Y",
  "Refactor Z to match pattern"
]
```

### Phase 5: Calculate Overall Score
```
overall_score = average(compliance, completeness, quality, implementation) / 10
Example: (72 + 85 + 68 + 90) / 4 / 10 = 7.9
```

### Phase 6: Return Result
```json
{
  "pattern": "Job Processing",
  "overall_score": 7.9,
  "scores": {
    "compliance": 72,
    "completeness": 85,
    "quality": 68,
    "implementation": 90
  },
  "codeReferences": [
    "src/jobs/processor.ts",
    "src/workers/base.ts"
  ],
  "issues": [
    {
      "severity": "HIGH",
      "category": "quality",
      "issue": "No dead letter queue",
      "suggestion": "Add Bull DLQ configuration",
      "effort": "4h"
    }
  ],
  "gaps": {
    "undocumented": ["Error recovery strategy"],
    "unimplemented": ["Job prioritization from ADR"]
  },
  "recommendations": [
    "Create ADR for dead letter queue strategy"
  ]
}
```

## Critical Rules
- **One pattern only:** Analyze only the pattern passed by coordinator
- **Read before score:** Never score without reading actual code
- **Effort estimates:** Always provide realistic effort for each issue
- **Best practices comparison:** Use bestPractices from coordinator, not assumptions
- **Code references:** Always include file paths for findings

## Definition of Done
- All implementations found via Glob/Grep
- Key files read and analyzed
- 4 scores calculated with justification
- Issues identified with severity, category, suggestion, effort
- Gaps documented (undocumented, unimplemented)
- Recommendations provided
- Structured result returned to coordinator

## Reference Files
- Scoring rules: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`
- Common patterns: `../ln-640-pattern-evolution-auditor/references/common_patterns.md`

---
**Version:** 1.0.0
**Last Updated:** 2026-01-29
