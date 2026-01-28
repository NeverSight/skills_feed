---
name: security-audit
description: Use when conducting security reviews, investigating vulnerabilities, or creating security documentation - provides systematic methodology for code audits with severity assessment, dual documentation patterns (client + internal), and acceptance-focused ticket creation
---

# Security Audit

## Overview

Security audits require systematic investigation, not surface-level checks. This skill provides a methodology for thorough security reviews with proper severity assessment, structured documentation, and security-focused ticket creation.

**Core Principle:** Follow the complete methodology regardless of time pressure. Cutting corners means missing vulnerabilities.

## When to Use

Use when:
- Conducting security reviews or audits
- Investigating reported vulnerabilities
- Creating security documentation
- Writing security-related Jira tickets
- Assessing authentication/authorization flows

Don't use for:
- Feature development
- Performance optimization
- General bug fixes

## Investigation Methodology

### 1. Systematic Code Review

**Follow this checklist regardless of time pressure:**

- [ ] Identify entry point (reported file, authentication flow, etc.)
- [ ] Trace complete flow (frontend → backend → database)
- [ ] Search for pattern repetition across codebase
- [ ] Check related configurations
- [ ] Review dependencies for known vulnerabilities
- [ ] Examine runtime behavior (not just static code)
- [ ] Document all findings with evidence (file paths, line numbers, code snippets)

**Under time pressure:** Ask user to prioritize scope, don't silently cut corners.

### 2. Severity Assessment

| Severity | Criteria |
|----------|----------|
| **CRITICAL** | Authentication bypass, RCE, direct data exposure, affects most sensitive data |
| **HIGH** | Privilege escalation, XSS with token access, weak crypto, data breach potential |
| **MEDIUM** | Information disclosure, CSRF, weak policies, requires multiple steps to exploit |
| **LOW** | Minor leaks, missing hardening, defense-in-depth gaps |

**Consider:**
- **Impact:** What can attacker do?
- **Exploitability:** How easy to exploit?
- **Data Sensitivity:** What data is exposed?

### 3. Documentation Structure

Create TWO documents:

**Client-Facing Report** (`docs/security-report-client.md`):
- What security controls ARE implemented
- Architecture and security measures
- Positive framing
- No vulnerability details

**Internal Findings** (`docs/security-findings-internal.md`):
- All vulnerabilities with severity
- Code evidence and file locations
- Attack scenarios
- Remediation steps
- Prioritized roadmap
- Links to Jira tickets

## Jira Integration

### Epic Creation

**When user requests Jira ticket creation:**

1. **First, get available Jira priorities** from the project:
   - Query Jira to get available priority values
   - Map security severity to Jira priorities based on what's available
   - Common mappings: CRITICAL→Highest, HIGH→High, MEDIUM→Medium, LOW→Low

2. **Create an Epic** that represents the security audit:
   - Title: "Security Report: [Application Name] from [Date]"
   - Description: Link to security report (Confluence or markdown docs)
   - Type: Epic
   - Priority: Based on highest severity finding

3. **Then create individual tickets** as children of this epic:
   - Link each ticket to parent epic
   - All vulnerability tickets grouped under one audit epic
   - **Use Jira's priority field** with values from step 1
   - **Use Jira's acceptance criteria custom field** (`customfield_13523`) when available

**Example:**
```
Epic: PROJ-100 "Security Report: Example Application from 2025-01-15"
├── PROJ-101 (CRITICAL: Sensitive Keys in Version Control)
├── PROJ-102 (CRITICAL: CORS Misconfiguration)
├── PROJ-103 (HIGH: Missing Trusted Host Patterns)
└── PROJ-104 (HIGH: Secrets in Version Control)
```

### Confluence Integration

**If Confluence pages are created:**

1. Create both client and internal pages on Confluence
2. **Add Confluence links to EVERY ticket:**
   - Link to internal findings page (full vulnerability details)
   - Optionally link to client report (security controls overview)

**Ticket format with Confluence:**
```markdown
## Description
[Vulnerability details]

## Link to Security Report
[Internal Security Findings](https://confluence.../internal-findings)
```

## Ticket Creation Rules

**CRITICAL: Security tickets focus on acceptance criteria, NOT implementation.**

### Jira Custom Fields

**Acceptance Criteria Field (`customfield_13523`):**

If available, use Jira's acceptance criteria custom field instead of adding criteria to description. Format as Atlassian Document Format (ADF):

```json
{
  "customfield_13523": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {"type": "text", "text": "- [Criterion 1]"},
          {"type": "hardBreak"},
          {"type": "text", "text": "- [Criterion 2]"},
          {"type": "hardBreak"}
        ]
      }
    ]
  }
}
```

**Each criterion should be:**
- Action-oriented (what must be done/verified)
- Testable (can be checked off as complete)
- Security-focused (what MUST/MUST NOT happen)

### What to Include in Ticket

**If using `customfield_13523` for acceptance criteria:**

```markdown
## Description
[Vulnerability explanation]

## Security Impact
- What can attacker do?
- What data is exposed?
- Attack scenario

## Affected Components
- File paths
- Code evidence (showing vulnerable pattern)

## Link to Security Report
[Internal Security Findings](https://confluence-url)
```

**If NOT using custom field, include in description:**

```markdown
## Description
[Vulnerability explanation]

## Security Impact
- What can attacker do?
- What data is exposed?
- Attack scenario

## Affected Components
- File paths
- Code evidence (showing vulnerable pattern)

## Acceptance Criteria
1. [Security requirement] MUST [not] happen
2. [Authentication tokens] MUST NOT be accessible to JavaScript
3. [Cookies] MUST include httpOnly, secure, and sameSite flags
4. Verification: Security testing confirms [specific requirement]

## Link to Security Report
[Internal Security Findings](https://confluence-url)
```

### What to EXCLUDE

- ❌ Code examples showing how to fix
- ❌ Implementation details
- ❌ Step-by-step fix instructions
- ❌ Specific library/function recommendations

**Exception:** Only include fixes if user explicitly requests "show me how to fix this."

### Questions to Ask BEFORE Creating Tickets

**STOP: Do not create ANY ticket content until these questions are answered:**

- "Should I create Confluence pages for the security reports?"
- "Do you want tickets for all findings or only CRITICAL/HIGH?"
- "Should I include remediation options or just acceptance criteria?"

**Don't ask about epic creation** - always create it when creating tickets.

**No exceptions:**
- Don't create "draft" tickets
- Don't create tickets "for review"
- Don't create tickets "to show what they would look like"
- Ask questions FIRST, create tickets AFTER answers received

## Pattern Investigation

**Don't stop at the reported issue:**

1. Search for same pattern across codebase (grep, ripgrep)
2. Check if pattern exists in:
   - Multiple modules
   - Both frontend and backend
   - Different authentication flows
   - Configuration files
3. Document ALL instances, not just the first one

**Red Flag:** "Already documented" - verify if NEW patterns exist.

## Workflow Summary

```markdown
1. Systematic investigation → findings list
2. Severity assessment → categorize findings
3. Create documentation:
   - Markdown: docs/security-report-client.md
   - Markdown: docs/security-findings-internal.md
   - (Optional) Confluence: client + internal pages
4. If Jira requested:
   a. Create Epic for security audit
   b. Create tickets as children of epic
   c. Add Confluence links to all tickets (if pages exist)
5. Update internal findings doc with ticket links
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Time pressure" → cut corners | Ask to prioritize scope, don't skip steps |
| "Out of scope" → stop investigating | Ask if deeper investigation needed |
| "Already documented" → stop early | Check for new patterns, ask if update needed |
| Include code examples in tickets | Focus on acceptance criteria only |
| Forget to create epic | Always create epic first, then tickets |
| Skip Confluence links in tickets | Add links if Confluence pages exist |
| Ask about epic creation | Don't ask - always create it |

## Rationalizations to Avoid

**If you think ANY of these, STOP:**

- "This is just a quick review, I'll skip X"
- "Out of scope" (without asking)
- "Already documented, no need to investigate further"
- "Being helpful by including code examples"
- "Time pressure means I should prioritize"
- "The user said 'include fixes' so I should add code"
- "I'll skip the epic and just create tickets"
- "I'll add Confluence links later"
- "Let me create a draft ticket to show what it would look like"
- "I'll create the ticket content and ask questions after"

**All of these mean:** Follow the complete methodology. Ask questions if scope unclear.

## Quick Reference

```markdown
1. Systematic investigation (complete checklist)
2. Severity assessment (CRITICAL/HIGH/MEDIUM/LOW)
3. Dual documentation (client + internal)
4. Jira workflow:
   a. Create Epic (always)
   b. Create tickets as children
   c. Add Confluence links (if pages exist)
5. Acceptance-focused tickets (NO code examples)
6. Pattern search (don't stop at first instance)
7. Ask clarifying questions (scope, Confluence, priorities)
```
