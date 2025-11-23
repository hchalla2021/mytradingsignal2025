#!/bin/bash
# Render.com Build Script

echo "🚀 Starting Render.com build..."

# Backend build
echo "📦 Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "✅ Backend ready!"
echo "Backend will start with: uvicorn main:app --host 0.0.0.0 --port \$PORT"
