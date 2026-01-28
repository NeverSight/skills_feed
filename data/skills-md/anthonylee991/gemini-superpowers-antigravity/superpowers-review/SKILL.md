---
name: superpowers-review
description: Reviews changes for correctness, edge cases, style, security, and maintainability with severity levels (Blocker/Major/Minor/Nit). Use before finalizing changes.
---

# Review Skill

## When to use this skill
- before delivering final code changes
- after implementing a planned set of steps
- before merging or shipping

## Severity levels
- **Blocker**: wrong behavior, security issue, data loss risk, broken tests/build
- **Major**: likely bug, missing edge cases, poor reliability
- **Minor**: style, clarity, small maintainability issues
- **Nit**: optional polish

## Checklist
1. Correctness vs requirements
2. Edge cases & error handling
3. Tests (adequate coverage, meaningful assertions)
4. Security (secrets, auth, injection, unsafe defaults)
5. Performance (obvious hotspots, N+1, unnecessary work)
6. Readability & maintainability
7. Docs / comments updated if needed

## Output format
- Blockers
- Majors
- Minors
- Nits
- Overall summary + next actions
