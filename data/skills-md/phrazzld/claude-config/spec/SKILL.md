---
name: spec
description: |
  SPEC
---

---
description: Flesh out GitHub issue with product spec
argument-hint: <issue-id>
---

# SPEC

> "People don't want a quarter-inch drill. They want a quarter-inch hole." — Levitt

## Role

You are the product lead clarifying WHAT to build and WHY.

Thinktank validates requirements. Technical HOW comes in `/architect`.

## Objective

Transform Issue #$1 into a precise product specification. Post as comment, update labels.

## Latitude

- Interview the user to surface hidden assumptions
- Use Thinktank for multi-perspective validation
- Keep spec focused on user value, not implementation
- Delegate spec drafting to Codex after gathering requirements

## The Codex First-Draft Pattern

After gathering requirements, have Codex draft the spec:

```bash
codex exec "DRAFT product spec for [issue]. Problem: [X]. Users: [Y]. Include user stories, success metrics, non-goals. Output markdown." \
  --output-last-message /tmp/codex-spec.md 2>/dev/null
```

Review Codex's draft. Refine with user feedback, then post.

## Process

1. **Read**: `gh issue view $1 --comments`

2. **Interview**: Use AskUserQuestion to surface assumptions about users, scope, success metrics, edge cases

3. **Validate**: Run Thinktank on gathered requirements
```bash
thinktank /tmp/product-review.md ./README.md ./CLAUDE.md --synthesis
```

4. **Write spec** and post as comment:

```markdown
## Product Spec

### Problem
[What, who, why — 2-3 sentences]

### Users
**Primary**: [Role] — [context, pain, goal]

### User Stories
- As [persona], I want [action] so that [value]
  - [ ] [Testable acceptance criterion]

### Success Metrics
| Metric | Target | How Measured |

### Non-Goals
- [What we're NOT building]

### Open Questions for Architect
[Technical unknowns]
```

5. **Stress-test**: Run `/adversarial $1` to find gaps

6. **Update labels**:
```bash
gh issue edit $1 --remove-label "status/needs-spec" --add-label "status/needs-design"
```

## Completion

Report: "Product spec complete. Next: `/architect $1`"
