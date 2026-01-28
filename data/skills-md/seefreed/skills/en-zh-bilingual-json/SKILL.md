---
name: en-zh-bilingual-json
description: Convert English .txt articles into a JSON array of sentence-level English/Chinese (zh) pairs. Translate English into Chinese and generating bilingual {en, zh} entries via the model (no external translation API), then saving to a JSON file.
---

# En Zh Bilingual Json

## Overview
Create bilingual JSON from English text, fist translating the text into Chinese using the model, and writing the final JSON array.

## Workflow

### 1) Translate with the model and fill zh
Translate English text to Chinese (zh) using the model and split sentence-level English/Chinese (zh) pairs, finally write back to the same JSON array. Preserve punctuation and sentence intent; keep proper nouns (e.g., product names) as appropriate  and remove relevant music transript.


Output format (top-level array):

```json
[
  {"en": "Sentence one.", "zh": " 句子一。"},
  {"en": "Sentence two?", "zh": "句子二？"}
]
```

### 2) Review and fix sentence boundaries
Make sure a splited sentence have the complete meaning and if one sentence has less than 5 words, you need to combine it with other sentences of the context so that every en item can't be too short and simple. Given showing a random Chinese sentence, a user will translate it back into English. The goal is to train a user translation ability.


### 4) Save final JSON
Ensure the JSON remains a valid array of `{en, zh}` objects. Keep UTF-8 output (the script already writes UTF-8). use the same filename with the text file aside from its format.
