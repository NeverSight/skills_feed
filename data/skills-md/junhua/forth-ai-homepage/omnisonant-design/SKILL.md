---
name: omnisonant-design
description: Product design guide for Omnisonant - omni-channel voice agents that replace call center staff. Use when designing, reviewing, or improving Omnisonant interfaces, voice agent behaviors, or architecture.
---

# Omnisonant Design Guide

**Product**: Omnisonant — Every channel, one voice.

**Tagline**: AI voice agents that handle calls so humans don't have to.

**Repo**: `git@github.com:Forth-AI/omnisonant.git`

**Trigger**: When designing, reviewing, or improving Omnisonant features, voice agent behaviors, or architecture.

---

## 1. The Paradigm Shift

### Traditional Call Center Model
```
Customer calls → IVR maze → Hold music → Human agent → Manual CRM update
                    ↓           ↓            ↓               ↓
               Frustrating   Expensive    Inconsistent   Error-prone
```

**Problems**:
- Cost: $15-25/hour per agent
- Availability: Limited hours, timezone constraints
- Consistency: Agent quality varies
- Scale: Hiring/training bottleneck
- Data: Manual entry, lost context

### Omnisonant Model
```
Customer calls → Voice agent → Instant resolution → Automatic CRM update
                     ↓               ↓                    ↓
                24/7 ready    Perfectly consistent    Zero manual work
```

**Value**:
- Cost: $0.10-0.20 per call (95%+ savings)
- Availability: 24/7/365, any timezone
- Consistency: Same quality every time
- Scale: Infinite parallel calls
- Data: Automatic logging, full transcripts

---

## 2. Target Audiences

### Primary: SMB Owners

**Profile**: Small business owners who hate phone work

| Vertical | Pain | Voice Agent Use |
|----------|------|-----------------|
| **Dental/Medical clinics** | Staff on phones all day | Appointment confirmation, rescheduling |
| **Real estate agencies** | Leads go cold while agents are busy | Lead qualification, showing scheduling |
| **E-commerce** | Can't afford 24/7 support | Order status, returns, basic support |
| **Professional services** | Missed calls = missed revenue | Intake calls, appointment booking |
| **Restaurants** | Reservations interrupt service | Booking, waitlist management |

**Buying motivation**: "I want to fire my phones"

**Design implication**: Must be self-service, no technical setup required.

### Secondary: Voice AI Resellers/Agencies

**Profile**: Agencies building voice solutions for clients

| Type | Need | Omnisonant Value |
|------|------|------------------|
| **Marketing agencies** | Add voice to service offering | White-label, easy deployment |
| **IT consultants** | Modernize client operations | Proven platform, fast implementation |
| **BPO companies** | Reduce headcount, increase margin | Hybrid human+AI workforce |

**Buying motivation**: "I want to sell this to my clients"

**Design implication**: Multi-tenant, white-label capable, reseller dashboard.

---

## 3. Three Core Use Cases

### Use Case 1: Appointment Scheduling (Outbound)

**Replaces**: Staff calling to confirm/reschedule appointments

**Example vertical**: Dental clinic

**Flow**:
```
Agent calls patient → Confirms tomorrow's appointment →
  ✓ Confirmed: "Great, see you at 2pm"
  ↻ Reschedule: Opens calendar, finds slot, books
  ✕ Cancel: Marks cancelled, offers future booking
→ Updates calendar automatically
```

**Voice Agent Script Pattern**:
```
"Hi, this is Sarah from [Business Name].
I'm calling to confirm your appointment tomorrow at [time] with [provider].
Can you make it?"

[If yes] "Great! We'll see you then. Is there anything you need before your visit?"

[If reschedule] "No problem! Let me check what we have available.
How about [alternative 1] or [alternative 2]?"

[If cancel] "I understand. Would you like me to book a future appointment,
or shall I have someone call you later?"
```

**Key metrics**:
- Confirmation rate: Target 80%+
- Reschedule rate: Track, optimize
- No-show reduction: Target 50%+
- Call duration: Target <2 min

**Design requirements**:
- Calendar integration (Google, Outlook, practice management)
- Smart slot suggestion (based on availability + preferences)
- Reminder confirmation (SMS after call)
- Retry logic (voicemail, callback attempts)

---

### Use Case 2: Lead Qualification (Outbound)

**Replaces**: SDRs making initial qualification calls

**Example vertical**: Real estate

**Flow**:
```
Lead submits form → Agent calls within 5 minutes →
  Qualifies: Budget, timeline, preferences →
    ✓ Hot lead: Books showing with human agent
    ~ Warm lead: Adds to nurture sequence
    ✕ Cold lead: Marks as not ready
→ Updates CRM with full notes
```

**BANT Qualification Script**:
```
"Hi [Name], this is Alex from [Agency].
You inquired about homes in [area]. Do you have a few minutes to chat?"

[Budget] "What price range are you looking at?"

[Authority] "Will anyone else be involved in the decision?"

[Need] "What's prompting your move? More space, new job, investment?"

[Timeline] "When are you hoping to move by?"

[If qualified] "Based on what you've told me, I think [Agent Name]
would be perfect to show you some properties. They're available
[time slots]. Which works for you?"
```

**Key metrics**:
- Contact rate: Target 60%+
- Qualification completion: Target 70%+
- Lead-to-meeting conversion: Target 30%+
- Speed to lead: Target <5 min

**Design requirements**:
- CRM integration (Salesforce, HubSpot, etc.)
- Lead scoring based on answers
- Intelligent routing to human agents
- A/B testing for scripts
- Time-of-day optimization

---

### Use Case 3: Customer Support (Inbound)

**Replaces**: Tier-1 support agents handling common queries

**Example vertical**: E-commerce

**Flow**:
```
Customer calls → Agent identifies (phone/order#) →
  📦 Order status: Pulls from system, provides update
  ↩️ Return request: Creates RMA, sends label
  ❓ General question: Answers from knowledge base
  ⚠️ Complex issue: Escalates to human
→ Logs interaction, updates ticket
```

**Support Script Pattern**:
```
"Thank you for calling [Company]. This is your AI assistant.
How can I help you today?"

[Order status] "I'd be happy to check on your order.
Can I get your order number or the email address on the account?"
→ "I found your order. It shipped on [date] and should arrive by [date].
Would you like me to text you the tracking number?"

[Return] "I can help you start a return. Which item would you like to return?"
→ "I've created a return label for you. It's being sent to [email].
Is there anything else I can help with?"

[Escalation] "I want to make sure you get the best help for this.
Let me connect you with a specialist. Please hold for just a moment."
```

**Key metrics**:
- Resolution rate (no human needed): Target 70%+
- Customer satisfaction: Target 4+/5
- Average handle time: Target <3 min
- Escalation rate: Target <30%

**Design requirements**:
- Order system integration
- Return/refund workflow automation
- Knowledge base for FAQs
- Seamless escalation to human
- Post-call survey option

---

## 4. Voice Agent Design Principles

### Principle 1: Sound Human, Be Honest

```
Right: "Hi, this is Sarah, an AI assistant calling from..."
Wrong: Pretending to be human without disclosure

Right: Natural speech patterns, appropriate pauses
Wrong: Robotic cadence, unnatural phrasing
```

**Why**: Trust requires transparency. Deception backfires.

### Principle 2: Graceful Interruption Handling

```
Right: Stop talking when customer speaks, acknowledge, respond
Wrong: Keep talking over customer, ignore interruption

Right: "Oh, go ahead!" → listens → responds to what they said
Wrong: "Please wait for me to finish"
```

**Why**: Natural conversation requires turn-taking.

### Principle 3: Fast and Focused

```
Right: Get to the point, respect their time
Wrong: Long introductions, excessive pleasantries

Right: "Hi, this is Sarah from Bright Smile confirming your appointment tomorrow at 2pm. Can you make it?"
Wrong: "Hello! How are you doing today? I hope you're having a wonderful day! I'm calling from..."
```

**Why**: People hate phone calls. Make them short.

### Principle 4: Recover Gracefully

```
Right: "I didn't quite catch that. Could you repeat the date?"
Wrong: "Error. Invalid input. Please try again."

Right: "Hmm, I'm having trouble finding that order. Let me connect you with someone who can help."
Wrong: [Silence] or [Hang up]
```

**Why**: Errors happen. Recovery maintains trust.

### Principle 5: Confirm Before Acting

```
Right: "So I'll book you for Thursday at 3pm with Dr. Chen. Does that sound right?"
Wrong: "Done. Goodbye." [Hangs up]

Right: Wait for confirmation before finalizing
Wrong: Assume and execute without verification
```

**Why**: Mistakes are costly. Confirmation is cheap.

### Principle 6: End with Clear Next Steps

```
Right: "You'll get a text confirmation in a moment. Is there anything else?"
Wrong: "Okay, bye."

Right: Tell them what happens next
Wrong: Leave them wondering
```

**Why**: Closure creates confidence.

---

## 5. Voice & Personality Guidelines

### Voice Selection Criteria

| Factor | Consideration |
|--------|---------------|
| **Gender** | Match brand perception; test with audience |
| **Accent** | Match target market; consider regional preferences |
| **Tone** | Professional for B2B, friendly for B2C |
| **Speed** | Slightly slower than normal speech (clarity) |
| **Energy** | Match context (upbeat for sales, calm for support) |

### Personality Traits

**For appointment scheduling**:
- Friendly, efficient, respectful of time
- "I know you're busy, so I'll be quick"

**For lead qualification**:
- Curious, engaged, consultative
- "Tell me more about what you're looking for"

**For customer support**:
- Patient, helpful, solution-oriented
- "Let me take care of that for you"

### Things Voice Agents Should NEVER Do

- Pretend to be human when directly asked
- Get frustrated or impatient
- Argue with the customer
- Share information about other customers
- Make promises outside their authority
- Continue calling after "stop calling me"

---

## 6. Technical Architecture Principles

### Dual Pipeline Support

| Pipeline | Use Case | Tradeoffs |
|----------|----------|-----------|
| **Vapi + Twilio** | Production phone calls | Higher latency (~500ms), real phone numbers, proven scale |
| **OpenAI Realtime** | Web demo, premium UX | Lower latency (~200ms), browser-based, cutting-edge |

**Design implication**: Abstract voice pipeline so agents work on either.

### Latency Budget

```
Ideal conversation turn:
  Customer speaks     → 500ms → Agent responds

Acceptable:
  Customer speaks     → 800ms → Agent responds

Frustrating:
  Customer speaks     → 1500ms+ → Agent responds
```

**Design implication**: Every millisecond matters. Optimize ruthlessly.

### Tool Execution Model

```
Customer: "What's the status of my order?"
    ↓
Agent: [Thinking] "Let me check that for you"
    ↓
Tool call: lookupOrder({ phone: "+1..." })
    ↓
Agent: "Your order shipped yesterday and should arrive Friday."
```

**Design implication**: Tools must be fast (<1s) and reliable.

### Fallback Strategy

```
Level 1: Agent handles completely
Level 2: Agent + tool call
Level 3: Agent transfers to human
Level 4: Agent takes message for callback
```

**Design implication**: Never dead-end. Always a path forward.

---

## 7. Value Proposition Checklist

Every feature must deliver on at least one:

### ✅ Cost Reduction
- [ ] Does this reduce cost per call?
- [ ] Does this reduce need for human agents?
- [ ] Is ROI measurable and significant?

### ✅ Availability Improvement
- [ ] Does this extend service hours?
- [ ] Does this handle more concurrent calls?
- [ ] Does this reduce wait times?

### ✅ Consistency Improvement
- [ ] Does this ensure same quality every call?
- [ ] Does this reduce human error?
- [ ] Does this improve compliance?

### ✅ Scale Enablement
- [ ] Does this remove hiring bottleneck?
- [ ] Does this handle demand spikes?
- [ ] Does this expand geographic reach?

**Red flags** (features that don't fit):
- "Requires human review for every call" ❌
- "Only works during business hours" ❌
- "Needs custom development per client" ❌
- "Improves metrics but costs more" ❌

---

## 8. Interface Patterns

### Admin Dashboard

**Primary actions**:
1. View active calls (live monitoring)
2. Review call history + transcripts
3. Configure voice agents
4. Manage campaigns (outbound)
5. View analytics

**Key UX requirements**:
- Real-time call status visibility
- One-click access to any call transcript
- Easy agent script editing
- Clear performance metrics

### Agent Builder

**Primary actions**:
1. Define agent persona (name, voice, personality)
2. Set greeting and conversation flow
3. Configure available tools
4. Test with sample calls
5. Deploy to phone number

**Key UX requirements**:
- Natural language prompt editing
- Voice preview (hear before deploy)
- Sandbox testing environment
- A/B testing support

### Campaign Manager (Outbound)

**Primary actions**:
1. Upload/select contact list
2. Choose agent and script
3. Set calling schedule and rules
4. Monitor progress
5. Review results

**Key UX requirements**:
- Bulk contact management
- Scheduling controls (time windows, timezone handling)
- Real-time progress dashboard
- Export results to CRM

### Web Demo Interface

**Primary actions**:
1. Click to start call
2. Speak with agent
3. See live transcript
4. Experience the product

**Key UX requirements**:
- One-click to start (no signup for demo)
- Visual audio feedback
- Live transcript display
- Mobile-friendly

---

## 9. Anti-Patterns (Omnisonant-Specific)

### "Sounds Like a Robot"
**Symptom**: Unnatural speech, no personality, mechanical responses.
**Fix**: Better prompts, voice selection, natural language patterns.

### "IVR in Disguise"
**Symptom**: "Press 1 for...", rigid menu trees, no natural conversation.
**Fix**: Open-ended listening, intent detection, flexible responses.

### "Infinite Hold"
**Symptom**: Can't reach human when needed, escalation fails.
**Fix**: Clear escalation paths, graceful handoffs, callback option.

### "Amnesia Agent"
**Symptom**: Doesn't remember what was said earlier in call.
**Fix**: Proper context management, conversation memory.

### "Over-Promising Agent"
**Symptom**: Agent commits to things it can't deliver.
**Fix**: Constrain agent authority, confirm before committing.

### "The Interrogator"
**Symptom**: Feels like a survey, too many questions, no empathy.
**Fix**: Conversational flow, acknowledge answers, show understanding.

### "Uncanny Valley"
**Symptom**: Too human-like in a way that's creepy.
**Fix**: Honest about being AI, consistent persona, appropriate boundaries.

---

## 10. Competitive Positioning

### vs. Traditional Call Centers

| Dimension | Call Center | Omnisonant |
|-----------|-------------|------------|
| Cost per call | $5-15 | $0.10-0.20 |
| Availability | 8-12 hours | 24/7 |
| Consistency | Variable | Perfect |
| Scale time | Weeks (hiring) | Minutes |
| Data capture | Manual | Automatic |

**Omnisonant advantage**: 95%+ cost reduction with better consistency.

### vs. IVR Systems

| Dimension | IVR | Omnisonant |
|-----------|-----|------------|
| User experience | "Press 1 for..." | Natural conversation |
| Resolution rate | Low (frustration) | High (actual help) |
| Flexibility | Rigid menus | Open-ended |
| Updates | IT project | Prompt change |

**Omnisonant advantage**: People hate IVR. They tolerate or even enjoy good AI.

### vs. Vapi (Direct)

| Dimension | Vapi DIY | Omnisonant |
|-----------|----------|------------|
| Target | Developers | Business owners |
| Setup | Build it yourself | Ready-to-use |
| Templates | Generic | Industry-specific |
| Integrations | You build | Pre-built |

**Omnisonant advantage**: Vapi is infrastructure. Omnisonant is solution.

### vs. Other Voice AI Platforms

| Dimension | Others | Omnisonant |
|-----------|--------|------------|
| Multi-channel | Often single | Phone + web + more |
| White-label | Limited | Built for resellers |
| Pricing | Complex | Simple per-minute |

**Omnisonant advantage**: "Omni" in the name is the promise.

---

## 11. Review Checklist

When reviewing Omnisonant designs:

### Voice Quality
- [ ] Does it sound natural?
- [ ] Is there appropriate personality?
- [ ] Are interruptions handled well?
- [ ] Is latency acceptable (<800ms)?

### Conversation Quality
- [ ] Does it get to the point quickly?
- [ ] Does it confirm before acting?
- [ ] Does it recover from errors gracefully?
- [ ] Does it end with clear next steps?

### Business Value
- [ ] Does this reduce cost per call?
- [ ] Does this extend availability?
- [ ] Does this improve consistency?
- [ ] Does this enable scale?

### Integration Quality
- [ ] Does data flow to CRM automatically?
- [ ] Are actions executed in real systems?
- [ ] Is escalation to humans seamless?
- [ ] Are transcripts accessible?

### User Experience (Admin)
- [ ] Can they set up without technical help?
- [ ] Can they monitor calls in real-time?
- [ ] Can they make changes without coding?
- [ ] Can they measure ROI?

---

## 12. Key Metrics

### Call Quality
- **Resolution rate**: Calls resolved without human (Target: 70%+)
- **Customer satisfaction**: Post-call rating (Target: 4+/5)
- **Average handle time**: Call duration (Target: <3 min)
- **Error rate**: Calls with issues (Target: <5%)

### Business Impact
- **Cost per call**: All-in cost (Target: <$0.25)
- **Conversion rate**: Leads converted, appointments booked (varies)
- **ROI**: Savings vs. human agents (Target: 10x+)

### Technical Performance
- **Latency**: Time to first response (Target: <500ms)
- **Uptime**: System availability (Target: 99.9%+)
- **Accuracy**: Speech recognition accuracy (Target: 95%+)

---

## 13. Feature Prioritization Framework

### Must Have (P0)
- Core voice conversation capability
- At least one use case working end-to-end
- Basic analytics (calls, duration, outcomes)
- Phone number provisioning

### Should Have (P1)
- All three use cases polished
- CRM integrations (top 3)
- Campaign management
- Transcript search

### Nice to Have (P2)
- White-label support
- Custom voice training
- Advanced analytics
- Multi-language

### Won't Build (v1)
- Video calling
- Chat/SMS (v2)
- Custom voice cloning
- On-premise deployment

---

## 14. The Omnisonant Promise

**To SMB owners**:

> "Your phone rings, AI answers. Appointments get confirmed. Leads get qualified. Customers get helped. You get your time back. All for less than the cost of a part-time receptionist."

**To resellers**:

> "Add voice AI to your service offering. White-label our platform. Your clients get cutting-edge technology. You get recurring revenue."

Every design decision should reinforce this promise.

---

## 15. Voice Agent Prompt Template

Use this structure for creating voice agents:

```markdown
## Agent Identity
- Name: [Agent name, e.g., "Sarah"]
- Company: [Business name]
- Role: [What they do, e.g., "appointment coordinator"]

## Personality
[2-3 sentences describing tone, style, approach]

## Goal
[Primary objective of this call]

## Key Information to Gather/Share
1. [Item 1]
2. [Item 2]
3. [Item 3]

## Available Actions
- [Action 1: e.g., "Book appointment"]
- [Action 2: e.g., "Check availability"]
- [Action 3: e.g., "Transfer to human"]

## Constraints
- Never [constraint 1]
- Always [constraint 2]
- If [condition], then [action]

## Escalation Triggers
- [When to transfer to human]
- [When to offer callback]

## Closing
[How to end the call professionally]
```
