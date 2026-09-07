---
name: simplify-comments
description: Condense and de-duplicate the code comments introduced by the current worktree diff — remove comments that restate the code, merge repeated explanations, and shorten the rest — while obeying repository-specific comment guidelines when they exist. Use when asked to simplify, shorten, clean up, trim, or de-duplicate comments, to remove noisy or redundant comments from a branch or diff, or when the user says "simplify-comments".
compatibility: Run from inside a git repository. Requires bash and git. Edits only files already changed in the current worktree; it never commits, pushes, or touches unrelated files.
---

# simplify-comments

Rewrite the comments **added by the current worktree diff** into the shortest form that still carries information the code cannot. Repository guidelines win over every default in this skill.

## When to use

The user asks to simplify, shorten, tidy, or de-duplicate comments in the work in progress, or says "simplify-comments".

## Scope rules

- **Diff-scoped.** Only comment lines added or modified in the current worktree diff are candidates. Never touch comments in unchanged regions, unchanged files, or vendored/generated code.
- **Comments only.** Never change executable code, string literals, or test expectations. Line counts may shrink; behaviour must not change.
- **Never commit or push.** Leave the result in the working tree for the user to review.
- **Repository guidelines override this skill.** If the repository states a comment policy, apply it verbatim — including a policy of "no comments", which means delete rather than shorten.

## Instructions

### 1. Find the repository guidelines first

Read whichever of these exist, nearest file to the changed code first:

```bash
git rev-parse --show-toplevel
ls AGENTS.md CLAUDE.md CONTRIBUTING.md CONTRIBUTING.rst STYLEGUIDE.md docs/style*.md .editorconfig 2>/dev/null
ls .github/copilot-instructions.md .cursorrules .cursor/rules 2>/dev/null
```

Also check directory-level `AGENTS.md`/`CLAUDE.md` beside the changed files, and any linter config that governs comments (`.golangci.yml`, `rustfmt.toml`, `.eslintrc*`, `ruff.toml`, `pyproject.toml`, `.rubocop.yml`).

Extract the rules that apply to comments: whether comments are allowed at all, required doc-comment format for exported symbols, language, line length, capitalisation, punctuation, tag conventions. **These replace the defaults below.** Report which file supplied them.

If no guideline exists, use the defaults in [Default style](#default-style).

### 2. Collect the added comments

```bash
git status --short
git diff --stat            # unstaged
git diff --cached --stat   # staged
```

Review both staged and unstaged changes. If the branch has commits not yet on the base branch and the user means the whole branch, diff against the merge base instead:

```bash
git merge-base HEAD origin/HEAD          # or the base branch the user names
git diff --unified=3 <merge-base>...HEAD
```

List every added line that is a comment — `//`, `/* */`, `#`, `--`, `"""`, `'''`, `<!-- -->`, `%`, `;`, docstrings and doc comments (`///`, `/**`, `//!`, `##`). Read enough surrounding code to judge each one; a comment is only redundant relative to the code it sits on.

### 3. Classify each comment

| Verdict | Applies to | Action |
| ------- | ---------- | ------ |
| **Delete** | Restates the code (`// increment i`), narrates the diff (`// new helper`, `// moved from utils`), section banners, commented-out code, obvious type restatements, an AI-authored preamble on every block | Remove the line and any now-orphaned blank line |
| **Merge** | The same explanation repeated on sibling branches, loop bodies, cases, or test cases; a block comment repeating the function's doc comment | Keep one instance at the highest useful level; delete the copies |
| **Shorten** | Multi-sentence prose where a clause suffices; hedging and filler (`Note that`, `Basically`, `In order to`, `This function will`) | Compress to one line, imperative or declarative, no filler |
| **Keep** | Non-obvious *why*, invariants, units, ranges, ordering constraints, workarounds with a reason or link, safety/concurrency notes, `TODO`/`FIXME`/`SAFETY`/`NOSONAR`, licence headers, linter and compiler directives, doc comments the language or repo requires | Leave untouched |

When in doubt between Delete and Keep, prefer Keep — losing a real constraint costs more than one redundant line.

**Never delete** directives that change tooling behaviour: `//nolint`, `# noqa`, `# type: ignore`, `// eslint-disable*`, `// @ts-*`, `#[allow(...)]`, `//go:build`, `# pylint:`, `/* istanbul ignore */`, coverage and codegen markers, or SPDX/licence headers.

### 4. Rewrite

Apply the edits file by file. Preserve indentation, comment markers, and the file's existing comment style. Where a doc comment is mandatory (Go exported identifiers, Rust public items with `#![warn(missing_docs)]`, Python public API in a documented package, JSDoc in a typed API), keep it and shorten its prose instead of removing it.

### 5. Verify

```bash
git diff --stat
git diff
```

Confirm that every changed line is a comment line. Then run whatever the repository provides — formatter, linter, build, tests:

```bash
# examples; use the repo's own commands
gofmt -l . ; go build ./... ; cargo check ; npm run lint ; ruff check .
```

A build or lint failure after a comment-only edit means a directive or doc comment was removed — restore it.

### 6. Report

Give a short table and stop:

```markdown
| File | Deleted | Merged | Shortened | Kept |
| ---- | ------- | ------ | --------- | ---- |
| `src/parser.ts` | 6 | 2 | 3 | 4 |
```

State which guideline file was applied (or that defaults were used), and name any comment that was kept despite looking redundant, with the reason.

## Default style

Used only when the repository states nothing:

- One line where one line does. No comment where the code says it.
- Explain **why**, never **what**. The code is the *what*.
- No preamble, no restated signature, no diff narration, no attribution.
- Sentence case, no trailing period on single-line comments.
- No ticket identifiers, issue keys, author names, or dates — a permalink to an upstream bug is acceptable when it justifies a workaround.
- Keep the language of the surrounding comments.

## Edge cases

- **Repo forbids comments outright:** delete every non-directive comment added by the diff, including doc comments the language does not require. Say so in the report.
- **Language requires doc comments:** shorten, never delete; a missing doc comment can fail the build.
- **Comment is wrong, not just verbose:** do not silently rewrite a comment that contradicts the code — flag it to the user and let them decide.
- **Commented-out code:** delete it; it lives in history. If it is a deliberate example inside a doc comment, keep it.
- **Generated files:** skip anything with a `Code generated ... DO NOT EDIT` header, and skip vendored trees.
- **Diff touches a file's pre-existing comments only incidentally:** leave them; scope stays on added lines.
- **Nothing to simplify:** report that the added comments already meet the guidelines and change nothing.
- **Large diff:** work file by file (`git diff -- <path>`) rather than loading the whole diff at once.
