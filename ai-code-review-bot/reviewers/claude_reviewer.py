#!/usr/bin/env python3
"""
AI Code Review Bot - Claude Integration
Built by Jackson Studio
"""

import os
import sys
import json
import time
from typing import List, Dict, Optional
from anthropic import Anthropic
import requests

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO_NAME = os.getenv("REPO_NAME")
BASE_SHA = os.getenv("BASE_SHA")
HEAD_SHA = os.getenv("HEAD_SHA")
REVIEW_FOCUS = os.getenv("REVIEW_FOCUS", "security,performance,readability").split(",")
MAX_FILES = int(os.getenv("MAX_FILES", "20"))
COST_LIMIT = float(os.getenv("COST_LIMIT", "0.10"))

# API clients
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Pricing (as of Feb 2026, adjust if needed)
INPUT_PRICE_PER_MTK = 0.003  # $3 per million tokens
OUTPUT_PRICE_PER_MTK = 0.015  # $15 per million tokens


def get_pr_diff() -> Optional[str]:
    """Fetch PR diff from GitHub API"""
    url = f"https://api.github.com/repos/{REPO_NAME}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR: {response.status_code}")
        return None
    
    return response.text


def get_pr_files() -> List[Dict]:
    """Get list of changed files"""
    url = f"https://api.github.com/repos/{REPO_NAME}/pulls/{PR_NUMBER}/files"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching files: {response.status_code}")
        return []
    
    return response.json()


def should_skip_file(filename: str) -> bool:
    """Check if file should be skipped"""
    skip_patterns = [
        ".generated.", "dist/", "build/", "vendor/",
        "package-lock.json", "yarn.lock", "Pipfile.lock",
        ".min.js", ".min.css"
    ]
    return any(pattern in filename for pattern in skip_patterns)


def build_review_prompt(diff: str, files: List[Dict]) -> str:
    """Build prompt for Claude"""
    file_list = "\n".join([f"- {f['filename']} (+{f['additions']} -{f['deletions']})" 
                            for f in files[:10]])
    
    focus_areas = ", ".join(REVIEW_FOCUS)
    
    return f"""You are an expert code reviewer. Review this pull request focusing on: {focus_areas}.

**Files Changed:**
{file_list}

**Full Diff:**
```diff
{diff[:15000]}  # Limit diff size
```

**Instructions:**
1. Identify critical issues (security, bugs, breaking changes)
2. Suggest improvements (performance, readability, maintainability)
3. Note good practices
4. Be specific: cite line numbers and explain WHY
5. Be concise: developers are busy
6. If no issues, say "LGTM" and highlight what's good

**Format your response as:**
### 🔴 Critical Issues
(if any)

### 🟡 Improvements
(if any)

### ✅ Good Practices
(what was done well)

Be direct and actionable. No fluff.
"""


def review_with_claude(prompt: str) -> tuple[str, float]:
    """Get review from Claude, return (review, cost)"""
    start_time = time.time()
    
    try:
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        review_text = response.content[0].text
        
        # Calculate cost
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        cost = (input_tokens / 1_000_000 * INPUT_PRICE_PER_MTK + 
                output_tokens / 1_000_000 * OUTPUT_PRICE_PER_MTK)
        
        elapsed = time.time() - start_time
        
        print(f"Review completed in {elapsed:.1f}s")
        print(f"Tokens: {input_tokens} in, {output_tokens} out")
        print(f"Cost: ${cost:.4f}")
        
        return review_text, cost
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None, 0.0


def post_review_comment(review: str, cost: float, review_time: float):
    """Post review as PR comment"""
    url = f"https://api.github.com/repos/{REPO_NAME}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Format comment
    comment_body = f"""🤖 **AI Code Review** (Claude Sonnet 4.5)

{review}

---
*Review time: {review_time:.0f}s | Cost: ${cost:.3f} | Built by Jackson Studio*
"""
    
    response = requests.post(url, headers=headers, json={"body": comment_body})
    
    if response.status_code == 201:
        print("Review posted successfully")
    else:
        print(f"Error posting comment: {response.status_code}")
        print(response.text)


def main():
    """Main review flow"""
    print("Starting AI code review...")
    
    # Validate environment
    if not all([ANTHROPIC_API_KEY, GITHUB_TOKEN, PR_NUMBER, REPO_NAME]):
        print("Missing required environment variables")
        sys.exit(1)
    
    # Get PR data
    print("Fetching PR diff...")
    diff = get_pr_diff()
    if not diff:
        print("Could not fetch PR diff")
        sys.exit(1)
    
    print("Fetching changed files...")
    files = get_pr_files()
    if not files:
        print("No files changed")
        sys.exit(0)
    
    # Filter files
    reviewable_files = [f for f in files if not should_skip_file(f['filename'])]
    if not reviewable_files:
        print("No reviewable files (all skipped)")
        sys.exit(0)
    
    if len(reviewable_files) > MAX_FILES:
        print(f"Too many files ({len(reviewable_files)}), reviewing first {MAX_FILES}")
        reviewable_files = reviewable_files[:MAX_FILES]
    
    # Build prompt
    print("Building review prompt...")
    prompt = build_review_prompt(diff, reviewable_files)
    
    # Get review
    print("Calling Claude API...")
    start_time = time.time()
    review, cost = review_with_claude(prompt)
    review_time = time.time() - start_time
    
    if not review:
        print("Review failed")
        sys.exit(1)
    
    # Check cost limit
    if cost > COST_LIMIT:
        print(f"Review cost (${cost:.3f}) exceeds limit (${COST_LIMIT})")
        print("Skipping this review. Consider increasing COST_LIMIT.")
        sys.exit(0)
    
    # Post comment
    print("Posting review comment...")
    post_review_comment(review, cost, review_time)
    
    print("Done!")


if __name__ == "__main__":
    main()
