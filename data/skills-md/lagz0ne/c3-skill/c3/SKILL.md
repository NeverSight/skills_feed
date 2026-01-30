---
name: c3
description: |
  Routes C3 architecture requests and audits existing C3 documentation for consistency.
  Use when the user asks to "audit architecture", "validate C3", "check C3 docs", "verify docs",
  "check documentation", "are docs up to date", or when no .c3/ directory exists (routes to onboarding).
  Routes navigation to c3-query, changes to c3-alter, patterns to c3-ref, design to c3-provision.
---

# C3 Architecture Assistant

## REQUIRED: Load References

Before proceeding, use Glob to find and Read these files:
1. `**/references/skill-harness.md` - Red flags and complexity rules
2. `**/references/layer-navigation.md` - How to traverse C3 docs

## Intent Recognition & Routing

This skill is the **primary entry point** for C3 tasks. Route based on intent:

| User Says | Intent | Route To | Agent Chain |
|-----------|--------|----------|-------------|
| "pattern/convention/standard/ref/how should we" | Pattern | `/c3-ref` | (inline) |
| "provision/design/plan/envision/architect X" (no ref keywords) | Design-only | `/c3-provision` | (inline, stops at ADR) |
| "where/what/how/explain/show me" | Question | `/c3-query` | c3-navigator → c3-summarizer |
| "add/modify/remove/fix/refactor/implement" | Change | `/c3-alter` | c3-orchestrator → c3-analysis → c3-synthesizer → c3-dev |
| "audit/validate/check/verify/sync" | Audit | this skill | → c3-content-classifier |
| (no .c3/ directory) | Initialize | `/onboard` | (inline) |

**When unclear:** Ask "Do you want to explore (query), design only (provision), change and implement (alter), manage patterns (ref), or audit?"

---

## Mode: Adopt

Route to `/onboard` skill for the full staged learning loop.

---

## Mode: Audit

**REQUIRED:** Load `**/references/audit-checks.md` for full procedure.

| Scope | Command |
|-------|---------|
| Full system | `audit C3` |
| Container | `audit container c3-1` |
| ADR | `audit adr adr-YYYYMMDD-slug` |

**Checks:** Inventory vs code, categorization, reference validity, diagrams, ADR lifecycle, abstraction boundaries, content separation, context files

**Content Separation Check (Phase 9):**
- Verifies components contain domain logic, refs contain usage patterns
- Uses `c3-skill:c3-content-classifier` agent for LLM-based analysis
- Detects: missing refs for technologies, integration patterns in components, duplicated patterns

**Context Files Check (Phase 10):**
- Verifies CLAUDE.md files exist in Code Reference directories
- Checks c3-generated blocks are current (match component/refs)
- Detects: missing CLAUDE.md, stale blocks, orphaned blocks
- Resolution: Run `/c3 apply` to generate/update files

**Example:**
```
User: "Check if C3 docs are up to date"

1. Load audit-checks.md
2. Run Phase 1: Gather (list containers, components, ADRs)
3. Run Phase 2-10: Validate each check
4. Output audit report with PASS/FAIL/WARN per check
5. List actionable fixes for any failures
```

---

## Proactive Pattern Awareness

C3 provides **ambient pattern awareness** through CLAUDE.md files in code directories:

| Mechanism | How It Works |
|-----------|--------------|
| CLAUDE.md files | Generated in Code Reference directories, loaded automatically by Claude |
| `/c3 apply` | Generates/updates CLAUDE.md files based on component docs |
| Audit Phase 10 | Checks CLAUDE.md presence and freshness |

**Why CLAUDE.md over hooks:**
- Hooks fire too late (PreToolUse on Edit/Write happens after Claude decides what to change)
- Subagents don't receive SessionStart context
- CLAUDE.md loads at session start for all agents

**Legacy hooks** (still available but less reliable):

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `c3-context-loader` | Loads system goal, all refs, code→component mapping |
| PreToolUse (Edit/Write) | `c3-edit-context` | Surfaces relevant patterns when editing documented files |
| PreToolUse (Edit/Write) | `c3-gate` | Gates edits to ADR-approved files only |

---

## Mode: Apply

**Trigger:** User says "apply", "generate context", "propagate context", "create CLAUDE.md"

Generates CLAUDE.md files in directories listed in component Code References.

```
/c3 apply [--dry-run]

1. Scan .c3/c3-*/c3-*.md for Code References sections
2. For each referenced directory:
   - Create CLAUDE.md if missing
   - Update c3-generated block if stale
   - Preserve user content outside block
3. Report: created, updated, skipped counts
4. Files left unstaged for user review
```

**CLAUDE.md template:**
```markdown
<!-- c3-generated: c3-201 -->
# c3-201: Component Title

Before modifying this code, read:
- Component: `.c3/c3-2-api/c3-201.md`
- Patterns: `ref-error-handling`, `ref-logging`

Full refs: `.c3/refs/ref-{name}.md`
<!-- end-c3-generated -->
```

**Workflow:**
1. Run `/c3 audit` to see what's missing (Phase 10)
2. Run `/c3 apply` to generate files
3. Review and commit generated files
