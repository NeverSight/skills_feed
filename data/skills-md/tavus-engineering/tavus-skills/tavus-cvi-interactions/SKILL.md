---
name: tavus-cvi-interactions
description: Control Tavus CVI conversations in real-time using the Interactions Protocol. Use when sending text for the replica to speak (echo), interrupting the replica, injecting context mid-conversation, handling tool calls, or listening to conversation events via WebRTC/Daily.
---

# Tavus CVI Interactions Protocol

Control live conversations programmatically via WebRTC data channel.

## Setup: Daily.js Client

```html
<script src="https://unpkg.com/@daily-co/daily-js"></script>
<script>
const call = window.Daily.createFrame();

// Listen for events from CVI
call.on('app-message', (event) => {
  console.log('CVI event:', event.data);
});

// Join the conversation
call.join({ url: 'YOUR_CONVERSATION_URL' });

// Send interaction
function send(interaction) {
  call.sendAppMessage(interaction, '*');
}
</script>
```

## Interactions You Can Send

### Echo: Make Replica Speak Text

Bypass LLM, replica speaks exactly what you provide:

```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.echo",
  "conversation_id": "YOUR_CONVERSATION_ID",
  "properties": {
    "modality": "text",
    "text": "Hello! Let me tell you about our product."
  }
});
```

For streaming audio (base64):
```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.echo",
  "conversation_id": "YOUR_CONVERSATION_ID",
  "properties": {
    "modality": "audio",
    "audio": "BASE64_ENCODED_AUDIO",
    "sample_rate": 24000,
    "inference_id": "unique-id",
    "done": "true"
  }
});
```

### Respond: Inject User Input

Treat text as if user spoke it (goes through LLM):

```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.respond",
  "conversation_id": "YOUR_CONVERSATION_ID",
  "properties": {
    "text": "What are your pricing plans?"
  }
});
```

### Interrupt: Stop Replica Speaking

```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.interrupt",
  "conversation_id": "YOUR_CONVERSATION_ID"
});
```

### Overwrite Context

Replace the entire conversational context:

```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.overwrite_context",
  "conversation_id": "YOUR_CONVERSATION_ID",
  "properties": {
    "context": "User is now asking about enterprise features."
  }
});
```

### Append Context

Add to existing context without replacing:

```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.append_context",
  "conversation_id": "YOUR_CONVERSATION_ID",
  "properties": {
    "context": "User mentioned they have a team of 50 people."
  }
});
```

### Adjust Sensitivity

Change turn-taking sensitivity mid-conversation:

```javascript
send({
  "message_type": "conversation",
  "event_type": "conversation.sensitivity",
  "conversation_id": "YOUR_CONVERSATION_ID",
  "properties": {
    "participant_pause_sensitivity": "high",
    "participant_interrupt_sensitivity": "low"
  }
});
```

Values: `low`, `medium`, `high`

## Events You Receive

### Utterance (What Was Said)

```json
{
  "event_type": "conversation.utterance",
  "properties": {
    "role": "user",
    "content": "Tell me about your product"
  }
}
```

Role: `user` or `replica`

### Replica Started/Stopped Speaking

```json
{
  "event_type": "conversation.replica.started_speaking",
  "properties": {
    "inference_id": "inf-123"
  }
}
```

```json
{
  "event_type": "conversation.replica.stopped_speaking",
  "properties": {
    "inference_id": "inf-123",
    "duration": 4.5
  }
}
```

### User Started/Stopped Speaking

```json
{
  "event_type": "conversation.user.started_speaking"
}
```

### Tool Call (Function Calling)

When LLM invokes a tool:

```json
{
  "event_type": "conversation.tool_call",
  "properties": {
    "tool_name": "get_weather",
    "arguments": {
      "location": "San Francisco, CA"
    },
    "inference_id": "inf-123"
  }
}
```

Handle it, then respond with echo or respond interaction.

### Perception Analysis

When Raven analyzes the user:

```json
{
  "event_type": "conversation.perception_analysis",
  "properties": {
    "analysis": "User appears engaged, smiling, looking at camera"
  }
}
```

### Replica Interrupted

Fired when replica was interrupted:

```json
{
  "event_type": "conversation.replica.interrupted",
  "properties": {
    "inference_id": "inf-123"
  }
}
```

## Python Client (Daily-Python)

```python
from daily import Daily, CallClient

Daily.init()
client = CallClient()

def on_app_message(message, sender):
    print(f"Received: {message}")

client.set_user_name("bot")
client.join(meeting_url, completion=on_join)

# Send interaction
client.send_app_message({
    "message_type": "conversation",
    "event_type": "conversation.echo",
    "conversation_id": "xxx",
    "properties": {"text": "Hello!"}
})
```

## Common Patterns

### Echo Mode with Manual Control

1. Create persona with `pipeline_mode: "echo"`
2. Join conversation with Daily client
3. Send `conversation.echo` events to control speech
4. Send `conversation.interrupt` to stop
5. Listen for events to track state

### Hybrid: LLM + Manual Injection

1. Use `pipeline_mode: "full"` for normal conversation
2. Inject context with `conversation.append_context`
3. Override with `conversation.echo` when needed
4. Use `conversation.interrupt` + `conversation.echo` for immediate takeover
