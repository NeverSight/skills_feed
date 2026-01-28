---
name: scorable-integration
description: Integrate Scorable LLM-as-a-Judge evaluators into applications with LLM interactions. Use when users want to add evaluation, guardrails, or quality monitoring to their LLM-powered applications. Also use when users mention Scorable, judges, LLM evaluation, or safeguarding applications.
---

# Scorable Integration

Guides integration of Scorable's LLM-as-a-Judge evaluation system into codebases with LLM interactions. Scorable creates custom evaluators (judges) that assess LLM outputs for quality, safety, and policy adherence.

## Overview

Your role is to:
1. Analyze the codebase to identify LLM interactions
2. Create judges via Scorable API to evaluate those interactions
3. Integrate judge execution into the code at appropriate points
4. Provide usage documentation for the evaluation setup

## Workflow

### Step 1: Analyze the Application

Examine the codebase to understand:
- What LLM interactions exist (prompts, completions, agent calls)
- What the application does at each interaction point
- Which interactions are most critical to evaluate

If multiple LLM interactions exist, help the user prioritize. Recommend starting with the most critical one first.

### Step 2: Get Scorable API Key

Ask the user if they want to:
- **Create a temporary API key** (for quick testing) - Warn that the judge will be public and visible to everyone
- **Use an existing API key** (for production)

#### Creating a Temporary API Key

```bash
curl --request POST \
  --url https://api.scorable.ai/create-demo-user/ \
  --header 'accept: application/json' \
  --header 'content-type: application/json'
```

Response includes `api_key` field. Warn the user appropriately that:
- The judge will be public and visible to everyone
- The key only works for a limited time
- For private judges, they should create a permanent key at https://scorable.ai/register
- Remember also the \`api_token\` field. It is used in the URL parameters for the judge URL, not in any other context.

### Step 3: Generate a Judge

Call `/v1/judges/generate/` with a detailed `intent` string describing what to evaluate.

#### Intent String Guidelines

- Describe the application context and what you're evaluating
- Mention the specific execution point (stage name)
- Include critical quality dimensions you care about
- Add examples, documentation links, or policies if relevant
- Be specific and detailed (multiple sentences/paragraphs are good)
- Code level details like frameworks, libraries, etc. do not need to be mentioned

#### Example Request

```bash
curl --request POST \
  --url https://api.scorable.ai/v1/judges/generate/ \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header 'Authorization: Api-Key <SCORABLE_API_KEY>' \
  --data '{
    "visibility": "unlisted", # or public if using a temporary key
    "intent": "An email automation system that creates summary emails using an LLM based on database query results and user input. Evaluate the LLM output for: accuracy in summarizing data, appropriate tone for the audience, inclusion of all key information from queries, proper formatting, and absence of hallucinations. The system is used for customer-facing communications.",
    "generating_model_params": {
      "temperature": 0.2,
      "reasoning_effort": "medium"
    }
  }'
```

**Note:** This can take up to 2 minutes to complete.

#### Handling API Responses

**1. `missing_context_from_system_goal` - Additional context needed:**

```json
{
  "missing_context_from_system_goal": [
    {
      "form_field_name": "target_audience",
      "form_field_description": "The intended audience for the content"
    }
  ]
}
```

Ask the user for these details (if not evident from the codebase), then call `/v1/judges/generate/` again with:

```json
{
  "judge_id": "existing-judge-id",
  "stage": "Stage name",
  "extra_contexts": {
    "target_audience": "Enterprise customers"
  }
}
```

**2. `multiple_stages` - Judge detected multiple evaluation points:**

```json
{
  "error_code": "multiple_stages",
  "stages": ["Stage 1", "Stage 2", "Stage 3"]
}
```

Ask the user which stage to focus on, or if they have a custom stage name. Each judge evaluates one stage. You can create additional judges later for other stages.

**3. Success - Judge created:**

```json
{
  "judge_id": "abc123...",
  "evaluator_details": [...]
}
```

Proceed to integration.

### Step 4: Integrate Judge Execution

Add code to evaluate LLM outputs at the appropriate execution point(s).

Check if the codebase is using a framework with integration instructions in Scorable docs (use curl to fetch https://docs.scorable.ai/llms.txt if needed).

#### Language-Specific Integration

Choose the appropriate integration guide based on the codebase language:

- **Python**: See [references/python.md](references/python.md) for installation, sync/async usage, multi-turn conversations, and common patterns
- **TypeScript/JavaScript**: See [references/typescript.md](references/typescript.md) for npm installation and usage examples
- **Other languages**: See [references/other-languages.md](references/other-languages.md) for REST API integration via cURL template

#### Integration Points

- Insert evaluation code where LLM outputs are generated (e.g., after OpenAI response calls)
- `response` parameter: The text you want to evaluate
- `request` parameter: The input that prompted the response
- `messages` parameter: The multi-turn conversation flow, do not use request and response parameters in this case.
- Use actual variables from your code, not static strings

#### Multi-Turn Conversations

If a multi-turn conversation is detected, use the Messages/multi-turn format to evaluate the entire conversation flow. Confirm from user if multi-turn evaluation would suit their needs. See language-specific guides for details.

### Step 5: Provide Next Steps

After integration:

1. **Ask about additional judges**: If multiple stages were identified, ask if the user wants to create judges for other stages

2. **Discuss evaluation strategy**:
   - Should every LLM call be evaluated or sampled (e.g., 10%)?
   - Should scores be stored in a database for analysis?
   - Should specific actions trigger based on scores (e.g., alerts for low scores)?
   - Batch evaluation vs real-time evaluation?

3. **Provide judge details**:
   - Judge URL: `https://scorable.ai/judge/{judge_id}`
   - If you used a temporary key, you must include its counterpart api_token base64 encoded in the url as a query parameter: `https://scorable.ai/judge/{judge_id}?token={base64 encoded temporary api_token}`
   - How to view results in the Scorable dashboard: https://scorable.ai/dashboard
   - If temporary key was used, note that it only works for a limited time and they should create an account with a permanent key

4. **Link to docs**: https://docs.scorable.ai

## Implementation Notes

- **Store API keys securely**: Use environment variables, not hardcoded strings
- **Handle errors gracefully**: Evaluation failures shouldn't break your application
- **Start simple**: Evaluate one stage first, then expand
- **Sampling for production**: 5-10% sampling reduces costs while maintaining visibility
- **Common patterns**: See language-specific reference files for integration patterns (development, production sampling, batch evaluation)
