#!/bin/bash
# Quick installation script
# Usage: curl -fsSL https://raw.githubusercontent.com/jackson-studio/ai-code-review-bot/main/install.sh | bash

set -e

echo "🤖 Installing AI Code Review Bot..."

# Check if running in a git repo
if [ ! -d .git ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Create workflow directory
mkdir -p .github/workflows

# Download workflow file
echo "📥 Downloading workflow file..."
curl -fsSL https://raw.githubusercontent.com/jackson-studio/ai-code-review-bot/main/workflow.yml \
    -o .github/workflows/ai-review.yml

# Download review script
echo "📥 Downloading review script..."
mkdir -p scripts
curl -fsSL https://raw.githubusercontent.com/jackson-studio/ai-code-review-bot/main/scripts/review.py \
    -o scripts/review.py

# Make script executable
chmod +x scripts/review.py

# Download config
echo "📥 Downloading config..."
curl -fsSL https://raw.githubusercontent.com/jackson-studio/ai-code-review-bot/main/config.json \
    -o config.json

# Download requirements
curl -fsSL https://raw.githubusercontent.com/jackson-studio/ai-code-review-bot/main/requirements.txt \
    -o requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Get Anthropic API key: https://console.anthropic.com/"
echo "2. Add GitHub secret: Settings → Secrets → Actions → New secret"
echo "   Name: ANTHROPIC_API_KEY"
echo "   Value: your-api-key"
echo ""
echo "3. Commit and push:"
echo "   git add .github/workflows/ai-review.yml scripts/ config.json requirements.txt"
echo "   git commit -m 'Add AI code review bot'"
echo "   git push"
echo ""
echo "4. Open a PR and watch the magic! 🎉"
echo ""
echo "Built by Jackson Studio — https://jackson.studio"
