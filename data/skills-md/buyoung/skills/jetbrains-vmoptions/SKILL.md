---
name: jetbrains-vmoptions
description: Provides JetBrains IDE VM options knowledge for version-specific GC selection and memory/performance tuning (JDK 17/21, IDE 222+). Cross-platform only.
---

# JetBrains IDE VM Options Capabilities

Provides reference knowledge to compose `.vmoptions` sets for JetBrains IDEs.
Output format: Markdown with code blocks containing `.vmoptions` lines (no file generation).

## Process Flow

```
Step 1: Collect Requirements
    │   └── Read [prerequisite-check.md] → Validate IDE version
    │
    ▼
Step 2: Research Options
    │   └── Read [gc-options.md], [memory-options.md], [common-options.md]
    │       based on user's goals
    │
    ▼
Step 3: Draft Output
    │   └── Generate preliminary vmoptions
    │
    ▼
Step 4: Self-Review
    │   └── Verify each option matches user's requirements
    │       Remove irrelevant or conflicting options
    │
    ▼
Step 5: Share & Review
    └── Present final vmoptions to user with explanations
```

## Scope

- IDE version ranges: 222-242 (JDK 17), 243+ (JDK 21)
- Cross-platform JVM options only (`.vmoptions`, one option per line, `#` comments)
- GC selection/tuning: Generational ZGC, ZGC, G1GC, Shenandoah, Parallel, Serial
- Memory/Code cache/Metaspace/Reference processing flags
- Compiler/runtime performance options commonly used for IDE tuning

## References

| File | Content |
|------|---------|
| [prerequisite-check.md](references/prerequisite-check.md) | **Required input validation logic (read first)** |
| [gc-options.md](references/gc-options.md) | Detailed GC flags and tuning parameters |
| [memory-options.md](references/memory-options.md) | Memory management options |
| [common-options.md](references/common-options.md) | Commonly used performance flags |
