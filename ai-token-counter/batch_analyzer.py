#!/usr/bin/env python3
"""
AI Token Batch Analyzer — analyze multiple files/prompts at once.
Built by Jackson Studio | jacksonlee71.gumroad.com
"""

import sys
import re
import argparse
import json
from pathlib import Path

# Pricing per 1K tokens (input) as of 2025 — update if needed
MODELS = {
    "gpt-4o":            {"price_per_1k": 0.0025,  "label": "GPT-4o"},
    "gpt-3.5-turbo":     {"price_per_1k": 0.0005,  "label": "GPT-3.5 Turbo"},
    "claude-3-5-sonnet": {"price_per_1k": 0.003,   "label": "Claude 3.5 Sonnet"},
    "claude-3-haiku":    {"price_per_1k": 0.00025, "label": "Claude 3 Haiku"},
    "gemini-1-5-pro":    {"price_per_1k": 0.00125, "label": "Gemini 1.5 Pro"},
    "gemini-1-5-flash":  {"price_per_1k": 0.000075,"label": "Gemini 1.5 Flash"},
}


def estimate_tokens(text: str) -> int:
    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff' or
              '\uac00' <= c <= '\ud7af' or '\u3040' <= c <= '\u30ff')
    remaining = len(text) - cjk
    return max(1, cjk + (remaining // 4))


def analyze_file(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"file": str(path), "error": str(e)}

    tokens = estimate_tokens(text)
    result = {
        "file": str(path),
        "chars": len(text),
        "words": len(re.findall(r'\S+', text)),
        "tokens": tokens,
        "costs": {}
    }
    for key, info in MODELS.items():
        result["costs"][info["label"]] = round((tokens / 1000) * info["price_per_1k"], 6)
    return result


def print_table(results: list, totals: bool = True):
    print(f"\n{'='*70}")
    print(f"  AI Token Batch Analyzer — {len(results)} file(s)")
    print(f"{'='*70}")
    header = f"  {'File':<30} {'Tokens':>8} {'GPT-4o':>10} {'Claude 3.5':>12}"
    print(header)
    print(f"  {'-'*62}")

    total_tokens = 0
    total_gpt4o = 0.0
    total_claude = 0.0

    for r in results:
        if "error" in r:
            print(f"  {'ERROR: ' + r['file']:<30}")
            continue
        fname = Path(r["file"]).name
        tokens = r["tokens"]
        gpt4o = r["costs"].get("GPT-4o", 0)
        claude = r["costs"].get("Claude 3.5 Sonnet", 0)
        print(f"  {fname:<30} {tokens:>8,} {f'${gpt4o:.5f}':>10} {f'${claude:.5f}':>12}")
        total_tokens += tokens
        total_gpt4o += gpt4o
        total_claude += claude

    if totals and len(results) > 1:
        print(f"  {'─'*62}")
        print(f"  {'TOTAL':<30} {total_tokens:>8,} {f'${total_gpt4o:.4f}':>10} {f'${total_claude:.4f}':>12}")

    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Batch-analyze multiple files for token count and API cost.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python batch_analyzer.py *.txt
  python batch_analyzer.py prompts/ --glob "**/*.md"
  python batch_analyzer.py file1.txt file2.py --json
        """
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to analyze")
    parser.add_argument("--glob", default="*", help="Glob pattern when a directory is given (default: *)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-totals", action="store_true", help="Skip totals row")

    args = parser.parse_args()

    if not args.paths:
        parser.print_help()
        sys.exit(0)

    files: list[Path] = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(path.glob(args.glob)))
        elif path.exists():
            files.append(path)
        else:
            print(f"Warning: '{p}' not found, skipping.", file=sys.stderr)

    if not files:
        print("No files found.", file=sys.stderr)
        sys.exit(1)

    results = [analyze_file(f) for f in files]

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_table(results, totals=not args.no_totals)


if __name__ == "__main__":
    main()
