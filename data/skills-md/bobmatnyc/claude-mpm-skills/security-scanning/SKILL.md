---
name: security-scanning
description: "CI security scanning: secrets, deps, SAST, triage, expiring exceptions"
license: MIT
compatibility: claude-code
metadata:
  version: 1.1.0
  category: universal
  author: Claude MPM Team
progressive_disclosure:
  entry_point:
    summary: "Baseline CI scans (secrets, deps, SAST) with triage and expiring exceptions"
tags: [security, scanning]
---

# Security Scanning

## Quick Start

- Secrets: fail fast; rotate on exposure.
- Dependencies: gate critical/high; automate updates.
- SAST: start high-signal; ratchet over time.
- Exceptions: require reason, owner, and expiry.

## Load Next (References)

- `references/tooling-matrix.md`
- `references/ci-workflows.md`
- `references/triage-and-remediation.md`
- `references/common-findings-and-fixes.md`
- `references/supply-chain-and-sbom.md`
