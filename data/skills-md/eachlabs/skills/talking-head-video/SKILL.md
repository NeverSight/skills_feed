---
name: talking-head-video
description: Generate talking head videos using each::sense AI. Create AI presenters, lip-sync avatars, corporate spokespersons, training videos, and multi-language content from photos, scripts, or audio files.
metadata:
  author: eachlabs
  version: "1.0"
---

# Talking Head Video Generation

Generate professional talking head videos using each::sense. This skill transforms static photos into lifelike talking videos, creates AI presenters from scripts, and enables lip-sync capabilities for various use cases.

## Features

- **AI Presenter from Script**: Generate talking head videos from text scripts
- **Photo to Talking Video**: Animate static portraits with speech
- **Lip Sync to Audio**: Synchronize lip movements to existing audio tracks
- **Corporate Spokesperson**: Professional business presentation videos
- **Training Video Presenter**: Educational and onboarding content
- **News Anchor Style**: Broadcast-quality presenter videos
- **Product Explainer**: Demo and tutorial presenter videos
- **Multi-Language Support**: Generate content in multiple languages
- **Custom Avatar Presenter**: Personalized AI spokesperson creation
- **Emotional Expression Control**: Varied expressions and delivery styles

## Quick Start

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a talking head video of a professional presenter saying: Welcome to our company. We are excited to have you join our team today.",
    "mode": "max"
  }'
```

## Video Output Specifications

| Type | Resolution | Aspect Ratio | Duration | Use Case |
|------|------------|--------------|----------|----------|
| Portrait | 1080x1920 | 9:16 | Up to 60s | Social media, mobile |
| Landscape | 1920x1080 | 16:9 | Up to 60s | YouTube, presentations |
| Square | 1080x1080 | 1:1 | Up to 60s | Social media feed |
| Headshot | 720x720 | 1:1 | Up to 30s | Quick clips, GIFs |

## Use Case Examples

### 1. AI Presenter from Script

Generate a talking head video from a text script with an AI-generated presenter.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a talking head video with a professional female presenter in business attire. She should say: Welcome to our quarterly earnings report. This quarter we achieved record growth across all market segments. Our revenue increased by 25 percent compared to last year. Speaking style should be confident and authoritative.",
    "mode": "max"
  }'
```

### 2. Photo to Talking Video

Transform a static portrait photo into an animated talking video.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Animate this photo to create a talking head video. The person should say: Hello, I am Dr. Sarah Chen, and I will be guiding you through todays medical seminar. Please ensure you have your notes ready. Make the lip movements natural and add subtle head movements.",
    "mode": "max",
    "image_urls": ["https://example.com/portrait-photo.jpg"]
  }'
```

### 3. Lip Sync to Audio

Synchronize a portrait photo or video with an existing audio track.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a lip-sync video using this portrait photo and audio file. Synchronize the lip movements perfectly to the speech. Add natural blinking and subtle expressions that match the audio tone.",
    "mode": "max",
    "image_urls": ["https://example.com/presenter-headshot.jpg"],
    "audio_url": "https://example.com/voiceover-script.mp3"
  }'
```

### 4. Corporate Spokesperson Video

Create professional business spokesperson content for corporate communications.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a corporate spokesperson video. Middle-aged professional male in a suit, neutral office background. Script: At TechCorp, we believe in innovation that matters. Our commitment to sustainability drives everything we do. Join us in building a better tomorrow. Delivery should be warm, trustworthy, and professional. 16:9 aspect ratio for website embedding.",
    "mode": "max"
  }'
```

### 5. Training Video Presenter

Generate educational and onboarding video content with an AI instructor.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a training video presenter. Friendly instructor appearance, casual professional attire. Script: Welcome to module three of your safety training. Today we will cover emergency procedures. First, locate your nearest exit. Second, familiarize yourself with the evacuation route. Remember, safety is everyones responsibility. Tone should be clear, encouraging, and educational.",
    "mode": "max"
  }'
```

### 6. News Anchor Style Video

Create broadcast-quality news presenter videos.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Generate a news anchor style talking head video. Professional female news presenter, polished appearance, studio background with subtle graphics. Script: Good evening. Tonight we bring you breaking coverage of the technology summit where world leaders announced new AI guidelines. Industry experts call this a historic moment. Speaking style should be authoritative, clear, and broadcast-professional.",
    "mode": "max"
  }'
```

### 7. Product Explainer Presenter

Create product demonstration and explainer videos with an AI host.

```bash
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a product explainer video with a talking head presenter. Young, energetic tech reviewer appearance. Script: Let me show you the amazing features of the new SmartWatch Pro. This device tracks your heart rate, monitors sleep patterns, and even measures stress levels. The battery lasts seven days on a single charge. Its a game-changer for fitness enthusiasts. Delivery should be enthusiastic and engaging, like a YouTube tech review.",
    "mode": "max"
  }'
```

### 8. Multi-Language Presenter

Generate talking head content in multiple languages for international audiences.

```bash
# English version
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a talking head video in English. Professional presenter appearance. Script: Welcome to our global platform. We connect businesses across continents. Keep the same presenter appearance for consistency with other language versions.",
    "session_id": "multilang-campaign-001",
    "mode": "max"
  }'

# Spanish version (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create the same talking head video but in Spanish. Use the same presenter from the previous video. Script: Bienvenidos a nuestra plataforma global. Conectamos empresas a traves de los continentes. Match the tone and delivery style of the English version.",
    "session_id": "multilang-campaign-001",
    "mode": "max"
  }'

# French version (same session for consistency)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create the French version with the same presenter. Script: Bienvenue sur notre plateforme mondiale. Nous connectons les entreprises a travers les continents. Maintain visual consistency with previous versions.",
    "session_id": "multilang-campaign-001",
    "mode": "max"
  }'
```

### 9. Custom Avatar Presenter

Create a personalized AI avatar spokesperson for consistent brand representation.

```bash
# Initial avatar creation
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a custom AI avatar presenter for our brand. Female, late 20s, professional but approachable appearance, dark hair, wearing a navy blazer. This will be our consistent brand spokesperson. Generate a reference image first.",
    "session_id": "brand-avatar-001",
    "mode": "max"
  }'

# Use avatar for video
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a talking head video using this avatar. Script: Hi, I am Maya, your AI assistant from TechBrand. I am here to help you get the most out of our products. Lets explore what we can do together. Keep her appearance consistent with the avatar we created.",
    "session_id": "brand-avatar-001",
    "mode": "max"
  }'
```

### 10. Emotional Expression Variations

Generate talking head videos with specific emotional expressions and delivery styles.

```bash
# Empathetic customer service
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a talking head video with empathetic expression. Customer service representative appearance. Script: We understand this has been a frustrating experience for you. Your satisfaction is our top priority. Let me personally ensure we resolve this issue today. Expression should convey genuine concern, understanding, and warmth. Soft, caring tone.",
    "session_id": "expression-variations",
    "mode": "max"
  }'

# Excited product launch
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Now create a talking head video with excited, energetic expression. Same presenter. Script: I am thrilled to announce our biggest launch ever! This is the moment weve all been waiting for. Get ready to experience something incredible. Expression should show genuine excitement, big smile, energetic delivery with dynamic gestures.",
    "session_id": "expression-variations",
    "mode": "max"
  }'

# Serious announcement
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a talking head video with serious, professional expression. Same presenter. Script: We need to address some important changes to our policies. Effective immediately, all accounts will require two-factor authentication. This measure protects your data and ensures platform security. Expression should be serious, authoritative, but not alarming. Measured, deliberate delivery.",
    "session_id": "expression-variations",
    "mode": "max"
  }'
```

## Best Practices

### Script Writing
- **Keep it conversational**: Write scripts as natural speech, not formal text
- **Use contractions**: "We're" instead of "We are" for natural delivery
- **Break into segments**: For longer content, split into multiple shorter clips
- **Include pauses**: Use commas and periods to indicate natural pauses
- **Avoid jargon**: Unless your audience expects technical terminology

### Visual Quality
- **High-resolution source**: Use clear, well-lit portrait photos for lip-sync
- **Front-facing angle**: Best results with subjects looking at camera
- **Neutral expression**: Starting images work best with neutral or slight smile
- **Clean background**: Simpler backgrounds produce cleaner results

### Audio Considerations
- **Clear audio source**: Use high-quality audio for lip-sync features
- **Consistent volume**: Normalize audio levels before processing
- **Natural pace**: Speech that's too fast may affect lip-sync quality

### Brand Consistency
- **Use session_id**: Maintain consistency across multiple videos
- **Document appearance**: Keep notes on presenter descriptions for future use
- **Standardize backgrounds**: Use consistent settings for brand recognition

## Prompt Tips for Talking Head Videos

When creating talking head content, include these details in your prompt:

1. **Presenter Appearance**: Age, gender, attire, professional style
2. **Script**: The exact text to be spoken
3. **Tone/Delivery**: Professional, friendly, energetic, serious, etc.
4. **Background**: Office, studio, neutral, custom environment
5. **Aspect Ratio**: 16:9, 9:16, or 1:1 based on platform
6. **Emotional Expression**: Neutral, happy, serious, empathetic
7. **Language**: Specify language and accent if needed

### Example Prompt Structure

```
"Create a talking head video with [presenter description].
Background: [setting/environment].
Script: [exact text to be spoken].
Delivery style: [tone and expression].
Format: [aspect ratio] for [platform/use case]."
```

## Mode Selection

Ask your users before generating:

**"Do you want fast & cheap, or high quality?"**

| Mode | Best For | Speed | Quality |
|------|----------|-------|---------|
| `max` | Final production videos, client deliverables | Slower | Highest |
| `eco` | Quick drafts, script testing, concept review | Faster | Good |

## Multi-Turn Video Iteration

Use `session_id` to iterate on talking head videos:

```bash
# Initial video
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a talking head video with a professional presenter for a tech company intro",
    "session_id": "company-intro-video"
  }'

# Iterate based on feedback
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Make the presenter look younger and more approachable, change to casual business attire",
    "session_id": "company-intro-video"
  }'

# Update script
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Same presenter, but change the script to: Hey there! Welcome to InnovateTech. Were a team of passionate builders creating the future of AI. Ready to join us?",
    "session_id": "company-intro-video"
  }'
```

## Video Series Generation

Create consistent video series for courses or campaigns:

```bash
# Module 1
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create a training series presenter. Instructor appearance, friendly and knowledgeable. Module 1 script: Welcome to the Python fundamentals course. In this first module, we will cover variables and data types. By the end, you will write your first Python program.",
    "session_id": "python-course-series",
    "mode": "max"
  }'

# Module 2 (same presenter)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Same instructor for Module 2. Script: Welcome back. Today we dive into control flow. You will learn about if statements, loops, and how to make your programs make decisions. Lets get started.",
    "session_id": "python-course-series",
    "mode": "max"
  }'

# Module 3 (same presenter)
curl -X POST https://sense.eachlabs.run/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Continue with Module 3, same instructor. Script: Great progress so far. Module 3 covers functions. Functions help you organize code and avoid repetition. This is where your code starts to feel professional.",
    "session_id": "python-course-series",
    "mode": "max"
  }'
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to create prediction: HTTP 422` | Insufficient balance | Top up at eachlabs.ai |
| Content policy violation | Prohibited content | Adjust prompt to comply with content policies |
| Timeout | Complex generation | Set client timeout to minimum 10 minutes |
| Low quality source image | Image too small or blurry | Use high-resolution, clear portrait photos |
| Audio sync issues | Audio quality problems | Use clear, consistent audio files |

## Related Skills

- `each-sense` - Core API documentation
- `voice-audio` - Voice generation and audio processing
- `video-generation` - General video creation
- `image-generation` - Portrait and avatar image creation
