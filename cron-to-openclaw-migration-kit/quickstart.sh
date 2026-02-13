#!/bin/bash
# Quick Start Guide - Cron-to-OpenClaw Migration Kit

set -e

echo "🚀 Cron-to-OpenClaw Migration Kit - Quick Start"
echo "Built by Jackson Studio"
echo ""

# Check dependencies
echo "📋 Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw is required but not installed."
    echo "Visit: https://openclaw.ai"
    exit 1
fi

echo "✅ All dependencies found"
echo ""

# Run tests
echo "🧪 Running tests..."
python3 tests/test_migrate.py
echo "✅ All tests passed"
echo ""

# Demo migration
echo "📝 Demo: Converting example crontab..."
echo ""

cat examples/sample_crontab | python3 migrate_cron.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Quick start complete!"
echo ""
echo "Next steps:"
echo "1. Test with your crontab:"
echo "   crontab -l | python3 migrate_cron.py"
echo ""
echo "2. Generate installation script:"
echo "   crontab -l | python3 migrate_cron.py --script > install.sh"
echo "   chmod +x install.sh"
echo "   ./install.sh"
echo ""
echo "3. Read full docs: README.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
