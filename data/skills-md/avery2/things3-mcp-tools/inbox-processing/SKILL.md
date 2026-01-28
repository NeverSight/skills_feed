---
name: inbox-processing
description: Workflow for processing large Things3 inboxes (100+ items) using LLM-driven confidence matching and intelligent automation. Integrates with personal taxonomy and MCP tools for efficient cleanup with self-improving pattern learning.
---

# Inbox Processing & Large-Scale Organization

## Overview

Process large Things3 inboxes (100+ items) efficiently through batch analysis, confidence-based automation, and intelligent user interaction.

**CRITICAL**: Before using this skill:
- Load `things3-productivity` skill for MCP tool patterns
- Read `private-prefs/personal-taxonomy.json` for organizational context
- Create `temp/inbox-processing/` folder for session state

**When to use**: Inbox has 100+ items requiring organization.

## Personal Organization Integration

Claude uses LLM-driven analysis with semantic understanding from `personal-taxonomy.json`:
- **Work identification**: Tags (e.g., "AMPL") and areas (e.g., "Amplitude")
- **Priority system**: 1-9 scale, 7+ for high priority
- **Project patterns**: Existing projects and typical content
- **Semantic matching**: Based on meaning, not just keywords

## Core Workflow: 14-Step Process

### Phase 1: Initialize & Analyze (Steps 1-3)

**Step 1: Setup** - Create `temp/inbox-processing/` with:
```
session.md                    # Batch progress, statistics
match_results.json            # Decisions with confidence scores
pending_decisions.json        # Items awaiting approval
high_confidence_actions.json  # Auto-apply candidates (≥90%)
reference_items.json          # Detected reference notes
execution_log.md              # Complete action history
```

**Step 2: Load Inbox Batch** - First batch: 50 items, subsequent: 50-100 items
```python
read_tasks(when="inbox", limit=50, include_notes=True)
```

**Step 3: Load System Inventory** - Cache once per session
```python
list_areas()    # All areas with IDs and tags
list_projects() # All projects with metadata
list_tags()     # All tags including hierarchy
```

### Phase 2: Categorize & Match (Steps 4-6)

**Step 4: Categorize Items** - Use semantic understanding:
- **Actionable tasks**: Clear next actions, specific outcomes
- **Reference items**: Notes, ideas, meeting summaries
- **Project candidates**: Multiple related tasks suggesting new project

**Step 5: Match to Existing Structure** - LLM-driven matching:
- Analyze title and notes semantically
- Consider existing areas, projects, tags
- Apply personal taxonomy patterns
- Generate confidence score (0-100%)

**Step 6: Categorize by Confidence**
- **High (90-100%)**: Auto-apply with batch approval
- **Medium (70-89%)**: Ask user in batches
- **Low (<70%)**: Keep in inbox or ask individually

### Phase 3: User Interaction (Steps 7-9)

**Step 7: High-Confidence Batch Approval**
```markdown
## High-Confidence Matches (Batch 1: 35 items)

### Area: Amplitude (25 items, 90-100% confidence)
**Direct area references:**
- "Amplitude: Fix login bug" (100%) - Explicit area mention
- "Dashboard review for AMPL" (95%) - Work tag + clear context

**Action Plan:**
1. Set area="Amplitude" for 25 items
2. Add tags=["AMPL"] where missing (15 items)
3. Move to Today (10 high-priority items)

Approve? [Yes/No/Review individually]
```

**Step 8: Ambiguous Matches** - Batched by suggested area/project
```markdown
## Ambiguous Matches (10 items, 70-85%)

1. "Design review notes" (85%) → area="Amplitude"?
   [Approve / Different area / Keep in Inbox]

Quick response: "1 Approve, 2 Different area: Personal, ..."
```

**Step 9: Reference Items** - Present individually
```markdown
## Reference Item 1 of 5

**Item:** [Empty title]
**Notes:** "Customer success meeting - Q4 roadmap..."

**Options:**
1. **Migrate to Notion** (Recommended)
2. **Create project "Q4 Roadmap"**
3. **Convert to task** with title
4. **Delete**

Your choice: [1/2/3/4]
```

### Phase 4: Execute (Steps 10-12)

**Step 10: Batch Execute** - Use MCP tools efficiently
```python
move_tasks(task_uuids=[...], target_list="today")
add_tags(task_uuids=[...], tags=["AMPL"])
edit_task(task_uuid="...", area="Amplitude")
migrate_inbox_to_notion(block_id="...")
create_project(name="Q4 Roadmap", area="Amplitude")
```

**Step 11: Track Progress** - Update `session.md` incrementally
```markdown
## Progress
- Total: 446 | Processed: 100 | Remaining: 346

## Statistics
- High confidence: 70 (70%)
- Auto-applied: 65 (93% of high-confidence)

## Patterns Learned
- "Dashboard" + AMPL → area="Amplitude" (98% accuracy)
```

**Step 12: Summary Report**
```markdown
## Complete Summary

**Before:** Inbox: 446 | Amplitude: 120 tasks

**Processed:** 310 organized (70%), 45 migrated (10%), 91 kept (20%)

**After:** Inbox: 91 | Amplitude: 385 tasks (+265)

**New Projects:** Q4 Roadmap (12 tasks), Team Onboarding (8 tasks)
```

### Phase 5: Learn & Cleanup (Steps 13-14)

**Step 13: Propose Taxonomy Updates** - Based on patterns discovered
```markdown
## Proposed Taxonomy Updates

### New Project Keywords
"On-call": ["on-call", "oncall", "incident"] (25 occurrences, 100% accuracy)
"Dashboard": ["dashboard", "metrics"] (18 occurrences, 98% accuracy)

### Common Patterns
- Empty title + meeting notes → migrate_to_notion (95% approval, 12 samples)

Approve these updates? [Yes/No/Modify]
```

**CRITICAL**: Always get user approval before updating `personal-taxonomy.json`.

**Step 14: Cleanup** - Archive or delete temp folder
```bash
mv temp/inbox-processing temp/inbox-processing-2025-11-30-archive
# Or: rm -rf temp/inbox-processing
```

## Matching Strategy: LLM-Driven

**Core Principle**: Use Claude's semantic understanding, not hard-coded algorithms.

### Confidence Assessment

**High Confidence (90-100%)**
- Explicit area/project mentions
- Strong semantic relationship to existing structure
- Consistent with taxonomy patterns

Example: "Amplitude: Fix login bug" → 100%
- Explicit area mention + work tag "AMPL" + matches existing area

**Medium Confidence (70-89%)**
- Reasonable but ambiguous
- Could fit multiple areas/projects

Example: "Design review notes" → 85%
- Has work tag but generic term, needs confirmation

**Low Confidence (<70%)**
- No clear organizational fit
- Keep in inbox or ask individually

### Always Provide Reasoning
```
**Task:** "Dashboard analytics update"
**Confidence:** 95%
**Suggested:** area="Amplitude", project="Dashboard"
**Reasoning:**
- Work tag "AMPL" present
- "Dashboard" matches existing project
- Pattern seen 18 times with 98% accuracy
```

## Reference Item Detection

Use semantic understanding to identify reference items:

**Strong indicators:**
- Empty title + substantial notes (>50 words)
- Tagged "migrate to notion"
- URL-only content
- Titles: "Note:", "Idea:", "Reference:"

**Contextual analysis:**
- Informational rather than actionable
- Multi-paragraph notes without clear next actions
- Meeting summaries, research findings

### Four-Option Decision Tree

**1. Migrate to Notion (Most Common)**
- Preserve detailed notes as documentation
- Extract actionable items as separate Things3 tasks
- Best for: Meeting notes, research, planning docs

**2. Create Project + Extract Tasks**
- Content suggests multiple related actions
- Best for: Multi-step initiatives, campaigns

**3. Convert to Single Task**
- Add descriptive title to empty-title item
- Best for: Simple notes, reminders

**4. Delete**
- Outdated or no longer relevant

## User Interaction Patterns

### Minimizing Fatigue
- Auto-apply ≥90% confidence (reduces decisions by 60-70%)
- Batch similar questions together
- Provide quick response formats
- Show progress and remaining items
- **Target**: <20 interaction points for 400 items

### Four Interaction Types

1. **Batch Approval** (High confidence) - Group by area/project, simple Yes/No
2. **Batched Questions** (Medium confidence) - Numbered list, quick format
3. **Individual Questions** (References) - Full preview with 4 options
4. **Change Validation** (Before execution) - Before/After summary

## Learning & Taxonomy Updates

After each session, propose updates to `personal-taxonomy.json`:

**What to capture:**
1. **New project keywords** - Projects that appeared frequently with accuracy rates
2. **Common matching patterns** - Successful matches and user corrections
3. **Reference patterns** - What user consistently migrated/converted
4. **Workflow preferences** - Batch sizes and interaction patterns that worked

**Update Format:**
```json
{
  "things3": {
    "project_keywords": {
      "On-call": ["on-call", "incident", "alert"]
    },
    "learned_patterns": [{
      "pattern": "Dashboard + AMPL tag",
      "action": "area=Amplitude, project=Dashboard",
      "accuracy": 98,
      "sample_count": 18
    }]
  }
}
```

### Continuous Improvement
- **First session**: ~70% auto-apply
- **Second session**: ~80% auto-apply (learned patterns)
- **Ongoing**: Approach 85-90% auto-apply

## Best Practices

### Batch Sizing
- **First batch**: 50 items (establish patterns)
- **Subsequent**: 50-100 items (apply learned patterns)
- **Large inboxes (500+)**: Consider 2-3 sessions across days

### Performance
- Cache system inventory once per session
- Use batch MCP operations where possible
- Leverage LLM context window
- Take breaks after 100-150 items

### Error Recovery
- All actions logged in execution_log.md
- Can undo with Things3 MCP tools
- Session state saved (resume capability)
- Ask before destructive operations

## Troubleshooting

**Low auto-apply rate (<50%)**
- Inbox too diverse - manual review outliers
- Update taxonomy after session
- Consider lowering threshold to 85%

**Processing too slow**
- Reduce batch size to 25-50
- Skip reference reviews (mark for later)
- Focus on high-confidence first pass

**Incorrect matches**
- Review confidence reasoning
- Check taxonomy alignment
- Add corrections to learned patterns

**Session interruption**
- Resume from session.md
- Check execution_log.md for last action

## Integration

**things3-productivity**: MCP tool patterns, taxonomy, change validation
**notion-workflows**: Migration destinations, documentation structure
**productivity-integration**: Cross-system orchestration, review cycles

---

**Remember**: Trust LLM semantic understanding over hard-coded rules. Always get user approval before changes. Learn from each session to improve future processing.
