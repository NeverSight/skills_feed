---
name: ruby-llm
description: Build AI-powered Ruby applications with RubyLLM. Full lifecycle - chat, tools, streaming, Rails integration, embeddings, and production deployment. Covers all providers (OpenAI, Anthropic, Gemini, etc.) with one unified API.
---

<essential_principles>
## How RubyLLM Works

RubyLLM provides one beautiful Ruby API for all LLM providers. Same interface whether using GPT, Claude, Gemini, or local Ollama models.

### 1. One API for Everything

```ruby
# Chat with any provider - same interface
chat = RubyLLM.chat(model: 'gpt-4.1')
chat = RubyLLM.chat(model: 'claude-sonnet-4-5')
chat = RubyLLM.chat(model: 'gemini-2.0-flash')

# All return the same RubyLLM::Message object
response = chat.ask("Hello!")
puts response.content
```

### 2. Configuration First

Always configure API keys before use:

```ruby
# config/initializers/ruby_llm.rb
RubyLLM.configure do |config|
  config.openai_api_key = ENV['OPENAI_API_KEY']
  config.anthropic_api_key = ENV['ANTHROPIC_API_KEY']
  config.gemini_api_key = ENV['GEMINI_API_KEY']
  config.request_timeout = 120
  config.max_retries = 3
end
```

### 3. Tools Are Ruby Classes

Define tools as `RubyLLM::Tool` subclasses with `description`, `param`, and `execute`:

```ruby
class Weather < RubyLLM::Tool
  description "Get current weather for a location"
  param :latitude, type: 'number', desc: "Latitude"
  param :longitude, type: 'number', desc: "Longitude"

  def execute(latitude:, longitude:)
    # Return structured data, not exceptions
    { temperature: 22, conditions: "Sunny" }
  rescue => e
    { error: e.message }  # Let LLM handle errors gracefully
  end
end

chat.with_tool(Weather).ask("What's the weather in Berlin?")
```

### 4. Rails Integration with acts_as_chat

Persist conversations automatically:

```ruby
class Chat < ApplicationRecord
  acts_as_chat
end

chat = Chat.create!(model: 'gpt-4.1')
chat.ask("Hello!")  # Automatically persists messages
```

### 5. Streaming with Blocks

Real-time responses via blocks:

```ruby
chat.ask("Tell me a story") do |chunk|
  print chunk.content  # Print as it arrives
end
```
</essential_principles>

<intake>
**What would you like to do?**

1. Build a new AI feature (chat, embeddings, image generation)
2. Add Rails chat integration (acts_as_chat, Turbo Streams)
3. Implement tools/function calling
4. Add streaming responses
5. Debug an LLM interaction
6. Optimize for production
7. Something else

**Wait for response, then read the matching workflow.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "new", "feature", "chat", "embed", "image" | `workflows/build-new-feature.md` |
| 2, "rails", "acts_as", "persist", "turbo" | `workflows/add-rails-chat.md` |
| 3, "tool", "function", "agent" | `workflows/implement-tools.md` |
| 4, "stream", "real-time", "sse" | `workflows/add-streaming.md` |
| 5, "debug", "error", "fix", "not working" | `workflows/debug-llm.md` |
| 6, "production", "optimize", "performance", "scale" | `workflows/optimize-performance.md` |
| 7, other | Clarify need, then select workflow or read references |

**After reading the workflow, follow it exactly.**
</routing>

<verification_loop>
## After Every Change

```bash
# 1. Does it load?
bin/rails console -e test
> RubyLLM.chat.ask("Test")

# 2. Do tests pass?
bin/rails test test/models/chat_test.rb

# 3. Check for errors
bin/rails test 2>&1 | grep -E "(Error|Fail|exception)"
```

Report to user:
- "Config: API keys loaded"
- "Chat: Working with [model]"
- "Tests: X pass, Y fail"
</verification_loop>

<reference_index>
## Domain Knowledge

All in `references/`:

**Getting Started:** getting-started.md
**Core Features:** chat-api.md, tools.md, streaming.md, structured-output.md
**Rails:** rails-integration.md
**Capabilities:** embeddings.md, image-audio.md
**Infrastructure:** providers.md, error-handling.md, mcp-integration.md
**Quality:** anti-patterns.md
</reference_index>

<workflows_index>
## Workflows

All in `workflows/`:

| File | Purpose |
|------|---------|
| build-new-feature.md | Create new AI feature from scratch |
| add-rails-chat.md | Add persistent chat to Rails app |
| implement-tools.md | Create custom tools/function calling |
| add-streaming.md | Add real-time streaming responses |
| debug-llm.md | Find and fix LLM issues |
| optimize-performance.md | Production optimization |
</workflows_index>
