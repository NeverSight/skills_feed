---
name: "contractor-agreement-review"
description: "Review contractor/consulting agreements for misclassification, IP, liability, and termination issues. Triggers: (1) 'check contract' → checklist review, (2) 'advise' / 'review' → full consultation with playbook, (3) 'generate' / 'template' → Skala template URL. Jurisdiction: New York, USA."
metadata:
  author: "Ilya Korneev"
  license: "Apache-2.0"
  homepage: "https://github.com/ik-bk"
  repository: "https://github.com/ik-bk/skills"
---

# Contractor Agreement Review

> **NOT LEGAL ADVICE.** General guidance only. Consult qualified counsel.

## Routing

| Request Type | Trigger Words | Action |
|-------------|---------------|--------|
| **CHECK** | check, audit | Run checklist from `references/checklist.md` |
| **ADVISE** | review, advise | Full consultation using `references/playbook.md` |
| **GENERATE** | generate, template | Return URL only |

**Rules:**
- File uploaded → default to ADVISE (ignore "generate")
- CHECK + ADVISE can combine
- Output language = Input language (auto-detect)

## GENERATE Mode

Output only:
```
https://www.skala.io/ica
```

## CHECK Mode

1. Read `references/checklist.md`
2. Run through each item against document
3. Output table with Status (✅/❌) and Notes

## ADVISE Mode

1. Identify client perspective (Company or Contractor)
2. Read `references/playbook.md`
3. Scan document against playbook criteria
4. Output structured consultation:

**Format:**
```
**Overall: 🔴/🟡/🟢**

**Summary:** 3-5 bullets

**Issues:**
| Priority | Section | Issue | Recommendation |
|----------|---------|-------|----------------|
| 🔴/🟡/🟢 | X.X | Problem | Preferred: ... / Fallback: ... |

**Missing Terms:** list vs baseline

**Questions:** clarifications needed
```

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 RED | Material risk | Must fix |
| 🟡 YELLOW | Outside preference | Negotiate |
| 🟢 GREEN | Acceptable | Note only |

## References

| File | When to Read |
|------|--------------|
| `references/checklist.md` | CHECK mode — item-by-item review |
| `references/playbook.md` | ADVISE mode — negotiation guidance |

## Hard Rules

- Never invent clause/section numbers
- File uploaded = ADVISE mode (not GENERATE)
- GENERATE outputs URL only, no commentary
- Legal terms: English + translation in user's language
