#!/bin/bash
# Render.com Build Script

set -e  # Exit on error

echo "🚀 Starting Render.com build..."

# Verify Python version
echo "🐍 Python version check:"
python --version

if python --version 2>&1 | grep -q "Python 3.13"; then
    echo "❌ ERROR: Python 3.13 detected but 3.11 required!"
    echo "Please set Python version to 3.11 in Render dashboard:"
    echo "  Settings > Environment > Python Version > 3.11"
    exit 1
fi

# Ensure we're using Python 3.11
if ! python --version 2>&1 | grep -q "Python 3.11"; then
    echo "⚠️  WARNING: Expected Python 3.11 but got:"
    python --version
fi

# Upgrade pip and setuptools to latest versions
echo "📦 Upgrading build tools..."
pip install --upgrade pip setuptools wheel

# Install backend dependencies with verbose output
echo "📦 Installing backend dependencies..."
pip install --no-cache-dir -r backend/requirements.txt

echo "✅ Backend build complete!"
echo "🔍 Installed packages:"
pip list | grep -E "pandas|numpy|fastapi|uvicorn|gunicorn|kiteconnect"
