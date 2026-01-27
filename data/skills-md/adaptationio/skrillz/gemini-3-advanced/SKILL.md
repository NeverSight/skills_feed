---
name: gemini-3-advanced
description: Advanced Gemini 3 Pro features including function calling, built-in tools (Google Search, Code Execution, File Search, URL Context), structured outputs, thought signatures, context caching, batch processing, and framework integration. Use when implementing tools, function calling, structured JSON output, context caching, batch API, LangChain, Vercel AI, or production features.
---

# Gemini 3 Pro Advanced Features

Comprehensive guide for advanced Gemini 3 Pro capabilities including function calling, built-in tools, structured outputs, context caching, batch processing, and framework integrations.

## Overview

This skill covers production-ready advanced features that extend Gemini 3 Pro's capabilities beyond basic text generation.

### Key Capabilities

- **Function Calling:** Custom tool integration with OpenAPI 3.0
- **Built-in Tools:** Google Search, Code Execution, File Search, URL Context
- **Structured Outputs:** Guaranteed JSON structure with Pydantic/Zod
- **Thought Signatures:** Managing multi-turn reasoning context
- **Context Caching:** Reuse large contexts (>2k tokens) for cost savings
- **Batch Processing:** Async processing at scale
- **Framework Integration:** LangChain, Vercel AI, Pydantic AI, CrewAI

### When to Use This Skill

- Implementing custom tools/functions
- Enabling Google Search grounding
- Executing code safely
- Requiring structured JSON output
- Optimizing costs with caching
- Batch processing requests
- Building production applications
- Integrating with AI frameworks

---

## Quick Start

### Function Calling Quick Start

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Define function
def get_weather(location: str) -> dict:
    return {"location": location, "temp": 72, "condition": "sunny"}

# Declare function to model
weather_func = genai.protos.FunctionDeclaration(
    name="get_weather",
    description="Get current weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"}
        },
        "required": ["location"]
    }
)

model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    tools=[genai.protos.Tool(function_declarations=[weather_func])]
)

# Use function
response = model.generate_content("What's the weather in San Francisco?")

# Handle function call
if response.parts[0].function_call:
    fc = response.parts[0].function_call
    result = get_weather(**dict(fc.args))

    # Send result back
    response = model.generate_content([
        {"role": "model", "parts": [response.parts[0]]},
        {"role": "user", "parts": [genai.protos.Part(
            function_response=genai.protos.FunctionResponse(
                name=fc.name,
                response=result
            )
        )]}
    ])

print(response.text)
```

---

## Core Tasks

### Task 1: Implement Function Calling

**Goal:** Create custom tools that the model can call.

**Python Example:**

```python
import google.generativeai as genai
from datetime import datetime

genai.configure(api_key="YOUR_API_KEY")

# Define Python functions
def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(operation: str, a: float, b: float) -> float:
    ops = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }
    return ops.get(operation, lambda x, y: "Unknown operation")(a, b)

# Declare functions to model (OpenAPI 3.0 format)
time_func = genai.protos.FunctionDeclaration(
    name="get_current_time",
    description="Get the current date and time",
    parameters={"type": "object", "properties": {}}
)

calc_func = genai.protos.FunctionDeclaration(
    name="calculate",
    description="Perform basic arithmetic operations",
    parameters={
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The operation to perform"
            },
            "a": {"type": "number", "description": "First number"},
            "b": {"type": "number", "description": "Second number"}
        },
        "required": ["operation", "a", "b"]
    }
)

# Create model with tools
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    tools=[genai.protos.Tool(function_declarations=[time_func, calc_func])]
)

# Use tools
chat = model.start_chat()
response = chat.send_message("What time is it? Also calculate 15 * 8")

# Process function calls
function_registry = {
    "get_current_time": get_current_time,
    "calculate": calculate
}

while response.parts[0].function_call:
    fc = response.parts[0].function_call
    func = function_registry[fc.name]
    result = func(**dict(fc.args))

    response = chat.send_message(genai.protos.Part(
        function_response=genai.protos.FunctionResponse(
            name=fc.name,
            response={"result": result}
        )
    ))

print(response.text)
```

**See:** `references/function-calling.md` for comprehensive guide

---

### Task 2: Use Built-in Tools

**Goal:** Enable Google Search, Code Execution, and other built-in tools.

**Google Search Grounding:**

```python
# Enable Google Search
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    tools=[{"google_search_retrieval": {}}]
)

response = model.generate_content("What are the latest developments in quantum computing?")

# Check grounding metadata
if hasattr(response, 'grounding_metadata'):
    print(f"Search sources used: {len(response.grounding_metadata.grounding_chunks)}")

print(response.text)
```

**Code Execution:**

```python
# Enable code execution
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    tools=[{"code_execution": {}}]
)

response = model.generate_content(
    "Calculate the first 20 Fibonacci numbers and show the results"
)

print(response.text)
```

**See:** `references/built-in-tools.md` for all tools

---

### Task 3: Implement Structured Outputs

**Goal:** Get guaranteed JSON structure from model.

**Python with Pydantic:**

```python
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

genai.configure(api_key="YOUR_API_KEY")

# Define schema
class Movie(BaseModel):
    title: str
    director: str
    year: int
    genre: List[str]
    rating: float

class MovieList(BaseModel):
    movies: List[Movie]

# Configure model for structured output
model = genai.GenerativeModel(
    "gemini-3-pro-preview",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": MovieList
    }
)

response = model.generate_content(
    "List 3 classic science fiction movies"
)

# Parse structured output
import json
data = json.loads(response.text)
movies = MovieList(**data)

for movie in movies.movies:
    print(f"{movie.title} ({movie.year}) - Rating: {movie.rating}")
```

**TypeScript with Zod:**

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import { z } from "zod";

const MovieSchema = z.object({
  title: z.string(),
  director: z.string(),
  year: z.number(),
  genre: z.array(z.string()),
  rating: z.number()
});

const MovieListSchema = z.object({
  movies: z.array(MovieSchema)
});

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);

const model = genAI.getGenerativeModel({
  model: "gemini-3-pro-preview",
  generationConfig: {
    responseMimeType: "application/json",
    responseSchema: MovieListSchema
  }
});

const result = await model.generateContent("List 3 classic science fiction movies");
const movies = MovieListSchema.parse(JSON.parse(result.response.text()));

console.log(movies);
```

**See:** `references/structured-outputs.md` for advanced patterns

---

### Task 4: Setup Context Caching

**Goal:** Reuse large contexts (>2k tokens) for cost savings.

**Python Example:**

```python
import google.generativeai as genai
from pathlib import Path

genai.configure(api_key="YOUR_API_KEY")

# Load large document
large_doc = Path("codebase.txt").read_text()  # Must be >2048 tokens

# Create cached content
cached_content = genai.caching.CachedContent.create(
    model="gemini-3-pro-preview",
    system_instruction="You are a code reviewer",
    contents=[large_doc]
)

# Use cached content
model = genai.GenerativeModel.from_cached_content(cached_content)

# Multiple queries using same cached context
response1 = model.generate_content("Find all security vulnerabilities")
response2 = model.generate_content("Suggest performance improvements")
response3 = model.generate_content("Check for code duplication")

# Cost savings: cached tokens are 90% cheaper
print(f"Cache name: {cached_content.name}")

# Clean up cache when done
cached_content.delete()
```

**Cost Comparison:**

| Context Size | Without Cache | With Cache | Savings |
|-------------|---------------|------------|---------|
| 100k tokens × 10 queries | $2.00 | $0.22 | 89% |
| 500k tokens × 50 queries | $50.00 | $5.50 | 89% |

**See:** `references/context-caching.md` for comprehensive guide

---

### Task 5: Implement Batch Processing

**Goal:** Process multiple requests asynchronously.

**Python Example:**

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3-pro-preview")

# Prepare batch requests
prompts = [
    "Summarize the benefits of AI",
    "Explain quantum computing",
    "Describe blockchain technology",
    "What is machine learning?"
]

# Process in batch
import asyncio

async def generate_async(prompt):
    response = model.generate_content(prompt)
    return {"prompt": prompt, "response": response.text}

async def batch_process(prompts):
    tasks = [generate_async(p) for p in prompts]
    results = await asyncio.gather(*tasks)
    return results

# Run batch
results = asyncio.run(batch_process(prompts))

for result in results:
    print(f"Q: {result['prompt']}")
    print(f"A: {result['response']}\n")
```

**See:** `references/batch-processing.md` for advanced patterns

---

### Task 6: Manage Thought Signatures

**Goal:** Handle thought signatures in complex multi-turn scenarios.

**Key Points:**

1. **Standard Chat:** SDKs handle automatically
2. **Function Calls:** Must return signatures in sequential order
3. **Parallel Calls:** Only first call contains signature
4. **Image Editing:** Required on first part and all subsequent parts

**Example with Function Calls:**

```python
# When handling function calls, preserve signatures
response = chat.send_message("Use these tools...")

function_calls = []
signatures = []

for part in response.parts:
    if part.function_call:
        function_calls.append(part.function_call)
    if hasattr(part, 'thought_signature'):
        signatures.append(part.thought_signature)

# Execute functions
results = [execute_function(fc) for fc in function_calls]

# Return results with signatures in order
response_parts = []
for i, result in enumerate(results):
    part = genai.protos.Part(
        function_response=genai.protos.FunctionResponse(
            name=function_calls[i].name,
            response=result
        )
    )
    if i < len(signatures):
        part.thought_signature = signatures[i]
    response_parts.append(part)

response = chat.send_message(response_parts)
```

**Bypass Validation (when needed):**

```python
# Use bypass string for migration/testing
bypass_signature = "context_engineering_is_the_way_to_go"
```

**See:** `references/thought-signatures.md` for complete guide

---

### Task 7: Integrate with Frameworks

**Goal:** Use Gemini 3 Pro with popular AI frameworks.

**LangChain:**

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    google_api_key="YOUR_API_KEY"
)

response = llm.invoke("Explain neural networks")
print(response.content)
```

**Vercel AI SDK:**

```typescript
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { generateText } from 'ai';

const google = createGoogleGenerativeAI({
  apiKey: process.env.GEMINI_API_KEY
});

const { text } = await generateText({
  model: google('gemini-3-pro-preview'),
  prompt: 'Explain neural networks'
});

console.log(text);
```

**Pydantic AI:**

```python
from pydantic_ai import Agent

agent = Agent(
    'google-genai:gemini-3-pro-preview',
    system_prompt='You are a helpful AI assistant'
)

result = agent.run_sync('Explain neural networks')
print(result.data)
```

**See:** `references/framework-integration.md` for all frameworks

---

## Production Best Practices

### 1. Error Handling

```python
from google.api_core import exceptions, retry

@retry.Retry(
    predicate=retry.if_exception_type(
        exceptions.ResourceExhausted,
        exceptions.ServiceUnavailable
    )
)
def safe_generate(prompt):
    try:
        return model.generate_content(prompt)
    except exceptions.InvalidArgument as e:
        logger.error(f"Invalid argument: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

### 2. Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_rpm=60):
        self.max_rpm = max_rpm
        self.requests = deque()

    def wait_if_needed(self):
        now = time.time()
        self.requests = deque([t for t in self.requests if t > now - 60])

        if len(self.requests) >= self.max_rpm:
            sleep_time = 60 - (now - self.requests[0])
            time.sleep(max(0, sleep_time))

        self.requests.append(now)
```

### 3. Cost Monitoring

```python
class CostTracker:
    def __init__(self):
        self.total_cost = 0

    def track(self, response):
        usage = response.usage_metadata
        input_cost = (usage.prompt_token_count / 1_000_000) * 2.00
        output_cost = (usage.candidates_token_count / 1_000_000) * 12.00

        cost = input_cost + output_cost
        self.total_cost += cost

        return {
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "cost": cost,
            "total_cost": self.total_cost
        }
```

---

## References

**Core Features**
- [Function Calling](references/function-calling.md) - Custom tool integration
- [Built-in Tools](references/built-in-tools.md) - Google Search, Code Execution, etc.
- [Structured Outputs](references/structured-outputs.md) - JSON schema with Pydantic/Zod
- [Thought Signatures](references/thought-signatures.md) - Managing reasoning context
- [Context Caching](references/context-caching.md) - Cost optimization with caching
- [Batch Processing](references/batch-processing.md) - Async and batch API

**Integration**
- [Framework Integration](references/framework-integration.md) - LangChain, Vercel AI, etc.
- [Production Guide](references/production-guide.md) - Deployment best practices

**Scripts**
- [Function Calling Script](scripts/function-calling.py) - Tool integration example
- [Tools Script](scripts/use-tools.py) - Built-in tools demonstration
- [Structured Output Script](scripts/structured-output.py) - JSON schema example
- [Caching Script](scripts/caching.py) - Context caching implementation
- [Batch Script](scripts/batch-process.py) - Batch processing example

**Official Resources**
- [Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Grounding](https://ai.google.dev/gemini-api/docs/grounding)
- [Caching](https://ai.google.dev/gemini-api/docs/caching)
- [Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output)

---

## Related Skills

- **gemini-3-pro-api** - Basic setup, authentication, text generation
- **gemini-3-multimodal** - Media processing (images, video, audio)
- **gemini-3-image-generation** - Image generation

---

## Summary

This skill provides advanced production features:

✅ Function calling with custom tools
✅ Built-in tools (Search, Code Exec, etc.)
✅ Structured JSON outputs
✅ Thought signature management
✅ Context caching for cost savings
✅ Batch processing at scale
✅ Framework integrations
✅ Production-ready patterns

**Ready for advanced features?** Start with the task that matches your use case above!
