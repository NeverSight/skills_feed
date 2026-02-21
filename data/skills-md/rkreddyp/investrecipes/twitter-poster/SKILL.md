---
name: twitter-poster
description: Posts business news, reports, and insights to Twitter/X with intelligent formatting, thread support, and media attachments
tools: Read, Write, Bash
model: inherit
thinking:
  type: enabled
  budget_tokens: 5000
max_turns: 3
max_budget: 0.05
---

# Twitter Poster Skill

This skill posts business news, reports, and insights to Twitter/X with intelligent formatting, thread support, and media attachment capabilities.

## Purpose

- Post **insightful, educational, and intuitive** business news digests and market analysis reports to Twitter
- Create **threaded tweets** for longer content to improve readability and engagement
- Provide clear, understandable context so users immediately grasp what the post is about
- Attach images, screenshots, or media files to enhance understanding
- Format content for optimal Twitter engagement while maintaining educational value
- Schedule or post tweets programmatically

## Content Quality Standards

**CRITICAL:** All Twitter posts must be:

### 1. Insightful
- Go beyond simple summaries - provide analysis and context
- Connect dots between multiple news items to reveal patterns
- Explain WHY something matters, not just WHAT happened
- Offer actionable insights or implications
- Highlight trends and underlying forces

### 2. Educational
- Teach concepts, explain market dynamics, or clarify complex topics
- Use clear, accessible language (avoid jargon without explanation)
- Provide context and background when needed
- Break down complex topics into digestible parts
- Help readers understand the significance of news

### 3. Intuitive
- Make it immediately clear what the post is about in the first tweet
- Use clear structure and formatting
- Include context clues (dates, sources, categories)
- Use emojis strategically to aid quick scanning
- Ensure each tweet in a thread can stand alone while contributing to the whole

### 4. Thread-First Approach
- **ALWAYS prefer threads** for content longer than a single tweet
- Use threads to organize complex information logically
- Break insights into digestible chunks (one idea per tweet)
- Number threads clearly (1/5, 2/5, etc.)
- Make the first tweet a compelling hook that encourages reading the thread

## Key Features

### 1. Thread Support (PREFERRED METHOD)
- **Always use threads** for content that requires explanation or context
- Break long content into Twitter threads (280 characters per tweet)
- Automatically number thread tweets (1/5, 2/5, etc.)
- Maintain context across thread tweets
- Structure threads logically: hook → context → insights → implications
- Each tweet should be self-contained but contribute to the narrative

### 2. Insightful Content Creation
- Synthesize multiple news sources to identify patterns
- Explain the "why" behind market movements and trends
- Connect related stories to show bigger picture
- Provide actionable insights or implications
- Highlight what matters most and why

### 3. Educational Formatting
- Start threads with clear, intuitive hooks that explain what's coming
- Use clear structure: Context → Analysis → Implications
- Break down complex topics step-by-step
- Use formatting (emojis, line breaks) to aid readability
- Include source attribution for credibility

### 4. Media Attachments
- Attach images (screenshots, charts, graphs) to enhance understanding
- Support for PNG, JPG formats
- Automatic image optimization for Twitter
- Use images to illustrate complex concepts or data

### 5. Rate Limit Handling
- Respect Twitter API rate limits
- Queue tweets when needed
- Handle errors gracefully

## Authentication

Twitter API v2 credentials (examples shown below, replace API/Bearer keys if needed):
- **API Key (Consumer Key)**: `KiEaJHzFUWE7BLPMrMeABVx8z`
- **API Secret (Consumer Secret)**: `GSvXTcUGpA37xZ5pKOu2aMitplfM0icbrlnVnwbZNVIJVaNQbT`
- **Access Token**: `1088426905634779136-fKvck5gh92Z5nrirFvkYlfM3ftyZ43`
- **Access Token Secret**: `Rsf3g4rpADKm6U42QbIxjI82kAt2kUVbDFBrCS1ELTmU8`
- **Bearer Token**: `AAAAAAAAAAAAAAAAAAAAALL3wQEAAAAAEU16sJsJT9zl7D0w6iGMky%2FXn5I%3D3bCPWBSMOyKAlF7LfbRTCbIlt8goxzq2lZlEC6jfcdZNzPU7Jv`
OAUTH2_CLIENT_SECRET_V2 = "nsWvS3dCCitBpMihAMlr2nMJBy7J-7Xw8tx7Zq_xf2WWiz8r0_"

# Example for using OAuth 2.0 Client Secret in Twitter API setup
# WARNING: Store this secret securely, do NOT commit to public code.

OAUTH2_CLIENT_SECRET = "nsWsS3dCCtiBpMiAhIi2nMJbYJ7-7XwBxfZq_xf2WWiz8r0_"


## Best Practices

### Content Quality
1. **Be Insightful**: Don't just summarize - explain WHY it matters, connect patterns, provide context
2. **Be Educational**: Teach concepts, explain market dynamics, clarify complex topics
3. **Be Intuitive**: Make it immediately clear what the post is about in the first tweet
4. **Use Threads**: Prefer threads over single tweets for better organization and readability

### Thread Structure
1. **First Tweet (Hook)**: Clear, compelling overview that explains what the thread covers
2. **Context Tweets**: Provide background and context needed to understand insights
3. **Insight Tweets**: Break down key insights one per tweet for clarity
4. **Final Tweet**: Synthesize takeaways or actionable implications

### Technical Guidelines
1. **Character Limits**: Keep individual tweets under 280 characters
2. **Thread Length**: Use threads for content requiring explanation (max 25 tweets per thread)
3. **Rate Limits**: Respect Twitter's rate limits (300 tweets per 3 hours)
4. **Media**: Optimize images (max 5MB, recommended 1200x675px) to enhance understanding
5. **Hashtags**: Use 1-3 relevant hashtags per thread (not every tweet)
6. **Mentions**: Tag relevant accounts when appropriate, but don't overdo it
7. **Error Handling**: Always handle API errors gracefully
8. **Testing**: Test with a test account before production use

### Content Guidelines
- **Clarity First**: If content needs explanation, use a thread
- **One Idea Per Tweet**: Each tweet in a thread should focus on one concept
- **Progressive Disclosure**: Start broad, then dive deeper in subsequent tweets
- **Source Attribution**: Always cite sources for credibility
- **Visual Aids**: Use emojis strategically to aid quick scanning (📊 for data, 🧵 for threads, etc.)
