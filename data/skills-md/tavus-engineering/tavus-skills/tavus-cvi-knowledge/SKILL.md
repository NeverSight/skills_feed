---
name: tavus-cvi-knowledge
description: Add knowledge bases and persistent memories to Tavus CVI personas. Use when uploading documents for RAG, enabling personas to reference PDFs/websites, persisting context across conversations, or building personas that remember users.
---

# Tavus CVI Knowledge Base & Memories

Give your personas access to documents and persistent memory.

## Knowledge Base (RAG)

Upload documents that personas can reference during conversations.

### Step 1: Create Document

```bash
curl -X POST https://tavusapi.com/v2/documents \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "document_name": "Product FAQ",
    "document_url": "https://example.com/faq.pdf",
    "tags": ["support", "faq"]
  }'
```

Response:
```json
{
  "document_id": "d1234567890",
  "status": "processing"
}
```

### Supported Sources

- **PDFs**: Direct URL to PDF file
- **Text files**: Plain text documents
- **Websites**: Single page or crawled

### Website Crawling

Single page (default):
```json
{
  "document_name": "Landing Page",
  "document_url": "https://example.com/features"
}
```

Multi-page crawl:
```json
{
  "document_name": "Full Docs",
  "document_url": "https://docs.example.com",
  "crawl_pages": true
}
```

### Step 2: Use in Conversation

By document IDs:
```json
{
  "persona_id": "p123",
  "replica_id": "r456",
  "document_ids": ["d1234567890", "d0987654321"]
}
```

By tags:
```json
{
  "persona_id": "p123",
  "replica_id": "r456",
  "document_tags": ["support", "faq"]
}
```

### Attach to Persona (Always Available)

Documents available in ALL conversations with this persona:

```bash
curl -X POST https://tavusapi.com/v2/personas \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "persona_name": "Support Agent",
    "pipeline_mode": "full",
    "system_prompt": "You are a helpful support agent...",
    "document_ids": ["d1234567890"],
    "document_tags": ["support"]
  }'
```

### Retrieval Strategy

Optimize search speed vs quality:

```json
{
  "persona_id": "p123",
  "document_ids": ["d123"],
  "retrieval_strategy": "balanced"
}
```

Options:
- `speed` - Fastest, good for simple lookups
- `quality` - Best results, slower
- `balanced` - Default, good tradeoff

### Manage Documents

```bash
# List documents
curl https://tavusapi.com/v2/documents \
  -H "x-api-key: YOUR_API_KEY"

# Get document status
curl https://tavusapi.com/v2/documents/{document_id} \
  -H "x-api-key: YOUR_API_KEY"

# Delete document
curl -X DELETE https://tavusapi.com/v2/documents/{document_id} \
  -H "x-api-key: YOUR_API_KEY"
```

---

## Memories (Persistent Context)

Remember information across conversations with the same user.

### How It Works

1. Assign a `memory_store` key to a conversation
2. Persona forms memories during conversation
3. Future conversations with same key access those memories

### Create Conversation with Memory

```json
{
  "persona_id": "p123",
  "replica_id": "r456",
  "memory_stores": ["user_alice_persona_sales"]
}
```

### Memory Store Naming

Use consistent, unique identifiers:
- `user_{user_id}_persona_{persona_id}` - Per user, per persona
- `user_{user_id}` - Per user across personas
- `session_{session_id}` - Per session

**Important**: Don't use persona names in keys (they might change).

### Example: Returning User

First conversation:
```json
{
  "persona_id": "p_coach",
  "memory_stores": ["user_alice_coaching"]
}
```
User mentions: "I'm training for a marathon in April."

Second conversation (days later):
```json
{
  "persona_id": "p_coach", 
  "memory_stores": ["user_alice_coaching"]
}
```
Persona remembers the marathon goal and can reference it.

### Multiple Memory Stores

Share memories across contexts:

```json
{
  "persona_id": "p123",
  "memory_stores": [
    "user_alice_global",
    "user_alice_sales_specific"
  ]
}
```

### Use Case: Multi-Persona Memory

User talks to Sales persona, then Support persona:

```json
// Sales conversation
{
  "persona_id": "p_sales",
  "memory_stores": ["user_alice"]
}

// Support conversation (later)
{
  "persona_id": "p_support",
  "memory_stores": ["user_alice"]
}
```

Support persona knows what Sales discussed.

---

## Combining Knowledge + Memories

Full-featured support agent:

```bash
# Create persona with knowledge base
curl -X POST https://tavusapi.com/v2/personas \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "persona_name": "Premium Support",
    "pipeline_mode": "full",
    "system_prompt": "You are a premium support agent. Reference the knowledge base for product info. Remember user preferences and past issues.",
    "document_tags": ["support", "product-docs"],
    "default_replica_id": "rfe12d8b9597"
  }'
```

```bash
# Start conversation with user memory
curl -X POST https://tavusapi.com/v2/conversations \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "persona_id": "p_premium_support",
    "memory_stores": ["user_12345_support"],
    "document_ids": ["d_urgent_issue_docs"]
  }'
```

Now the persona can:
- Look up product info from documents
- Remember this user's past issues
- Build on previous conversations
