---
name: project-scanner
description: Codebase analysis tool for quality-first editing. Scan before edit to understand relationships, patterns, and impact.
---

# Project Scanner Workflow

## Scanner Location

```
C:\Users\BLogic\.cursor\user-scripts\project-scanner\
```

## Commands

```bash
# Full scan
npx tsx scan.ts --path "<project-src-path>" --framework angular

# Query specific
npx tsx scan.ts --path "<project-src-path>" --framework angular --query "ClassName"
```

## Output Files

| File | When |
|------|------|
| `output.json` | Full scan |
| `output-query.json` | Query mode |

## When to Scan

| Situation | Action |
|-----------|--------|
| First time với project | Full scan |
| Edit shared service/utility | Query class |
| Change method signature | Query class → check calledBy |
| Delete/rename | Query → check all references |
| Create new code | Query similar existing |

## When NOT to Scan

- Simple typo fix
- Private method internal change
- New isolated code (0 callers)
- Already have context
- Comment/doc updates

## Quality Gates (MANDATORY)

| Trigger | MUST Check |
|---------|------------|
| Change method signature | `calledBy` |
| Class extends another | `inheritance` |
| Shared service | `summary.mostUsedServices` |
| Delete/rename | All references |

## Reading Output (Token-Efficient)

```
Full scan → Read ONLY summary section first
Query → Read calledBy + inheritance
```

**Key sections:**
- `calledBy`: Ai gọi method này
- `callChain`: Multi-level call path
- `inheritance`: Parent/child classes
- `deadCode`: Unused methods
- `summary.mostUsedServices`: High-impact services

## Pattern-First Principle

```
Before CREATE → Query similar existing code
Before EDIT → Check existing patterns
Follow 100% existing style
```

## Example Workflow

```
User: "Sửa SalonService.list()"

1. Query SalonService
2. Read calledBy → Biết SalonsComponent gọi
3. Check signature → Không đổi thì OK
4. Edit safely
```

## Integration

Scanner được reference từ:
- `angular-coding/SKILL.md` → Pre-edit analysis
