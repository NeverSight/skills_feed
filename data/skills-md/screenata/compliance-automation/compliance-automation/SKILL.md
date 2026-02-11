---
name: compliance-automation
description: Generate draft compliance policy documents (SOC 2, ISO 27001) with optional codebase, cloud infrastructure, and SaaS tool scanning for evidence, plus automated GitHub Actions workflows for recurring evidence collection. Use when the user needs to create compliance policies, security policies, or mentions SOC 2, ISO 27001, or audit preparation.
license: MIT
metadata:
  author: screenata
  version: "2.5"
---

# Compliance Automation

Generate draft compliance policy documents based on company context, answers to targeted questions, and optionally detected codebase evidence.

## Important Disclaimer

**GENERATED DRAFTS ONLY** - All policies require human review before use. These are starting points, not audit-ready documents.

## When to Use This Skill

Use this skill when the user:
- Needs to create compliance policies (SOC 2, ISO 27001, or both)
- Mentions SOC 2 certification, ISO 27001 certification, or audit preparation
- Asks for security policy templates
- Wants to generate compliance documentation

## Workflow

**CRITICAL: This is a conversational flow. Ask ONE question, wait for answer, then ask the next. NEVER list multiple questions in a single message.**

**CRITICAL: All session state MUST be written to the `.compliance/` folder.** Configuration goes in `.compliance/config.json`, progress tracking in `.compliance/status.md`, and policy answers in `.compliance/answers/`. Do NOT rely on in-memory context, agent-internal files (`.context/notes.md`, `.context/todos.md`), or conversation history. The `.compliance/` folder is the single source of truth — write to it after each significant step so progress survives session restarts.

### Step 1: Gather Company Context

**First, check for existing session state:**

Before asking any questions, check if `.compliance/config.json` exists. If it does:
1. Read `.compliance/config.json` to recover previously saved answers (org name, description, industry, size, executives, work model, devices, identity provider, data types, data location, hosting, frameworks, cert type, SaaS tools, report signoff, evidence method)
2. Read `.compliance/status.md` to recover progress on policies, SaaS tools, cloud providers, and workflows
3. Present a summary to the user:
   > I found your previous session state. Here's what I have:
   > - **Org:** [org_name] — [company_description]
   > - **Industry:** [industry], [company_size] employees, [work_model]
   > - **Infrastructure:** Hosted on [hosting_providers], data in [data_locations]
   > - **Identity:** [identity_provider], devices: [device_types]
   > - **Data types:** [data_types]
   > - **Frameworks:** [frameworks]
   > - **Cert:** [cert_type] (SOC 2 only)
   > - **Evidence method:** [evidence_method]
   > - **SaaS tools:** [saas_tools list]
   > - **Policies generated:** [count] of 17 ([names])
   > - **SaaS tools configured:** [count] of [total] fully wired
   >
   > Would you like to continue from where you left off, or start fresh?
4. If the user continues, skip all answered questions and jump to the next incomplete step (next pending policy, next untested SaaS tool, etc.)
5. If the user starts fresh, proceed with all questions below (`.compliance/` will be overwritten)

If `.compliance/config.json` exists but cannot be parsed, ask the user if they want to start fresh.

If `.compliance/config.json` does not exist, proceed with the questions below.

Ask each question separately. After receiving an answer, proceed to the next question.

**Update `.compliance/config.json` after every answer.** Create the `.compliance/` directory and `.compliance/config.json` after Q1 is answered. When creating the `.compliance/` directory, also ensure `.compliance/secrets.env` is in `.gitignore` (append it if not already present — this file will hold API tokens for local testing and must never be committed). Use the JSON format shown at the end of Step 1, with empty/null values for unanswered questions. After each subsequent question, update the corresponding field immediately. This ensures progress is saved even if the session ends between questions.

Field mapping: Q1 → `org_name`, Q2 → `company_description`, Q3 → `industry`, Q4 → `company_size`, Q5 → `executives`, Q6 → `work_model`, Q7 → `device_types`, Q8 → `identity_provider`, Q9 → `data_types`, Q10 → `data_locations`, Q11 → `hosting_providers`, Q12 → `frameworks`, Q12a → `cert_type` (SOC 2 only), Q13 → `saas_tools`, Q14 → `report_signoff`.

**Question 1** (ask first, wait for response):
> What is your organization's name?

**Question 2** (ask after Q1 answered):
> Describe your company in a few sentences — what does it do?

**Question 3** (ask after Q2 answered):
> What industry is your company in?
> 1. Healthcare
> 2. Fintech
> 3. B2B SaaS
> 4. E-commerce
> 5. Other

**Question 4** (ask after Q3 answered):
> How many employees do you have?
> 1. 1-10
> 2. 11-50
> 3. 51-200
> 4. 200+

**Question 5** (ask after Q4 answered):
> Who are your C-Suite executives? (names and titles, e.g. "Jane Doe — CEO, John Smith — CTO")

**Question 6** (ask after Q5 answered):
> How does your team work?
> 1. Fully remote
> 2. Hybrid (office + remote)
> 3. Office-based

**Question 7** (ask after Q6 answered):
> What devices do your team members use? (select all that apply)
> 1. Company-provided laptops
> 2. Personal laptops
> 3. Company phones
> 4. Personal phones
> 5. Tablets
> 6. Other (please specify)

**Question 8** (ask after Q7 answered):
> How do your team members sign in to work tools? (identity/SSO provider)
> 1. Google Workspace
> 2. Microsoft 365
> 3. Okta
> 4. Auth0
> 5. Email/Password (no SSO)
> 6. Other (please specify)

**Question 9** (ask after Q8 answered):
> What types of data do you handle? (select all that apply)
> 1. Customer PII
> 2. Payment information
> 3. Employee data
> 4. Health records
> 5. Intellectual property
> 6. Other (please specify)

**Question 10** (ask after Q9 answered):
> Where is your data located? (select all that apply)
> 1. North America
> 2. Europe (EU)
> 3. United Kingdom
> 4. Asia-Pacific
> 5. South America
> 6. Africa
> 7. Middle East
> 8. Australia/New Zealand

**Question 11** (ask after Q10 answered):

Before asking this question, auto-detect hosting providers from the codebase. Scan for:

- **Terraform providers:** Grep `*.tf` files for `provider "aws"` → AWS, `provider "google"` → Google Cloud, `provider "azurerm"` → Microsoft Azure, `provider "heroku"` → Heroku
- **Config files:** Glob for `vercel.json` → Vercel, `fly.toml` → Fly.io, `Procfile` or `app.json` → Heroku, `appspec.yml` → AWS, `app.yaml` with `runtime:` → Google Cloud App Engine
- **CI/CD deployments:** Grep `.github/workflows/*.yml` for `aws-actions/` → AWS, `google-github-actions/` → Google Cloud, `azure/` → Microsoft Azure, `amondnet/vercel-action` or `vercel deploy` → Vercel, `akhileshns/heroku-deploy` or `heroku container` → Heroku
- **Package/SDK signals:** Grep `package.json`, `requirements.txt`, `go.mod` for `@aws-sdk/` or `boto3` → AWS, `@google-cloud/` or `google-cloud-` → Google Cloud, `@azure/` or `azure-` → Microsoft Azure
- **Env templates:** Grep `.env.example`, `.env.sample` for `AWS_ACCESS_KEY_ID` or `AWS_REGION` → AWS, `GOOGLE_CLOUD_PROJECT` or `GCP_PROJECT` → Google Cloud, `AZURE_SUBSCRIPTION_ID` or `AZURE_TENANT_ID` → Microsoft Azure, `VERCEL_TOKEN` → Vercel, `HEROKU_API_KEY` → Heroku
- **Docker/K8s:** Grep for ECR image URLs (`*.dkr.ecr.*.amazonaws.com`) → AWS, GCR URLs (`gcr.io/`) → Google Cloud, ACR URLs (`*.azurecr.io`) → Microsoft Azure

**If providers are detected**, present as confirmation:
> I scanned your codebase and detected the following hosting providers:
>
> - **AWS** (found: provider "aws" in infrastructure/main.tf, @aws-sdk/ in package.json)
> - **Vercel** (found: vercel.json in project root)
>
> Are these correct? Any to add or remove?

**If nothing is detected**, fall back to the manual question:
> Where do you host your applications and data? (select all that apply)
> 1. AWS
> 2. Google Cloud
> 3. Microsoft Azure
> 4. Heroku
> 5. Vercel
> 6. Other (please specify)

**Question 12** (ask after Q11 answered):
> Which compliance framework(s) are you targeting? (select all that apply)
> 1. SOC 2
> 2. ISO 27001
> 3. Both SOC 2 and ISO 27001

**Question 12a** (ask only if SOC 2 was selected in Q12):
> Are you pursuing SOC 2 Type I or Type II?
> 1. Type I (point-in-time)
> 2. Type II (operational over time)

**Question 13** (ask after Q12/Q12a answered):

Before asking this question, run the SaaS auto-detection scan per [references/scanning-patterns/saas-detection.md](references/scanning-patterns/saas-detection.md). This scans `.env.example` files, package managers, Terraform providers, GitHub Actions workflows, and tool-specific config files to detect which SaaS tools are already in use.

**If tools are detected**, present them as a confirmation instead of the manual question:
> I scanned your codebase and detected the following SaaS tools:
>
> **Identity:** Okta (OKTA_DOMAIN in .env.example, @okta/okta-sdk-nodejs in package.json)
> **Monitoring:** Datadog (DD_API_KEY in .env.example, provider "datadog" in main.tf)
> **Security:** Snyk (.snyk config file, snyk/actions in CI)
>
> Are these correct? Any to add or remove?
> (Or type "skip" for no SaaS integrations)

**If nothing is detected**, fall back to the manual question:
> What SaaS tools does your team use? (select all that apply, or skip)
> 1. Identity: Okta, Auth0, Google Workspace, JumpCloud
> 2. Monitoring: Datadog, PagerDuty, New Relic, Splunk
> 3. Project management: Jira, Linear, GitHub Issues
> 4. HR: BambooHR, Gusto, Rippling
> 5. Endpoint: Jamf, Kandji, Intune
> 6. Other (please list)
> 7. Skip — no SaaS integrations

For each category selected (or confirmed), ask which specific tool(s) if not already clear. Save the tool list — it's used in policy generation (Step 5) and workflow generation (Step 7).

**Question 14** (ask after Q13 answered):
> Who will sign off on the final report? (full name, title, and email)

All answers apply to all policies generated in this session. By this point, `.compliance/config.json` should already contain all answers from the per-question updates above.

**Verify config is complete:** After Q14 is answered, read back `.compliance/config.json` and confirm all fields are populated. The complete JSON format is:

```json
{
  "org_name": "Acme Corp",
  "company_description": "Acme automates application-level compliance evidence collection",
  "industry": "B2B SaaS",
  "company_size": "11-50",
  "executives": [
    { "name": "Jane Doe", "title": "CEO" },
    { "name": "John Smith", "title": "CTO" }
  ],
  "work_model": "fully remote",
  "device_types": ["company-provided laptops"],
  "identity_provider": "Microsoft 365",
  "data_types": ["Customer PII"],
  "data_locations": ["North America"],
  "hosting_providers": ["AWS", "Vercel"],
  "frameworks": ["SOC 2", "ISO 27001"],
  "cert_type": "Type II",
  "saas_tools": ["okta", "datadog", "jira"],
  "report_signoff": {
    "name": "Jane Doe",
    "title": "CEO",
    "email": "jane@acme.com"
  },
  "evidence_method": "",
  "cloud_providers": [],
  "cloud_regions": []
}
```

Also create `.compliance/status.md` with empty progress tables (filled in later steps):

```markdown
# Compliance Automation — Progress

## Policies

| Policy | Answers | Policy File | Status |
|--------|---------|-------------|--------|

## SaaS Tool Configuration

| Tool | Script | Config | Tested | Workflow |
|------|--------|--------|--------|----------|

## Workflows Generated

| Workflow | File | Tools |
|----------|------|-------|
```

The "Answers" column links to `.compliance/answers/{policy-id}.md`. The "Policy File" column links to `.compliance/policies/{policy-id}.md` once generated. Status values: `answers-saved`, `generated`, `approved`.

`.compliance/config.json` should already exist from the per-question updates. Verify all fields are populated before proceeding to Step 2.

### Step 2: Choose Evidence Collection Method

**Default: Code + Cloud + SaaS.** After gathering context, tell the user the default and offer to change it:
> I'll scan your codebase, cloud infrastructure, and SaaS tools for evidence. Want to adjust?
> 1. **Code + Cloud + SaaS** — scan all three (default)
> 2. Code + Cloud — skip SaaS tools
> 3. Code + SaaS — skip cloud infrastructure
> 4. Code only — scan codebase for security patterns only
> 5. Q&A only — generate policies based on your answers only

If the user listed no SaaS tools in Q13, default to Code + Cloud instead and hide SaaS options (1, 3).

**If user chooses an option with Cloud:**
First, detect available cloud CLIs and verify authentication per [cloud-shared.md](references/scanning-patterns/cloud-shared.md). Report which providers are available. Ask which region(s) to scan. Then scan both codebase (using per-policy scanning files) and cloud infrastructure (using provider files) for the selected policy.

**If user chooses an option with SaaS:**
For each SaaS tool the user listed in Q13, check the per-category files in `references/saas-integrations/` for the tool-to-policy mapping. Only load the category file relevant to the selected policy. The agent generates the API calls on demand — use the API patterns from the reference file and the agent's knowledge of each tool's API.

**If user chooses Code only (option 4):**
Use the scanning patterns for the selected policy from `references/scanning-patterns/` to detect security implementations and extract concrete values (password lengths, role names, session timeouts, TLS versions, etc.). Each policy has its own scanning file — only load the one you need.

**If user chooses Q&A only (option 5):**
Skip scanning entirely.

**Update config:** Write the chosen evidence collection method to the `evidence_method` field in `.compliance/config.json`. If cloud was chosen, also write `cloud_providers` and `cloud_regions` after detecting/asking.

### Step 3: Select Policy

Show the numbered list of 17 policies and ask which to generate. The same 17 policies apply to both SOC 2 and ISO 27001 — the policy content is the same, only the control mappings in the YAML frontmatter differ. When generating a policy, look up the policy ID in the relevant framework file(s) to get control codes:

- **SOC 2:** [references/frameworks/soc2.md](references/frameworks/soc2.md)
- **ISO 27001:** [references/frameworks/iso27001.md](references/frameworks/iso27001.md)

Include only the control mappings for the framework(s) selected in Q12 (TSC for SOC 2, Annex A for ISO 27001, or both).

> Which policy would you like to generate?
> 1. Governance & Board Oversight
> 2. Organizational Structure
> ... (list all 17)
> 18. **Generate all** — I'll ask policy-specific questions for each, then generate all 17

**If "generate all":** Two-phase approach:
1. **Phase 1 — Collect all answers:** Loop through each policy, ask its policy-specific questions (Step 4), and write each answer file to `.compliance/answers/{policy-id}.md`. After all 17 answer files are written, tell the user:
   > All answers saved to `.compliance/answers/`. You can review and edit any file before I generate. Ready to generate all, or want to review first?
2. **Phase 2 — Generate all policies:** Loop through each answer file and run Steps 5-6. Update `.compliance/status.md` after each policy so progress is saved even if the session ends mid-way. After all are generated, proceed to Step 7.

**If a single policy is selected:** Proceed to Step 4 for that policy.

### Step 4: Ask Policy-Specific Questions

For the selected policy, ask each question from [references/policies.md](references/policies.md) **one at a time**. Wait for each answer before asking the next.

**Write answers to file immediately:** After all policy-specific questions are answered, write them to `.compliance/answers/{policy-id}.md`. Create the `answers/` directory if needed. This file serves two purposes:
1. **Persistence** — answers survive session restarts
2. **Editability** — the user can review and edit answers before generation

Use this format:

```markdown
---
policy: Access Control
policy_id: access-control
answered: 2025-01-15
generated: false
---

# Access Control — Answers

## Company Context (from Step 1)
- Organization: Acme Corp
- Description: Acme automates application-level compliance evidence collection
- Industry: B2B SaaS
- Size: 11-50 employees
- Executives: Jane Doe (CEO), John Smith (CTO)
- Work model: Fully remote
- Devices: Company-provided laptops, company phones
- Identity provider: Microsoft 365
- Data types: Customer PII
- Data locations: North America
- Hosting: AWS, Vercel
- Certification: Type II
- Report signoff: Jane Doe, CEO, jane@acme.com

## Policy-Specific Answers
- Access review frequency: Quarterly
- Provisioning approval: Manager + IT
- MFA scope: All employees
- Deprovisioning timeline: Same business day
- Privileged access review: Monthly
```

**Update `.compliance/status.md` immediately:** Add or update the policy row in the "Policies" table. Set the Answers column to `.compliance/answers/{policy-id}.md`, leave Policy File empty, and set Status to `answers-saved`.

After writing, tell the user:
> Answers saved to `.compliance/answers/{policy-id}.md`.
> You can edit this file before I generate the policy. Ready to generate, or want to review first?

**If the user says "review" or "edit":** Wait for them to confirm they're done editing, then read the file back before generating.

**On session resume:** If `.compliance/answers/{policy-id}.md` exists with `generated: false`, the agent can skip re-asking questions and go straight to generation (after confirming with the user).

### Step 5: Generate the Policy

**Read answers from file:** Before generating, read `.compliance/answers/{policy-id}.md` to get the answers. This ensures any edits the user made are picked up.

Generate the policy document following the template structure in [assets/policy-template.md](assets/policy-template.md).

**If codebase evidence was detected**, include an "Evidence from Codebase" section before the "Proof Required Later" section. **If cloud evidence was detected**, include an "Evidence from Cloud Infrastructure" section as well. **If SaaS evidence was detected**, include an "Evidence from SaaS Tools" section.

**Critical Language Guidelines** - Prioritize under-claiming to minimize audit risk:

| AVOID | PREFER |
|-------|--------|
| "continuous", "real-time", "automated" | "periodic review", "documented process" |
| "ensures", "prevents", "guarantees" | "aims to", "intended to", "process includes" |
| "all users", "always" | "applicable users", "when possible" |
| Specific timeframes without brackets | "[timeframe]" placeholders |

**Exception for codebase-extracted values:** When a concrete value is extracted from the codebase via deep scanning (e.g., password minimum length, session timeout, bcrypt rounds), use that specific value in the policy text with a file:line reference. This is more valuable than a placeholder because it's backed by code evidence. Always include the caveat that values represent code-level configuration and should be verified against production.

**Exception for cloud-extracted values:** When a concrete value is extracted from live cloud infrastructure (e.g., IAM password policy minimum length, RDS backup retention period), use that specific value in the policy text with a CLI command reference. This is more valuable than a placeholder because it reflects actual production configuration. Always include the caveat that values represent a point-in-time snapshot and should be re-verified before audit.

### Step 6: Save and Review

1. Save the policy to `./.compliance/policies/{policy-id}.md`
2. Show a preview of the generated content
3. **Update `.compliance/status.md` immediately:** Add or update the policy row in the "Policies" table. Set the Answers column to the answer file path, the Policy File to the output path, and Status to `generated`. Update the answer file's frontmatter: set `generated: true`.
4. Ask what to do next:
   > Policy saved to `.compliance/policies/{policy-id}.md`. What would you like to do?
   > 1. Generate another policy (go to Step 3)
   > 2. Generate all remaining policies (asks questions for each, then generates)
   > 3. Set up automated evidence collection workflows (Step 7)
   > 4. Regenerate this policy with different answers
   > 5. Done for now

**If option 1:** Go back to Step 3 (policy selection).
**If option 2:** Loop through all policies not yet in `.compliance/status.md`, running Steps 4-5-6 for each. After all are generated, proceed to Step 7.
**If option 3:** Proceed to Step 7.
**If option 4:** Go back to Step 4 for this policy.
**If option 5:** End the session. `.compliance/` has all progress saved.

### Step 7: Generate Evidence Collection Workflows

Ask:
> Would you like to set up automated evidence collection?
> 1. Yes — full setup (code + cloud + SaaS scripts and workflows)
> 2. Yes — code + SaaS only
> 3. Yes — code + cloud only
> 4. Yes — code only (no external credentials needed)
> 5. No — skip for now

Only show options with SaaS/Cloud if they were enabled in Step 2.

**If yes**, proceed with Step 7a then Step 7b.

#### Step 7a: Set Up & Test Evidence Scripts

**Resume check:** Before starting, check existing progress:
1. Read `.compliance/status.md` — check the "SaaS Tool Configuration" and "Cloud Provider Configuration" tables for checkmarks
2. Check for existing `.compliance/scripts/{tool}.sh` files (script already copied/generated)
3. Check for existing `.compliance/scripts/{tool}.config.json` files (config already provided)
4. Check `.compliance/secrets.env` for existing tokens (e.g., `OKTA_API_TOKEN` is already set)

If any tools have partial or complete progress, present a status summary:
> Picking up evidence collection. Here's where we are:
>
> | Tool | Script | Config | Tested | Workflow |
> |------|--------|--------|--------|----------|
> | Okta | [x] | [x] | [x] | [ ] |
> | Datadog | [x] | [x] | [ ] | [ ] |
> | Jira | [ ] | [ ] | [ ] | [ ] |
>
> I'll continue with testing Datadog, then set up Jira.
> Want to skip any tools, or continue with all?

**Skip any tool that already has all checkmarks** (Script + Config + Tested). For partially completed tools, resume from the next incomplete step — don't re-ask for config values that already exist in `{tool}.config.json` or tokens already in `secrets.env`.
For each tool/provider selected, set up an evidence collection script + config pair. Follow [references/script-templates.md](references/script-templates.md) for conventions.

Pre-built scripts for 21 common tools are available in `assets/scripts/`. Use the **copy-first** approach — fall back to generating on demand only when needed.

**For each SaaS tool** (skip steps that are already complete):
1. **If `.compliance/scripts/{tool}.sh` already exists**, skip to step 4. Otherwise: **if pre-built script exists** in `assets/scripts/{tool}.sh`, copy it to `.compliance/scripts/{tool}.sh`. **If no pre-built script**, generate one using API patterns from `references/saas-integrations/{category}.md`.
2. **Update `.compliance/status.md`** — mark `[x] Script` for this tool in the "SaaS Tool Configuration" table.
3. **If `.compliance/scripts/{tool}.config.json` already exists**, skip to step 6. Otherwise: ask the user for non-secret config values (domain, project key, etc.) and write to `.compliance/scripts/{tool}.config.json`.
4. **Update `.compliance/status.md`** — mark `[x] Config` for this tool.
5. **Check `.compliance/secrets.env`** for the required token (e.g., `OKTA_API_TOKEN`). If already present, skip to step 7. Otherwise: ask the user to add the required API token to `.compliance/secrets.env`: `{TOOL}_API_TOKEN=your-token-here`
6. Source secrets and test: `set -a; source .compliance/secrets.env; set +a && bash .compliance/scripts/{tool}.sh`
7. Read the output evidence file and verify it looks correct
8. If there are errors (API changed, missing fields), fix the script and rerun — this is the **generate fallback**
9. Repeat until all evidence rows are populated correctly
10. **Update `.compliance/status.md`** — mark `[x] Tested` for this tool.

Do the same for cloud providers in the "Cloud Provider Configuration" table.

**For cloud providers** (skip steps that are already complete):
1. **If `.compliance/scripts/{provider}.sh` already exists**, skip to step 4. Otherwise: generate using CLI patterns from `references/scanning-patterns/{provider}.md`.
2. **If `.compliance/scripts/{provider}.config.json` already exists**, skip to step 4. Otherwise: write config with region and other settings.
3. **Update `.compliance/status.md`** — mark `[x] Script` and `[x] Config` for this provider in the "Cloud Provider Configuration" table.
4. Verify cloud CLI is authenticated (`aws sts get-caller-identity`, `gcloud auth list`, etc.)
5. Run `bash .compliance/scripts/{provider}.sh` to test
6. Verify and iterate
7. **Update `.compliance/status.md`** — mark `[x] Tested` for this provider.

**For code scanning:**
1. **If `.compliance/scripts/code-scan.sh` already exists and status.md shows tested**, skip entirely.
2. Otherwise: generate `.compliance/scripts/code-scan.sh` using patterns from `references/scanning-patterns/{policy-id}.md`
3. Run `bash .compliance/scripts/code-scan.sh` to test
4. Verify the output contains detected patterns
5. **Update `.compliance/status.md`** — mark code scanning as tested.

Copy `assets/scripts/collect-all.sh` to `.compliance/scripts/collect-all.sh` — the runner that executes all scripts in the directory.

#### Step 7b: Generate Workflows

Once scripts are tested and working, generate GitHub Actions workflows that call them. Use [references/workflow-templates.md](references/workflow-templates.md) for the workflow structure.

Workflows are thin wrappers — they just:
1. Check out the repo
2. Inject secrets as env vars
3. Call `bash .compliance/scripts/{tool}.sh` for each tool
4. Commit evidence files

Generate:
- `.github/workflows/compliance-code-scan.yml` — runs `code-scan.sh` weekly + on PRs
- `.github/workflows/compliance-cloud-scan.yml` — runs `{provider}.sh` weekly/monthly (only if Cloud was chosen)
- `.github/workflows/compliance-saas-scan.yml` — runs `{tool}.sh` weekly (only if SaaS was chosen)

Evidence files are saved to `.compliance/evidence/` with code, cloud, and saas subdirectories.

**If workflows already exist** from a previous policy, update them to include new script calls rather than creating duplicate workflow files.

**Update `.compliance/status.md` after each workflow is generated:** Add or update the workflow's row in the "Workflows Generated" table with the workflow file path, tools included, and creation date. Also mark the `Workflow` column as `[x]` for each tool included in that workflow in the "SaaS Tool Configuration" table.

After generating, output:
1. The list of required GitHub Secrets (per provider)
2. The minimum IAM/RBAC permissions needed (read-only)
3. The scan schedule summary

---

## Codebase Scanning Reference

Scanning patterns are organized per policy in `references/scanning-patterns/`. Load only the file for the policy being generated.

| Policy | Scanning File | SOC 2 TSC | ISO 27001 Annex A |
|--------|--------------|-----------|-------------------|
| Access Control | [access-control.md](references/scanning-patterns/access-control.md) | CC6.1-6.3 | A.5.15-5.18, A.8.2-8.3, A.8.5 |
| Data Management | [data-management.md](references/scanning-patterns/data-management.md) | CC6.5-6.7 | A.5.9-5.13, A.8.10-8.12 |
| Network Security | [network-security.md](references/scanning-patterns/network-security.md) | CC6.6-6.7, CC7.1 | A.8.20-8.22, A.8.24 |
| Change Management | [change-management.md](references/scanning-patterns/change-management.md) | CC8.1 | A.8.9, A.8.25, A.8.32 |
| Vulnerability & Monitoring | [vulnerability-monitoring.md](references/scanning-patterns/vulnerability-monitoring.md) | CC7.1-7.2 | A.5.7, A.8.8, A.8.16 |

| SaaS Tool Detection | [saas-detection.md](references/scanning-patterns/saas-detection.md) | Step 1 Q13 |

Shared guidelines (evidence formatting, value usage, unit conversions): [shared.md](references/scanning-patterns/shared.md)

Policies without a scanning file use basic detection only (Glob for file presence, simple Grep for pattern matching).

## Cloud Scanning Reference

Cloud scanning patterns are organized per provider in `references/scanning-patterns/`. Load only the file for the detected provider(s).

| Provider | Scanning File | Covers |
|----------|--------------|--------|
| AWS | [aws.md](references/scanning-patterns/aws.md) | IAM, S3, RDS, KMS, ELB, EC2, WAF, ECR, SecurityHub, GuardDuty, CloudTrail, Backup |
| GCP | [gcp.md](references/scanning-patterns/gcp.md) | IAM, Cloud SQL, KMS, SSL Policies, Firewall, Cloud Armor, SCC |
| Azure | [azure.md](references/scanning-patterns/azure.md) | Azure AD, RBAC, Storage, SQL, NSG, App Gateway, Defender |

Shared cloud guidelines (detection, auth, safety, evidence format, drift detection): [cloud-shared.md](references/scanning-patterns/cloud-shared.md)

## SaaS Integration Reference

SaaS integration patterns are organized per category in `references/saas-integrations/`. Load only the file for the relevant category.

| Category | File | Tools | Policies Covered |
|----------|------|-------|-----------------|
| Identity & Access | [identity.md](references/saas-integrations/identity.md) | Okta, Auth0, Google Workspace, JumpCloud | Access Control |
| Monitoring & Alerting | [monitoring.md](references/saas-integrations/monitoring.md) | Datadog, PagerDuty, New Relic, Splunk | Vulnerability Monitoring, Incident Response |
| Project & Change Mgmt | [project-management.md](references/saas-integrations/project-management.md) | Jira, Linear, GitHub | Change Management |
| Communications | [communications.md](references/saas-integrations/communications.md) | Slack, Opsgenie, Statuspage | Incident Response, Business Continuity |
| HR & People | [hr.md](references/saas-integrations/hr.md) | BambooHR, Gusto, Rippling | Human Resources |
| Endpoint Management | [endpoint.md](references/saas-integrations/endpoint.md) | Jamf, Kandji, Intune | Mobile & Endpoint |
| Security Scanning | [security.md](references/saas-integrations/security.md) | Snyk, SonarCloud | Vulnerability Monitoring |

Shared guidelines (evidence format, script pattern, secrets, handling unknown tools): [shared.md](references/saas-integrations/shared.md)

The agent generates integrations on demand — for tools not in the catalog, it uses its API knowledge or asks the user for documentation.

## Evidence Scripts Reference

Pre-built scripts for 21 SaaS tools: [assets/scripts/](assets/scripts/) — copy to `.compliance/scripts/`, add config, test.

Script templates, per-tool config convention, collect-all.sh runner, and test-first workflow: [references/script-templates.md](references/script-templates.md)

## Workflow Generation Reference

Workflow templates, schedule mapping, output formats, and secrets setup: [references/workflow-templates.md](references/workflow-templates.md)

Code scan YAML template: [assets/workflow-compliance-code-scan.yml.template](assets/workflow-compliance-code-scan.yml.template)
SaaS scan YAML template: [assets/workflow-compliance-saas-scan.yml.template](assets/workflow-compliance-saas-scan.yml.template)

---

## Output Location

All policies are saved to `./.compliance/policies/` directory with filenames matching the policy ID (e.g., `access-control.md`).

## File Header

Every policy file MUST start with this disclaimer:

```markdown
<!--
GENERATED DRAFT ONLY - USER REVIEW REQUIRED

- Not audit-ready
- Not legally binding
- Not a substitute for professional audits

Review, edit, and own all content.
-->
```

## File Footer

Every policy MUST end with:

```markdown
---
**Policy Safety Note:** This draft deliberately under-claims to reduce risk.
Auditors may require stronger language + evidence of operation.

---
Generated with [Compliance Automation](https://github.com/screenata/compliance-automation)
```

## Evidence Types

Each policy includes a "Proof Required Later" section with evidence items. Categorize each evidence item by type:

| Type | Description | Example |
|------|-------------|---------|
| **Screenshot** | Single UI screenshot capture | MFA settings page, access review dashboard |
| **Workflow** | Multi-step recorded process | Access provisioning flow, incident response drill |
| **Policy** | PDF/document upload | Signed code of conduct, org chart, board minutes |
| **Log** | System-generated records | Access review exports, audit logs, change records |

Format evidence requirements as a table with a Status checkbox column for tracking. Include **sufficiency criteria** (what auditors look for) in the Description:

```markdown
## Proof Required Later

| Status | Evidence | Type | Description |
|--------|----------|------|-------------|
| [ ] | MFA enforcement settings | Screenshot | IdP admin console showing MFA required. Must show: policy enabled, scope = all users, no exceptions |
| [ ] | Access provisioning ticket | Workflow | Recording of approval flow. Must show: request, manager approval, IT provisioning, access granted |
| [ ] | Organizational chart | Policy | Current org chart. Must show: all employees, reporting lines, date updated within audit period |
| [ ] | Access review export | Log | CSV/report from IdP. Must show: reviewer, review date, users reviewed, action taken, 100% coverage |
```

## Important Notes

- **NEVER batch questions** - ask ONE question per message, wait for answer
- Generate ONE policy at a time
- Use the user's actual answers to customize procedures
- Tailor complexity to company size (smaller = simpler controls)
- For healthcare/fintech, include relevant compliance alignment notes
- Always include placeholders like `[timeframe]`, `[owner name]` for values the user should fill in
- When scanning is enabled, extract concrete values and use them in procedures instead of placeholders. Reference with file:line
- When a concrete value is found, bold it in both the evidence table and the policy text
- **Cloud scanning safety**: Only run read-only CLI commands (describe, list, get, show). NEVER run commands that modify infrastructure. Never include secrets, private keys, or credential values in evidence output
- **SaaS scanning safety**: Only call read-only API endpoints (GET requests). Never call endpoints that create, update, or delete data. Redact PII — use counts and percentages instead of user lists. Never include API tokens in evidence output
- When evidence exists from multiple sources (code, cloud, SaaS), compare overlapping controls and flag drift/discrepancies with a cross-source comparison table
