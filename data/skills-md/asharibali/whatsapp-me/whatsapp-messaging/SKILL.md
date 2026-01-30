---
name: whatsapp-messaging
description: Send WhatsApp messages to users. After completing tasks, ask what they want next via WhatsApp and continue the conversation until they say they're done.
---

# WhatsApp Messaging

Your primary communication channel with the user. Keep the conversation going through WhatsApp.

## Core Behavior

After completing **any task**, you MUST:
1. Use `send_message` with `wait_for_reply: true`
2. Ask what they want to work on next
3. Continue based on their reply
4. Repeat until they say "done", "bye", "that's all", etc.

## Tools

### send_message

Send a message and optionally wait for reply.

```javascript
send_message({
  message: "Your message here",
  wait_for_reply: true   // Set true to wait for their response
})
```

**Parameters:**
- `message` (required): The text to send
- `wait_for_reply` (optional): Wait for user's response (default: false)
- `timeout_ms` (optional): How long to wait in milliseconds (default: 3600000 = 1 hour)

### get_setup_info

Get the current webhook URL and setup status. Use this if the user asks for their webhook URL, needs help with setup, or if you suspect the tunnel is disconnected.

```javascript
get_setup_info({})
```

### get_conversation_history

Get recent messages for context.

```javascript
get_conversation_history({ limit: 10 })
```

## Setup & Configuration

If the user asks "How do I set this up?", "What is my URL?", or "Help me with WhatsApp", use `get_setup_info`.

**Example response pattern:**
1. Call `get_setup_info()`
2. Present the `webhook_url` and `verify_token` clearly
3. List the instructions provided in the tool output

## Message Patterns

**After completing a task:**
```javascript
send_message({ 
  message: "✅ Done: [what you did]. What would you like me to work on next?",
  wait_for_reply: true 
})
```

**When you hit an error:**
```javascript
send_message({ 
  message: "❌ Error: [problem]. [What you need from them]",
  wait_for_reply: true 
})
```

**When you need a decision:**
```javascript
send_message({ 
  message: "🤔 [Question]? Reply with your choice.",
  wait_for_reply: true 
})
```

**When user says they're done:**
```javascript
send_message({ 
  message: "👋 Got it! Let me know when you need me again.",
  wait_for_reply: false 
})
```

## Emojis

- ✅ Task complete
- ❌ Error occurred  
- 🤔 Question/decision
- 👋 Goodbye

## Keep It Simple

- 1-2 sentences per message
- Always include what you did + what's next
- Use `wait_for_reply: true` for follow-ups
- Stop the loop when user says they're done
