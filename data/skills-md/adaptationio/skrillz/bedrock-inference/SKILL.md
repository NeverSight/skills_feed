---
name: bedrock-inference
description: Amazon Bedrock Runtime API for model inference including Claude, Nova, Titan, and third-party models. Covers invoke-model, converse API, streaming responses, token counting, async invocation, and guardrails. Use when invoking foundation models, building conversational AI, streaming model responses, optimizing token usage, or implementing runtime guardrails.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Amazon Bedrock Inference

## Overview

Amazon Bedrock Runtime provides APIs for invoking foundation models including Claude (Opus, Sonnet, Haiku), Nova (Amazon), Titan (Amazon), and third-party models (Cohere, AI21, Meta). Supports both synchronous and asynchronous inference with streaming capabilities.

**Purpose**: Production-grade model inference with unified API across all Bedrock models

**Pattern**: Task-based (independent operations for different inference modes)

**Key Capabilities**:
1. **Model Invocation** - Direct model calls with native or Converse API
2. **Streaming** - Real-time token streaming for low latency
3. **Async Invocation** - Long-running tasks up to 24 hours
4. **Token Counting** - Cost estimation before inference
5. **Guardrails** - Runtime content filtering and safety
6. **Inference Profiles** - Cross-region routing and cost optimization

**Quality Targets**:
- Latency: < 1s first token for streaming
- Throughput: Up to 4,000 tokens/sec
- Availability: 99.9% SLA with cross-region profiles

---

## When to Use

Use bedrock-inference when:

- Invoking Claude, Nova, Titan, or other Bedrock models
- Building conversational AI applications
- Implementing streaming responses for better UX
- Running long-running async inference tasks
- Applying runtime guardrails for content safety
- Optimizing costs with inference profiles
- Counting tokens before model invocation
- Implementing multi-turn conversations

**When NOT to Use**:
- Building complex agents (use bedrock-agentcore)
- Knowledge base RAG (use bedrock-knowledge-bases)
- Model customization (use bedrock-fine-tuning)

---

## Prerequisites

### Required
- AWS account with Bedrock access
- Model access enabled in AWS Console
- IAM permissions for Bedrock Runtime

### Recommended
- `boto3 >= 1.34.0` (for latest Converse API)
- Understanding of model-specific input formats
- CloudWatch for monitoring

### Installation

```bash
pip install boto3 botocore
```

### Enable Model Access

```bash
# Check available models
aws bedrock list-foundation-models --region us-east-1

# Request model access via Console:
# AWS Console → Bedrock → Model access → Manage model access
```

---

## Model IDs and Inference Profiles

### Claude Models (Anthropic)

| Model | Model ID | Inference Profile ID | Region | Max Tokens |
|-------|----------|---------------------|--------|------------|
| **Claude Opus 4.5** | `anthropic.claude-opus-4-5-20251101-v1:0` | `global.anthropic.claude-opus-4-5-20251101-v1:0` | Global | 200K |
| **Claude Sonnet 4.5** | `anthropic.claude-sonnet-4-5-20250929-v1:0` | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` | US | 200K |
| **Claude Haiku 4.5** | `anthropic.claude-haiku-4-5-20251001-v1:0` | `us.anthropic.claude-haiku-4-5-20251001-v1:0` | US | 200K |
| **Claude Sonnet 3.5 v2** | `anthropic.claude-3-5-sonnet-20241022-v2:0` | `us.anthropic.claude-3-5-sonnet-20241022-v2:0` | US | 200K |
| **Claude Haiku 3.5** | `anthropic.claude-3-5-haiku-20241022-v1:0` | `us.anthropic.claude-3-5-haiku-20241022-v1:0` | US | 200K |

### Amazon Nova Models

| Model | Model ID | Inference Profile ID | Region | Max Tokens |
|-------|----------|---------------------|--------|------------|
| **Nova Pro** | `amazon.nova-pro-v1:0` | `us.amazon.nova-pro-v1:0` | US | 300K |
| **Nova Lite** | `amazon.nova-lite-v1:0` | `us.amazon.nova-lite-v1:0` | US | 300K |
| **Nova Micro** | `amazon.nova-micro-v1:0` | `us.amazon.nova-micro-v1:0` | US | 128K |

### Amazon Titan Models

| Model | Model ID | Region | Max Tokens |
|-------|----------|--------|------------|
| **Titan Text Premier** | `amazon.titan-text-premier-v1:0` | All | 32K |
| **Titan Text Express** | `amazon.titan-text-express-v1` | All | 8K |

### Inference Profile Prefixes

- `us.` - US-only routing (lower latency for US traffic)
- `global.` - Global cross-region routing (highest availability)
- `apac.` - Asia-Pacific routing (lower latency for APAC traffic)

---

## Quick Reference

### Client Initialization

```python
import boto3
from typing import Optional

def get_bedrock_client(region_name: str = 'us-east-1',
                        profile_name: Optional[str] = None):
    """Initialize Bedrock Runtime client"""
    session = boto3.Session(
        region_name=region_name,
        profile_name=profile_name
    )
    return session.client('bedrock-runtime')

# Usage
bedrock = get_bedrock_client(region_name='us-west-2')
```

---

## Operations

### 1. Invoke Model (Native API)

Direct model invocation using model-specific request format.

**Basic Invocation**:
```python
import json

def invoke_claude(prompt: str, model_id: str = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'):
    """Invoke Claude with native API"""
    bedrock = get_bedrock_client()

    # Claude-specific request format
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "top_p": 0.9
    }

    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(request_body)
    )

    # Parse response
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

# Usage
result = invoke_claude("Explain quantum computing in simple terms")
print(result)
```

**With System Prompts**:
```python
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 2048,
    "system": "You are a helpful AI assistant specialized in technical documentation.",
    "messages": [
        {
            "role": "user",
            "content": "Write API documentation for a REST endpoint"
        }
    ]
}
```

**With Tool Use**:
```python
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4096,
    "messages": [
        {
            "role": "user",
            "content": "What's the weather in San Francisco?"
        }
    ],
    "tools": [
        {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        }
    ]
}
```

---

### 2. Converse API (Unified Interface)

Model-agnostic API that works across all Bedrock models with consistent interface.

**Basic Conversation**:
```python
def converse_with_model(
    messages: list,
    model_id: str = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
    system_prompts: Optional[list] = None,
    max_tokens: int = 2048
):
    """Converse API for unified model interaction"""
    bedrock = get_bedrock_client()

    inference_config = {
        'maxTokens': max_tokens,
        'temperature': 0.7,
        'topP': 0.9
    }

    request_params = {
        'modelId': model_id,
        'messages': messages,
        'inferenceConfig': inference_config
    }

    if system_prompts:
        request_params['system'] = system_prompts

    response = bedrock.converse(**request_params)

    return response

# Usage
messages = [
    {
        'role': 'user',
        'content': [
            {'text': 'What are the benefits of microservices architecture?'}
        ]
    }
]

system_prompts = [
    {'text': 'You are a software architecture expert.'}
]

response = converse_with_model(messages, system_prompts=system_prompts)
assistant_message = response['output']['message']
print(assistant_message['content'][0]['text'])
```

**Multi-turn Conversation**:
```python
def multi_turn_conversation():
    """Multi-turn conversation with context"""
    bedrock = get_bedrock_client()

    messages = []
    model_id = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'

    # Turn 1
    messages.append({
        'role': 'user',
        'content': [{'text': 'My name is Alice and I work in healthcare.'}]
    })

    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={'maxTokens': 1024}
    )

    # Add assistant response to history
    messages.append(response['output']['message'])

    # Turn 2 (model remembers context)
    messages.append({
        'role': 'user',
        'content': [{'text': 'What are some AI applications in my field?'}]
    })

    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={'maxTokens': 1024}
    )

    return response['output']['message']['content'][0]['text']
```

**With Tool Use (Converse API)**:
```python
def converse_with_tools():
    """Converse API with tool use"""
    bedrock = get_bedrock_client()

    tools = [
        {
            'toolSpec': {
                'name': 'get_stock_price',
                'description': 'Get current stock price for a symbol',
                'inputSchema': {
                    'json': {
                        'type': 'object',
                        'properties': {
                            'symbol': {
                                'type': 'string',
                                'description': 'Stock ticker symbol'
                            }
                        },
                        'required': ['symbol']
                    }
                }
            }
        }
    ]

    messages = [
        {
            'role': 'user',
            'content': [{'text': "What's the price of AAPL stock?"}]
        }
    ]

    response = bedrock.converse(
        modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        messages=messages,
        toolConfig={'tools': tools},
        inferenceConfig={'maxTokens': 2048}
    )

    # Check if model wants to use a tool
    if response['stopReason'] == 'tool_use':
        tool_use = response['output']['message']['content'][0]['toolUse']
        print(f"Tool requested: {tool_use['name']}")
        print(f"Tool input: {tool_use['input']}")

        # Execute tool and return result
        # (Add tool result to messages and call converse again)

    return response
```

---

### 3. Stream Response (Real-time Tokens)

Stream tokens as they're generated for lower perceived latency.

**Streaming with Native API**:
```python
def stream_claude_response(prompt: str):
    """Stream response tokens in real-time"""
    bedrock = get_bedrock_client()

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock.invoke_model_with_response_stream(
        modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        body=json.dumps(request_body)
    )

    # Process event stream
    stream = response['body']
    full_text = ""

    for event in stream:
        chunk = event.get('chunk')
        if chunk:
            chunk_obj = json.loads(chunk['bytes'].decode())

            if chunk_obj['type'] == 'content_block_delta':
                delta = chunk_obj['delta']
                if delta['type'] == 'text_delta':
                    text = delta['text']
                    print(text, end='', flush=True)
                    full_text += text

            elif chunk_obj['type'] == 'message_stop':
                print()  # New line at end

    return full_text

# Usage
response = stream_claude_response("Write a short story about a robot")
```

**Streaming with Converse API**:
```python
def stream_converse(messages: list, model_id: str):
    """Stream response using Converse API"""
    bedrock = get_bedrock_client()

    response = bedrock.converse_stream(
        modelId=model_id,
        messages=messages,
        inferenceConfig={'maxTokens': 2048}
    )

    stream = response['stream']
    full_text = ""

    for event in stream:
        if 'contentBlockDelta' in event:
            delta = event['contentBlockDelta']['delta']
            if 'text' in delta:
                text = delta['text']
                print(text, end='', flush=True)
                full_text += text

        elif 'messageStop' in event:
            print()
            break

    return full_text

# Usage
messages = [{'role': 'user', 'content': [{'text': 'Explain neural networks'}]}]
stream_converse(messages, 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')
```

**Streaming with Error Handling**:
```python
def safe_streaming(prompt: str):
    """Streaming with comprehensive error handling"""
    bedrock = get_bedrock_client()

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = bedrock.invoke_model_with_response_stream(
            modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
            body=json.dumps(request_body)
        )

        full_text = ""
        for event in response['body']:
            chunk = event.get('chunk')
            if chunk:
                chunk_obj = json.loads(chunk['bytes'].decode())

                if chunk_obj['type'] == 'content_block_delta':
                    text = chunk_obj['delta'].get('text', '')
                    print(text, end='', flush=True)
                    full_text += text

                elif chunk_obj['type'] == 'error':
                    print(f"\nStreaming error: {chunk_obj['error']}")
                    break

        return full_text

    except Exception as e:
        print(f"Stream failed: {e}")
        raise
```

---

### 4. Count Tokens

Estimate token usage and costs before invoking models.

**Converse Token Counting**:
```python
def count_tokens(messages: list, model_id: str):
    """Count tokens for cost estimation"""
    bedrock = get_bedrock_client()

    # Optional system prompts
    system_prompts = [
        {'text': 'You are a helpful assistant.'}
    ]

    # Optional tools
    tools = [
        {
            'toolSpec': {
                'name': 'example_tool',
                'description': 'Example tool',
                'inputSchema': {
                    'json': {
                        'type': 'object',
                        'properties': {}
                    }
                }
            }
        }
    ]

    response = bedrock.converse_count(
        modelId=model_id,
        messages=messages,
        system=system_prompts,
        toolConfig={'tools': tools}
    )

    # Get token counts
    usage = response['usage']
    print(f"Input tokens: {usage['inputTokens']}")
    print(f"System tokens: {usage.get('systemTokens', 0)}")
    print(f"Tool tokens: {usage.get('toolTokens', 0)}")
    print(f"Total input: {usage['totalTokens']}")

    return usage

# Usage
messages = [
    {'role': 'user', 'content': [{'text': 'This is a test message'}]}
]
tokens = count_tokens(messages, 'us.anthropic.claude-sonnet-4-5-20250929-v1:0')
```

**Cost Estimation**:
```python
def estimate_cost(messages: list, model_id: str, estimated_output_tokens: int = 1000):
    """Estimate inference cost before invocation"""
    bedrock = get_bedrock_client()

    # Count input tokens
    token_response = bedrock.converse_count(
        modelId=model_id,
        messages=messages
    )

    input_tokens = token_response['usage']['totalTokens']

    # Pricing (as of December 2024, prices vary by region)
    pricing = {
        'us.anthropic.claude-opus-4-5-20251101-v1:0': {
            'input': 15.00 / 1_000_000,   # $15 per 1M input tokens
            'output': 75.00 / 1_000_000   # $75 per 1M output tokens
        },
        'us.anthropic.claude-sonnet-4-5-20250929-v1:0': {
            'input': 3.00 / 1_000_000,
            'output': 15.00 / 1_000_000
        },
        'us.anthropic.claude-haiku-4-5-20251001-v1:0': {
            'input': 0.80 / 1_000_000,
            'output': 4.00 / 1_000_000
        }
    }

    if model_id in pricing:
        input_cost = input_tokens * pricing[model_id]['input']
        output_cost = estimated_output_tokens * pricing[model_id]['output']
        total_cost = input_cost + output_cost

        print(f"Input tokens: {input_tokens:,} (${input_cost:.6f})")
        print(f"Estimated output: {estimated_output_tokens:,} (${output_cost:.6f})")
        print(f"Estimated total: ${total_cost:.6f}")

        return {
            'input_tokens': input_tokens,
            'estimated_output_tokens': estimated_output_tokens,
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': total_cost
        }
    else:
        print("Pricing not available for this model")
        return None
```

---

### 5. Async Invoke (Long-Running Tasks)

For inference tasks that take longer than 60 seconds (up to 24 hours).

**Start Async Invocation**:
```python
def async_invoke_model(prompt: str, s3_output_uri: str):
    """Start async model invocation for long tasks"""
    bedrock = get_bedrock_client()

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 10000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock.invoke_model_async(
        modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        modelInput=json.dumps(request_body),
        outputDataConfig={
            's3OutputDataConfig': {
                's3Uri': s3_output_uri
            }
        }
    )

    invocation_arn = response['invocationArn']
    print(f"Async invocation started: {invocation_arn}")

    return invocation_arn

# Usage
s3_output = 's3://my-bucket/bedrock-outputs/result.json'
arn = async_invoke_model("Write a 10,000 word technical guide", s3_output)
```

**Check Async Status**:
```python
def check_async_status(invocation_arn: str):
    """Check status of async invocation"""
    bedrock = get_bedrock_client()

    response = bedrock.get_async_invoke(
        invocationArn=invocation_arn
    )

    status = response['status']
    print(f"Status: {status}")

    if status == 'Completed':
        output_uri = response['outputDataConfig']['s3OutputDataConfig']['s3Uri']
        print(f"Output available at: {output_uri}")

        # Download and parse result
        # (Use boto3 S3 client to retrieve)

    elif status == 'Failed':
        print(f"Failure reason: {response.get('failureMessage', 'Unknown')}")

    return response

# Usage
status = check_async_status(arn)
```

**List Async Invocations**:
```python
def list_async_invocations(status_filter: Optional[str] = None):
    """List all async invocations"""
    bedrock = get_bedrock_client()

    params = {}
    if status_filter:
        params['statusEquals'] = status_filter  # 'InProgress', 'Completed', 'Failed'

    response = bedrock.list_async_invokes(**params)

    for invocation in response.get('asyncInvokeSummaries', []):
        print(f"ARN: {invocation['invocationArn']}")
        print(f"Status: {invocation['status']}")
        print(f"Submit time: {invocation['submitTime']}")
        print("---")

    return response
```

---

### 6. Apply Guardrail (Runtime Safety)

Apply content filtering and safety policies at runtime.

**Invoke with Guardrail**:
```python
def invoke_with_guardrail(
    prompt: str,
    guardrail_id: str,
    guardrail_version: str = 'DRAFT'
):
    """Invoke model with runtime guardrail"""
    bedrock = get_bedrock_client()

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        body=json.dumps(request_body),
        guardrailIdentifier=guardrail_id,
        guardrailVersion=guardrail_version
    )

    # Check if content was blocked
    response_body = json.loads(response['body'].read())

    if 'amazon-bedrock-guardrailAction' in response['ResponseMetadata']['HTTPHeaders']:
        action = response['ResponseMetadata']['HTTPHeaders']['amazon-bedrock-guardrailAction']
        if action == 'GUARDRAIL_INTERVENED':
            print("Content blocked by guardrail")
            return None

    return response_body['content'][0]['text']

# Usage
result = invoke_with_guardrail(
    "Tell me about quantum computing",
    guardrail_id='abc123xyz',
    guardrail_version='1'
)
```

**Converse with Guardrail**:
```python
def converse_with_guardrail(messages: list, guardrail_config: dict):
    """Converse API with guardrail configuration"""
    bedrock = get_bedrock_client()

    response = bedrock.converse(
        modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        messages=messages,
        inferenceConfig={'maxTokens': 2048},
        guardrailConfig=guardrail_config
    )

    # Check trace for guardrail intervention
    if 'trace' in response:
        trace = response['trace']['guardrail']
        if trace.get('action') == 'GUARDRAIL_INTERVENED':
            print("Guardrail blocked content")
            for assessment in trace.get('assessments', []):
                print(f"Policy: {assessment['topicPolicy']}")

    return response

# Usage
guardrail_config = {
    'guardrailIdentifier': 'abc123xyz',
    'guardrailVersion': '1',
    'trace': 'enabled'
}

messages = [{'role': 'user', 'content': [{'text': 'Test message'}]}]
converse_with_guardrail(messages, guardrail_config)
```

---

## Error Handling Patterns

### Comprehensive Error Handling

```python
from botocore.exceptions import ClientError, BotoCoreError
import time

def robust_invoke(prompt: str, max_retries: int = 3):
    """Invoke model with retry logic and error handling"""
    bedrock = get_bedrock_client()

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}]
    }

    for attempt in range(max_retries):
        try:
            response = bedrock.invoke_model(
                modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
                body=json.dumps(request_body)
            )

            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']

        except ClientError as e:
            error_code = e.response['Error']['Code']

            if error_code == 'ThrottlingException':
                wait_time = (2 ** attempt) + 1  # Exponential backoff
                print(f"Throttled. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                continue

            elif error_code == 'ModelTimeoutException':
                print("Model timeout - request took too long")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                raise

            elif error_code == 'ModelErrorException':
                print("Model error - check input format")
                raise

            elif error_code == 'ValidationException':
                print("Invalid parameters")
                raise

            elif error_code == 'AccessDeniedException':
                print("Access denied - check IAM permissions and model access")
                raise

            elif error_code == 'ResourceNotFoundException':
                print("Model not found - check model ID")
                raise

            else:
                print(f"Unexpected error: {error_code}")
                raise

        except BotoCoreError as e:
            print(f"Connection error: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            raise

    raise Exception(f"Failed after {max_retries} attempts")
```

### Specific Error Scenarios

```python
def handle_model_errors():
    """Common error scenarios and solutions"""
    bedrock = get_bedrock_client()

    try:
        # Attempt invocation
        response = bedrock.invoke_model(
            modelId='us.anthropic.claude-sonnet-4-5-20250929-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": "test"}]
            })
        )

    except ClientError as e:
        error_code = e.response['Error']['Code']

        if error_code == 'ModelNotReadyException':
            # Model is still loading
            print("Model not ready, wait 30 seconds and retry")

        elif error_code == 'ServiceQuotaExceededException':
            # Hit service quota
            print("Exceeded quota - request increase or use different region")

        elif error_code == 'ModelStreamErrorException':
            # Error during streaming
            print("Stream interrupted - restart stream")
```

---

## Best Practices

### 1. Cost Optimization

```python
def cost_optimized_inference(prompt: str, require_high_accuracy: bool = False):
    """Choose model based on task complexity and cost"""

    # Simple tasks → Haiku (cheapest)
    # Moderate tasks → Sonnet (balanced)
    # Complex tasks → Opus (most capable)

    if not require_high_accuracy:
        model_id = 'us.anthropic.claude-haiku-4-5-20251001-v1:0'
        print("Using Haiku for cost efficiency")
    elif require_high_accuracy:
        model_id = 'global.anthropic.claude-opus-4-5-20251101-v1:0'
        print("Using Opus for maximum accuracy")
    else:
        model_id = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
        print("Using Sonnet for balanced performance")

    return invoke_claude(prompt, model_id)
```

### 2. Use Inference Profiles

```python
def use_inference_profiles():
    """Leverage inference profiles for cost savings"""

    # Cross-region profiles offer 30-50% cost savings
    # with automatic region failover

    profiles = {
        'global_opus': 'global.anthropic.claude-opus-4-5-20251101-v1:0',
        'us_sonnet': 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
        'us_haiku': 'us.anthropic.claude-haiku-4-5-20251001-v1:0'
    }

    # Use global profile for high availability
    # Use regional profile for lower latency

    return profiles
```

### 3. Implement Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_inference(prompt: str, model_id: str):
    """Cache responses for identical prompts"""
    return invoke_claude(prompt, model_id)

def cache_key(prompt: str) -> str:
    """Generate cache key for prompt"""
    return hashlib.sha256(prompt.encode()).hexdigest()
```

### 4. Monitor Token Usage

```python
def track_token_usage(messages: list, model_id: str):
    """Track and log token usage"""
    bedrock = get_bedrock_client()

    # Count before invocation
    token_count = bedrock.converse_count(
        modelId=model_id,
        messages=messages
    )

    input_tokens = token_count['usage']['totalTokens']

    # Invoke
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig={'maxTokens': 2048}
    )

    # Get actual output tokens
    output_tokens = response['usage']['outputTokens']
    total_tokens = response['usage']['totalInputTokens'] + output_tokens

    # Log to CloudWatch or database
    print(f"Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}")

    return response
```

### 5. Use Streaming for Better UX

```python
def stream_for_user_experience(prompt: str):
    """Always use streaming for interactive applications"""

    # Streaming reduces perceived latency
    # Users see tokens immediately instead of waiting

    return stream_claude_response(prompt)
```

### 6. Async for Long Tasks

```python
def use_async_for_batch(prompts: list, s3_bucket: str):
    """Use async invocation for batch processing"""

    invocation_arns = []

    for idx, prompt in enumerate(prompts):
        s3_uri = f's3://{s3_bucket}/outputs/result-{idx}.json'
        arn = async_invoke_model(prompt, s3_uri)
        invocation_arns.append(arn)

    return invocation_arns
```

---

## IAM Permissions

### Minimum Runtime Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
        "arn:aws:bedrock:*::foundation-model/amazon.nova-*",
        "arn:aws:bedrock:*::foundation-model/amazon.titan-*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:Converse",
        "bedrock:ConverseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

### With Async Invocation

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:InvokeModelAsync",
        "bedrock:GetAsyncInvoke",
        "bedrock:ListAsyncInvokes"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::my-bedrock-bucket/*"
    }
  ]
}
```

---

## Progressive Disclosure

### Quick Start (This File)
- Client initialization
- Model IDs and inference profiles
- Basic invocation (native and Converse API)
- Streaming responses
- Token counting
- Async invocation
- Guardrail application
- Error handling patterns
- Best practices

### Detailed References
- **[Advanced Invocation Patterns](references/advanced-invocation.md)**: Batch processing, parallel requests, custom retry logic, response parsing
- **[Multimodal Support](references/multimodal.md)**: Image inputs, document parsing, vision capabilities for Claude and Nova
- **[Tool Use and Function Calling](references/tool-use.md)**: Complete tool use patterns, multi-turn tool conversations, error handling
- **[Performance Optimization](references/performance.md)**: Latency optimization, throughput tuning, cost reduction strategies
- **[Monitoring and Observability](references/monitoring.md)**: CloudWatch integration, custom metrics, cost tracking, usage analytics

---

## Related Skills

- **bedrock-agentcore**: Build production AI agents with managed infrastructure
- **bedrock-guardrails**: Configure content filters and safety policies
- **bedrock-knowledge-bases**: RAG with vector stores and retrieval
- **bedrock-prompts**: Manage and version prompts
- **anthropic-expert**: Claude API patterns and best practices
- **claude-cost-optimization**: Cost tracking and optimization for Claude
- **boto3-eks**: For containerized Bedrock applications

---

## Sources

- [Amazon Bedrock Runtime API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_Operations_Amazon_Bedrock_Runtime.html)
- [Boto3 Bedrock Runtime](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
- [Converse API Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html)
- [Claude on Bedrock](https://docs.anthropic.com/en/api/claude-on-amazon-bedrock)
- [Inference Profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles.html)
