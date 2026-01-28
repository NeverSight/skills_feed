---
name: gemini-to-seedream-migration
description: |
  Migrate AI image generation from Google Gemini 2.5 Flash to BytePlus SeeDream v4.5. 
  Use when: (1) User wants to switch from Gemini to SeeDream/BytePlus for image generation,
  (2) User asks about migrating image generation APIs or replacing Gemini with BytePlus,
  (3) User needs cost optimization or better image quality for AI-generated images,
  (4) User mentions SeeDream, BytePlus, or wants SDK-to-REST API migration for image generation
---

# Gemini to SeeDream v4.5 Migration

Migrate AI image generation from Google Gemini 2.5 Flash Image to BytePlus SeeDream v4.5 with this proven, production-ready workflow.

## Quick Start

**Migration Overview:**
- Replace Gemini SDK with BytePlus REST API
- Update environment variables and validation
- Migrate API routes to new client
- Test and validate changes
- Update documentation

**Benefits:**
- Higher resolution support (up to 4K vs 2K)
- Better control over image dimensions and generation
- Built-in prompt optimization for quality improvement
- Potentially lower costs (check BytePlus pricing)
- Broader format support (adds BMP, TIFF, GIF)

**Prerequisites:**
- Existing project using Google Gemini 2.5 Flash Image
- BytePlus API key (get from https://console.byteplus.com/ark/region:ark+ap-southeast-1/apiKey)
- TypeScript/JavaScript project with image generation endpoints

**Time Estimate:** 3-4 hours for complete migration

---

## Core Migration Workflow

### Phase 1: Environment Setup

Replace Gemini environment variables with BytePlus configuration.

#### Step 1.1: Update .env.example

Find and remove Gemini configuration:
```bash
# REMOVE
GEMINI_API_KEY=your_google_ai_api_key_here
```

Add BytePlus configuration:
```bash
# ADD
BYTEPLUS_API_KEY=your_byteplus_api_key_here
```

#### Step 1.2: Update Environment Validator

If you have environment validation (recommended), update it to check for `BYTEPLUS_API_KEY` instead of `GEMINI_API_KEY`.

Example changes:
```typescript
// OLD
{
  name: 'GEMINI_API_KEY',
  required: true,
  description: 'Google AI API key for image generation',
  setupUrl: 'https://aistudio.google.com/app/apikey',
}

// NEW
{
  name: 'BYTEPLUS_API_KEY',
  required: true,
  description: 'BytePlus SeeDream API key for image generation',
  setupUrl: 'https://console.byteplus.com/ark/region:ark+ap-southeast-1/apiKey',
}
```

#### Step 1.3: Add API Key to Local Environment

Add to your `.env.local`:
```bash
BYTEPLUS_API_KEY=your_actual_byteplus_api_key
```

#### Step 1.4: Verify Environment

Test that validation detects the new key correctly:
```bash
npm run validate  # or your validation command
```

---

### Phase 2: Create BytePlus Client

Create a reusable REST API client for BytePlus SeeDream v4.5.

#### Step 2.1: Create Client File

Create `lib/byteplus-client.ts` (or appropriate path for your project).

See **[references/client-template.ts](references/client-template.ts)** for a fully commented, production-ready template.

**Key implementation points:**
- Use native `fetch` API (no SDK required)
- Convert base64 to data URI format: `data:image/png;base64,${base64String}`
- Add comprehensive error handling for all HTTP status codes
- Validate API key before making requests
- Include verbose logging for debugging
- Return consistent interface matching your app's expectations

#### Step 2.2: Configure Model Parameters

Choose appropriate parameters for your use case:

**Model ID:** `seedream-4-5-251128` (latest as of Dec 2025)

**Size options:**
- Fixed pixels: `2048x2560` (portrait), `2560x2048` (landscape), `2048x2048` (square)
- Semantic: `2K`, `4K` (model determines exact dimensions)

**Prompt optimization:**
- `mode: "standard"` - Higher quality, slower (~45-60s)
- `mode: "fast"` - Good quality, faster (~15-30s)

**Other settings:**
- `sequential_image_generation: "disabled"` - Single image output
- `watermark: false` - No watermark
- `response_format: "b64_json"` - Base64 response

#### Step 2.3: Test Client

Create a simple test to verify the client works:
```typescript
const result = await generateImageWithByteplus({
  prompt: "A simple test image of a red circle",
  images: [] // or test images
})

console.log(result.imageUrl ? "Success!" : result.error)
```

---

### Phase 3: Migrate API Routes

Replace Gemini SDK calls with BytePlus client in all API routes.

#### Step 3.1: Remove Gemini Imports

In each API route file:
```typescript
// REMOVE
import { GoogleGenAI } from "@google/genai"
```

Add BytePlus import:
```typescript
// ADD
import { generateImageWithByteplus } from "@/lib/byteplus-client"
```

#### Step 3.2: Replace Generation Calls

**Before (Gemini SDK):**
```typescript
const genAI = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! })

const result = await genAI.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: [{
    role: "user",
    parts: [
      { text: prompt },
      { inlineData: { mimeType: "image/png", data: base64Image1 } },
      { inlineData: { mimeType: "image/jpeg", data: base64Image2 } }
    ]
  }],
  config: {
    responseModalities: ["IMAGE"],
    imageConfig: { aspectRatio: "4:5" }
  }
})

// Extract image from candidates
const imagePart = result.candidates[0].content.parts.find(p => p.inlineData)
const base64Image = `data:${imagePart.inlineData.mimeType};base64,${imagePart.inlineData.data}`
```

**After (BytePlus REST):**
```typescript
const result = await generateImageWithByteplus({
  prompt: prompt,
  images: [
    { data: base64Image1, mimeType: "image/png" },
    { data: base64Image2, mimeType: "image/jpeg" }
  ]
})

if (result.error) {
  return NextResponse.json({ error: result.error }, { status: 500 })
}

// Image already in data URI format
const base64Image = result.imageUrl
```

#### Step 3.3: Handle Response Differences

BytePlus doesn't return text alongside images. If your frontend expects both:
```typescript
return NextResponse.json({
  imageUrl: result.imageUrl,
  text: "", // BytePlus doesn't generate text
  usage: result.usage
})
```

#### Step 3.4: Update Logging

Replace Gemini-specific log messages:
```typescript
// OLD
console.log("[v0] Gemini API key available:", !!process.env.GEMINI_API_KEY)
console.log("[v0] Calling Gemini API...")

// NEW
console.log("[v0] BytePlus API key available:", !!process.env.BYTEPLUS_API_KEY)
console.log("[v0] Calling BytePlus SeeDream v4.5 API...")
```

---

### Phase 4: Dependency Cleanup

Remove Gemini SDK from project dependencies.

#### Step 4.1: Uninstall Gemini SDK

```bash
npm uninstall @google/genai
```

This automatically updates `package.json` and `package-lock.json`.

#### Step 4.2: Verify Removal

Check that Gemini is no longer referenced:
```bash
grep -i "genai\|gemini" package.json
```

Expected: No matches (empty output).

#### Step 4.3: Rebuild

```bash
npm install
npx tsc --noEmit  # Verify no type errors
```

---

### Phase 5: Testing & Validation

See **[references/testing-checklist.md](references/testing-checklist.md)** for comprehensive testing guide.

**Quick validation:**
1. Environment validation passes: `npm run validate`
2. TypeScript compiles: `npx tsc --noEmit`
3. Linting passes: `npm run lint`
4. Build succeeds: `npm run build`
5. Manual API test generates images correctly

**Test scenarios:**
- Happy path: Valid images + prompt → generates image
- Invalid API key → Returns 401 with clear message
- Missing images → Returns 400 error
- Rate limit → Returns 429 with retry message
- Service error → Returns 500 with retry message

---

### Phase 6: Documentation Updates

Update all documentation to reflect BytePlus instead of Gemini.

**Files to update:**
- README.md - Replace "Gemini 2.5 Flash" with "BytePlus SeeDream v4.5"
- SETUP.md - Update API key setup instructions
- ARCHITECTURE.md - Update AI integration section
- Any troubleshooting guides - Update error codes and debugging steps

**Search for remaining references:**
```bash
grep -ri "gemini\|google ai" *.md docs/*.md
```

---

## Key Differences: Gemini vs BytePlus

See **[references/api-comparison.md](references/api-comparison.md)** for detailed parameter mapping.

**Quick comparison:**

| Aspect | Gemini 2.5 Flash | BytePlus SeeDream v4.5 |
|--------|------------------|------------------------|
| Integration | SDK (`@google/genai`) | REST API (native `fetch`) |
| Auth | API key in constructor | Bearer token in header |
| Image input | Base64 in `inlineData` | Data URI in `image` array |
| Resolution | Aspect ratio (`4:5`) | Exact pixels (`2048x2560`) |
| Response | `candidates[].content.parts[]` | `data[0].b64_json` |
| Text output | Supported | Not supported |

---

## Common Pitfalls

See **[references/troubleshooting.md](references/troubleshooting.md)** for detailed solutions.

**Common mistakes:**
1. **Forgetting data URI format** - BytePlus requires `data:image/png;base64,...` not plain base64
2. **Wrong model ID** - Use `seedream-4-5-251128` not `seedream-4.5`
3. **Missing error handling** - Handle all HTTP status codes (400, 401, 429, 500)
4. **Not validating API key** - Check key exists before making requests
5. **Incorrect image format** - Ensure images are in supported formats (PNG/JPEG/WEBP)

---

## Quick Reference

### Gemini SDK Pattern
```typescript
import { GoogleGenAI } from "@google/genai"

const genAI = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY! })

const result = await genAI.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: [{
    role: "user",
    parts: [
      { text: prompt },
      { inlineData: { mimeType, data: base64String } }
    ]
  }],
  config: {
    responseModalities: ["IMAGE"],
    imageConfig: { aspectRatio: "4:5" }
  }
})
```

### BytePlus REST Pattern
```typescript
import { generateImageWithByteplus } from "@/lib/byteplus-client"

const result = await generateImageWithByteplus({
  prompt: prompt,
  images: [{ data: base64String, mimeType: "image/png" }]
})

if (result.error) {
  // Handle error
}
```

---

## Error Handling

See **[references/error-handling.md](references/error-handling.md)** for comprehensive guide.

**HTTP Status Codes:**
- `400` - Invalid request (check image format, size, aspect ratio)
- `401` - Authentication failed (invalid API key)
- `429` - Rate limit exceeded (implement backoff)
- `500` - Service error (retry with exponential backoff)

**Example error handler:**
```typescript
if (!response.ok) {
  switch (response.status) {
    case 400:
      return { error: "Invalid image or prompt" }
    case 401:
      return { error: "BytePlus API authentication failed" }
    case 429:
      return { error: "Rate limit exceeded, please try again later" }
    case 500:
      return { error: "BytePlus service error, please retry" }
    default:
      return { error: "Failed to generate image" }
  }
}
```

---

## Success Criteria

Migration complete when:
- ✅ All API routes use BytePlus instead of Gemini
- ✅ Environment validation passes
- ✅ TypeScript compilation passes (`npx tsc --noEmit`)
- ✅ Linting passes (`npm run lint`)
- ✅ Build succeeds
- ✅ Generated images meet quality expectations
- ✅ All error scenarios handled gracefully
- ✅ Documentation updated
- ✅ Production deployment stable

---

## Additional Resources

- **BytePlus API Documentation:** https://docs.byteplus.com/en/docs/ModelArk/1666945
- **API Console:** https://console.byteplus.com/ark/region:ark+ap-southeast-1/apiKey
- **Model Pricing:** https://docs.byteplus.com/en/docs/ModelArk/1099320#image-generation
- **Prompt Guide:** https://docs.byteplus.com/en/docs/ModelArk/1829186

---

## Troubleshooting

For common issues and solutions, see **[references/troubleshooting.md](references/troubleshooting.md)**.

For API parameter details, see **[references/api-comparison.md](references/api-comparison.md)**.

For comprehensive testing checklist, see **[references/testing-checklist.md](references/testing-checklist.md)**.
