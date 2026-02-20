#!/usr/bin/env python3
"""
AI Model Cost Report Generator — generate a Markdown/CSV cost comparison report.
Built by Jackson Studio | jacksonlee71.gumroad.com
"""

import sys
import re
import argparse
import csv
import io
from datetime import datetime


MODELS = {
    "gpt-4o":            {"price_in": 0.0025,  "price_out": 0.010,  "label": "GPT-4o",           "provider": "OpenAI"},
    "gpt-4o-mini":       {"price_in": 0.00015, "price_out": 0.0006, "label": "GPT-4o Mini",       "provider": "OpenAI"},
    "gpt-3.5-turbo":     {"price_in": 0.0005,  "price_out": 0.0015, "label": "GPT-3.5 Turbo",     "provider": "OpenAI"},
    "claude-3-5-sonnet": {"price_in": 0.003,   "price_out": 0.015,  "label": "Claude 3.5 Sonnet", "provider": "Anthropic"},
    "claude-3-haiku":    {"price_in": 0.00025, "price_out": 0.00125,"label": "Claude 3 Haiku",    "provider": "Anthropic"},
    "gemini-1-5-pro":    {"price_in": 0.00125, "price_out": 0.005,  "label": "Gemini 1.5 Pro",    "provider": "Google"},
    "gemini-1-5-flash":  {"price_in": 0.000075,"price_out": 0.0003, "label": "Gemini 1.5 Flash",  "provider": "Google"},
    "gemini-2-flash":    {"price_in": 0.0001,  "price_out": 0.0004, "label": "Gemini 2.0 Flash",  "provider": "Google"},
}


def estimate_tokens(text: str) -> int:
    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff' or
              '\uac00' <= c <= '\ud7af' or '\u3040' <= c <= '\u30ff')
    return max(1, cjk + (len(text) - cjk) // 4)


def generate_markdown(text: str, source: str, output_ratio: float) -> str:
    tokens_in = estimate_tokens(text)
    tokens_out = int(tokens_in * output_ratio)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        f"# AI Model Cost Report",
        f"",
        f"**Generated:** {now}  ",
        f"**Source:** {source}  ",
        f"**Input tokens (est.):** {tokens_in:,}  ",
        f"**Output tokens (est.):** {tokens_out:,} ({output_ratio:.1f}x input)  ",
        f"",
        f"| Provider | Model | Input cost | Output cost | Total |",
        f"|----------|-------|-----------|-------------|-------|",
    ]

    rows = []
    for key, m in MODELS.items():
        cost_in  = (tokens_in  / 1000) * m["price_in"]
        cost_out = (tokens_out / 1000) * m["price_out"]
        total    = cost_in + cost_out
        rows.append((total, m["provider"], m["label"], cost_in, cost_out, total))

    rows.sort(key=lambda x: x[0])  # cheapest first

    for _, provider, label, cost_in, cost_out, total in rows:
        lines.append(f"| {provider} | {label} | ${cost_in:.5f} | ${cost_out:.5f} | **${total:.5f}** |")

    lines += [
        f"",
        f"> Prices per 1K tokens (input). Output pricing varies — check provider docs.",
        f"> Built by Jackson Studio | jacksonlee71.gumroad.com",
    ]
    return "\n".join(lines)


def generate_csv(text: str, source: str, output_ratio: float) -> str:
    tokens_in = estimate_tokens(text)
    tokens_out = int(tokens_in * output_ratio)
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["provider", "model", "input_tokens", "output_tokens",
                     "input_cost_usd", "output_cost_usd", "total_cost_usd"])
    for key, m in MODELS.items():
        cost_in  = round((tokens_in  / 1000) * m["price_in"],  6)
        cost_out = round((tokens_out / 1000) * m["price_out"], 6)
        writer.writerow([m["provider"], m["label"], tokens_in, tokens_out,
                         cost_in, cost_out, round(cost_in + cost_out, 6)])
    return buf.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description="Generate a cost comparison report for LLM models.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cat prompt.txt | python model_report.py
  python model_report.py prompt.txt --format csv --output costs.csv
  python model_report.py prompt.txt --output-ratio 2.0
        """
    )
    parser.add_argument("file", nargs="?", help="Input file (default: stdin)")
    parser.add_argument("--text", "-t", help="Inline text")
    parser.add_argument("--format", choices=["markdown", "csv"], default="markdown",
                        help="Output format (default: markdown)")
    parser.add_argument("--output", "-o", help="Write report to file instead of stdout")
    parser.add_argument("--output-ratio", type=float, default=1.0,
                        help="Estimated output/input token ratio (default: 1.0)")

    args = parser.parse_args()

    if args.text:
        text, source = args.text, "inline text"
    elif args.file:
        from pathlib import Path
        p = Path(args.file)
        if not p.exists():
            print(f"Error: '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        text, source = p.read_text(encoding="utf-8", errors="replace"), str(p)
    elif not sys.stdin.isatty():
        text, source = sys.stdin.read(), "stdin"
    else:
        parser.print_help()
        sys.exit(0)

    if args.format == "csv":
        report = generate_csv(text, source, args.output_ratio)
    else:
        report = generate_markdown(text, source, args.output_ratio)

    if args.output:
        from pathlib import Path
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
