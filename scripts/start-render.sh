#!/bin/bash
# Render Start Script

set -e

echo "🚀 Starting FastAPI application..."
echo "📍 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"

# Change to backend directory and set Python path
cd backend

# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo "📂 Backend directory: $(pwd)"
echo "🔍 Files in directory:"
ls -la

# Start gunicorn
echo "🌐 Starting gunicorn on 0.0.0.0:$PORT"
exec gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
