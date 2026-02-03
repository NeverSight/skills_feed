---
name: observability
description: "Logs AI thoughts and decisions for human observability. Applies continuously throughout all tasks to maintain transparency."
---

# Observability Skill

Maintain transparent, human-readable logs of AI decision-making process.

## Workspace Mode Note

When running in workspace mode, log to `.aha-loop/logs/ai-thoughts.md` instead of `logs/ai-thoughts.md`.
The orchestrator will provide the actual paths in the prompt context.

---

## The Job

1. Log significant thoughts and decisions to `logs/ai-thoughts.md`
2. Provide visibility into AI reasoning process
3. Create anchors for humans to understand what's happening
4. Never hide failures or uncertainty

---

## When to Log

### Always Log

- **Starting a new task** - What am I about to do and why
- **Major decisions** - When choosing between approaches
- **Unexpected findings** - Something surprising or important
- **Errors and recovery** - What went wrong and how I'm handling it
- **Completion** - What was accomplished

### Optional Log (Detailed Level)

- Intermediate steps
- Research findings
- Minor decisions
- Progress updates

---

## Log Format

Append to `logs/ai-thoughts.md`:

```markdown
## 2026-01-29 14:30:00 | Task: PRD-003 | Phase: Research

### Context
I'm researching authentication strategies for the web app. This is critical 
because it affects security architecture and user experience.

### Inner Thoughts
The vision mentions "simple" and "quick to use". Traditional username/password 
might add friction. Considering passwordless options but need to evaluate 
complexity tradeoffs.

### Decision Point
- Considering: Traditional email/password
- Considering: Magic link (passwordless)
- Considering: OAuth only (Google/GitHub)
- **Chosen:** Magic link with OAuth fallback
- **Reason:** Aligns with "simple" goal, reduces password fatigue, 
  OAuth provides familiar alternative

### Current Progress
- [x] Read vision requirements
- [x] Research auth options
- [ ] Prototype magic link flow
- [ ] Evaluate email service options

### Observations
- Magic link requires reliable email delivery
- Need to consider rate limiting to prevent abuse
- Session duration is important for UX

### Next Action
Will research email service providers (Resend, SendGrid) and evaluate 
their free tiers since budget constraint mentioned "no paid APIs".

---
```

---

## Log Levels

Configure in `config.json`:

### Minimal
- Task start/end only
- Major errors

### Normal (Default)
- All major decisions
- Phase transitions
- Errors and recovery

### Detailed
- Everything above
- Intermediate thoughts
- Research notes
- Minor decisions

---

## Thought Categories

### Inner Monologue
Express your actual reasoning:
- "I'm uncertain about X because..."
- "This seems risky because..."
- "I'm choosing Y over Z because..."
- "I notice that..."

### Decision Points
When facing choices:
```markdown
### Decision Point
- Considering: [Option A] - [pros/cons]
- Considering: [Option B] - [pros/cons]
- **Chosen:** [Option]
- **Reason:** [Why]
- **Tradeoffs:** [What we're giving up]
```

### Uncertainty
Be honest about what you don't know:
```markdown
### Uncertainty
I'm not 100% sure about [X]. My current assumption is [Y] because [Z].
If this proves wrong, I'll need to [fallback plan].
```

### Errors
When things go wrong:
```markdown
### Error Encountered
**What happened:** [Description]
**Why:** [Root cause if known]
**Impact:** [What this affects]
**Recovery:** [How I'm handling it]
```

---

## Principles

### Be Transparent
- Don't hide uncertainty
- Don't pretend to know what you don't
- Admit mistakes openly

### Be Useful
- Logs should help humans understand
- Avoid jargon without explanation
- Provide context

### Be Honest
- Express genuine reasoning, not performance
- Include doubts and concerns
- Note when guessing vs. knowing

### Be Concise
- Important details only
- No filler text
- Structured for scanning

---

## Integration

### At Task Start
```markdown
## [timestamp] | Task: [id] | Phase: Starting

### Context
[What I'm about to do]

### Approach
[How I plan to tackle it]

### Potential Concerns
[What might go wrong]
```

### At Decision Points
```markdown
### Decision Point
[Structured decision format]
```

### At Task End
```markdown
## [timestamp] | Task: [id] | Phase: Complete

### Summary
[What was accomplished]

### Key Decisions Made
- [Decision 1]
- [Decision 2]

### Learnings
[What I learned that might be useful later]

### Concerns for Future
[Any issues to watch for]
```

---

## Example: Full Task Log

```markdown
## 2026-01-29 10:00:00 | Task: PRD-001 | Phase: Starting

### Context
Beginning the project scaffolding PRD. This sets up the foundation for 
the entire project, so I need to be careful about initial decisions.

### Approach
1. First, review the architecture document for tech stack
2. Initialize the project with chosen tools
3. Set up basic structure
4. Configure development environment

### Potential Concerns
- Version compatibility between dependencies
- Getting the directory structure right from the start

---

## 2026-01-29 10:15:00 | Task: PRD-001 | Phase: Research

### Inner Thoughts
The architecture specifies Rust + Axum. I should verify I'm using the 
latest stable versions. Let me check crates.io...

### Observations
- Axum 0.7.4 is latest (released 2 weeks ago, stable)
- Tokio 1.35 is latest
- Should use workspace structure for future modularity

---

## 2026-01-29 10:30:00 | Task: PRD-001 | Phase: Implementation

### Decision Point
- Considering: Single crate structure
- Considering: Workspace with multiple crates
- **Chosen:** Workspace structure
- **Reason:** Project will likely grow, easier to refactor now than later

### Progress
- [x] Created Cargo.toml with workspace
- [x] Added main crate
- [ ] Add configuration
- [ ] Add basic error handling

---

## 2026-01-29 11:00:00 | Task: PRD-001 | Phase: Complete

### Summary
Successfully set up Rust project with Axum 0.7.4, configured workspace,
added basic structure with src/main.rs entry point.

### Key Decisions Made
- Workspace structure for scalability
- Tokio multi-threaded runtime
- Tracing for logging

### Learnings
- Axum 0.7 changed some APIs from 0.6, needed to use new Router syntax

### Files Created
- Cargo.toml
- src/main.rs
- src/lib.rs

---
```

---

## Mindset

**You are thinking out loud for human benefit.**

Your logs should read like a competent colleague explaining their work:
- Clear reasoning
- Honest about uncertainty
- Proactive about potential issues
- Documenting for future reference

**Remember:** Humans will read these logs to understand what you did and why. Make their job easy.
