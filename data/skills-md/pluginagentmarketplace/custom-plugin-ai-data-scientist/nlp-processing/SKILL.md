---
name: nlp-processing
description: Text processing, sentiment analysis, LLMs, and NLP frameworks. Use for text classification, named entity recognition, or language models.
sasmp_version: "1.3.0"
bonded_agent: 04-machine-learning-ai
bond_type: SECONDARY_BOND
---

# Natural Language Processing

Process, analyze, and understand text data with modern NLP techniques.

## Quick Start

### Text Preprocessing
```python
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    # Lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]

    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]

    return ' '.join(tokens)
```

### Sentiment Analysis
```python
from transformers import pipeline

# Pre-trained model
sentiment_analyzer = pipeline("sentiment-analysis")
result = sentiment_analyzer("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Custom model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(documents)

model = LogisticRegression()
model.fit(X, labels)
```

## TF-IDF Vectorization

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    max_features=5000,
    ngram_range=(1, 2),  # Unigrams and bigrams
    min_df=2,            # Minimum document frequency
    max_df=0.8           # Maximum document frequency
)

X = vectorizer.fit_transform(documents)
feature_names = vectorizer.get_feature_names_out()
```

## Named Entity Recognition

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple Inc. was founded by Steve Jobs in California.")

for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
# Apple Inc.: ORG
# Steve Jobs: PERSON
# California: GPE
```

## BERT for Text Classification

```python
from transformers import (
    BertTokenizer, BertForSequenceClassification,
    Trainer, TrainingArguments
)

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained(
    'bert-base-uncased',
    num_labels=2
)

# Tokenize
def tokenize_function(examples):
    return tokenizer(
        examples['text'],
        padding='max_length',
        truncation=True,
        max_length=128
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Train
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy='epoch'
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test']
)

trainer.train()
```

## Text Generation with GPT

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

input_text = "The future of AI is"
input_ids = tokenizer.encode(input_text, return_tensors='pt')

output = model.generate(
    input_ids,
    max_length=50,
    num_return_sequences=1,
    temperature=0.7,
    top_k=50,
    top_p=0.95
)

generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)
```

## Topic Modeling with LDA

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(max_features=1000, max_df=0.8, min_df=2)
X = vectorizer.fit_transform(documents)

lda = LatentDirichletAllocation(n_components=5, random_state=42)
lda.fit(X)

# Display topics
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    top_words = [feature_names[i] for i in topic.argsort()[-10:]]
    print(f"Topic {topic_idx}: {', '.join(top_words)}")
```

## Word Embeddings

```python
from gensim.models import Word2Vec

# Train Word2Vec
sentences = [word_tokenize(doc) for doc in documents]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)

# Get vector
vector = model.wv['king']

# Find similar words
similar = model.wv.most_similar('king', topn=5)
```

## Common Tasks

**Text Classification:**
- Sentiment analysis
- Spam detection
- Intent classification
- Topic categorization

**Sequence Labeling:**
- Named Entity Recognition (NER)
- Part-of-Speech (POS) tagging
- Keyword extraction

**Generation:**
- Text summarization
- Machine translation
- Chatbots
- Code generation

## Best Practices

1. Clean text (remove noise, normalize)
2. Handle class imbalance
3. Use pre-trained models when possible
4. Fine-tune on domain-specific data
5. Validate with diverse test data
6. Monitor for bias and fairness
