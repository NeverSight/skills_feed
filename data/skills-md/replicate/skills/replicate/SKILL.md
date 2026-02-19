---
name: replicate
description: Discover, compare, and run AI models using Replicate's API
---

## Docs

- Reference docs: https://replicate.com/docs/llms.txt
- HTTP API schema: https://api.replicate.com/openapi.json
- MCP server: https://mcp.replicate.com
- Set an `Accept: text/markdown` header when requesting docs pages to get a Markdown response.

## Workflow

Here's a common workflow for using Replicate's API to run a model:

1. **Choose the right model** - Search with the API or ask the user
2. **Get model metadata** - Fetch model input and output schema via API
3. **Create prediction** - POST to /v1/predictions
4. **Poll for results** - GET prediction until status is "succeeded"
5. **Return output** - Usually URLs to generated content

## Choosing models

- Use the search and collections APIs to find and compare the best models. Do not list all the models via API, as it's basically a firehose.
- Collections are curated by Replicate staff, so they're vetted.
- Official models are in the "official" collection.
- Use official models because they:
  - are always running
  - have stable API interfaces
  - have predictable output pricing
  - are maintained by Replicate staff
- If you must use a community model, be aware that it can take a long time to boot.
- You can create always-on deployments of community models, but you pay for model uptime.

## Running models

Models take time to run. There are three ways to run a model via API and get its output:

1. Create a prediction, store its id from the response, and poll until completion.
2. Set a `Prefer: wait` header when creating a prediction for a blocking synchronous response. Only recommended for very fast models.
3. Set an HTTPS webhook URL when creating a prediction, and Replicate will POST to that URL when the prediction completes.

Follow these guideliness when running models:

- Use the "POST /v1/predictions" endpoint, as it supports both official and community models.
- Every model has its own OpenAPI schema. Always fetch and check model schemas to make sure you're setting valid inputs.
- Use HTTPS URLs for file inputs whenever possible. You can also send base64-encoded files, but they should be avoided.
- Fire off multiple predictions concurrently. Don't wait for one to finish before starting the next.
- Output file URLs expire after 1 hour, so back them up if you need to keep them, using a service like Cloudflare R2.
- Webhooks are a good mechanism for receiving and storing prediction output.


