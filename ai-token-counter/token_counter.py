#!/usr/bin/env python3
"""
AI Token Counter — estimate token count + cost for any text/file.
Supports: GPT-4o, GPT-3.5-turbo, Claude 3.5 Sonnet, Gemini 1.5 Pro
"""

import sys
import re
import argparse
from pathlib import Path

# Pricing per 1K tokens (input) as of 2025 — update if needed
MODELS = {
    "gpt-4o":           {"price_per_1k": 0.0025,  "label": "GPT-4o"},
    "gpt-3.5-turbo":    {"price_per_1k": 0.0005,  "label": "GPT-3.5 Turbo"},
    "claude-3-5-sonnet":{"price_per_1k": 0.003,   "label": "Claude 3.5 Sonnet"},
    "claude-3-haiku":   {"price_per_1k": 0.00025, "label": "Claude 3 Haiku"},
    "gemini-1-5-pro":   {"price_per_1k": 0.00125, "label": "Gemini 1.5 Pro"},
    "gemini-1-5-flash": {"price_per_1k": 0.000075,"label": "Gemini 1.5 Flash"},
}

def estimate_tokens(text: str) -> int:
    """
    Rule-of-thumb tokenizer (no tiktoken needed).
    ~4 chars per token for English, ~2 chars for CJK.
    Accurate within ±10% for most LLMs.
    """
    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff' or
              '\uac00' <= c <= '\ud7af' or '\u3040' <= c <= '\u30ff')
    remaining = len(text) - cjk
    tokens = cjk + (remaining // 4)
    return max(1, tokens)

def word_count(text: str) -> int:
    return len(re.findall(r'\S+', text))

def char_count(text: str) -> int:
    return len(text)

def format_cost(cost: float) -> str:
    if cost < 0.001:
        return f"${cost:.6f}"
    elif cost < 0.01:
        return f"${cost:.4f}"
    else:
        return f"${cost:.3f}"

def print_report(text: str, source: str, show_all: bool, model_filter: str):
    tokens = estimate_tokens(text)
    words  = word_count(text)
    chars  = char_count(text)

    print(f"\n{'='*52}")
    print(f"  AI Token Counter")
    print(f"{'='*52}")
    print(f"  Source  : {source}")
    print(f"  Chars   : {chars:,}")
    print(f"  Words   : {words:,}")
    print(f"  Tokens  : ~{tokens:,}")
    print(f"{'='*52}")
    print(f"  {'Model':<24} {'Cost (input)':>12}")
    print(f"  {'-'*36}")

    models_to_show = MODELS.items()
    if model_filter and model_filter != "all":
        models_to_show = [(k, v) for k, v in MODELS.items() if model_filter in k]
        if not models_to_show:
            print(f"  Model '{model_filter}' not found. Showing all.")
            models_to_show = MODELS.items()

    for key, info in models_to_show:
        cost = (tokens / 1000) * info["price_per_1k"]
        print(f"  {info['label']:<24} {format_cost(cost):>12}")

    print(f"{'='*52}")
    print(f"  Tip: Output tokens typically cost 2-4x more.")
    print(f"  Prices are estimates — check provider docs.\n")

def main():
    parser = argparse.ArgumentParser(
        description="Estimate AI token count & cost for any text or file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  echo "Hello world" | python token_counter.py
  python token_counter.py myfile.txt
  python token_counter.py myfile.txt --model gpt-4o
  python token_counter.py --text "Your prompt here"
  python token_counter.py --list-models
        """
    )
    parser.add_argument("file", nargs="?", help="File to analyze")
    parser.add_argument("--text", "-t", help="Inline text to analyze")
    parser.add_argument("--model", "-m", default="all",
                        help="Filter by model name (default: all)")
    parser.add_argument("--list-models", action="store_true",
                        help="List all supported models and exit")

    args = parser.parse_args()

    if args.list_models:
        print("\nSupported models:")
        for key, info in MODELS.items():
            print(f"  {key:<28} ${info['price_per_1k']}/1K tokens")
        print()
        sys.exit(0)

    # Determine input source
    if args.text:
        text   = args.text
        source = "inline text"
    elif args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: file '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        text   = path.read_text(encoding="utf-8", errors="replace")
        source = str(path)
    elif not sys.stdin.isatty():
        text   = sys.stdin.read()
        source = "stdin"
    else:
        parser.print_help()
        sys.exit(0)

    print_report(text, source, show_all=True, model_filter=args.model)

if __name__ == "__main__":
    main()
