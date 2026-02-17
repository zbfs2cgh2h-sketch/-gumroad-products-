"""
Auto-update checker (GitHub releases)
Built by Jackson Studio
"""

import os
import json
import time
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error
from packaging import version


CACHE_FILE = Path.home() / ".cache" / "cli-update-check.json"
CACHE_TTL = 86400  # 24 hours


def check_for_updates(current_version: str, repo: str) -> Optional[str]:
    """
    Check for new releases on GitHub (non-blocking, cached)
    
    Args:
        current_version: Current version (e.g., "1.2.3")
        repo: GitHub repo (e.g., "jackson-studio/my-tool")
    
    Returns:
        Latest version if newer available, else None
    """
    
    # Check cache
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            cache = json.load(f)
            if time.time() - cache.get("timestamp", 0) < CACHE_TTL:
                # Cache is fresh
                latest = cache.get("latest_version")
                if latest and version.parse(latest) > version.parse(current_version):
                    print(f"\n🔔 New version {latest} available! Run: pip install --upgrade {repo.split('/')[-1]}\n")
                return None
    
    # Fetch latest release
    try:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        req = urllib.request.Request(url, headers={"User-Agent": "Python-CLI-Framework"})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            latest_version = data.get("tag_name", "").lstrip("v")
            
            # Update cache
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CACHE_FILE, "w") as f:
                json.dump({"timestamp": time.time(), "latest_version": latest_version}, f)
            
            # Notify if newer
            if version.parse(latest_version) > version.parse(current_version):
                print(f"\n🔔 New version {latest_version} available! Run: pip install --upgrade {repo.split('/')[-1]}\n")
                return latest_version
    
    except (urllib.error.URLError, json.JSONDecodeError, Exception):
        # Silent fail (don't block CLI)
        pass
    
    return None
