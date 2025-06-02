# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project that appears to be a document analysis and tagging system using the Anthropic Claude API. The core functionality involves:

- Template-based prompt generation using Jinja2 templates
- Document analysis with AI-powered summarization and tagging
- JSON-formatted output for structured document categorization

## Key Architecture

- **bucket.py**: Main application logic containing template loading, prompt generation, and (commented) Anthropic API integration
- **prompts/**: Jinja2 template directory containing prompt templates for document analysis
  - `tag-list.txt`: Template for available tags selection
  - `summary-tagging.txt`: Main document analysis prompt template
- **main.py**: Simple entry point (currently just prints hello message)

## Development Commands

Run the main application:
```bash
python bucket.py
```

Run the entry point:
```bash
python main.py
```

Install dependencies (using uv):
```bash
uv sync
```

## Environment Setup

The application expects a `.env` file with:
- `MODEL`: Anthropic model to use (defaults to "claude-opus-4-20250514")
- Anthropic API key should be set in environment

## Template System

The project uses Jinja2 templates in the `prompts/` directory. When modifying prompts:
- Templates support variable substitution (e.g., `{{tag_list}}`, `{{document_content}}`)
- The system expects JSON output format from the AI model
- Tag system supports both predefined tags and new tag suggestions