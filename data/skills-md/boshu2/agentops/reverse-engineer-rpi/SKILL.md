---
name: reverse-engineer-rpi
description: >
  Reverse-engineer a product into a mechanically verifiable feature catalog + code map + specs using an RPI-style loop.
  Triggers: reverse engineer product, catalog full feature set, docs->code mapping, feature inventory, code map, “Ralph loop”,
  SaaS boundary mapping, security audit reverse engineering, authorized binary analysis.
metadata:
  tier: research
  internal: false
---

# /reverse-engineer-rpi

Reverse-engineer a product into a mechanically verifiable feature inventory + registry + spec set, with optional security-audit artifacts and validation gates.

## Hard Guardrails (MANDATORY)

- Only operate on code/binaries you own or have **explicit written authorization** to analyze.
- Do not provide steps to bypass protections/ToS or to extract proprietary source code/system prompts from third-party products.
- Do not output reconstructed proprietary source or embedded prompts from binaries (index only; redact in reports).
- Redact secrets/tokens/keys if encountered; run the secret-scan gate over outputs.
- Always separate: **docs say** vs **code proves** vs **hosted/control-plane**.

## One-Command Example

```bash
python3 skills/reverse-engineer-rpi/scripts/reverse_engineer_rpi.py ao \
  --authorized \
  --mode=binary \
  --binary-path="$(command -v ao)" \
  --output-dir=".agents/research/ao/"
```

If you do not have explicit written authorization to analyze that binary, do not run the above. Use the included demo fixture instead (see Self-Test below).

Repo-only example (no binary required):

```bash
python3 skills/reverse-engineer-rpi/scripts/reverse_engineer_rpi.py cc-sdd \
  --mode=repo \
  --upstream-repo="https://github.com/gotalab/cc-sdd.git" \
  --output-dir=".agents/research/cc-sdd/"
```

## Invocation Contract

Required:
- `product_name`

Optional:
- `--docs-sitemap-url` (recommended when available; supports `https://...` and `file:///...`)
- `--docs-features-prefix` (default: `docs/features/`)
- `--upstream-repo` (optional)
- `--local-clone-dir` (default: `.tmp/<product_name>`)
- `--output-dir` (default: `.agents/research/<product_name>/`)
- `--mode` (default: `repo`; allowed: `repo|binary|both`)
- `--binary-path` (required if `--mode` includes `binary`)
- `--no-materialize-archives` (authorized-only; binary mode extracts embedded ZIPs by default; this disables extraction and keeps index-only)

Security audit flags (optional):
- `--security-audit` (enables security artifacts + gates)
- `--sbom` (generate SBOM + dependency risk report where possible; may no-op with a note)
- `--fuzz` (only if a safe harness exists; timeboxed)

Mandatory guardrail flag:
- `--authorized` (required for binary mode; refuses to run binary analysis without it)

## Script-Driven Workflow

Run:

```bash
python3 skills/reverse-engineer-rpi/scripts/reverse_engineer_rpi.py <product_name> --authorized [flags...]
```

This generates the required outputs under `output_dir/` and (when applicable) `.agents/council/` and `.agents/learnings/`.

## Outputs (MUST be generated)

Core outputs under `output_dir/`:
1. `feature-inventory.md`
2. `feature-registry.yaml`
3. `validate-feature-registry.py`
4. `feature-catalog.md`
5. `spec-architecture.md`
6. `spec-code-map.md`
7. `spec-cli-surface.md` (only if a CLI exists; otherwise a note is written to `spec-code-map.md`)
8. `spec-clone-vs-use.md`
9. `spec-clone-mvp.md` (original MVP spec; do not copy from target)

Binary-mode extras:
- `binary-analysis.md` (best-effort summary)
- `binary-embedded-archives.md` (index only; no dumps)

Repo-mode extras:
- `spec-artifact-surface.md` (best-effort; template/manifest driven install surface)
- `artifact-registry.json` (best-effort; hashed template inventory when manifests/templates exist)

If `--security-audit`, also create `output_dir/security/`:
- `threat-model.md`
- `attack-surface.md`
- `dataflow.md`
- `crypto-review.md`
- `authn-authz.md`
- `findings.md`
- `reproducibility.md`
- `validate-security-audit.sh`

## Self-Test (Acceptance Criteria)

End-to-end fixture (safe, owned demo binary with embedded ZIP):

```bash
bash skills/reverse-engineer-rpi/scripts/self_test.sh
```

This must show:
- feature inventory generated
- registry generated
- registry validator exits 0
- in security mode: `validate-security-audit.sh` exits 0 and secret scan passes
