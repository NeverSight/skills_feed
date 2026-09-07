---
name: service-scorecard
description: Audit a service repository and produce a shareable HTML report card grading it A–F across 23 facets — logic duplication, layering, API completeness and security, event contracts, storage, deployment, observability, coupling, maintenance effort, naming consistency, tests, error handling, dependencies, dead code, documentation rot, config and secrets, local dev experience, API versioning, domain boundaries, data migrations, performance shape, and repo navigability — each with the top 3 paths to improvement. Use when asked to score, grade, audit, assess, or review the quality, health, or maintainability of a service or codebase, or when the user says "service-scorecard".
compatibility: Run from the root of a git repository that contains a single service. Requires file read and shell access. Optional — a browser opener (`open`, `xdg-open`, or `start`) to display the report, and an artifact/document publishing capability if the user wants a hosted link instead of a local file.
---

# service-scorecard

Explore a service repository, grade it across 23 facets on an A–F report-card scale, and emit a styled, self-contained HTML report.

The objective driving every grade and every recommendation is: **simplify maintenance and improve discoverability**. When two readings of a facet are defensible, pick the one that answers "how fast can a newcomer find the right code and change it safely?"

## When to use

The user asks to score, grade, audit, or assess the quality, health, or maintainability of a service; asks for a report card on a codebase; or says "service-scorecard".

## Instructions

### 1. Confirm the target

Run from the repo root. Verify and capture context:

```bash
git rev-parse --show-toplevel
git remote get-url origin 2>/dev/null
git log -1 --format='%H %ad' --date=short
git rev-list --count HEAD
```

If the current directory is not a git repo, ask the user for the path instead of guessing.

If the repo is a monorepo holding several services, ask which service to grade and scope every command below to that subdirectory. Do not grade a whole monorepo as one service — the grades become meaningless.

### 2. Ask where the report goes

Ask this **before** the analysis, so the run is not interrupted at the end:

> Publish the report as a shareable artifact/hosted link, or write it to a temp file?

Both routes end with the report opened in the default browser. Record the answer and continue.

### 3. Survey the repository

Build a cheap map first, then read deeply only where a grade needs evidence. Do not read every file.

```bash
git ls-files | head -400
git ls-files | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -40
git ls-files | sed -n 's/.*\.\([a-zA-Z0-9]*\)$/\1/p' | sort | uniq -c | sort -rn | head -20
git ls-files | xargs wc -l 2>/dev/null | sort -rn | head -30
```

Identify, and note the evidence paths for each:

- **Language and framework** — manifest files (`go.mod`, `package.json`, `Cargo.toml`, `pyproject.toml`, `pom.xml`, …).
- **Entrypoint(s)** — `main.*`, `cmd/`, `src/index.*`, `app.py`, container `CMD`.
- **Layer structure** — directory names that read as layers (`handler`, `controller`, `service`, `usecase`, `repository`, `store`, `dao`, `model`, `dto`, `mapper`).
- **API surface** — route registrations, OpenAPI/protobuf/GraphQL schemas, handler files.
- **Storage** — migrations, ORM models, raw SQL, cache clients, queue clients.
- **Deployment** — `Dockerfile`, `k8s/`, Helm charts, Terraform, CI deploy jobs.
- **Observability** — metrics/tracing/logging library imports and their call sites.
- **Async contracts** — publish and subscribe call sites, topic/queue/subject names, message schemas, DLQ and retry configuration, consumer groups.
- **Outbound calls** — HTTP clients, gRPC stubs, SDKs, queue producers pointing at other services.
- **Tests** — test file count and placement versus source file count.
- **Docs** — `README`, `docs/`, ADRs, runbooks, `Makefile`, `docker-compose.yml`, devcontainer. Note the last commit date of each against the code it describes.

Prefer targeted searches over bulk reads. Useful probes:

```bash
git grep -lE 'func (Get|Post|Put|Patch|Delete)|@(Get|Post|Put|Patch|Delete)Mapping|app\.(get|post|put|patch|delete)|router\.(HandleFunc|Handle)|@app\.route'
git grep -lniE 'authenticat|authoriz|jwt|oauth|bearer|api[_-]?key|middleware.*auth'
git grep -lniE 'prometheus|opentelemetry|otel|datadog|statsd|zap|logrus|slog|winston|structlog'
git grep -lniE 'kafka|nats|rabbit|amqp|sqs|sns|pubsub|eventbridge|kinesis|redis.*stream|celery|sidekiq'
git grep -nEi 'publish|produce|emit|subscribe|consume|\.ack\(|dead[_-]?letter|dlq' | head -40
git grep -nE '(TODO|FIXME|HACK|XXX|DEPRECATED)' | wc -l
```

Adapt every probe to the language actually found — these are starting points, not a fixed list.

### 4. Grade each facet

Read [references/rubric.md](references/rubric.md) for all 23 facets: what each measures, the concrete signals to look for, the A/C/F anchors, and each facet's weight.

Rules that apply to every facet:

- **Evidence or no claim.** Every grade cites at least one concrete path, and ideally a `path:line`. A grade you cannot support with a path is a guess — say so in the report rather than dressing it up.
- **Grade what exists, not what you wish existed.** A small service with two layers is not under-engineered; it is appropriately sized. The rubric anchors are written to reward fit, not ceremony.
- **N/A is a legitimate result.** A service with no database gets N/A on storage simplicity, not an F. N/A facets are excluded from the overall grade and shown as N/A in the report.
- **Three paths to improvement per facet, always.** Ranked by impact on maintenance and discoverability. Each one names the file or directory it applies to and states the concrete change. "Improve naming" is not a path to improvement; "rename `svc/h.go`'s `Do()` / `Do2()` / `DoX()` to the operations they perform" is.
- **A facet graded A still gets three paths.** Frame them as the next increments, not invented problems.

### 5. Compute the overall grade

Grades convert to points: **A=5, B=4, C=3, D=2, E=1, F=0**.

```
overall_points = Σ(weight × points) / Σ(weight)      # N/A facets excluded from both sums
```

Map back to a letter: `≥4.5 → A`, `≥3.5 → B`, `≥2.5 → C`, `≥1.5 → D`, `≥0.5 → E`, else `F`.

Weights are in the rubric. The report prints the weights and the arithmetic so the number is auditable — never present the overall grade without them.

### 6. Render the report

Start from [assets/report-template.html](assets/report-template.html). It is a complete, self-contained, theme-aware document: no external fonts, scripts, stylesheets, or images. Keep it that way — a report that only renders on your machine is not shareable.

[references/template-tokens.md](references/template-tokens.md) lists every token, which three elements are duplicated per facet, and the rules for filling them. Delete any token you cannot fill rather than leaving it visible.

Ordering: both the summary grid and the facet sections run worst grade first — F to A, then N/A last — so the reader meets the problems before the praise. Break ties on grade by weight, heaviest first. Keep the two lists in the same order so a chip and its section line up.

### 7. Deliver

**Temp file route:**

```bash
out="${TMPDIR:-/tmp}/service-scorecard-<service>-$(date +%Y%m%d-%H%M%S).html"
```

Write the complete document there, then open it:

```bash
open "$out"        # macOS
xdg-open "$out"    # Linux
start "" "$out"    # Windows
```

Report the path.

**Artifact / hosted route:**

Publish the report with whatever artifact or document publishing capability the agent has. If that agent also has design guidance for published pages, load and follow it before writing the file. If the publishing surface supplies its own `<!doctype>`/`<head>`/`<body>` wrapper, strip those tags from the template and keep the `<title>` and `<style>` at the top of the content. Open the returned URL in the browser with the same opener command, and report the URL.

If no publishing capability exists, say so and fall back to the temp file rather than silently downgrading.

### 8. Summarize in chat

Keep it to: overall grade, the three worst facets with their grades, and the single highest-impact fix. The detail lives in the report.

## Edge cases

- **Not a service** (library, CLI, infra-only repo): several facets go N/A. Say which and why in the report methodology, and confirm with the user before spending the analysis if more than a third of the facets would be N/A.
- **Monorepo:** scope to one service per run. Grading several means several reports.
- **Huge repo:** sample. Read the largest files, the entrypoints, and one representative slice per layer, then state in the report that the grade is based on a sample and name what was sampled.
- **Documentation with no code left to describe:** a doc for a removed component is rot, not navigability — grade it in facet 6 and recommend deletion, not an update.
- **Generated code** (`*.pb.go`, `openapi_gen.*`, `node_modules`, vendored trees): exclude from duplication, naming, dead-code, and maintenance grades. Say that it was excluded.
- **No tests at all:** test coverage is F, not N/A. Absence is a finding.
- **Repo with no HTTP/RPC surface** (worker, consumer): API completeness, security, and versioning go N/A, and event contract quality carries the contract grade — say so in the methodology note rather than leaving four blanks unexplained.
- **Both surfaces present:** grade the synchronous facets and the event facet independently. A well-documented REST API does not excuse untyped events, and the reverse is just as common.
- **Queue used only as internal state** (a job table, a work list with no external producer or consumer): event contract quality is N/A; the queue is graded under storage simplicity.
