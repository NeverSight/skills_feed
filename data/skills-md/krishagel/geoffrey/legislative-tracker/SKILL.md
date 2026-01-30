---
name: legislative-tracker
description: >
  Track Washington State K-12 education legislation using committee-based discovery
  via SOAP API. Gets ALL bills from education committees - no keyword filtering
  that might miss bills. Use when: checking legislature, tracking bills,
  legislative updates, morning briefing legislative section.
triggers:
  - legislative tracker
  - leg tracker
  - wa legislature
  - check bills
  - education legislation
  - track bills
  - legislative radar
allowed-tools: Read, Bash, WebSearch, WebFetch, mcp__obsidian-vault__*
version: 0.2.0
---

# Legislative Tracker Skill

Track Washington State K-12 education legislation from leg.wa.gov using committee-based discovery. This approach queries committees directly via SOAP API to get ALL bills - not just keyword matches.

## Why Committee-Based Discovery

**Problem with keyword searching:** Bills with unexpected wording or indirect impacts get missed. A bill about "unfunded mandates" might never mention "school" but still affect districts.

**Solution:** Query education committees directly. If a bill is in the House Education Committee or Senate Early Learning & K-12 Education Committee, it's education-related by definition.

---

## Discovery Strategy

### Tier 1: Direct Education Bills (Comprehensive)

Query these committees to get **ALL** education bills:

| Committee | Chamber | Query |
|-----------|---------|-------|
| Education | House | All bills - no filtering |
| Early Learning & K-12 Education | Senate | All bills - no filtering |

### Tier 2: Indirect Impact Bills (Candidates)

Query these committees and filter via WebFetch:

| Committee | Chamber |
|-----------|---------|
| Appropriations | House |
| Capital Budget | House |
| Labor & Workplace Standards | House |
| Ways & Means | Senate |
| Labor & Commerce | Senate |
| State Government, Tribal Affairs & Elections | Senate |

**Workflow:** The SOAP API returns only bill IDs. Geoffrey must:
1. Get all bill IDs from Tier 2 committees (~700 bills)
2. WebFetch each bill's summary page to get the title/description
3. Filter for education keywords in the description
4. Add matching bills to the tracked list

**Filter keywords:** school, student, teacher, education, k-12, district, ospi, classroom, principal, paraeducator, learning, instruction, curriculum, diploma, graduation, superintendent, levy, bond, capital, school construction

### Tier 3: WebSearch Fallback

If SOAP API fails, use WebSearch:
```
site:leg.wa.gov "referred to Education" 2025-26
site:leg.wa.gov "Early Learning & K-12" 2025-26
site:leg.wa.gov K-12 school district bill 2025
```

---

## Workflow Phases

### Phase 1: Committee Discovery (SOAP)

Run the orchestrator script:

```bash
bun skills/legislative-tracker/scripts/get_bills.js
```

Returns two lists:
- **confirmed_bills**: From Tier 1 education committees (definitely education-related)
- **tier2_candidates**: From Tier 2 finance committees (need filtering)

### Phase 2: WebFetch Confirmed Bills

For each bill in `confirmed_bills`:

```
URL: https://app.leg.wa.gov/billsummary?BillNumber={NUM}&Year=2025
```

Extract full details for analysis.

### Phase 3: Filter Tier 2 Candidates

For each bill in `tier2_candidates`:

1. WebFetch the bill summary page
2. Check if title/description contains education keywords
3. If relevant, add to tracked bills list

**Education keywords:** school, student, teacher, education, k-12, district, ospi, classroom, principal, paraeducator, learning, instruction, curriculum, diploma, graduation, superintendent, levy, bond, capital

### Phase 4: Analysis

Apply analysis framework to all tracked bills:
- Assign priority level (HIGH/MEDIUM/LOW)
- Categorize impact type (FISCAL/OPERATIONAL/WORKFORCE/GOVERNANCE)
- Assess fiscal implications
- Flag district legislator sponsorship

### Phase 4: Output

Generate report in requested format and save to Obsidian:

```
Path: Work/PSD/Legislative/[YYYY-MM-DD].md
Tags: #legislation #psd #work
```

---

## Script Usage

### Main Orchestrator

```bash
# Full discovery (both tiers)
bun skills/legislative-tracker/scripts/get_bills.js

# Education committees only (Tier 1)
bun skills/legislative-tracker/scripts/get_bills.js --tier 1

# Finance committees only (Tier 2)
bun skills/legislative-tracker/scripts/get_bills.js --tier 2

# Briefing format for morning-briefing integration
bun skills/legislative-tracker/scripts/get_bills.js --format briefing
```

### Committee Explorer

```bash
# List all active committees
bun skills/legislative-tracker/scripts/get_committees.js

# House committees only
bun skills/legislative-tracker/scripts/get_committees.js --chamber house

# Education committees only
bun skills/legislative-tracker/scripts/get_committees.js --filter education
```

### Single Committee Query

```bash
# Get bills in a specific committee
bun skills/legislative-tracker/scripts/get_committee_bills.js \
  --committee "Education" --agency House

# Include referral history
bun skills/legislative-tracker/scripts/get_committee_bills.js \
  --committee "Education" --agency House --referrals
```

### Single Bill Lookup

```bash
# Get WebFetch URL for a specific bill
bun skills/legislative-tracker/scripts/get_bill_info.js HB 2551 --year 2025
bun skills/legislative-tracker/scripts/get_bill_info.js "SB 6247" --year 2025
```

---

## Analysis Framework

### Priority Levels

| Level | Symbol | Criteria |
|-------|--------|----------|
| HIGH | 🔴 | Direct fiscal impact >$100K, immediate deadline (<7 days), new mandates affecting operations, sponsored by district legislator |
| MEDIUM | 🟡 | Moderate impact, compliance changes, deadline within 30 days |
| LOW | 🟢 | Minimal direct impact, monitoring only, distant timeline |

### Impact Categories

| Category | Keywords | Description |
|----------|----------|-------------|
| FISCAL | levy, bond, funding, appropriation | Funding formulas, levies, bonds, appropriations |
| OPERATIONAL | procurement, transportation, facilities | Day-to-day operations, contracts, services |
| WORKFORCE | staff, salary, certification, benefits | Staffing, compensation, certification requirements |
| GOVERNANCE | reporting, accountability, board | Compliance, reporting, board authority |

### Fiscal Impact Indicators

| Indicator | Symbol | Meaning |
|-----------|--------|---------|
| COST INCREASE | ⬆️ | Adds expense to district budget |
| COST DECREASE | ⬇️ | Reduces costs or adds revenue |
| RISK | ⚠️ | Financial uncertainty or liability exposure |
| NEUTRAL | ➡️ | No direct fiscal impact to district |

---

## Output Formats

### Briefing JSON (for morning-briefing)

```json
{
  "summary": {
    "total_bills": 12,
    "new_this_period": 3,
    "urgent": 2,
    "by_priority": { "high": 2, "medium": 5, "low": 5 }
  },
  "priority_items": [
    {
      "bill": "HB 1234",
      "title": "Concerning school construction funding",
      "priority": "high",
      "impact": "fiscal",
      "fiscal_indicator": "cost_increase",
      "next_action": "House vote 2026-01-30",
      "summary": "Increases capital project funding requirements by 15%"
    }
  ],
  "upcoming_deadlines": [],
  "generated_at": "2026-01-27T08:00:00Z"
}
```

### Full Report Markdown

```markdown
# WA School Legislation Radar
Report Date: 2026-01-27
Session: 2025-26 Regular
Discovery: Committee-based (Tier 1 + Tier 2)

## 🚨 Priority Action Items

### 🔴 HIGH Priority

#### HB 1234 - School Construction Funding
- **Status:** Passed House, in Senate Education Committee
- **Sponsors:** Rep. Smith (26th), Rep. Jones
- **Impact:** FISCAL ⬆️
- **Summary:** Increases capital project funding requirements
- **Next Action:** Senate hearing Feb 1

## 📊 Legislative Dashboard

### Discovery Summary
| Source | Bills Found |
|--------|-------------|
| House Education | 15 |
| Senate EL/K-12 | 12 |
| Tier 2 (filtered) | 8 |
| **Total Unique** | **28** |

### By Priority
| Priority | Count | Bills |
|----------|-------|-------|
| 🔴 HIGH | 2 | HB 1234, SB 5678 |
| 🟡 MEDIUM | 5 | ... |
| 🟢 LOW | 5 | ... |

## 📋 All Tracked Bills

[Per-bill details grouped by priority level]

---
*Generated by Geoffrey Legislative Tracker*
*Discovery: Committee-based SOAP API*
```

---

## Data Sources

### SOAP API (Primary)

**Endpoint:** `https://wslwebservices.leg.wa.gov/`

| Service | Method | Purpose |
|---------|--------|---------|
| CommitteeService | GetActiveHouseCommittees | List House committee names |
| CommitteeService | GetActiveSenateCommittees | List Senate committee names |
| CommitteeActionService | GetInCommittee | Bills currently in committee |
| CommitteeActionService | GetCommitteeReferralsByCommittee | All bills ever referred |

**Parameters:**
- `biennium`: "2025-26"
- `agency`: "House" or "Senate"
- `committeeName`: Exact name from GetActive*Committees

### WebFetch (Bill Details)

**URL Pattern:** `https://app.leg.wa.gov/billsummary?BillNumber={NUM}&Year=2025`

---

## District Configuration

From `config/topics.yaml`:

```yaml
district:
  name: "Peninsula School District"
  legislators:
    - name: "Sen. Emily Randall"
      district: 26
      chamber: senate
    - name: "Rep. Spencer Hutchins"
      district: 26
      chamber: house
    - name: "Rep. Adison Richards"
      district: 26
      chamber: house
```

Bills sponsored by district legislators get elevated priority consideration.

---

## Error Handling

| Scenario | Response |
|----------|----------|
| SOAP timeout/error | Fall back to WebSearch (Tier 3) |
| Committee not found | Check exact name via get_committees.js |
| No bills in committee | Normal - committee may not have active bills |
| Bill page unavailable | Skip bill, note in report |

---

## Session Scope

- **Current biennium:** 2025-26
- **Session types:** Regular, Special (1st, 2nd, 3rd)
- **Year parameter for URLs:** 2025 (uses session start year)

---

## Related Skills

- **morning-briefing:** Receives legislative JSON for audio summary
- **obsidian-manager:** Stores full reports to vault
- **omnifocus-manager:** (Optional) Could create tasks for urgent deadlines
