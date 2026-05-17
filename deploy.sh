#!/bin/bash
# deploy.sh - Quick deployment script for Railway
# Run: bash deploy.sh

set -e

echo "======================================================================"
echo "Aviation Intelligence Platform - Railway Deployment"
echo "======================================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo "   Please create .env with your API keys before deploying."
    echo "   Copy from .env.example and fill in your keys."
    exit 1
fi

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git repository already exists"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo ""
    echo "📝 Uncommitted changes detected. Committing..."
    git add .
    git commit -m "Aviation Intelligence Platform - Ready for deployment

- Fixed f-string syntax error in cesium_map.py
- Integrated accuracy improvements (holidays, fog alerts, live traffic)
- Enhanced ML model with new features for retraining
- Added comprehensive documentation and guides"
    echo "✅ Changes committed"
fi

# Check if remote is set
if ! git remote | grep -q origin; then
    echo ""
    echo "🌐 No remote repository found."
    echo ""
    read -p "   Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " REPO_URL

    if [ -z "$REPO_URL" ]; then
        echo "❌ No repository URL provided. Exiting."
        exit 1
    fi

    git remote add origin "$REPO_URL"
    echo "✅ Remote added: $REPO_URL"
else
    echo "✅ Remote repository already configured"
fi

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# Push to remote
echo ""
echo "🚀 Pushing to GitHub..."
if git push -u origin "$BRANCH"; then
    echo "✅ Code pushed to GitHub successfully!"
else
    echo ""
    echo "⚠️  Push failed. You may need to:"
    echo "   1. Create the repository on GitHub first"
    echo "   2. Run: git push -u origin $BRANCH --force (if you're sure)"
    exit 1
fi

echo ""
echo "======================================================================"
echo "✅ Git deployment complete!"
echo "======================================================================"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Go to https://railway.app/new"
echo "2. Click 'Deploy from GitHub repo'"
echo "3. Select your repository"
echo "4. Add these environment variables in Railway dashboard:"
echo ""
echo "   Required:"
echo "   - AIRLABS_API_KEY"
echo "   - MAPBOX_TOKEN"
echo ""
echo "   Recommended:"
echo "   - CHECKWX_API_KEY"
echo ""
echo "   Optional:"
echo "   - CESIUM_TOKEN"
echo ""
echo "5. Click 'Deploy' and wait 2-3 minutes"
echo "6. Railway will generate your live URL!"
echo ""
echo "======================================================================"
echo "🎉 Your Aviation Intelligence Platform will be live soon!"
echo "======================================================================"
