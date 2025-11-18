#!/bin/bash
# TreeType Deployment Script - Clean gh-pages Method (v4 - Fixed)

set -e

echo "🚀 TreeType Deployment Script"
echo "=============================="

# Safety checks
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then 
    echo "⚠️  Must be on main branch to deploy."
    exit 1
fi

if [[ -n $(git status --porcelain) ]]; then 
    echo "⚠️  Uncommitted changes found. Please commit or stash."
    git status --short
    exit 1
fi

# Run tests with visible output
echo "🧪 Running tests..."
if ! pnpm run test; then
    echo "❌ Tests failed! Fix errors before deploying."
    exit 1
fi
echo "   ✅ Tests passed"

# Type check with visible output
echo "📝 Type checking..."
if ! pnpm run type-check; then
    echo "❌ Type errors found! Fix errors before deploying."
    exit 1
fi
echo "   ✅ No type errors"

# Build
echo "📦 Building production bundle..."
if ! pnpm run build; then
    echo "❌ Build failed!"
    exit 1
fi

# Create temporary directory for build output
TMP_DIR=$(mktemp -d)
cp -r dist/* "$TMP_DIR"
echo "   ✅ Build artifacts saved to temporary location"

echo "🌿 Preparing gh-pages branch..."
# Fetch latest branches
git fetch origin

# Checkout gh-pages (create if doesn't exist)
if git rev-parse --verify origin/gh-pages > /dev/null 2>&1; then
    git checkout gh-pages
    git pull origin gh-pages
else
    git checkout --orphan gh-pages
fi

# Clean working directory
git rm -rf . 2>/dev/null || true

# Copy build files from temporary directory
cp -r "$TMP_DIR"/* .
touch .nojekyll  # Tell GitHub Pages not to use Jekyll

# Clean up temporary directory
rm -rf "$TMP_DIR"

echo "📦 Files copied to gh-pages branch"

# Commit and push
git add .
if git diff --staged --quiet; then
    echo "ℹ️  No changes to deploy"
else
    git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "⬆️  Pushing to GitHub..."
    git push origin gh-pages
    echo "✅ Deployment successful!"
fi

# Return to main
git checkout main
echo "↩️  Switched back to main branch"
echo ""
echo "🌍 Your site will be live at: https://akbargherbal.github.io/treetype/"
echo "   (Usually takes 30-60 seconds for first deployment)"