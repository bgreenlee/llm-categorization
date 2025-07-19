# Bucket Categorization Experiment

Proof-of-concept for categorizing/tagging links.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) (`brew install uv`)
2. `cp .env.example .env` and add your `ANTHROPIC_API_KEY`
3. `uv run bucket.py ...` (see below for usage)

## Usage

```
usage: bucket.py [-h] [--tags TAGS] [--cost] document|url

Analyze documents with AI-powered summarization and tagging

positional arguments:
  document|url  URL or file path of the document to analyze

options:
  -h, --help    show this help message and exit
  --tags TAGS   Comma-separated list of tags to use for analysis
  --cost        Log Anthropic API cost information at the end
```

## Examples

```
uv run bucket.py attention.pdf
{
  "summary": "This paper introduces the Transformer, a novel neural network architecture for sequence transduction tasks that relies entirely on attention mechanisms, eliminating the need for recurrent or convolutional layers. The model achieves state-of-the-art results on machine translation tasks, including 28.4 BLEU on English-to-German and 41.8 BLEU on English-to-French translation, while being significantly more parallelizable and faster to train than existing approaches. The Transformer uses multi-head self-attention and positional encoding to capture dependencies between sequence elements, and demonstrates strong performance on English constituency parsing as well.",
  "tags": ["Machine Translation", "Neural Networks", "Attention Mechanism", "Deep Learning", "Natural Language Processing"]
}
```

