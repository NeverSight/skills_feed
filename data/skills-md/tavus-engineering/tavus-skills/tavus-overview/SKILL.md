---
name: tavus-overview
description: Overview of Tavus, the AI research lab pioneering human computing. Use when you need context about what Tavus is, their mission, core concepts like CVI and Human Computing, the model stack (Phoenix, Raven, Sparrow), or links to docs/platform/resources.
---

# Tavus Overview

Tavus is a San Francisco-based AI research lab pioneering **Human Computing** — teaching machines the art of being human.

## Mission

> "Automation has scaled efficiency but stripped away empathy, nuance, and presence from digital interactions."

Tavus exists to close the gap between humans and machines by creating AI that can see, hear, understand, and respond with emotional intelligence in real time. Not chatbots with faces — authentic, face-to-face digital presence.

## What is Human Computing?

Human Computing is a paradigm shift: computing that adapts to humans, not the other way around.

**Core principles:**
- **Human UI**: Interact with AI as naturally as talking to another person — no commands, no learning curve
- **Presence over automation**: AI that feels like *someone*, not *something*
- **Emotional intelligence**: Reading tone, expressions, context — not just words

## The Conversational Video Interface (CVI)

CVI is Tavus's flagship product — an API-first platform for real-time, face-to-face AI conversations.

**What makes CVI different from chatbots/avatars:**
- Real-time interactive conversation (not pre-rendered video)
- ~600ms latency utterance-to-utterance
- Reads facial expressions, interprets tone, adapts in real-time
- Full orchestration: function calling, RAG, memories
- White-labeled, embeddable, enterprise-ready

**CVI Components:**
| Component | What it does |
|-----------|--------------|
| **Replica** | The visual avatar — your AI's face and appearance |
| **Persona** | Behavior, personality, LLM config, system prompt |
| **Conversation** | A live WebRTC session connecting replica + persona |

## The Model Stack

Tavus builds proprietary models that work together to create human presence:

### Phoenix-4 (Rendering)
Gaussian-diffusion model for photorealistic face rendering. Synthesizes high-fidelity facial behavior with:
- Micro-expressions and subtle movements
- Full-face animation (not just lips)
- Real-time emotional response
- Identity preservation

### Raven-1 (Perception)
Multimodal perception model that lets AI "see":
- Reads facial expressions and body language
- Detects emotions and intent
- Analyzes environment and screen content
- Contextual awareness

### Sparrow-1 (Turn-Taking)
Transformer-based dialogue model for natural conversation flow:
- Knows when to listen, pause, or speak
- ~600ms response latency
- Handles interruptions naturally
- Multilingual support

## Products

### Conversational Video Interface (CVI)
API-first platform for developers to embed real-time AI video conversations.
- Full pipeline: perception → STT → LLM → TTS → rendering
- Customizable layers (bring your own LLM/TTS)
- Knowledge base (RAG) and memories
- Function calling for external integrations

### Video Generation API
Async video generation from scripts or audio.
- Personalized videos at scale
- Custom backgrounds and watermarks
- Transparent background support

### Replica API
Create digital twins from 2 minutes of training video.
- Studio-grade fidelity
- Stock replicas available
- Identity preservation

### PALs (Personal AI Lifeforms)
Consumer-facing AI companions that remember, evolve, and connect.
- Text, call, or video chat
- Persistent memory
- Proactive check-ins

## Use Cases

- **Sales & Recruiting**: AI SDRs, interviewers, qualification flows
- **Education**: Tutors, trainers, onboarding
- **Healthcare**: Patient companions, training simulations
- **Customer Support**: 24/7 face-to-face assistance
- **Personal**: Companions, coaches, productivity assistants

## Key Stats

- 2B+ interactions powered
- ~600ms utterance-to-utterance latency
- 30+ languages supported
- SOC 2, GDPR, HIPAA compliant (enterprise)

## Links

### Platform & Docs
- **Homepage**: https://www.tavus.io
- **Developer Portal**: https://platform.tavus.io
- **Documentation**: https://docs.tavus.io
- **API Reference**: https://docs.tavus.io/api-reference/overview
- **CVI Overview**: https://docs.tavus.io/sections/conversational-video-interface/overview-cvi

### Resources
- **Research**: https://www.tavus.io/research
- **Blog**: https://www.tavus.io/blog
- **Example Projects**: https://github.com/Tavus-Engineering/tavus-examples
- **Status**: https://status.tavus.io

### Community
- **Discord**: https://discord.gg/5Y9Er6WNN5
- **GitHub**: https://github.com/Tavus-Engineering

### Getting Started
- **Sign Up**: https://platform.tavus.io/auth/sign-up?is_developer=true
- **Free Tier**: 25 conversational minutes + stock replicas

## Company

- **Founded**: 2021 by Hassaan Raza & Quinn Favret
- **HQ**: San Francisco
- **Backed by**: Sequoia, Scale Venture Partners, Y Combinator, HubSpot
- **Category**: Human Computing / AI Research Lab

## Pricing Tiers

| Tier | Minutes | Replicas | Concurrency |
|------|---------|----------|-------------|
| Free | 25 | Stock only | 1 |
| Starter ($59/mo) | 100 | 1 custom | 3 |
| Growth ($397/mo) | 1,250 | 3 custom | 15 |
| Enterprise | Custom | Custom | Custom + SLAs |

## Ethics & Trust

Tavus is built on:
- **Informed consent**: Every likeness used with permission
- **Transparent systems**: No hidden levers
- **Full disclosure**: You know how the magic works
- **Bias reviews**: Active monitoring and advisory oversight
