---
name: audit-reports
description: Generate formatted security audit findings for Web3 platforms (Sherlock, Code4rena, Cantina). Use when user needs to report vulnerabilities, format findings, or create audit reports for smart contract security contests.
version: 1
---

# Audit Reports

Generate properly formatted security vulnerability reports for major Web3 audit contest platforms. Each platform has specific formatting requirements and judging criteria.

## Supported Platforms

| Platform | Format | Severity Levels |
|----------|--------|-----------------|
| **Sherlock** | GitHub Issues | HIGH, MEDIUM |
| **Code4rena** | Submission Form | High (3), Medium (2), QA (1) |
| **Cantina** | LightChaser | High, Medium, Low, Info |

## Quick Start

When user requests to generate a finding report:

1. Ask which platform (default: Code4rena format)
2. Collect vulnerability details: title, severity, description, affected code, PoC, remediation
3. Generate formatted report using the appropriate platform template
4. Output the complete markdown ready for submission

## Platform Resources

### Sherlock
- `guides/sherlock/` - Official judging guidelines and severity criteria
- `examples/sherlock.md` - Complete finding example
- `platforms/sherlock/template.md` - Report template with invalid issues checklist

### Code4rena
- `guides/code4rena/` - Risk ratings, PoC rules, QA report format
- `examples/code4rena.md` - Complete finding example
- `platforms/code4rena/template.md` - Submission format

### Cantina
- `guides/cantina/` - Severity matrix, duplication rules, PoC requirements
- `examples/cantina.md` - Complete finding example
- `platforms/cantina/template.md` - Detailed submission template

## Severity Quick Reference

### Sherlock
| Severity | Criteria |
|----------|----------|
| **HIGH** | >1% AND >$10 loss, direct without extensive conditions |
| **MEDIUM** | >0.01% AND >$10 loss, with constraints OR breaks core functionality |
| **DOS** | >1 week locked = Medium; + time-sensitive = High |

### Code4rena
| Risk Rating | Criteria |
|-------------|----------|
| **3 - High** | Assets stolen/lost/compromised (directly or via valid attack path) |
| **2 - Medium** | Assets not at direct risk, but protocol function/availability impacted |
| **1 - QA** | No assets at risk; includes Low + Governance/Centralization |

### Cantina
| Severity | Impact | Likelihood |
|----------|--------|------------|
| **High** | Loss of funds / Breaks core functionality | High |
| **Medium** | DOS / Minor fund loss / Breaks non-core | Medium |
| **Low** | No assets at risk | Any |

## Common Invalid Issues (All Platforms)

- Gas optimizations
- Incorrect event values (no broader impact)
- Zero address checks
- User input validation only
- Admin mistakes (common sense)
- Approve/safeApprove front-running (Code4rena: explicitly invalid)
- Weird/non-standard tokens (unless explicitly in scope)
- View function errors (unused within protocol)

## Best Practices

1. **Clear Title** - Concise, describes vulnerability type
2. **Impact First** - Judges need to quickly understand risk
3. **Root Cause** - Explain WHY, not just WHAT
4. **Code References** - Include `file:line` format (e.g., `src/Vault.sol:142`)
5. **Working PoC** - Executable test demonstrating the issue
6. **Clear Remediation** - Specific code-level fix suggestions

## Workflow Checklist

- [ ] Identify target platform
- [ ] Verify severity matches platform guidelines
- [ ] Ensure PoC is executable
- [ ] Include specific code references
- [ ] Provide actionable remediation
- [ ] Review against platform's judging criteria

## Resources

- `examples/` - Complete finding examples for each platform
- `guides/` - Official judging criteria and severity guides
- `platforms/` - Report templates and checklists
