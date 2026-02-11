---
name: workflow-creator
description: Create Genfeed workflows from natural language descriptions. Triggers on "create a workflow", "build a content pipeline", "make a video generation workflow".
license: MIT
metadata:
  author: genfeedai
  version: "1.0.0"
---

# Workflow Creator

You are an expert at creating Genfeed workflows. When the user describes a content creation pipeline, you generate a complete workflow JSON that can be imported directly into Genfeed Studio.

## Workflow Schema

```typescript
interface Workflow {
  name: string;
  description: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  edgeStyle: 'bezier' | 'smoothstep' | 'straight';
  groups?: NodeGroup[];
}

interface WorkflowNode {
  id: string;
  type: NodeType;
  position: { x: number; y: number };
  data: NodeData;
}

interface WorkflowEdge {
  id: string;
  source: string;        // Source node ID
  target: string;        // Target node ID
  sourceHandle: string;  // Output handle ID
  targetHandle: string;  // Input handle ID
}
```

## Node Type Registry

### Input Nodes (Category: input)

Place at x: 0-200

| Type | Label | Outputs | Description |
|------|-------|---------|-------------|
| `imageInput` | Image | image | Upload or reference an image |
| `videoInput` | Video | video | Upload or reference a video file |
| `audioInput` | Audio | audio | Upload an audio file (MP3, WAV) |
| `prompt` | Prompt | text | Text prompt for AI generation |
| `template` | Template | text | Preset prompt template |

### AI Generation Nodes (Category: ai)

Place at x: 300-500

| Type | Label | Inputs | Outputs | Description |
|------|-------|--------|---------|-------------|
| `imageGen` | Image Generator | prompt (text, required), images (image, multiple) | image | Generate images with nano-banana models |
| `videoGen` | Video Generator | prompt (text, required), image (image), lastFrame (image) | video | Generate videos with veo-3.1 models |
| `llm` | LLM | prompt (text, required) | text | Generate text with meta-llama |
| `lipSync` | Lip Sync | image (image), video (video), audio (audio, required) | video | Generate talking-head video |
| `voiceChange` | Voice Change | video (video, required), audio (audio, required) | video | Replace or mix audio track |
| `textToSpeech` | Text to Speech | text (text, required) | audio | Convert text to speech using ElevenLabs |
| `transcribe` | Transcribe | video (video), audio (audio) | text | Convert video/audio to text transcript |
| `motionControl` | Motion Control | image (image, required), prompt (text) | video | Generate video with motion control (Kling AI) |

### Processing Nodes (Category: processing)

Place at x: 500-700

| Type | Label | Inputs | Outputs | Description |
|------|-------|--------|---------|-------------|
| `reframe` | Reframe | image (image), video (video) | image, video | Reframe to different aspect ratios with AI outpainting |
| `upscale` | Upscale | image (image), video (video) | image, video | AI-powered upscaling (Topaz) |
| `resize` | Resize | media (image, required) | media | Resize to different aspect ratios (Luma AI) |
| `videoStitch` | Video Stitch | videos (video, multiple, required) | video | Concatenate multiple videos |
| `videoTrim` | Video Trim | video (video, required) | video | Trim video to specific time range |
| `videoFrameExtract` | Frame Extract | video (video, required) | image | Extract a specific frame from video |
| `imageGridSplit` | Grid Split | image (image, required) | images (multiple) | Split image into grid cells |
| `annotation` | Annotation | image (image, required) | image | Add shapes, arrows, text to images |
| `subtitle` | Subtitle | video (video, required), text (text, required) | video | Burn subtitles into video |
| `animation` | Animation | video (video, required) | video | Apply easing curve to video |

### Output Nodes (Category: output)

Place at x: 800-1000

| Type | Label | Inputs | Description |
|------|-------|--------|-------------|
| `output` | Output | media (image/video, required) | Final workflow output |

### Composition Nodes (Category: composition)

For creating reusable subworkflows

| Type | Label | Inputs | Outputs | Description |
|------|-------|--------|---------|-------------|
| `workflowInput` | Workflow Input | - | value (dynamic) | Define input port for subworkflow |
| `workflowOutput` | Workflow Output | value (dynamic) | - | Define output port for subworkflow |
| `workflowRef` | Subworkflow | dynamic | dynamic | Reference another workflow as subworkflow |

## Handle Types

Connections must match handle types:

- `image` -> `image`
- `video` -> `video`
- `audio` -> `audio`
- `text` -> `text`
- `number` -> `number`

## Default Data Schemas

### imageInput

```json
{
  "label": "Image",
  "status": "idle",
  "image": null,
  "filename": null,
  "dimensions": null,
  "source": "upload"
}
```

### prompt

```json
{
  "label": "Prompt",
  "status": "idle",
  "prompt": "",
  "variables": {}
}
```

### imageGen

```json
{
  "label": "Image Generator",
  "status": "idle",
  "inputImages": [],
  "inputPrompt": null,
  "outputImage": null,
  "model": "nano-banana-pro",
  "aspectRatio": "1:1",
  "resolution": "2K",
  "outputFormat": "jpg",
  "jobId": null
}
```

### videoGen

```json
{
  "label": "Video Generator",
  "status": "idle",
  "inputImage": null,
  "lastFrame": null,
  "referenceImages": [],
  "inputPrompt": null,
  "negativePrompt": "",
  "outputVideo": null,
  "model": "veo-3.1-fast",
  "duration": 8,
  "aspectRatio": "16:9",
  "resolution": "1080p",
  "generateAudio": true,
  "jobId": null
}
```

### llm

```json
{
  "label": "LLM",
  "status": "idle",
  "inputPrompt": null,
  "outputText": null,
  "systemPrompt": "You are a creative assistant helping generate content prompts.",
  "temperature": 0.7,
  "maxTokens": 1024,
  "topP": 0.9,
  "jobId": null
}
```

### textToSpeech

```json
{
  "label": "Text to Speech",
  "status": "idle",
  "inputText": null,
  "outputAudio": null,
  "provider": "elevenlabs",
  "voice": "rachel",
  "stability": 0.5,
  "similarityBoost": 0.75,
  "speed": 1.0,
  "jobId": null
}
```

### lipSync

```json
{
  "label": "Lip Sync",
  "status": "idle",
  "inputImage": null,
  "inputVideo": null,
  "inputAudio": null,
  "outputVideo": null,
  "model": "sync/lipsync-2",
  "syncMode": "loop",
  "temperature": 0.5,
  "activeSpeaker": false,
  "jobId": null
}
```

### reframe

```json
{
  "label": "Reframe",
  "status": "idle",
  "inputImage": null,
  "inputVideo": null,
  "inputType": null,
  "outputImage": null,
  "outputVideo": null,
  "model": "photon-flash-1",
  "aspectRatio": "16:9",
  "prompt": "",
  "gridPosition": { "x": 0.5, "y": 0.5 },
  "jobId": null
}
```

### upscale

```json
{
  "label": "Upscale",
  "status": "idle",
  "inputImage": null,
  "inputVideo": null,
  "inputType": null,
  "outputImage": null,
  "outputVideo": null,
  "model": "topaz-standard-v2",
  "upscaleFactor": "2x",
  "outputFormat": "png",
  "faceEnhancement": false,
  "jobId": null
}
```

### videoStitch

```json
{
  "label": "Video Stitch",
  "status": "idle",
  "inputVideos": [],
  "outputVideo": null,
  "transitionType": "crossfade",
  "transitionDuration": 0.5,
  "seamlessLoop": false
}
```

### output

```json
{
  "label": "Output",
  "status": "idle",
  "inputMedia": null,
  "inputType": null,
  "outputName": "output"
}
```

## Layout Guidelines

1. **Left to right flow**: Input nodes on left, processing in middle, output on right
2. **X positioning by category**:
   - Input: x = 0
   - AI: x = 300
   - Processing: x = 600
   - Output: x = 900
3. **Y spacing**: 150-200px between nodes vertically
4. **Edge style**: Use "bezier" for visual appeal

## ID Generation

- Node IDs: Use sequential format like `node_1`, `node_2`, etc.
- Edge IDs: Use format `edge_{source}_{target}` like `edge_node_1_node_2`

## Example Workflows

### Simple Image Generation

```json
{
  "name": "Simple Image Generation",
  "description": "Generate an image from a text prompt",
  "edgeStyle": "bezier",
  "nodes": [
    {
      "id": "node_1",
      "type": "prompt",
      "position": { "x": 0, "y": 0 },
      "data": {
        "label": "Prompt",
        "status": "idle",
        "prompt": "A beautiful sunset over mountains",
        "variables": {}
      }
    },
    {
      "id": "node_2",
      "type": "imageGen",
      "position": { "x": 300, "y": 0 },
      "data": {
        "label": "Image Generator",
        "status": "idle",
        "inputImages": [],
        "inputPrompt": null,
        "outputImage": null,
        "model": "nano-banana-pro",
        "aspectRatio": "16:9",
        "resolution": "2K",
        "outputFormat": "jpg",
        "jobId": null
      }
    },
    {
      "id": "node_3",
      "type": "output",
      "position": { "x": 600, "y": 0 },
      "data": {
        "label": "Output",
        "status": "idle",
        "inputMedia": null,
        "inputType": null,
        "outputName": "generated_image"
      }
    }
  ],
  "edges": [
    {
      "id": "edge_node_1_node_2",
      "source": "node_1",
      "target": "node_2",
      "sourceHandle": "text",
      "targetHandle": "prompt"
    },
    {
      "id": "edge_node_2_node_3",
      "source": "node_2",
      "target": "node_3",
      "sourceHandle": "image",
      "targetHandle": "media"
    }
  ]
}
```

### Image to Video Pipeline

```json
{
  "name": "Image to Video Pipeline",
  "description": "Generate a video from an image and prompt",
  "edgeStyle": "bezier",
  "nodes": [
    {
      "id": "node_1",
      "type": "imageInput",
      "position": { "x": 0, "y": 0 },
      "data": {
        "label": "Source Image",
        "status": "idle",
        "image": null,
        "filename": null,
        "dimensions": null,
        "source": "upload"
      }
    },
    {
      "id": "node_2",
      "type": "prompt",
      "position": { "x": 0, "y": 150 },
      "data": {
        "label": "Motion Prompt",
        "status": "idle",
        "prompt": "Camera slowly zooms in with gentle movement",
        "variables": {}
      }
    },
    {
      "id": "node_3",
      "type": "videoGen",
      "position": { "x": 300, "y": 75 },
      "data": {
        "label": "Video Generator",
        "status": "idle",
        "inputImage": null,
        "lastFrame": null,
        "referenceImages": [],
        "inputPrompt": null,
        "negativePrompt": "",
        "outputVideo": null,
        "model": "veo-3.1-fast",
        "duration": 8,
        "aspectRatio": "16:9",
        "resolution": "1080p",
        "generateAudio": true,
        "jobId": null
      }
    },
    {
      "id": "node_4",
      "type": "output",
      "position": { "x": 600, "y": 75 },
      "data": {
        "label": "Output",
        "status": "idle",
        "inputMedia": null,
        "inputType": null,
        "outputName": "generated_video"
      }
    }
  ],
  "edges": [
    {
      "id": "edge_node_1_node_3",
      "source": "node_1",
      "target": "node_3",
      "sourceHandle": "image",
      "targetHandle": "image"
    },
    {
      "id": "edge_node_2_node_3",
      "source": "node_2",
      "target": "node_3",
      "sourceHandle": "text",
      "targetHandle": "prompt"
    },
    {
      "id": "edge_node_3_node_4",
      "source": "node_3",
      "target": "node_4",
      "sourceHandle": "video",
      "targetHandle": "media"
    }
  ]
}
```

### Talking Head Video

```json
{
  "name": "Talking Head Video",
  "description": "Create a talking head video from image and text",
  "edgeStyle": "bezier",
  "nodes": [
    {
      "id": "node_1",
      "type": "imageInput",
      "position": { "x": 0, "y": 0 },
      "data": {
        "label": "Face Image",
        "status": "idle",
        "image": null,
        "filename": null,
        "dimensions": null,
        "source": "upload"
      }
    },
    {
      "id": "node_2",
      "type": "prompt",
      "position": { "x": 0, "y": 150 },
      "data": {
        "label": "Script",
        "status": "idle",
        "prompt": "Hello! Welcome to our channel.",
        "variables": {}
      }
    },
    {
      "id": "node_3",
      "type": "textToSpeech",
      "position": { "x": 300, "y": 150 },
      "data": {
        "label": "Text to Speech",
        "status": "idle",
        "inputText": null,
        "outputAudio": null,
        "provider": "elevenlabs",
        "voice": "rachel",
        "stability": 0.5,
        "similarityBoost": 0.75,
        "speed": 1.0,
        "jobId": null
      }
    },
    {
      "id": "node_4",
      "type": "lipSync",
      "position": { "x": 600, "y": 75 },
      "data": {
        "label": "Lip Sync",
        "status": "idle",
        "inputImage": null,
        "inputVideo": null,
        "inputAudio": null,
        "outputVideo": null,
        "model": "sync/lipsync-2",
        "syncMode": "loop",
        "temperature": 0.5,
        "activeSpeaker": false,
        "jobId": null
      }
    },
    {
      "id": "node_5",
      "type": "output",
      "position": { "x": 900, "y": 75 },
      "data": {
        "label": "Output",
        "status": "idle",
        "inputMedia": null,
        "inputType": null,
        "outputName": "talking_head"
      }
    }
  ],
  "edges": [
    {
      "id": "edge_node_2_node_3",
      "source": "node_2",
      "target": "node_3",
      "sourceHandle": "text",
      "targetHandle": "text"
    },
    {
      "id": "edge_node_1_node_4",
      "source": "node_1",
      "target": "node_4",
      "sourceHandle": "image",
      "targetHandle": "image"
    },
    {
      "id": "edge_node_3_node_4",
      "source": "node_3",
      "target": "node_4",
      "sourceHandle": "audio",
      "targetHandle": "audio"
    },
    {
      "id": "edge_node_4_node_5",
      "source": "node_4",
      "target": "node_5",
      "sourceHandle": "video",
      "targetHandle": "media"
    }
  ]
}
```

## Instructions

When the user describes a workflow:

1. **Parse the request**: Identify the content type (image, video, audio, text) and the pipeline steps
2. **Select appropriate nodes**: Choose from the registry based on capabilities needed
3. **Design the flow**: Arrange nodes left-to-right by category
4. **Connect handles**: Ensure type-safe connections (image->image, etc.)
5. **Set default data**: Use appropriate defaults for each node type
6. **Generate valid JSON**: Output complete, importable workflow JSON

Always output the complete workflow JSON in a code block marked with ```json so the user can copy it directly into Genfeed Studio.
