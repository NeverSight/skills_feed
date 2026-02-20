---
name: google-zx-scripting
description: "Use when writing shell scripts, automation, build tools, file processing, or ad-hoc CLI tasks with Google's zx library. Covers command execution, process control, file operations, and scripting patterns."
metadata:
  author: Danilo Alonso
  version: "1.0"
  references: core-api, scripting-patterns, processing-recipes
---

# Google ZX Scripting


Use this skill when writing scripts with Google's `zx` library — the tool that makes shell scripting with JavaScript/TypeScript productive and safe. Read only the reference file(s) needed for the task.

## Quick Start

All zx scripts use the **lite** entry point for portability. Scripts are standalone `.mjs` files — no project setup required.

    #!/usr/bin/env npx zx

    import { $, fs, path, glob, chalk } from 'zx/core';

    const files = await glob('src/**/*.ts');
    await $`eslint ${files}`;

Run directly:

    chmod +x script.mjs && ./script.mjs
    # or
    npx zx script.mjs

## Critical Rules

1. **Always use `zx/core`** — import from `zx/core` (the lite bundle), never bare `zx`. This avoids the heavy CLI wrapper and keeps scripts lean and embeddable.
2. **Template literals auto-escape** — interpolated values in `` $`...` `` are automatically shell-quoted. Never manually quote interpolated variables: `` $`echo ${userInput}` `` is safe, `` $`echo "${userInput}"` `` double-quotes and may break.
3. **Arrays expand correctly** — `` $`cmd ${arrayOfArgs}` `` expands each element as a separate quoted argument. Use this for flags, file lists, etc.
4. **Non-zero exits throw** — by default, a failed command throws `ProcessOutput` as an error. Use `nothrow` option or `.nothrow()` to suppress when you expect failures (e.g., `grep` returning no matches).
5. **Use `within()` for isolation** — `within()` creates an async scope with its own `$.cwd`, `$.env`, and other settings. Essential for parallel tasks that need different working directories.
6. **Pipe with `.pipe()`** — use `` $`cmd1`.pipe($`cmd2`) `` instead of shell pipes. This keeps each process managed by zx.
7. **Prefer zx builtins over shell commands** — use `glob()` instead of `find`, `fs` instead of `cat`/`cp`/`mv`, `fetch()` instead of `curl`. These are cross-platform and return proper JS types.
8. **`cd()` is global** — `cd()` changes `$.cwd` for ALL subsequent commands. Use `within()` or `$({cwd: '/path'})` for scoped directory changes.
9. **Scripts must be `.mjs`** — use `.mjs` extension for top-level `await` support without bundler config.

## Reference Map

| Need | File |
|------|------|
| `$`, ProcessPromise, ProcessOutput, configuration, piping, streams | `references/core-api.md` |
| Ad-hoc scripts, CLI tools, build scripts, deployment, project scaffolding | `references/scripting-patterns.md` |
| File processing, data pipelines, batch ops, AI scripts, log analysis | `references/processing-recipes.md` |

## Task Routing

- Writing a quick one-off command or shell automation -> `references/scripting-patterns.md`
- Building a build/deploy/CI script -> `references/scripting-patterns.md`
- Processing files, data, logs, or batch operations -> `references/processing-recipes.md`
- Need API details for `$`, pipes, streams, config -> `references/core-api.md`
- Combining multiple patterns (e.g., build + process) -> read both relevant files

## Import Cheatsheet

    // Core — always start here
    import { $, fs, path, glob, chalk } from 'zx/core';

    // Additional utilities (import individually as needed)
    import { spinner, retry, question, echo, sleep, within,
             stdin, tmpdir, tmpfile, which, ps, kill,
             quote, YAML, argv, fetch } from 'zx/core';

## Conventions for Generated Scripts

1. **Shebang line**: Always include `#!/usr/bin/env npx zx` as the first line
2. **Error handling**: Wrap top-level logic in a main function with try/catch, or use `$.nothrow` selectively
3. **Output**: Use `chalk` for colored terminal output — green for success, red for errors, yellow for warnings, dim for secondary info
4. **Progress**: Use `spinner()` for long-running operations in interactive contexts
5. **Arguments**: Use `argv` (pre-parsed `minimist`) for CLI argument handling
6. **Temp files**: Use `tmpdir()` and `tmpfile()` — they auto-clean on exit
7. **Parallelism**: Use `Promise.all()` with `within()` for parallel operations that need isolation
