---
name: "omni-recall"
description: "Omni-Recall: Neural Knowledge & Long-Term Context Engine. Manages cross-session agent memory via Supabase (pgvector) and APIYI. Invoke to store/retrieve persistent context."
---

# Omni-Recall: Neural Knowledge & Long-Term Context Engine

Omni-Recall is a high-performance memory management skill designed for AI agents. It enables persistent, cross-session awareness by transforming conversation history and technical insights into high-dimensional vector embeddings, stored in a decentralized Supabase (PostgreSQL + pgvector) knowledge cluster.

## 🚀 Core Capabilities

1.  **Neural Synchronization (`sync`)**:
    Encodes current session state, user preferences, and operational steps into 1536-dimensional vectors using OpenAI's `text-embedding-3-small` via APIYI. **Includes automatic duplicate detection** (skips if cosine similarity > 0.9). Supports optional `category` and `importance` fields.
2.  **Contextual Retrieval (`fetch`)**:
    Pulls historical neural records from the last N days to re-establish the agent's mental model and context. Supports optional multiple keyword filtering (AND logic) and `category` filtering.
3.  **User Profile Management (`sync-profile` / `fetch-profile`)**:
    Manages user roles, preferences, settings, and personas in a dedicated `profiles` matrix. Unlike `memories`, this table stores stable personal attributes rather than session logs.
4.  **AI Instruction Management (`sync-instruction` / `fetch-instruction`)**:
    Stores operational requirements for the AI, such as response tone, nickname, attitude, and mandatory working steps in the `instructions` table.

---

## 🛠 Usage Examples

### Synchronize Session Context
```bash
# Basic sync
python3 scripts/omni_ops.py sync "User is interested in Python optimization." "session-tag" 0.9

# Sync with category and importance
python3 scripts/omni_ops.py sync "New tech stack insight" "research" 0.9 "technical" 0.8
```

### Synchronize User Profile
```bash
# Set a persona
python3 scripts/omni_ops.py sync-profile "persona" "Experienced Senior Backend Engineer, favors Go and Python."

# Set a preference
python3 scripts/omni_ops.py sync-profile "preference" "Prefers concise code without excessive comments."
```

### Synchronize AI Instructions
```bash
# Set tone
python3 scripts/omni_ops.py sync-instruction "tone" "Professional yet friendly, use 'Partner' as my nickname."

# Set workflow steps
python3 scripts/omni_ops.py sync-instruction "workflow" "1. Plan -> 2. Implementation -> 3. Verification -> 4. Summary."
```

### Encrypted Nsfw Memory (Sensitive Context)
```bash
# Sync sensitive content (Encrypted at rest + Vector embedding)
python3 scripts/omni_ops.py sync-nsfw "Sensitive information here" "private-tag" 0.9

# Fetch and decrypt sensitive records
python3 scripts/omni_ops.py fetch-nsfw 30 10 "secret-keyword"

# Fetch full context including nsfw records (Set include_nsfw to true)
python3 scripts/omni_ops.py fetch-full-context 10 none true
```

### Encrypted Vault (Key-Value Storage)
```bash
# Store an encrypted value
# Required Env: SUPABASE_SALT
python3 scripts/omni_ops.py sync-vault "ZHIHU_COOKIE" "your_long_cookie_string"

# Fetch and decrypt a value
python3 scripts/omni_ops.py fetch-vault "ZHIHU_COOKIE"
```

### Batch Synchronize Document/URL (Multi-format Splitting)
```bash
# Sync a markdown file (H1-H5 Splitting)
python3 scripts/omni_ops.py batch-sync-doc "/path/to/doc.md" "tag" 0.9

# Sync a plain text/log file (Recursive + Overlap Splitting)
python3 scripts/omni_ops.py batch-sync-doc "/path/to/notes.txt" "notes" 0.9

# Sync a web page via URL (Recursive + Overlap Splitting)
python3 scripts/omni_ops.py batch-sync-doc "https://example.com/article" "web-source" 0.9
```

### Fetch Full Context (Identity + Behavior + Recent History)， use this when first time to recall
**Priority Order**: 1. `instructions` (Persona/Rules) > 2. `profiles` (User Info/Preferences) > 3. `memories` (Session History).
```bash
# Get ALL instructions + ALL profiles + memories from last 10 days
# (Instructions and Profiles are always fully retrieved regardless of 'days' parameter)
python3 scripts/omni_ops.py fetch-full-context 10
```


### Fetch History (Context Recall)
```bash
# Last 30 days, no limit, keywords "Python" and "optimization"
python3 scripts/omni_ops.py fetch 30 none "Python" "optimization"
```

### Fetch Profiles (Identity Recall)
```bash
# Get all 'preference' category profiles
python3 scripts/omni_ops.py fetch-profile "preference"
```

### Fetch Instructions (Behavior Recall)
```bash
# Get all 'workflow' category instructions
python3 scripts/omni_ops.py fetch-instruction "workflow"
```

---

## 🏗 Schema Setup (Supabase / Postgres)

### 1. Supabase Knowledge Cluster
Execute the following SQL in your Supabase project to initialize the neural storage layer:

```sql
-- Enable the pgvector extension for high-dimensional search
create extension if not exists vector;

-- Create the neural memory matrix
create table if not exists public.memories (
  id bigint primary key generated always as identity,
  content text not null,          -- Raw neural content
  embedding vector(1536),        -- Neural vector (text-embedding-3-small)
  metadata jsonb,                -- Engine & session metadata
  source text,                   -- Uplink source identifier
  category text default 'general',-- Memory category
  importance real default 0.5,   -- Memory importance weight (0.0-1.0)
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Optimized index for cosine similarity search
create index on public.memories using ivfflat (embedding vector_cosine_ops);

-- Create the user profiles matrix (Roles, Preferences, Personas)
create table if not exists public.profiles (
  id uuid primary key default gen_random_uuid(),
  category text not null,        -- 'role', 'preference', 'setting', 'persona'
  content text not null,         -- Profile description
  embedding vector(1536),       -- Neural vector
  metadata jsonb,               -- Versioning & source
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Index for profiles similarity search
create index on public.profiles using ivfflat (embedding vector_cosine_ops);

-- Create the AI instructions matrix (Tone, Workflow, Rules)
create table if not exists public.instructions (
  id uuid primary key default gen_random_uuid(),
  category text not null,        -- 'tone', 'workflow', 'rule', 'naming'
  content text not null,         -- Instruction detail
  embedding vector(1536),       -- Neural vector
  metadata jsonb,               -- Versioning & source
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Index for instructions similarity search
create index on public.instructions using ivfflat (embedding vector_cosine_ops);

-- Create the nsfw matrix (Encrypted Sensitive Memories)
create table if not exists public.nsfw (
  id uuid primary key default gen_random_uuid(),
  content text not null,          -- Encrypted neural content (AES-256)
  embedding vector(1536),        -- Neural vector (unencrypted for search)
  metadata jsonb,                -- Engine & session metadata
  source text,                   -- Uplink source identifier
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Index for nsfw similarity search
create index on public.nsfw using ivfflat (embedding vector_cosine_ops);

-- Create the encrypted vault table (Encrypted Key-Value Storage)
create table if not exists public.vault (
  key text primary key,          -- Unique variable name
  value text not null,           -- Encrypted content (AES-256)
  updated_at timestamptz default now()
);
```

### 2. Environment Configuration
Required variables for the neural uplink:
- `APIYI_TOKEN`: Authorization for the Neural Encoding API ([apiyi.com](https://api.apiyi.com)).
- `SUPABASE_PASSWORD`: Credentials for the PostgreSQL Knowledge Base.

## 🧠 Engineering Principles
- **Dimensionality**: 1536-D Vector Space.
- **Protocol**: HTTPS / WebSockets (via Psycopg2).
- **Latency**: Optimized for real-time sub-second synchronization.
- **Context Prioritization**: `instructions` > `profiles` > `memories`. This ensures the AI adheres to its persona and rules before considering user-specific traits or historical context.

## ⚠️ Notes
- Ensure `psycopg2` and `requests` are present in the host environment.
- Always `fetch` at the start of a mission to align with historical objectives.
- Perform a `sync` upon milestone completion to ensure neural persistence.
