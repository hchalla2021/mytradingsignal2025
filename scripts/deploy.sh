#!/bin/bash
# Quick Deploy Script for Market Signals

echo "=================================="
echo "  Market Signals - Quick Deploy"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Market Signals Zerodha"
fi

# Menu
echo "Choose deployment platform:"
echo "1) Vercel (Recommended - Fast & Free)"
echo "2) Railway (Backend-friendly)"
echo "3) Render.com (Free tier)"
echo "4) Docker (Local/Cloud)"
echo "5) Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "📦 Deploying to Vercel..."
        echo ""
        if ! command -v vercel &> /dev/null; then
            echo "Installing Vercel CLI..."
            npm i -g vercel
        fi
        echo "Running: vercel --prod"
        vercel --prod
        echo ""
        echo "✅ Deployment complete!"
        echo "⚠️  Don't forget to:"
        echo "   1. Add environment variables in Vercel dashboard"
        echo "   2. Update CORS in backend/main.py"
        ;;
    2)
        echo ""
        echo "🚂 Deploying to Railway..."
        echo ""
        if ! command -v railway &> /dev/null; then
            echo "Installing Railway CLI..."
            npm i -g @railway/cli
        fi
        railway login
        railway init
        railway up
        echo ""
        echo "✅ Deployment complete!"
        echo "⚠️  Add environment variables in Railway dashboard"
        ;;
    3)
        echo ""
        echo "🎨 Deploying to Render.com..."
        echo ""
        echo "Please follow these steps:"
        echo "1. Go to https://render.com/dashboard"
        echo "2. Connect your Git repository"
        echo "3. Create two services:"
        echo "   - Web Service (Backend): uvicorn main:app"
        echo "   - Static Site (Frontend): npm run build"
        echo "4. Add environment variables"
        echo ""
        echo "See DEPLOYMENT.md for detailed instructions"
        ;;
    4)
        echo ""
        echo "🐳 Building Docker containers..."
        echo ""
        docker-compose up --build
        echo ""
        echo "✅ Docker containers running!"
        echo "Backend: http://localhost:8000"
        echo "Frontend: http://localhost:3000"
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

echo ""
echo "=================================="
echo "  Read DEPLOYMENT.md for details"
echo "=================================="
