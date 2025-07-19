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

### Remote PDF

```
uv run bucket.py https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf
{
  "summary": "This paper introduces the Transformer, a novel neural network architecture for sequence transduction that relies entirely on attention mechanisms, eliminating the need for recurrent or convolutional layers. The model achieves state-of-the-art results on machine translation tasks, including 28.4 BLEU on WMT 2014 English-to-German translation, while being significantly more parallelizable and requiring less training time than previous approaches. The key innovation is the use of multi-head self-attention and scaled dot-product attention, which allows the model to capture long-range dependencies more efficiently than traditional RNN-based encoder-decoder architectures.",
  "tags": ["Machine Translation", "Neural Networks", "Attention Mechanisms", "Deep Learning", "Natural Language Processing"]
}
```

### Remote PDF, with Predefined Tags

```
uv run bucket.py --tags ai,cooking,papers,python,rust,politics https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa
-Paper.pdf
{
  "summary": "This paper introduces ....",
  "tags": ["ai", "papers"],
  "suggested_tags": ["machine translation", "neural networks", "transformers"]
}
```

### HTML Page, with Cost Estimation

```
 uv run bucket.py --cost https://footle.org/2025/03/21/screensaver-spelunking/
{
  "summary": "This document describes a technical project to create a Mac menu bar app that displays descriptions for macOS Sonoma's aerial screensavers. The author reverse-engineered how macOS stores and manages these screensavers by exploring SQLite databases, JSON configuration files, and system processes, ultimately creating a solution that identifies the currently active screensaver and displays its description using localized string bundles.",
  "tags": ["MacOS Development", "Reverse Engineering", "System Integration", "Menu Bar App"]
}

==================================================
ANTHROPIC API COST INFORMATION
==================================================
Model: claude-sonnet-4-0
Input tokens: 2,661
Output tokens: 119
Total tokens: 2,780
Input cost: $0.007983
Output cost: $0.001785
Total cost: $0.009768
==================================================
```

