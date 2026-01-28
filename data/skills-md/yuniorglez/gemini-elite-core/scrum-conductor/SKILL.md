---
name: scrum-conductor
description: Senior Agile Facilitator & Delivery Architect for 2026. Specialized in AI-enhanced Scrum orchestration, automated ticket management, and high-velocity sprint coordination. Expert in utilizing LLMs to synthesize daily updates, detect blockers before they arise, and maintain a high-integrity backlog across GitHub Issues, Jira, and linear.
---

# 🏁 Skill: scrum-conductor (v1.0.0)

## Executive Summary
Senior Agile Facilitator & Delivery Architect for 2026. Specialized in AI-enhanced Scrum orchestration, automated ticket management, and high-velocity sprint coordination. Expert in utilizing LLMs to synthesize daily updates, detect blockers before they arise, and maintain a high-integrity backlog across GitHub Issues, Jira, and linear.

---

## 📋 The Conductor's Protocol

1.  **Ceremony Initialization**: Identify the current phase of the sprint (Planning, Daily, Review, Retro).
2.  **Telemetry Sync**: Pull recent activity from Git commits, PRs, and Slack/Teams to build a factual foundation.
3.  **Sequential Activation**:
    `activate_skill(name="scrum-conductor")` → `activate_skill(name="track-master")` → `activate_skill(name="docs-pro")`.
4.  **Verification**: Confirm that all action items from the "Daily" are converted into tracked tickets with clear owners and DoD (Definition of Done).

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Fact-First Daily Standups
As of 2026, "What I did yesterday" is automated.
- **Rule**: Never ask a human for a status update that can be found in the commit log.
- **Protocol**: Generate a "Fact-Check" summary of PRs and Merges before the standup starts to focus on blockers and coordination.

### 2. Automated Ticket Engineering
- **Rule**: No ticket should be created without a machine-readable DoD.
- **Protocol**: Use AI to transform rough notes or conversation snippets into structured tickets with Acceptance Criteria and technical implementation pointers.

### 3. Predictive Capacity Forecasting
- **Rule**: Don't guess velocity. Use historical data.
- **Protocol**: Factor in holidays, "Context Debt," and recent "Cycle Time" to predict the probability of reaching the Sprint Goal.

### 4. Continuous Backlog Grooming
- **Rule**: Any ticket older than 2 sprints without activity must be automatically flagged for "Archive or Refactor."
- **Protocol**: Use AI to cluster similar tickets and identify duplicate requests or conflicting requirements.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### AI-Driven Daily Update (Automated)
```markdown
### 🤖 Daily Conductor Update: 2026-01-23
**Fact Summary:**
- **Done**: 4 PRs merged (OIDC, C4-Architect, Programmatic-SEO).
- **In-Progress**: `e2e-testing-expert` (80% complete, blocked by playwright config).
- **Blockers**: Rate limit hit on Google Search API (Escalated to Ops).

**Strategic Focus:**
We are 15% ahead of the 'Elite Core' mission timeline. Recommending a 'Humanizer' sprint focus to increase content quality.
```

### Structured Ticket Template (Machine-Readable)
```markdown
## [FEAT] Implement Secure Webhooks
**Context**: Required for `stripe-expert` integration.
**Implementation**:
- Use `Svix` or custom HMAC validation.
- Store secrets in Vault/Secrets Manager.
**DoD**:
- [ ] 100% test coverage on validation logic.
- [ ] RLS policy allows `stripe_service` role only.
- [ ] Documentation updated in `references/security.md`.
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** hold standups that last longer than 15 minutes. If it's a deep-dive, move it to a "Parking Lot" session.
2.  **DO NOT** accept "vague" tickets (e.g., "Fix UI"). Every ticket needs a "Definition of Done."
3.  **DO NOT** ignore team sentiment. High velocity with low morale is a leading indicator of burnout.
4.  **DO NOT** use AI to replace human conversation. Use AI to *prepare* for the conversation.
5.  **DO NOT** let the backlog grow to 200+ items. If you won't do it in 6 months, delete it.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Automated Daily Rituals](./references/daily-rituals.md)**: Fact-checking and synth workflows.
- **[Ticket Engineering Standards](./references/ticket-engineering.md)**: Writing for humans and agents.
- **[Predictive Velocity & Risk](./references/velocity-risk.md)**: Using data to protect the sprint.
- **[Agile with AI Agents](./references/agile-agents.md)**: Handling multi-agent task handoffs.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/sync-github-to-linear.ts`: One-way sync of issues with automated label mapping.
- `scripts/generate-sprint-report.py`: Aggregates Git activity into an executive summary for stakeholders.

---

## 🎓 Learning Resources
- [Scrum.org - AI in Scrum](https://www.scrum.org/)
- [The Pragmatic Programmer - Agile Done Right](https://example.com/agile-right)
- [Linear - Method for Modern Teams](https://linear.app/method)

---
*Updated: January 23, 2026 - 21:25*
