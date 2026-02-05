---
name: address-review
description: |
  Systematically address code review findings using TDD. Fixes in-scope issues, creates GitHub issues for out-of-scope items. Keywords: address review, fix review, review findings, TDD fix, code review response.
---

# Address Review Findings

Systematically work through code review findings: TDD for in-scope fixes, GitHub issues for out-of-scope items.

## Usage

```
/address-review              # Accept review from previous context
/address-review ./review.md  # From file
/address-review strict       # Only Critical items
/address-review verify       # Re-review after fixes
```

## Workflow

### 1. Parse Findings

Accept review output (from `/review-branch` or similar). Extract:
- File locations (`file.ts:42`)
- Severity (Critical, Important, Suggestion)
- Issue description
- Recommended fix

### 2. Categorize: In-Scope vs Out-of-Scope

Reference `references/scope-rules.md` for guidance.

**In-scope** (fix now with TDD):
- File in diff
- Critical or Important severity
- Localized fix (doesn't require architectural changes)

**Out-of-scope** (create GitHub issue):
- Pre-existing issues surfaced by review
- Suggestions / nice-to-haves
- Architectural changes requiring broader discussion
- Systemic issues touching many files

**When ambiguous:** Confirm with user via AskUserQuestion.

### 3. Fix In-Scope Items (TDD)

For each in-scope item, follow TDD:

1. **Write failing test** that exposes the issue
2. **Verify test fails** for the right reason
3. **Fix the code** minimally
4. **Verify test passes**
5. **Commit** with conventional format: `fix(scope): description`

Reference `references/tdd-fix-pattern.md` for the detailed workflow.

### 4. Create Issues for Out-of-Scope

For each out-of-scope item:

```bash
gh issue create \
  --title "[Type] Brief description" \
  --body "$(cat <<'EOF'
## Origin

Surfaced during code review of PR #[number] / branch `[branch-name]`

## Finding

[Quote the reviewer's finding]

## Recommended Action

[What should be done]

## Priority

[Critical/Important/Suggestion] — [Why deferred]

---
*Created by /address-review from [reviewer] finding*
EOF
)"
```

Reference `templates/deferred-issue.md` for the template.

### 5. Verify

After all fixes:

```bash
# Run quality gates
pnpm typecheck && pnpm lint && pnpm test

# Show what was fixed
git log --oneline main..HEAD
```

## Output Format

```markdown
## Address Review Summary

### Fixed (In-Scope)
| Finding | Commit | Test Added |
|---------|--------|------------|
| `file.ts:42` — [issue] | abc1234 | Yes |

### Deferred (Out-of-Scope)
| Finding | Issue | Reason |
|---------|-------|--------|
| [issue] | #123 | Pre-existing / Architectural |

### Quality Gates
- [ ] `pnpm typecheck` — ✅
- [ ] `pnpm lint` — ✅
- [ ] `pnpm test` — ✅ (X passed, Y new)

### Next Steps
- [ ] Run `/review-branch verify` to confirm all issues addressed
- [ ] Create PR with `/pr`
```

## Modes

**Default:** Address Critical + Important items. Create issues for Suggestions.

**`strict`:** Only address Critical items. Everything else becomes issues.

**`verify`:** Re-run `/review-branch` after fixes to confirm resolution.

## Philosophy

**No finding gets lost.** Every review item either:
1. Gets fixed with a test proving it's fixed
2. Becomes a tracked GitHub issue

This ensures compounding engineering: reviews produce permanent improvements, not just temporary fixes.
