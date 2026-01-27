---
name: ai-sdk-elements
description: |
  Build AI chat interfaces with AI SDK Elements - React components for chatbots.
  Use when: implementing chat UIs, adding AI reasoning displays, tool confirmations,
  message components, or any AI-native interface. Built on shadcn/ui.
---

# AI SDK Elements

## Overview

AI SDK Elements is a React component library built on **shadcn/ui** for AI-native applications. Part of Vercel's AI SDK ecosystem.

**Requirements:**
- React 19 (no forwardRef patterns)
- Tailwind CSS 4
- shadcn/ui configured

**Docs:** https://ai-sdk.dev/elements

## Quick Reference

```bash
# Install all components
npx ai-elements@latest

# Install specific component
npx ai-elements@latest add conversation
npx ai-elements@latest add message
npx ai-elements@latest add reasoning

# Alternative (shadcn CLI)
npx shadcn@latest add @ai-elements/conversation
```

Components install to `@/components/ai-elements/`

---

## Core Components

### Conversation (Chat Container)

Main wrapper with auto-scroll to bottom.

```tsx
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';

<Conversation className="relative h-full">
  <ConversationContent>
    {messages.length === 0 ? (
      <ConversationEmptyState
        icon={<MessageSquareIcon />}
        title="Start a conversation"
        description="Ask me anything"
      />
    ) : (
      messages.map((msg) => (
        <Message key={msg.id} from={msg.role}>
          <MessageContent>{msg.content}</MessageContent>
        </Message>
      ))
    )}
  </ConversationContent>
  <ConversationScrollButton />
</Conversation>
```

### Message

Individual chat message display.

```tsx
import { Message, MessageContent } from '@/components/ai-elements/message';

<Message from="user">
  <MessageContent>Hello, can you help me?</MessageContent>
</Message>

<Message from="assistant">
  <MessageContent>{response}</MessageContent>
</Message>
```

### Prompt Input

User input for chat.

```tsx
import { PromptInput } from '@/components/ai-elements/prompt-input';

<PromptInput
  value={input}
  onChange={(e) => setInput(e.target.value)}
  onSubmit={handleSubmit}
  placeholder="Type a message..."
/>
```

---

## AI Reasoning Components

### Reasoning (Collapsible Thinking)

Auto-opens during streaming, collapses when done.

```tsx
import {
  Reasoning,
  ReasoningTrigger,
  ReasoningContent,
} from '@/components/ai-elements/reasoning';

<Reasoning isStreaming={isStreaming} className="w-full">
  <ReasoningTrigger title="Thinking..." />
  <ReasoningContent>{reasoningText}</ReasoningContent>
</Reasoning>
```

### Chain of Thought

Visual step-by-step reasoning with search results, images, progress.

```tsx
import { ChainOfThought } from '@/components/ai-elements/chain-of-thought';

<ChainOfThought>
  <ChainOfThoughtStep>
    <ChainOfThoughtIcon><SearchIcon /></ChainOfThoughtIcon>
    <ChainOfThoughtContent>
      Searching for profiles...
      <ChainOfThoughtLinks>
        <ChainOfThoughtLink href="https://x.com">x.com</ChainOfThoughtLink>
        <ChainOfThoughtLink href="https://github.com">github.com</ChainOfThoughtLink>
      </ChainOfThoughtLinks>
    </ChainOfThoughtContent>
  </ChainOfThoughtStep>
</ChainOfThought>
```

### Plan & Task

Display agent plans and individual tasks.

```tsx
import { Plan, Task } from '@/components/ai-elements/plan';

<Plan title="Implementation Plan">
  <Task status="completed">Set up project structure</Task>
  <Task status="in_progress">Implement core features</Task>
  <Task status="pending">Write tests</Task>
</Plan>
```

---

## Interactivity Components

### Confirmation (Tool Approval)

Manage tool execution approval workflows.

```tsx
import {
  Confirmation,
  ConfirmationRequest,
  ConfirmationAccepted,
  ConfirmationRejected,
  ConfirmationActions,
  ConfirmationAction,
} from '@/components/ai-elements/confirmation';

<Confirmation approval={tool.approval} state={tool.state}>
  <ConfirmationRequest>
    This tool wants to delete: <code>{tool.input?.filePath}</code>
    <br />Do you approve?
  </ConfirmationRequest>
  <ConfirmationAccepted>File deleted successfully</ConfirmationAccepted>
  <ConfirmationRejected>Action cancelled</ConfirmationRejected>
  <ConfirmationActions>
    <ConfirmationAction
      onClick={() => respondToConfirmationRequest({ approvalId, approved: false })}>
      Reject
    </ConfirmationAction>
    <ConfirmationAction
      onClick={() => respondToConfirmationRequest({ approvalId, approved: true })}>
      Approve
    </ConfirmationAction>
  </ConfirmationActions>
</Confirmation>
```

### Suggestion (Quick Prompts)

Horizontal row of clickable suggestions.

```tsx
import { Suggestions, Suggestion } from '@/components/ai-elements/suggestion';

const prompts = [
  'How do I get started?',
  'What can you help with?',
  'Show me examples',
];

<Suggestions>
  {prompts.map((prompt) => (
    <Suggestion
      key={prompt}
      suggestion={prompt}
      onClick={(text) => setInput(text)}
    />
  ))}
</Suggestions>
```

### Tool

Display tool calls and results.

```tsx
import { Tool, ToolContent, ToolResult } from '@/components/ai-elements/tool';

<Tool name="search_web">
  <ToolContent>
    Searching for: {tool.args.query}
  </ToolContent>
  <ToolResult>
    {tool.result}
  </ToolResult>
</Tool>
```

### Checkpoint (Restore Points)

Mark and restore conversation history.

```tsx
import {
  Checkpoint,
  CheckpointIcon,
  CheckpointTrigger,
} from '@/components/ai-elements/checkpoint';

<Checkpoint>
  <CheckpointIcon />
  <CheckpointTrigger onClick={() => restoreToCheckpoint(index)}>
    Restore to this point
  </CheckpointTrigger>
</Checkpoint>
```

---

## Citation Components

### Sources

Collapsible source citations.

```tsx
import {
  Sources,
  SourcesTrigger,
  SourcesContent,
  Source,
} from '@/components/ai-elements/sources';

<Sources>
  <SourcesTrigger count={3} />
  <SourcesContent>
    <Source href="https://docs.example.com/api" title="API Documentation" />
    <Source href="https://example.com/guide" title="Getting Started Guide" />
    <Source href="https://example.com/faq" title="FAQ" />
  </SourcesContent>
</Sources>
```

### Inline Citation

Citations within text content.

```tsx
import { InlineCitation } from '@/components/ai-elements/inline-citation';

<p>
  According to the documentation
  <InlineCitation href="https://docs.example.com" index={1} />
  , you should...
</p>
```

---

## Loading Components

### Queue

Message queue/loading state.

```tsx
import { Queue } from '@/components/ai-elements/queue';

<Queue>Processing your request...</Queue>
```

### Shimmer

Skeleton loading placeholder.

```tsx
import { Shimmer } from '@/components/ai-elements/shimmer';

{isLoading && <Shimmer className="h-20 w-full" />}
```

---

## Utility Components

### Model Selector

Switch between AI models.

```tsx
import { ModelSelector } from '@/components/ai-elements/model-selector';

<ModelSelector
  models={['gpt-4', 'claude-3', 'gemini-pro']}
  selected={model}
  onSelect={setModel}
/>
```

### Context

Display context information.

```tsx
import { Context } from '@/components/ai-elements/context';

<Context title="Current Context">
  Working on: Project Alpha
  Files: 3 selected
</Context>
```

---

## Complete Chat Example

```tsx
'use client';

import { useState } from 'react';
import { useChat } from 'ai/react';
import {
  Conversation,
  ConversationContent,
  ConversationEmptyState,
  ConversationScrollButton,
} from '@/components/ai-elements/conversation';
import { Message, MessageContent } from '@/components/ai-elements/message';
import { PromptInput } from '@/components/ai-elements/prompt-input';
import { Reasoning, ReasoningTrigger, ReasoningContent } from '@/components/ai-elements/reasoning';
import { Suggestions, Suggestion } from '@/components/ai-elements/suggestion';
import { Sources, SourcesTrigger, SourcesContent, Source } from '@/components/ai-elements/sources';

export function Chat() {
  const { messages, input, setInput, handleSubmit, isLoading } = useChat();

  const suggestions = [
    'What can you help me with?',
    'Tell me about AI SDK',
    'How do I get started?',
  ];

  return (
    <div className="flex h-screen flex-col">
      <Conversation className="flex-1">
        <ConversationContent className="p-4">
          {messages.length === 0 ? (
            <>
              <ConversationEmptyState
                title="Welcome!"
                description="Ask me anything to get started"
              />
              <Suggestions className="mt-4">
                {suggestions.map((s) => (
                  <Suggestion key={s} suggestion={s} onClick={setInput} />
                ))}
              </Suggestions>
            </>
          ) : (
            messages.map((msg) => (
              <Message key={msg.id} from={msg.role}>
                <MessageContent>{msg.content}</MessageContent>

                {/* Show reasoning if available */}
                {msg.reasoning && (
                  <Reasoning isStreaming={isLoading && msg.id === messages.at(-1)?.id}>
                    <ReasoningTrigger />
                    <ReasoningContent>{msg.reasoning}</ReasoningContent>
                  </Reasoning>
                )}

                {/* Show sources if available */}
                {msg.sources?.length > 0 && (
                  <Sources>
                    <SourcesTrigger count={msg.sources.length} />
                    <SourcesContent>
                      {msg.sources.map((src, i) => (
                        <Source key={i} href={src.url} title={src.title} />
                      ))}
                    </SourcesContent>
                  </Sources>
                )}
              </Message>
            ))
          )}
        </ConversationContent>
        <ConversationScrollButton />
      </Conversation>

      <form onSubmit={handleSubmit} className="border-t p-4">
        <PromptInput
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          disabled={isLoading}
        />
      </form>
    </div>
  );
}
```

---

## Styling

All components accept `className` prop for Tailwind customization:

```tsx
<Message className="bg-muted/50 rounded-lg p-4">
  <MessageContent className="text-sm">{content}</MessageContent>
</Message>

<Reasoning className="border-l-2 border-blue-500 pl-4">
  <ReasoningTrigger className="text-blue-600" />
  <ReasoningContent className="text-muted-foreground" />
</Reasoning>
```

---

## Integration with AI SDK

These components work seamlessly with Vercel AI SDK hooks:

```tsx
import { useChat } from 'ai/react';
import { useCompletion } from 'ai/react';
import { useAssistant } from 'ai/react';

// useChat for conversational interfaces
const { messages, input, handleSubmit } = useChat();

// useCompletion for single completions
const { completion, complete } = useCompletion();

// useAssistant for OpenAI Assistants
const { messages, submitMessage } = useAssistant();
```

---

## Reference

See `references/component-api.md` for complete props documentation.
