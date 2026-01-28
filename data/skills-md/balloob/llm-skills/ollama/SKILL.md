---
name: ollama
description: Use this if the user wants to connect to Ollama or leverage Ollama in any shape or form inside their project. Guide users integrating Ollama into their projects for local AI inference. Covers installation, connection setup, model management, and API usage for both Python and Node.js. Helps with text generation, chat interfaces, embeddings, streaming responses, and building AI-powered applications using local LLMs.
---

# Ollama

## Overview

This skill helps users integrate Ollama into their projects for running large language models locally. The skill guides users through setup, connection validation, model management, and API integration for both Python and Node.js applications. Ollama provides a simple API for running models like Llama, Mistral, Gemma, and others locally without cloud dependencies.

## When to Use This Skill

Use this skill when users want to:
- Run large language models locally on their machine
- Build AI-powered applications without cloud dependencies
- Implement text generation, chat, or embeddings functionality
- Stream LLM responses in real-time
- Create RAG (Retrieval-Augmented Generation) systems
- Integrate local AI capabilities into Python or Node.js projects
- Manage Ollama models (pull, list, delete)
- Validate Ollama connectivity and troubleshoot connection issues

## Installation and Setup

### Step 1: Collect Ollama URL

**IMPORTANT**: Always ask users for their Ollama URL. Do not assume it's running locally.

Ask the user: "What is your Ollama server URL?"

Common scenarios:
- **Local installation**: `http://localhost:11434` (default)
- **Remote server**: `http://192.168.1.100:11434`
- **Custom port**: `http://localhost:8080`
- **Docker**: `http://localhost:11434` (if port mapped to 11434)

If the user says they're running Ollama locally or doesn't know the URL, suggest trying `http://localhost:11434`.

### Step 2: Check if Ollama is Installed

Before proceeding, verify if Ollama is installed and running at the provided URL. Users can check by visiting the URL in their browser or running:

```bash
curl <OLLAMA_URL>/api/version
```

If Ollama is not installed, guide users to install it:

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

**Docker:**
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Step 3: Start Ollama Service

Ensure Ollama is running:

**macOS/Linux:**
```bash
ollama serve
```

**Docker:**
```bash
docker start ollama
```

The service typically runs at `http://localhost:11434` by default.

### Step 4: Validate Connection

Use the validation script to test connectivity and list available models.

**IMPORTANT**: The script path is relative to the skill directory. When running the script, either:
1. Use the full path from the skill directory (e.g., `/path/to/ollama/scripts/validate_connection.py`)
2. Change to the skill directory first and then run `python scripts/validate_connection.py`

```bash
# Run from the skill directory
cd /path/to/ollama
python scripts/validate_connection.py <OLLAMA_URL>
```

Example with the user's Ollama URL:
```bash
cd /path/to/ollama
python scripts/validate_connection.py http://192.168.1.100:11434
```

The script will:
- Normalize the URL (remove any path components)
- Check if Ollama is accessible
- Display the Ollama version
- List all installed models with sizes
- Provide troubleshooting guidance if connection fails

**Success output:**
```
✓ Connection successful!
  URL: http://localhost:11434
  Version: Ollama 0.1.0
  Models available: 2

Installed models:
  - llama3.2 (4.7 GB)
  - mistral (7.2 GB)
```

**Failure output:**
```
✗ Connection failed: Connection refused
  URL: http://localhost:11434

Troubleshooting:
  1. Ensure Ollama is installed and running
  2. Check that the URL is correct
  3. Verify Ollama is accessible at the specified URL
  4. Try: curl http://localhost:11434/api/version
```

## Model Management

### Pulling Models

Help users download models from the Ollama library. Common models include:

- `llama3.2` - Meta's Llama 3.2 (various sizes: 1B, 3B)
- `llama3.1` - Meta's Llama 3.1 (8B, 70B, 405B)
- `mistral` - Mistral 7B
- `phi3` - Microsoft Phi-3
- `gemma2` - Google Gemma 2

Users can pull models using:
```bash
ollama pull llama3.2
```

Or programmatically using the API (examples in reference docs).

### Listing Models

Guide users to list installed models:
```bash
ollama list
```

Or use the validation script to see models with detailed information.

### Removing Models

Help users delete models to free space:
```bash
ollama rm llama3.2
```

### Model Selection Guidance

Help users choose appropriate models based on their needs:

- **Small models (1-3B)**: Fast, good for simple tasks, lower resource requirements
- **Medium models (7-13B)**: Balanced performance and quality
- **Large models (70B+)**: Best quality, require significant resources

## Implementation Guidance

### Python Projects

For Python-based projects, refer to the Python API reference:

- **File**: `references/python_api.md`
- **Usage**: Load this reference when implementing Python integrations
- **Contains**:
  - REST API examples using `urllib.request` (standard library)
  - Text generation with the Generate API
  - Conversational interfaces with the Chat API
  - **Streaming responses for real-time output (RECOMMENDED)**
  - Embeddings for semantic search
  - Complete RAG system example
  - Error handling patterns
  - PEP 723 inline script metadata for dependencies
- **No dependencies required**: Uses only Python standard library

**IMPORTANT**: When creating Python scripts for users, include PEP 723 inline script metadata to declare dependencies. See the reference docs for examples.

**DEFAULT TO STREAMING**: When implementing text generation or chat, use streaming responses unless the user explicitly requests non-streaming.

Common Python use cases:
```python
# Streaming text generation (RECOMMENDED)
for token in generate_stream("Explain quantum computing"):
    print(token, end="", flush=True)

# Streaming chat conversation (RECOMMENDED)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
for token in chat_stream(messages):
    print(token, end="", flush=True)

# Non-streaming (use only when needed)
response = generate("Explain quantum computing")

# Embeddings for semantic search
embedding = get_embeddings("Hello, world!")
```

### Node.js Projects

For Node.js-based projects, refer to the Node.js API reference:

- **File**: `references/nodejs_api.md`
- **Usage**: Load this reference when implementing Node.js integrations
- **Contains**:
  - Official `ollama` npm package examples
  - Alternative Fetch API examples (Node.js 18+)
  - Text generation and chat APIs
  - **Streaming with async iterators (RECOMMENDED)**
  - Embeddings and semantic similarity
  - Complete RAG system example
  - Error handling and retry logic
  - TypeScript support examples

Installation:
```bash
npm install ollama
```

**DEFAULT TO STREAMING**: When implementing text generation or chat, use streaming responses unless the user explicitly requests non-streaming.

Common Node.js use cases:
```javascript
import { Ollama } from 'ollama';
const ollama = new Ollama();

// Streaming text generation (RECOMMENDED)
const stream = await ollama.generate({
  model: 'llama3.2',
  prompt: 'Explain quantum computing',
  stream: true
});

for await (const chunk of stream) {
  process.stdout.write(chunk.response);
}

// Streaming chat conversation (RECOMMENDED)
const chatStream = await ollama.chat({
  model: 'llama3.2',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'What is the capital of France?' }
  ],
  stream: true
});

for await (const chunk of chatStream) {
  process.stdout.write(chunk.message.content);
}

// Non-streaming (use only when needed)
const response = await ollama.generate({
  model: 'llama3.2',
  prompt: 'Explain quantum computing'
});

// Embeddings
const embedding = await ollama.embeddings({
  model: 'llama3.2',
  prompt: 'Hello, world!'
});
```

## Common Integration Patterns

### Text Generation

Generate text completions from prompts. Use cases:
- Content generation
- Code completion
- Question answering
- Summarization

Guide users to use the Generate API with appropriate parameters (temperature, top_p, etc.) for their use case.

### Conversational Interfaces

Build chat applications with conversation history. Use cases:
- Chatbots
- Virtual assistants
- Customer support
- Interactive tutorials

Guide users to use the Chat API with message history management. Explain the importance of system prompts for behavior control.

### Embeddings & Semantic Search

Generate vector embeddings for text. Use cases:
- Semantic search
- Document similarity
- RAG systems
- Recommendation systems

Guide users to use the Embeddings API and implement cosine similarity for comparing embeddings.

### Streaming Responses

**RECOMMENDED APPROACH**: Always prefer streaming for better user experience.

Stream LLM output token-by-token. Use cases:
- Real-time chat interfaces
- Progressive content generation
- Better user experience for long outputs
- Immediate feedback to users

**When creating code for users, default to streaming API** unless they specifically request non-streaming responses.

Guide users to:
- Enable `stream: true` in API calls
- Handle async iteration (Node.js) or generators (Python)
- Display tokens as they arrive for real-time feedback
- Show progress indicators during generation

### RAG (Retrieval-Augmented Generation)

Combine document retrieval with generation. Use cases:
- Question answering over documents
- Knowledge base chatbots
- Context-aware assistance

Guide users to:
1. Generate embeddings for documents
2. Store embeddings with associated text
3. Search for relevant documents using query embeddings
4. Inject retrieved context into prompts
5. Generate answers with context

Both reference docs include complete RAG system examples.

## Best Practices

### Security
- Never hardcode sensitive information
- Use environment variables for configuration
- Validate and sanitize user inputs before sending to LLM

### Performance
- Use streaming for long responses to improve perceived performance
- Cache embeddings for documents that don't change
- Choose appropriate model sizes for your use case
- Consider response time requirements when selecting models

### Error Handling
- Always implement proper error handling for network failures
- Check model availability before making requests
- Provide helpful error messages to users
- Implement retry logic for transient failures

### Connection Management
- Validate connections before proceeding with implementation
- Handle connection timeouts gracefully
- For remote Ollama instances, ensure network accessibility
- Use the validation script during development

### Model Management
- Check available disk space before pulling large models
- Keep only models you actively use
- Inform users about model download sizes
- Provide model selection guidance based on requirements

### Context Management
- For chat applications, manage conversation history to avoid token limits
- Trim old messages when conversations get too long
- Consider using summarization for long conversation histories

## Troubleshooting

### Connection Issues

If connection fails:
1. Verify Ollama is installed: `ollama --version`
2. Check if Ollama is running: `curl http://localhost:11434/api/version`
3. Restart Ollama service: `ollama serve`
4. Check firewall settings for remote connections
5. Verify the URL format (should be `http://host:port` with no path)

### Model Not Found

If model is not available:
1. List installed models: `ollama list`
2. Pull the required model: `ollama pull model-name`
3. Verify model name spelling (case-sensitive)

### Out of Memory

If running out of memory:
1. Use a smaller model variant
2. Close other applications
3. Increase system swap space
4. Consider using a machine with more RAM

### Slow Performance

If responses are slow:
1. Use a smaller model
2. Reduce `num_predict` parameter
3. Check CPU/GPU usage
4. Ensure Ollama is using GPU if available
5. Close other resource-intensive applications

## Resources

### scripts/validate_connection.py
Python script to validate Ollama connection and list available models. Normalizes URLs, tests connectivity, displays version information, and provides troubleshooting guidance.

### references/python_api.md
Comprehensive Python API reference with examples for:
- Installation and setup
- Connection verification
- Model management (list, pull, delete)
- Generate API for text completion
- Chat API for conversations
- Streaming responses
- Embeddings and semantic search
- Complete RAG system implementation
- Error handling patterns
- Best practices

### references/nodejs_api.md
Comprehensive Node.js API reference with examples for:
- Installation using npm
- Official `ollama` package usage
- Alternative Fetch API examples
- Model management
- Generate and Chat APIs
- Streaming with async iterators
- Embeddings and semantic similarity
- Complete RAG system implementation
- Error handling and retry logic
- TypeScript support
- Best practices
