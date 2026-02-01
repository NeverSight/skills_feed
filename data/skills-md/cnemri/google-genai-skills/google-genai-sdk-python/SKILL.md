---
name: google-genai-sdk-python
description: Expert guidance for writing Python code using the official Google GenAI SDK (google-genai) for Gemini API and Vertex AI. Use for text generation, multimodal inputs, reasoning, tools, and media generation.
---

# Google GenAI Python SDK Skill

Use this skill to write high-quality, idiomatic Python code for the Gemini API.

## Reference Materials

Identify the user's task and refer to the relevant file:

- **[Setup & Client](references/setup.md)**: Installation, auth, client initialization.
- **[Models](references/models.md)**: Recommended models (Flash, Pro, Lite, Imagen, Veo).
- **[Text Generation](references/text_generation.md)**: Basic inference, streaming, system instructions, safety.
- **[Chat](references/chat.md)**: Multi-turn conversations and history.
- **[Reasoning](references/reasoning.md)**: Thinking config (`thinking_level` / `thinking_budget`), thought signatures.
- **[Structured Output](references/structured_output.md)**: JSON schemas, Pydantic models, Enums.
- **[Multimodal Inputs](references/multimodal_inputs.md)**: Images, audio, video, PDFs, media resolution.
- **[Tools](references/tools.md)**: Function calling, code execution, Google Search grounding.
- **[Media Generation](references/media_generation.md)**: Image generation/editing (Imagen), video generation (Veo).
- **[Source Code](references/source_code.md)**: Raw SDK source code for deep inspection.

## Core Principles

1.  **Unified SDK**: Always use `google-genai`.
2.  **Stateless Models**: Use `client.models` for single requests.
3.  **Stateful Chats**: Use `client.chats` for conversations.
4.  **Types**: Import from `google.genai.types`.