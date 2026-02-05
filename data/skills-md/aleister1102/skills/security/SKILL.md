---
name: security
description: Use when the user requests a security audit workflow (vulnerability scan and verification) for sensitive code.
---

# /security - Security Audit Workflow

Use this skill to run a security audit workflow on sensitive code, prioritizing findings that can realistically become CRITICAL or HIGH impact.

## When to Use

- The user asks for a security audit / vulnerability review ("is this secure?", "check for vulns").
- The code touches authn/authz, payments, secrets, PII, file upload/download, webhooks, admin actions, deserialization, or command execution.
- The user wants a scan + verification loop (audit findings → fixes → re-check).

## When NOT to Use

- The user wants a general code review, debugging, refactor, or style improvements.
- The code is clearly non-sensitive (toy scripts, local-only utilities) and the user isn’t asking about security.

## Defaults / Guardrails

- Report **CRITICAL/HIGH only**. If none exist, explicitly report **none**.
- Treat "possession implies compromise" as non-finding unless you show a feasible token/secret acquisition path.
- Prefer exploit-chain depth over breadth. Drop noise that can’t reach material impact.

For deeper triage/prerequisite rules and consistent output formats, read:
- `references/triage-and-prereqs.md`
- `references/report-templates.md`

## Workflow

### 0) Confirm Scope

Determine one of:
- **Full codebase**: `/security`
- **Area**: `/security auth` (or similar)
- **Single file**: `/security path/to/file`
- **Dependencies only**: `/security --deps`

### 1) Static Audit (Phase 1)

Goal: find and explain only CRITICAL/HIGH issues with clear attacker prerequisites.

Prioritize:
- Injection: SQL/NoSQL, command/OS, template injection, SSRF, XSS.
- Authz failures: IDOR, missing checks, privilege escalation.
- Authn/session: token validation mistakes that increase attacker capability.
- Secrets: hardcoded credentials, leaked tokens/keys, unsafe secret handling.
- Insecure deserialization, unsafe file handling (path traversal), dangerous eval.
- Supply chain: obviously vulnerable deps or unsafe install/build hooks.

Evidence required per finding:
- Attacker-controlled **source** → security-sensitive **sink** (show the path).
- Concrete exploit narrative and prerequisites.
- Containment + long-term remediation steps.

### 2) Runtime Verification (When Runnable)

If there is a runnable target, verify with minimal, safe steps.

Rules:
- Only test instances you control / are authorized to test (prefer `localhost`).
- Avoid DoS-like loops, mass writes, or destructive behavior.
- Prefer repo-native commands (README, Makefile, Docker, package scripts).

Verification checklist:
- Find how to run: README, Dockerfile, docker-compose, Makefile, package scripts.
- Start the service in minimal config.
- Prove impact with 1–3 deterministic requests/steps.

### 3) Fix Guidance

Recommend changes that eliminate the root cause:
- Parameterize queries; avoid shell; escape/encode; strong allowlists for URLs/paths.
- Enforce deny-by-default authorization.
- Remove secrets from repo; use env/secret store; rotate compromised keys.

### 4) Re-Verify (Phase 2)

After fixes, re-run minimal repros and any relevant security checks.

## Triage Rules (Noise to Skip Unless Chained)

Skip by default unless you can chain to data loss/auth bypass/priv-esc with evidence:
- CORS/OPTIONS “bypass” without protected response body or state change.
- Missing rate limiting/lockout by itself.
- Account enumeration without a takeover/privileged action path.
- Timing side-channels without a feasible remote measurement model.
- Swagger/UI exposure gated to non-prod.
- Token-type confusion unless it **meaningfully increases capability** beyond intended flows.

If a borderline issue is showing up repeatedly, apply the stricter escalation criteria in `references/triage-and-prereqs.md`.

## Subagent Prompts

### Phase 1: `aegis` (Audit)

```text
Security audit: [SCOPE]

Find CRITICAL/HIGH only. For each finding include:
- severity (CRITICAL/HIGH)
- attacker prerequisites
- source → sink evidence (file/function references)
- minimal repro steps (safe)
- remediation (containment first, then long-term)

If no CRITICAL/HIGH exist, explicitly output: NONE.

Deprioritize noise categories unless chained to material impact.
```

### Phase 2: `arbiter` (Verify)

```text
Verify security fixes: [SCOPE]

- Re-run minimal repro steps for each previously reported CRITICAL/HIGH
- Run the repo’s test/build checks relevant to the changed area
- Run dependency audit appropriate to stack (e.g., npm/pip/go)

Output: verification report (fixed/not fixed) and any regressions.
```

## Flags

- `--deps`: dependencies-only audit
- `--verify`: post-fix verification run
- `--secrets`: prioritize secret detection and leakage paths
