---
name: huggingface-tokenizers
description: Use when "tokenizers", "HuggingFace tokenizer", "BPE", "WordPiece", or asking about "train tokenizer", "custom vocabulary", "tokenization", "subword", "fast tokenizer", "encode text"
version: 1.0.0
---

<!-- Adapted from: claude-scientific-skills/scientific-skills/huggingface-tokenizers -->

# HuggingFace Tokenizers

Fast, production-ready tokenization - Rust-powered, Python API.

## When to Use

- High-performance tokenization (<20s per GB)
- Train custom tokenizers from scratch
- Track token-to-text alignment
- Production NLP pipelines
- Need BPE, WordPiece, or Unigram tokenization

## Quick Start

```python
from tokenizers import Tokenizer

# Load pretrained
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")

# Encode
output = tokenizer.encode("Hello, how are you?")
print(output.tokens)  # ['hello', ',', 'how', 'are', 'you', '?']
print(output.ids)     # [7592, 1010, 2129, 2024, 2017, 1029]

# Decode
text = tokenizer.decode(output.ids)
```

## Train Custom Tokenizer

### BPE (GPT-2 style)

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import ByteLevel

# Initialize
tokenizer = Tokenizer(BPE(unk_token="<|endoftext|>"))
tokenizer.pre_tokenizer = ByteLevel()

# Configure trainer
trainer = BpeTrainer(
    vocab_size=50000,
    special_tokens=["<|endoftext|>", "<|pad|>"],
    min_frequency=2
)

# Train
tokenizer.train(files=["data.txt"], trainer=trainer)

# Save
tokenizer.save("my-tokenizer.json")
```

### WordPiece (BERT style)

```python
from tokenizers import Tokenizer
from tokenizers.models import WordPiece
from tokenizers.trainers import WordPieceTrainer
from tokenizers.pre_tokenizers import Whitespace

tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

trainer = WordPieceTrainer(
    vocab_size=30000,
    special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
)

tokenizer.train(files=["data.txt"], trainer=trainer)
```

## Encoding Options

```python
# Single text
output = tokenizer.encode("Hello world")

# Batch encoding
outputs = tokenizer.encode_batch(["Hello", "World"])

# With padding
tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")
outputs = tokenizer.encode_batch(texts)

# With truncation
tokenizer.enable_truncation(max_length=512)
output = tokenizer.encode(long_text)
```

## Access Encoding Data

```python
output = tokenizer.encode("Hello world")

output.ids           # Token IDs
output.tokens        # Token strings
output.attention_mask  # Attention mask
output.offsets       # Character offsets (alignment)
output.word_ids      # Word indices
```

## Pre-tokenizers

```python
from tokenizers.pre_tokenizers import (
    Whitespace,      # Split on whitespace
    ByteLevel,       # Byte-level (GPT-2)
    BertPreTokenizer,  # BERT style
    Punctuation,     # Split on punctuation
    Sequence,        # Chain multiple
)

# Chain pre-tokenizers
from tokenizers.pre_tokenizers import Sequence, Whitespace, Punctuation
tokenizer.pre_tokenizer = Sequence([Whitespace(), Punctuation()])
```

## Post-processing

```python
from tokenizers.processors import TemplateProcessing

# BERT-style: [CLS] ... [SEP]
tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[
        ("[CLS]", tokenizer.token_to_id("[CLS]")),
        ("[SEP]", tokenizer.token_to_id("[SEP]")),
    ],
)
```

## Normalization

```python
from tokenizers.normalizers import (
    NFD, NFKC, Lowercase, StripAccents, Sequence
)

# BERT normalization
tokenizer.normalizer = Sequence([NFD(), Lowercase(), StripAccents()])
```

## With Transformers

```python
from transformers import PreTrainedTokenizerFast

# Wrap for transformers compatibility
fast_tokenizer = PreTrainedTokenizerFast(tokenizer_object=tokenizer)

# Now works with transformers
encoded = fast_tokenizer("Hello world", return_tensors="pt")
```

## Save and Load

```python
# Save
tokenizer.save("tokenizer.json")

# Load
tokenizer = Tokenizer.from_file("tokenizer.json")

# From HuggingFace Hub
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
```

## Performance Tips

1. **Use batch encoding** for multiple texts
2. **Enable padding/truncation** once, not per-encode
3. **Pre-tokenizer choice** affects speed significantly
4. **Train on representative data** for better vocabulary

## vs Alternatives

| Tool | Best For |
|------|----------|
| **tokenizers** | Speed, custom training, production |
| SentencePiece | T5/ALBERT, language-independent |
| tiktoken | OpenAI models (GPT) |

## Resources

- Docs: <https://huggingface.co/docs/tokenizers/>
- GitHub: <https://github.com/huggingface/tokenizers>
