---
name: launch-plan
description: >
  Plan product launches with the right tier and coordinated checklists.
  Use when asked to plan a launch, coordinate a release, prepare for
  go-to-market, or figure out how to announce a new feature or product.
  Covers silent, soft, and big-bang launch tiers.
---

Launch based on the size of the bet, not the size of your ambition. Most features deserve a silent or soft launch. Save the big-bang for genuinely new products or major pivots. Linear's principle: launch early, launch often, launch multiple times.

## Launch Tiers

### Tier 1: Silent Launch
Ship it, turn it on, see what happens. No announcement.

**Use for:** Bug fixes, minor improvements, internal tools, infrastructure changes, experiments.

**Checklist:**
- Feature is behind a flag or gradually rolled out
- Monitoring/alerting is in place
- Rollback plan exists
- One person is on point to watch metrics for 24 hours

### Tier 2: Soft Launch
Ship it, tell existing users, collect feedback before going wide.

**Use for:** New features for existing users, significant UX changes, pricing changes, beta programs.

**Checklist:**
- Changelog entry or in-app notification written
- Help docs updated (or created)
- Support team briefed with FAQ
- Feedback collection mechanism in place (survey, feedback button, Slack channel)
- Known limitations documented
- Rollback plan exists
- 1-2 week feedback period before going wide

Example: Launching real-time collaboration — Changelog: "Edit together, see cursors live." Support FAQ covers latency expectations and max concurrent editors. Roll out to 20% of teams for 3 days via feature flag, then 100%. Rollback: disable WebSocket sync, fall back to polling. Feedback widget live for 2 weeks. Success metric: % of teams with 2+ simultaneous editors.

### Tier 3: Big-Bang Launch
Coordinated, public, designed for maximum reach. Expensive in time and attention.

**Use for:** New product launch, major pivot, rebrand, entering a new market. Maximum 2-3 per year.

**Checklist:**

*Product*
- Feature complete and tested at scale
- Onboarding flow tested with 5+ new users
- Performance benchmarked under expected load

*Content*
- Landing page or product page live
- Blog post / announcement written
- Demo video or screenshots prepared
- Social posts drafted for launch day and day +1, +3, +7

*Distribution*
- Email to existing users scheduled
- Social media posts queued
- Community posts drafted (relevant subreddits, Slack groups, Discord)
- Product Hunt launch prepared (if applicable)
- Influencer/partner outreach done 1 week before

*Support*
- Support team briefed and staffed for launch day
- FAQ and known issues documented
- Escalation path defined

*Measurement*
- Success metrics defined before launch (not after)
- Analytics tracking verified
- Daily review scheduled for first week

## Post-Launch

Regardless of tier:

1. **Day 1:** Watch metrics. Fix anything broken. Respond to all feedback.
2. **Day 3:** First retro — what's working, what's not, what surprised you.
3. **Week 1:** Decide whether to iterate, expand, or pull back.
4. **Week 2-4:** Write up learnings. Update the roadmap based on real data.

## Guidelines

- CRITICAL: Default to Tier 1 or 2. Upgrade to Tier 3 only with strong justification. Over-launching creates announcement fatigue.
- NEVER launch without a rollback plan. If you can't revert, you're not ready.
- ALWAYS define success metrics BEFORE launch, not after. Post-hoc metrics are just storytelling.
- NEVER launch on a Friday. Launch Monday-Wednesday to have the week for monitoring and iteration.
- ALWAYS have one person on point for the first 24 hours. Launches without owners drift.
- NEVER do a big-bang launch for features with known bugs. Soft launch first, fix, then go wide.

---

*Built on Linear's "launch multiple times" philosophy. Skills from [productskills](https://github.com/assimovt/productskills).*
