---
name: prd-generator
description: Generate comprehensive Product Requirements Documents with interactive discovery, progress tracking, and True Ralph Loop support for autonomous implementation. Use when user wants to (1) create a PRD for a new project/feature, (2) implement a PRD autonomously with fresh Claude sessions, (3) track implementation progress, (4) recover context after session loss. Creates docs/PRD.md and docs/PROGRESS.md.
---

# PRD Generator with True Ralph Loop

Generate production-quality PRDs through interactive discovery, then implement autonomously using fresh Claude sessions (True Ralph Loop).

## When to Use

- User says: "create PRD", "generate PRD", "new project", "write requirements", "plan feature"
- User wants to implement a PRD autonomously: "implement PRD", "start ralph loop", "autonomous mode"
- User needs to check progress: "PRD status", "what's left", "implementation progress"
- User returns after break/crash: "where was I", "resume", "continue from last session"

## Phase 1: Discovery (Interactive Q&A)

Before generating a PRD, gather comprehensive requirements through adaptive, **collaborative** questioning.

### Discovery Philosophy

**Be a thought partner, not an interrogator.**

Many users start with only a vague idea. Your job is to:
- Help them clarify and refine their thinking
- Offer concrete suggestions when they're unsure
- Validate rough ideas and help shape them
- Make "I don't know" a safe answer that leads somewhere useful

### Handling Uncertainty

When a user says "I don't know" or seems unsure:

1. **Offer 2-3 concrete options** to choose from
2. **Suggest what's typical** for similar projects
3. **Propose a sensible default** they can accept or modify
4. **Break big questions into smaller ones**

**Examples:**

User: "I'm not sure what tech stack to use"
→ "Based on [what you've described], here are three approaches that would work well:
   1. **React + Node.js** - Great for interactive UIs, huge ecosystem
   2. **Next.js** - Good if you need SEO, built-in API routes
   3. **SvelteKit** - Lighter weight, excellent performance
   What feels right, or should I explain the tradeoffs?"

User: "I don't know about scale requirements"
→ "Let's work backwards: Is this for personal use, a small team (<50 users), a growing startup (hundreds), or enterprise scale (thousands+)? For most new projects, starting with 'handles 100 concurrent users smoothly' is a reasonable baseline we can adjust."

User: "I have no idea what success looks like"
→ "That's normal at this stage! Let me suggest some metrics based on similar projects:
   - For a tool: 'Users complete [core task] in under 2 minutes'
   - For an app: 'Daily active users grows 10% week over week'
   - For an API: '99.9% uptime, <200ms p95 latency'
   Which of these resonates, or what matters most to you?"

### Question Flow

Ask questions ONE AT A TIME. Adapt based on answers. Be ready to suggest and guide.

**Problem Space (Start Here - Be Exploratory)**

1. **Tell me about what you're trying to build**
   - Start open-ended: "What's the idea?" or "What sparked this?"
   - If vague: "Paint me a picture - what does a user do with this?"
   - If stuck: Offer examples: "Is it more like [A], [B], or something different?"
   - Follow-up: "What's frustrating about how people handle this today?"

2. **Who will use this?**
   - If unsure: "Let's imagine your first 10 users - who are they?"
   - Offer personas: "Is this for developers, business users, consumers, or internal teams?"
   - Follow-up: "How technical are they? What tools do they already use?"

3. **How will you know this is working?**
   - If stuck: "If we check in 3 months from now, what would make you say 'this was worth it'?"
   - Offer metrics: "Would success be measured by time saved, revenue, user growth, or something else?"
   - Follow-up: "What's the minimum outcome that would make this a win?"

**Technical Context (Offer Guidance)**

4. **What's the tech landscape?**
   - If undecided: "I can suggest a stack based on your constraints. Any languages/frameworks you prefer or want to avoid?"
   - If existing code: "Point me to the repo or key files and I'll understand the patterns"
   - Proactively suggest: "Given [requirements], I'd recommend [X] because [reason]. Thoughts?"

5. **Existing code or greenfield?**
   - If existing: Explore architecture, patterns, conventions
   - If greenfield: "Great! We have flexibility. Any architectural patterns you like?"
   - Read key files to understand context before asking more questions

6. **Scale and performance?**
   - If unsure: "Let's estimate: how many users in month 1? Month 6? Year 1?"
   - Offer baselines: "For most new projects, designing for 1000 daily users is a safe start"
   - "Any hard requirements like 'must work offline' or 'real-time updates'?"

**Scope & Constraints (Help Define Boundaries)**

7. **What should we explicitly NOT build?**
   - If stuck: "What features would be 'nice to have later' vs 'must have now'?"
   - Suggest: "For a solid MVP, I'd suggest cutting [X] and [Y] for phase 2. Sound right?"
   - "What would be gold-plating vs essential?"

8. **Non-functional requirements?**
   - Offer checklist: "Let me run through some common ones:
     - Auth needed? (none / basic / OAuth / SSO)
     - Accessibility level? (basic / WCAG AA / AAA)
     - Compliance? (GDPR, HIPAA, SOC2, none)"
   - Suggest defaults: "For most projects, I'd recommend [X]. Any reason to go stricter?"

9. **External dependencies?**
   - Proactively identify: "Based on what you've described, you'll likely need [payment API / auth provider / etc]. Any preferences?"
   - "Any services you're already paying for that we should leverage?"

**Verification (Guide Toward Testability)**

10. **Testing strategy?**
    - If unsure: "I'll include a testing approach. Any existing test setup, or should I recommend one?"
    - Suggest: "For this type of project, I'd recommend [unit tests for core logic, integration tests for API, e2e for critical flows]"

11. **What does 'done' look like?**
    - If stuck: "Let's define the launch checklist together. What MUST work on day 1?"
    - Offer: "Typical launch criteria: [feature complete, tests pass, docs exist, deployed to prod]. Add or remove?"

12. **Edge cases and failure modes?**
    - Prompt thinking: "What's the worst thing that could happen? Data loss? Security breach? Downtime?"
    - Suggest: "Common edge cases for this type of project: [network failures, invalid input, concurrent edits]. I'll include handling for these."

### Brainstorming Mode

If the user has only a vague idea, switch to brainstorming mode:

1. **Explore the problem space**: "Let's forget solutions for a moment. Tell me about the frustration or opportunity you've noticed."

2. **Generate options**: "Based on that, here are 3 different products you could build: [A], [B], [C]. Which excites you most?"

3. **Refine iteratively**: "Interesting! Let's explore [choice]. What if it also did [X]? Or would that be too much?"

4. **Validate direction**: "So the core idea is [summary]. Before we go deeper, does that capture it?"

### Advanced Discovery Techniques

**Five Whys** - When the problem is unclear, keep asking "why" to find the root:
```
User: "I need a dashboard"
→ Why? "To see metrics"
→ Why do you need to see metrics? "To know if campaigns are working"
→ Why do you need to know that? "To stop wasting money on bad campaigns"
→ ROOT: The real need is campaign ROI visibility, not "a dashboard"
```

**Ask About Past Behavior** - People remember the past better than they predict the future:
- Instead of: "Would you use a feature that does X?"
- Ask: "Tell me about the last time you tried to do X. What happened? Where did you get stuck?"

**Jobs to Be Done (JTBD)** - Frame requirements around the "job" users hire the product to do:
- Template: "When [situation], I want to [motivation], so I can [outcome]"
- Example: "When I'm reviewing PRs late at night, I want to quickly see what changed, so I can approve without missing bugs"

**Opportunity Solution Tree** - Connect outcomes to opportunities to solutions:
```
Outcome: Increase user retention
  └── Opportunity: Users forget to return
        └── Solution A: Email reminders
        └── Solution B: Mobile push notifications
  └── Opportunity: Users don't see value quickly
        └── Solution A: Improved onboarding
        └── Solution B: Quick wins in first session
```

**Pre-Mortem Technique** (Shreyas Doshi) - Before building, imagine it failed:
- "It's 6 months from now and this project was a disaster. What went wrong?"
- Forces realistic risk assessment upfront

### Encouraging Responses

Use encouraging language throughout:

- "That's a great starting point - let's build on it"
- "Good instinct. Here's how we might refine that..."
- "That's actually a common challenge. Here's what usually works..."
- "Perfect, that tells me a lot. Now I'm curious about..."
- "Not sure? No problem - let me offer some options..."

### Completeness Check

Before generating PRD, verify each section has sufficient detail:

| Section | Required Info |
|---------|--------------|
| Problem | Clear pain points, user impact |
| Users | Persona, technical level, workflow |
| Success | Measurable metrics |
| Tech | Stack, architecture decisions |
| Scope | In/out of scope explicit |
| Testing | Strategy defined |
| Done | Acceptance criteria clear |

If any section is sparse, ask targeted follow-ups.

## Phase 2: PRD Generation

Once discovery is complete, generate `docs/PRD.md`:

```bash
mkdir -p docs
```

Use the template in [`templates/PRD-TEMPLATE.md`](templates/PRD-TEMPLATE.md).

**Critical PRD Requirements:**
- Every task must have a checkbox: `- [ ] Task description`
- Group tasks into numbered phases (Phase 1, Phase 2, etc.)
- Each task ID format: `Task X.Y` (e.g., Task 1.1, Task 2.3)
- Include testable acceptance criteria for each user story
- Explicit "Out of Scope" section to prevent scope creep

## Phase 3: PROGRESS.md Creation

Immediately after PRD, create `docs/PROGRESS.md`:

Use the template in [`templates/PROGRESS-TEMPLATE.md`](templates/PROGRESS-TEMPLATE.md).

**Critical PROGRESS.md Requirements:**
- "Quick Context" section at top for instant orientation
- Current task clearly identified
- Recovery instructions for context loss scenarios
- Session history log for debugging

## Phase 4: True Ralph Loop (Autonomous Implementation)

### Why "True Ralph"?

The official Anthropic Ralph plugin uses a Stop hook that keeps Claude in the SAME session. This causes:
- Context rot from compaction over time
- "Ralph Wiggum state" - confusion from accumulated noise
- Degraded output quality after many iterations

**True Ralph** (Geoffrey Huntley's original vision) spawns FRESH Claude sessions:
- Each iteration has full context capacity
- No accumulated noise from previous attempts
- State persists only through files (PRD.md, PROGRESS.md, git)

### Mode 1: External Script (Recommended)

When user wants to start Ralph loop, explain clearly:

```
True Ralph requires fresh Claude sessions OUTSIDE of this conversation.
This cannot run from within Claude - you need to run it from your terminal.

1. Open a NEW terminal window

2. Navigate to your project:
   cd [PROJECT_PATH]

3. Run the True Ralph Loop:
   ~/.claude/plugins/indrasvat-skills/skills/prd-generator/scripts/true-ralph-loop.sh -n [ITERATIONS]

4. Monitor progress:
   - Watch terminal output
   - Check docs/PROGRESS.md
   - View logs in .ralph/logs/

5. Stop gracefully: Ctrl+C
```

Before handing off:
1. Validate docs/PRD.md exists and has tasks
2. Ensure docs/PROGRESS.md exists
3. Verify git repo if applicable
4. Output the exact command to run

### Mode 2: tmux Detach

If user prefers tmux and it's available:

```bash
# Check tmux availability
command -v tmux &>/dev/null || { echo "tmux not installed"; exit 1; }

# Get project name for session naming
PROJECT_NAME=$(basename "$(pwd)" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Spawn detached session
tmux new-session -d -s "ralph-${PROJECT_NAME}" \
  "~/.claude/plugins/indrasvat-skills/skills/prd-generator/scripts/true-ralph-loop.sh -n [ITERATIONS]"

echo "Ralph loop started in tmux session: ralph-${PROJECT_NAME}"
echo "Attach: tmux attach -t ralph-${PROJECT_NAME}"
echo "Kill:   tmux kill-session -t ralph-${PROJECT_NAME}"
```

## Phase 5: Status Check

When user asks about progress:

```bash
echo "=== PRD Status ==="
if [ -f docs/PRD.md ]; then
    TOTAL=$(grep -c '^\- \[' docs/PRD.md 2>/dev/null || echo "0")
    DONE=$(grep -c '^\- \[x\]' docs/PRD.md 2>/dev/null || echo "0")
    PENDING=$(grep -c '^\- \[ \]' docs/PRD.md 2>/dev/null || echo "0")
    echo "Total tasks:     $TOTAL"
    echo "Completed:       $DONE"
    echo "Pending:         $PENDING"
    if [ "$TOTAL" -gt 0 ]; then
        PCT=$((DONE * 100 / TOTAL))
        echo "Progress:        $PCT%"
    fi
else
    echo "No PRD found at docs/PRD.md"
fi

echo ""
echo "=== Current State ==="
if [ -f docs/PROGRESS.md ]; then
    head -25 docs/PROGRESS.md
else
    echo "No PROGRESS.md found"
fi
```

## Phase 6: Context Recovery

When user returns after a break, crash, or context loss:

1. **Read PROGRESS.md first** - contains quick context and current task
2. **Read PRD.md** - understand full requirements
3. **Check git log** - see recent commits
4. **Check git status** - see uncommitted changes

```bash
echo "=== Recovering Context ==="
echo ""
if [ -f docs/PROGRESS.md ]; then
    echo "Quick context from PROGRESS.md:"
    head -20 docs/PROGRESS.md
fi

echo ""
echo "Recent git activity:"
git log --oneline -5 2>/dev/null || echo "Not a git repo"

echo ""
echo "Uncommitted changes:"
git status -s 2>/dev/null || echo "Not a git repo"
```

Then summarize:
- Current phase and task
- What was last completed
- What should be done next

## Best Practices

### PRD Writing
- Use checkboxes (`- [ ]`) for ALL actionable items
- Group tasks logically into phases
- Each phase should be independently deployable
- Include "Out of Scope" to prevent creep
- Make acceptance criteria testable

### PROGRESS.md Updates
- Update after EVERY task completion
- Move next pending task to "In Progress"
- Log blockers immediately
- Include relevant file paths and commit hashes

### Ralph Loop Success
- Set realistic `--max-iterations` (start with 10-15)
- Ensure PRD tasks are granular (1-2 hour chunks)
- Each task should be independently verifiable
- Include test commands in PRD when applicable

## Troubleshooting

### "Claude keeps doing the same thing"
- Check PROGRESS.md - is the current task clearly marked?
- Regenerate PROGRESS.md with explicit task state
- Verify PRD tasks are actually checkboxed

### "Ralph loop stops unexpectedly"
- Check `.ralph/logs/` for the last iteration log
- Verify `claude` CLI is working: `claude --version`
- Check for syntax errors in PROGRESS.md

### "Lost context after compaction"
- This is normal - use PROGRESS.md for recovery
- Run context recovery steps above
- The whole point of True Ralph is to handle this gracefully

## See Also

- [`templates/PRD-TEMPLATE.md`](templates/PRD-TEMPLATE.md) - Full PRD template
- [`templates/PROGRESS-TEMPLATE.md`](templates/PROGRESS-TEMPLATE.md) - Full progress template
- [`scripts/true-ralph-loop.sh`](scripts/true-ralph-loop.sh) - The True Ralph Loop script
- [`references/discovery-questions.md`](references/discovery-questions.md) - Extended question bank
