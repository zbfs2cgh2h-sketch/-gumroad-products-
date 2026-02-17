#!/usr/bin/env python3
"""
AI Code Review Bot
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
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
PR_NUMBER = os.environ.get("PR_NUMBER")
REPO_OWNER = os.environ.get("REPO_OWNER")
REPO_NAME = os.environ.get("REPO_NAME")
REVIEW_DEPTH = os.environ.get("REVIEW_DEPTH", "balanced")
MODEL = os.environ.get("MODEL", "claude-sonnet-4")
MAX_FILES = int(os.environ.get("MAX_FILES", "10"))
LANGUAGE = os.environ.get("LANGUAGE", "en")

# Validation
if not ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not set")
    sys.exit(1)

if not GITHUB_TOKEN:
    print("❌ GITHUB_TOKEN not set")
    sys.exit(1)

# Initialize clients
anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
github_api = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

def get_pr_diff() -> str:
    """Fetch PR diff from GitHub API"""
    url = f"{github_api}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def get_pr_details() -> Dict:
    """Fetch PR metadata"""
    url = f"{github_api}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_pr_files() -> List[Dict]:
    """Get list of changed files"""
    url = f"{github_api}/pulls/{PR_NUMBER}/files"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def post_review_comment(body: str, commit_id: str, path: str = None, line: int = None):
    """Post review comment to PR"""
    url = f"{github_api}/pulls/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "body": body,
        "commit_id": commit_id,
    }
    
    if path and line:
        data["path"] = path
        data["line"] = line
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 422:
        # Line might not be in diff, post as general comment instead
        post_general_comment(body)
    else:
        response.raise_for_status()

def post_general_comment(body: str):
    """Post general comment to PR"""
    url = f"{github_api}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {"body": body}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

def build_review_prompt(pr_details: Dict, diff: str, files: List[Dict]) -> str:
    """Build context-aware review prompt"""
    
    depth_instructions = {
        "quick": "Focus only on critical bugs, security issues, and obvious errors.",
        "balanced": "Review for bugs, security, performance issues, and code quality.",
        "deep": "Perform thorough review including: bugs, security, performance, maintainability, best practices, and architectural concerns."
    }
    
    language_instructions = {
        "en": "Reply in English.",
        "ko": "한국어로 답변하세요.",
        "es": "Responde en español.",
        "fr": "Répondez en français.",
        "de": "Antworten Sie auf Deutsch."
    }
    
    file_list = "\n".join([f"- {f['filename']} (+{f['additions']} -{f['deletions']})" for f in files[:20]])
    
    prompt = f"""You are an expert code reviewer. Review this pull request.

## PR Context
**Title:** {pr_details['title']}
**Description:** {pr_details.get('body', 'No description provided')}

## Changed Files
{file_list}

## Review Instructions
{depth_instructions.get(REVIEW_DEPTH, depth_instructions['balanced'])}

Focus on:
1. **Security** (injection, XSS, secrets, auth)
2. **Bugs** (null refs, off-by-one, race conditions)
3. **Performance** (N+1, memory leaks, inefficient algorithms)
4. **Code Quality** (naming, complexity, duplication)
5. **Best Practices** (error handling, type safety)

## Diff
```diff
{diff[:8000]}  # Truncate to avoid token limits
```

## Output Format
Provide a structured JSON response:

```json
{{
  "summary": "Brief overall assessment",
  "severity": "low|medium|high",
  "issues": [
    {{
      "file": "path/to/file.py",
      "line": 42,
      "severity": "medium",
      "category": "performance",
      "message": "Specific issue description",
      "suggestion": "How to fix it"
    }}
  ],
  "positives": ["Things done well"]
}}
```

{language_instructions.get(LANGUAGE, language_instructions['en'])}
"""
    
    return prompt

def review_with_claude(prompt: str) -> Dict:
    """Send review request to Claude"""
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            response = anthropic.messages.create(
                model=MODEL,
                max_tokens=4096,
                temperature=0.3,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            content = response.content[0].text
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except anthropic.RateLimitError:
            if attempt < max_retries - 1:
                print(f"⏳ Rate limited, retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse JSON response: {e}")
            print(f"Raw response: {content[:500]}")
            # Return minimal valid structure
            return {
                "summary": "Review completed but response parsing failed",
                "severity": "unknown",
                "issues": [],
                "positives": []
            }

def format_review_comment(review: Dict) -> str:
    """Format review as markdown comment"""
    
    severity_emoji = {
        "low": "✅",
        "medium": "⚠️",
        "high": "🚨",
        "unknown": "❓"
    }
    
    comment = f"""## 🤖 AI Code Review
    
{severity_emoji.get(review['severity'], '❓')} **Overall: {review['severity'].upper()}**

{review['summary']}

"""
    
    if review.get('issues'):
        comment += "\n### Issues Found\n\n"
        for issue in review['issues']:
            icon = {"low": "ℹ️", "medium": "⚠️", "high": "🚨"}.get(issue['severity'], "•")
            comment += f"{icon} **{issue['category'].title()}** in `{issue['file']}`"
            if issue.get('line'):
                comment += f" (line {issue['line']})"
            comment += f"\n   {issue['message']}\n"
            if issue.get('suggestion'):
                comment += f"   💡 {issue['suggestion']}\n"
            comment += "\n"
    
    if review.get('positives'):
        comment += "\n### ✨ What's Good\n\n"
        for positive in review['positives']:
            comment += f"- {positive}\n"
    
    comment += "\n---\n*Built by [Jackson Studio](https://jackson.studio) • [Get this bot](https://jackson.gumroad.com/l/ai-review)*"
    
    return comment

def main():
    print("🤖 Starting AI Code Review...")
    
    # Fetch PR data
    print("📥 Fetching PR details...")
    pr_details = get_pr_details()
    files = get_pr_files()
    
    # Check file count limit
    if len(files) > MAX_FILES:
        comment = f"⚠️ This PR changes {len(files)} files (limit: {MAX_FILES}). Skipping automated review.\n\n*Tip: Break large PRs into smaller chunks for better reviews.*"
        post_general_comment(comment)
        print(f"⏭️ Skipped: too many files ({len(files)} > {MAX_FILES})")
        return
    
    print("📥 Fetching diff...")
    diff = get_pr_diff()
    
    # Build prompt
    print("🔨 Building review prompt...")
    prompt = build_review_prompt(pr_details, diff, files)
    
    # Get review from Claude
    print(f"🧠 Requesting review from {MODEL}...")
    review = review_with_claude(prompt)
    
    # Post comment
    print("💬 Posting review...")
    comment = format_review_comment(review)
    commit_id = pr_details['head']['sha']
    
    post_general_comment(comment)
    
    # Post inline comments for specific issues
    for issue in review.get('issues', []):
        if issue.get('file') and issue.get('line'):
            try:
                inline_comment = f"**{issue['category'].title()}:** {issue['message']}"
                if issue.get('suggestion'):
                    inline_comment += f"\n\n💡 **Suggestion:** {issue['suggestion']}"
                
                post_review_comment(
                    body=inline_comment,
                    commit_id=commit_id,
                    path=issue['file'],
                    line=issue['line']
                )
                print(f"  ✅ Posted inline comment on {issue['file']}:{issue['line']}")
            except Exception as e:
                print(f"  ⚠️ Failed to post inline comment: {e}")
    
    print("✅ Review complete!")
    
    # Exit with error if high severity issues found
    if review.get('severity') == 'high':
        print("🚨 High severity issues found")
        sys.exit(1)

if __name__ == "__main__":
    main()
