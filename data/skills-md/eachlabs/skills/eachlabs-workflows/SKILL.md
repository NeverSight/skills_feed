---
name: eachlabs-workflows
description: Build and orchestrate multi-step AI workflows combining multiple EachLabs models. Create custom pipelines, trigger executions, and manage workflow versions. Use when the user needs to chain multiple AI models or automate multi-step content creation.
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs Workflows

Build, manage, and execute multi-step AI workflows that chain multiple models together via the EachLabs Workflows API.

## Authentication

```
Header: X-API-Key: <your-api-key>
```

Set the `EACHLABS_API_KEY` environment variable. Get your key at [eachlabs.ai](https://eachlabs.ai).

## Base URL

```
https://workflows.eachlabs.run/api/v1
```

## Building a Workflow

To build a workflow, you must: (1) create the workflow, then (2) create a version with the steps.

### Step 1: Create the Workflow

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/workflows \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "name": "Product Photo to Video",
    "description": "Generate a product video from a product photo"
  }'
```

This returns a `workflowID`. Use it in the next step.

### Step 2: Create a Version with Steps

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "description": "Initial version",
    "steps": [
      {
        "name": "enhance_photo",
        "model": "gpt-image-v1-5-edit",
        "version": "0.0.1",
        "input": {
          "prompt": "Place this product on a clean white background with studio lighting",
          "image_urls": ["{{inputs.image_url}}"],
          "quality": "high"
        }
      },
      {
        "name": "create_video",
        "model": "pixverse-v5-6-image-to-video",
        "version": "0.0.1",
        "input": {
          "image_url": "{{steps.enhance_photo.output}}",
          "prompt": "Slow cinematic rotation around the product",
          "duration": "5",
          "resolution": "1080p"
        }
      }
    ]
  }'
```

**Important:** Before adding a model to a workflow step, check its schema with `GET https://api.eachlabs.ai/v1/model?slug=<slug>` to validate the correct input parameters.

### Step 3: Trigger the Workflow

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/{workflowID}/trigger \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "inputs": {
      "image_url": "https://example.com/product.jpg"
    }
  }'
```

### Step 4: Poll for Result

```bash
curl https://workflows.eachlabs.run/api/v1/executions/{executionID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

Poll until `status` is `"completed"` or `"failed"`. Extract output from `step_outputs`.

## Workflow Management

### List Workflows

```bash
curl https://workflows.eachlabs.run/api/v1/workflows \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

### Get Workflow Details

```bash
curl https://workflows.eachlabs.run/api/v1/workflows/{workflowID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

### Bulk Trigger

Trigger the same workflow with multiple inputs:

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/{workflowID}/trigger/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "executions": [
      { "inputs": { "image_url": "https://example.com/product1.jpg" } },
      { "inputs": { "image_url": "https://example.com/product2.jpg" } },
      { "inputs": { "image_url": "https://example.com/product3.jpg" } }
    ]
  }'
```

### Check Execution Status

```bash
curl https://workflows.eachlabs.run/api/v1/executions/{executionID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

Response includes `status` (`pending`, `running`, `completed`, `failed`) and `step_outputs` with results from each step.

### Webhooks

Configure a webhook to receive results asynchronously:

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/{workflowID}/trigger \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "inputs": { "image_url": "https://example.com/photo.jpg" },
    "webhook_url": "https://your-server.com/webhook"
  }'
```

## Version Management

Workflow versions allow you to iterate on workflows while keeping previous versions intact. Steps are defined in versions, not in the workflow itself.

### Create a Version

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "description": "Added upscaling step",
    "steps": [
      {
        "name": "generate_image",
        "model": "gpt-image-v1-5-text-to-image",
        "version": "0.0.1",
        "input": {
          "prompt": "{{inputs.prompt}}",
          "quality": "high"
        }
      },
      {
        "name": "upscale",
        "model": "topaz-upscale-image",
        "version": "0.0.1",
        "input": {
          "image_url": "{{steps.generate_image.output}}"
        }
      }
    ]
  }'
```

### Get a Version

```bash
curl https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions/{versionID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

### Update a Version

```bash
curl -X PUT https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions/{versionID} \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "description": "Updated prompt template",
    "steps": [
      {
        "name": "generate_image",
        "model": "gpt-image-v1-5-text-to-image",
        "version": "0.0.1",
        "input": {
          "prompt": "Professional photo: {{inputs.prompt}}",
          "quality": "high"
        }
      }
    ]
  }'
```

### List Versions

```bash
curl https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

## Workflow Features

- **Two-phase creation**: Create workflow first, then add steps via versions
- **Step chaining**: Reference previous step outputs with `{{steps.step_name.output}}`
- **Input variables**: Use `{{inputs.variable_name}}` to pass dynamic inputs
- **Version management**: Create, update, and retrieve workflow versions
- **Bulk execution**: Process multiple inputs in a single API call
- **Webhook support**: Get notified when executions complete
- **Public/unlisted sharing**: Share workflows with others

## Example Workflow References

See [references/WORKFLOW-EXAMPLES.md](references/WORKFLOW-EXAMPLES.md) for common workflow patterns.
