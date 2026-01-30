---
name: personal-strategic-planning
description: Annual strategic review and goal-setting interview for personal life/work domains with quarterly progress check-ins
triggers:
  - "personal annual review"
  - "personal strategic planning"
  - "personal goals"
  - "set personal goals"
  - "quarterly check-in"
  - "review my progress"
  - "year in review"
  - "plan for 2026"
  - "plan for 2027"
  - "personal planning"
  - "life goals"
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - mcp__obsidian-vault__create_vault_file
  - mcp__obsidian-vault__get_vault_file
version: 1.1.0
---

# Personal Strategic Planning Skill

Annual strategic review and goal-setting system combining interview-driven planning with evidence-based reflection across five personal life/work domains.

> **Note:** For organizational/K-12 district strategic planning, use the `strategic-planning-manager` skill instead.

## When to Activate

This skill activates when the user requests:

**Annual Review (Primary Mode):**
- "Let's do my annual review"
- "Help me plan for [year]"
- "I want to do strategic planning"
- "Set goals for next year"

**Quarterly Check-In (Lighter Mode):**
- "Quarterly check-in"
- "Review my progress"
- "How am I tracking against my goals?"

**Domain Modes:**
Each review covers 5 domains:
1. **CIO Role** (day job - Technology, Communications, Safety/Security)
2. **Consulting/Speaking** (reputation building, CoSN board, conferences)
3. **Product Development** (AI products: voice app, survey tool)
4. **Real Estate Investing** (portfolio management)
5. **Financial Planning** (entrepreneurial income, retirement prep)

## Available Scripts

### `scripts/generate_annual_review.py`
Generates formatted annual review markdown file in Obsidian.

**Usage:**
```bash
uv run scripts/generate_annual_review.py '{json_data}' --year 2026
```

**Input:** JSON with interview data (all domains, goals, indicators)
**Output:** Markdown file at `Personal_Notes/Reviews/Annual/{YEAR}-Annual-Review.md`

### `scripts/generate_quarterly_review.py`
Generates quarterly check-in markdown file in Obsidian.

**Usage:**
```bash
uv run scripts/generate_quarterly_review.py '{json_data}' --year 2026 --quarter Q1
```

**Input:** JSON with progress data per domain
**Output:** Markdown file at `Personal_Notes/Reviews/Quarterly/{YEAR}-Q{N}-Review.md`

### `scripts/sync_to_omnifocus.js`
Creates OmniFocus projects and tasks from Priority Goals.

**Usage:**
```bash
osascript -l JavaScript scripts/sync_to_omnifocus.js '{json_data}'
```

**Input:** JSON with goals, indicators, actions, milestones
**Output:** OmniFocus projects created, returns confirmation JSON

## Annual Review Workflow

The annual review follows a 6-phase interview pattern modeled after the `writer` skill.

### Phase 1: Domain Selection & Context Loading

**Objective:** Set scope and load relevant context for each domain.

**Geoffrey:**
1. Displays 5 domains with mission from `identity-core.json`:
   - CIO Role → TELOS Technology/Communications/Safety sections
   - Consulting/Speaking → TELOS Economics (reputation building)
   - Product Development → Short-term goals (AI products)
   - Real Estate → TELOS Economics (income streams)
   - Financial → Long-term goals (retirement, entrepreneurial income)

2. Asks: "Which domain(s) do you want to review?" (allow multi-select for first run)

3. For first annual review: Offer "Retrospective (2025) + Prospective (2026)" or "Prospective only"

**Output:** List of selected domains with loaded context

---

### Phase 2: Year-in-Review Reflection (Per Domain)

**Objective:** Ground planning in reality by examining what actually happened.

**Interview Questions (one domain at a time):**

**Q1:** "What were your top 3 priorities in [domain] this year?"

**Q2:** "For each priority, what actually happened?"
- **Challenge:** Require evidence/outcomes, not just activities
- **Push for:** Specific metrics, concrete changes, measurable results

**Q3:** "What worked exceptionally well in [domain]?"
- **Challenge:** Require specifics, not generalities
- **Push for:** Root causes of success, replicable patterns

**Q4:** "What underperformed or stalled?"
- **Challenge:** Require root causes, not just symptoms
- **Push for:** Honest assessment, systemic barriers

**Q5:** "What surprised you—positive or negative?"

**After all domains reviewed:**

**Q6:** "Looking across all domains, what patterns do you see?"

**Q7:** "What's one lesson you'd apply everywhere next year?"

**Challenge Mechanisms:**
- **Vague answer** → "Say more? What would that look like specifically?"
- **Activity-focused** → "That's what you did. What was the result?"
- **No evidence** → "What metric or outcome would prove that?"

---

### Phase 3: Strategic Direction (Per Domain)

**Objective:** Define clear vision for next year aligned with core mission.

**Interview Questions (one domain at a time):**

**Q1:** "At the end of [next year], what does success look like in [domain]?"
- **Must be:** Specific, measurable, stakeholder-focused
- **Challenge:** Push beyond vague aspirations to concrete outcomes

**Q2:** "Who are the primary stakeholders for [domain]?"
- **Follow-up:** "For each stakeholder, what specifically changes for them if you succeed?"

**Q3:** "How does [domain] success contribute to your core mission?"
- **Display:** Relevant TELOS section + constitution values
- **Challenge:** If alignment is weak, ask "Is this the right priority?"

**Q4:** "What are 2-3 major initiatives or changes in [domain]?"
- **Challenge if >3:** "Which would you protect if capacity gets constrained?"
- **Challenge if maintenance:** "Is this strategic work or keeping lights on?"

**Q5:** "What will you explicitly NOT do in [domain]?"
- **This is the hardest question** - use scaffolding if stuck:
  1. "What requests have you said no to—or wish you had?"
  2. "What did you consider but decide against?"
  3. "If someone proposed adding [new initiative], what would you tell them?"
  4. "What are you currently doing that you should stop?"
- **Why it matters:** "Every 'yes' is an implicit 'no' to something else. If you can't name what you're not doing, you haven't made strategic choices."

**Q6:** "What's the biggest barrier to success in [domain]?"
- **Follow-up:** "What needs to be true for you to succeed?"

**Q7:** "What resources/support do you need that you don't have?"
- **Challenge if "nothing":** "Most meaningful work requires time, development, or coordination—not just money."

**Challenge Progression:**
1. **Curious:** "Say more?" / "What would that look like?"
2. **Gentle push:** "Help me see this concretely. If I walked into your office in December [next year], what would I notice?"
3. **Direct challenge:** "This is staying abstract. Let's get specific—what's one concrete outcome?"
4. **Support scaffolding:** Offer frameworks, examples, different angles

**After domain completed:**
- Summarize strategic direction back to user
- Get confirmation before moving to next domain

---

### Phase 4: Priority Goals with Success Indicators (Per Domain)

**Objective:** Translate strategic direction into measurable progress.

**Constraints:**
- **Maximum 3 Priority Goals per domain** (hard cap)
- Each goal requires **2-3 Success Indicators** with baselines + targets
- Each goal requires **Key Actions** with owners, dependencies, timeline
- Each goal requires **Quarterly Milestones**

**Interview Process:**

**For each domain:**

1. **Establish Priority Goals:**
   - "Based on our conversation, what are your 2-3 Priority Goals for [domain]?"
   - **Challenge if >3:** "You've listed [N]. Research shows more than 3 priorities means none get focus. Which would you cut?"
   - **Challenge if activity-focused:** Reframe as outcome (e.g., "implement curriculum" → "students demonstrate deeper engagement")

2. **Define Success Indicators (for each goal):**
   - "How will you know you're making progress on [goal]?"
   - **Require:** Current state (baseline) → Target state (end of year)
   - **Accept:** Both quantitative and qualitative
     - Quantitative: "Student re-enrollment: 92% → 95%"
     - Qualitative: "Faculty report feeling supported: 45% agree → 70% agree"
   - **Challenge if no baseline:** "How will you establish one?" or "Is this a learning year?"
   - **Challenge if vague target:** "Too easy or unrealistic?"
   - **Challenge if activity metric:** "That measures what you did, not the result. What outcome changes?"

3. **Identify Actions, Owners, Dependencies:**
   - "What are the key actions that will drive [goal]?"
   - For each action:
     - **Action/Project:** What will be done
     - **Owner:** Who is accountable (a person, not committee)
     - **Dependencies:** Other people/teams/resources required
     - **Timeline:** Q1/Q2/Q3/Q4 milestones

4. **Map Quarterly Milestones:**
   - "What should be true by end of Q1 (Mar 31), Q2 (Jun 30), Q3 (Sep 30), Q4 (Dec 31)?"

**Challenge Mechanisms:**
- **Activity → Outcome reframing:** "If you do X successfully, what changes? That's the priority."
- **No baseline:** "Can you establish one now? If not, note this as 'learning year' for baseline."
- **Vague targets:** "If you hit this target, would you be satisfied? What would failure look like?"

**After all domains completed:**

5. **Confirm Alignment:**
   - "Looking at all your goals together—do they clearly ladder up to your strategic direction AND to your core mission?"
   - **If weak alignment:** Work to adjust or note misalignment for discussion

---

### Phase 5: Cross-Domain Integration

**Objective:** Portfolio view, trade-offs, advisor review, identity alignment.

**Portfolio Questions:**

**Q1:** "Looking at all 5 domains—what's the overall story of [next year]?"

**Q2:** "Where are you over-committed? What trade-offs do you need to make?"

**Q3:** "Which domain gets your BEST energy? Which gets leftovers?"

**Q4:** "If one domain had to be 'maintenance mode' in [next year], which and why?"

**Personal Board of Directors (optional but recommended):**

**Q5:** "Who are your 4-7 advisors across domains?"
- For each: Name, Domain expertise, What they help with, Last consulted
- **Roles to consider:** Connector, Accountability Partner, Futurist, Subject Matter Expert

**Q6:** "Who's missing from your board?"
- **Prompt:** "Do you have a Connector (network access), Futurist (trends), Accountability Partner?"

**Alignment with Identity:**

**Q7:** "Do these goals align with your Type 3w4 achievement pattern?"
- **Context:** Meaningful, competent, expert-level impact (from identity-core.json)

**Q8:** "Which goals leverage your Input/Analytical/Learner strengths?"
- **Display:** How each goal creates opportunities for information gathering, evidence-based thinking, mastery

**Q9:** "Any goals that require relationship building (your 0% Blue gap)?"
- **Follow-up:** "How will you handle that? Who can help?"

**Q10:** "Looking at your workload—where's the Type 3 stress risk?"
- **Context:** Type 3 pattern = push harder when stressed
- **Prompt:** "If things get overwhelming in Q2, what's your PAUSE trigger before pushing harder?"

---

### Phase 6: Review & Finalize

**Objective:** Generate output, get approval, save to systems.

**Geoffrey:**

1. **Display Complete Annual Review**
   - Use `templates/annual-review-template.md` format
   - Show full markdown output for review

2. **Get User Approval**
   - "Does this capture your strategic plan for [year]?"
   - "What would you adjust?"
   - Iterate until confirmed

3. **Save to Obsidian**
   - Run `scripts/generate_annual_review.py`
   - Save to `Personal_Notes/Reviews/Annual/{YEAR}-Annual-Review.md`

4. **Ask about OmniFocus**
   - "Create OmniFocus projects from your Priority Goals now or later?"
   - If now: Run `scripts/sync_to_omnifocus.js`

5. **Review Personal User Guide for Updates**
   - Read current User Guide: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal_Notes/Geoffrey/Kris-Hagel-User-Guide.md`
   - Compare to this year's review conversation:
     - Role changes (meeting cadences, team structure, responsibilities)
     - New growth areas identified
     - Communication pattern shifts
     - Changed priorities, frustrations, or energizers
     - "What drains me" / "What energizes me" updates
   - Propose specific, evidence-based updates:
     - "In this review you mentioned X, but your User Guide says Y. Should I update?"
     - "You identified [growth area] but it's not documented. Should we add it?"
   - If updates approved: Edit the User Guide and confirm changes
   - If significant changes: Suggest notifying team/peers

6. **Schedule Quarterly Reviews**
   - Confirm quarterly timing: Mar 31, Jun 30, Sep 30, Dec 31
   - Add to OmniFocus as recurring tasks

**Final Output:**
- Annual review markdown file (Obsidian)
- OmniFocus projects (if requested)
- Confirmation message with file path

---

## Quarterly Check-In Workflow

The quarterly check-in is a lighter interview (15-20 min) focused on progress and adjustment.

### Check-In Questions

**For each domain with Priority Goals:**

**Q1:** "Progress status on [Goal]?"
- ✅ On track (will hit target)
- ⚠️ At risk (may miss target without intervention)
- ❌ Off track (unlikely to hit target)

**Q2:** "What evidence supports your assessment?"
- Current state vs. Q{N} milestone
- What happened this quarter?

**Q3:** "What's working? What's stalled?"

**Q4:** "Do Success Indicators still make sense?"
- Adjust targets? (yes/no + rationale)
- Add/remove indicators?

**Q5:** "What needs to change for Q{N+1}?"
- Actions to add/drop
- Resources needed
- Trade-offs with other domains

**After all domains:**

**Q6:** "Overall portfolio health?"
- Energy distribution across domains
- Over-committed anywhere?
- Mid-course corrections needed?

**Q7:** "User Guide check against this quarter's insights"
- Read current User Guide: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Personal_Notes/Geoffrey/Kris-Hagel-User-Guide.md`
- Compare to quarterly progress discussion:
  - Any communication preferences that changed?
  - New frustrations or energizers to document?
  - Growth areas with visible progress?
- Propose specific updates based on evidence from this check-in
- If updates approved: Edit and save

### Check-In Output

**Geoffrey:**

1. Run `scripts/generate_quarterly_review.py`
2. Save to `Personal_Notes/Reviews/Quarterly/{YEAR}-Q{N}-Review.md`
3. Update annual review frontmatter with link to quarterly review
4. Confirm adjustments to OmniFocus if targets/actions changed

---

## Output Format

### Annual Review

See `templates/annual-review-template.md` for complete format.

**Key sections:**
- Year-in-Review Summary (cross-domain patterns, lessons)
- Per Domain: Review + Strategic Direction + Priority Goals
- Cross-Domain Integration (portfolio, trade-offs, advisors, alignment)
- Next Steps (quarterly reviews, OmniFocus sync, advisor shares)

### Quarterly Review

See `templates/quarterly-review-template.md` for complete format.

**Key sections:**
- Progress status per Priority Goal
- Evidence of progress vs. milestones
- What's working / what's stalled
- Adjustments for next quarter
- Portfolio health check

---

## Integration with Existing Systems

### Obsidian

**Storage locations:**
```
Personal_Notes/
└── Reviews/
    ├── Annual/
    │   └── YYYY-Annual-Review.md
    └── Quarterly/
        └── YYYY-QN-Review.md
```

**Frontmatter:**
```yaml
---
created: {date}
year: {YEAR}
domains: [CIO, Consulting, Product, RealEstate, Financial]
status: Draft | Final
quarterly_reviews:
  - Q1: [[YYYY-Q1-Review]]
  - Q2: null
  - Q3: null
  - Q4: null
---
```

### OmniFocus

**Project structure:**
- `[Domain] - [Goal Name]` (e.g., "CIO Role - Improve AI Adoption")
- Tasks for each action (owner/dependencies in notes)
- Milestones as tasks with Q1/Q2/Q3/Q4 due dates
- Tags: domain name + "2026 Goals"

### Personal User Guide

**Location:**
```
Personal_Notes/Geoffrey/Kris-Hagel-User-Guide.md
```

**Review triggers:**
- Annual review (Phase 6) - comprehensive review
- Quarterly check-ins - light evidence-based updates

**Update approach:**
- Evidence-based: Compare User Guide to review conversation
- Specific proposals: Point out discrepancies with examples
- User approval required before editing

### Identity-Core Integration

**Loads from:**
- `~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/knowledge/identity-core.json`

**References:**
- TELOS mission per domain
- Constitution values (equity, excellence, empathy, learning, innovation, integrity)
- Strengths (Input, Significance, Analytical, Achiever, Learner)
- Personality (Type 3w4, Green-Orange, 0% Blue relationship gap)
- Decision framework, stress patterns, growth edges

**Uses for:**
- Alignment checks in Part 3 (Strategic Direction)
- Challenge questions in Part 5 (Cross-Domain Integration)
- Framing success in terms of Mastery + Legacy + Freedom

---

## Framework Integration

### James Clear Systems Focus

**Applied in:**
- Success Indicators: Include leading (process) + lagging (outcome) metrics
- During goal-setting: Ask "What system/habit supports this goal?"
- Reframe outcome goals → process goals where appropriate

**Example:**
- Outcome: "Launch AI voice app"
- System: "Ship feature every 2 weeks" + "User feedback session biweekly"

### Personal Board of Directors

**Included in:** Part 5 (Cross-Domain Integration)

**Tracks:**
- 4-7 advisors across domains
- Roles: Connector, Accountability Partner, Futurist, Subject Matter Expert
- Last consulted date (accountability)

### Life Map (Alex Lieberman)

**Maps to 5 domains:**
- Career → CIO Role + Consulting/Speaking
- Finances → Real Estate + Financial Planning
- Meaning → Product Development (AI products = legacy)
- Relationships → Cross-domain question (0% Blue gap)
- Health → Not covered (note for future expansion)
- Fun → Not covered (note for future expansion)

### Ideal Lifestyle Costing (Tim Ferriss)

**Optional exercise in:** Financial Planning domain

**Question:** "What does your ideal [year] look like? Cost it out."
**Use for:** Retirement planning milestone

---

## Error Handling

### Common Scenarios

**1. User can't answer "what you will NOT do" (Q5 in Strategic Direction):**
- **Response:** Use scaffolding questions (see Phase 3)
- **If still stuck:** "Let's flag this and come back after Priority Goals are defined."
- **Note in output:** "Strategic exclusions to be determined"

**2. User has no baseline for Success Indicator:**
- **Response:** "Can you establish a baseline now? If not, we'll note this as a 'learning year' for baseline setting."
- **Record:** Current = "Baseline TBD" → Target = [value]

**3. User proposes >3 Priority Goals:**
- **Response:** "You've listed [N] priorities. Research shows more than 3 means none get focus. Which would you cut?"
- **Enforce:** Hard cap at 3 per domain

**4. User's goals don't align with strategic direction:**
- **Response:** "You said your strategic direction was [X], but this goal seems focused on [Y]. Help me see the connection."
- **If misalignment remains:** Note in "Potential Misalignments" section for discussion

**5. User wants to skip domains:**
- **Response:** Allow skipping for quarterly check-ins
- **For annual:** Recommend covering all 5, but allow "maintenance mode" designation

**6. User wants to adjust targets mid-year (quarterly check-in):**
- **Response:** "What changed? What's the rationale for adjusting?"
- **Record:** Original target + Revised target with date/reason
- **Update:** OmniFocus milestones if needed

---

## Future Enhancements

- [ ] Add Health and Fun domains to Life Map coverage
- [ ] Integrate with calendar for automatic quarterly review reminders
- [ ] Add mid-year strategic adjustment session (July)
- [ ] Create visualization dashboard for progress tracking
- [ ] Add retrospective analysis comparing year-over-year patterns
- [ ] Integration with knowledge-manager for automatic preference updates based on goals
- [ ] Add voice AI option for conducting interview (user speaks, Geoffrey transcribes and challenges)

---

## Version History

**v1.1.0** (2026-01-26)
- Renamed from strategic-planning-manager to personal-strategic-planning
- Updated triggers to avoid conflict with organizational planning skill
- For organizational/K-12 strategic planning, use strategic-planning-manager

**v1.0.0** (2026-01-02)
- Initial release
- Annual review interview (6 phases)
- Quarterly check-in interview
- Obsidian integration (Reviews folder)
- OmniFocus integration (auto-create projects)
- Identity-core alignment checks
- Progressive challenge mechanisms
- 5-domain structure
