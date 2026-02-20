---
name: springboot-migration
description: Migrate Spring Boot projects to version 4.0 with Java 25, including Spring Modulith 2.0 and Testcontainers 2.x upgrades. Use when user requests upgrading Spring Boot, migrating to Java 25, updating dependencies to Spring Boot 4, mentions Jackson 3 migration, asks about starter renames (web→webmvc, aop→aspectj), fixing test annotations (@MockBean→@MockitoBean), or needs help with Spring Modulith 2.0 or Testcontainers 2.x compatibility. Analyzes codebase for migration issues and guides through changes with specific file references.
---

# Spring Boot Migration

## Critical Rules

**NEVER migrate blindly. ALWAYS scan the codebase first to understand the current state.**

**NEVER apply all migrations at once. ALWAYS follow the phased approach.**

**MANDATORY versions:** Java 25 + Spring Boot 4.0.x + Spring Modulith 2.0.x + Testcontainers 2.x

## Workflow

### Step 1: Scan Project

Use the migration scanner to identify what needs to be migrated:

```bash
# Run from the skill directory
python3 <SKILL_DIR>/scripts/scan_migration_issues.py /path/to/project

# Or if the skill is in .codex:
python3 .codex/springboot-migration/scripts/scan_migration_issues.py /path/to/project
```

**Note:** Replace `<SKILL_DIR>` with the actual path to this skill directory. When copying skills to `.codex/`, use the second form.

This will analyze:
- Spring Boot version and required changes
- Dependency issues (starter renames, version updates)
- Code issues (annotation changes, package relocations)
- Configuration issues (property renames, new defaults)
- Spring Modulith compatibility
- Testcontainers compatibility

### Step 2: Assess Migration Scope

Based on scan results, determine which migrations apply:

| Migration | Trigger | Reference |
|-----------|---------|-----------|
| **Spring Boot 4.0** | Any Spring Boot 3.x → 4.0 upgrade | `references/spring-boot-4-migration.md` |
| **Spring Modulith 2.0** | Using Spring Modulith 1.x | `references/spring-modulith-2-migration.md` |
| **Testcontainers 2.x** | Using Testcontainers 1.x | `references/testcontainers-2-migration.md` |

**Decision tree:**

```
Is project using Spring Boot 3.x?
├─ Yes → Spring Boot 4.0 migration required
│   ├─ Using Spring Modulith? → Also migrate Spring Modulith 2.0
│   ├─ Using Testcontainers? → Also migrate Testcontainers 2.x
│   └─ Read: references/spring-boot-4-migration.md
└─ No → Check individual component versions
```

### Step 3: Plan Migration Phases

**CRITICAL:** Migrations must be done in phases to ensure stability:

For scenario-specific guidance and common pitfalls, see `references/migration-overview.md` before planning.

#### Phase 1: Dependencies (Safe)
- Update `pom.xml` / `build.gradle`
- Rename starters (web→webmvc, aop→aspectj, etc.)
- Add missing dependencies (Spring Retry, etc.)
- Update version numbers

**Reference:** Each migration guide's "Dependency Changes" section

#### Phase 2: Code Changes (Breaking)
- Update imports and package relocations
- Migrate test annotations (@MockBean→@MockitoBean)
- Fix Jackson 3 usage (if applicable)
- Update Testcontainers imports (if applicable)

**Reference:** Each migration guide's "Code Changes" section

#### Phase 3: Configuration (Optional)
- Update application.properties
- Configure new Spring Boot 4 defaults
- Add Spring Modulith event store config (if applicable)

**Reference:** Each migration guide's "Configuration Changes" section

#### Phase 4: Testing (Mandatory)
- Run unit tests
- Run integration tests
- Verify container tests
- Check for deprecation warnings

### Step 4: Execute Migration

**For each phase:**

1. **Read the relevant migration guide** (don't skip this)
2. **Apply changes to files** identified in scan
3. **Verify after each phase** with tests
4. **DO NOT continue** if tests fail - fix issues first

**Migration order for multi-component upgrades:**
1. Spring Boot 4.0 first (base framework)
2. Spring Modulith 2.0 second (depends on Boot 4)
3. Testcontainers 2.x third (test infrastructure)

### Step 5: Verification Checklist

After migration, follow the verification sections in the relevant references.

## Quick Reference

### When to Load References

- **Spring Boot 4 issues** → `references/spring-boot-4-migration.md`
- **Spring Modulith 2 issues** → `references/spring-modulith-2-migration.md`
- **Testcontainers 2 issues** → `references/testcontainers-2-migration.md`
- **Scenarios, strategies, common issues** → `references/migration-overview.md`

### Available Scripts

- `scripts/scan_migration_issues.py` - Analyzes project for migration issues

## Anti-Patterns

| Don't | Do | Why |
|-------|-----|-----|
| Migrate everything at once | Migrate in phases | Easier debugging |
| Skip scanning | Scan first | Know the scope |
| Ignore test failures | Fix immediately | Prevents cascading issues |
| Use classic starters permanently | Migrate to modular eventually | Technical debt |
| Suppress type errors with `@ts-ignore` equivalent | Fix root cause | Maintainability |
| Skip reading migration guides | Read before implementing | Avoid mistakes |

## Key Principle

**Understand before changing. Verify after changing. Never skip testing.**
