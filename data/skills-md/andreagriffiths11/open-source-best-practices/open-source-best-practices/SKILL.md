---
name: open-source-best-practices
description: Complete framework for preparing GitHub projects for sustainable open source release. Covers security scanning with Git History Cleaner, legal foundations, governance, contributor onboarding, maintainer expectations, and GitHub Sponsors setup. Use when launching a project publicly, preparing a private repo for open source, or hardening an existing public repo for long-term maintenance.
license: CC-BY-4.0
metadata:
  author: AndreaGriffiths11
  version: "1.0.0"
---

# Open Source Best Practices

Eight phases. Do them in order. Phase 1 isn't optional.

Most of this is about being honest with people upfront. About governance so decisions aren't chaos. About not burning yourself out. About saying no kindly. About building something sustainable.

Start with Phase 1. Always.

---

## The Complete Release Workflow

## Phase 1: Security Foundation

Clean your git history. Today. Before anything else.

Look for API keys, tokens, passwords, database credentials. Check .env files with real values. Look for AWS keys, Firebase secrets, anything internal. Private URLs, internal hostnames, IP addresses. Employee emails, customer data, anything personal. Large binaries and build artifacts.

Use Git History Cleaner to remove secrets and rewrite history so the data is truly gone.

See security-practices.md for the full scanning and cleanup process.

Why first? If secrets are in the repo, nothing else matters. Everything falls apart. Clean history is the foundation. Do this before you tell anyone about the project.

---

### Phase 2: Legal & Ownership (Before Public)

**2.1 License & Rights**

Choose a real open source license and verify ownership of all code/assets:

**Choose a license**:
- **MIT** - Most permissive, highest adoption
- **Apache 2.0** - Permissive + patent protection, good for businesses
- **GPL v3** - Copyleft; derivatives must stay open source

See **[references/license-selection.md](references/license-selection.md)** for decision tree and detailed comparisons.

**Verify ownership**:
- [ ] Do you own all the code in this repo?
- [ ] Are there third-party libraries? Check their licenses are compatible.
- [ ] Did you write all the code, or is some from colleagues/previous work?
- [ ] Do you have permission from your employer to open source this?

**Add the license**:
- Create `LICENSE` file in repo root
- Include full, unmodified license text (GitHub has templates)
- Reference license in README: "MIT License - see [LICENSE](LICENSE)"

**2.2 Ownership & Admin Rights**

Clarify who controls the repo (not tied to one person's account):

- [ ] Repo owner defined (individual, org, or team?)
- [ ] Admin rights assigned to at least 2 people (bus factor)
- [ ] Who can: merge PRs? manage security? publish releases?
- [ ] Documented in GOVERNANCE.md or README

See **[references/governance.md](references/governance.md)** for detailed governance framework.

**2.3 Vision & Scope**

Document what the project does and doesn't do:

Create a **VISION.md** or add to README:
```markdown
## Vision

This project solves [specific problem] for [specific audience].

## What We Do
- Feature A
- Feature B
- Feature C

## What We Don't Do
- Out-of-scope feature X (consider this alternative: Y)
- Platform-specific features (we focus on cross-platform)
- Enterprise features (use open-source alternative Z)

## Decision Framework

We say "no" to features that:
1. Expand scope without clear benefit
2. Add maintenance burden we can't sustain
3. Conflict with the core use case
```

Helps you reject out-of-scope requests kindly. See **[references/governance.md](references/governance.md)**.

---

### Phase 3: Community Foundations (Before Public)

**3.1 Code of Conduct**

Set expectations for community behavior:

- [ ] CODE_OF_CONDUCT.md added (use Contributor Covenant)
- [ ] Contact method for violations is clear
- [ ] Scope defined (online interactions, meetings, events, etc.)
- [ ] Linked in README

See **[references/template-examples.md](references/template-examples.md)** for template and customization tips.

**3.2 Governance & Decision-Making**

Document how the project works:

Add to **GOVERNANCE.md** or README's "Contributing" section:
```markdown
## How Decisions Are Made

- **Small changes** (docs, bug fixes): Maintainers can approve directly
- **Features**: Discussion in issues/RFCs, maintainer vote if disagreement
- **Breaking changes**: RFC required, discussed publicly
- **Governance changes**: All maintainers must agree

## Maintainer Responsibilities

See MAINTAINERS.md for current maintainers, how to become one, and expectations.
```

See **[references/governance.md](references/governance.md)** for full framework.

---

### Phase 4: Documentation & Onboarding

**4.1 README**

Clear, complete introduction:

Must include:
- One-line description of what it does
- Who it's for (users, use cases)
- Status: alpha/beta/stable (realistic)
- Quickstart (copy-paste should work)
- How to get help (issues, discussions, Discord, mailing list)
- Links to: CONTRIBUTING, LICENSE, GOVERNANCE
- Sponsor link if applicable

See **[references/template-examples.md](references/template-examples.md)** for full README template.

**4.2 CONTRIBUTING**

Explain how to contribute:

Must cover:
- How to set up local development (end-to-end, testable by newcomers)
- How to run tests, linting, builds
- Coding style and standards
- Commit message format
- How to propose changes (issues first, then PRs)
- Review expectations (SLAs, who decides)
- What maintainers care about (tests, docs, backwards compatibility)

Tested by someone **new to the project**, not just maintainers.

See **[references/template-examples.md](references/template-examples.md)** for full CONTRIBUTING template.

**4.3 Issue & PR Templates**

Standardize reports and proposals:

GitHub provides UI to add these. Include:

**Issue template** (.github/ISSUE_TEMPLATE/bug_report.md):
```markdown
## Describe the bug
[Clear description]

## Steps to reproduce
1. ...
2. ...

## Expected behavior
[What should happen]

## Actual behavior
[What happened]

## Environment
- OS/version
- Node/Python/etc version
- Project version
```

**PR template** (.github/PULL_REQUEST_TEMPLATE.md):
```markdown
## What does this do?
[Clear description of changes]

## Why?
[Motivation, solves issue #X]

## Testing
- [ ] Added tests
- [ ] Tests pass
- [ ] Docs updated

## Checklist
- [ ] No breaking changes
- [ ] Backwards compatible
- [ ] Ready to merge
```

See **[references/template-examples.md](references/template-examples.md)** for full templates.

**4.4 Labels for Newcomers**

Help people find approachable tasks:

Create GitHub labels:
- `good first issue` - Beginner-friendly, good entry point
- `help wanted` - Team wants external input
- `documentation` - Docs improvements
- `bug` - Something broken
- `enhancement` - New feature request
- `question` - User asking for help

Use `/contribute` endpoint on GitHub to highlight good first issues.

**4.5 Docs-as-Code**

Keep documentation versioned and reviewed:

- [ ] Docs live in repo (not external wiki)
- [ ] Docs go through PR review
- [ ] Docs tied to releases (not always "latest")
- [ ] Automation: link checkers, spell check
- [ ] Regular docs audits to prevent rot

---

### Phase 5: Setup Files & Basic Infrastructure

**5.1 Setup Instructions**

Verified by someone new (not just maintainers):

```markdown
## Development Setup

### Prerequisites
- Node 18+ (or Python 3.10+, etc.)
- [Tool X] for [what it does]

### First Time Setup

1. Clone and install:
   git clone ...
   cd project
   npm install

2. Run tests to verify setup works:
   npm test

3. Run the project:
   npm start

4. Make a change:
   - Edit src/index.js
   - Run npm test
   - See your change work

### Common Issues
- [Problem X]: [Solution]
```

**5.2 CI/CD Setup**

Enforce quality on every PR:

- [ ] Tests run on PR (GitHub Actions, Travis, etc.)
- [ ] Linting enforced
- [ ] Required checks prevent merge if failing
- [ ] Coverage tracked (if applicable)

**5.3 .gitignore**

Prevent accidental commits:

```
# Dependencies
node_modules/
__pycache__/
vendor/

# Environment
.env
.env.local

# Build
build/
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

Use [gitignore.io](https://gitignore.io) for templates.

---

### Phase 6: Maintainer Expectations & Communication

**6.1 Define Maintainer Roles**

Document who does what:

Create **MAINTAINERS.md**:
```markdown
## Current Maintainers
- [Name] - Project lead, final decisions
- [Name] - Core contributor, PR reviews
- [Name] - Community liaison, issue triage

## Responsibilities
1. Triage issues and PRs
2. Review code quality
3. Maintain backwards compatibility
4. Shepherd breaking changes
5. Respond to community within SLA
6. Publish releases

## How to Become a Maintainer
- Be active for 3+ months
- Demonstrate good judgment
- Asked by current maintainers
```

See **[references/maintainer-expectations.md](references/maintainer-expectations.md)** for full framework.

**6.2 Set Response SLAs**

Be realistic about availability:

```markdown
## Support SLAs

- **Issues**: We aim to respond within 1 week
- **Security reports**: Within 48 hours (email security@example.com)
- **PRs from maintainers**: Within 3 days
- **PRs from community**: Within 1-2 weeks

## Release Cadence
- Bug fixes: ASAP (as needed)
- Minor releases: Monthly if changes exist
- Major releases: 2-4x per year (as needed)

We're all volunteers. Responses may be slower during high-activity periods.
```

See **[references/maintainer-expectations.md](references/maintainer-expectations.md)**.

**6.3 Public Communication**

Prefer open discussion:

- [ ] Issues and discussions are public by default
- [ ] Key decisions documented in issues (not Slack/Discord)
- [ ] Major changes discussed publicly before implementation
- [ ] When rejecting ideas, explain kindly and document in issues

See **[references/maintainer-expectations.md](references/maintainer-expectations.md)** for "How to Say No" framework.

**6.4 Roadmap & Visibility**

Help newcomers see direction:

Create **ROADMAP.md** or GitHub Project:
```markdown
## What We're Working On

### Short Term (Next 1-2 releases)
- [ ] Feature A
- [ ] Bug fix B

### Medium Term (3-6 months)
- [ ] Performance improvement
- [ ] New platform support

### Long Term (Vision)
- We want to eventually support X

## How to Propose Ideas
- Open an issue to discuss
- We prioritize based on community need and maintainer capacity
```

---

### Phase 7: Security & Vulnerability Reporting

**7.1 Security Policy**

How to report vulnerabilities safely:

Create **SECURITY.md**:
```markdown
## Reporting a Vulnerability

Do NOT open a public issue.

Email: security@example.com with:
- Description of vulnerability
- Steps to reproduce
- Impact assessment

## What to Expect
- Acknowledgment within 48 hours
- Private fix before public disclosure
- Credit in security advisory (unless you decline)

## Supported Versions
- 2.x: Full support
- 1.x: Security fixes only
- 0.x: No longer supported
```

See **[references/template-examples.md](references/template-examples.md)** for full template.

**7.2 Security Posture**

Document your approach:

- [ ] Vulnerability reporting process clear
- [ ] Response process defined (who handles, timeline)
- [ ] Dependency updates tracked (Dependabot, etc.)
- [ ] Security policy linked in README

See **[references/security-practices.md](references/security-practices.md)**.

---

### Phase 8: Funding & Sustainability (Optional but Recommended)

**8.1 GitHub Sponsors Setup**

Enable funding if you plan to accept support:

- [ ] Sponsors profile enabled
- [ ] Bio, project description, goals clear
- [ ] 2-4 sponsorship tiers defined with concrete benefits
- [ ] Sponsor link in README and repo sidebar
- [ ] Plan for sponsor communication

See **[references/sponsors-setup.md](references/sponsors-setup.md)** for detailed guidance.

**Example tiers**:
```
$5/month: Supporter
- Name in README
- Credit in release notes

$25/month: Contributor
- ↑ + Priority issue triage
- ↑ + Early access to roadmap discussions

$100/month: Sponsor
- ↑ + Monthly office hours (30 min)
- ↑ + Custom feature consultation
```

**8.2 Transparency on Funding**

Be clear about what sponsorship enables:

```markdown
## Sponsorship

This project is maintained by volunteers. Sponsorship helps:
- Pay for infrastructure costs ($X/month)
- Fund one day/week of maintenance time
- Support long-term security updates

Sponsors are credited in:
- README Sponsors section
- Release notes
- Annual thank-you blog post

See [SPONSORS.md](SPONSORS.md) for tier details and how your support is used.
```

See **[references/sponsors-setup.md](references/sponsors-setup.md)**.

---

## Complete Pre-Open-Sourcing Checklist

Use this before making your repo public:

**Legal & Security**:
- [ ] License chosen and LICENSE file committed (unmodified text)
- [ ] Verified: you own or have rights to all code/assets
- [ ] Git history scanned for secrets (use Git History Cleaner)
- [ ] All secrets, PII, sensitive data removed from history
- [ ] Copyright/ownership clarified in docs

**Governance & Vision**:
- [ ] VISION.md or scope section in README defining what's in/out of scope
- [ ] GOVERNANCE.md documenting decision-making process
- [ ] MAINTAINERS.md documenting maintainer roles and responsibilities
- [ ] CODE_OF_CONDUCT.md added and linked
- [ ] Admin rights clarified (at least 2 people have write access)

**Documentation**:
- [ ] README with: value prop, quickstart, status, help channels, links
- [ ] CONTRIBUTING.md with setup, tests, coding style, PR process
- [ ] Setup instructions verified by someone new to the project
- [ ] Issue and PR templates added (.github folder)
- [ ] Labels created (good first issue, help wanted, etc.)

**Infrastructure**:
- [ ] CI/CD set up (tests, linting, required checks on PRs)
- [ ] .gitignore configured for your tech stack
- [ ] Default branch protected (require PR reviews, pass checks)

**Community & Maintenance**:
- [ ] Response SLAs documented (e.g., "1 week for issues")
- [ ] Release cadence defined (e.g., "monthly if changes exist")
- [ ] Roadmap or backlog visible (GitHub Project or ROADMAP.md)
- [ ] Security.md documenting vulnerability reporting
- [ ] Public communication preference clear (issues/discussions, not DMs)

**Funding (If Applicable)**:
- [ ] GitHub Sponsors profile set up (if accepting donations)
- [ ] Sponsorship tiers defined with concrete benefits
- [ ] Sponsor link in README and repo sidebar
- [ ] Plan for communicating with sponsors

**Final Checks**:
- [ ] README proofread and links tested
- [ ] CONTRIBUTING steps actually work
- [ ] All documents linked and discoverable
- [ ] Ready to respond to issues/PRs (even if "best effort")
- [ ] Team/colleagues aware it's going public

---

## When to Reference Each Guide

- **"Help me understand what files I need"** → [references/file-checklist.md](references/file-checklist.md)
- **"How do I choose a license?"** → [references/license-selection.md](references/license-selection.md)
- **"How do I clean my git history?"** → [references/security-practices.md](references/security-practices.md)
- **"How do I set up governance?"** → [references/governance.md](references/governance.md)
- **"What are maintainer expectations?"** → [references/maintainer-expectations.md](references/maintainer-expectations.md)
- **"How do I set up GitHub Sponsors?"** → [references/sponsors-setup.md](references/sponsors-setup.md)
- **"I need template text"** → [references/template-examples.md](references/template-examples.md)

---

## By Project Type

### For Libraries (npm, PyPI, crates, gems)
- Emphasize API reference and usage examples in README
- Include installation command prominently
- Show dependency count and compatibility matrix
- Link to full API docs if extensive
- Consider: version compatibility guarantees

### For CLI Tools
- Show real command examples in README
- Document all major flags/options
- Include example output
- Explain use cases clearly
- Consider: shell completion, plugin system

### For Frameworks
- Emphasize getting-started guide
- Show 2-3 real code examples (not toy examples)
- Explain design philosophy
- Link to full documentation
- Consider: ecosystem and plugin guidelines

### For Server/Infrastructure
- Document system requirements clearly
- Include Docker setup if applicable
- Explain security implications
- Show typical deployment workflow
- Consider: monitoring, logging, observability

### For Developer Tools
- Show before/after or problem/solution
- Document configuration clearly
- Include troubleshooting section
- Link to video tutorials if available
- Consider: plugin/extension system

---

## Success Indicators

Your open source project is healthy when:

✅ New users can set up locally in <30 minutes  
✅ Contributors understand how to submit PRs without asking  
✅ Issues get responses within your stated SLA  
✅ Roadmap is visible and community input is welcome  
✅ Security issues are reported privately  
✅ Rejections are kind and documented  
✅ Decision-making is transparent  
✅ Governance is clear (not tied to one person)  
✅ You can sustain maintenance (via time or funding)  
✅ Community feels welcome and heard
