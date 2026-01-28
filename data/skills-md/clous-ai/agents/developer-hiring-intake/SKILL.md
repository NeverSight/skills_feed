---
name: developer-hiring-intake
description: This skill should be used when the user asks to "start a hiring process", "create a job requisition", "define hiring requirements", "gather role details for hiring", or "create structured intake for a new role". Transforms unstructured hiring needs into comprehensive, legal-compliant JSON intake documents.
version: 0.1.0
license: MIT
---

# Developer Hiring Intake

Transform unstructured hiring needs into comprehensive, structured intake documents that ensure legal compliance, clear expectations, and effective recruiting strategies.

## Purpose

This skill guides the creation of standardized hiring intake documents for engineering roles. Intake documents serve as the foundation for job descriptions, recruiting strategies, interview loops, and offer packages. A well-structured intake prevents miscommunication, ensures legal compliance, and improves hiring outcomes.

## When to Use

Invoke this skill when:
- Starting a new engineering role requisition
- Replacing a departing team member
- Planning headcount for next quarter/year
- Converting contractor role to full-time
- Creating backfill requisition

## Core Process

### 1. Gather Role Context

Collect essential information about the role:

**Role Identity:**
- Job title (use standard industry titles: "Senior Backend Engineer", not "Code Ninja")
- Team and department
- Reporting structure (who the role reports to)
- Location requirements (remote, hybrid, specific office)

**Business Context:**
- Why is this role needed? (new headcount, backfill, team growth)
- What problem does this role solve?
- What happens if the role remains unfilled?
- Target start date and urgency level

**Team Structure:**
- Current team size
- Team distribution (locations, timezones)
- Related roles that interface with this position
- Team growth trajectory

### 2. Define Requirements

Create clear, legally-compliant requirements:

**Must-Have Requirements (Non-Negotiable):**
- Technical skills with proficiency levels (e.g., "5+ years Python production experience")
- Domain expertise (e.g., "distributed systems", "frontend frameworks")
- Behavioral competencies (e.g., "cross-functional collaboration")
- Legal requirements (work authorization, certifications)

**Nice-to-Have Requirements (Differentiators):**
- Bonus technical skills
- Industry experience
- Specific tool familiarity
- Advanced degrees or certifications

**Legal Compliance Check:**
- Avoid protected class references (age, race, gender, etc.)
- Use years of experience cautiously (can indicate age bias)
- Focus on skills and outcomes, not demographic characteristics
- Review jurisdiction-specific requirements (see `references/legal-compliance.md`)

### 3. Map Competencies

Define success criteria across competency areas:

**Technical Competency (Weight: typically 60-70%):**
- Core technical skills required
- Complexity of problems to solve
- Technical decision-making scope
- Code quality expectations

**Leadership Competency (Weight: typically 10-30%):**
- Mentoring expectations
- Technical leadership scope
- Influence beyond immediate team
- Strategic contributions

**Collaboration Competency (Weight: typically 10-20%):**
- Cross-functional work requirements
- Communication expectations
- Stakeholder management
- Team dynamics fit

Assign weights to competencies based on role level and team needs. Total weights must equal 100%.

### 4. Define Compensation

Establish competitive, equitable compensation:

**Base Salary Range:**
- Research market rates (use `references/compensation-research.md`)
- Consider: level, location, company stage, market conditions
- Define range with 15-25% spread (e.g., $180k-220k)
- Document competitive positioning (market rate, below, above)

**Equity/Stock Options:**
- Percentage or option count
- Vesting schedule (typically 4 years, 1-year cliff)
- Refresh policy

**Total Compensation:**
- Calculate total comp including equity, benefits
- Compare to market benchmarks
- Justify any below-market positioning

**Legal Considerations:**
- Comply with pay transparency laws (required in CA, CO, NY, WA, etc.)
- Document compensation rationale
- Ensure internal equity (similar roles, similar pay)

### 5. Plan Timeline

Create realistic hiring timeline:

**Key Milestones:**
- Intake approval date
- Job description completion
- Sourcing start date
- Interview loop availability
- Target offer date
- Target start date

**Interview Capacity:**
- Interviewers available per week
- Interview slots per week
- Estimated weeks from screen to offer
- Buffer for scheduling, decision-making

**Urgency Assessment:**
- Critical role (blocks major initiatives): expedited process
- Important role (team growth): standard process
- Future planning (building pipeline): extended process

### 6. Generate Structured Output

Produce JSON intake document conforming to schema:

```json
{
  "role": {
    "title": "string",
    "level": "string (Junior/Mid/Senior/Staff/Principal)",
    "team": "string",
    "department": "string",
    "reports_to": "string",
    "location": "string",
    "employment_type": "string (Full-time/Contract/Part-time)"
  },
  "business_context": {
    "role_type": "string (new_headcount/backfill/conversion)",
    "business_need": "string",
    "impact_if_unfilled": "string",
    "urgency": "string (critical/high/medium/low)"
  },
  "requirements": {
    "must_have": ["array of strings"],
    "nice_to_have": ["array of strings"],
    "years_experience": "string (e.g., '5-8 years')",
    "education": "string or null"
  },
  "competencies": {
    "technical": {
      "weight": 0.70,
      "description": "string",
      "key_skills": ["array"]
    },
    "leadership": {
      "weight": 0.20,
      "description": "string",
      "expectations": ["array"]
    },
    "collaboration": {
      "weight": 0.10,
      "description": "string",
      "expectations": ["array"]
    }
  },
  "compensation": {
    "base_range": "string (e.g., '$180k-220k')",
    "equity_range": "string",
    "total_comp_target": "string",
    "market_positioning": "string (market-rate/below/above)",
    "rationale": "string"
  },
  "timeline": {
    "target_start_date": "YYYY-MM-DD",
    "intake_approval_date": "YYYY-MM-DD",
    "sourcing_start_date": "YYYY-MM-DD",
    "interview_slots_per_week": 5,
    "estimated_weeks_to_offer": 4
  },
  "metadata": {
    "created_date": "YYYY-MM-DD",
    "created_by": "string",
    "approved_by": "string or null",
    "version": "1.0"
  }
}
```

Save output to `intake-{role-title}-{date}.json`.

### 7. Validate and Review

Run validation checks using `scripts/validate-intake.py`:

```bash
python scripts/validate-intake.py intake-senior-backend-2026-01-22.json
```

Validation checks:
- ✓ Schema compliance
- ✓ No protected class language
- ✓ Competency weights sum to 1.0
- ✓ Compensation range is reasonable (15-25% spread)
- ✓ Timeline is realistic (not too aggressive)
- ✓ Required fields populated

Review checklist:
- [ ] Role title uses industry-standard terminology
- [ ] Requirements focus on skills/outcomes, not demographics
- [ ] Compensation is competitive and internally equitable
- [ ] Timeline accounts for team interview capacity
- [ ] Business need clearly articulated
- [ ] Approval chain documented

## Using Supporting Resources

### Templates

Use the intake JSON template:
- **`templates/intake-template.json`** - Complete schema with examples
- **`templates/intake-minimal.json`** - Minimal required fields

### References

Consult detailed guidance:
- **`references/legal-compliance.md`** - EEOC guidelines, state laws, protected classes
- **`references/compensation-research.md`** - Market data sources, benchmarking methodology
- **`references/competency-frameworks.md`** - Detailed competency definitions by level

### Scripts

Run validation and analysis:
- **`scripts/validate-intake.py`** - Schema and compliance validation
- **`scripts/analyze-requirements.py`** - Detect biased language
- **`scripts/benchmark-comp.py`** - Compare compensation to market data

## Example Workflow

User request: "We need to hire a senior backend engineer for the platform team"

Response steps:
1. Ask clarifying questions about role context, urgency, team structure
2. Gather must-have vs nice-to-have requirements
3. Define competency expectations and weights
4. Research compensation ranges for level and location
5. Plan realistic timeline based on team capacity
6. Generate structured JSON intake document
7. Run validation script to check compliance
8. Present intake JSON and suggest next steps (job description, sourcing strategy)

## Next Steps After Intake

Once intake is complete:
1. Use `developer-recruiting-strategy` skill to create sourcing plan
2. Use `developer-interview-loop-design` skill to design interview process
3. Create job description based on intake document
4. Get intake approved by hiring manager and HR/legal

## Legal Disclaimer

This skill provides guidance based on best practices and common legal frameworks. It is not legal advice. Always consult with HR and legal counsel before finalizing hiring decisions, especially regarding:
- Protected class compliance
- Pay transparency requirements
- Offer letter language
- Background check policies

Jurisdictions have varying requirements. See `references/legal-compliance.md` for jurisdiction-specific considerations.

---

**Progressive Disclosure:** For detailed legal compliance guidance, compensation benchmarking methodology, and competency frameworks by level, consult the reference files. The core process above covers 90% of use cases; references handle edge cases and advanced scenarios.
