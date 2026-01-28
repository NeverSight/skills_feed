---
name: apply-job
description: Automated job applications with AI-powered resume tailoring, cover letters, and recruiter outreach via email and LinkedIn.
license: MIT
metadata:
  author: theaayushstha1
  version: "3.1.0"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - Bash
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - mcp__playwright__browser_type
  - mcp__playwright__browser_fill_form
  - mcp__playwright__browser_file_upload
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_wait_for
  - mcp__playwright__browser_evaluate
  - mcp__playwright__browser_console_messages
  - mcp__playwright__browser_run_code
  - mcp__playwright__browser_press_key
---

# Job Application Agent

Automated job application system with multi-channel recruiter outreach.

## Quick Start

```bash
/apply-job <url>              # Apply to specific job
/apply-job search <query>     # Search and batch apply
/apply-job outreach <url>     # Recruiter outreach only
/apply-job status             # View statistics
/apply-job score <url>        # Score job fit only
```

## Setup Required

Before first use, ensure these files exist:

| File | Purpose |
|------|---------|
| `$APPLIER_HOME/data/profile.json` | Your personal info (from template) |
| `$APPLIER_HOME/data/applications.json` | Application tracking |
| `$APPLIER_HOME/resume/master_resume.md` | Your complete resume |
| `$APPLIER_HOME/resume/formatting_rules.md` | **CRITICAL** - Exact resume formatting specs |
| `$APPLIER_HOME/resume/create_resume.py` | Master Python script for DOCX generation |
| `$APPLIER_HOME/templates/cover_letter.md` | Cover letter template |
| `$APPLIER_HOME/templates/cold_email.md` | Cold email template |

**$APPLIER_HOME** = `~/job-applier-agent` (cross-platform)

See [SETUP.md](SETUP.md) for installation instructions.

---

## Core Principles

### AUTO-PROCEED Mode
- **DO NOT** ask for confirmation at routine steps
- **JUST DO IT** - proceed through entire workflow automatically
- **ONLY STOP** for: login walls, CAPTCHA, critical errors, fit score < 5.0

### ⚠️ Outreach Order (CRITICAL)
```
1. Find recruiters on LinkedIn (names, titles, URLs)
2. Discover email addresses (WebSearch company email pattern)
3. Send cold emails via Gmail FIRST
4. THEN send LinkedIn connection requests
5. Track everything in applications.json
```
**Email = PRIMARY (higher response rate). LinkedIn = SECONDARY.**

---

## Workflow: Apply to Job URL

### Step 1: Extract Job Description
```
1. Navigate to job URL with Playwright
2. Capture page snapshot
3. Extract: title, company, location, requirements
4. Identify key skills/technologies
```

### Step 2: Score Job Fit (0-10 each)
- **Technical Fit**: Skills match percentage
- **Level Match**: Appropriate for experience level
- **Location**: Remote/local/relocation
- **Mission**: Company alignment

Score >= 5.0 → AUTO-PROCEED | Score < 5.0 → Notify user

### Step 3: Tailor Resume

**CRITICAL:** Follow [formatting_rules.md](../../resume/formatting_rules.md) exactly!

```
1. Read $APPLIER_HOME/resume/master_resume.md
2. Copy master Python script (create_resume.py)
3. Analyze JD for:
   - Required technologies
   - Nice-to-have technologies
   - Scale/performance language
   - Domain keywords (AI, data, etc.)
4. Modify CONTENT ONLY in the copied script:
   - Reword bullets to match JD language
   - Bold technologies that match JD exactly
   - Reorder skills (JD technologies first)
   - Reorder projects (most relevant first)
   - Add power words matching JD focus
5. NEVER modify functions, margins, font sizes, or spacing
6. Save tailored script to $APPLIER_HOME/applications/<Company>/
7. Generate DOCX with: python create_<company>_resume.py
```

**Tailoring Rules:**
- NEVER add skills you don't have
- NEVER fabricate metrics or achievements
- DO reword bullets using JD terminology
- DO bold exact technologies from JD
- DO reorder sections for relevance
- DO add scale/performance words if JD mentions them

**Power Words by JD Focus:**
| JD Focus | Use These Words |
|----------|-----------------|
| Scale | "high-traffic", "thousands of requests", "production system" |
| Performance | "sub-second", "reduced latency", "optimized" |
| Data | "data pipelines", "real-time", "event processing" |
| AI | "AI-powered", "LLMs", "ML models" |

### Step 4: Generate Cover Letter
```
1. Read $APPLIER_HOME/templates/cover_letter.md
2. Research company (WebFetch)
3. Personalize for role + company
4. Keep to 250-350 words
5. Save to $APPLIER_HOME/applications/<Company>/
```

### Step 5: Auto-Fill Application
Use Playwright to fill forms based on platform:
- LinkedIn Easy Apply
- Company career pages (Greenhouse, Lever, Workday, ADP, etc.)
- Upload resume, add cover letter if field exists

### Step 6: Track & Screenshot
```
1. Take confirmation screenshot
2. Update $APPLIER_HOME/data/applications.json
3. Update stats
```

### Step 7: Recruiter Outreach

See [WORKFLOWS.md](WORKFLOWS.md) for detailed outreach steps.

**Summary:**
1. Search LinkedIn for company recruiters (3+ people)
2. Discover emails via WebSearch (company email pattern)
3. Send cold emails via Gmail (use template)
4. Send LinkedIn connections (after emails)
5. Track all outreach in applications.json

---

## Email Discovery

### Common Patterns (try in order)
```
Startups:      firstname@company.com
Mid-size:      firstname.lastname@company.com, flastname@company.com
Enterprise:    firstname.lastname@company.com, firstnamel@company.com
```

### Discovery Method
```
1. WebSearch: "[Company] email format site:rocketreach.co"
2. WebSearch: "[Name] [Company] email"
3. Apply pattern to recruiter names
```

---

## Profile Configuration

All personal data comes from `$APPLIER_HOME/data/profile.json`:

```json
{
  "personal": {
    "name": "Your Name",
    "email": "you@email.com",
    "phone": "123-456-7890",
    "location": "City, State"
  },
  "links": {
    "website": "https://yoursite.com",
    "linkedin": "linkedin.com/in/you",
    "github": "github.com/you"
  },
  "education": {
    "school": "University Name",
    "degree": "BS Computer Science",
    "gpa": "3.9",
    "graduation": "May 2026"
  },
  "headline": "Your professional headline",
  "top_skills": ["Python", "React", "AWS"],
  "flagship_project": {
    "name": "Project Name",
    "description": "Brief description",
    "users": "100+"
  },
  "work_auth": true,
  "willing_to_relocate": true,
  "location_preference": ["Remote", "NYC", "SF"]
}
```

See [profile-template.json](profile-template.json) for full template.

---

## Application Tracking

`$APPLIER_HOME/data/applications.json` schema:

```json
{
  "applications": [{
    "id": "company-date-001",
    "company": "Company Name",
    "role": "Job Title",
    "url": "https://...",
    "platform": "linkedin|greenhouse|workday|adp",
    "applied_date": "2026-01-27",
    "status": "applied|interviewed|rejected|offer",
    "fit_score": 7.5,
    "cover_letter": true,
    "outreach": [{
      "name": "Recruiter Name",
      "title": "Technical Recruiter",
      "email": "recruiter@company.com",
      "linkedin": "linkedin.com/in/...",
      "email_sent": true,
      "connection_sent": true,
      "date": "2026-01-27"
    }]
  }],
  "stats": {
    "total": 0,
    "applied": 0,
    "interviewed": 0,
    "emailsSent": 0,
    "connectionsSent": 0
  }
}
```

---

## Cold Email Template

```
Subject: Referral Request - [Role] Application | [School] [Major] Senior

Hi [First Name],

I just applied for the [Role] position at [Company] and wanted to reach out.

I'm a [Major] senior at [School] ([GPA] GPA) graduating [Graduation].
[Flagship project description with metrics].

[1-2 sentences about why THIS company excites you]

Would appreciate if you could review my application or put in a referral.

Thanks!
[Name]
[Website]
[Phone]
```

**Rules**: Under 150 words. Personalize company line. Include contact info.

---

## Error Handling

| Error | Action |
|-------|--------|
| Login required | Notify user, wait for "continue" |
| CAPTCHA | Notify user, wait |
| Rate limit | Wait 60s, retry once, skip if still blocked |
| Email failed | Log, continue with LinkedIn |
| Form field missing | Screenshot, ask user |

---

## Reference Files

| File | Content |
|------|---------|
| [WORKFLOWS.md](WORKFLOWS.md) | Detailed step-by-step workflows |
| [SETUP.md](SETUP.md) | Installation & configuration |
| [profile-template.json](profile-template.json) | Profile data template |
| [formatting_rules.md](../../resume/formatting_rules.md) | **CRITICAL** - Exact DOCX formatting specs |

---

## Path Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `$APPLIER_HOME` | `~/job-applier-agent` | Base directory |
| `$APPLICATIONS_DIR` | `$APPLIER_HOME/applications` | Per-company files |

**Cross-platform**: Use `~/` which expands to home directory on all OS.

---

## Best Practices

1. **Email FIRST, LinkedIn SECOND** - Always send emails before connections
2. **AUTO-PROCEED** - Don't ask, just do (except critical errors)
3. **Track everything** - Update applications.json after every action
4. **Personalize** - Reference specific company details in outreach
5. **Screenshot** - Capture confirmation for records
6. **Be honest** - Never fabricate skills or metrics

---

**Line Count**: ~280 (under 500 ✓)
**Cross-Platform**: Yes (uses ~/ paths) ✓
**User-Agnostic**: Yes (data in profile.json) ✓
