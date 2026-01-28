---
name: baml
description: Learn how to use the BAML programming language for LLM structured outputs
---

# BAML Quick Reference

BAML (Boundary AI Markup Language) is a DSL for building LLM applications with structured, type-safe outputs. It generates client code for Python, TypeScript, Go, and Ruby.

## How BAML Works

- All `.baml` files in `baml_src/` are globally accessible to each other
- Generate the client with `baml-cli generate`
- The generated `baml_client/` provides type-safe functions you import and call
- BAML types become Pydantic models (Python), TypeScript types, Go structs, or Sorbet types (Ruby)

---

## Essential Syntax

### Types

```baml
// Primitives
string, int, float, bool, null

// Composite
Type?           // optional (nullable)
Type[]          // array
Type1 | Type2   // union
map<K, V>       // dictionary

// Literals
"spam" | "ham"  // literal string union

// Multimodal
image, audio, video, pdf
```

### Classes

Define structured data shapes. **No colons between field name and type.**

```baml
class Resume {
    name string
    email string?                           // optional
    skills string[]                         // array
    experience Experience[]                 // nested type
    seniority SeniorityLevel               // enum
}

class Experience {
    company string
    role string @description("Job title")   // hint for the LLM
    years int @alias("duration_years")      // JSON key mapping
}
```

### Enums

Fixed set of values. Great for classification tasks.

```baml
enum SeniorityLevel {
    JUNIOR @description("0-2 years experience")
    MID @description("2-5 years experience")
    SENIOR @description("5+ years experience")
}

enum Category {
    SPAM
    HAM
    UNKNOWN @skip  // excluded from prompts
}
```

### Functions

Define the LLM interaction. **Function names must start with a capital letter.**

```baml
function ExtractResume(resume_text: string) -> Resume {
    client "openai/gpt-4o"
    prompt #"
        Extract structured information from this resume.

        {{ ctx.output_format }}

        Resume:
        ---
        {{ resume_text }}
        ---
    "#
}
```

### Clients

Configure LLM providers. Two styles:

```baml
// Shorthand (uses env vars automatically)
client "openai/gpt-4o"
client "anthropic/claude-sonnet-4-20250514"

// Named client (full control)
client<llm> GPT4 {
    provider openai
    options {
        model "gpt-4o"
        api_key env.OPENAI_API_KEY
        temperature 0.0
    }
}

// Fallback chain
client<llm> Resilient {
    provider fallback
    options {
        clients [GPT4, Claude, GPT4Mini]
    }
}
```

### Generator

Configure code generation:

```baml
generator target {
    output_type "python/pydantic"  // or "typescript", "go", "ruby/sorbet"
    output_dir "../"
    default_client_mode "sync"     // or "async"
    version "0.203.1"
}
```

You may set up codegen for multiple locations in multiple languages.
For example, you may want to keep backend and frontend types aligned for your respective BAML clients.
You can do this by initializing two `generator` blocks.

---

## The Two Critical Concepts

### 1. `{{ ctx.output_format }}`

This Jinja macro **must be included in every prompt**. It renders the return type schema so the LLM knows what structure to produce.

```baml
function ClassifyEmail(email: string) -> Category {
    client GPT4
    prompt #"
        Classify this email.

        {{ ctx.output_format }}

        Email: {{ email }}
    "#
}
```

For a `Category` enum, this renders something like:
```
Answer with any of the categories:
SPAM
HAM
```

For a class, it renders the JSON schema with field descriptions.

### 2. Schema-Aligned Parsing (SAP)

BAML's parser is intentionally lenient. It automatically fixes common LLM output issues:
- Missing quotes around strings
- Trailing commas
- Comments in JSON
- Incomplete sequences
- Unescaped characters

This means you get **87-93% better accuracy** than strict JSON parsing or function calling.

---

## Prompt Syntax (Jinja)

BAML prompts use Jinja templating:

```baml
prompt #"
    {# Comments don't appear in output #}

    {{ _.role("system") }}
    You are a helpful assistant.

    {{ _.role("user") }}
    {% for msg in messages %}
        {{ msg.content }}
    {% endfor %}

    {% if verbose %}
        Be detailed in your response.
    {% endif %}

    {{ ctx.output_format }}
"#
```

**Key constructs:**
- `{{ variable }}` - interpolate values
- `{% for item in list %}...{% endfor %}` - loops
- `{% if cond %}...{% endif %}` - conditionals
- `{{ _.role("system"|"user"|"assistant") }}` - set message role
- `{{ value|filter }}` - apply filters (e.g., `|upper`, `|length`, `|join(",")`)

---

## Calling BAML Functions

### Python

```python
from baml_client import b
from baml_client.types import Resume

# Sync
resume = b.ExtractResume(resume_text)
print(resume.name, resume.skills)

# Async
from baml_client.async_client import b
resume = await b.ExtractResume(resume_text)

# Streaming
stream = b.stream.ExtractResume(resume_text)
for partial in stream:
    print(partial)  # partial Resume object
final = stream.get_final_response()
```

### TypeScript

```typescript
import { b } from './baml_client'

// Async (default)
const resume = await b.ExtractResume(resumeText)
console.log(resume.name, resume.skills)

// Streaming
const stream = b.stream.ExtractResume(resumeText)
for await (const partial of stream) {
    console.log(partial)
}
const final = await stream.getFinalResponse()
```

### Go

```go
import b "example.com/myproject/baml_client"

resume, err := b.ExtractResume(ctx, resumeText, nil)
if err != nil {
    log.Fatal(err)
}
fmt.Println(resume.Name, resume.Skills)
```

---

## Testing

Define tests directly in BAML files:

```baml
test SimpleExtraction {
    functions [ExtractResume]
    args {
        resume_text "John Doe, Software Engineer at Acme Corp for 5 years"
    }
    @@assert({{ this.name == "John Doe" }})
}
```

Run tests:
```bash
baml-cli test                    # run all
baml-cli test -i "ExtractResume" # filter by function
baml-cli test --parallel 5       # parallel execution
```

---

## Attributes Reference

**Field-level:**
- `@alias("name")` - rename field in JSON output
- `@description("...")` - add context for the LLM
- `@skip` - exclude from prompts (enums only)

**Block-level:**
- `@@dynamic` - allow runtime modification of class/enum

**Validation:**
- `@check(expr, name)` - soft validation (returns result, doesn't fail)
- `@assert(expr, name)` - hard validation (throws on failure)

**Streaming:**
- `@@stream.done` - object only appears when complete
- `@stream.not_null` - field must have value before parent streams
- `@stream.with_state` - include completion state metadata

---

## CLI Commands

```bash
baml-cli init          # initialize new project
baml-cli generate      # generate client code
baml-cli dev           # dev server with hot reload
baml-cli test          # run tests
baml-cli serve         # start REST API server (port 2024)
baml-cli fmt           # format BAML files
```

---

## Common Patterns

See the `examples/` directory for complete working examples:
- `extraction.baml` - structured data extraction
- `classification.baml` - enum-based classification
- `chat.baml` - multi-turn chat with message history
- `multimodal.baml` - image/audio/pdf inputs
- `usage.py` - Python calling patterns

---

## Further Resources

**Getting Started**
- Installation: https://docs.boundaryml.com/guide/installation-language/python.md
- TypeScript setup: https://docs.boundaryml.com/guide/installation-language/typescript.md
- Go setup: https://docs.boundaryml.com/guide/installation-language/go.md

**Language Reference**
- Complete syntax: https://docs.boundaryml.com/ref/overview.md
- Type system: https://docs.boundaryml.com/ref/baml/types.md
- Classes: https://docs.boundaryml.com/ref/baml/class.md
- Enums: https://docs.boundaryml.com/ref/baml/enum.md
- Functions: https://docs.boundaryml.com/ref/baml/function.md
- Generator: https://docs.boundaryml.com/ref/baml/generator.md

**LLM Providers**
- OpenAI: https://docs.boundaryml.com/ref/llm-client-providers/open-ai.md
- OpenAI-compatible (Ollama, vLLM, etc.): https://docs.boundaryml.com/ref/llm-client-providers/openai-generic.md
- Fallback strategy: https://docs.boundaryml.com/ref/llm-client-strategies/fallback.md
- Round-robin strategy: https://docs.boundaryml.com/ref/llm-client-strategies/round-robin.md

**Prompt Engineering**
- Reducing hallucinations: https://docs.boundaryml.com/examples/prompt-engineering/reducing-hallucinations.md
- Classification patterns: https://docs.boundaryml.com/examples/prompt-engineering/classification.md

**Advanced**
- Streaming: https://docs.boundaryml.com/guide/baml-basics/streaming.md
- Dynamic types: https://docs.boundaryml.com/guide/baml-advanced/dynamic-types.md

**Testing**
- Writing tests: https://docs.boundaryml.com/ref/baml/test.md
