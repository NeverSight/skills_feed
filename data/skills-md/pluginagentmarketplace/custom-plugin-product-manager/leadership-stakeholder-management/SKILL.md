---
name: leadership-stakeholder-management
version: "2.0.0"
description: Master stakeholder management, executive communication, cross-functional alignment, and product advocacy. Lead effectively across your organization.
sasmp_version: "1.3.0"
bonded_agent: 07-leadership-stakeholder
bond_type: PRIMARY_BOND
parameters:
  - name: communication_type
    type: string
    enum: [executive, cross_functional, board, team]
    required: true
  - name: stakeholder_count
    type: number
retry_logic:
  max_attempts: 3
  backoff: exponential
logging:
  level: info
  hooks: [start, complete, error]
---

# Leadership & Stakeholder Management Skill

Master the human side of product management. Align stakeholders, communicate effectively, resolve conflicts, and inspire teams toward shared vision.

## Stakeholder Mapping & Analysis

### Identify All Stakeholders

```
┌─────────────────┬──────────────────┐
│   DECISION      │    INFLUENCE     │  ← POWER
│   MAKERS        │    MAKERS        │
│                 │                  │
│   CEO, Board    │  VP Eng, Design  │
├─────────────────┼──────────────────┤
│   USERS         │   SUPPORT        │  ← LOW POWER
│                 │   TEAM           │
└─────────────────┴──────────────────┘
     LOW              HIGH
     INTEREST    ← INTEREST →
```

### Stakeholder List

**Internal Stakeholders:**

**Executive Team**
- CEO: Company success
- CFO: Budget/profitability
- CTO: Technical feasibility
- COO: Operational impact

**Engineering**
- VP Engineering: Tech strategy, resourcing
- Engineering Lead: Implementation difficulty
- QA Lead: Testing time needed

**Design**
- Design Lead: User experience, design system impact

**Marketing**
- VP Marketing: GTM, messaging
- Demand Gen: Conversion impact

**Sales**
- VP Sales: Sales enablement, revenue impact
- Sales team: Product capability

**Customer Success**
- VP CS: Customer satisfaction impact

**Support**
- Support Lead: Support volume impact

**External Stakeholders:**
- Investors: Business metrics
- Major customers: Feature requests
- Partners: Integration impact
- Community: Open source projects

### Stakeholder Assessment

For each stakeholder:
1. **Interest Level** - How much do they care?
2. **Influence Level** - How much power do they have?
3. **Attitude** - Supportive, neutral, or resistant?
4. **Communication Needs** - What do they need to hear?

**Engagement Strategy:**
- **Manage Closely** (high interest, high power) - Weekly updates, deep involvement
- **Keep Satisfied** (low interest, high power) - Monthly updates, key decisions
- **Keep Informed** (high interest, low power) - Transparency, feedback loops
- **Monitor** (low interest, low power) - Occasional updates

## Communication Frameworks

### BLUF (Bottom Line Up Front)

**Structure:**
1. **Bottom Line** (1 sentence) - The decision/news
2. **Situation** (2-3 sentences) - Context and background
3. **Implications** (2-3 sentences) - Why it matters
4. **Next Steps** - What happens now

**Example:**
```
BOTTOM LINE: We're pausing the mobile app to focus on web performance.

SITUATION: Our web app speed is 2x slower than competitors, causing
40% of free users to churn. Mobile app is only 5% of usage.

IMPLICATIONS: Focusing on web unlocks 10x retention improvements,
strengthens our core offering, and builds foundation for mobile later.

NEXT STEPS: Engineering team shifts Tuesday. We'll replan mobile for Q2.
```

### SitRep (Situation Report)

**Weekly Status Template:**
```
PROJECT: [Name]
STATUS: On Track / At Risk / Off Track
PROGRESS:
- Completed: [Achievement]
- In Progress: [Current work]
- Blocked: [Blockers]

METRICS:
- Metric 1: [Current vs Target]
- Metric 2: [Current vs Target]

CHALLENGES:
- Challenge 1 (Severity: High)
  Mitigation: [Plan]
- Challenge 2 (Severity: Medium)

NEXT WEEK:
- Next step 1
- Next step 2
```

### One-Pager Format

**2-Page Executive Brief:**

**Page 1:**
- Title and date
- Summary (2-3 sentences)
- Problem statement
- Proposed solution
- Expected impact (revenue/growth/NPS)

**Page 2:**
- Detailed reasoning
- Success metrics
- Timeline
- Resource needs
- Risks and mitigations
- Decision requested

## Executive Communication

### Board Update (Monthly/Quarterly)

**Presentation Structure (30 minutes):**

1. **Dashboard** (5 min)
   - Key metrics vs targets
   - Green/yellow/red status
   - Trend arrows

2. **Progress** (5 min)
   - Launched features
   - Customer wins
   - Team updates

3. **Challenges** (5 min)
   - Market challenges
   - Competitive threats
   - Internal blockers

4. **Opportunities** (5 min)
   - Market opportunities
   - Strategic bets
   - Investment needs

5. **Request** (5 min)
   - What you need (capital, resources, approval)
   - Timeline and impact
   - Board decision needed

### Pitch Deck (Investor Ready)

**15-20 Slides:**
1. Problem (customer pain)
2. Market opportunity (TAM/SAM/SOM)
3. Solution (what you're building)
4. Product demo (show it working)
5. Business model (how you make money)
6. Go-to-market (customer acquisition)
7. Team (why you'll win)
8. Traction (customer proof)
9. Financials (revenue projections)
10. Use of funds (how you'll use investment)
11. Q&A (be ready)

### Executive Storytelling

**Golden Circle Framework:**

```
       WHY?
      ░░░░░
    ┌────────┐
    │ What?  │
    │(Facts) │
    └────────┘

WHY: Why does this matter?
WHAT: What are we doing?
HOW: How will we do it?
```

**Example:**
```
WHY: Every team wastes hours syncing data across tools
WHAT: We're building one unified hub for collaboration
HOW: Real-time sync, zero-config integrations, beautiful UX
```

## Cross-Functional Alignment

### Stakeholder Alignment Meeting

**Pre-Meeting (Friday before):**
- Send agenda + context
- 1-pager with key points
- Data/evidence
- Proposed decision

**Meeting (Monday, 45 minutes):**
- **Opening** (5 min) - Goal and decision needed
- **Context** (10 min) - Why this matters
- **Proposal** (10 min) - What we recommend
- **Discussion** (15 min) - Questions and concerns
- **Decision** (5 min) - Clear decision and next steps

**Post-Meeting (Tuesday):**
- Send summary
- Decision documented
- Next steps assigned
- Follow-up timeline

### Conflict Resolution

**When stakeholders disagree:**

1. **Listen deeply** - Understand both perspectives
2. **Find common ground** - What do both care about?
3. **Reframe** - Bigger goal both support
4. **Propose trade-off** - Can you do both phased?
5. **Decide** - If needed, PM makes call (with escalation path)

**Example:**

Engineering wants more technical debt cleanup.
Sales wants new features for customers.

**Reframe:** Both want happy, sticky customers.
- Cleanup: Makes new features faster, higher quality
- Features: What customers actively need

**Trade-off:** 70% features, 30% cleanup each sprint

### Regular Cadence Meetings

**Weekly:**
- Product standup (15 min) - Progress update
- Engineering sync (30 min) - Technical discussions
- Design review (30 min) - Design progress

**Bi-Weekly:**
- Product council (60 min) - Roadmap decisions
- Cross-functional planning (60 min) - Upcoming work

**Monthly:**
- All hands (30 min) - Company updates
- Customer advisory board (60 min) - Customer feedback

**Quarterly:**
- Planning (8 hours) - Next quarter roadmap
- Retrospective (2 hours) - Learnings

## Product Advocacy

### Internal Advocacy

**Get team excited about vision:**
- Tell compelling stories
- Share customer quotes
- Celebrate wins
- Make impact visible
- Create ownership

**Communication:**
- Weekly email update
- Monthly townhall
- Slack announcements
- One-on-ones

### External Advocacy

**Build authority and trust:**

**Writing:**
- Blog posts on industry trends
- LinkedIn articles on product thinking
- Case studies of successful customers

**Speaking:**
- Conferences talks (be selective)
- Podcast interviews
- Webinars for customers
- Media interviews

**Community:**
- Twitter/LinkedIn engagement
- Answer user questions
- Share roadmap transparently
- Ask for feedback publicly

### Media & PR

**Press Release Template:**
```
For Immediate Release

[Company] Launches [Product] to Help [Customer Type] [Benefit]

[City] - [Company] today announced the launch of [Product],
which [key benefit].

Key features:
- Feature 1
- Feature 2
- Feature 3

"[CEO quote about why this matters]," said [Name].

Availability: [Where/when available]

About [Company]: [1-2 sentence description]

Contact: [PR contact]
```

## Change Management

### When You Need to Change Course

**Announcement Framework:**

1. **The Past** - What we learned, why it was right then
2. **The Present** - New information/market reality
3. **The Future** - New direction and why it's better
4. **The Impact** - What changes for each group
5. **The Support** - How we'll help with transition

**Example:**

"We've learned that SMBs (not Enterprise) is our biggest opportunity.
(Our focus was backwards.)

We're shifting all resources to SMB GTM starting next month.
(The change.)

Enterprise sales team will transition to SMB sales team.
(Impact.)

We'll provide training and offer roles in other departments.
(Support.)"

## Communication Cadence

### Weekly
- Status email
- 1-on-1s with reports
- Product standup
- Stakeholder updates

### Monthly
- All-hands presentation
- Product email newsletter
- Metrics review
- Stakeholder meetings

### Quarterly
- Strategic review
- Roadmap presentation
- Team offsite
- Board update

### Annually
- Company retreat
- Vision refresh
- Compensation/promotion cycle

## Difficult Conversations

### Delivering Difficult News

**Structure:**
1. **Lead with empathy** - "I know this affects you"
2. **Be clear and direct** - Not dancing around
3. **Explain why** - Context and reasoning
4. **Give space** - Let them react
5. **Offer support** - "Here's how I'll help"

**Example:**

"I know you were expecting the mobile app this quarter. We've made
the difficult decision to delay it to focus on web performance,
which is causing churn. This was a tough call but right for the
business. I want to help you through the transition. What concerns
you most?"

### Saying No

**To feature requests:**
"That's a great idea. It would solve [problem]. Right now we're
focused on [strategic priority] which impacts [bigger opportunity].
I'm adding it to the roadmap for Q2. Can we put a placeholder?"

**To stakeholder pressure:**
"I understand you need this. Our roadmap is full of higher-impact
items. If this is truly critical, what would you deprioritize?
I need to understand the trade-off."

## Troubleshooting

### Yaygın Hatalar & Çözümler

| Hata | Olası Sebep | Çözüm |
|------|-------------|-------|
| Stakeholder resistance | Insufficient involvement | Early inclusion |
| Decision paralysis | Too many stakeholders | RACI matrix |
| Misalignment | Poor communication | Increase cadence |
| Conflict escalation | Unaddressed concerns | 1:1 meetings |

### Debug Checklist

```
[ ] Tüm stakeholder'lar identified mi?
[ ] RACI matrix var mı?
[ ] Communication cadence set mi?
[ ] Decision rights clear mi?
[ ] Conflict early identified mi?
```

### Recovery Procedures

1. **Stakeholder Conflict** → 1:1 meetings, understand concerns
2. **Decision Deadlock** → Trade-off matrix, escalate
3. **Change Resistance** → Address concerns, show benefits

---

**Master leadership and inspire your organization toward great products!**
