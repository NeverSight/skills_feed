---
name: security-privacy
description: Pre-flight security & privacy checklist for changes touching identity, data, logging, or external integrations; ensures secrets/PII hygiene and boundary-safe design.
---

# Security & Privacy (Pre-flight)

## Use when
- Adding/reading/writing user/workspace data.
- Touching identity/auth, permissions, Firebase rules, or external APIs.
- Adding logging, analytics, telemetry, or error reporting.

## Workflow
1. Identify data: what fields are PII, where stored, retention expectations.
2. Identify trust boundaries: browser ↔ Firebase/backend; who can call what.
3. Minimize & redact: remove unnecessary fields; ensure logs/errors redact secrets/PII.
4. Validate inputs at the edge; keep Domain pure.
5. Confirm least privilege: tokens, rules, and access paths.

## Output checklist
- No secrets in repo, fixtures, or logs.
- No PII in logs/errors/templates.
- Clear authorization point (not scattered across UI).
- Deletion path does not leave access holes.

## References
- `.github/instructions/65-security-privacy-copilot-instructions.md`

