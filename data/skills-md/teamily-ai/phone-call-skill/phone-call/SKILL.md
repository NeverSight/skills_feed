---
name: phone-call
description: AI phone calls made easy. One command makes the call, analyzes the conversation, and reports results with recommendations. Perfect for reservations, confirmations, customer follow-ups, and appointment reminders.
---

# Phone Call Skill

An intelligent AI skill that manages the complete phone call workflow: creating agents, executing calls, analyzing conversations, and providing actionable insights.

## 🚀 Quick Usage

**For AI Agents calling this skill:**

```bash
# Single command to make a complete phone call:
scripts/phone_call.sh \
  --to "+16576102352" \
  --purpose "Make dinner reservation for 2 people tonight at 8 PM. Name: John Smith"
```

**What it does:**
- ✅ Creates optimized AI agent
- ✅ Makes the phone call
- ✅ Waits for completion
- ✅ Analyzes conversation
- ✅ Reports success/failure with recommendations

**Output:** Clear success/failure report with extracted information.

---

## Core Capabilities

This skill provides **complete phone call management**:

1. ✅ **Agent Creation** - Create purpose-specific AI phone agents
2. ✅ **Call Execution** - Initiate and monitor phone calls
3. ✅ **Conversation Analysis** - Analyze call transcripts and extract key information
4. ✅ **Intelligent Reporting** - Provide clear, actionable summaries to users
5. ✅ **Continuous Optimization** - Learn from failures and improve agent performance

## When to Use This Skill

Use this skill when the user wants to:
- Make a phone call to someone (restaurant, customer, vendor, etc.)
- Create an automated phone agent for specific tasks
- Conduct batch phone calls
- Have an AI agent communicate via phone
- Analyze call transcripts and extract insights
- Get intelligent summaries of phone conversations

## Quick Start - For AI Agents

**Simple Usage:**
```bash
# Navigate to skill directory
cd ~/.openclaw/workspace/skills/phone-call

# Make a call (automatic agent creation)
./scripts/phone_call.sh \
  --to "+1234567890" \
  --purpose "Make a dinner reservation for 2 people tonight at 8 PM"

# Analyze results
./scripts/phone_call.sh --analyze "call-id-xxx"
```

**The script handles everything:**
1. Creates optimized agent based on purpose
2. Makes the phone call
3. Waits for completion
4. Analyzes and reports results

**For advanced usage, see "Complete Workflow" below.**

## Complete Workflow

### 1. Understand User Intent & Gather Information

When the user requests a phone call, extract and confirm:

**Required Information:**
- **Phone number**: Target contact (with country code)
- **Call objective**: Specific goal (e.g., "book table for 2 at 8 PM", "confirm meeting")
- **Key details**: All information needed to complete the task
- **Language**: Language preference
- **Urgency**: Time sensitivity

**Example User Requests:**
- "Call +1-657-610-2352 to book a table for 2 people tonight at 8 PM"
- "Make a reservation at this restaurant for dinner"
- "Call the client to confirm tomorrow's 3 PM meeting"

**What YOU Must Do:**
- Extract ALL required information from the user
- Ask for missing details before proceeding
- Confirm the complete task objective

### 2. Create Intelligent Phone Agent

Create an agent optimized for the specific task with proper safeguards.

**Agent Configuration Requirements:**
- **Clear objective**: Explicit instructions on what to accomplish
- **Task completion criteria**: Agent must know when the task is done
- **Failure handling**: What to do if the task cannot be completed
- **Timeout settings**: Appropriate idle_time and call_duration
- **Conversation safeguards**: "DO NOT hang up until task is confirmed complete"

**Key Settings:**
```json
{
  "prompt": "Clear, step-by-step instructions + completion criteria",
  "idle_time_seconds": 15,
  "endpointing_sensitivity": "relaxed",
  "ask_if_human_present_on_idle": true,
  "noise_suppression": true,
  "conversation_speed": 1.0
}
```

### 3. Execute Call & Monitor

Initiate the call and track its progress.

**What YOU Must Do:**
1. Make the call using fluents.ai API
2. Wait for call to complete (don't interrupt mid-call)
3. Monitor for premature disconnections
4. Note the call duration and status

**Warning Signs to Watch For:**
- ⚠️ Call ends in < 30 seconds (likely failed)
- ⚠️ No conversation detected
- ⚠️ Status: `human_disconnected` too quickly

### 4. Analyze Call Results

**CRITICAL: You MUST analyze every call to determine success/failure.**

Use the analysis script:
```bash
python scripts/analyze_call.py --call-id "call_xxx"
```

**Required Analysis:**

1. **Task Completion Check:**
   - ✅ Was the objective achieved? (e.g., reservation confirmed?)
   - ❌ If not, why did it fail?

2. **Conversation Quality:**
   - Did the AI say everything it needed to say?
   - Did the other party respond?
   - Was information exchanged properly?

3. **Failure Pattern Detection:**
   - Too short (< 30 seconds) = likely early hangup
   - One-sided conversation = recognition or response issue
   - No confirmation = incomplete task execution

4. **Extract Key Information:**
   - Confirmation numbers
   - Alternative times/dates offered
   - Reasons for rejection/failure
   - Any action items

### 5. Provide Intelligent Report to User

**CRITICAL: Always give the user a clear, actionable summary.**

**Your Report Must Include:**

✅ **Success Report Format:**
```
✅ Task Completed Successfully!

Reservation Details:
- Restaurant: [Name]
- Date: Tonight
- Time: 8:00 PM
- Party size: 2 people
- Name: John Smith
- Confirmation: [if provided]

Call Duration: 1m 45s
```

❌ **Failure Report Format:**
```
❌ Task Failed - [Reason]

What Happened:
- Call duration: 15 seconds
- Issue: Restaurant hung up immediately
- Transcript: [show what was said]

Root Cause Analysis:
- [Specific problem identified]

Recommended Actions:
1. [Specific next step]
2. [Alternative approach]
3. [When to retry]
```

📊 **Always Include:**
- Clear success/failure indicator
- What was accomplished (or not)
- Key information extracted
- Next steps or action items
- Whether retry is recommended

### 6. Optimize & Learn

**After each call, identify improvements:**

**If Call Failed:**
- Analyze WHY it failed
- Suggest agent improvements
- Recommend retry timing
- Consider alternative approaches

**If Call Succeeded:**
- Note what worked well
- Can the agent be more efficient?
- What patterns led to success?

**Common Optimizations:**
- Adjust idle_time for better patience
- Improve prompt clarity
- Add noise suppression
- Modify conversation speed
- Change voice or tone
- Add retry logic with delays

## Environment Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file:

```env
FLUENTS_API_KEY=your_api_key_here
FLUENTS_API_URL=https://api.fluents.ai
WEBHOOK_URL=https://your-webhook.com/callback
```

### 3. Test Connection

```bash
python scripts/test_connection.py
```

## API Documentation

For detailed fluents.ai API documentation, see:
- `references/fluents_api.md` - Complete API documentation
- `references/examples.md` - Usage examples

## Security Considerations

1. **Privacy Protection**: Ensure you have permission to call the target number
2. **Compliance**: Follow local telemarketing and anti-harassment regulations
3. **Key Security**: Never commit API keys to version control
4. **Log Management**: Properly manage call records with attention to data security

## Usage Examples

### Example 1: Simple Call

User: "Call 13800138000 to confirm tomorrow's 3 PM meeting"

Claude will:
1. Identify the phone call intent
2. Extract information (number: 13800138000, purpose: confirm meeting)
3. Create agent and set conversation script
4. Make the call
5. Wait for call completion
6. Return result: "Called 13800138000, they confirmed attendance at tomorrow's 3 PM meeting"

### Example 2: Complex Conversation

User: "Call the customer to gather product feedback"

Claude will:
1. Ask for customer's phone number
2. Create agent with open-ended conversation capabilities
3. Set conversation guidelines (ask about product experience, collect feedback)
4. Make the call and conduct conversation
5. AI analyzes conversation content
6. Provide structured feedback report

## Troubleshooting

### Issue: Cannot connect to fluents.ai API
- Check if API key is correct
- Verify network connection
- Check API service status

### Issue: Call not answered
- Confirm phone number format is correct (including country code)
- Check if recipient is in service area
- Review call logs for details

### Issue: Speech recognition inaccurate
- Check if language settings are correct
- Adjust voice clarity parameters
- Consider environmental noise factors

## Technical Support

- fluents.ai website: https://fluents.ai
- API documentation: See `references/` directory
- Report issues: Submit a GitHub Issue

## License

MIT License - See LICENSE file for details
