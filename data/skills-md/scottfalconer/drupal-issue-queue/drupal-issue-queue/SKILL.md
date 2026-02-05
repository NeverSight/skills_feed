---
name: drupal-issue-queue
description: Search Drupal.org issue queues and summarize individual issues via the Drupal.org api-d7 endpoints. Use for triage or debugging errors by checking for existing issues before patching, filtering by status/priority/category/version/component/tag, summarizing issue threads, or extracting recent patches/files into JSON or Markdown while respecting Drupal.org API constraints (single-threaded, cached, rate-limited, read-only).
---

# Drupal Issue Queue

## Guardrails

- Use the Drupal.org API only; do not scrape HTML.
- Keep requests single-threaded, cached, and rate-limited.
- Respect request budgets and Retry-After headers.
- Prefer small, scoped queries with explicit limits.

## Commands

### Summarize an issue

```bash
python scripts/dorg.py issue <nid-or-url> --format json
python scripts/dorg.py issue <nid-or-url> --format md
```

Common options:

- `--mode summary|full` (default: `summary`)
- `--comments N` (default: 10 in summary mode, 50 in full mode)
- `--files-limit N|all|0` (default: 10)
- `--resolve-tags none|api|static` (default: `api`)
- `--tag-map path/to/map.json` (required when `--resolve-tags=static`)
- `--related-mrs` or `--extra-credit`
- `--max-requests`, `--sleep-ms`, `--cache-ttl`, `--user-agent`

### Search issues in a project

```bash
python scripts/dorg.py search --project <machine_name> --format json
```

Common filters:

- `--status <alias|code>`
- `--priority <alias|code>`
- `--category <alias|code>`
- `--version <string>`
- `--component <string>`
- `--tag-tid <tid>`
- `--limit N --sort changed|created|nid --direction ASC|DESC`

## Outputs

- JSON output is structured for downstream agents; see `references/output-schema.md`.
- Markdown output provides a human-readable summary and is suitable for briefings.

## References

- `references/drupalorg-api-d7.md` for endpoints, limits, and headers.
- `references/issue-field-mappings.md` for status/priority/category codes and aliases.
- `references/output-schema.md` for JSON schema and examples.
