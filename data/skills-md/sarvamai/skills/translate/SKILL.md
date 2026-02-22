---
name: translate
description: Translate text between English and Indian languages using Sarvam AI's Mayura model. Use when the user needs to translate content, localize applications, or convert text between Hindi, Tamil, Bengali, Telugu, and 7 other Indian languages. Supports bidirectional translation, script control, and code-mixed text.
license: Apache-2.0
metadata:
  author: sarvam-ai
  version: "1.0"
  model: mayura:v1
---

# Translation with Mayura

Mayura is Sarvam AI's translation model optimized for Indian languages with support for script variations, numeral formats, and code-mixed text.

## Installation

```bash
pip install sarvamai
```

## Quick Start

```python
from sarvamai import SarvamAI

client = SarvamAI()

response = client.translate.translate(
    input="Hello, how are you?",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    model="mayura:v1"
)

print(response.translated_text)  # "नमस्ते, आप कैसे हैं?"
```

## Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| `hi-IN` | Hindi | `ta-IN` | Tamil |
| `bn-IN` | Bengali | `te-IN` | Telugu |
| `kn-IN` | Kannada | `ml-IN` | Malayalam |
| `mr-IN` | Marathi | `gu-IN` | Gujarati |
| `pa-IN` | Punjabi | `or-IN` | Odia |
| `en-IN` | English | `auto` | Auto-detect |

## Translation Directions

- **English → Indian Language:** Translate English to any supported Indian language
- **Indian Language → English:** Translate any Indian language to English
- **Indian → Indian:** Translate between Indian languages (via English pivot)

## Translation Modes

### Formal Translation

```python
response = client.translate.translate(
    input="Please submit the report by Friday",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    model="mayura:v1",
    mode="formal"
)
```

### Casual Translation

```python
response = client.translate.translate(
    input="Hey, what's up?",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    model="mayura:v1",
    mode="casual"
)
```

## Script Control

Choose the output script for languages with multiple scripts:

```python
# Hindi in Devanagari (default)
response = client.translate.translate(
    input="Hello",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    output_script="devanagari"
)
# Output: "नमस्ते"

# Hindi in Latin (transliteration)
response = client.translate.translate(
    input="Hello",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    output_script="latin"
)
# Output: "Namaste"
```

## Numeral Format

Control numeral representation:

```python
# International numerals (default)
response = client.translate.translate(
    input="The price is 500 rupees",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    numeral_format="international"
)
# Output: "कीमत 500 रुपये है"

# Native numerals
response = client.translate.translate(
    input="The price is 500 rupees",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    numeral_format="native"
)
# Output: "कीमत ५०० रुपये है"
```

## Code-Mixed Input

Mayura handles code-mixed text (e.g., Hinglish):

```python
response = client.translate.translate(
    input="Yaar, let's go for a movie tonight",
    source_language_code="auto",  # Auto-detect
    target_language_code="hi-IN",
    model="mayura:v1"
)
# Output: "यार, चलो आज रात फिल्म देखने चलते हैं"
```

## Batch Translation

Translate multiple texts:

```python
texts = [
    "Hello",
    "How are you?",
    "Thank you"
]

responses = []
for text in texts:
    response = client.translate.translate(
        input=text,
        source_language_code="en-IN",
        target_language_code="hi-IN",
        model="mayura:v1"
    )
    responses.append(response.translated_text)

print(responses)
# [
    "नमस्ते",
    "आप कैसे हैं?",
    "धन्यवाद"
]
```

## JavaScript

```javascript
import { SarvamAI
} from "sarvamai";

const client = new SarvamAI();

const response = await client.translate.translate({
  input: "Hello, how are you?",
  sourceLanguageCode: "en-IN",
  targetLanguageCode: "hi-IN",
  model: "mayura:v1"
});

console.log(response.translatedText);
```

## cURL

```bash
curl -X POST "https://api.sarvam.ai/translate" \
  -H "api-subscription-key: $SARVAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Hello, how are you?",
    "source_language_code": "en-IN",
    "target_language_code": "hi-IN",
    "model": "mayura:v1"
}'
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `input` | string | Yes | Text to translate |
| `source_language_code` | string | Yes | Source language or `auto` |
| `target_language_code` | string | Yes | Target language code |
| `model` | string | Yes | `mayura:v1` |
| `mode` | string | No | `formal` or `casual` |
| `output_script` | string | No | `devanagari`, `latin`, etc. |
| `numeral_format` | string | No | `international` or `native` |

## Response

```json
{
    "request_id": "abc123",
    "translated_text": "नमस्ते, आप कैसे हैं?",
    "source_language_code": "en-IN",
    "target_language_code": "hi-IN"
}
```

See [references/languages.md
](references/languages.md) for language-specific notes.
