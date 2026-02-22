---
name: roslynskills-research
description: Roslyn-first C#/.NET coding workflow using RoslynSkills (roscli). Use when user asks for symbol navigation, semantic context, structured refactors (rename/transactions), workspace-backed diagnostics triage, or evidence capture for benchmark runs. Avoid for non-C# repos or tasks that do not need semantic certainty.
license: MIT
compatibility: Claude.ai / Claude Code. Requires local shell access (Bash or PowerShell) plus RoslynSkills CLI (roscli) and/or the RoslynSkills MCP server.
metadata:
  author: DNA Kode
  mcp-server: roslynskills
allowed-tools: "Bash Read Write Edit Grep Glob"
---

# RoslynSkills Research

Goal: use Roslyn semantics as the truth source (not regex) when correctness matters.

## Session Start

Run command inventory first:

```powershell
roscli list-commands --ids-only
roscli list-commands --stable-only --ids-only
roscli quickstart
```

If `roscli` is not on PATH, in this repository use:

```powershell
scripts\roscli.cmd list-commands --ids-only
scripts\roscli.cmd list-commands --stable-only --ids-only
scripts\roscli.cmd quickstart
```

Cross-platform wrapper:

```bash
bash scripts/roscli list-commands --ids-only
bash scripts/roscli list-commands --stable-only --ids-only
bash scripts/roscli quickstart
```

Pit-of-success contract:

- Discover: `list-commands --ids-only`
- Disambiguate args: `describe-command <command-id>`
- Execute semantic-first: `nav.*`, `ctx.*`, `diag.*` before text fallback
- Start stable-first: use `list-commands --stable-only --ids-only`; only step into `advanced`/`experimental` commands when needed
- Verify workspace binding: use `--workspace-path ... --require-workspace true` on project code
- Verify before finalize: diagnostics + build/tests

Mandatory policy: if you use non-Roslyn tooling to read/edit `.cs`, append a short entry to `ROSLYN_FALLBACK_REFLECTION_LOG.md`.

## Canonical Workflow (Find -> Edit -> Verify)

1) Find declaration coordinates (workspace-bound for project code):

```powershell
roscli nav.find_symbol src/MyFile.cs MySymbol --brief true --max-results 50 --workspace-path MyProject.csproj --require-workspace true
```

2) Apply a structured edit:

```powershell
roscli edit.rename_symbol src/MyFile.cs 42 17 NewName --apply true --max-diagnostics 50 --workspace-path MyProject.csproj --require-workspace true
```

3) If the edit response does not include post-edit diagnostics (or reports errors/warnings), verify:

```powershell
roscli diag.get_file_diagnostics src/MyFile.cs --workspace-path MyProject.csproj --require-workspace true
```

Investigative tracing (when target is unclear across many files):

```powershell
roscli ctx.search_text "RemoteUserAction" src --mode literal --max-results 120 --brief true
roscli nav.find_invocations src/MyFile.cs 42 17 --brief true --max-results 100 --workspace-path MyProject.csproj --require-workspace true
roscli nav.call_hierarchy src/MyFile.cs 42 17 --direction both --max-depth 2 --brief true --workspace-path MyProject.csproj --require-workspace true
roscli analyze.control_flow_graph src/MyFile.cs 42 17 --brief true --max-blocks 120 --max-edges 260 --workspace-path MyProject.csproj --require-workspace true
roscli analyze.dataflow_slice src/MyFile.cs 42 17 --brief true --max-symbols 120 --workspace-path MyProject.csproj --require-workspace true
roscli analyze.unused_private_symbols src --brief true --max-symbols 120
roscli analyze.dependency_violations src MyApp.Web MyApp.Application MyApp.Domain --direction toward_end --brief true
roscli analyze.impact_slice src/MyFile.cs 42 17 --brief true --include-callers true --include-callees true
roscli analyze.override_coverage src --coverage-threshold 0.6 --brief true
roscli analyze.async_risk_scan src --brief true --max-findings 120 --severity-filter warning --severity-filter info
```

Bundle multiple read-only probes in one call when useful:

```powershell
roscli run query.batch --input "{`"queries`":[{`"command_id`":`"ctx.search_text`",`"input`":{`"patterns`":[`"RemoteUserAction`",`"ReplicationUpdate`"],`"roots`":[`"src`"],`"mode`":`"literal`"}},{`"command_id`":`"nav.find_invocations`",`"input`":{`"file_path`":`"src/MyFile.cs`",`"line`":42,`"column`":17,`"brief`":true,`"workspace_path`":`"MyProject.csproj`",`"require_workspace`":true}}],`"continue_on_error`":true}"
```

## Troubleshooting (Fast Fail-Closed)

- Args/schema error: run `roscli describe-command <command-id>` once, fix args, retry.
- Workspace is `ad_hoc` for project code: rerun with explicit `--workspace-path ... --require-workspace true`.
- You see `CS0518` (missing core types): treat as invalid workspace binding and retry with correct workspace root.

## Deep Reference (Progressive Disclosure)

Keep this SKILL.md small. Use these references only when needed:

- `references/diagnostics.md`: workspace vs solution snapshots, common failure modes
- `references/sessions.md`: non-destructive sessions, apply-and-commit
- `references/performance.md`: published-mode speed knobs (`ROSCLI_USE_PUBLISHED`)
- `references/dependency-intel.md`: when to combine with `dotnet-inspect`
