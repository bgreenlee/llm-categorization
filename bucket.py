import os
import logging
import argparse
import sys
from urllib.parse import urlparse
from pathlib import Path

import anthropic
import requests
import trafilatura
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pypdf import PdfReader

# configure logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def extract_text_from_url(url):
    """Extract human-readable text content from a URL."""
    try:
        # Download the page
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            logger.error(f"Failed to download content from URL: {url}")
            return None

        # Extract text content
        text = trafilatura.extract(downloaded)
        if text is None:
            logger.error(f"Failed to extract text from URL: {url}")
            return None

        return text
    except Exception as e:
        logger.error(f"Error extracting text from URL {url}: {e}")
        return None


def extract_text_from_pdf(file_path):
    """Extract text content from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        return None


def read_file_content(file_path):
    """Read content from a file, handling PDFs specially."""
    path = Path(file_path)

    if not path.exists():
        logger.error(f"File not found: {file_path}")
        return None

    if path.suffix.lower() == '.pdf':
        return extract_text_from_pdf(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


def get_document_content(input_path):
    """Get document content from either a URL or file path."""
    if input_path.startswith(('http://', 'https://')):
        logger.debug(f"Extracting content from URL: {input_path}")
        content = extract_text_from_url(input_path)
    else:
        logger.debug(f"Reading content from file: {input_path}")
        content = read_file_content(input_path)

    if content is None:
        logger.error("Failed to extract document content")
        sys.exit(1)

    return content


def log_cost_information(usage):
    """Log cost information based on API usage."""
    # Anthropic pricing for Claude models (as of recent pricing)
    # These are approximate rates - check current Anthropic pricing for exact values
    pricing = {
        "claude-opus-4-0": {
            "input": 0.000015,
            "output": 0.000075,
        },  # $15/$75 per MTok
        "claude-sonnet-4-0": {
            "input": 0.000003,
            "output": 0.000015,
        },  # $3/$15 per MTok
        "claude-3-7-sonnet-latest": {
            "input": 0.000003,
            "output": 0.000015,
        },  # $3/$15 per MTok
        "claude-3-5-haiku-latest": {
            "input": 0.00000080,
            "output": 0.000004,
        },  # $0.80/$4 per MTok
        "claude-3-opus-latest": {
            "input": 0.000015,
            "output": 0.000075,
        },  # $15/$75 per MTok
        # Default fallback pricing (using Sonnet rates)
        "default": {"input": 0.000003, "output": 0.000015},
    }

    model = os.getenv("MODEL", "claude-sonnet-4-0")
    rates = pricing.get(model, pricing["default"])

    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens

    input_cost = input_tokens * rates["input"]
    output_cost = output_tokens * rates["output"]
    total_cost = input_cost + output_cost

    print("\n" + "="*50)
    print("ANTHROPIC API COST INFORMATION")
    print("="*50)
    print(f"Model: {model}")
    print(f"Input tokens: {input_tokens:,}")
    print(f"Output tokens: {output_tokens:,}")
    print(f"Total tokens: {input_tokens + output_tokens:,}")
    print(f"Input cost: ${input_cost:.6f}")
    print(f"Output cost: ${output_cost:.6f}")
    print(f"Total cost: ${total_cost:.6f}")
    print("="*50)


def analyze_document(tags, document_path, track_cost=False):
    """Analyze a document with the given tags."""
    # load template environment
    jinja = Environment(
        loader=FileSystemLoader("prompts"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    tag_list_template = jinja.get_template("tag-list.txt")
    tagging_template = jinja.get_template("summary-tagging.txt")

    # Get document content
    document_content = get_document_content(document_path)

    # Generate tag list prompt
    if tags:
        tag_list_prompt = tag_list_template.render(
            tag_list=", ".join(tags)
        )
    else:
        tag_list_prompt = "No existing tags are provided. Please suggest tags based on the document content."

    # Generate final prompt
    tagging_prompt = tagging_template.render(
        tag_list_prompt=tag_list_prompt,
        document_content=document_content
    )

    # print(tagging_prompt)
    # Call Anthropic API
    model = os.getenv("MODEL", "claude-sonnet-4-0")
    logger.debug(f"using model: {model}")

    client = anthropic.Anthropic()

    message = client.messages.create(
        model=model,
        max_tokens=20000,
        temperature=1,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": tagging_prompt}],
            }
        ],
    )
    print(message.content[0].text)

    if track_cost:
        return message.usage
    return None


def main():
    load_dotenv()

    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="Analyze documents with AI-powered summarization and tagging"
    )
    parser.add_argument(
        "document",
        help="URL or file path of the document to analyze"
    )
    parser.add_argument(
        "--tags",
        help="Comma-separated list of tags to use for analysis",
        default=""
    )
    parser.add_argument(
        "--cost",
        action="store_true",
        help="Log Anthropic API cost information at the end"
    )

    args = parser.parse_args()

    # Parse tags
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()] if args.tags else []

    # Analyze document
    usage = analyze_document(tags, args.document, track_cost=args.cost)

    if args.cost and usage:
        log_cost_information(usage)


if __name__ == "__main__":
    main()
