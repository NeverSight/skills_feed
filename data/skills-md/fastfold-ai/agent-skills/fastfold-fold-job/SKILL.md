---
name: fastfold-fold-job
description: Submits and manages FastFold protein folding jobs via the Jobs API. Covers authentication, creating jobs, polling for completion, and fetching CIF/PDB URLs, metrics, and viewer links. Use when folding protein sequences with FastFold, calling the FastFold API, or scripting fold-and-wait workflows.
---

# FastFold Fold Job

## Overview

This skill guides correct use of the [FastFold Jobs API](https://docs.fastfold.ai/docs/api): create fold jobs, wait for completion with polling, then fetch results (CIF/PDB URLs, metrics, viewer link). Use the bundled OpenAPI schema and scripts in this skill for consistent behavior (skill is self-contained).

## Authentication

**Get an API key:** Create a key in the [FastFold dashboard](https://cloud.fastfold.ai/api-keys). Keep it secret; anyone with the key can make requests on your behalf.

**Use the key:** Send it in the `Authorization` header:

```
Authorization: Bearer <your-api-key>
```

- **`.env` file (recommended):** Scripts automatically load `FASTFOLD_API_KEY` from a `.env` file in the project (current dir or any parent). Do not commit `.env`.
- **Environment:** `export FASTFOLD_API_KEY="sk-..."` (overrides `.env` if both set).
- **Scripts** read `FASTFOLD_API_KEY` from env (after loading `.env`); override with `--api-key` when needed.

**Agent — when the user needs to set the API key:** If `FASTFOLD_API_KEY` is not set and the user has not provided `--api-key`:

1. **Copy the template for the user:** Copy `skills/fastfold-fold-job/references/.env.example` to `.env` at the **workspace (project) root**. Create the `.env` file yourself (e.g. read the example file and write its contents to `.env`); do not ask the user to run the copy command.
2. **Guide the user:** Tell the user that a `.env` file has been created and they need to add their key. Say: *"Open the `.env` file in the project root and paste your FastFold API key after the `=` on the line `FASTFOLD_API_KEY=`. You can create a key at [FastFold API Keys](https://cloud.fastfold.ai/api-keys) if you don’t have one. Save the file when done."*
3. **Offer to run the workflow:** Add: *"Let me know when you’ve pasted your key—I can run the create job and the rest of the steps (wait for completion, fetch results, download CIF, viewer link) for you."* Do not give the user a list of commands to run themselves; offer to execute the scripts yourself once the key is set.
4. **Wait:** Do not run create job, wait, fetch, or download until the user confirms they have pasted and saved the key (or provides the key via `--api-key` / env). After they confirm, run the scripts from the workspace root using the path `skills/fastfold-fold-job/scripts/` (e.g. `python skills/fastfold-fold-job/scripts/create_job.py ...`), not `.agents/...`.

**Required before any authenticated action:** If `FASTFOLD_API_KEY` is not set and no `--api-key` was given, follow the Agent steps above (create `.env` from `references/.env.example`, then ask the user to paste the key and confirm). Only proceed with jobs after the key is set.

Public jobs (`isPublic: true`) can be read without auth via Get Job Results; private jobs require the owner’s API key. See [references/auth_and_api.md](references/auth_and_api.md) for details and quota limits.

## When to Use This Skill

- User wants to fold a protein sequence with FastFold (API or scripts).
- User mentions FastFold API, fold job, CIF/PDB results, or viewer link.
- User needs to script: create job → wait for completion → download results / metrics / viewer URL.

## Workflow: Create → Wait → Results

0. **Ensure API key is set** – If `FASTFOLD_API_KEY` is not set (and no `--api-key` given), copy `skills/fastfold-fold-job/references/.env.example` to `.env` at the project root, then ask the user to open `.env` and paste their key after `FASTFOLD_API_KEY=`. Do not proceed until they confirm.
1. **Create job** – POST `/v1/jobs` with `name`, `sequences`, `params` (required). Optional: `isPublic`, `constraints`, `from` (library ID). See schema in this skill: [references/jobs.yaml](references/jobs.yaml).
2. **Wait for completion** – Poll GET `/v1/jobs/{jobId}/results` until `job.status` is `COMPLETED`, `FAILED`, or `STOPPED`. Use a 5–10 s interval and a timeout (e.g. 900 s).
3. **Fetch results** – For `COMPLETED` jobs: read `cif_url`, `pdb_url`, metrics (e.g. `meanPLLDT`, `ptm_score`, `iptm_score`), and build viewer link. Complex vs non-complex jobs differ (see below).

**Scripts:** Prefer the bundled scripts so behavior matches the SDK. From the **workspace root**, run them as e.g. `python skills/fastfold-fold-job/scripts/create_job.py ...` (use `skills/fastfold-fold-job/scripts/`, not `.agents/...`). The agent should run these scripts for the user, not hand them a list of commands.

- **Create job (two modes):**
  - **Simple (single protein):** `python scripts/create_job.py --name "My Job" --sequence MALW... [--model boltz-2] [--public]`
  - **Full payload (same as [FastFold Python SDK](https://github.com/fastfold-ai/fastfold-python) / JobInput):** `python scripts/create_job.py --payload job.json` or `python scripts/create_job.py --payload -` (stdin). Payload must be JSON with `name`, `sequences`, `params`; optional `constraints` (pocket, bond), `isPublic`, and sequence types: `proteinChain`, `rnaSequence`, `dnaSequence`, `ligandSequence`. Use this for multi-chain, ligands, constraints, or custom params (e.g. `recyclingSteps`, `relaxPrediction`) so the agent does not need to write one-off scripts. Examples in [references/jobs.yaml](references/jobs.yaml).
- **Wait for completion:** `python scripts/wait_for_completion.py <job_id> [--poll-interval 5] [--timeout 900]`
- **Fetch results (JSON):** `python scripts/fetch_results.py <job_id>`
- **Download CIF:** `python scripts/download_cif.py <job_id> [--out output.cif]`
- **Viewer link:** `python scripts/get_viewer_link.py <job_id>`

All scripts accept `--api-key` and `--base-url`; they use `FASTFOLD_API_KEY` and `https://api.fastfold.ai` by default.

## Complex vs Non-Complex Jobs

- **Complex** (e.g. boltz-2 single complex): Results have a single top-level `predictionPayload`; use `results.cif_url()`, `results.metrics()` once.
- **Non-complex** (e.g. multi-chain monomer/simplefold): Each sequence has its own `predictionPayload`; use `results[0].cif_url()`, `results[1].cif_url()`, etc., and `results[i].metrics()` per chain.

The scripts handle both: `fetch_results.py` and `download_cif.py` output or download the right CIF(s); `get_viewer_link.py` prints the job viewer URL (one URL per job on FastFold cloud).

## Job Status Values

- `PENDING` – Queued, not yet initialized  
- `INITIALIZED` – Ready to run  
- `RUNNING` – Processing  
- `COMPLETED` – Success; artifacts and metrics available  
- `FAILED` – Error  
- `STOPPED` – Stopped before completion  

Only use `cif_url`, `pdb_url`, metrics, and viewer link when status is `COMPLETED`.

## Viewer Link (3D structure)

For a completed job, the 3D structure viewer URL is:

`https://cloud.fastfold.ai/mol/new?from=jobs&job_id=<job_id>`

Use `scripts/get_viewer_link.py <job_id>` to print this URL. If the job is private, the user must be logged in to the same FastFold account to view it.

## Resources

- **Auth and API overview:** [references/auth_and_api.md](references/auth_and_api.md)  
- **Schema summary:** [references/schema_summary.md](references/schema_summary.md)  
- **Full request/response schema (in this skill):** [references/jobs.yaml](references/jobs.yaml)
