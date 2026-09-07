---
name: callidescope-configure
description: Tell callidescope what to do — the command-line flags (--check, --write, --addresses, --directories, --format, --config, --json, --markdown) and the callidescope.config.ts they read alongside, covering depth, breadth, and spread limits, call-stack entry points, exclusions and ignored callees, the workspace's module layout, and where a run writes its JSON, markdown, mermaid, and per-project reports. Use when wiring a depth gate into CI or a commit hook, when a whole-workspace run is too slow, when choosing between --check and --write, when a repository has no callidescope configuration yet, when a trace judges code it should not be judging, when everything is reported as an orphan root, or when deciding where a committed report should live.
license: MIT
---

# Telling callidescope what to do

Two surfaces, read together on every run: the flags on the command line, and
the `callidescope.config.ts` they layer over. Neither is complete on its own —
`--check` names a limit the file has to have set, and a destination in the file
is only written when a flag asks for it.

## The two decisions a run makes

Every invocation answers two independent questions, and neither implies the
other:

| Question | Answered by |
| -------- | ----------- |
| What does this run fail on? | `--check`, a comma-separated set |
| What does this run rewrite? | `--write`, plus the destinations in the configuration |

A run given neither `--write` nor `--check reports` **reads no destination and
rewrites none**. It traces, prints, and exits. That is what makes a bare run
safe to type inside somebody's checkout, and it is why `--check depth` on a
pull request leaves every committed report exactly as it found it.

## The flags

| Flag | Meaning |
| ---- | ------- |
| `-a, --addresses` | Comma-separated callable addresses, each `<file>#<qualified-name>`. `depth` and `breadth` only. Prompted for when omitted |
| `--config` | Path to a `callidescope.config.ts`. Searched for when omitted |
| `-d, --directories` | Comma-separated project directories to trace, each holding its own `tsconfig.json` |
| `-f, --format` | `markdown`, `mermaid`, or `json`, for what it prints. Markdown by default |
| `--json` | Path to write the machine-readable report to |
| `-m, --markdown` | Path to splice the markdown block into |
| `--check` | Fail on a comma-separated set drawn from `breadth`, `depth`, and `reports` |
| `--write` | Write every configured destination |

`--config`, `--directories`, and `--format` are the three that `depth` and
`breadth` also take, and `--addresses` is theirs alone — it names what to
report on, which a whole-workspace trace never needs. The rest are the whole-workspace command's alone, because
a lookup never writes or compares a destination.

### `--check` takes a set, and the set matters

| Value | What fails the run |
| ----- | ------------------ |
| `depth` | A call stack deeper than `limits.maximumDepth` |
| `breadth` | A callable calling more callables directly than `limits.maximumBreadth` |
| `reports` | A configured destination no longer holding what a fresh run would write |

Three refusals to expect, all deliberate:

- **`--check` with no value is refused.** A set with nothing in it is
  indistinguishable from the flag having been left off, so reading it as "gate
  nothing" would produce a gate that cannot fail. `--check "$GATES"` with the
  variable unset would then pass forever over a stack twice as deep as anything
  allowed — worse than no gate, because it looks like protection.
- **An unrecognized value is refused**, and the message lists what is accepted.
- **`--check breadth` with no `limits.maximumBreadth` configured is refused.**
  Breadth is the one limit with no default: until a repository picks a number,
  nothing can exceed it, and falling back to an unbounded limit would look
  exactly like passing.

### Why `depth` and `reports` belong on opposite sides of a pull request

**Depth is the gate.** A stack got longer in this change, and this change is
what fixes it. Run it on every pull request, and on every commit if you like —
depth reads source and needs no build, which is what keeps it cheap enough for
a commit hook.

```bash
npx callidescope --check depth
```

**Staleness is not a gate.** A report goes stale whenever the call graph moves
anywhere, which is nearly every change. Gating on it would fail pull requests
for drift they did not cause. Publish the report on the default branch instead,
where nothing else is competing to rewrite the same block:

```bash
npx callidescope --write
```

`--write --check reports` is **refused outright**: a report cannot be stale in
the run that just wrote it, so a command line asking for both has misunderstood
one of them and would pass whatever it was meant to catch.

Those two are the whole target set. If a task runner is in play, neither may be
reachable from a composite task that forwards a configuration down its
dependencies — otherwise a `write` run from a branch publishes a report from a
branch. Name the depth gate directly alongside whatever else gates, rather than
hanging it off a lint-style aggregate.

### `--directories`, and why a run is slow without it

This is the difference between a whole-workspace analysis and a check that
finishes in seconds. Each directory named needs its own `tsconfig.json`, and
the programs built are those plus the ones of every project those directories
transitively import — so a call into a dependency still resolves to a real
frame:

```bash
npx callidescope -d packages/foo,packages/bar --check depth
```

Omit it and callidescope walks the working directory for every `tsconfig.json`
it can find. Reach for the wide run when you want the workspace-wide picture,
not when you want an answer about one package.

It takes **paths**, not project names. Callidescope has no idea what workspace
tool a repository uses; a directory holding a `tsconfig.json` is the whole
contract, and it holds in a monorepo, in a single package, or in neither. The
same list can be set once as `directories` in the configuration file.

There is a real trade-off when narrowing a `breadth` lookup: **callers outside
the named directories and the closure below them do not exist to the run** —
the closure runs downward, so a dependent that calls in is never built. For a
rename whose blast radius is the whole point, trace wide enough to contain
every consumer — a narrowed lookup reporting two callers when there are nine is
worse than a slow one.

An Nx workspace can hand the selecting to Nx instead, through the separate
`@callidescope/nx` plugin, which infers `trace`, `depth`, and `breadth` targets
onto every project and traces each one _with its Nx dependencies_ — so those
dependencies are projects the run is scoped to rather than ones it merely
reached through a closure. It is a separate package rather than a flag here on
purpose: this CLI depends on nothing Nx-shaped, and a flag that worked only
when an optional package happened to be installed would advertise in `--help`
something that silently did nothing.

### `--format` decides what prints, not what is written

Printing and writing are independent, and both can be on at once. `--format`
names one of `markdown` (the default), `mermaid`, or `json` for standard
output; the destinations in the configuration decide what reaches a file.
`markdown` is the default because it is the one rendering that reads in a
terminal, pastes into an issue, and is already what the files hold.

### Prompting, and why it will not hang a script

`callidescope`, `depth`, and `breadth` all prompt for a value left off the
command line — `depth` and `breadth` for a missing `--addresses`, all three for
a missing `--format`. There is no flag to turn that off, because **an attached
terminal is the whole condition**: a script, a hook, or a CI job never has one
and so is never prompted.

What each command does with a value it cannot ask for depends on whether
anything else could supply it:

| Value | With no terminal |
| ----- | ---------------- |
| `--addresses`, which `depth` and `breadth` need | **Refused**, exit non-zero. Nothing else can supply it |
| `--format` | The format in the configuration stands, and the run proceeds |

The refusal is the load-bearing half. `prompts` does not fail on a
non-terminal stdin — it draws its menu, never resolves, and lets the process
**exit 0 having done nothing** — so a required value asserts a terminal before
it prompts at all and reports a rejected command line instead. Without that,
a CI run that forgot an argument would read as a green one.

## The configuration file

Any of `callidescope.config.{ts,mts,cts,js,mjs,cjs,json,jsonc}`, searched for
upward from the working directory, TypeScript first because that is the form
that gets type checking. **Every field has a default except one**, so a file
names only what it wants to change.

```ts
import { type CallidescopeConfiguration } from "@callidescope/configuration";

const callidescopeConfiguration: CallidescopeConfiguration = {
  excludeFrom: ["configuration/.callidescopeignore"],
  limits: { maximumDepth: 6, spreadThreshold: 4 },
};

export default callidescopeConfiguration;
```

The whole surface is nine top-level keys: `allowSpreadFor`, `directories`,
`entryPoints`, `exclude`, `excludeFrom`, `ignoreCallees`, `limits`, `output`,
and `workspaceStructure`.

### `limits`

| Limit | Default | Meaning |
| ----- | ------- | ------- |
| `maximumDepth` | `6` | Frames a call stack may hold, entry point inclusive |
| `maximumBreadth` | **none** | Callables one callable may call directly |
| `spreadThreshold` | `4` | Distinct modules a callable's transitive callees may touch |
| `directSpreadThreshold` | `3` | Modules a callable must call _directly_ before spread is reported |
| `maximumImplementationCandidates` | `8` | Implementations one interface member may resolve to |
| `minimumCallers` | `2` | Callers a callable needs before its placement is judged |
| `callerMajorityRatio` | `0.8` | Share of callers in one foreign module that marks a callable misplaced |

Four are worth understanding rather than copying:

- **`maximumBreadth` has no default, on purpose.** Until a repository picks a
  number, nothing exceeds it and breadth is reported without being gated.
  `--check breadth` with none set is refused rather than falling back to an
  unbounded limit, because an unbounded limit looks exactly like passing.
- **`directSpreadThreshold` is what makes module spread mean anything.**
  Transitive reach alone flags every entry point, since an entry point
  legitimately reaches the whole program. Requiring direct breadth as well is
  what isolates the callable personally orchestrating unrelated concerns.
- **`maximumImplementationCandidates` is the primary noise control.** A
  structurally matched interface member named `run` or `sync` otherwise
  resolves to dozens of unrelated classes and manufactures a call stack no
  execution ever takes. Lower it when a report is full of stacks that could not
  happen; raise it and expect noise.
- **`minimumCallers` and `callerMajorityRatio` together define "misplaced".** A
  callable with one caller is not evidence of anything, which is why the floor
  exists.

Picking a first `maximumDepth`: run once with no gate, read the deepest stacks,
and set the limit at the shape you want rather than at whatever the code
currently is. A limit set to today's worst number gates nothing.

### `entryPoints`

| Option | Default | Meaning |
| ------ | ------- | ------- |
| `decorators` | 13 framework decorators | Decorators whose methods a framework invokes |
| `includeExportedFunctions` | `true` | Treat every `src/index.ts` export as a root |
| `includeOrphans` | `true` | Promote callables nothing in the repository calls |
| `includeTests` | `false` | Trace test files too |

`decorators` **replaces** the built-in list rather than adding to it, so a
configuration naming its own framework's decorator should restate the ones it
still wants. A report where nearly everything is an orphan root usually means
the decorators in use are not in this list.

**`includeOrphans` is a safety net rather than a feature.** Without it, a
missing entry-point rule silently removes whole subtrees from every
measurement. With it, they surface as orphan roots — which is itself worth
knowing, since an orphan is either dead code or a rule that needs adding. Turn
it off and you lose the signal that told you the configuration was incomplete.

### Keeping code out of a run

Three tools, for three different questions:

- **`exclude`** takes globs and is **additive** to the built-in defaults
  (`node_modules`, `dist`, `coverage`, `output`, `.nx`, `.conformetry`), so a
  configuration naming its own noise does not restate them.
- **`excludeFrom`** names gitignore-syntax files. This is how a long exclusion
  list stays out of the configuration file itself, and it is the right home for
  fixture packages written to be deliberately bad.
- **`ignoreCallees`** takes globs matched against a callable's display name
  (`Type.member`), and drops calls landing on a match from the graph entirely —
  counting toward neither the caller's depth nor its breadth. This is for
  cross-cutting instrumentation: every call to a logger is a fact about
  instrumentation, not about how deep or wide the code around it is, and
  counting it would move every other callable's numbers on a change that has
  nothing to do with them.

`exclude` and `excludeFrom` remove _files_. `ignoreCallees` removes _edges_.
Reaching for the first when you meant the second deletes real findings.

**`allowSpreadFor`** is narrower still: globs whose callables are exempt from
the module-spread finding alone, defaulting to command files, module files, and
`main.ts`. Orchestrating unrelated concerns is the job of a command; it is not
the job of a service.

### `directories` and `workspaceStructure`

`directories` is the same list `--directories` takes, set once.

`workspaceStructure` is only needed by a repository whose layout differs from
the tool's own assumptions, because module identity is what module spread and
misplacement are measured against: `modulesDirectory` (default `"modules"`) is
the subdirectory a module identifier is derived from, and `rootModuleSegment`
(default `"src"`) is the identifier for a file sitting directly under the
source root. Symptoms of getting it wrong are every file collapsing into one
module, so spread is never reported, or every file becoming its own module, so
everything looks misplaced.

### `output`

Every destination is optional, and unconfigured is the normal case: a run
naming no destination reports to the console and exits non-zero on violations,
so nothing it writes can go stale.

| Key | Purpose |
| --- | ------- |
| `output.format` | What the run **prints**: `markdown`, `mermaid`, or `json`. Default `markdown` |
| `output.json` | A machine-readable report at `path`, indented by `indentation` |
| `output.markdown` | A marker-delimited block spliced into `path` |
| `output.mermaid` | The same block with the stacks drawn as one flowchart |
| `output.projectReadmes` | One section per traced project, in that project's own readme |

`output.mermaid` takes the same keys as `output.markdown` — they differ in what
goes between the markers, not in how a block is placed — and is a separate
destination precisely so a repository can publish the printed trees _and_ the
diagram from one run. They answer different questions: the tree says what each
frame takes, returns, and documents; the diagram says what shape they make
together.

```ts
output: {
  json: { indentation: 2, path: "output/callidescope.json" },
  markdown: { path: "docs/call-stacks.md" },
  mermaid: { path: "docs/call-stacks-diagram.md" },
  projectReadmes: {},
},
```

`output.projectReadmes` takes `heading` (`## 🔭 Callidescope` by default),
`previewCount` (stacks shown before the rest fold into a disclosure, three by
default), and the same `startMarker`/`endMarker` pair the markdown destination
uses. `{}` accepts all four defaults — and is usually the right answer, because
which files those are follows from which projects were traced. Restating that
as a list of paths would only give it somewhere to drift from.

A markdown destination may also supply `render`, to replace the built-in
tables, or `write`, to place the block itself. A `write` function is handed
`syncAnchoredBlock` and `wrapInAnchors`, so a custom writer reuses the same
splice rather than reimplementing it. **Returning `false` reports the
destination as stale**; anything else, `undefined` included, counts as current.

## After changing any of this

A configuration change usually moves the numbers, which makes every committed
report stale. Re-run the write configuration in the same change, and lint
**before** regenerating rather than after: every frame carries a `file:line`,
so a formatter that sorts class members moves the line numbers of everything
after it, and a report written before that sort is stale the moment it lands.

When a run is refused or a report reads stale, reach for the
`callidescope-triage` skill. To read what a run printed, reach for
`callidescope-trace`.
