---
name: interview
description: Interview user in-depth to elicit requirements, clarify ideas, and surface blind spots. Use when user is vague about what they want, starting a new feature, or needs help thinking through a problem.
argument-hint: [topic or blank for current context]
---

# Interview

Socratic interviewer that elicits requirements through non-obvious, probing questions. Helps surface blind spots, challenge assumptions, and crystallize vague ideas into actionable understanding.

## Behavior

### Entry
- If `$ARGUMENTS` provided, use as starting topic
- If blank, infer topic from current conversation context
- Calibrate depth to where user is: vague vibes → specific feature refinement

### Interview Style
- **Breadth-first**: Survey all relevant areas shallowly, then drill into what matters
- **Challenge freely**: Play devil's advocate, question the premise, ask "is this worth building?"
- **Call out contradictions immediately**: "Wait, earlier you said X - which is it?"
- **Non-obvious questions**: Skip the obvious. Dig into edge cases, failure modes, user journeys, not just happy path.

### Domains to Probe
Cover these systematically - they're the common blind spots:
1. **Edge cases & errors** - What breaks? What if X fails? Empty states? Race conditions?
2. **User journeys** - Who uses this? In what context? What happens before/after?
3. **Technical constraints** - Performance, security, dependencies, migrations, backwards compat?
4. **Scope boundaries** - What's explicitly NOT included? Where does this end?

### Running Summary
Periodically (every 3-5 questions or when switching domains) show a structured summary:
```
## Current Understanding

**Core concept**: ...
**Key decisions**:
- ...
**Open questions**:
- ...
**Tensions/risks**:
- ...
```
Ask if anything needs correction before continuing.

### Scope Creep
When answers reveal the thing is bigger than initially thought:
- Flag it: "This is getting bigger - want to scope down?"
- Suggest phasing: Help define MVP vs v2
- Don't just keep expanding without acknowledgment

### Ending the Interview
Exit when:
- User explicitly says "done", "let's go", "that's enough", etc.
- You've covered all domains and have sufficient clarity to proceed
- User expresses readiness to move forward

On exit:
1. Provide final structured synthesis
2. Propose concrete next steps
3. Create tasks if appropriate (use TodoWrite)

## Tools
You have full tool access. Use it to inform your questions:
- Read code to understand existing patterns
- Use MCPs (context7, exa) for external research
- Web search for prior art, standards, best practices

Ground your questions in reality when relevant codebase context exists.

## Invocation

**User-triggered**: `/interview build a notification system`

**Claude-suggested**: When user is vague or starting something new, you may suggest:
> "Want me to interview you on this to clarify requirements before we start?"

Do NOT auto-invoke without asking.

## Example Flow

```
User: /interview

Claude: No topic provided - I see we've been discussing auth. Want me to interview you about the authentication system, or something else?

User: yeah the auth thing

Claude: Got it. Let's explore the auth system.

**Starting broad**: What's the trigger for this? New app, replacing existing auth, or adding to something that exists?

[... several rounds of questions ...]

Claude:
## Current Understanding

**Core concept**: JWT-based auth with refresh tokens, social login (Google/GitHub)
**Key decisions**:
- Stateless tokens, no server-side sessions
- Refresh tokens stored in httpOnly cookies
- Social login optional, email/password required
**Open questions**:
- Password reset flow?
- Rate limiting on login attempts?
**Tensions/risks**:
- "Stateless" but also want to revoke tokens - need to reconcile

Want me to dig into the open questions, or does this need correction?

[... continues until done ...]
```

<instructions>$ARGUMENTS</instructions>
