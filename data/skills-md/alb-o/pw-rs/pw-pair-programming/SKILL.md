---
name: pw-pair-programming
description: driver-to-navigator collaboration using pp (send messages, attach files, download artifacts) on pw protocol wrappers.
---

# pw-pair-programming

interact with the navigator using the pp.nu nushell script, uses pw protocol wrappers behind the scenes

* the driver (you) must collaborate with the navigator in back-and-forth loops
* the driver writes code and runs tools; the navigator steers design
* requires cdp connection to a debug-enabled browser with an active navigator session, user should already have this setup

## invocation

from a global skills directory (most basic usage):

`nu -I ~/.claude/skills/pw-pair-programming/scripts -c 'use pp.nu *; pp send "Hello"'`

## quickstart

1. write a prompt preamble to a temp file
2. run from your project root when using relative paths
3. use a nu list + splat for entries, and keep the `nu -c` body in single quotes so bash does not consume `$entries`
4. `pp send`/`pp brief` wait for navigator response to finish by default
	* be patient; set your bash tool timeout extremely high (2+ hours if possible), and let navigator take its time
	* if your timeout and no response returned, use `pp wait`, do NOT try to send more responses
	* use `--no-wait` only for fire-and-continue flows (not recommended for regular use)

example:

```bash
nu -I ~/.claude/skills/pw-pair-programming/scripts -c '
use pp.nu *
let entries = [
  "crates/worker/src/lib.rs"
  "crates/worker/src/supervisor.rs"
]
pp brief --preamble-file /tmp/preamble.md ...$entries
'
```

## commands

`pp send` send one message and wait for response by default (`--file` accepts *one* file path)
`pp compose` build message from preamble + context entries
`pp brief` compose + send and wait for response by default
`pp attach` attach files/text/images (binary-safe; infers common MIME types; add `--send` to submit)
`pp paste` paste inline text
`pp new` start fresh conversation
`pp set-model` set mode (`auto` | `instant` | `thinking` | `pro`)
`pp wait` wait for response
`pp get-response` fetch latest response
`pp history` transcript
`pp refresh` reload UI
`pp download` download artifacts

## <entries> formats

* full file: `src/main.rs` or `file:src/main.rs`
* line slice: `slice:path:start:end[:label]`
* shorthand line slice: `path:start-end` or `path:start-end,start-end`

## notes

* write preamble content to files instead of inline shell.
* when running inside `nu -c`, use single quotes around the script and prefer list + splat (`...$entries`) instead of bash-style line continuations.
* entries like `path:10-40`, can pass them directly as shorthand slices.
* the outer agent bash terminal tool may have its own timeout, hitting it means the flow will break, so set it very high (e.g. 2+ hours) when running pp.
* if compacting/summarizing context, always restore this skill or invoke the skill immediately again and continue the workflow loop (don't wait for confirmation/approval)
* sessions have a char size limit, if hit and starting pp new, continue the workflow loop (don't wait for confirmation/approval)
* ask about good commit breakpoints, committing progress is encouraged, but no upstream PRs/pushes
* always show your actual working files (entries), be honest and transparent, don't just summarize and pretend all is perfect
* if getting stuck, complexity rising, tests failing for unclear reason, SHOW TO NAVIGATOR AND GET ADVICE
