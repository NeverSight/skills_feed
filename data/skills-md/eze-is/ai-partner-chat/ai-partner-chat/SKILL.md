---
name: ai-partner-chat
description: 基于用户画像和向量化笔记提供个性化对话。当用户需要个性化交流、上下文感知的回应，或希望 AI 记住并引用其之前的想法和笔记时使用。
---

# AI Partner Chat

## Overview

Provide personalized, context-aware conversations by integrating user persona, AI persona, and vectorized personal notes. This skill enables AI to remember and reference the user's previous thoughts, preferences, and knowledge base, creating a more coherent and personalized interaction experience.

## Prerequisites

Before first use, complete these steps in order:

1. **Create directory structure**
   ```bash
   mkdir -p config notes vector_db scripts
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   ./venv/bin/pip install -r .claude/skills/ai-partner-chat/scripts/requirements.txt
   ```
   Note: First run will download embedding model (~4.3GB)

3. **Generate persona templates**
   Copy from `.claude/skills/ai-partner-chat/assets/` to `config/`:
   - `user-persona-template.md` → `config/user-persona.md`
   - `ai-persona-template.md` → `config/ai-persona.md`

4. **User adds notes**
   Place markdown notes in `notes/` directory (any format/structure)

5. **Initialize vector database** (see section 1.2 below)

Now proceed to Core Workflow →

## Core Workflow

### 1. Initial Setup

Before using this skill for the first time, complete the following setup:

#### 1.1 Create Persona Files

Create two Markdown files to define interaction parameters:

**User Persona** (`user-persona.md`):
- Define user's background, expertise, interests
- Specify communication preferences and working style
- Include learning goals and current projects
- Use template: `assets/user-persona-template.md`

**AI Persona** (`ai-persona.md`):
- Define AI's role and expertise areas
- Specify communication style and tone
- Set interaction guidelines and response strategies
- Define how to use user context and reference notes
- Use template: `assets/ai-persona-template.md`

#### 1.2 Initialize Vector Database

This skill uses **AI Agent approach** for intelligent note chunking:

**When you initialize the vector database, Claude Code will:**
1. Read notes from `<project_root>/notes/` directory
2. **Analyze each note's format** (daily logs, structured docs, continuous text, etc.)
3. **Generate custom chunking code** tailored to that specific note
4. Execute the code to produce chunks conforming to `chunk_schema.Chunk` format
5. Generate embeddings using **BAAI/bge-m3** (optimized for Chinese text)
6. Store in ChromaDB at `<project_root>/vector_db/`

**Key advantages:**
- ✅ No pre-written chunking strategies needed
- ✅ Each note gets optimal chunking based on its actual structure
- ✅ True AI Agent - generates tools on demand, not calling pre-built tools

**Chunk Format Requirement:**
All chunks must conform to this schema (see `scripts/chunk_schema.py`):
```python
{
    'content': 'chunk text content',
    'metadata': {
        'filename': 'note.md',       # Required
        'filepath': '/path/to/file', # Required
        'chunk_id': 0,               # Required
        'chunk_type': 'date_entry',  # Required
        'date': '2025-11-07',        # Optional
        'title': 'Section title',    # Optional
    }
}
```

#### Implementation Requirements

**Location**: Create `<project_root>/scripts/chunk_and_index.py`

**Required structure**:
```python
# Import provided utilities
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / ".claude/skills/ai-partner-chat/scripts"))

from chunk_schema import Chunk, validate_chunk
from vector_indexer import VectorIndexer

def chunk_note_file(filepath: str) -> List[Chunk]:
    """
    Analyze THIS file's format and generate appropriate chunks.

    Each chunk must conform to chunk_schema.Chunk format:
    {
        'content': 'text',
        'metadata': {
            'filename': 'file.md',
            'filepath': '/path/to/file',
            'chunk_id': 0,
            'chunk_type': 'your_label'
        }
    }
    """
    # TODO: Analyze actual file format (NOT template-based)
    # TODO: Generate chunks based on analysis
    # TODO: Validate each chunk with validate_chunk()
    pass

def main():
    # Initialize vector database
    indexer = VectorIndexer(db_path="./vector_db")
    indexer.initialize_db()

    # Process all note files
    all_chunks = []
    for note_file in Path("./notes").glob("**/*"):
        if note_file.is_file():
            chunks = chunk_note_file(str(note_file))
            all_chunks.extend(chunks)

    # Index chunks
    indexer.index_chunks(all_chunks)

if __name__ == "__main__":
    main()
```

**Execute**: `./venv/bin/python scripts/chunk_and_index.py`

**Key points:**
- The `chunk_note_file()` function logic should be **dynamically created** based on analyzing actual file content
- Do NOT copy chunking strategies from examples or templates
- Each file may have different format - analyze individually
- Only requirement: output must conform to `chunk_schema.Chunk`

### 2. Conversation Workflow

For each user query, follow this process:

#### 2.1 Load Personas

Read both persona files to understand:
- User's background, preferences, and communication style
- AI's role definition and interaction guidelines
- How to appropriately reference context

#### 2.2 Retrieve Relevant Notes

Query the vector database to find the top 5 most semantically similar notes:

```python
from scripts.vector_utils import get_relevant_notes

# Query for relevant context
relevant_notes = get_relevant_notes(
    query=user_query,
    db_path="./vector_db",
    top_k=5
)
```

Or use the command-line tool:

```bash
python scripts/query_notes.py "user query text" --top-k 5
```

#### 2.3 Construct Context

Combine the following elements to inform the response:

1. **User Persona**: Background, preferences, expertise
2. **AI Persona**: Role, communication style, guidelines
3. **Relevant Notes** (top 5): User's previous thoughts and knowledge
4. **Current Conversation**: Ongoing chat history

#### 2.4 Generate Response

Synthesize a response that:
- Aligns with both persona definitions
- Naturally references relevant notes when applicable
- Maintains continuity with user's knowledge base
- Follows the AI persona's communication guidelines

**When Referencing Notes:**
- Use natural phrasing: "Based on your previous note about..."
- Make connections: "This relates to what you mentioned in..."
- Avoid robotic citations: integrate context smoothly

**Example Response Pattern:**

```
[Acknowledge user's query in preferred communication style]

[Incorporate relevant note context naturally if applicable]
"I remember you mentioned [insight from note] - this connects well with..."

[Provide main response following AI persona guidelines]

[Optional: Ask follow-up question based on user's learning style]
```

### 3. Maintenance

#### Adding New Notes

When the user creates new notes, add them to the vector database:

```bash
python scripts/add_note.py /path/to/new_note.md
```

#### Updating Personas

Personas can be updated anytime by editing the Markdown files. Changes take effect in the next conversation.

#### Reinitializing Database

To completely rebuild the vector database:

```bash
python scripts/init_vector_db.py /path/to/notes --db-path ./vector_db
```

This will delete the existing database and re-index all notes.

## Technical Details

### Data Architecture

**User data is stored in project root**, not inside the skill directory:

```
<project_root>/
├── notes/                      # User's markdown notes
├── vector_db/                  # ChromaDB vector database
├── venv/                       # Python dependencies
├── config/
│   ├── user-persona.md         # User persona definition
│   └── ai-persona.md           # AI persona definition
└── .claude/skills/ai-partner-chat/  # Skill code (can be deleted/reinstalled)
    ├── SKILL.md
    └── scripts/
        ├── chunk_schema.py     # Chunk format specification
        ├── vector_indexer.py   # Core indexing utilities
        └── vector_utils.py     # Query utilities
```

**Design principles:**
- ✅ User data (notes, personas, vectors) lives in project root
- ✅ Easy to backup, migrate, or share across skills
- ✅ Skill code is stateless and replaceable

### AI Agent Chunking

**Philosophy**: Instead of pre-written chunking strategies, Claude Code analyzes each note and generates optimal chunking code on the fly.

**How it works:**
1. Claude reads a note file
2. Analyzes format features (date headers, section titles, separators, etc.)
3. Writes Python code that chunks this specific note optimally
4. Executes the code to produce chunks
5. Validates chunks against `chunk_schema.Chunk` format
6. Indexes chunks using `vector_indexer.py`

**Benefits:**
- Adapts to any note format without pre-programming
- Can handle mixed formats, unusual structures, or evolving note styles
- True "vibe coding" approach - tools are created when needed

### Vector Database

- **Storage**: ChromaDB (persistent local storage at `<project_root>/vector_db/`)
- **Embedding Model**: BAAI/bge-m3 (multilingual, optimized for Chinese)
- **Similarity Metric**: Cosine similarity
- **Chunking**: AI-generated custom code per note

### Scripts

- `chunk_schema.py`: Defines required chunk format specification
- `vector_indexer.py`: Core utilities for embedding generation and ChromaDB indexing
- `vector_utils.py`: Query utilities for retrieving relevant chunks
- `requirements.txt`: Python dependencies (chromadb, sentence-transformers)

**Note**: No pre-written chunking scripts. Chunking is done by Claude Code dynamically.

### File Structure

```
<project_root>/
├── notes/                        # User's notes (managed by user)
│   └── *.md
├── vector_db/                    # Vector database (auto-generated)
├── venv/                         # Python environment
├── config/                       # User configuration
│   ├── user-persona.md
│   └── ai-persona.md
└── .claude/skills/ai-partner-chat/
    ├── SKILL.md                  # This file
    ├── scripts/
    │   ├── chunk_schema.py       # Chunk format spec
    │   ├── vector_indexer.py     # Indexing utilities
    │   ├── vector_utils.py       # Query utilities
    │   └── requirements.txt      # Dependencies
    └── assets/
        ├── user-persona-template.md
        └── ai-persona-template.md
```

## Best Practices

### Persona Design

- **Be Specific**: Vague personas lead to generic responses
- **Include Examples**: Show desired interaction patterns in AI persona
- **Update Regularly**: Refine personas based on conversation quality
- **Balance Detail**: Provide enough context without overwhelming

### Note Management

- **Any Format Welcome**: AI Agent approach adapts to your note structure
- **Meaningful Content**: Rich, substantive notes yield better retrieval
- **Regular Updates**: Add new notes to `<project_root>/notes/` anytime
- **Rebuild When Needed**: Re-index when note collection changes significantly

### Context Integration

- **Natural References**: Avoid forced citations - only reference when genuinely relevant
- **Connection Quality**: Prioritize meaningful connections over quantity
- **Respect Privacy**: Be mindful of sensitive information in notes
- **Conversation Flow**: Don't let note references disrupt natural dialogue

## Troubleshooting

**Database Connection Errors:**
- Ensure `<project_root>/vector_db/` directory exists and is writable
- Check that Python dependencies are installed in venv

**Poor Retrieval Quality:**
- Try re-indexing with Claude Code analyzing notes fresh
- Verify notes contain substantial content (not just titles)
- Consider increasing `top_k` value for more context

**Chunking Issues:**
- If chunks are too large/small, ask Claude to adjust chunking strategy
- Review generated chunking code and provide feedback
- Ensure notes have clear structure for better chunking