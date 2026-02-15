---
name: thai-interpreter
description: Enable efficient communication between Thai-language users and agents by translating Thai prompts into English in two modes and by preventing Thai text corruption in files. Use when the user writes in Thai, asks for Thai-to-English interpretation, wants token-efficient prompt rewriting, or reports mojibake/replacement-character issues such as U+FFFD in saved files.
---

# Thai Interpreter

Interpret Thai user intent with two explicit modes while preserving meaning.

Use this mode selector first:

1. `Literal Translation`:
   - Translate Thai to natural English with high fidelity.
   - Preserve tone, nuance, and intent.
   - Do not compress unless requested.
2. `Execution Translation`:
   - Translate Thai to compact, execution-ready English.
   - Optimize for fewer tokens and direct agent action.
   - Keep wording concise; do not force a fixed response template.

Default to `Execution Translation` unless the user asks for direct/literal translation.

Use this workflow:

1. Extract user intent from Thai text.
2. Select translation mode based on user instruction.
3. Preserve key Thai domain terms, names, and literals exactly.
4. Produce English output in the chosen mode.
5. Validate any file write path for UTF-8 safety before finalizing.

## Prompt Compression Rules

Apply these rules for `Execution Translation`:

1. Convert long Thai narrative into concise, actionable instructions.
2. Remove repetition, filler phrases, and polite particles that do not affect behavior.
3. Preserve non-negotiable requirements exactly as written.
4. Keep dates, numbers, IDs, file paths, and code literals unchanged.
5. Keep the compressed instruction under 8 lines when possible.

## Literal Translation Rules

Apply these rules for `Literal Translation`:

1. Keep sentence-level meaning and pragmatic intent faithful to Thai source.
2. Preserve ambiguity if the original Thai is ambiguous.
3. Preserve names, domain terms, and quoted literals exactly.
4. Do not add implementation assumptions unless requested.
5. Keep formatting close to the source when practical.

## Thai Text Safety Rules

Always protect Thai text writes:

1. Use UTF-8 explicitly when creating or updating files.
2. Detect suspicious replacement characters (U+FFFD) before and after writing.
3. If corruption appears, stop and rewrite from clean source text.
4. Avoid lossy encoding conversions (for example ANSI/Windows-1252 fallback).
5. Re-open written files and verify expected Thai snippets.

For deep checks and command recipes, read:
- `references/encoding-playbook.md`
- `references/translation-rules.md`

For automated checks and safe writes, use:
- `scripts/check-thai-encoding.ps1`
- `scripts/write-utf8.ps1`

## Output Contract

When handling Thai requests, produce:

1. English translation in the selected mode.
2. Natural, user-facing phrasing by default (no forced mode label or fixed headings).
3. Only use explicit sections (for example `Goal`, `Inputs`, `Constraints`, `Output`) when the user asks for that format.
4. The implementation result (if execution is requested).
5. A brief encoding safety confirmation when files were changed.
