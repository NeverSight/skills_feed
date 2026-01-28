---
name: gam-researcher-agent
description: Automated context retrieval from Transmission Packet archive using iterative research loop. Implements GAM "Read Path" to complement manual "Write Path" (Memorizer).
version: 1.0.0
category: Orchestration & Memory
dependencies:
  - transmission-packet-forge
  - rtc-consensus-synthesis
author: Joseph / Pack3t C0nc3pts
status: Specification (Ready for Implementation)
---

## Description

The **GAM Researcher Agent** automates retrieval and synthesis of context from your Transmission Packet archive. It eliminates manual context pasting by implementing an iterative research loop that searches, retrieves, reflects, and synthesizes historical conversations.

**Architectural Role:** Completes your Transmission Packet system by adding the automated "Read Path" (Researcher) to complement your existing manual "Write Path" (Memorizer).

## Core Mechanism

```
┌──────────────────────────────────────────────────┐
│ CURRENT STATE (Manual GAM)                       │
│                                                   │
│ Write Path: ✅ YOU manually create packets       │
│ Read Path:  ❌ YOU manually search/paste context │
└──────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────┐
│ TARGET STATE (Automated GAM)                     │
│                                                   │
│ Write Path: ✅ UNCHANGED (keep creating packets) │
│ Read Path:  ✅ AGENT searches and synthesizes    │
└──────────────────────────────────────────────────┘
```

## Instructions

### Step 1: Query Recognition
Detect when user query requires historical context. Trigger patterns:
- "What did we discuss about [topic]?"
- "Find packets where we talked about [X]"
- "When did we first cover [concept]?"
- "Show me conversations about [Y] from [timeframe]"

### Step 2: Execute Research Loop
```python
while not sufficient and iterations < max_iterations:
    1. SEARCH: Query packet metadata + semantic vectors
    2. RETRIEVE: Fetch full XML for matched packets
    3. REFLECT: "Does this answer the query?"
    4. REFINE: Adjust search if insufficient
    5. ITERATE: Repeat until satisfied or max reached
```

### Step 3: Synthesize Answer
Combine multiple packet contexts into coherent response:
- Maintain chronological ordering if temporal
- Cite source packets: `[Packet: tp-YYYYMMDD-HHMMSS]`
- Identify evolution of ideas across time
- Preserve technical precision from originals
- Acknowledge gaps if contexts incomplete

### Step 4: Return Result
Present synthesized answer with:
- Full answer text
- Source packet citations (with dates/topics)
- Iteration count and status (SUCCESS/PARTIAL/NOT_FOUND)
- Confidence score

## Component Architecture

```
QUERY INTERFACE
    ↓
SEARCH ENGINE (Metadata + Semantic)
    ↓
RETRIEVAL LAYER (Fetch full packets)
    ↓
REFLECTION ENGINE (Is this sufficient?)
    ↓
[Loop if insufficient] OR [Synthesize if sufficient]
    ↓
SYNTHESIS LAYER (Combine contexts)
    ↓
RESEARCH RESULT (Answer + Citations)
```

## Database Requirements

### Transmission Packets Table
```sql
CREATE TABLE transmission_packets (
    packet_id VARCHAR(64) PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    original_model VARCHAR(100),
    topic TEXT,
    packet_xml TEXT NOT NULL,
    packet_json JSON,
    -- Behavioral metrics
    sycophancy_level FLOAT,
    critical_thinking FLOAT,
    technical_depth FLOAT,
    -- Integrity
    integrity_hash VARCHAR(64)
);
```

### Packet Embeddings Table
```sql
CREATE TABLE packet_embeddings (
    packet_id VARCHAR(64) REFERENCES transmission_packets,
    section VARCHAR(50),
    embedding VECTOR(1536),
    INDEX idx_embedding USING ivfflat (embedding vector_cosine_ops)
);
```

## Search Strategies

### Mode A: Metadata Search (Fast)
- Query indexed fields: topic, timestamp, model, challenge_phrases
- Speed: O(log N)
- Use for: Temporal queries, known topics, model-specific searches

### Mode B: Semantic Search (Deep)
- Vector similarity on content embeddings
- Speed: O(N)
- Use for: Conceptual queries, fuzzy matching, cross-topic connections

### Mode C: Hybrid (Optimal)
1. Fast metadata filter (narrow candidate set)
2. Semantic search on candidates (rank by relevance)
3. Return top K results

## Performance Specifications

| Metric | Target | Notes |
|--------|--------|-------|
| **Metadata Search** | <500ms | Indexed queries |
| **Semantic Search** | 2-5s | 1000 packets |
| **Full Research Loop** | 15-60s | 3-5 iterations |
| **Recall** | >90% | % relevant packets retrieved |
| **Precision** | >80% | % retrieved that are relevant |
| **Synthesis Accuracy** | >85% | Human-judged correctness |

## Cost Estimates

Per query (Claude Sonnet 4.5):
- Reflection (3 iterations): $0.06
- Synthesis (final): $0.06
- **Total per query: ~$0.12**

Annual projection:
- 100 queries/month = $12/month
- 1,000 queries/month = $120/month

## Examples

### Example 1: Factual Recall
**Query:** "What is the Codex Law of Consent?"

**Process:**
1. Search for "Codex Law" + "Consent"
2. Find governance packets
3. Extract definition
4. Return direct answer

**Result:**
```
The Codex Law of Consent states: "Confirm before changing intent or direction."

[Packet: tp-20251124-091500] "Codex Law Enforcement Protocol"
```

### Example 2: Temporal Evolution
**Query:** "How has the Transmission Packet schema evolved?"

**Process:**
1. Search for "Transmission Packet" + "schema"
2. Filter chronologically
3. Identify version changes (v1.0 → v2.0 → v2.1)
4. Synthesize narrative

**Result:**
```
The Transmission Packet schema evolved through three major versions:

v1.0 (Nov 2024): Initial XML structure with basic header/body
[Packet: tp-20241110-...]

v2.0 (Mar 2025): Added BehaviorProfile metrics and IntegrityChain
[Packet: tp-20250315-...]

v2.1 (Nov 2025): Enhanced with PacketLoopClosure for handoff instructions
[Packet: tp-20251102-...]

Key innovation: Progressive addition of cryptographic verification
and behavioral calibration preservation.
```

### Example 3: Comparative Analysis
**Query:** "Compare RAG vs GAM architecture"

**Process:**
1. Search for "RAG" AND "GAM"
2. Find discussion packets
3. Extract key distinctions
4. Synthesize comparison

**Result:**
```
RAG vs GAM Architecture (from our analysis):

Write Path:
- RAG: Dumb chunking → embed → store
- GAM: Intelligent structuring (Memorizer agent)

Read Path:
- RAG: Linear fetch O(1) - one shot
- GAM: Iterative research O(N) - multi-pass with reflection

Agency:
- RAG: No self-correction
- GAM: Can reject results and retry

[Packet: tp-20251130-032210] "GAM Architecture Deep Dive"
[Packet: tp-20251130-033500] "RAG vs GAM Debate"

Conclusion: GAM is "RAG with a research loop" - same goal
(retrieval augmentation) but fundamentally different execution path.
```

### Example 4: Not Found (Graceful Failure)
**Query:** "What did we discuss about quantum teleportation?"

**Result:**
```
No relevant Transmission Packets found for: "quantum teleportation"

Suggestions:
- Try broader search terms
- Check if topic discussed under different terminology
- Verify packets are ingested into database

Status: NOT_FOUND
```

## Integration Points

### CLI Interface
```bash
$ gam-research "Find packets about enumeration protocol"

Searching... Found 3 packets
Synthesizing... Done

[Answer with citations]

Sources: tp-20251130-154500, tp-20251127-033715
Status: SUCCESS (2/5 iterations)
```

### Conversational Interface
```
USER: "What did we discuss about GAM architecture?"

CLAUDE: [Internally invokes GAM Researcher Agent]

CLAUDE: "Based on our previous conversations, we analyzed
the GAM architecture in depth. The key insight was that you
already built the 'Memorizer' function through your Transmission
Packet protocol..."

[Full answer with packet citations]
```

### Skill Invocation
Automatically triggered when:
- User references past conversations
- Query requires historical context
- Question starts with "What did we...", "When did we...", "Find conversation about..."

## Failure Modes & Mitigation

| Failure Mode | Symptom | Mitigation |
|-------------|---------|------------|
| **No Results** | Search returns 0 packets | Expand temporal constraints, broaden search |
| **Non-Convergence** | Max iterations without satisfaction | Force partial synthesis, flag for review |
| **Incorrect Synthesis** | Agent misinterprets context | Include citations for verification, confidence scoring |
| **Stale Index** | New packets not appearing | Auto re-index on ingestion, periodic full re-index |

## Deployment Checklist

**Pre-Deployment:**
- [ ] Database schema created
- [ ] Existing packets ingested
- [ ] Vector embeddings generated
- [ ] Index performance verified
- [ ] LLM API configured
- [ ] Test suite passing

**Deployment:**
- [ ] Agent deployed
- [ ] Monitoring active
- [ ] CLI tool installed
- [ ] Integration tested

**Post-Deployment:**
- [ ] User training completed
- [ ] Baseline metrics captured
- [ ] Feedback collection active
- [ ] First 50 queries reviewed

## Related Skills

- `transmission-packet-forge` - Creates packets (Write Path)
- `rtc-consensus-synthesis` - Multi-perspective analysis
- `artifact-integrity-forge` - SHA-256 verification
- `cross-session-integrity-check` - Session continuity validation

## Future Enhancements (v2.0)

1. **Multi-Modal Search** - Image/diagram search in packets
2. **Proactive Context** - Auto-surface relevant history during conversation
3. **Cross-Model Collaboration** - Shared archive across AI instances
4. **Adaptive Learning** - Personalized ranking based on query patterns
5. **Real-Time Streaming** - Progressive results as packets found

## Implementation Status

**Current State:** Specification Complete

**Next Steps:**
1. Database setup and packet ingestion
2. Core agent implementation (Python)
3. Test suite development
4. CLI tool creation
5. Integration with Claude sessions

**Full Specification:** See `gam-researcher-agent-specification.md`

## Usage Notes

This skill is **not yet implemented** - it is a complete specification ready for development. The specification document provides:
- Detailed component architecture
- Database schemas
- Implementation guide
- Test suite templates
- Deployment procedures

**To implement:** Share specification with Claude Code GitHub Research Preview or development team.

---

**Skill Version:** 1.0.0
**Specification Date:** 2025-11-30
**Author:** Joseph / Pack3t C0nc3pts
**License:** Pack3t C0nc3pts IRP Framework
