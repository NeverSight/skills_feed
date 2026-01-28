---
name: readthedocs-build-failure-triage
description: Triage Read the Docs build failures using build logs and config context. Use when a build fails, logs need analysis, or you need fix recommendations.
---

# Read the Docs Build Failure Triage

Use RTD build metadata plus raw build logs to identify the failure category and
recommend fixes. This is a diagnostic workflow, not just API wrapping.

## Required inputs

- RTD host in `RTD_HOST`
  - Community: `https://app.readthedocs.org`
  - Business: `https://app.readthedocs.com`
- API token available in `RTD_TOKEN` (preferred) or provided by the user
- Project slug
- Build logs (raw text) or a build URL the user can open

## Quick workflow

1. Fetch the latest build metadata.
2. Open the build page and view raw logs.
3. Identify the failure category and apply fixes.
4. If warnings are hidden, enable `sphinx.fail_on_warning` to make them visible.

## Get build metadata

Latest build:
```bash
curl -s -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/builds/?limit=1"
```

Specific build:
```bash
curl -s -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v3/projects/project-slug/builds/123456/"
```

Use the `urls.build` value from the API to open the build page. From there,
use the "View raw" link to copy the full log.

## Get the raw log directly

Read the Docs exposes raw build logs via the API v2 text endpoint:

```
GET ${RTD_HOST}/api/v2/build/{build_id}.txt
```

Example:
```bash
curl -s -H "Authorization: Token $RTD_TOKEN" \
  "${RTD_HOST}/api/v2/build/123456.txt"
```

## Common failure categories and fixes

### Dependency install failures

Symptoms: `pip install` errors, missing packages, resolver conflicts.

Actions:
- Verify `python.install` requirements path in `.readthedocs.yaml`.
- Pin versions for brittle deps and add missing build tools.
- For Sphinx autodoc failures, install the project with `python.install`:
  - `method: pip`
  - `path: .`

### Missing config file or wrong path

Symptoms: `conf.py` not found, `mkdocs.yml` not found.

Actions:
- Check `sphinx.configuration` or `mkdocs.configuration` paths.
- Confirm repo layout matches configured paths.

### Build tool mismatch

Symptoms: Sphinx config but MkDocs project (or vice versa).

Actions:
- Confirm `.readthedocs.yaml` uses the right tool block.
- Ensure dependencies align with the tool (Sphinx vs MkDocs).

### Warnings treated as failures

Symptoms: build fails after enabling warnings-as-errors.

Actions:
- Fix the warning in logs, or temporarily disable `sphinx.fail_on_warning`.
- Use warnings to prioritize broken references/imports.

### Resource limits or timeouts

Symptoms: build timeouts, memory errors, OOM kills.

Actions:
- Reduce build scope or switch to incremental tooling.
- Split large docs builds or trim heavy extensions.
- For Business, request more resources if needed.

### Version-specific failures

Symptoms: only a tag/branch fails.

Actions:
- Check version-specific dependencies or config drift.
- Verify `default_branch` and version slugs.
- If a version is obsolete, consider hiding it.

## Notes from RTD docs

- Use build logs to make warnings visible and fix underlying issues.
- Read the Docs can disable builds after too many consecutive failures.
- Build notifications (email/webhooks) help catch failures quickly.
