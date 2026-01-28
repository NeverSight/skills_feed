---
name: developer-recruiting-strategy
description: This skill should be used when the user asks to "create a recruiting strategy", "plan sourcing channels", "define role scorecard", "build hiring plan", "identify must-haves vs nice-to-haves", or "create talent acquisition plan". Transforms hiring intake into actionable recruiting strategy with sourcing channels, scorecard, and execution plan.
version: 0.1.0
license: MIT
---

# Developer Recruiting Strategy

Convert hiring intake documents into comprehensive recruiting strategies that maximize candidate quality while minimizing time-to-hire.

## Purpose

This skill creates data-driven recruiting strategies for engineering roles. A strong strategy defines clear must-haves (non-negotiable) vs nice-to-haves (differentiators), identifies optimal sourcing channels, and establishes a realistic execution plan.

## When to Use

Invoke this skill when:
- Hiring intake is approved and ready for execution
- Need to define role scorecard for recruiters and hiring managers
- Planning multi-channel sourcing approach
- Establishing pass/fail criteria for candidates
- Creating recruiting team briefing document

## Core Process

### 1. Build Role Scorecard

Transform intake requirements into prioritized scorecard:

**Must-Have Criteria (Pass/Fail):**
- Extract from intake "must_have" requirements
- Make each criterion measurable and observable
- Define minimum acceptable evidence for each
- Ensure criteria are job-related (legal compliance)

**Nice-to-Have Criteria (Differentiators):**
- Extract from intake "nice_to_have" requirements
- Assign point values or tier ranking
- Use for candidate comparison, not screening

**Scoring Framework:**
```
Must-Haves: Binary (Yes/No) - candidate must pass ALL
Nice-to-Haves: Weighted (0-5 points each)
  - 5: Exceptional strength
  - 3-4: Clear evidence
  - 1-2: Some evidence
  - 0: No evidence
```

**Example Scorecard:**

| Criterion | Type | Evidence Required | Points |
|-----------|------|-------------------|--------|
| 5+ years backend experience | Must-have | Resume + references | Pass/Fail |
| Python production expertise | Must-have | Code review or take-home | Pass/Fail |
| Distributed systems | Must-have | System design interview | Pass/Fail |
| Kubernetes experience | Nice-to-have | Resume + discussion | 0-5 |
| Open source contributions | Nice-to-have | GitHub profile | 0-5 |

### 2. Define Sourcing Channels

Identify optimal channels based on role, urgency, and budget:

**Active Sourcing (Proactive Outreach):**
- LinkedIn Recruiter (best for senior+ engineers)
- GitHub (for open source contributors, technical roles)
- Stack Overflow Jobs/Talent (technical credibility signal)
- Conferences and meetups (niche specializations)
- Employee referrals (highest conversion, cultural fit)

**Passive Sourcing (Job Postings):**
- Company careers page (employer brand showcase)
- LinkedIn Jobs (broad reach, professional network)
- AngelList/Wellfound (startup ecosystem)
- Hacker News Who's Hiring (engineering-focused audience)
- Specialized job boards (e.g., RemoteOK for remote roles)

**Channel Selection Matrix:**

| Role Level | Urgency | Recommended Channels | Expected Conversion |
|------------|---------|---------------------|---------------------|
| Junior-Mid | Medium | Job postings, referrals, LinkedIn | 15-20% screen → offer |
| Senior | High | Active sourcing, referrals, GitHub | 10-15% screen → offer |
| Staff+ | Critical | Executive recruiting, warm intros | 5-10% screen → offer |

**Budget Considerations:**
- Employee referral bonus: $1,000-$5,000 (highest ROI)
- LinkedIn Recruiter: $8,000-$12,000/year
- External recruiter: 20-30% of first-year salary
- Job board postings: $200-$1,000 per posting

### 3. Craft Compelling Role Pitch

Create messaging that attracts target candidates:

**Value Proposition Elements:**
- **Technical Challenge:** What interesting problems will they solve?
- **Impact:** How does their work affect customers/business?
- **Growth:** Career development opportunities
- **Team:** Who will they work with? (highlight strong team members)
- **Tech Stack:** Modern, exciting technologies
- **Culture:** Remote flexibility, work-life balance, learning culture
- **Compensation:** Competitive range (required in many states)

**Messaging Framework:**

```markdown
## The Opportunity

[Company] is solving [important problem] for [customer type].
As [Role Title], you'll [key responsibility] to [business outcome].

## What You'll Do

- [Impactful project 1]
- [Technical challenge 2]
- [Leadership opportunity 3]

## What You'll Bring

- [Must-have 1]
- [Must-have 2]
- [Must-have 3]

Nice to have: [Differentiators]

## Why Join Us

- Work on [interesting technical challenge]
- [Growth opportunity]
- [Company momentum/traction]
- Compensation: [Range] + equity

[Apply link]
```

**Avoid Common Mistakes:**
- "Rockstar/Ninja/Guru" titles (unprofessional)
- Laundry list of 20+ requirements
- Vague responsibilities ("build cool stuff")
- No compensation information (illegal in many states)

### 4. Plan Execution Timeline

Create realistic timeline with milestones:

**Typical Engineering Hiring Timeline:**

| Stage | Duration | Cumulative | Activities |
|-------|----------|------------|------------|
| Sourcing | 1-2 weeks | Week 2 | Post jobs, active outreach, referrals |
| Phone screens | 1-2 weeks | Week 4 | Initial qualification calls |
| Technical screens | 1-2 weeks | Week 6 | Coding challenges, tech conversations |
| Onsite/Virtual onsites | 1-2 weeks | Week 8 | Full interview loops |
| Offer & negotiation | 0.5-1 week | Week 9 | Extend offer, negotiate, close |
| **Total** | **6-9 weeks** | | Screen to signed offer |

**Accelerated Timeline (Critical Roles):**
- Collapse sourcing + screening: Week 1-2
- Fast-track promising candidates
- Reduce to 4-6 weeks total
- Risk: May sacrifice candidate quality

**Extended Timeline (Pipeline Building):**
- Ongoing sourcing (no urgency)
- More thorough evaluation
- 10-12 weeks acceptable
- Benefit: Higher quality bar

**Capacity Planning:**
```
Required: [X] interview slots/week
Available: [Y] interviewers × [Z] hours/week
Bottleneck: [Identify constraint]
Mitigation: [Add interviewers or reduce loop]
```

### 5. Define Success Metrics

Establish measurable goals for recruiting process:

**Funnel Metrics:**
- Sourced candidates → Applications: X candidates
- Applications → Phone screen: Y% pass rate
- Phone screen → Technical: Y% pass rate
- Technical → Onsite: Y% pass rate
- Onsite → Offer: Y% pass rate
- Offer → Accept: Y% acceptance rate

**Quality Metrics:**
- Average interview scorecard rating: ≥ 3.5/5
- Must-have pass rate: 100%
- Diversity of candidate pipeline: X% underrepresented groups
- Referral rate: X% of hires from referrals

**Time Metrics:**
- Time to first interview: ≤ 1 week
- Time to offer: ≤ 6-8 weeks
- Offer acceptance time: ≤ 1 week

**Cost Metrics:**
- Cost per hire: $X,000
- Recruiter hours per hire: X hours
- ROI by channel: $ spent / hire made

### 6. Generate Strategy Document

Produce comprehensive recruiting strategy:

**Output Structure:**

```json
{
  "role_summary": {
    "title": "string",
    "level": "string",
    "team": "string",
    "target_start_date": "YYYY-MM-DD"
  },
  "scorecard": {
    "must_haves": [
      {
        "criterion": "string",
        "evidence_required": "string",
        "assessment_stage": "resume|screen|technical|onsite"
      }
    ],
    "nice_to_haves": [
      {
        "criterion": "string",
        "points": 5,
        "assessment_stage": "string"
      }
    ]
  },
  "sourcing_strategy": {
    "primary_channels": ["array"],
    "secondary_channels": ["array"],
    "estimated_outreach": {
      "linkedin_messages": 100,
      "referral_asks": 20,
      "job_posting_reach": 5000
    },
    "budget": {
      "total": "$X,000",
      "breakdown": {}
    }
  },
  "value_proposition": {
    "technical_challenge": "string",
    "impact": "string",
    "growth_opportunity": "string",
    "team_strength": "string"
  },
  "timeline": {
    "milestones": [
      {
        "stage": "string",
        "target_date": "YYYY-MM-DD",
        "deliverable": "string"
      }
    ],
    "estimated_weeks_to_hire": 8
  },
  "success_metrics": {
    "target_applications": 50,
    "target_phone_screens": 20,
    "target_onsites": 8,
    "target_offers": 2,
    "acceptance_rate_target": "50%"
  }
}
```

Save to `strategy-{role}-{date}.json`.

### 7. Brief Recruiting Team

Create recruiter briefing document:

**Briefing Contents:**
- Role overview (from intake)
- Scorecard (must-haves, nice-to-haves)
- Ideal candidate profile
- Sourcing channels and messaging
- Disqualification criteria (red flags)
- Selling points (why join)
- Interview process overview
- Timeline and urgency

Use template at `templates/recruiter-brief.md`.

## Using Supporting Resources

### Templates
- **`templates/scorecard-template.json`** - Role scorecard schema
- **`templates/sourcing-plan.md`** - Channel strategy template
- **`templates/recruiter-brief.md`** - Recruiter onboarding doc

### References
- **`references/sourcing-channels.md`** - Detailed channel comparison, conversion rates
- **`references/messaging-best-practices.md`** - Job description writing, outreach templates
- **`references/diversity-sourcing.md`** - Strategies for diverse candidate pipelines

### Scripts
- **`scripts/validate-scorecard.py`** - Check scorecard completeness
- **`scripts/estimate-funnel.py`** - Model hiring funnel metrics
- **`scripts/channel-roi.py`** - Calculate ROI by sourcing channel

## Example Workflow

User: "Create recruiting strategy for the senior backend role we just defined"

Steps:
1. Load hiring intake JSON
2. Extract must-haves → Build scorecard criteria
3. Assess role level + urgency → Select sourcing channels
4. Draft value proposition highlighting technical challenges
5. Plan 8-week timeline with capacity constraints
6. Define success metrics (50 applies → 2 offers)
7. Generate strategy JSON + recruiter brief
8. Validate with scorecard script

Output: Complete recruiting strategy ready for execution

## Next Steps

After strategy is complete:
1. Use `developer-interview-loop-design` to build interview process
2. Share strategy with recruiting team
3. Launch sourcing campaigns
4. Track metrics weekly
5. Adjust strategy based on early funnel performance

---

**Progressive Disclosure:** Detailed sourcing channel data, messaging templates, and diversity recruiting strategies are in references/. Core strategy framework above handles standard use cases.
