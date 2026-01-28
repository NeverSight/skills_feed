---
name: oss-product-manager
description: Navigate open source product strategy, community dynamics, and sustainable maintenance. Use when planning OSS releases, managing contributors, handling community expectations, balancing commercial and community interests, or when the user needs battle-tested wisdom on building in the open.
---

# Open Source Product Manager

Building in public is different. The community is your team, your users, and your critics—often simultaneously.

## When to Use

- Planning an OSS release or roadmap
- Deciding how to handle a feature request or PR
- Managing community expectations
- Choosing governance or funding models
- Writing contributor guidelines
- Handling burnout or sustainability concerns

## Output Contract

For OSS decisions, structure your analysis as:

```markdown
## Decision: [The Question]

### Context
- Project stage: [Early / Growth / Mature]
- Community size: [Rough estimate]
- Current challenge: [1 sentence]

### Recommendation
[1-2 sentences: what to do]

### Trade-offs
| Option | Pros | Cons |
|--------|------|------|
| ... | ... | ... |

### Action Items
- [ ] [Specific next step]
- [ ] [Another step]

### What to Communicate
[How to explain this to the community]
```

For contributor/PR decisions:

```markdown
## PR/Issue: [Title or link]

### Verdict
[Merge / Request changes / Close with explanation / Needs discussion]

### Reasoning
- [Factor 1]
- [Factor 2]

### Response Template
[Draft message to contributor]
```

## Fundamental Truths

### Open Source Is Not Free
- Free as in speech, not as in beer
- Maintenance costs are real and ongoing
- Community management is work
- Documentation is work
- Saying no is work

### The Maintainer's Burden
- You owe the community nothing
- But if you want the project to thrive, you owe it everything
- Sustainable pace beats heroic sprints
- Your time is the scarcest resource

### Community Is Everything
- Code can be forked; community cannot
- Trust takes years to build, moments to destroy
- The best contributors become maintainers
- The best maintainers build more maintainers

## Project Lifecycle

### Early Stage (0→1)
- Scratch your own itch first
- Document why, not just how
- Make it easy to contribute from day one
- Your first contributor is more valuable than your first 1000 stars

**Focus:**
- Core functionality that works
- Clear README and getting started guide
- Contributing guidelines
- License (choose early, change is painful)

### Growth Stage (1→100)
- Establish governance before you need it
- Define scope—what you won't do matters
- Build a contributor ladder
- Automate everything that can be automated

**Focus:**
- CI/CD pipeline
- Issue and PR templates
- Code of conduct
- Release process
- Triaging workflow

### Mature Stage (100→∞)
- Succession planning
- Sustainable funding model
- Clear decision-making process
- Balance stability with evolution

**Focus:**
- Long-term support policy
- Breaking change process
- Security response plan
- Mentorship of new maintainers

## Roadmap and Planning

### Public Roadmaps
- Show direction, not deadlines
- Use milestones, not dates
- "Next" / "Later" / "Exploring" beats Q1/Q2/Q3
- Update regularly or remove entirely

### Saying No
The most important skill. Ways to say no:
- "Out of scope for this project"
- "Great idea—would you like to build it as a plugin?"
- "We're not prioritizing this, but PRs welcome"
- "This conflicts with our design principles"
- Silence (sometimes appropriate for obvious trolls)

### Scope Management
- Narrow scope = maintainable project
- Every feature is a maintenance commitment
- "Do one thing well" is sustainable
- "Kitchen sink" projects burn out maintainers

### Version Strategy

**Semantic Versioning:**
- MAJOR: Breaking changes
- MINOR: New features, backwards compatible
- PATCH: Bug fixes

**Communication:**
- CHANGELOG is sacred
- Breaking changes need migration guides
- Deprecation before removal
- LTS versions for enterprise adoption

## Community Management

### Contributor Pipeline
```
User → Reporter → Contributor → Reviewer → Maintainer
```

**At each stage, make the next step obvious:**
- "Good first issue" labels
- Contributing guide
- Mentorship for promising contributors
- Clear path to commit access

### Communication Channels

| Channel | Use for |
|---------|---------|
| GitHub Issues | Bug reports, feature requests |
| GitHub Discussions | Questions, ideas, show & tell |
| Discord/Slack | Real-time help, community building |
| Twitter/Mastodon | Announcements, celebrations |
| Blog | Deep dives, release notes, roadmap |

**Pick few, maintain well.** Dead channels are worse than no channels.

### Issue Management

**Triage immediately:**
- Label appropriately
- Ask clarifying questions
- Close duplicates with links
- Close won't-fix with explanation

**Issue labels that work:**
- `bug` / `enhancement` / `question`
- `good first issue` / `help wanted`
- `needs-reproduction` / `needs-info`
- `breaking-change` / `security`
- `wontfix` / `duplicate`

**The 90-day rule:** Issues without activity for 90 days should be closed or revived. Stale issues demoralize everyone.

### PR Management

**Review promptly:**
- First response within 48 hours
- Silence kills contributor enthusiasm
- "Thanks for this! I'll review properly this weekend" is fine

**Review kindly:**
- Praise what's good
- Explain why, not just what
- Offer to pair on complex changes
- Remember: this person volunteered their time

**Merge or close:**
- Don't let PRs languish
- Close with clear explanation if not merging
- "Not now" is better than silence

### Difficult Situations

**Entitled users:**
- Don't engage emotionally
- Point to contribution guidelines
- Block if necessary—your mental health matters

**Bike-shedding:**
- Make a decision and move on
- "Maintainer's prerogative" is valid
- Not everything needs consensus

**Feature creep:**
- "That's a great idea for a plugin"
- "PRs welcome, but not prioritized by maintainers"
- Hold the line on scope

**Burnout:**
- Take breaks publicly—it normalizes it
- Ask for help before you need it
- It's okay to step back
- Archive is better than abandoned

## Documentation

### Documentation Is Product
- README is your landing page
- Docs are your onboarding
- Examples are your marketing
- Bad docs = no users (good)
- Bad docs = frustrated users (worse)

### Documentation Hierarchy
1. **README** — What is this? Why should I care? How do I start?
2. **Getting Started** — Zero to working in 5 minutes
3. **Guides** — Common tasks, explained
4. **API Reference** — Complete, accurate, boring
5. **Examples** — Copy-paste solutions
6. **Contributing** — How to help

### README Essentials
1. Project name and one-line description
2. Status badges (build, version, license)
3. Installation (copy-paste command)
4. Quick start example
5. Links to docs, examples, community
6. License and contribution note

### Documentation Maintenance
- Docs are never done
- Link docs to code (so they update together)
- Every breaking change needs doc updates
- Examples must be tested

## Release Management

### Release Process
1. Changelog is complete
2. Version bump
3. Tests pass
4. Build artifacts
5. Tag release
6. Publish to registries
7. Announce

Automate all of this. Humans make mistakes.

### Release Communication
- Changelog for the detail-oriented
- Blog post for the big picture
- Tweet for the drive-by
- Migration guide for breaking changes

### Backwards Compatibility
- Breaking changes are expensive for users
- Bundle breaking changes into major versions
- Deprecate before removing
- Provide codemods when possible

## Governance

### Governance Models

**BDFL (Benevolent Dictator For Life):**
- One person makes final decisions
- Fast, clear, but bus factor of 1
- Common in early projects

**Core Team:**
- Small group with commit access
- Consensus or voting
- More sustainable, slower decisions

**Foundation:**
- Formal structure, bylaws, membership
- For very large projects
- Overhead can be significant

### Decision Making
- Small decisions: Just do it
- Medium decisions: Discuss in issue, maintainer decides
- Large decisions: RFC process
- Reversible decisions: Bias to action
- Irreversible decisions: Take your time

### RFC Process
1. Problem statement
2. Proposed solution
3. Alternatives considered
4. Open questions
5. Community feedback period
6. Decision and rationale

## Sustainability

### Funding Models

**Sponsorship:**
- GitHub Sponsors, Open Collective, Patreon
- Works for individuals, scales poorly
- Builds community connection

**Dual licensing:**
- Open source + commercial license
- Works for specific use cases
- Can create community tension

**Open core:**
- Core is open, extras are paid
- Clear value differentiation needed
- Common and sustainable if balanced

**Foundation support:**
- Grants from Linux Foundation, Apache, etc.
- Requires maturity and adoption
- Comes with governance requirements

**Corporate backing:**
- Company employs maintainers
- Fast and well-resourced
- Risk if company priorities change

### Avoiding Burnout
- Set boundaries publicly
- "I maintain this in my spare time"
- Disable notifications on weekends
- Recruit co-maintainers early
- It's okay to say "not this week"

### Bus Factor
- More than one person should be able to release
- Document everything
- Share credentials securely
- Plan for your own disappearance

## Legal and Licensing

### License Selection

**Permissive (MIT, Apache, BSD):**
- Maximum adoption
- Can be used in proprietary software
- No copyleft obligations

**Copyleft (GPL, AGPL):**
- Changes must be shared
- Protects from proprietary forks
- Reduces corporate adoption

**Middle ground (MPL, LGPL):**
- File-level copyleft
- Can be linked from proprietary software

Choose based on your goals, not your feelings.

### CLA and DCO
- **CLA** (Contributor License Agreement): Legal protection, friction for contributors
- **DCO** (Developer Certificate of Origin): Lighter weight, sign-off in commit

### Trademark
- Protect your project name
- Define acceptable use
- Prevents confusion and abuse

## Metrics That Matter

### Health Indicators
- Time to first response on issues
- PR merge time
- Contributor retention
- Bus factor
- Release frequency

### Vanity Metrics (Use Carefully)
- GitHub stars (awareness, not usage)
- Download counts (bots, CI, duplicates)
- Twitter followers (reach, not engagement)

### Real Usage Signals
- Issues from real users with real problems
- PRs that improve the project
- Stackoverflow questions
- Blog posts and tutorials by others
- Companies using in production

## Hard-Won Lessons

### On Contributors
- Most contributors contribute once—make it count
- Regular contributors are gold—invest in them
- Not everyone who opens a PR will finish it
- "PRs welcome" is not a strategy

### On Growth
- Stars don't matter; users do
- Users don't matter; contributors do
- Contributors don't matter; maintainers do
- Slow growth is fine; no growth is also fine

### On Communication
- Over-communicate your availability
- Silence is interpreted as abandonment
- "I'm busy but I see this" goes a long way
- Automate responses if you can't respond personally

### On Yourself
- Your side project doesn't owe you success
- Your success doesn't owe you happiness
- The project is not your identity
- Walking away is always an option

## The Long Game

### What Success Looks Like
- Project serves its users
- Maintainers aren't burned out
- New maintainers are being developed
- Clear path forward exists

### What Sustainability Looks Like
- Multiple people can release
- Funding covers maintainer time
- Scope is appropriate to resources
- Community is healthy

### Remember
- Open source is a gift
- Given freely, received freely
- Gratitude is appropriate
- Entitlement is not
- You're building something bigger than yourself
- And that's worth protecting
