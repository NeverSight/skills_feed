---
name: language
description: Verify non-English phrases in your manuscript. Checks grammar, period accuracy, dialect, and translations.
argument-hint: "[chapter] [language-name]"
---

Run the language-checker agent to verify all foreign language phrases in your manuscript.

## What This Does

1. Scans all chapters for non-English text
2. Identifies the language of each phrase
3. Verifies grammatical correctness
4. Checks period/historical appropriateness
5. Validates dialect and register (formality level)
6. Confirms translation accuracy where translations are provided
7. Resolves author markers (`**check**`, `[verify]`, etc.)

## Usage

```
/fiction:language                    # Check all chapters
/fiction:language 5                  # Check chapter 5 only
/fiction:language swedish            # Focus on Swedish phrases only
/fiction:language 3-7                # Check chapters 3 through 7
```

If arguments provided: $ARGUMENTS

## What It Catches

- **Grammatical errors** — Spelling, agreement, conjugation, case endings
- **Anachronisms** — Modern phrases in historical settings
- **Dialect mismatches** — Stockholm Swedish used where Gotland dialect expected
- **Register errors** — Wrong formality level (du/ni, tu/vous, du/Sie)
- **Translation issues** — English translations that miss nuance
- **Diacritical marks** — Missing or incorrect accents (o, u, e, etc.)

## Languages Supported

The agent can verify phrases in any language by using web research to cross-reference grammar rules, dictionaries, and native speaker resources. Common languages in fiction:

- Swedish, Norwegian, Danish, Finnish
- German, French, Italian, Spanish, Portuguese
- Russian, Polish, Ukrainian
- Yiddish, Hebrew
- Japanese (romanized or characters)
- Any language with online resources

## Parallel Processing

When checking a full manuscript, chapters are processed in parallel:

1. Spawn reader agents to extract all foreign phrases from each chapter
2. Aggregate findings
3. Verify each unique phrase (avoids duplicate research)
4. Generate comprehensive report

## Output

A report with:
- Summary statistics
- Issues found with suggested corrections
- Verified phrases (confirmation they're correct)
- Author markers resolved
- Phrases needing native speaker review

## When to Use

- After completing draft (catches errors before readers see them)
- Before sending to native speaker beta readers (reduces their workload)
- During revision when adding foreign dialogue
- After `/fiction:edit` for complete polish

## Example Issues Found

```markdown
### Issue 1: Anachronistic Phrase

**Location:** Chapter 12, line 87
**Original:** `"Det ar cool"`
**Language:** Swedish
**Problem:** "Cool" is a modern English loanword. Wouldn't be used in 1943 Swedish.
**Suggested fix:** `"Det ar fint"` or `"Det ar bra"`
**Severity:** Moderate
```

```markdown
### Issue 2: Register Mismatch

**Location:** Chapter 4, line 156
**Original:** `"Hur mar du?"`
**Language:** Swedish
**Problem:** Informal "du" form used in formal context. 1943 Swedish would use "ni" when addressing strangers.
**Suggested fix:** `"Hur mar ni?"`
**Severity:** Moderate
```

## Related Commands

- `/fiction:edit` — Line-level English editing
- `/fiction:review` — Story and craft feedback
- `/fiction:continuity` — Cross-chapter consistency (run separately)
