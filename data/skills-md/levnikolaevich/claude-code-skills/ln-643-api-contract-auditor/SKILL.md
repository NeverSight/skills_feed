---
name: ln-643-api-contract-auditor
description: "API contract audit worker (L3). Checks layer leakage in method signatures, missing DTOs, entity leakage to API, inconsistent error contracts, redundant method overloads. Returns findings with 4-score model (compliance, completeness, quality, implementation)."
allowed-tools: Read, Grep, Glob, Bash
---

# API Contract Auditor (L3 Worker)

Specialized worker auditing API contracts, method signatures at service boundaries, and DTO usage patterns.

## Purpose & Scope

- **Worker in ln-640 coordinator pipeline** - invoked by ln-640-pattern-evolution-auditor
- Audit **API contracts** at architecture level (service boundaries, layer separation)
- Check layer leakage, DTO patterns, error contract consistency
- Return structured analysis with 4 scores (compliance, completeness, quality, implementation)

**Out of Scope** (owned by ln-623-code-principles-auditor):
- Code duplication (same DTO shape repeated, same mapping logic, same validation)
- Report only ARCHITECTURE BOUNDARY findings (wrong layer, missing contract)

## Input (from ln-640 coordinator)

```
- pattern: "API Contracts"     # Pattern name
- locations: string[]          # Service/API directories
- adr_reference: string        # Path to related ADR
- bestPractices: object        # Best practices from MCP Ref/Context7

# Domain-aware (optional, from coordinator)
- domain_mode: "global" | "domain-aware"   # Default: "global"
- current_domain: string                   # e.g., "users", "billing" (only if domain-aware)
- scan_path: string                        # e.g., "src/users/" (only if domain-aware)
```

## Workflow

### Phase 0: Load References

**MANDATORY READ:** Load `references/detection_patterns.md` — language-specific Grep patterns for all 5 rules.

### Phase 1: Discover Service Boundaries

```
scan_root = scan_path IF domain_mode == "domain-aware" ELSE codebase_root

1. Find API layer: Glob("**/api/**/*.py", "**/routes/**/*.ts", "**/controllers/**/*.ts", root=scan_root)
2. Find service layer: Glob("**/services/**/*.py", "**/services/**/*.ts", root=scan_root)
3. Find domain layer: Glob("**/domain/**/*.py", "**/models/**/*.py", root=scan_root)
4. Map: which services are called by which API endpoints
```

### Phase 2: Analyze Contracts (5 Rules)

**MANDATORY READ:** Use detection_patterns.md for language-specific Grep patterns per rule.

| # | Rule | Severity | What to Check |
|---|------|----------|---------------|
| 1 | Layer Leakage | HIGH/MEDIUM | Service/domain accepts HTTP types (Request, parsed_body, headers) |
| 2 | Missing DTO | MEDIUM/LOW | 4+ params repeated in 2+ methods without grouping DTO |
| 3 | Entity Leakage | HIGH/MEDIUM | ORM entity returned from API without response DTO |
| 4 | Error Contracts | MEDIUM/LOW | Mixed error patterns (raise + return None) in same service |
| 5 | Redundant Overloads | LOW/MEDIUM | Method pairs with `_with_`/`_and_` suffix differing by 1-2 params |

**Scope boundary:** SKIP DUPLICATION findings (owned by ln-623), REPORT only ARCHITECTURE BOUNDARY findings.

### Phase 3: Calculate 4 Scores

**Compliance Score (0-100):**

| Criterion | Points |
|-----------|--------|
| No layer leakage (HTTP types in service) | +35 |
| Consistent error handling pattern | +25 |
| Follows project naming conventions | +20 |
| No entity leakage to API | +20 |

**Completeness Score (0-100):**

| Criterion | Points |
|-----------|--------|
| All service methods have typed params | +30 |
| All service methods have typed returns | +30 |
| DTOs defined for complex data | +20 |
| Error types documented/typed | +20 |

**Quality Score (0-100):**

| Criterion | Points |
|-----------|--------|
| No boolean flag params in service methods | +25 |
| No methods with >5 params without DTO | +25 |
| Consistent naming across module | +25 |
| No redundant overloads | +25 |

**Implementation Score (0-100):**

| Criterion | Points |
|-----------|--------|
| DTOs/schemas exist and are used | +30 |
| Type annotations present | +25 |
| Validation at boundaries (Pydantic, Zod) | +25 |
| API response DTOs separate from domain | +20 |

### Phase 4: Return Result

```json
{
  "pattern": "API Contracts",
  "overall_score": 6.75,
  "domain": "users",
  "scan_path": "src/users/",
  "scores": {
    "compliance": 65,
    "completeness": 70,
    "quality": 55,
    "implementation": 80
  },
  "checks": [
    {"id": "layer_leakage", "name": "Layer Leakage", "status": "failed", "details": "..."},
    {"id": "missing_dto", "name": "Missing DTO", "status": "warning", "details": "..."},
    {"id": "entity_leakage", "name": "Entity Leakage", "status": "passed", "details": "..."},
    {"id": "error_contracts", "name": "Error Contracts", "status": "warning", "details": "..."},
    {"id": "redundant_overloads", "name": "Redundant Overloads", "status": "passed", "details": "..."}
  ],
  "codeReferences": ["app/services/translation/", "app/api/v1/"],
  "issues": [
    {
      "severity": "HIGH",
      "location": "app/services/user/service.py:23",
      "issue": "Service accepts parsed_body: dict (HTTP layer leak)",
      "principle": "API Contract / Layer Leakage",
      "recommendation": "Create UserCreateDTO, accept typed params",
      "effort": "M",
      "domain": "users"
    }
  ],
  "gaps": {},
  "recommendations": []
}
```

## Critical Rules

- **Architecture-level only:** Focus on service boundaries, not internal implementation
- **Read before score:** Never score without reading actual service code
- **Scope boundary:** SKIP duplication findings (owned by ln-623)
- **Detection patterns:** Use language-specific Grep from detection_patterns.md
- **Domain-aware:** When domain_mode="domain-aware", scan only scan_path, tag findings with domain

## Definition of Done

- Service boundaries discovered (API, service, domain layers)
- Method signatures extracted and analyzed
- All 5 rules checked using detection_patterns.md
- Scope boundary applied (no duplication with ln-623)
- 4 scores calculated with justification
- Issues identified with severity, location, suggestion, effort
- If domain-aware: findings tagged with domain field
- Structured result returned to coordinator

## Reference Files

- Detection patterns: `references/detection_patterns.md`
- Scoring rules: `../ln-640-pattern-evolution-auditor/references/scoring_rules.md`
- Pattern library: `../ln-640-pattern-evolution-auditor/references/pattern_library.md`

---
**Version:** 2.0.0
**Last Updated:** 2026-02-08
